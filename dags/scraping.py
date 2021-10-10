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

def gen_dict_extract(var, key):
    if hasattr(var,'iteritems'):
        for k, v in var.iteritems():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result

class YoutubeSpider(scrapy.Spider):
    name = 'ish_tecnologia'
    start_urls = ['https://www.youtube.com/results?search_query=ish+tecnologia&sp=EgQIBRAB']

    def parse(self, response):
        # import ipdb; ipdb.set_trace()
        script = response.xpath("//script[contains(text(), 'videoRenderer')]").extract_first()
        print("=================")
        print(list(gen_dict_extract(list(extract_json_objects(script))[0], ['videoId'])))
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
