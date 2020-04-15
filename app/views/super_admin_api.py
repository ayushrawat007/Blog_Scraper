from app import blogapp 
from app import api

from flask_restful import reqparse
from flask_restful import Resource,Api  

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app import mongo

from blogscraper.blogscraper.spiders.wiki_spider import WikiSpider

from scrapy.crawler import CrawlerProcess

import subprocess
from scrapy.utils.project import get_project_settings
import json

from scrapy.settings import Settings

from blogscraper.blogscraper import settings as wiki_settings


Limiter=Limiter(blogapp,key_func=get_remote_address)
Limiter.init_app(blogapp)


parser=reqparse.RequestParser()
parser.add_argument('keywords',type=str ,required=True,help="Please enter the Keyword before running the Scraper")


class runscraper(Resource):
    def __init__(self):
        self.__keywords=parser.parse_args().get('keywords',None)

    def get(self):
        return {'data':self.__keywords}
        
    def post(self):
        # s=get_project_settings()
        # print(s['BOT_NAME'])

        crawler_settings=Settings()
        crawler_settings.setmodule(wiki_settings)
        # print(crawler_settings['SPLASH_URL'])

        # subprocess.check_output(['scrapy', 'crawl', "WikiSpider", 'mental health', 'cs='+json.dumps(get_project_settings())])

        #run spider
        process=CrawlerProcess(crawler_settings)
        # process.crawl('wiki_blogs',domain='wikihow.com')
        # process.start()
        # wiki=WikiSpider(self.__keywords)
        process.crawl(WikiSpider,self.__keywords)
        # # process.crawl(WikiSpider)
        process.start()
        

        return {'keywords':"this is your keyword {} ".format(parser.parse_args())}
        
    def delete(self):
        pass
    def update(self):
        pass
api.add_resource(runscraper,'/runscraper')

