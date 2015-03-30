from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from sinaRss.items import NewsMarqueDdtItem
from scrapy.http import Request
import xmltodict

class SinaNewsMarqueeDdtSpider( CrawlSpider ):

    name = 'marquee'
    allowed_domains = [ 'sina.com.cn' ]
    start_urls = ['http://rss.sina.com.cn/news/marquee/ddt.xml']

    def parse( self, response ):
        xmldata = response.body
        dict = xmltodict.parse(xmldata,  encoding='utf-8')
        items = dict['rss']['channel']['item']

        for item in items:
            print '\n\n\n------------------'
            print item['title']
            print item['link']
            print item['author']
            print item['guid']
            print item['pubDate']
            print item['description']
            print '++++++++++++++++++++++++'

            yield Request( item['link'], self.articleParse )
    
    def articleParse( self, response ):
        print "\n\n\n++++++++++++++\n\n\n"
        sel = HtmlXPathSelector( response )
        title = sel.xpath('//*[@id="artibodyTitle"]/child::text()')[0].extract()
        print title
        l = sel.xpath('//*[@id="artibody"]/p/text()').extract()
        for x in l:
            print x
        
        
    

