# coding=utf-8

__author__ = 'carwest'
# -*- encoding=utf-8 -*-

import psycopg2
import jieba
import codecs
import json
from lxml import etree

class Preprocess:
    KEYWORDS = [u"聚众", u"强占", u"强征", u"强拆", u"非法集会", u"大众恐慌", u"骚乱", u"集会", u"罢工", u"集体怠工", u"上访", u"游行", u"示威", u"抗议"]


    def __init__(self):
        self.conn = psycopg2.connect("dbname=news user=carwest")
        self.cur = self.conn.cursor()
        self.filePtr = None
        self.cnt = 0

    def all(self):
        self.conn.commit()
        self.cur.execute("select * from allcontent")
        self.filePtr = codecs.open('selected_all.txt', 'w', 'utf-8')
        for record in self.cur.fetchall():
            #print record[2]
            try:
                content = record[1]
                #print content
                seglist = jieba.cut(content)
                for word in seglist:
                    flag = False
                    for keyword in self.KEYWORDS:
                        if word == keyword:
                            flag = True
                            print content
                            self.filePtr.write(json.dumps({"content": content}) + "\n")
                            self.cnt += 1
                            break
                    if flag:
                        break
            except:
                print "some error"

        self.conn.commit()

    def baidu(self):
        self.filePtr = codecs.open('selected.txt', 'w', 'utf-8')
        self.conn.commit()
        self.cur.execute("select * from baiducontent")
        for record in self.cur.fetchall():
            #print record[2]
            try:
                root = etree.fromstring(record[2])
                contentList = root.xpath("//descendant-or-self::*/text()")
                content = ""
                for part in contentList:
                    content += " " + part
                #print content
                seglist = jieba.cut(content)
                for word in seglist:
                    flag = False
                    for keyword in self.KEYWORDS:
                        if word == keyword:
                            flag = True
                            print content
                            self.filePtr.write(json.dumps({"title": record[1], "content": content}) + "\n")
                            self.cnt += 1
                            break
                    if flag:
                        break
            except:
                print "some error"

        self.conn.commit()


if __name__ == "__main__":
    pre = Preprocess()
    pre.baidu()
    pre.all()
    print pre.cnt



