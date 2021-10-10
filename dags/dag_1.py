from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

import scrapy
from scrapy.crawler import CrawlerProcess
from json import JSONDecoder

configs = {
    'process': {
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT': 'json',
        'FEED_URI': 'dags/data_youtube.json'
    },
    'url': 'https://www.youtube.com/results?search_query=ish+tecnologia&sp=EgQIBRAB',
    'youtube_watch': 'https://www.youtube.com/watch?v=',
    'interval': '@daily',
    # 'interval': '*/5 * * * *',
    'default_args': {
        'owner': 'airflow',
        'dependes_on_past': False,
        'start_date': datetime(2021, 10, 9),
        'retries': 0
    }
}

def extract_json_objects(text, decoder=JSONDecoder()):
    pos = 0
    while True:
        match = text.find('{', pos)
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result
            pos = match + index
        except ValueError:
            pos = match + 1

class YoutubeSpider(scrapy.Spider):
    name = 'ish_tecnologia'
    start_urls = [configs['url']]

    def parse(self, response):
        script = response.xpath("//script[contains(text(), 'videoRenderer')]").extract_first()
        for item in list(extract_json_objects(script))[0]['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']:
            yield {
                'title': item['videoRenderer']['title']['runs'][0]['text'],
                'link': configs['youtube_watch']+item['videoRenderer']['videoId'],
            }

def run():
    process = CrawlerProcess(configs['process'])
    process.crawl(YoutubeSpider)
    process.start()

with DAG(
    dag_id='DAG-1',
    schedule_interval=configs['interval'],
    default_args=configs['default_args'],
    catchup=False,
) as dag:

    start = DummyOperator(task_id='start', dag=dag)
    t2=PythonOperator(
        task_id='python_script',
        python_callable=run,
        dag=dag
    )
    end = DummyOperator(task_id='end', dag=dag)

start >> t2
t2 >> end
