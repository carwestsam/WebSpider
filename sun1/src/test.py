import requests
import bs4
import codecs
import datetime
import json
import sys

WebsiteUrl = 'http://orientaldaily.on.cc'


def dealOnepage( bo ):
    
    idleadin =  bo.find( id='leadin' )
    
    #print idleadin

    haveTitle = len ( idleadin.select('h1') )
    if ( haveTitle == 0 ):
        articleTitle = "null"
    else:
        articleTitle = idleadin.select('h1')[0].string
        print articleTitle
    articleLeadin = idleadin.select('div.leadin')[0].string
    #print articleTitle
    #print articleLeadin

    idcontent = bo.find(id='contentCTN-right')

    articleContent = idcontent.find_all(['p', 'h3'])
    #print articleContent

    articleContentStream = ""
    for passage in articleContent:
        articleContentStream += passage.encode('utf-8')

    returnObject = { 'title':articleTitle, 'leadin': articleLeadin, 'content': articleContentStream}
    #print json.dumps( articleObject )
    #print json.dumps( returnObject )
    return returnObject

def dealOneDay( date ):

    response = requests.get("http://orientaldaily.on.cc/cnt/news/%d/index.html" % date);

    response.encoding = 'utf-8'

    soup =  bs4.BeautifulSoup( response.text )
    pageCTNcol2 = soup.find(id='pageCTN-col2')
    #print pageCTNcol2

    linkList = pageCTNcol2.select( 'li a' )

    
    cnt = 0;

    pageList = []

    for link in linkList:
        href = link.get('href')
        #print cnt 
        #print href
        print WebsiteUrl + href
        #outputfile = codecs.open(OutputDir+href, 'w', 'utf-8')
        
        try:
            webContent = requests.get( WebsiteUrl + href )
            webContent.encoding = 'utf-8'
            tmpSoup = bs4.BeautifulSoup( webContent.text )
            pageObject = dealOnepage ( tmpSoup )
            pageList.append( {'url': WebsiteUrl+href, 'page' : pageObject} )
        except ValueError:
            print "ValueError"
        except IOError:
            print "IOError"
        except:
            pass
        else:
            print "ok\n-----------"
            pass



        #outputfile.write( webContent.text )
        #outputfile.close()
        cnt += 1

        #if cnt > 1:
        #    break;


    dayJson = json.dumps(pageList, encoding='utf-8')
    #print dayJson



    OutputDir = '../output/jsonFormat/%d.json' % date
    ofile = codecs.open( OutputDir, 'w', 'utf-8' )
    ofile.write ( dayJson )
    #print json.loads( dayJson )[0]['page']['content']
    ofile.close()

    print 'finished'


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




