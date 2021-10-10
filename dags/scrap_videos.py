from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

from src.tasks import *
from src.settings import *

# def extract_json_objects(text, decoder=JSONDecoder()):
#     pos = 0
#     while True:
#         match = text.find('{', pos)
#         if match == -1:
#             break
#         try:
#             result, index = decoder.raw_decode(text[match:])
#             yield result
#             pos = match + index
#         except ValueError:
#             pos = match + 1

# def get_recursively(search_dict, field):
#     fields_found = []
#     for key, value in search_dict.items():
#         if key == field:
#             fields_found.append(value)
#         elif isinstance(value, dict):
#             results = get_recursively(value, field)
#             for result in results:
#                 fields_found.append(result)
#         elif isinstance(value, list):
#             for item in value:
#                 if isinstance(item, dict):
#                     more_results = get_recursively(item, field)
#                     for another_result in more_results:
#                         fields_found.append(another_result)
#     return fields_found

# class YoutubeSpider(scrapy.Spider):
#     name = 'ish_tecnologia'
#     start_urls = [configs['url']]

#     def parse(self, response):
#         script = response.xpath("//script[contains(text(), 'videoRenderer')]").extract_first()
#         for item in get_recursively(list(extract_json_objects(script))[0], 'videoRenderer'):
#             yield {
#                 'title': item['title']['runs'][0]['text'].encode().decode('utf-8', 'ignore'),
#                 'link': item['videoId'],
#             }

# def run():
#     process = CrawlerProcess(configs['process'])
#     process.crawl(YoutubeSpider)
#     process.start()

with DAG(
    dag_id='scrap_videos',
    schedule_interval=configs.INTERVAL,
    default_args=configs.DEFAULT_ARGS,
    catchup=False,
) as dag:

    start = DummyOperator(task_id='start', dag=dag)
    scrap=PythonOperator(
        task_id='scrap',
        python_callable=scrap,
        dag=dag
    )
    end = DummyOperator(task_id='end', dag=dag)

start >> scrap
scrap >> end
