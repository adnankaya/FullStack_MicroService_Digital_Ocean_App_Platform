import os
import ssl

REDIS_USERNAME = os.environ.get('REDIS_USERNAME')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
REDIS_DB_NUM = os.environ.get('REDIS_DB_NUM', '0')

PARAMS_CELERY = {}
if REDIS_USERNAME and REDIS_PASSWORD:
    # for secure connection use rediss://
    CELERY_BROKER_URL = f'rediss://{REDIS_USERNAME}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NUM}'
    CELERY_RESULT_BACKEND = f'rediss://{REDIS_USERNAME}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NUM}'
    PARAMS_CELERY.update({
        "redbeat_redis_url":CELERY_BROKER_URL,
        "broker_use_ssl":{"ssl_cert_reqs": ssl.CERT_NONE},
        "redis_backend_use_ssl":{"ssl_cert_reqs": ssl.CERT_NONE},
    })
else:
    CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NUM}'
    CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NUM}'

PARAMS_CELERY.update({
    "broker":CELERY_BROKER_URL,
    "backend":CELERY_RESULT_BACKEND,
})