from .config import Config
from .filler import Try


default_kafka_consumer_config = Config.from_dict({
    "bootstrap.servers": Try.cfgmap("kafka", "internal_bootstrap_servers"),
    "client.id": "eo4eu",
    "api.version.fallback.ms": 0,
    "group.id": "eo4eu",
    'enable.auto.commit': False,
    "auto.offset.reset": "latest",
})

default_kafka_producer_config = Config.from_dict({
    "bootstrap.servers": Try.cfgmap("kafka", "internal_bootstrap_servers"),
    "client.id": "eo4eu",
    "api.version.fallback.ms": 0,
})

default_boto_config = Config.from_dict({
    "region_name":           Try.cfgmap("s3-access", "region_name"),
    "endpoint_url":          Try.cfgmap("s3-access", "endpoint_url"),
    "aws_access_key_id":     Try.secret("s3-access-scr", "aws_access_key_id"),
    "aws_secret_access_key": Try.secret("s3-access-scr", "aws_secret_access_key"),
})

default_cloud_config = Config.from_dict({
    "endpoint_url":          Try.cfgmap("s3-access", "endpoint_url"),
    "aws_access_key_id":     Try.secret("s3-access-scr", "aws_access_key_id"),
    "aws_secret_access_key": Try.secret("s3-access-scr", "aws_secret_access_key"),
})

default_eo4eu_config = Config.from_dict({
    "namespace":      Try.cfgmap("eo4eu", "namespace"),
    "s3_bucket_name": Try.cfgmap("eo4eu", "s3-bucket-name"),
})

default_logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": " - ".join([
                "[\033[31;1m%(levelname)s\033[0m]",
                "\033[92;1m%(asctime)s\033[0m",
                "%(name)s",
                "%(message)s",
            ]),
            "datefmt": "%H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
