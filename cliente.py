from urllib import request
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

URL = "http://localhost:8000/"


response = request.urlopen(URL)
logger.info(f" response -----> {response}")
# print(f" response -----> {response.__dict__}")
print(f" response -----> {response.read()}")
