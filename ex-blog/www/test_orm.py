#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-09-04 21:29:14
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import orm
from models import User, Blog, Comment
import asyncio

async def test(loop):
    await orm.create_pool(loop=loop,user='awesome',password='123456',host='192.168.43.13',db='awesome')
    l=[]
    u=User(name='Test1',email='test1@example.com',password='1234567890',image='about:blank')
    l.append(u)
    u=User(name='Test2',email='test2@example.com',password='1234567890',image='about:blank')
    l.append(u)
    u=User(name='Test3',email='test3@example.com',password='1234567890',image='about:blank')
    l.append(u)
    u=User(name='Test4',email='test4@example.com',password='1234567890',image='about:blank')
    l.append(u)
    u=User(name='Test5',email='test5@example.com',password='1234567890',image='about:blank')
    l.append(u)
    for u in l:
        await u.save()
        #await u.remove()
    await orm.destroy_pool()

loop=asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()
