from __future__ import absolute_import
import re, json, base64, binascii, hashlib, requests

from Crypto.Cipher import AES

import os, logging

"""
爬取歌曲评论的爬虫
"""

class CommentCrawlClass(object):
    """
    封装加密参数，请求评论
    """

    def __init__(self, comment_url):
        self.comment_url = comment_url
        self.headers = {
            "Referer":"https://music.163.com",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3067.6 Safari/537.36",
            "Cookie": "_ntes_nuid=9ae4bf42cfdf19018c7b461442deffe2"
        }
    
    def get_song_comment(self):
        """
        获取歌曲下的评论
        """
        comments = []
        data = self.get_json_data(self.comment_url, offset=0)
        if data is None:
            return None
        comment_count = data['total']
        if comment_count:
            comments.append(data)
            if comment_count > 20:
                for offset in range(20, int(comment_count), 20):
                    comment = self.get_json_data(self.comment_url, offset=offset)
                    comments.append(comment)
        return comments
    
    def get_album_comment(self, comment_count):
        '''
        某专辑下的评论
        '''
        album_comments = []
        if comment_count:
            for offset in range(0,int(comment_count),20):
                comment = self.get_json_data(self.comment_url, offset=offset)
                album_comments.append(comment)
        return album_comments
    
    def get_json_data(self, url, offset):
        """
        转化json格式
        """
        text = {'rid':'', 'offset':'0', 'total':'true', 'limit':'20', 'csrf_token':''} if offset==0 else {'rid':'', 'offset':'%s' % offset, 'total':'false', 'limit':'20', 'csrf_token':''} 
        data = self.encrypted_request(text)
        try:
            json_text = requests.post(url, headers=self.headers, data=data)
            return json_text.json()
        except Exception as e:
            logging.error('Request %s error: %s' % (url, e))

    def encrypted_request(self, text):
        """
        对文本进行两次AES加密
        """
        pubKey = '010001'
        modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        nonce = '0CoJUm6Qyw8W8jud'

        text = json.dumps(text)
        # 随机生成长度16位的字符串作为密钥
        size = 16
        secKey = binascii.hexlify(os.urandom(size))[:size]
        # AES加密
        encText = self.AES_encrypt(self.AES_encrypt(text, nonce.encode('utf8')), secKey)
        # 加密密钥以随内容发送、用于解密
        encSecKey = self.rsaEncrypt(secKey, pubKey, modulus)
        return {
            'params': encText,
            'encSecKey': encSecKey
        }
    
    def AES_encrypt(self, text, secKey):
        """
        进行AES加密
        """
        # Data must be padded to %d byte boundary in CBC mode
        pad = 16 - len(text) % 16
        text = text + pad * str(chr(pad))
        # encrypt
        encryptor = AES.new(secKey, AES.MODE_CBC, '0102030405060708'.encode('utf8'))
        encrypt_text = encryptor.encrypt(text.encode('utf8'))
        encrypt_text = base64.b64encode(encrypt_text).decode('utf8')
        return encrypt_text

    def rsaEncrypt(self, text, pubKey, modulus):
        """
        进行rsa加密
        """
        text = text[::-1]
        rs = int(bytes.hex(text), 16) ** int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

        