"""
Platform Logger
"""

import logging

LOGGER_NAME = "platform-core"

logger = logging.getLogger(LOGGER_NAME)

logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

stream = logging.StreamHandler()

stream.setFormatter(formatter)

logger.addHandler(stream)
