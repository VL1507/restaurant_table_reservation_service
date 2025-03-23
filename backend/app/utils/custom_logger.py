import logging


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"

    reset = "\x1b[0m"

    _format = "%(filename)s:%(lineno)d - %(levelname)-8s - [%(asctime)s] - %(name)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + _format + reset,
        logging.INFO: grey + _format + reset,
        logging.WARNING: yellow + _format + reset,
        logging.ERROR: red + _format + reset,
        logging.CRITICAL: bold_red + _format + reset,
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class CustomHandler(logging.StreamHandler):  # type: ignore
    fmtr = CustomFormatter()

    def format(self, record: logging.LogRecord) -> str:
        return self.fmtr.format(record)


def setup_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    handler.setFormatter(CustomFormatter())
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger


def custom_logging_basicConfig(level: int) -> None:
    logging.basicConfig(
        level=level,
        handlers=[CustomHandler()],
    )
