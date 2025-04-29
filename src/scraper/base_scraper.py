import time
import random
import logging

class BaseScraper:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_random_delay(self, min_delay=1, max_delay=3):
        delay = random.uniform(min_delay, max_delay)
        self.logger.debug(f"Sleeping for {delay:.2f} seconds to mimic human behavior.")
        time.sleep(delay)

    def start(self):
        raise NotImplementedError("Each scraper must implement the start() method")
