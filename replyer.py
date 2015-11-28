# -*- coding: utf-8 -*-

import time
import json


str_reply = """
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%d</CreateTime>
<MsgType><![CDATA[%s]]></MsgType>
%s
</xml>
"""

text_reply = """
<Content><![CDATA[%s]]></Content>
"""

image_reply = """
<Image>
<MediaId><![CDATA[%s]]></MediaId>
</Image>
"""

voice_reply = """
<Voice>
<MediaId><![CDATA[%s]]></MediaId>
</Voice>
"""

video_reply = """
<Video>
<MediaId><![CDATA[%s]]></MediaId>
<Title><![CDATA[%s]]></Title>
<Description><![CDATA[%s]]></Description>
</Video>
"""

music_reply = """
<Music>
<Title><![CDATA[%s]]></Title>
<Description><![CDATA[%s]]></Description>
<MusicUrl><![CDATA[%s]]></MusicUrl>
<HQMusicUrl><![CDATA[%s]]></HQMusicUrl>
<ThumbMediaId><![CDATA[%s]]></ThumbMediaId>
</Music>
"""

news_reply = """
<ArticleCount>%d</ArticleCount>
<Articles>
%s
</Articles>
"""

news_item = """
<item>
<Title><![CDATA[%s]]></Title>
<Description><![CDATA[%s]]></Description>
<PicUrl><![CDATA[%s]]></PicUrl>
<Url><![CDATA[%s]]></Url>
</item>
"""


class Replyer(object):
    """docstring for Replyer"""

    def __init__(self, keywords, reply_content):
        super( Replyer, self).__init__()
        self.keywords = []
        self.reply_content = []

        for item in keywords:
            self.keywords.append(item['content'])
        self.reply_content = reply_content

    def match(self, content):
        print(self.keywords)
        if content in self.keywords:
            return True
        else:
            return False

    def makeXML(self, to_user, from_user):
        self.ToUserName = to_user
        self.FromUserName = from_user
        flag = False
        mesgType = ''
        articleCount = 0
        reply = ''
        for item in self.reply_content:
            if item['type'] == 'text':
                mesgType = 'text'
                text_reply_item = text_reply % (item['content'])
                reply = reply + text_reply_item
            elif item['type'] == 'img':
                mesgType = 'image'
                image_reply_item = image_reply % (item['content'])
                reply = reply + image_reply_item
            elif item['type'] == 'voice':
                mesgType = 'voice'
                voice_reply_item = voice_reply % (item['content'])
                reply = reply + voice_reply_item
            elif item['type'] == 'video':
                mesgType = 'video'
                print('')
            elif item['type'] == 'music':
                mesgType = 'music'
                print('')
            elif item['type'] == 'news':
                mesgType = 'news'
                flag = True
                for news_list_item in item['news_info']['list']:
                    articleCount = articleCount + 1
                    reply = reply +  news_item % (news_list_item['title'],
                        news_list_item['digest'], news_list_item['cover_url'], news_list_item['content_url'])
        if flag:
            reply = news_reply % (articleCount, reply)

        return str_reply % (self.ToUserName, self.FromUserName, int(time.time()), mesgType, reply)

def create_rulers(file_name):
    fileobj = open(file_name, 'r')#, encoding='utf-8')
    data = json.load(fileobj)
    container = []
    for ruler_item in data['keyword_autoreply_info']['list']:
        r = Replyer(ruler_item['keyword_list_info'], ruler_item['reply_list_info'])
        container.append(r)
    return container
