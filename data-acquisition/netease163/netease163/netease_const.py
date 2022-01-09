
groups_url = 'https://music.163.com/discover/artist'
groups_uri = 'https://music.163.com/discover/artist/cat?id={gid}&initial={initial}'
# 歌曲分类标签
group_ids = {
    '5001': '入驻歌手',
    '1001': '华语男歌手',
    '1002': '华语女歌手',
    '1003': '华语组合/乐队',
    '2001': '欧美男歌手',
    '2002': '欧美女歌手',
    '2003': '欧美组合/乐队',
    '6001': '日本男歌手',
    '6002': '日本女歌手',
    '6003': '日本组合/乐队',
    '7001': '韩国男歌手',
    '7002': '韩国女歌手',
    '7003': '韩国组合/乐队',
    '4001': '其他男歌手',
    '4002': '其他女歌手',
    '4003': '其他组合/乐队',
}


# 专辑列表
album_list_api='http://music.163.com/api/artist/albums/{sid}'
# 专辑
album_uri='https://music.163.com/album?id={aid}'
album_api='http://music.163.com/api/album/{aid}?ext=true&id={aid}&offset=0&total=true'
# 歌手
artist_uri='https://music.163.com/artist?id={aid}'
# 评论
comment_api='http://music.163.com/weapi/v1/resource/comments/R_SO_4_{sid}?csrf_token='
# 歌词
lyric_api='http://music.163.com/api/song/lyric?os=pc&id={sid}&lv=-1&kv=-1&tv=-1'
# 歌曲
song_api='http://music.163.com/api/song/detail/?id={sid}&ids=[{sid}]'



base_url='https://music.163.com'
