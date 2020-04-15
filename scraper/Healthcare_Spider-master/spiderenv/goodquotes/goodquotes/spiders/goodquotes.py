import scrapy
from scrapy.loader import ItemLoader
from goodquotes.items import HealthLineItem
from scrapy_splash import SplashRequest

class GoodReadsSpider(scrapy.Spider):
    #identity
    name='goodreads'
    root='Start'
    keywords='daily health fooding routine'
    article_links=[]
    count=0

    #requests
    start_urls=['https://www.healthline.com/search?q1=']

    def start_requests(self):
        print(self.start_urls[0]+GoodReadsSpider.keywords.replace(" ","/"))
        for url in self.start_urls:
            yield SplashRequest(url=url+GoodReadsSpider.keywords.replace(" ","/"), callback=self.parse,
            endpoint='render.html',
            args={'wait': 8},
            )

    #response 
    def parse(self, response):
        if GoodReadsSpider.root=="Start":
            links=response.xpath("//div[@class='gsc-webResult gsc-result']//div[@class='gsc-thumbnail-inside']//a/@href").extract()
            for link in links:
                GoodReadsSpider.article_links.append(link)
            
            print(GoodReadsSpider.article_links)
            GoodReadsSpider.root="Get_article"
            next_page=GoodReadsSpider.article_links[GoodReadsSpider.count]
            GoodReadsSpider.count+=1
            yield response.follow(next_page, callback=self.parse,dont_filter=True)
        
        elif GoodReadsSpider.root=="Get_article":
            article=response.xpath(".//div[@class='css-z468a2']")
            loader=ItemLoader(item=HealthLineItem(), selector=article, response=response)
            loader.add_xpath('blogTitle',"./h1")
            loader.add_xpath("blogText",".//article[@class='article-body css-d2znx6 undefined']//h2 | .//article[@class='article-body css-d2znx6 undefined']//p")
            loader.add_value("source","Healthline.com")
            loader.add_value("keyword",GoodReadsSpider.keywords)
            loader.add_value("link",GoodReadsSpider.article_links[(GoodReadsSpider.count-1)])
            yield loader.load_item()

            
            next_page=GoodReadsSpider.article_links[GoodReadsSpider.count]

            GoodReadsSpider.count+=1
            yield response.follow(next_page, callback=self.parse,dont_filter=True)

