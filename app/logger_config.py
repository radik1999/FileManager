import logging

logger = logging.getLogger()

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger.setLevel(logging.INFO)
logger.addHandler(handler)

logging.getLogger('googleapiclient').setLevel(logging.ERROR)
