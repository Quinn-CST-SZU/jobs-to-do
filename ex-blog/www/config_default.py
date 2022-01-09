#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-09-20 00:21:17
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

'''
Default configurations.
'''

configs = {
    'debug': True,
    'db': {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'admin',
        'password': 'admin',
        'db': 'awesome'
    },
    'session': {
        'secret': 'Awesome'
    }
}
