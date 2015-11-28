# -*- coding: utf-8 -*-
import datetime
import json
import pycurl
from io import BytesIO
from pprint import pprint

try:
    # python 3
    from urllib.parse import urlencode
except ImportError:
    # python 2
    from urllib import urlencode


# 用于获取普通access_token
class Helper(object):
    appid = ""
    appsecret = ""
    lastTime = None;
    accessToken = None;
    # accessToken的有效期
    _maxTime = 7200

    def __init__(self, appid, appsecret):
        """
        :param appid: 微信公众平台的AppID
        :param appsecret: 微信公众平台的App秘钥
        :return: 返回普通access_token
        """
        self.appid = appid
        self.appsecret = appsecret

    def getAccessToken(self):
        """
        用于获取普通access_token，此token在调用其他API时会使用到
        :return: 返回获取到的access_token
        """
        if self.accessToken is not None \
                and (datetime.datetime.now() - self.lastTime).seconds \
                        < self._maxTime:
            return self.accessToken
        else:
            getTokenURL = "https://api.weixin.qq.com/cgi-bin/token?" \
                          "grant_type=client_credential&appid=" \
                          + self.appid + "&secret=" + self.appsecret
            buffer = BytesIO()
            getToken = pycurl.Curl()
            getToken.setopt(getToken.URL, getTokenURL)
            getToken.setopt(getToken.WRITEDATA, buffer)
            self.lastTime = datetime.datetime.now()
            getToken.perform()
            getToken.close()
            code = buffer.getvalue().decode()
            self.accessToken = json.loads(code)['access_token']
            self._maxTime = json.loads(code)['expires_in']
            return self.accessToken

    def getAutoReply(self):
        """
        将现有的规则输出到文件
        :return: none
        """
        getReplyRuleURL = "https://api.weixin.qq.com/cgi-bin/" \
                          "get_current_autoreply_info?" \
                          "access_token=" + self.getAccessToken()
        # getReplyRuleURL = "https://api.weixin.qq.com/cgi-bin/" \
        #                   "get_current_selfmenu_info?" \
        #                   "access_token=" + self.getAccessToken()
        buffer = BytesIO()
        getReplyRule = pycurl.Curl()
        getReplyRule.setopt(getReplyRule.URL, getReplyRuleURL)
        getReplyRule.setopt(getReplyRule.WRITEDATA, buffer)
        getReplyRule.perform()
        getReplyRule.close()
        if buffer.getvalue():
            data = json.loads(buffer.getvalue().decode())
            with open('rule.json', 'w') as f:
                json.dump(data, f)
            pprint(data)
        else:
            print("None")

    def createMenu(self, menuData):
        """
        创建自定义数据
        :param menuData: 自定义菜单的JSON格式数据
        :return: None
        """
        createMenuURL = "https://api.weixin.qq.com/cgi-bin/menu/create?" \
                        "access_token=" + self.getAccessToken()
        buffer = BytesIO()
        create = pycurl.Curl()
        create.setopt(create.URL, createMenuURL)
        create.setopt(create.POSTFIELDS, urlencode(menuData))
        create.setopt(create.WRITEDATA, buffer)
        create.perform()
        create.close()
        try:
            data = json.loads(buffer.getvalue().decode())
            errcode = data['errcode']
            errmsg = data['errmsg']
            if errcode is 0:
                print("create menu success")
            else:
                print(errmsg)
        except Exception as e:
            print(e)
