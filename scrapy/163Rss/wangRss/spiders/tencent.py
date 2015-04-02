from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from sinaRss.items import NewsMarqueDdtItem
from sinaRss.items import SinaRssItem
from sinaRss.items import contentItem
from scrapy.http import Request
from scrapy.http import HtmlResponse
import psycopg2
import xmltodict
import codecs
import json
from lxml import html

class TencentNewsSpider( CrawlSpider ):
    name = 'qq'
    allowed_domains = ['qq.com']

    start_urls = []
    #start_urls = ['http://rss.sina.com.cn/news/world/focus15.xml']

    encodeDict = {}

    fileptr = None
    
    conn = None
    cur = None

    def op( self, str ):
        self.fileptr.write ( str )
        

    def __init__( self ):
        self.conn = psycopg2.connect("dbname=news user=carwest ")
        self.cur = self.conn.cursor()
        self.fileptr = codecs.open( self.name + ".logfile", "w", 'utf-8' )

        readin = codecs.open( 'sinaRss/spiders/'+self.name+"_rss.txt", "r", "utf-8" )
        for rss in readin.readlines():
            obj = json.loads( rss )
            self.start_urls.append( obj['url'] )


    def parse( self, response ):

        print response.url
        #print self.encodeDict[response.url]

        xmldata = response.body
        
        t_unicode = xmldata.decode( response.encoding )
        xmldata = t_unicode.encode('utf-8')

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

                self.op( "\n\n\n" )
                self.op( "title:\t" + title )
                self.op ( [link , date, time, weekday].__str__() )
                self.op( 'desc:\t' + desc )

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
        #self.op( '\n\n\n' +  response.url + '\n' + response )
        #print response.__dict__
        #sel = HtmlXPathSelector( response )
        doc = response.body
        tree = html.fromstring(response.body.decode( response.encoding))
        r = tree.xpath('//*[@id="Cnt-Main-Article-QQ"]/p/text()')
        print r[0]

        #l = sel.xpath('//*[@id="artibody"]/p/text()').extract()
        #l = sel.xpath('//*[@id="Cnt-Main-Article-QQ"]/p/text()').extract()


        
        _str = ""
        #for x in l:
        #    _str+= " " + x

        item = contentItem()
        item['url'] = response.url
        item['content'] = _str
        self.op( '\n\n\n' )
        self.op( response.url )
        self.op( _str )
        
        try:
            self.conn.commit()
            #self.cur.execute('insert into sinaarticle( url, content ) values( %s, %s )', ( response.url, _str ))
            self.conn.commit()
        except:
            print 'error!!!! at articleParse'
            pass

        print '++++++++++++++++\n'

        yield item
