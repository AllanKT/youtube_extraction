import scrapy
from json import JSONDecoder

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

def get_recursively(search_dict, field):
    fields_found = []
    for key, value in search_dict.items():
        if key == field:
            fields_found.append(value)
        elif isinstance(value, dict):
            results = get_recursively(value, field)
            for result in results:
                fields_found.append(result)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    more_results = get_recursively(item, field)
                    for another_result in more_results:
                        fields_found.append(another_result)
    return fields_found

class YoutubeSpider(scrapy.Spider):
    name = 'ish_tecnologia'
    start_urls = ['https://www.youtube.com/results?search_query=ish+tecnologia&sp=EgQIBRAB']

    def parse(self, response):
        # import ipdb; ipdb.set_trace()
        script = response.xpath("//script[contains(text(), 'videoRenderer')]").extract_first()
        # print("=================")
        # print(len(get_recursively(
        #     list(extract_json_objects(script))[0],
        #     'videoRenderer')))
        # print(list(extract_json_objects(script))[0]['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['videoRenderer'].keys())
        # print("=================")
        # print(list(extract_json_objects(script))[0]['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['videoRenderer']['videoId'])
        # print(list(extract_json_objects(script))[0]['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['videoRenderer']['title']['runs'][0]['text'])
        # print(len(list(extract_json_objects(script))[0]['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']))

        # for item in list(extract_json_objects(script))[0]['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']:
        #     yield {
        #         'title': item['videoRenderer']['title']['runs'][0]['text'],
        #         'link': item['videoRenderer']['videoId'],
        #     }

        for item in get_recursively(list(extract_json_objects(script))[0], 'videoRenderer'):
            yield {
                'title': item['title']['runs'][0]['text'],
                'link': item['videoId'],
            }
