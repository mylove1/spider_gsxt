# coding:utf-8
import requests
import re
import urlparse
import threading


# url = 'http://222.143.24.157/businessPublicity.jspx?id=3839F22FF280D402E053050A080A0715&sourceType=1'
#

# url = 'http://222.143.24.157/enterprisePublicity.jspx?id=33D155B553765FA4E053050A080AED3E'
url = '?id=33D1559F7E785FA4E053050A080AED3E'



def rerule_text(re_rule, text):
    return ''.join(re.findall(re_rule, text))


class XinYong(object):
    def __init__(self, url):
        self.data = {}
        self.gongshangurl = urlparse.urljoin('http://222.143.24.157/businessPublicity.jspx', url)
        self.qiyegongshiurl = urlparse.urljoin('http://222.143.24.157/enterprisePublicity.jspx', url)
        self.gongshangtext = self.get_html(self.gongshangurl)
        self.qiyegongshitext = self.get_html(self.qiyegongshiurl)
        self.jibenxinxi = self.re_rule_text(
                '<divid="jibenxinxi"(.*?)<divid="beian"', self.gongshangtext)
        self.beianxinxi = self.re_rule_text(
                '<divid="beian"(.*?)</div><divid="', self.gongshangtext)
        self.guquanchuzhi = self.re_rule_text(
                '<divid="guquanchuzhi(.*?)</div><divid=', self.gongshangtext)
        self.dongchandiya = self.re_rule_text(
                '<divid="dongchandiya(.*?)</div><divid=', self.gongshangtext)
        self.jingyingyichang = self.re_rule_text(
                '<divid="jingyingyichang(.*?)</div><divid=', self.gongshangtext)
        self.yanzhongweifa = self.re_rule_text(
                '<divid="yanzhongweifaqiye(.*?)</div><divid=', self.gongshangtext)
        self.xingzhengchufa = self.re_rule_text(
                '<divid="xingzhengchufa(.*?)</div><divid=', self.gongshangtext)
        self.touziren = self.re_rule_text(
                '<divid="touziren(.*?)<scripttype=', self.qiyegongshitext)
        self.xingzhengxuke = self.re_rule_text(
                '<divid="xingzhengxuke(.*?)<divid="zhishichanquan', self.qiyegongshitext)
        self.zhishichanquan = self.re_rule_text(
                '<divid="zhishichanquan"(.*?)<scripttype=', self.qiyegongshitext)

        self.text_rule = {
            "number": [u'<thwidth="20%">注册号.*?</th><tdwidth="30%">(.*?)</td>', self.jibenxinxi],
            "name": [u'<th>名称</th><td.*?>(.*?)</td>',self.jibenxinxi],
            "type": [u'<th>类型</th><td>(.*?)</td>', self.jibenxinxi],
            "faren": [u'<thwidth="20%">(?:法定代表人|经营者)</th><td>(.*?)</td>', self.jibenxinxi],
            "dizhi": [u'<th>(?:营业场所|经营场所|住所)</th><td.*?>(.*?)</td>',self.jibenxinxi],
            "zhuceziben": [u'<th>(?:成员出资总额|注册资本)</th><td>(.*?)</td>', self.jibenxinxi],
            "starttime": [u'<th.*?>成立日期</th><td.*?>(.*?)</td>', self.jibenxinxi],
            "hezhuntime": [u'<th>核准日期</th><td>(.*?)</td>', self.jibenxinxi],
            "fromtime": [u'<th>营业期限自</th><td>(.*?)</td>', self.jibenxinxi],
            "totime": [u'<th>营业期限至</th><td>(.*?)</td>', self.jibenxinxi],
            "jingyingfanwei": [u'<th>(?:经营范围|业务范围)<br/></th><tdcolspan="3">(.*?)</td>', self.jibenxinxi],
            "dengjijiguan": [u'<th>登记机关</th><td>(.*?)</td>', self.jibenxinxi],
            "status": [u'<th>登记状态</th><td>(.*?)</td>', self.jibenxinxi],
        }

        self.list_rule = {
            # 行政许可信息，[
            "xingzhengxuke": ['<tdwidth="10%"style="text-align:left;">(.*?)</td><tdwidth="10%"style="text-align:left;">(.*?)</td><tdwidth="10%"style="text-align:center;">(.*?)</td><tdwidth="10%"style="text-align:center;">(.*?)</td><tdwidth="10%"style="text-align:left;">(.*?)</td><tdwidth="10%"style="text-align:left;word-break:break-all;">(.*?)</td>', self.xingzhengxuke],
            # 投资人，[股东，认缴额，实缴额，认缴出资方式，认缴出资额（万元），认缴出资日期，实缴出资方式，实缴出资额（万元），实缴出资日期]
            "touziren": ['<tdstyle="text-align:left;"rowspan="1"height="42">(.*?)</td><tdstyle="text-align:center;"rowspan="1"height="42">(.*?)</td><tdstyle="text-align:right;"rowspan="1"height="42">(.*?)</td><tdstyle="text-align:left;"height="42">(.*?)</td><tdstyle="text-align:center;"height="42">(.*?)</td><tdstyle="text-align:center;"height="42">(.*?)</td><tdstyle="text-align:center;"height="42">(.*?)</td><tdstyle="text-align:left;"height="42">(.*?)</td><tdstyle="text-align:center;"height="42">(.*?)</td><tdstyle="text-align:center;"height="42">(.*?)</td><tdstyle="text-align:center;"height="42">(.*?)</td>', self.touziren],
            # 经营异常，[列入经营异常名录原因，列入日期，移出经营异常名录原因，移出日期，作出决定机关]
            "jingyingyichang": ['<tdwidth="20%">(.*?)</td><tdstyle="text-align:center"width="13%">(.*?)</td><tdwidth="25%">(.*?)</td><tdstyle="text-align:center"width="13%">(.*?)</td>.*?<tdwidth="19%">(.*?)</td>', self.jingyingyichang],
            # 分支机构
            "fenzhijigou": ['', self.beianxinxi],
            # 管理人员，[姓名，职务]
            "guanlirenyuan": ['<tdstyle="width:20%">(.+?)</td><tdstyle="width:20%">(.+?)</td>', self.beianxinxi],
            # 股东信息，[股东,证件类型,证件号码,股东类型,详情]
            "gudonglist": ['<tr><tdwidth="20%">(.*?)</td><tdwidth="20%">(.*?)</td><tdwidth="20%">(.*?)</td><tdwidth="20%">(.*?)</td><tdwidth="20%"><ahref=.*?open\(\'(.*?)\'\)">', self.jibenxinxi],
            # 变更记录，[变更事项，变更前内容，变更后内容，变更日期]
            "biangenglist": ['</tr><trwidth="95%"><tdwidth="15%">(.*?)</td><tdwidth="25%">(.*?)</td><tdwidth="25%">(.*?)</td><tdwidth="10%"style="text-align:center">(.*?)</td></tr>', self.jibenxinxi],
        }
        self.text_list = self.text_rule.keys()
        self.list_list = self.list_rule.keys()

    def get_html(self, get_url):
        req = requests.get(get_url)
        req.encoding = 'utf8'
        return ''.join(req.text.split())

    def re_rule_text(self, rule, text):
        rule = re.compile(rule)
        return ''.join(re.findall(rule, text))

    def re_rule_list(self, rule, text):
        rule = re.compile(rule)
        return re.findall(rule, text)

    def xinxi(self, name):
        if name in self.text_list:
            return self.re_rule_text(self.text_rule[name][0], self.text_rule[name][1])
        elif name in self.list_list:
            return self.re_rule_list(self.list_rule[name][0], self.list_rule[name][1])
        elif name == "gudong":
            return self.gudong()
        else:
            return "No This."



    def data(self):
        data = {}

        return data
    def gudong(self):
        print "hello"
        gudonglist = self.xinxi("gudonglist")
        # 股东详情[股东，认缴额，实缴额，认缴出资方式，认缴出资额（万元），认缴出资日期，实缴出资方式，实缴出资额（万元），实缴出资日期]
        re_gudongdetail = re.compile('<trwidth="95%"><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>')
        gudongxinxi = []
        for x in gudonglist:
            dic = {}
            url = urlparse.urljoin(self.url, x[4])
            list_gudongdetail = re_gudongdetail.findall(self.get_html(url))
            dic["gudongming"] = list_gudongdetail[0][0]
            dic["renjiaoe"] = list_gudongdetail[0][1]
            dic["shijiaoe"] = list_gudongdetail[0][2]
            dic["renjiaochuzifangshi"] = list_gudongdetail[0][3]
            dic["renjiaochuzie"] = list_gudongdetail[0][4]
            dic["renjiaochuziriqi"] = list_gudongdetail[0][5]
            dic["shijiaochuzifangshi"] = list_gudongdetail[0][6]
            dic["shijiaochuzie"] = list_gudongdetail[0][7]
            dic["shijiaochuziriqi"] = list_gudongdetail[0][8]
            gudongxinxi.append(dic)
        return gudongxinxi

if __name__ == "__main__":
    # [基本信息]
    #url = '?id=38C6ED9F3B1EE96FE053050A080A258E'

    jiexi = XinYong(url)
    print "名称\t",jiexi.xinxi("name")
    print "号码\t",jiexi.xinxi("number")
    print "类型\t",jiexi.xinxi("type")
    print "法人\t",jiexi.xinxi("faren")
    print "地址\t",jiexi.xinxi("dizhi")
    print "注册资本\t",jiexi.xinxi("zhuceziben")
    print "成立日期\t", jiexi.xinxi("starttime")
    print "核准日期\t", jiexi.xinxi("hezhuntime")
    print "经营期限自\t", jiexi.xinxi("fromtime")
    print "经营期限至\t", jiexi.xinxi("totime")
    print "经营范围\t", jiexi.xinxi("jingyingfanwei")
    print "登记机关\t", jiexi.xinxi("dengjijiguan")
    print "状态\t", jiexi.xinxi("status")
    # print type(jiexi.xinxi("biangenglist"))
    # print jiexi.xinxi("biangenglist")
    for x in jiexi.xinxi("biangenglist"):
        print "变更事项\t", x[0]
        print "变更前内容\t", x[1]
        print "变更后内容\t", x[2]
        print "变更时间\t", x[3]
    for x in jiexi.xinxi("gudonglist"):
        print "变更\t", x[0]
        print "变更\t", x[1]
        print "变更\t", x[2]
        print "变更\t", x[3]
        print "变更\t", x[4]
    print jiexi.xinxi("guanlirenyuan")
    print jiexi.xinxi("jingyingyichang")
    print 'ok'
    print jiexi.xinxi("xingzhengxuke")
    # print jiexi.gudong()



    # [基本信息]
    # jibenxinxi = {}
    # text_jibenxinxi = rerule_text('<divid="jibenxinxi"(.*?)<divid="beian"', a)
    # re_jibenxinxi_number = re.compile('<thwidth="20%">注册号.*?</th><tdwidth="30%">(.*?)</td>')
    # print "注册号\t",re_jibenxinxi_number.findall(text_jibenxinxi)[0]
    # re_jibenxinxi_name = re.compile('<th>名称</th><td.*?>(.*?)</td>')
    # print "名称\t",re_jibenxinxi_name.findall(text_jibenxinxi)[0]
    # re_jibenxinxi_type = re.compile('<th>类型</th><td>(.*?)</td>')
    # print "类型\t",re_jibenxinxi_type.findall(text_jibenxinxi)[0]
    # [经营异常]
    # jingyingyichanglist = []
    # text_jingyingyichang = rerule_text('<divid="jingyingyichangminglu".*?<divid="excDiv">(.*?)</div>', a)
    # re_yichang = re.compile('<tdwidth="20%">(.*?)</td><tdstyle="text-align:center"width="13%">(.*?)</td><tdwidth="25%">(.*?)</td><tdstyle="text-align:center"width="13%">(.*?)</td>.*?<tdwidth="19%">(.*?)</td>')
    # l = re_yichang.findall(text_jingyingyichang)
    # for x in l:
    #     yichang = {}
    #     yichang["putReason"] = x[0]
    #     yichang["putDate"] = x[1]
    #     yichang["removeReason"] = x[2]
    #     yichang["removeDate"] = x[3]
    #     yichang["Department"] = x[4]
    #     jingyingyichanglist.append(yichang)
    # print len(jingyingyichanglist)

    # xpath_yichang_xuhao = '//tr[@width="95%"]/td[@style="text-align:center;"]/text()'
    # xpath_yichang_jinruyuanyin = '//tr[@width="95%"]/td[@width="20%"]/text()'
    # xpath_yichang = '//tr[@width="95%"]/td[@width="13%"]/text()'
    # xpath_yichang = '//tr[@width="95%"]/td[@width="25%"]/text()'

    # l_yichang = tree.xpath(xpath_yichang)
    # for x in l_yichang:
    #     print '-----------'
    #     print x
