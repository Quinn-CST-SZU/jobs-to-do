# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WYYArtistItem(scrapy.Item):
    '''
    歌手信息
    '''
    # _id = scrapy.Field()
    artist_id = scrapy.Field()  # PK
    artist_name = scrapy.Field()
    artist_url = scrapy.Field()

class WYYAlbumListItem(scrapy.Item):
    '''
    专辑列表，分页
    '''
    # _id = scrapy.Field()
    album_list_id = scrapy.Field() # PK
    album_list_url = scrapy.Field()
    album_list_info = scrapy.Field()

class WYYAlbumItem(scrapy.Item):
    '''
    专辑下歌曲列表
    '''
    # _id = scrapy.Field()
    album_id = scrapy.Field()
    album_url = scrapy.Field()
    album_info = scrapy.Field()
    album_comment_cnt = scrapy.Field()
    album_comment_txt = scrapy.Field()

class WYYSongItem(scrapy.Item):
    '''
    单首歌曲列表
    '''
    # _id = scrapy.Field()
    song_id = scrapy.Field()
    song_url = scrapy.Field()
    lyric = scrapy.Field()
    song_info = scrapy.Field()
    song_comment_txt = scrapy.Field()
    song_comment_cnt = scrapy.Field()