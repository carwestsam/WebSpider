# coding=utf-8

__author__ = 'carwest'
# -*- encoding=utf-8 -*-



import codecs
import json
import jieba
from lxml import etree
import psycopg2

class locationFilter:

    LOCATIONS = [u"合肥", u"宿州", u"淮北", u"阜阳", u"蚌埠", u"淮南", u"滁州", u"马鞍山", u"芜湖", u"铜陵", u"安庆", u"黄山", u"六安", u"池州", u"宣城", u"亳州", u"界首", u"明光", u"天长", u"桐城", u"宁国", u"巢湖", u"厦门", u"福州", u"南平", u"三明", u"莆田", u"泉州", u"漳州", u"龙岩", u"宁德", u"福清", u"长乐", u"邵武", u"武夷山", u"建瓯", u"永安", u"石狮", u"晋江", u"南安", u"龙海", u"漳平", u"福安", u"福鼎", u"兰州", u"嘉峪关", u"金昌", u"白银", u"天水", u"酒泉", u"张掖", u"武威", u"庆阳", u"平凉", u"定西", u"陇南", u"玉门", u"敦煌", u"临夏", u"合作", u"广州", u"深圳", u"清远", u"韶关", u"河源", u"梅州", u"潮州", u"汕头", u"揭阳", u"汕尾", u"惠州", u"东莞", u"珠海", u"中山", u"江门", u"佛山", u"肇庆", u"云浮", u"阳江", u"茂名", u"湛江", u"英德", u"连州", u"乐昌", u"南雄", u"兴宁", u"普宁", u"陆丰", u"恩平", u"台山", u"开平", u"鹤山", u"高要", u"四会", u"罗定", u"阳春", u"化州", u"信宜", u"高州", u"吴川", u"廉江", u"雷州", u"贵阳", u"六盘水", u"遵义", u"安顺", u"毕节", u"铜仁", u"清镇", u"赤水", u"仁怀", u"凯里", u"都匀", u"兴义", u"福泉", u"石家庄", u"邯郸", u"唐山", u"保定", u"秦皇岛", u"邢台", u"张家口", u"承德", u"沧州", u"廊坊", u"衡水", u"辛集", u"晋州", u"新乐", u"遵化", u"迁安", u"霸州", u"三河", u"定州", u"涿州", u"安国", u"高碑店", u"泊头", u"任丘", u"黄骅", u"河间", u"冀州", u"深州", u"南宫", u"沙河", u"武安", u"哈尔滨", u"齐齐哈尔", u"黑河", u"大庆", u"伊春", u"鹤岗", u"佳木斯", u"双鸭山", u"七台河", u"鸡西", u"牡丹江", u"绥化", u"尚志", u"五常", u"讷河", u"北安", u"五大连池", u"铁力", u"同江", u"富锦", u"虎林", u"密山", u"绥芬河", u"海林", u"宁安", u"安达", u"肇东", u"海伦", u"郑州", u"开封", u"洛阳", u"平顶山", u"安阳", u"鹤壁", u"新乡", u"焦作", u"濮阳", u"许昌", u"漯河", u"三门峡", u"南阳", u"商丘", u"周口", u"驻马店", u"信阳", u"济源", u"荥阳", u"新郑", u"登封", u"新密", u"偃师", u"孟州", u"沁阳", u"卫辉", u"辉县", u"林州", u"禹州", u"长葛", u"舞钢", u"义马", u"灵宝", u"项城", u"巩义", u"邓州", u"永城", u"汝州", u"武汉", u"十堰", u"襄阳", u"荆门", u"孝感", u"黄冈", u"鄂州", u"黄石", u"咸宁", u"荆州", u"宜昌", u"随州", u"仙桃", u"天门", u"潜江", u"丹江口", u"老河口", u"枣阳", u"宜城", u"钟祥", u"汉川", u"应城", u"安陆", u"广水", u"麻城", u"武穴", u"大冶", u"赤壁", u"石首", u"洪湖", u"松滋", u"宜都", u"枝江", u"当阳", u"恩施", u"利川", u"长沙", u"衡阳", u"张家界", u"常德", u"益阳", u"岳阳", u"株洲", u"湘潭", u"郴州", u"永州", u"邵阳", u"怀化", u"娄底", u"耒阳", u"常宁", u"浏阳", u"津市", u"沅江", u"汨罗", u"临湘", u"醴陵", u"湘乡", u"韶山", u"资兴", u"武冈", u"洪江", u"冷水江", u"涟源", u"吉首", u"长春", u"吉林", u"白城", u"松原", u"四平", u"辽源", u"通化", u"白山", u"德惠", u"榆树", u"磐石", u"蛟河", u"桦甸", u"舒兰", u"洮南", u"大安", u"双辽", u"公主岭", u"梅河口", u"集安", u"临江", u"延吉", u"图们", u"敦化", u"珲春", u"龙井", u"和龙, 扶余", u"南昌", u"九江", u"景德镇", u"鹰潭", u"新余", u"萍乡", u"赣州", u"上饶", u"抚州", u"宜春", u"吉安", u"瑞昌", u"共青城", u"乐平", u"瑞金", u"德兴", u"丰城", u"樟树", u"高安", u"井冈山", u"贵溪", u"南京", u"徐州", u"连云港", u"宿迁", u"淮安", u"盐城", u"扬州", u"泰州", u"南通", u"镇江", u"常州", u"无锡", u"苏州", u"江阴", u"宜兴", u"邳州", u"新沂", u"金坛", u"溧阳", u"常熟", u"张家港", u"太仓", u"昆山", u"如皋", u"海门", u"启东", u"大丰", u"东台", u"高邮", u"仪征", u"扬中", u"句容", u"丹阳", u"兴化", u"泰兴", u"靖江", u"沈阳", u"大连", u"朝阳", u"阜新", u"铁岭", u"抚顺", u"本溪", u"辽阳", u"鞍山", u"丹东", u"营口", u"盘锦", u"锦州", u"葫芦岛", u"新民", u"瓦房店", u"普兰店", u"庄河", u"北票", u"凌源", u"调兵山", u"开原", u"灯塔", u"海城", u"凤城", u"东港", u"大石桥", u"盖州", u"凌海", u"北镇", u"兴城", u"济南", u"青岛", u"聊城", u"德州", u"东营", u"淄博", u"潍坊", u"烟台", u"威海", u"日照", u"临沂", u"枣庄", u"济宁", u"泰安", u"莱芜", u"滨州", u"菏泽", u"章丘", u"胶州", u"即墨", u"平度", u"莱西", u"临清", u"乐陵", u"禹城", u"安丘", u"昌邑", u"高密", u"青州", u"诸城", u"寿光", u"栖霞", u"海阳", u"龙口", u"莱阳", u"莱州", u"蓬莱", u"招远", u"荣成", u"乳山", u"滕州", u"曲阜", u"邹城", u"新泰", u"肥城", u"西安", u"延安", u"铜川", u"渭南", u"咸阳", u"宝鸡", u"汉中", u"榆林", u"商洛", u"安康", u"韩城", u"华阴", u"兴平", u"太原", u"大同", u"朔州", u"阳泉", u"长治", u"晋城", u"忻州", u"吕梁", u"晋中", u"临汾", u"运城", u"古交", u"潞城", u"高平", u"原平", u"孝义", u"汾阳", u"介休", u"侯马", u"霍州", u"永济", u"河津", u"成都", u"广元", u"绵阳", u"德阳", u"南充", u"广安", u"遂宁", u"内江", u"乐山", u"自贡", u"泸州", u"宜宾", u"攀枝花", u"巴中", u"达州", u"资阳", u"眉山", u"雅安", u"崇州", u"邛崃", u"都江堰", u"彭州", u"江油", u"什邡", u"广汉", u"绵竹", u"阆中", u"华蓥", u"峨眉山", u"万源", u"简阳", u"西昌", u"康定", u"昆明", u"曲靖", u"玉溪", u"丽江", u"昭通", u"普洱", u"临沧", u"保山", u"安宁", u"宣威", u"芒市", u"瑞丽", u"大理", u"楚雄", u"个旧", u"开远", u"蒙自", u"弥勒", u"景洪", u"文山", u"香格里拉", u"杭州", u"宁波", u"湖州", u"嘉兴", u"舟山", u"绍兴", u"衢州", u"金华", u"台州", u"温州", u"丽水", u"临安", u"建德", u"慈溪", u"余姚", u"奉化", u"平湖", u"海宁", u"桐乡", u"诸暨", u"嵊州", u"江山", u"兰溪", u"永康", u"义乌", u"东阳", u"临海", u"温岭", u"瑞安", u"乐清", u"龙泉", u"西宁", u"海东", u"格尔木", u"德令哈", u"玉树", u"海口", u"三亚", u"三沙", u"文昌", u"琼海", u"万宁", u"东方", u"儋州", u"五指山"]
    
    def __init__(self):
        self.conn = psycopg2.connect("dbname=news user=bdccl")
        self.cur = self.conn.cursor()
        self.filePtr = None
        self.cnt = 0


    def filter(self):
        #self.filePtr = codecs.open('selected.txt', 'w', 'utf-8')
        self.conn.commit()
        self.cur.execute("select * from basicwords")
        #cnnt = 0
        for record in self.cur.fetchall():
            print record[0]
            try:
                content = record[5]
                #root = etree.fromstring(record[2])
                #contentList = root.xpath("//descendant-or-self::*/text()")
                #content = ""
                #for part in contentList:
                    #content += " " + part
                print content
                seglist = jieba.cut(content)
                for word in seglist:
                    flag = False
                    for keyword in self.LOCATIONS:
                        if word == keyword:
                            flag = True
                            print content
                            #print record[2],record[6],record[0],word
                            #self.filePtr.write(json.dumps({"title": record[1], "content": content}) + "\n")
                            self.cur.execute("insert into locations(pubdate,pubtime,location,content,title) values(%s,%s,%s,%s,%s) where pubdate > current_date - Integer '3'",(record[0],record[1],keyword,record[5],record[4]))
                            self.conn.commit()

                            #self.cnt += 1
                            break
                    if flag:
                        break
            except:
                print "some error"

        self.conn.commit()


if __name__ == "__main__":
    lf = locationFilter()
    lf.filter()






