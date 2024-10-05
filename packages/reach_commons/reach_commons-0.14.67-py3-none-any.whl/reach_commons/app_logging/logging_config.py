import logging


class CustomPrefixFilter(logging.Filter):
    def __init__(self, prefix="[ReachLogProcessor]"):
        super().__init__()
        self.prefix = prefix

    def filter(self, record):
        if self.prefix not in record.msg:
            record.msg = f"{self.prefix} {record.msg}"
        return True


def setup_logger(prefix="[ReachLogProcessor]"):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    prefix_filter = CustomPrefixFilter(prefix)
    logger.addFilter(prefix_filter)

    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


logger = setup_logger()
