from retry import retry

import logging
import requests

class Download(object):

    def __init__(self):
        self.logger = logging.getLogger('DOWNLOAD')

    @retry(exceptions=Exception, delay=20, tries=5)
    def getData(self, url):
        self.logger.info("Start to download the csv file")
        response = requests.get(url);
        if response.status_code >= 200 and response.status_code <= 299:
            return response.content
        self.logger.debug("Problem to download the csv file, the system will retry in 20s.")
        raise Exception("Problem to get data from url.")
            