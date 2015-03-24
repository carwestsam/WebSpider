from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from sinaRss.items import NewsMarqueDdtItem
from sinaRss.items import SinaRssItem
from sinaRss.items import contentItem
from scrapy.http import Request
import psycopg2
import xmltodict

class SinaNewsSpider( CrawlSpider ):
    name = 'qq'
    allowed_domains = ['qq.com']
    start_urls = [ 'http://news.qq.com/newsgn/rss_newsgn.xml','http://ent.qq.com/movie/rss_movie.xml' ]
    #start_urls = ['http://rss.sina.com.cn/news/world/focus15.xml']
    
    conn = None
    cur = None

    def __init__( self ):
        self.conn = psycopg2.connect("dbname=news user=root ")
        self.cur = self.conn.cursor()


    def parse( self, response ):

        print response.url

        xmldata = response.body
        dict = xmltodict.parse( xmldata, encoding='utf-8' )
        rssItems = dict['rss']['channel']['item']

        NewsList = []

        for rssItem in rssItems:
            title = rssItem['title']
            link = rssItem['link']
            pubDate = rssItem['pubDate']
            desc = rssItem['description']
            print title
            print '-------------'

            date = 0
            time = 0

            if pubDate != None:
                time = pubDate[11:19]
                year = pubDate[0:4]
                mon = pubDate[5:7]
                day = pubDate[8:10]
                weekday = ""
                date = year+"-"+mon+"-"+day
                #self.cur.execute('select * from sinarss where ')
                try:
                    #print "%s+%s+%s+%s+%s+%s" %( link, title, date, time, weekday, desc)
                    if link == None or title == None or date == None or time == None or weekday == None or desc == None:
                        print 'nonononono!!!'

                    self.conn.commit()
                    self.cur.execute('insert into sinarss( url, title, pubDate, pubTime, weekday, description) values( %s, %s, %s, %s, %s, %s )', (link, title, date, time, weekday, desc ))
                    self.conn.commit()
                except psycopg2.Error as e:
                    print e.pgerror
                    print 'error!!! at parse'
                    pass
                except:
                    print 'no'
                    pass

            yield Request( rssItem['link'], self.articleParse )

    def articleParse( self, response ):
        print 'articleParse'
        sel = HtmlXPathSelector( response )
        l = sel.xpath('//*[@id="artibody"]/p/text()').extract()
        l = sel.xpath('//*[@id="Cnt-Main-Article-QQ"]/p/text()').extract()


        _str = ""
        for x in l:
            _str+= x

        item = contentItem()
        item['url'] = response.url
        item['content'] = _str
        
        try:
            self.conn.commit()
            self.cur.execute('insert into sinaarticle( url, content ) values( %s, %s )', ( response.url, _str ))
            self.conn.commit()
        except:
            print 'error!!!! at articleParse'
            pass

        print '++++++++++++++++\n'

        yield item

