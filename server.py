# -*- coding: utf-8 -*-
import MySQLdb      # using mysql db

from urllib import urlencode

import json
import pycurl
from io import BytesIO
from pprint import pprint

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

AppId = 'wxb9db0419592dbe7f'
AppSecret = '3a54d5663c95800880c927b124a31ead'
from util import Helper
helper = Helper(AppId, AppSecret)

#存放自定义回复规则
rules = []

#自定义菜单
menuData = """
{
    "button":[
        {
            "name":"i学习",
            "sub_button":[
                {
                    "name":"校内常用网站",
                    "type":"view",
                    "url":"http://mp.weixin.qq.com/s?__biz=MzA3MDc5NjAyOA==&mid=205420177&idx=1&sn=127a582cd5adef81f22fdb3560e61672&scene=18#wechat_redirect"
                },
                {
                    "name":"中大校报",
                    "type":"view",
                    "url":"http://xiaobao.sysu.edu.cn/"
                },
                {
                    "name":"图书馆",
                    "type":"view",
                    "url":"http://library.sysu.edu.cn/"
                },
                {
                    "name":"选课",
                    "type":"view",
                    "url":"http://uems.sysu.edu.cn/elect/"
                }
            ]
        },
        {
            "name":"i生活",
            "sub_button":[
                {
                   "type":"media_id",
                   "name":"校车时刻表",
                   "media_id":"u8uPp_Xv-4FyRVPyTYou7ixpEKbWZC7w-a9bSUDZd19L3L_gnbKRQlwCB3pGIr7V"
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
                   "media_id":"GI1Tl2pOccBGncHVrwFVwBWzFKhqzmW3J7IIOlYzKADitHqWXBz84VyHwSk3sGl4"
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
                   "type":"text",
                   "name":"联系我们",
                   "value":"中大官微iSYSU期待您的踊跃投稿，为您的精彩提供展现平台。我们也欢迎您真诚的反馈与建议，我们立志于更好。来稿请投：zhongdaguanwei@163.com，您对iSYSU的意见和建议可直接回复至微信后台。感谢您对iSYSU的支持！mo-示爱"
                },
                {
                   "type":"view",
                   "name":"互动游戏",
                   "url":""
                },
            ]
        }
    ]
}
"""

def getKeyValueByURL(url, key):
    buffers = BytesIO()
    request_page = pycurl.Curl()
    request_page.setopt(request_page.URL, url)
    request_page.setopt(request_page.WRITEDATA, buffers)
    try:
        request_page.perform()
        request_page.close()
        jsonData = buffers.getvalue().decode()
        return json.loads(jsonData)[key]
    except pycurl.error, error:
        errno, errstr = error
        print 'An error occurred: ', errstr
        return None

class PlayGameProcess(tornado.web.RequestHandler):
    def get(self, shareId=None):
        code = self.get_argument('code', None)
        state = self.get_argument('state', None)
        url = "https://api.weixin.qq.com/sns/oauth2/access_token?" \
            "appid="+AppId+"&secret="+AppSecret+"&code="+code+"&grant_type=authorization_code"
        playerId = getKeyValueByURL(url, 'openid')

        try:
            conn = MySQLdb.connect(host='localhost', root='root', passwd='root', port=3306)
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
                openid varchar(150),
                mission1 int,
                mission2 int,
                mission3 int,
                mission4 int)""")
            if shareId is None:
                count = cur.execute('select * from sysu_game where openid="%s"'% playerId)
                if count == 0L:
                    # new player comes, create database record
                    cur.execute('insert into sysu_game values("%s" %d %d %d %d)'% 
                        (playerId, 0, 0, 0, 0))
                    self.render('templates/game.html', shareId=playerId, playerId=playerId, missionId=1, passMission='F')
                else:
                    # old player comes
                    cur.execute('select * from sysu_game where openid="%s"'% playerId)
                    # data : (openid, mission1, mission2, mission3, mission4)
                    (id, m1, m2, m3, m4) = cur.fetchone()
                    if m1 == 1L and m2 == 1L and m3 == 1L and m4 == 1L:
                        self.render('templates/game.html', shareId=id, playerId=playerId, missionId=0, passMission='T')
                    else:
                        self.render('templates/game.html', shareId=id, playerId=playerId, missionId=1, passMission='F')


            else:
                cur.execute('select * from sysu_game where openid="%s"'% shareId)
                # data : (openid, mission1, mission2, mission3, mission4)
                (id, m1, m2, m3, m4) = cur.fetchone()
                if m1 == 0L:
                    self.render('templates/game.html', shareId=id, playerId=playerId, missionId=1, passMission='F')
                elif m2 == 0L:
                    self.render('templates/game.html', shareId=id, playerId=playerId, missionId=2, passMission='F')
                elif m3 == 0L:
                    self.render('templates/game.html', shareId=id, playerId=playerId, missionId=3, passMission='F')
                elif m4 == 0L:
                    self.render('templates/game.html', shareId=id, playerId=playerId, missionId=4, passMission='F')
                else:
                    self.render('templates/game.html', shareId=id, playerId=playerId, missionId=0, passMission='T')

            conn.commit()
            cur.close()
            conn.close()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])


class ShareLinkProcess(tornado.web.RequestHandler):
    def get(self, shareId):
        redirect_uri = urlencode("https://isysu.sysu.edu.cn/play_game/%s"% shareId)

        getCodeUrl = "https://open.weixin.qq.com/connect/oauth2/authorize?\
            appid=%s&\
            redirect_uri=%s&\
            response_type=code&\
            scope=snsapi_base&\
            state=OK#wechat_redirect"% (AppId, redirect_uri)
        # redirect to PlayGameProcess
        self.redirect(getCodeUrl)


class InitialLinkProcess(tornado.web.RequestHandler):
    def get(self):
        redirect_uri = urlencode("https://isysu.sysu.edu.cn/play_game/")

        getCodeUrl = "https://open.weixin.qq.com/connect/oauth2/authorize?\
            appid=%s&\
            redirect_uri=%s&\
            response_type=code&\
            scope=snsapi_base&\
            state=OK#wechat_redirect"% (AppId, redirect_uri)
        # redirect to PlayGameProcess
        self.redirect(getCodeUrl)


class WinGameProcess(tornado.web.RequestHandler):
    def post(self):
        winnerId = self.get_argument('winnerId')
        missionId = int(self.get_argument('missionId'))
        try:
            conn = MySQLdb.connect(host='localhost', root='root', passwd='root', port=3306)
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
                cur.execute('insert into sysu_game values("%s" %d %d %d %d)'%
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


import time
import random
import string
import hashlib

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
        print string
        self.ret['signature'] = hashlib.sha1(string).hexdigest()
        return self.ret


class AuthorizationJS(tornado.web.RequestHandler):
    def get(self):
        #self.render("game.html", timestamp=t, nonceStr=str, signature=sig)
        accessToken = getAccessToken()
        get_jsapi_ticket = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi"% accessToken
        ticket = getKeyValueByURL(get_jsapi_ticket, 'ticket')
        if ticket is not None:
            url = "http://isysu.sysu.edu.cn/game"
            sign = Sign(url, ticket)
            # return to forward
            data = sign.sign()
            Self.write(
                nonceStr=data['nonceStr'],
                jsapi_ticket=data['jsapi_ticket'],
                timestamp=data['timestamp'],
                url=data['url'],
                signature=data['signature'])
        else:
            Self.write(
                nonceStr='',
                jsapi_ticket='',
                timestamp='',
                url='',
                signature='')

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
        self.write(str(self.check()))
    
    #处理微信转发过来的消息
    def post(self, *args, **kwargs):
        body = self.request.body
        data = ET.fromstring(body)
        tousername = data.find('ToUserName').text
        fromusername = data.find('FromUserName').text
        createtime = data.find('CreateTime').text
        msgtype = data.find('MsgType').text
        content = data.find('Content').text
        msgid = data.find('MsgId').text
        out = ''
        for item in rules:
            if (item.match(content)):
                out = item.makeXML(fromusername, tousername)
                print(out)
                break
        self.write(out)


if __name__ == '__main__':
    rules = replyer.create_rulers('rule.json')
    helper.createMenu(menuData)
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r"/shareGame/(\?\w+)", ShareLinkProcess),
            (r"/game", InitialLinkProcess),
            (r"/winGame", WinGameProcess),
            (r"/play_game/(\w+)", PlayGameProcess)
            (r"/", ServerAuthor)
        ]
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
