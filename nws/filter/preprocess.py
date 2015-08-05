#!/bin/python2
# -*- encoding=utf-8 -*-

import psycopg2
import jieba
import codecs
import json
from lxml import etree

conn = psycopg2.connect("dbname=news2 user=bdccl")
cur = conn.cursor()
filePtr = None
cnt = 0
KEYWORDS = [u"聚众", u"强占", u"强征", u"强拆", u"非法集会", u"大众恐慌", u"骚乱", u"集会", u"集体怠工", 
            u"集体上访", u"游行示威", u"示威", u"抗议", u"罢工", u"罢课", u"哄抢", u"斗殴", u"闹事", u"暴乱", 
            u"暴动", u"劫机", u"劫船", u"劫持", u"暴力性犯罪", u"暴力群斗", u"宗教冲突", u"恶性侵犯"]
conn.commit()
cur.execute("select * from labeled")
        #self.filePtr = codecs.open('selected_all.txt', 'w', 'utf-8')
from event_label import Event
from location_label import Location

ev = Event()

for record in cur.fetchall():

    page_idx = record[0]
    title = record[1]
    content = record[2]
    url = record[3]
    time = record[4]
    event = record[5]
    location = record[6]
                
    try:
        content = content.decode('utf-8')    
        #conn.commit()
        seglist = jieba.cut(content)
        for word in seglist:
            flag = False
            for keyword in KEYWORDS:
                if word == keyword:
                    flag = True
                    print content
                            #self.filePtr.write(json.dumps({"content": content}) + "\n")
                    cnt += 1
                    cur.execute("insert into preprocess(id,title,content,url,pubtime,event,location,matchedwords) values(%s,%s,%s,%s,%s,%s,%s,%s)",(record[0],record[1],record[2],record[3],record[4],record[5],record[6],word))

                    break
                if flag:
                    break

    except:
        print "some error"
    print cnt
conn.commit()
cur.execute("update filterlock set lock=False where id=1")
conn.commit()

cur.close()
conn.close()
