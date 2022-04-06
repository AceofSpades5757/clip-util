import logging.config
from pathlib import Path


logs_path = Path(__file__).parent / 'logs'
logs_path.mkdir(exist_ok=True)


date_format: str = '%Y-%m-%dT%H:%M:%S%z'
message_format = '{asctime} - {name} - {levelname:<8} - {message}'
logging_config = dict(
    version=1,
    disable_existing_loggers=False,
    root=dict(
        level=logging.INFO,
        handlers=[
            'file_handler',
        ],
    ),
    formatters={
        'default': {
            # 'date_format': '%Y-%m-%dT%H:%M:%S+0000%z',
            'date_format': date_format,
            'format': message_format,
            'style': '{',
        },
    },
    handlers={
        'file_handler': {
            'level': logging.INFO,
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': logs_path / 'root.log',
        },
    },
    loggers={},
)

logging.config.dictConfig(logging_config)
formatter: logging.Formatter = logging.Formatter(
    datefmt=date_format,
    style='{',
    fmt=message_format,
)
logging.getLogger().handlers[0].setFormatter(formatter)


def get_logger(
    name: str, level=logging.DEBUG, debug: bool = False
) -> logging.Logger:

    logger: logging.Logger = logging.getLogger(__name__)
    logger.setLevel(level)

    log_file: Path = logs_path / Path(name).with_suffix('.log').name

    formatter: logging.Formatter = logging.Formatter(
        datefmt=date_format,
        style='{',
        fmt=message_format,
    )

    file_handler: logging.FileHandler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    if debug:
        stream_handler: logging.StreamHandler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        logger.addHandler(stream_handler)

    return logger
