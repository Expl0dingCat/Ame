import logging
import os

def configure_logging():
    logging.basicConfig(filename=f'logs/ame.log', level=logging.INFO)
