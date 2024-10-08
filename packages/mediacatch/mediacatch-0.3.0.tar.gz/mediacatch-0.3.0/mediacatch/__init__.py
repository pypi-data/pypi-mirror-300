import logging
import sys
import os

from dotenv import load_dotenv

logging.basicConfig(
    format='[%(asctime)s][%(levelname)s][%(name)s] %(message)s',
    datefmt='%d/%m/%Y-%H:%M:%S',
    handlers=[logging.StreamHandler(sys.stdout)],
    level=logging.INFO,
)

load_dotenv()
mediacatch_api_key = os.environ['MEDIACATCH_API_KEY']

__version__ = '0.3.0'
