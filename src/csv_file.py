from datetime import date

import logging

class CsvFile(object):

    def __init__(self):
        self.logger = logging.getLogger('CSV-FILE')

    def save(self, content, file_name='file', path='./'):
        self.logger.info("Starting saving the content into a CSV File")
        current_date = date.today()
        with open('{}{}-{}.csv'.format(path, file_name, current_date), 'wb') as file:
            file.write(content)
        file.close()
        self.logger.info("Finished saving the content into a CSV File")
