import requests
import bs4
import codecs
import datetime
import json
import sys
from lxml import html

WebsiteUrl = 'http://the-sun.on.cc'


def dealOnePage ( bo ):
    article = bo.find( id='pageLeftCTN' )
    #print article
    title = article.find( id='acticle_header_and_textlink' ).find('h1')
    print title.string

    contents = article.find('div', {'class', 'para_content'}) .find_all( 'div', { 'class', 'newsText' } ) 
    #print contents
    print '-------'

    articleContentStream = ""
    for passage in contents :
        for pp in passage.find_all(['h2', 'p']):
            articleContentStream += pp.encode('utf-8')
        
    #print articleContentStream

    returnObject = { 'title': title.string, 'content': articleContentStream}
    return returnObject


def dealOneDay( date ):

    response = requests.get("http://the-sun.on.cc/cnt/news/%d/index.html" % date);

    response.encoding = 'utf-8'

    pageList = []
    soup =  bs4.BeautifulSoup( response.text )
    sectionContentCTN = soup.find(id='sectionContentCTN').find_all( 'div', { 'class' : 'displayContent' } )
    #print sectionContentCTN

    cnt = 0
    for item in sectionContentCTN:
        #print item
        href =  item.find( 'a' , { 'class' : 'headlineNewsTitle' } ).get('href')
        fullUrl = WebsiteUrl + href
        print fullUrl
        try:
            webContent = requests.get( fullUrl )
            webContent.encoding = 'utf-8'
            tmpSoup = bs4.BeautifulSoup( webContent.text)
            pageObject = dealOnePage( tmpSoup )
            pageList.append( { 'url' : fullUrl, 'page' : pageObject } )
        except:
            print 'error'
            pass
        else:
            print 'ok'
        
        cnt += 1
        #if ( cnt > 3 ) :
        #    break


    dayJson = json.dumps(pageList, encoding='utf-8')

    OutputDir = '../output/jsonFormat/sun%d.json' % date
    ofile = codecs.open( OutputDir, 'w', 'utf-8' )
    ofile.write ( dayJson )
    #print json.loads( dayJson )[0]['page']['content']
    ofile.close()
    return

def getParseDateNumber( number ):
    year = number/10000
    month = (number%10000) / 100
    day = number%100
    return [ year, month, day ]

def loopDates( start, end ):
    
    [sYear, sMonth, sDay] = getParseDateNumber( start )
    [eYear, eMonth, eDay] = getParseDateNumber( end )

    date = datetime.date( 2015, 1, 12 )

    todayDate = datetime.date.today();
    endDate = datetime.date( eYear, eMonth, eDay )
    startDate = datetime.date( sYear, sMonth, sDay )

    oneDay = datetime.timedelta( days=1 )
    
    loopDate = startDate
    for x in range( 10000000 ):
        if  ( loopDate >= endDate or loopDate > todayDate ):
            break
        aDay = int(loopDate.strftime("%Y%m%d"))
        print "----------------\n get date %d \n" % aDay
        dealOneDay( aDay )
        print "---------------\n"
        loopDate = loopDate + oneDay

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print 'error arguments'
    else:
        loopDates( int(sys.argv[1]), int(sys.argv[2]) )




