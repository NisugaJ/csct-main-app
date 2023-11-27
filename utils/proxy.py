import logging
import random

class ProxyList:
    def __init__(self, file_path):
        self.proxies = []
        self.load_proxies(file_path)

    def pick_random_proxy(self):
        picked_proxy = random.choice(
            self.proxies
            )
        logging.info(
            f"Picked proxy: {picked_proxy}"
            )
        return picked_proxy

    def load_proxies(self, file_path):
        with open(file_path,'r') as file:
            lines = file.readlines()
            temp_proxies = []
            for line in lines:
                temp_proxies.append(line.strip())

            self.proxies = temp_proxies

