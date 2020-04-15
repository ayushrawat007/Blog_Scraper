import scrapy
from ..items import BlogscraperItem

from scrapy_splash import SplashRequest


from scrapy.utils.project import get_project_settings

class WikiSpider(scrapy.Spider):
    name="wiki_blogs"
    start_urls=["http://www.wikihow.com/wikiHowTo?search="]
    

    def __init__(self, keyword="", *args, **kwargs):
        print("="*100)
        print(keyword)
        print("="*100)
        print("="*100)
        print(args)
        print("="*100)
        print("="*100)
        print(kwargs)
        print("="*100)
        
        super(WikiSpider, self).__init__(*args, **kwargs)
        self.keyword=keyword
        self.start_urls[0]=str(self.start_urls[0])+self.keyword.replace(' ','+')
        print("="*100)
        print(self.start_urls)
        print("="*100)

        # yield SplashRequest(url=self.start_urls[0], callback=self.parse_search,
        #     endpoint='render.html',
        #     args={'wait': 8},
        # )   

    def start_requests(self):

        yield SplashRequest(url=self.start_urls[0], callback=self.parse_search,
            endpoint='render.html',
            args={'wait': 0},
        )   



    def parse_search(self,response):

        blogs_links=response.css("a.result_link::attr(href)").extract()

        for link in blogs_links:
            print("-"*100)
            print(link)
            print("-"*100)
            # yield scrapy.Request(link, callback = self.parse_article)
            yield SplashRequest(url=link, callback=self.parse_article,
                endpoint='render.html',
                args={'wait': 0},
            )   




    
    def parse_article(self,response):

        items=BlogscraperItem()

        items["title"]=response.xpath('//*[(@id = "section_0")]//a/text()')[0].extract()
        items["dateCreated"]=response.xpath('//*[(@id = "expert_coauthor")]//p/text()')[0].extract()
        items["blogText"]=response.xpath('//*[(@id = "mf-section-0")]//p | //*[@class="step"]').extract()
        items["source"]="wikihow"
        items["keyword"]=self.keyword
        items["link"]=response.url

        yield items



        


