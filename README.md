# youtube_extraction

curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.1.4/docker-compose.yaml'

mkdir -p ./dags ./logs ./plugins
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env

docker-compose up airflow-init && docker-compose up

docker-compose down --volumes --rmi all

# Scrapy

- processamento assincrono
``` scrapy shell "https://www.youtube.com/results?search_query=ish+tecnologia&sp=EgQIBRAB" ```
``` scrapy runspider code.py ```
