import sys

from pandasaurus.utils.logging_config import configure_logger


def test_logger_propagate_setting():
    is_pytest_running = "pytest" in sys.modules

    logger = configure_logger()

    if is_pytest_running:
        assert logger.propagate  # Propagate should be True when pytest is running
    else:
        assert not logger.propagate  # Propagate should be False when pytest is not running
