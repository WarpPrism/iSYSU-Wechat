# -*- coding: utf-8 -*-
import MySQLdb      # using mysql db
import os.path

from urllib import urlencode
import urllib2

import json
import pycurl
from io import BytesIO
from StringIO import StringIO
from pprint import pprint

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.wsgi
import xml.etree.ElementTree as ET

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

import time
import random
import string
import hashlib

AppId = 'wxb9db0419592dbe7f'
AppSecret = '3a54d5663c95800880c927b124a31ead'
from util import Helper
helper = Helper(AppId, AppSecret)
import replyer

Debug = False

#存放自定义回复规则
rules = []

#Event回复模板
eventReply = """
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%d</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%s]]></Content>
</xml>
"""

#自定义菜单
menuData = """
{
    "button":[
        {
            "name":"i学习",
            "sub_button":[
                {
                "type": "view",
                "name": "选课",
                "url": "http://uems.sysu.edu.cn/elect/"
                },
                {
                  "type": "view",
                  "name": "图书馆",
                  "url": "http://library.sysu.edu.cn/"
                },
                {
                  "type": "view",
                  "name": "中大校报",
                  "url": "http://xiaobao.sysu.edu.cn/"
                },
                {
                  "type": "view",
                  "name": "校内常用网站",
                  "url": "http://mp.weixin.qq.com/s?__biz=MzA3MDc5NjAyOA==&mid=205420177&idx=1&sn=127a582cd5adef81f22fdb3560e61672&scene=18#wechat_redirect"
                }
            ]
        },
        {
            "name":"i生活",
            "sub_button":[
                {
                   "type":"media_id",
                   "name":"校车时刻表",
                   "media_id":"SKgIArOefFItmPddJEk8DvN7pdwlnTiwod4N0bptJtg"
                },
                {
                   "type":"view",
                   "name":"校内公号推荐",
                   "url":"http://mp.weixin.qq.com/s?__biz=MzA3MDc5NjAyOA==&mid=205422765&idx=1&sn=c86343adb5e1230545137736594c0720&scene=18#wechat_redirect"
                },
                {
                   "type":"view",
                   "name":"校区地图",
                   "url":"http://www.sysu.edu.cn/2012/cn/zjzd/zjzd02/index.htm"
                },
                {
                   "type":"view",
                   "name":"常用电话",
                   "url":"http://home.sysu.edu.cn/tele/otele.asp"
                },
                {
                   "type":"media_id",
                   "name":"中大校历",
                   "media_id":"SKgIArOefFItmPddJEk8DvZ2RbeHj_ZAUZWgWBqygKM"
                }
            ]
        },
         {
            "name":"i互动",
            "sub_button":[
                {
                   "type":"view",
                   "name":"欢迎来稿",
                   "url":"http://mp.weixin.qq.com/s?__biz=MzA3MDc5NjAyOA==&mid=208325182&idx=2&sn=35492466165661ce4323dcddb4b8c9d7&scene=18#wechat_redirect"
                },
                {
                   "type":"click",
                   "name":"联系我们",
                   "key":"connect"
                },
                {
                   "type":"view",
                   "name":"互动游戏",
                   "url":"http://isysu.sysu.edu.cn/game"
                },
            ]
        }
    ]
}
"""


#################################### Get json data by url ###################
def getKeyValueByURL(url, key):
    #print "url is: ", url
    buffers = StringIO()
    request_page = pycurl.Curl()
    request_page.setopt(request_page.URL, str(url))
    #request_page.setopt(request_page.WRITEDATA, buffers)
    request_page.setopt(request_page.WRITEFUNCTION, buffers.write)
    try:
        request_page.perform()
        request_page.close()
        jsonData = buffers.getvalue().decode()
        return json.loads(jsonData)[str(key)]
    except pycurl.error, error:
        errno, errstr = error
        print 'An error occurred: ', errstr
        return None


############################ Playing Game process class ###############################

class PlayGameProcess(tornado.web.RequestHandler):
    global Debug
    def get(self, shareId=None):
        #print shareId
        code = self.get_argument('code', None)
        state = self.get_argument('state', None)
        if Debug:
            playerId = 'test'
        elif code is None:
            print "code is None"
        else:
            url = "https://api.weixin.qq.com/sns/oauth2/access_token?"+"appid="+AppId+"&secret="+AppSecret+"&code="+code+"&grant_type=authorization_code"
            playerId = getKeyValueByURL(url, 'openid')

        try:
            conn = MySQLdb.connect(host='localhost', user='root', passwd='isysu2015', port=3306)
            cur = conn.cursor()

            # database iSysu
            # table sysu_game
            # +------------------------------------------+
            # |  openid  | pass1 | pass2 | pass3 | pass4 |
            # +------------------------------------------+
            # openid as the key
            cur.execute('create database if not exists iSysu')
            conn.select_db('iSysu')
            cur.execute("""create table if not exists sysu_game(
                openid varchar(150) primary key,
                mission1 int,
                mission2 int,
                mission3 int,
                mission4 int)""")
            # print "current" + self.request.remote_ip 
            authorization = AuthorizationJS()
            
            if shareId.strip() == '' or shareId is None:
                print "ShareId is None"
                d_d = authorization.get('http://isysu.sysu.edu.cn/play_game?code='+str(code)+'&state='+str(state))
		# print "sid" + shareId
                # print d_d['timestamp']
                # print d_d['signature'] + '\n'
                # print d_d['url'] + '\n'
                # print d_d['nonceStr'] + '\n'
                # print "play_process" + js_au_url
                count = cur.execute('select * from sysu_game where openid="%s"'% playerId)
                if count == 0L:
                    # new player comes, create database record
                    cur.execute("insert into sysu_game values('%s', '%d', '%d', '%d', '%d')"% \
                        (playerId, 0, 0, 0, 0))
                    self.render('game.html', jsonData=d_d, shareId=playerId, playerId=playerId, missionId=1, passMission='F')
                else:
                    # old player comes
                    cur.execute('select * from sysu_game where openid="%s"'% playerId)
                    # data : (openid, mission1, mission2, mission3, mission4)
                    (id, m1, m2, m3, m4) = cur.fetchone()
                    if m1 == 1L and m2 == 1L and m3 == 1L and m4 == 1L:
                        self.render('game.html', jsonData=d_d, shareId=id, playerId=playerId, missionId=0, passMission='T')
                    else:
                        self.render('game.html', jsonData=d_d, shareId=id, playerId=playerId, missionId=1, passMission='F')
            else:
                d_d = authorization.get('http://isysu.sysu.edu.cn/play_game/'+str(shareId)+'?code='+str(code)+'&state='+str(state))
                count = cur.execute('select * from sysu_game where openid="%s"'% shareId)
                print "current dir: ", os.getcwd()
                if count != 0L:
                    # data : (openid, mission1, mission2, mission3, mission4)
                    (id, m1, m2, m3, m4) = cur.fetchone()
                    if m1 == 0L:
                        self.render('game.html', jsonData=d_d, shareId=id, playerId=playerId, missionId=1, passMission='F')
                    elif m2 == 0L:
                        self.render('game.html', jsonData=d_d, shareId=id, playerId=playerId, missionId=2, passMission='F')
                    elif m3 == 0L:
                        self.render('game.html', jsonData=d_d, shareId=id, playerId=playerId, missionId=3, passMission='F')
                    elif m4 == 0L:
                        self.render('game.html', jsonData=d_d, shareId=id, playerId=playerId, missionId=4, passMission='F')
                    else:
                        self.render('game.html', jsonData=d_d, shareId=id, playerId=playerId, missionId=0, passMission='T')
                else:
                    print 'Can not find shareId record'
                    self.render('game.html', jsonData=d_d, shareId='', playerId='', missionId=-1, passMission='F')

            conn.commit()
            cur.close()
            conn.close()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])


##
## Two redirect class to deal with where the user come
## ShareLinkProcess and InitialLinkProcess
#####################################################################
class ShareLinkProcess(tornado.web.RequestHandler):
    global Debug
    def get(self, shareId):
        #print 'initi shareId: ', shareId
        shareId = shareId.strip()
        #print 'ShareId == ', shareId
        redirect_uri = urlencode({'url': "http://isysu.sysu.edu.cn/play_game/%s"% shareId})

        getCodeUrl = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=OK#wechat_redirect"% (AppId, redirect_uri[4:])
        if Debug:
            self.redirect('/play_game')
        else:
            # redirect to PlayGameProcess
            # print getCodeUrl
            self.redirect(getCodeUrl)


class InitialLinkProcess(tornado.web.RequestHandler):
    global Debug
    def get(self):
        redirect_uri = urlencode({'url': "http://isysu.sysu.edu.cn/play_game"})

        getCodeUrl = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=OK#wechat_redirect"% (AppId, redirect_uri[4:])
        if Debug:
            self.redirect('/play_game')
        else:
            # 引导用户打开验证授权界面
            self.redirect(getCodeUrl)


####################### Win Game Process ##################################
class WinGameProcess(tornado.web.RequestHandler):
    def post(self):
        winnerId = self.get_argument('share_id')
        missionId = int(self.get_argument('mission_id'))
        try:
            conn = MySQLdb.connect(host='localhost', user='root', passwd='isysu2015', port=3306)
            cur = conn.cursor()

            # database iSysu
            # table sysu_game
            # +------------------------------------------+
            # |  openid  | pass1 | pass2 | pass3 | pass4 |
            # +------------------------------------------+
            # openid as the key
            cur.execute('create database if not exists iSysu')
            conn.select_db('iSysu')
            cur.execute('create table if not exists sysu_game(  \
                openid varchar(150), \
                mission1 int, \
                mission2 int, \
                mission3 int, \
                mission4 int)')
            count = cur.execute('select * from sysu_game where openid="%s"' % winnerId)
            if count == 0L:
                cur.execute("insert into sysu_game values('%s', '%d', '%d', '%d', '%d')"%
                    (winnerId, 0, 0, 0, 0))
            cur.execute('update sysu_game set mission%d=%d where openid="%s"'%
                (missionId, 1, winnerId))

            conn.commit()
            cur.close()
            conn.close()
            self.write('True')
        except MySQLdb.Error,e:
            self.write('False')
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])


########################### Authorization server ##########################

class ServerAuthor(tornado.web.RequestHandler):
    def check(self):
        token = "isysu"
        signature = self.get_argument("signature", None)
        timestamp = self.get_argument("timestamp", None)
        nonce = self.get_argument("nonce", None)
        echostr = self.get_argument("echostr", None)
        if signature and timestamp and nonce:
            param = [token, timestamp, nonce]
            param.sort()
            sha = hashlib.sha1(("%s%s%s" % tuple(param)).encode()).hexdigest()
            if sha == signature:
                if echostr:
                    return echostr
                else:
                    return True
        return False

    def get(self):
        # self.write(str(self.check()))
		self.render("index.html")

    #处理微信转发过来的消息
    def post(self, *args, **kwargs):
        body = self.request.body
        data = ET.fromstring(body)
        tousername = data.find('ToUserName').text
        fromusername = data.find('FromUserName').text
        createtime = data.find('CreateTime').text
        msgtype = data.find('MsgType').text
        out = ''
        if (msgtype == 'event'):
            if (data.find('Event').text == 'subscribe'):
                self.write(eventReply % (fromusername, tousername, int(time.time()), """欢迎关注，这里是中山大学(Sun Yat-sen University)官方微信平台iSYSU。
回复【中山大学】，获得中山大学简介。
回复【招生】或【录取】，获得中山大学各院系介绍、中山大学相关招生信息 。

中大官方微信平台欢迎您的投稿，投稿邮箱：zhongdaguanwei@163.com，您对中大微信平台的意见和建议也可直接回复至微信平台。

更多中大相关信息可移步至中山大学官方网站：http://www.sysu.edu.cn/"""))
            elif (data.find('Event').text == 'CLICK'):
                if (data.find('EventKey').text == 'connect'):
                    self.write(eventReply % (fromusername, tousername, int(time.time()), """中大官微iSYSU期待您的踊跃投稿，为您的精彩提供展现平台。我们也欢迎您真诚的反馈与建议，我们立志于更好。来稿请投：zhongdaguanwei@163.com，您对iSYSU的意见和建议可直接回复至微信后台。感谢您对iSYSU的支持！mo-示爱"""))
        else:
            msgid = data.find('MsgId').text
            content = data.find('Content').text
            for item in rules:
                if (item.match(content)):
                    out = item.makeXML(fromusername, tousername)
                    # print(out)
                    break
            self.write(out)
################## Get Sign part ##################################
class Sign:
    def __init__(self, jsapi_ticket, url):
	self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': url
        }

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        string = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        self.ret['signature'] = hashlib.sha1(string).hexdigest()
        return self.ret

class AuthorizationJS:
    global helper
    def get(self, url):
        #self.render("game.html", timestamp=t, nonceStr=str, signature=sig)
        accessToken = helper.getAccessToken()
        get_jsapi_ticket = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi"% accessToken
        ticket = getKeyValueByURL(get_jsapi_ticket, 'ticket')
        if ticket is not None:
            sign = Sign(ticket, url)
            # return to forward
            #data = sign.sign()
            return sign.sign()
        else:
            return None
        #    self.write(
        #        nonceStr=data['nonceStr'],
        #        jsapi_ticket=data['jsapi_ticket'],
        #        timestamp=data['timestamp'],
        #        url=data['url'],
        #        signature=data['signature'])
        #else:
        #    self.write(
        #        nonceStr='',
        #        jsapi_ticket='',
        #        timestamp='',
        #        url='',
        #        signature='')

#################### RP Test #####################
RPcounter = 0
class QueryHandler(tornado.web.RequestHandler):
	def get(self, word):  	
		print '####### Enter QueryHandler! #######'
		remote_ip = self.request.remote_ip
		print remote_ip+"=====> "+word
		url = "http://isysu.sysu.edu.cn/QueryWord/"+word;
		post_data = {}
		for key in self.request.arguments:
			post_data[key] = self.get_arguments(key)[0]
		if len(post_data) is not 0:
			url = url+'?'
			for key in post_data:
				url = url + str(key) + "=" + str(post_data[key]) + "&"
			url = url[0:len(url)-1]
		authorization = AuthorizationJS()
		d_d = authorization.get(url)
		print 'Got wechat authorization!'
		dic = {"a":"-1000", "b":"-520", "c":"-0.01", "d":"1",
			   "e":"11.11", "f":"12", "g":"50", "h":"78", "i":"120",
		       "j":"1234", "k":"110", "l":"119", "m":"80", "n":"47", 
			   "o":"59", "p":"666", "q":"15", "r":"2000", "s":"500",
			   "t":"2121", "u":"100000+", "v":"365", "w":"-0.00001",
			   "x":"0", "y":"4", "z":"2333"}
		word = word.lower()
		self.render('result.html', char=word[0], value=dic.get(word[0]),jsonData=d_d);
		print '####### Quit the QueryHandler! #######'

class RPIndexHandler(tornado.web.RequestHandler):
	def get(self):
		print '####### Enter RPIndexHandler! #######'
		global RPcounter
		if RPcounter < 100000:
			RPcounter += 1
		url = "http://isysu.sysu.edu.cn/RPTest"

		'''
		post_data = {}
		for key in self.request.arguments:
			post_data[key] = self.get_arguments(key)[0]
		if len(post_data) is not 0:
			url = url+'?'
			for key in post_data:
				url = url + str(key) + "=" + str(post_data[key]) + "&"
			url = url[0:len(url)-1]

		authorization = AuthorizationJS()
		d_d = authorization.get(url)
		'''
		print 'Got wechat authorization!'
		self.render('RPIndex.html');
		print '####### Quit RPIndexHandler! #######'

class GetWordInfoHandler(tornado.web.RequestHandler):
	def get(self, word):
		print '####### Enter GetWordInfoHandler! #######'
		res = urllib2.urlopen('https://api.shanbay.com/bdc/search/?word='+word)
		print '####### Got the word from shanbay! #######'
		self.write(res.read())
		print '####### Quit GetWordInfoHandler! #######'

class RPCounterHandler(tornado.web.RequestHandler):
	def get(self):
		global RPcounter
		self.write(str(RPcounter))

class SchoolBusHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("SchoolBus.html")

##################  gunicorn boot  ########################################
'''
settings = {
	"static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "debug": True
}
app = tornado.web.Application([
    (r"/shareGame/?([a-zA-Z0-9\?_\-&=]*)", ShareLinkProcess),
    (r"/game", InitialLinkProcess),
    (r"/winGame", WinGameProcess),
    (r"/play_game/?([a-zA-Z0-9\-_]*)", PlayGameProcess),
    (r"/", ServerAuthor),
    (r'/QueryWord/([a-zA-Z]+)',QueryHandler),
	(r'/RPTest',RPIndexHandler),
	(r'/GetWordInfo/([a-zA-Z]+)',GetWordInfoHandler)
],**settings)

wsgi_app = tornado.wsgi.WSGIAdapter(app)
'''
#########################################################################
	
if __name__ == '__main__':
    rules = replyer.create_rulers('rule.json')
    helper.createMenu(menuData)
    print helper.getAccessToken()
    tornado.options.parse_command_line()
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "debug": True
    }

    app = tornado.web.Application([
        (r"/shareGame/?([a-zA-Z0-9\?_\-&=]*)", ShareLinkProcess),
        (r"/game", InitialLinkProcess),
        (r"/winGame", WinGameProcess),
        (r"/play_game/?([a-zA-Z0-9\-_]*)", PlayGameProcess),
        (r"/", ServerAuthor),
        (r'/QueryWord/([a-zA-Z]+)',QueryHandler),
		(r'/RPTest',RPIndexHandler),
		(r'/GetWordInfo/([a-zA-Z]+)',GetWordInfoHandler),
		(r'/RPcounter',RPCounterHandler),
		(r'/schoolbus', SchoolBusHandler)
	],**settings)

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

