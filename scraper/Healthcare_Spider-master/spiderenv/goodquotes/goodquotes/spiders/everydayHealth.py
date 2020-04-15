import scrapy
from scrapy.loader import ItemLoader
from goodquotes.items import HealthLineItem
from scrapy_splash import SplashRequest

class EverydayHealthSpider(scrapy.Spider):
    #identity
    name='spider_evdayhealth'
    root='Start'
    keywords='daily health fooding routine'
    article_links=[]
    count=0

    #requests
    start_urls=['https://www.everydayhealth.com/search/'+ keywords.replace(' ','%20')]

    #response 
    def parse(self, response):
        if EverydayHealthSpider.root=="Start":
            links=response.xpath("//div[@class='result-item']/h2[@class='result-item__title']/a/@href").extract()
            for link in links:
                EverydayHealthSpider.article_links.append(link)
            
            EverydayHealthSpider.root="Get_article"
            next_page=EverydayHealthSpider.article_links[EverydayHealthSpider.count]
            EverydayHealthSpider.count+=1
            yield response.follow(next_page, callback=self.parse,dont_filter=True)
        
        elif EverydayHealthSpider.root=="Get_article":
            title=response.xpath(".//h1/text()").extract_first()
            try:
                content=response.xpath('.//section//p | .//section//h2 | .//section//ul | .//section//h3')[:-2].extract()
            except:
                content="Not a Blog"

            # yield{
            #     'title':title,
            #     'content':content,
            #     'source':"Everydayhealth.com",x   
            #     'keyword':EverydayHealthSpider.keywords,
            #     'link':EverydayHealthSpider.article_links[(EverydayHealthSpider.count-1)]
            # }
            loader=ItemLoader(item=HealthLineItem(), selector=response, response=response)
            loader.add_value('blogTitle',title)
            loader.add_value('blogText',content)
            loader.add_value("source","Everydayhealth.com")
            loader.add_value("keyword",EverydayHealthSpider.keywords)
            loader.add_value("link",EverydayHealthSpider.article_links[(EverydayHealthSpider.count-1)])
            yield loader.load_item()

            
            next_page=EverydayHealthSpider.article_links[EverydayHealthSpider.count]

            EverydayHealthSpider.count+=1
            yield response.follow(next_page, callback=self.parse,dont_filter=True)

