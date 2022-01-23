import json
import logging

class Config(object):

    def __init__(self):
        self.logger = logging.getLogger('CONFIG')

    def read(self):
        with open("config.json") as file:
            data = json.load(file)
        file.close()
        self.logger.info("Success on reading configuration file.")
        return data