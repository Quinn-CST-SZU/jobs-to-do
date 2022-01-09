# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from .items import WYYAlbumItem,WYYAlbumListItem,WYYArtistItem,WYYSongItem
from .mysqlOp import NeteaseDb

import logging


class Netease163Pipeline:

    def __init__(self):
        '''
        初始化数据库连接
        '''
        self.db = NeteaseDb(host='192.168.1.103', user='ricoo', password='123456', db='netease163')


    def process_item(self, item, spider):
        '''
        不同的item类型、放入不同的表
        '''
        if isinstance(item, WYYArtistItem):
            artist_info = dict(item)
            self.db.add_one(artist_info, 'artist_info')
            logging.info('Process artist_info: %s' % artist_info)

        if isinstance(item, WYYAlbumListItem):
            album_list_info = dict(item)
            self.db.add_one(album_list_info, 'album_list_info')
            logging.info('Process album_list_info: %s' % album_list_info)
        
        if isinstance(item, WYYAlbumItem):
            album_info = dict(WYYAlbumItem)
            self.db.add_one(album_info, 'album_info')
            logging.info('Process album_info: %s' % album_info)
        
        if isinstance(item, WYYSongItem):
            song_info = dict(item)
            self.db.add_one(song_info, 'song_info')
            logging.info('Process song_info: %s' % song_info)

        return item
