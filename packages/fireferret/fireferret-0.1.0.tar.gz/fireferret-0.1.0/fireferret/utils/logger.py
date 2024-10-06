import logging

logger = logging.getLogger("fireferret")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("debug.log")

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
