LAMBDA_DEFAULT_LOGGER = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'correlation_id': {'()': 'finalsa.common.logger.filter.CorrelationIdFilter'},
    },
    'formatters': {
        'console': {
            'class': 'finalsa.common.logger.CustomJsonFormatter',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['correlation_id'],
            'formatter': 'console',
        },
    },
    'loggers': {
        'root': {'handlers': ['console'], 'level': 'INFO', 'propagate': True},
    },
}
