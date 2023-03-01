from logging.config import dictConfig


def set_dict_config():
    dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'console': {
                'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
            },
            'file': {
                'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'console',
            },

        },
        'loggers': {
            # root logger
            '': {
                'level': 'INFO',
                'handlers': ['console'],
            },
            'stomp.py ': {
                'level': 'WARN',
                'handlers': ['console'],
            },
        },
    })
