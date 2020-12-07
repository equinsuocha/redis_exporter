import sys
import yaml
import logging
import redis
import time
from prometheus_client import start_http_server, REGISTRY, PROCESS_COLLECTOR, PLATFORM_COLLECTOR

from .metric_map import METRIC_MAP
from .collector import RedisCollector

LOGGER = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = "/etc/redis_exporter/redis_exporter.yaml"


def write_to_redis_on_startup(host, port, exposed_metrics):
    r = redis.Redis(host=host, port=port, db=0)
    r.set('_redis_exporter_exposed_metrics', ' '.join(exposed_metrics))
    r = redis.Redis(host=host, port=port, db=1)
    r.set('_redis_exporter_exposed_metrics', ' '.join(exposed_metrics))


def load_config_file(path: str = DEFAULT_CONFIG_PATH) -> dict:
    try:
        with open(path, 'r') as f:
            return yaml.load(f, Loader=yaml.SafeLoader)
    except FileNotFoundError:
        return {}


class RedisExporter(object):
    """ configuration manager for RedisCollector """

    def __init__(self, config_path: str):
        """ load and test mandatory config values """
        self._config = load_config_file(path=config_path)
        self._global_options = self._config.get('global', {})
        self._collector_options = self._config.get('collector', {})
        try:
            # doesn't make sense to any set defaults for these:
            self._redis_options = self._config['redis']
            self._redis_host = self._redis_options['host']
            self._redis_port = self._redis_options.get('port', 6379)
        except KeyError:
            raise AttributeError("redis target is not configured; explicitly specify host under redis key")
        self._include_keyspace_metrics = 'keyspace' in self._collector_options.get('sections', [])
        self._exposed_info_metrics = None
        self._collector = None
        self._init_collector()
    
    def _init_collector(self) -> None:
        """ initialize RedisCollector class with respect to config options """
        if not self._collector:
            include_sections = set(self._collector_options.get('sections', []))
            drop_metrics = set(self._collector_options.get('drop', []))
            exposed_info_section_metrics = \
                set().union(*[set(metrics.keys()) for section, metrics in METRIC_MAP.items()
                              if section in include_sections and section not in ('keyspace', 'server')])
            self._exposed_info_metrics = list(exposed_info_section_metrics.difference(drop_metrics))
            self._collector = RedisCollector(host=self._redis_host,
                                             port=self._redis_port,
                                             include_keyspace_metrics=self._include_keyspace_metrics,
                                             exposed_info_metrics=self._exposed_info_metrics)

    def start(self) -> None:
        """
        configure internal python and scrape metrics exposure
        and start http server exposing prometheus metrics
        """
        write_to_redis_on_startup(self._redis_host, self._redis_port, self._exposed_info_metrics)
        REGISTRY.register(self._collector)
        if self._global_options.get('disable_builtin_collectors', False):
            LOGGER.info("Disabling builtin collectors")
            REGISTRY.unregister(PROCESS_COLLECTOR)
            REGISTRY.unregister(PLATFORM_COLLECTOR)
            REGISTRY.unregister(REGISTRY._names_to_collectors['python_gc_objects_collected_total'])

        if self._collector_options.get('disable_scrape_metrics', False):
            LOGGER.info("Disabling scrape metrics")
            REGISTRY.unregister(REGISTRY._names_to_collectors['redis_exporter_failed_scrape_total'])
            REGISTRY.unregister(REGISTRY._names_to_collectors['redis_exporter_successful_scrape_total'])

        start_http_server(self._global_options.get('exporter_port', 9999))
        try:
            while True:
                time.sleep(60)
        except (KeyboardInterrupt, SystemExit):
            LOGGER.info("Exit redis exporter")
            sys.exit()
