from src.download import Download
from src.csv_file import CsvFile

from src.gmail import Gmail

import logging

class Manager(object):

    def __init__(self, config):
        self.config = config
        self.mount()

    def mount(self):
        self.download = Download()
        self.csvFile = CsvFile()
        
        self.logger = logging.getLogger('MANAGER')
        self.logger.info("Read Config Params")
        
        self.logger.info("Create Gmail reader")
        self.gmail = Gmail(self.config)

        self.logger.info("Add schedule task to capture the data")

    def runCapture(self):
        self.logger.info("start capture the forest data")
        urlList = self.gmail.get_url_from_email()
        count = 1
        try:
            for url in urlList:
                content = self.download.getData(url)
                file_name = '{}-{}'.format(count, self.config.get('file_name'))
                self.csvFile.save(content, path=self.config.get('write_path'), file_name=file_name)
                self.logger.info("fineshed capture the forest data")
                count += 1
        except:
            self.logger.error("Was not possible to download file from: {}".format(url))