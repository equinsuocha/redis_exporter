#### Run redis_exporter and redis instance via docker-compose

    git clone https://github.com/equinsuocha/redis_exporter.git
    cd redis_exporter
    docker-compose build && docker-compose up -d
    
Prometheus exporter will be running in a container,
exposing metrics at http://localhost:9999/metrics in
such a way:

    # HELP redis_connected_clients Active client connections
    # TYPE redis_connected_clients gauge
    redis_connected_clients 1.0
    # HELP redis_keys_per_database_count_total Total number of keys
    # TYPE redis_keys_per_database_count_total counter
    redis_keys_per_database_count_total{database="db0"} 1.0
    redis_keys_per_database_count_total{database="db1"} 1.0
    # HELP redis_expiring_keys_count Number of expiring keys
    # TYPE redis_expiring_keys_count gauge
    redis_expiring_keys_count{database="db0"} 0.0
    redis_expiring_keys_count{database="db1"} 0.0
    # HELP redis_average_key_ttl_seconds Average key ttl
    # TYPE redis_average_key_ttl_seconds gauge
    redis_average_key_ttl_seconds{database="db0"} 0.0
    redis_average_key_ttl_seconds{database="db1"} 0.0

#### Scrape Configuration

exporter configuration is managed by yaml file of the following format:
    
    redis:
      host: localhost
      port: 6379
    global:
      disable_builtin_collectors: True
      exporter_port: 9999
    collector:
      disable_scrape_metrics: False
      sections:
        - clients
        - keyspace
      drop:
        - redis_blocked_clients

where set of mandatory options is limited to:

    redis:
      host: localhost

and defaults are provided to the rest of it.
Configuration file default path is _'/etc/redis_exporter/redis_exporter.yaml'_
Package is provided with redis_exporter executable script which allows to specify alternative
configuration file path under **--config** key 

All data is scraped from a single Redis request, and all unwanted metrics are dropped by the parser.
Set of wanted sections is managed by specifying Redis info sections 
(server, clients, memory, persistence, stats, replication, cpu, cluster, keyspace)
in 'section' list under 'collector' key:

    collector:
      sections:
        - clients
        - keyspace

Then metrics specified in a 'drop' list under 'collector' key are goind to be dropped from it:
    
    collector:
          drop:
            - redis_blocked_clients

Keyspace section does not follow this rule and parsed by a separate parse function.
All available keyspace metrics are included if 'keyspace' section is specified in the 'sections' list.

Metrics parsing is backed by "metric_map.py" containing a mapping of Redis metrics to prometheus-compatible metric names and types.
If 'metric_type' == None, the metric is dropped by parser, since it does not know which prometheus metric type should be used
for a given Redis metric.


#### Sidenote on query performance (why always query all metrics)

First function queries all info section

    def query_info_all():
        r = redis.Redis(host="localhost", port=6379)
        return r.info()
     
        # mean 1 iterations: 0.0028962803599999983
        # mean 10 iterations: 0.027015079450000003
        # mean 100 iterations: 0.33245466103999993
        
        # 1000 iterations:  2.785119376
        # 10000 iterations:  32.412030314000006
        # 100000 iterations:  371.631752054

Second function queries only "stats" section of info.
Query optimisation does not make much difference at expected query rates:

    def query_info_section():
        r = redis.Redis(host="localhost", port=6379)
        return r.info(section="stats")
        
        mean 1 iterations: 0.0029437660400000046
        mean 10 iterations: 0.025255221780000007
        mean 100 iterations: 0.32260823110999987
    
        1000 iterations:  2.6220872500000003
        10000 iterations:  28.180730579
        100000 iterations:  372.834810817