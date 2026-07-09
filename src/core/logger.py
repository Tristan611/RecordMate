import logging


def setup_logger(level="INFO"):

    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S"
    )

    return logging.getLogger("RecordMate")
