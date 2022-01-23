import schedule
import logging

from src.manager import Manager
from src.config import Config

if __name__ == "__main__":
    config = Config()
    configParams = config.read()
    logging.basicConfig(filename='{}py-gmail.log'.format(configParams['write_path']),
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                        filemode='a',
                        datefmt='%d/%m/%Y %I:%M:%S %p',
                        level=logging.INFO)

    manager = Manager(configParams)

    schedule.every().day.at(configParams.get("exec_time")).do(manager.runCapture)
    
    while True:
        schedule.run_pending()