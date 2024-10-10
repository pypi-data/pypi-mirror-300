# __init__.py
import logging

def setup_logging(level = logging.INFO, logger_name = "sane_logger"):
    """Set up logging with a named logger."""
    # Create or get a logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # Create a formatter
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

    # Create a console handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    return logger

sane_logger = setup_logging()
