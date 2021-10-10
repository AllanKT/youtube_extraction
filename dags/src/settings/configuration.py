
# -*- coding: utf-8 -*-

import os
from datetime import datetime

def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        raise KeyError(f"Expected environment variable '{name}' not set.")

class Configuration(object):
    """Interacting with environment variables."""
    BASE_DIR = "\\".join(os.path.abspath(os.path.dirname(__file__)).split("\\")[:-1])

    URL_YOUTUBE_SCRAP = 'https://www.youtube.com/results?search_query=ish+tecnologia&sp=EgQIBRAB'
    URL_YOUTUBE_WATCH = 'https://www.youtube.com/watch?v='
    INTERVAL = '@once'
    # INTERVAL = '*/5 * * * *'

    PROCESS = {
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT': 'json',
        'FEED_URI': f'dags/assets/data-{datetime.now().strftime("%d_%m_%Y-%H_%M_%S")}.json',
        'FEED_EXPORT_ENCODING': 'utf-8',
    }

    DEFAULT_ARGS = {
        'owner': 'airflow',
        'dependes_on_past': False,
        'start_date': datetime(2021, 10, 9),
        'retries': 0
    }
