LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] # %(levelname)s    # %(message)s'
        },
        'worker': {
            'format': '[%(asctime)s] # %(levelname)s    # [%(process)d] %(message)s'
        },
    },
    'filters': {
        'api_filter': {
            '()': 'utils.logging_filters.APILogsFilter',
        },
        'generic_data_filter': {
            '()': 'utils.logging_filters.GenericDataFilter'
        }
    },
    'handlers': {
        'stdout': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'console': {
            'handlers': ['stdout'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['stdout'],
            'level': 'ERROR',   # only catches 5xx not 4xx messages
            'propagate': True,
        },
        'audio': {
            'handlers': ['stdout'],
            'level': 'INFO',
            'propagate': False,
        },
        'api': {
            'handlers': ['stdout'],
            'level': 'INFO',
            'propagate': False,
        },
        'api_errors': {
            'handlers': ['stdout'],
            'level': 'INFO',
            'propagate': False,
        },
        'web': {
            'handlers': ['stdout'],
            'level': 'INFO',
            'propagate': False,
        },
        'search': {
            'handlers': ['stdout'],
            'level': 'INFO',
            'propagate': False,
        },
        'upload': {
            'handlers': ['stdout'],
            'level': 'INFO',
            'propagate': False,
        },
        'processing': {
            'handlers': ['stdout'],
            'level': 'INFO',
            'propagate': False,
        },
        'gearman_worker_processing': {
            'handlers': ['stdout'],
            'level': 'INFO',
            'propagate': False,
        },    
    },
}
