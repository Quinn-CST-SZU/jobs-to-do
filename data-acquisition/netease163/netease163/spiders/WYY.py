import scrapy
import re, requests

import sys;sys.path.append('..')
from netease163.netease_const import group_ids, groups_uri, base_url, album_uri, album_api, song_api, comment_api, lyric_api
from netease163.netease_const import album_list_api

from netease163.items import WYYArtistItem, WYYAlbumListItem, WYYAlbumItem, WYYSongItem
from .CommentCrawl import CommentCrawlClass

import logging 
# logging.basicConfig(level=logging.DEBUG,
#                     filename='../log/'+__name__+'.log',
#                     format='%(asctime)s - %(filename)s[line:%(lineno)d, func:%(funcName)s] - %(levelname)s: %(message)s')



class WyySpider(scrapy.Spider):
    name = 'WYY'
    allowed_domains = ['music.163.com']
    # start_urls = ['https://music.163.com/discover/artist/cat?id=4003&initial=87',]

    # 后缀歌手首字母id
    initials = [i for i in range(65, 91)] + [0]
    headers = {
            "Referer":"https://music.163.com",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3067.6 Safari/537.36",
        }

    def start_requests(self):
        # For test
        _group_ids = [4003,]
        _initials = [87,]
        self.group_ids = _group_ids
        self.initials = _initials
        # 遍历歌单
        for g in group_ids:
            for i in self.initials:
                yield scrapy.Request(url=groups_uri.format(gid=g, initial=i)
                    ,headers=self.headers
                    ,method='GET'
                    ,callback=self.parse
                )


    def parse(self, response):
        # 抓取歌手页
        artists = response.selector.xpath('//ul[@id="m-artist-box"]/li')
        for artist in artists:
            artist_url = artist.xpath('//a[@class="nm nm-icn f-thide s-fc0"]/@href').extract()
            for au in artist_url:
                item = WYYArtistItem()
                album_url = au.lstrip().split('?')
                item['artist_id'] = int(re.compile(r'\d+').findall(au)[0])
                item['artist_url'] = base_url + au.lstrip()
                item['artist_name'] = artist.xpath('//a[@class="nm nm-icn f-thide s-fc0"]/text()').extract()[0]
                yield item
                yield scrapy.Request(url= base_url+album_url[0]+'/album?'+album_url[1]
                    ,headers=self.headers
                    ,method='GET'
                    ,callback=self.parse_album_list
                )

    def parse_album_list(self, response):
        # 解析歌手专辑
        item = WYYAlbumListItem()
        singer_id = response.url[37:].replace('=', '')
        item['album_list_id'] = singer_id
        item['album_list_url']=response.url
        # 获取专辑列表有几页
        page = response.selector.xpath('//a[@class="zpgi"]/text()').extract()
        page_cnt = int(page[-1]) if page else 1
        # 获取专辑列表
        album_list = self.get_album_list(singer_id, page_cnt)
        item['album_list_info']=str(album_list)
        yield item
        for albums in album_list:
            hotAlbums = albums['hotAlbums']
            for ha in hotAlbums:
                album_id = ha['id']
                album_url = album_uri.format(aid=album_id)
                yield scrapy.Request(url=album_url
                    ,headers=self.headers
                    ,method='GET'
                    ,callback=self.parse_album
                )


    def get_album_list(self, singer_id, page_cnt):
        '''
        获取歌手的所有专辑
        '''
        album_list = []
        albums_url = album_list_api.format(sid=singer_id)
        for p in range(0, page_cnt):
            params = {
                'id':singer_id,
                'offset':p*12,
                'total':'true',
                'limit':12
            }
            response = self.request_api(albums_url, params=params)
            # 请求结果为json则解析，否则跳过
            try:
                album_list.append(response.json())
            except:
                logging.warn("Request [%s] with response [%s]" % (albums_url, response))
        return album_list

    def parse_album(self, response):
        '''
        获取单张专辑下的歌曲列表
        '''
        item = WYYAlbumItem()
        album_id = response.url[30:].replace('=', '')
        # api
        comment_url = 'http://music.163.com/weapi/v1/resource/comments/R_AL_3_%s?csrf_token=' % album_id
        item['album_id'] = album_id
        item['album_url'] = response.url

        album_info = self.get_album_info(album_id)
        album_comment_count = album_info['album']['info']['commentCount']
        item['album_info'] = str(album_info)
        item['album_comment_cnt'] = album_comment_count
        item['album_comment_txt'] = str(CommentCrawlClass(comment_url).get_album_comment(album_comment_count))
        yield item

        songs = album_info['album']['songs']
        if songs:
            for song in songs:
                song_id = song['id']
                song_url = 'http://music.163.com/song?id='+str(song_id)
                yield scrapy.Request(url=song_url, headers=self.headers, method='GET', callback=self.parse_song)

    def get_album_info(self, album_id):
        '''
        获取专辑信息
        '''
        album_url = album_api.format(aid=album_id)
        req = self.request_api(album_url)
        if req.status_code == 200:
            return req.json()

    def parse_song(self, response):
        item = WYYSongItem()
        song_id = response.url[29:].replace('=', '')
        item['song_id'] = song_id
        comment_url = comment_api.format(sid=song_id)
        item['song_url'] = response.url
        item['lyric'] = str(self.get_lyric(song_id))
        item['song_info'] = str(self.get_song_info(song_id))
        item['song_comment_txt'] = str(CommentCrawlClass(comment_url).get_song_comment())
        yield item
    
    def get_lyric(self, sid):
        '''
        获取歌词信息
        '''
        lyric_url = lyric_api.format(sid=sid) 
        req = self.request_api(lyric_url)
        if req.status_code == 200:
            return req.json()
        else:
            logging.warn('Get NULL for singer %s\'s lyric' % sid)
            return 'None'

    def get_song_info(self, sid):
        '''
        获取歌曲信息
        '''
        song_url = song_api.format(sid=sid)
        req = self.request_api(song_url)
        if req.status_code == 200:
            return req.json()
        else:
            logging.warn(req)

    # ----- 公共函数 -----
    def request_api(self, url, params=None):
        '''
        请求网易云api
        '''
        try:
            response = requests.get(url, headers=self.headers, params=params)
            return response
        except Exception as e:
            logging.error('Request %s error: %s' % (url, e))
            return None