"""
contains simple mapping of prometheus-appropriate names and metric types to redis metric names

section_name: {
  prometheus_metric_name: {
    "redis_alias": redis_metric_name
    "metric_type": Metric

"""

from prometheus_client.core import CounterMetricFamily, GaugeMetricFamily

METRIC_MAP = {
    "server": {
        "redis_version": {
            "redis_alias": "redis_version",
            "metric_type": None
        },  # 6.0.9

        "redis_git_sha1": {
            "redis_alias": "redis_git_sha1",
            "metric_type": None
        },  # 00000000

        "redis_git_dirty": {
            "redis_alias": "redis_git_dirty",
            "metric_type": None
        },  # 0

        "redis_build_id": {
            "redis_alias": "redis_build_id",
            "metric_type": None
        },  # 285ea3bd83c4efcc

        "redis_mode": {
            "redis_alias": "redis_mode",
            "metric_type": None
        },  # standalone

        "redis_os": {
            "redis_alias": "os",
            "metric_type": None
        },  # Linux 5.4.0-1017-aws x86_64

        "redis_arch_bits": {
            "redis_alias": "arch_bits",
            "metric_type": None
        },  # 64

        "redis_multiplexing_api": {
            "redis_alias": "multiplexing_api",
            "metric_type": None
        },  # epoll

        "redis_gcc_version": {
            "redis_alias": "gcc_version",
            "metric_type": None
        },  # 9.3.0

        "redis_process_id": {
            "redis_alias": "process_id",
            "metric_type": None
        },  # 1413526

        "redis_run_id": {
            "redis_alias": "run_id",
            "metric_type": None
        },  # 0e2ea9fe17094d578b33c4199c74c1785d7c885a

        "redis_tcp_port": {
            "redis_alias": "tcp_port",
            "metric_type": None
        },  # 6379

        "redis_uptime_seconds": {
            "redis_alias": "uptime_in_seconds",
            "metric_type": CounterMetricFamily
        },  # 3302737

        "redis_uptime_days": {
            "redis_alias": "uptime_in_days",
            "metric_type": CounterMetricFamily
        },  # 38

        "redis_hz": {
            "redis_alias": "hz",
            "metric_type": None
        },  # 10

        "redis_lru_clock_min": {
            "redis_alias": "lru_clock",
            "metric_type": CounterMetricFamily
        }  # 13252060
    },

    "clients": {
        "redis_connected_clients": {
            "redis_alias": "connected_clients",
            "metric_type": GaugeMetricFamily,
            "documentation": "Active client connections"
        },  # 3

        "redis_blocked_clients": {
            "redis_alias": "blocked_clients",
            "metric_type": GaugeMetricFamily
        }  # 0
    },

    "memory": {
        "redis_used_memory_bytes": {
            "redis_alias": "used_memory",
            "metric_type": GaugeMetricFamily
        },  # 199981280

        "redis_used_memory_mb": {
            "redis_alias": "used_memory_human",
            "metric_type": None
        },  # 190.72M

        "redis_used_memory_rss": {
            "redis_alias": "used_memory_rss",
            "metric_type": GaugeMetricFamily
        },  # 212561920

        "redis_used_memory_peak_bytes": {
            "redis_alias": "used_memory_peak",
            "metric_type": CounterMetricFamily
        },  # 203398872

        "redis_used_memory_peak_mb": {
            "redis_alias": "used_memory_peak_human",
            "metric_type": None
        },  # 193.98M

        "redis_used_memory_lua": {
            "redis_alias": "used_memory_lua",
            "metric_type": GaugeMetricFamily
        },  # 37888

        "redis_mem_fragmentation_ratio": {
            "redis_alias": "mem_fragmentation_ratio",
            "metric_type": GaugeMetricFamily
        },  # 1.06

        "redis_mem_allocator": {
            "redis_alias": "mem_allocator",
            "metric_type": None
        }  # jemalloc-5.1.0
    },

    "persistence": {
        "redis_loading": {
            "redis_alias": "loading",
            "metric_type": None
        },  # 0

        "redis_rdb_changes_since_last_save": {
            "redis_alias": "rdb_changes_since_last_save",
            "metric_type": CounterMetricFamily
        },  # 10979540

        "redis_rdb_bgsave_in_progress": {
            "redis_alias": "rdb_bgsave_in_progress",
            "metric_type": None
        },  # 0

        "redis_rdb_last_save_time": {
            "redis_alias": "rdb_last_save_time",
            "metric_type": None
        },  # 1603784843

        "redis_rdb_last_bgsave_status": {
            "redis_alias": "rdb_last_bgsave_status",
            "metric_type": None
        },  # ok

        "redis_rdb_last_bgsave_time_sec": {
            "redis_alias": "rdb_last_bgsave_time_sec",
            "metric_type": None
        },  # -1

        "redis_rdb_current_bgsave_time_sec": {
            "redis_alias": "rdb_current_bgsave_time_sec",
            "metric_type": None
        },  # -1

        "redis_aof_enabled": {
            "redis_alias": "aof_enabled",
            "metric_type": None
        },  # 0

        "redis_aof_rewrite_in_progress": {
            "redis_alias": "aof_rewrite_in_progress",
            "metric_type": None
        },  # 0

        "redis_aof_rewrite_scheduled": {
            "redis_alias": "aof_rewrite_scheduled",
            "metric_type": None
        },  # 0

        "redis_aof_last_rewrite_time_sec": {
            "redis_alias": "aof_last_rewrite_time_sec",
            "metric_type": None
        },  # -1

        "redis_aof_current_rewrite_time_sec": {
            "redis_alias": "aof_current_rewrite_time_sec",
            "metric_type": None
        },  # -1

        "redis_aof_last_bgrewrite_status": {
            "redis_alias": "aof_last_bgrewrite_status",
            "metric_type": None
        }  # ok
    },

    "stats": {
        "redis_connections_received_total": {
            "redis_alias": "total_connections_received",
            "metric_type": CounterMetricFamily
        },  # 318271

        "redis_commands_processed_total": {
            "redis_alias": "total_commands_processed",
            "metric_type": CounterMetricFamily
        },  # 26817713

        "redis_instantaneous_ops_per_sec": {
            "redis_alias": "instantaneous_ops_per_sec",
            "metric_type": GaugeMetricFamily
        },  # 41

        "redis_rejected_connections": {
            "redis_alias": "rejected_connections",
            "metric_type": CounterMetricFamily
        },  # 0

        "redis_sync_full": {
            "redis_alias": "sync_full",
            "metric_type": CounterMetricFamily
        },  # 0

        "redis_sync_partial_ok": {
            "redis_alias": "sync_partial_ok",
            "metric_type": CounterMetricFamily
        },  # 0

        "redis_sync_partial_err": {
            "redis_alias": "sync_partial_err",
            "metric_type": CounterMetricFamily
        },  # 0

        "redis_expired_keys": {
            "redis_alias": "expired_keys",
            "metric_type": CounterMetricFamily
        },  # 73423

        "redis_evicted_keys": {
            "redis_alias": "evicted_keys",
            "metric_type": CounterMetricFamily
        },  # 1214638

        "redis_keyspace_hits": {
            "redis_alias": "keyspace_hits",
            "metric_type": CounterMetricFamily
        },  # 6185641

        "redis_keyspace_misses": {
            "redis_alias": "keyspace_misses",
            "metric_type": CounterMetricFamily
        },  # 2884567

        "redis_pubsub_channels": {
            "redis_alias": "pubsub_channels",
            "metric_type": GaugeMetricFamily
        },  # 0

        "redis_pubsub_patterns": {
            "redis_alias": "pubsub_patterns",
            "metric_type": GaugeMetricFamily
        },  # 0

        "redis_latest_fork_usec": {
            "redis_alias": "latest_fork_usec",
            "metric_type": None
        },  # 0

        "redis_migrate_cached_sockets": {
            "redis_alias": "migrate_cached_sockets",
            "metric_type": GaugeMetricFamily
        },  # 0
    },

    "replication": {
        "redis_role": {
            "redis_alias": "role",
            "metric_type": None
        },  # master

        "redis_connected_slaves": {
            "redis_alias": "connected_slaves",
            "metric_type": None
        },  # 0

        "redis_master_repl_offset": {
            "redis_alias": "master_repl_offset",
            "metric_type": None
        },  # 0

        "redis_repl_backlog_active": {
            "redis_alias": "repl_backlog_active",
            "metric_type": None
        },  # 0

        "redis_repl_backlog_size": {
            "redis_alias": "repl_backlog_size",
            "metric_type": None
        },  # 1048576

        "redis_repl_backlog_first_byte_offset": {
            "redis_alias": "repl_backlog_first_byte_offset",
            "metric_type": None
        },  # 0

        "redis_repl_backlog_histlen": {
            "redis_alias": "repl_backlog_histlen",
            "metric_type": None
        }  # 0
    },

    "cpu": {
        "redis_used_cpu_sys": {
            "redis_alias": "used_cpu_sys",
            "metric_type": CounterMetricFamily
        },  # 2319.741921

        "redis_used_cpu_user": {
            "redis_alias": "used_cpu_user",
            "metric_type": CounterMetricFamily
        },  # 20157.177191

        "redis_used_cpu_sys_children": {
            "redis_alias": "used_cpu_sys_children",
            "metric_type": CounterMetricFamily
        },  # 0.000000

        "redis_used_cpu_user_children": {
            "redis_alias": "used_cpu_user_children",
            "metric_type": CounterMetricFamily
        }  # 0.000000
    },

    "cluster": {
        "redis_cluster_enabled": {
            "redis_alias": "cluster_enabled",
            "metric_type": None
        }  # 0
     },

    "keyspace": {
        "redis_keys_per_database_count": {
            "redis_alias": "keys",
            "metric_type": CounterMetricFamily,
            "documentation": "Total number of keys",
            "labels": ["database"]
        },

        "redis_expiring_keys_count": {
            "redis_alias": "expires",
            "metric_type": GaugeMetricFamily,
            "documentation": "Number of expiring keys",
            "labels": ["database"]
        },

        "redis_average_key_ttl_seconds": {
            "redis_alias": "avg_ttl",
            "metric_type": GaugeMetricFamily,
            "documentation": "Average key ttl",
            "labels": ["database"]
        }
    }
}

ALL_SECTIONS = {section for section in METRIC_MAP.keys()}
ALL_METRICS_FLAT = dict()
[ALL_METRICS_FLAT.update(metrics) for section, metrics in METRIC_MAP.items() if section != 'keyspace']
