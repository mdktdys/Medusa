from logging import DEBUG, Logger, StreamHandler, getLogger
from typing import TextIO

logger: Logger = getLogger()
logger.setLevel(DEBUG)
handler: StreamHandler[TextIO] = StreamHandler()
handler.setLevel(DEBUG)
logger.addHandler(handler)
