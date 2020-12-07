import logging
import redis
from dataclasses import dataclass, field
from typing import Any, List
from prometheus_client.core import Metric, Counter

from redis_exporter.metric_map import METRIC_MAP, ALL_METRICS_FLAT

LOGGER = logging.getLogger(__name__)

DEFAULT_EXPOSED_METRICS = ["redis_connected_clients", "redis_connections_received_total"]
DEFAULT_DOCUMENTATION = "Metric info is not provided"


@dataclass(frozen=True)
class LabelValueContainer:
    """ a container with value and corresponding tag values usage:

    values = [LabelValueContainer]
    metric = MetricClass(name="somename", documentation="somedoc", labels=["label_tag1", "label_tag2"])

    for value in values:
        metric.add_metric(lables=value.label_values, value=value.value)

    """
    value: Any
    label_values: List[str] = field(default_factory=list)


class RedisCollector(object):
    def __init__(self,
                 host: str,
                 port: int = 6379,
                 include_keyspace_metrics: bool = True,
                 exposed_info_metrics=DEFAULT_EXPOSED_METRICS):
        self.host = host
        self.port = port
        self.include_keyspace_metrics = include_keyspace_metrics
        self.exposed_info_metrics = exposed_info_metrics
        self.scrape_failed = Counter(name="redis_exporter_failed_scrape",
                                     documentation="Redis exporter total failed scrapes")
        self.scrape_succeeded = Counter(name="redis_exporter_successful_scrape",
                                        documentation="Redis exporter total succeeded scrapes")

    def collect(self) -> bool:
        """ function called by Collector on /metrics request """
        info = self.query_redis_info()
        if not info:
            LOGGER.error("Couldn't get metrics from Redis")
            self.scrape_failed.inc(1)
        else:
            LOGGER.debug('Info query result:', info)
            yield from self.parse_info(info)
            if self.include_keyspace_metrics:
                yield from self.parse_keyspace_metrics(info)
            self.scrape_succeeded.inc(1)

    def query_redis_info(self) -> dict:
        try:
            LOGGER.debug('Connecting to Redis %s', self.host)
            r = redis.Redis(host=self.host, port=self.port)
            return r.info()
        except (redis.exceptions.ConnectionError, ConnectionRefusedError):
            LOGGER.error('Redis connection failed')
            return {}

    def parse_info(self, info: dict) -> Metric:
        for metric in self.exposed_info_metrics:
            metric_info = ALL_METRICS_FLAT[metric]
            if metric_info['metric_type'] is None:
                """ drop metric if type is not mapped in metric_map.py """
                LOGGER.debug('drop metric %s, since type is not specified', metric)
                continue
            LOGGER.debug('processing metric %s %s', metric, metric_info)
            value = LabelValueContainer(info.get(metric_info['redis_alias'], None))
            LOGGER.debug('new value: %s', value)
            yield from RedisCollector._create_metric(metric, values=[value], **metric_info)

    @staticmethod
    def parse_keyspace_metrics(info: dict) -> Metric:
        keyspaces = {k for k in info.keys() if k.startswith('db')}
        for metric, metric_info in METRIC_MAP['keyspace'].items():
            LOGGER.debug('processing metric %s %s', metric, metric_info)
            values = []
            for keyspace in keyspaces:
                value = LabelValueContainer(info[keyspace].get(metric_info['redis_alias'], None),
                                            label_values=[keyspace])
                LOGGER.debug('new value: %s', value)
                values.append(value)
            yield from RedisCollector._create_metric(metric, values=values,
                                                     **metric_info)

    @staticmethod
    def _create_metric(name,
                       metric_type: type = None,
                       documentation: str = DEFAULT_DOCUMENTATION,
                       values: list = [],
                       labels: list = [], **_) -> Metric:
        m = metric_type(name, documentation, labels=labels)
        for value in values:
            m.add_metric(labels=value.label_values, value=value.value)
        LOGGER.debug('created metric %s', m)
        yield m
