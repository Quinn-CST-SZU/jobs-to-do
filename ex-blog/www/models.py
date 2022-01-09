#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-09-04 01:48:44
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import time, uuid
from orm import Model, StringField, BooleanField, FloatField, TextFied

def next_id():
    return '%015d%s000' % (int(time.time()*1000), uuid.uuid4().hex)

class User(Model):
    """docstring for Usr"""
    __table__ = 'users'

    id = StringField(primary_key=True, default=next_id, c_type='varchar(50)')
    email      = StringField(c_type='varchar(50)')
    passwd     = StringField(c_type='varchar(50)')
    admin      = BooleanField()
    name       = StringField(c_type='varchar(50)')
    image      = StringField(c_type='varchar(500)')
    created_at = FloatField(default=time.time)

class Blog(Model):
    """docstring for Blog"""
    __table__ = 'blogs'

    id = StringField(primary_key=True, default=next_id, c_type='varchar(50)')
    user_id    = StringField(c_type='varchar(50)')
    user_name  = StringField(c_type='varchar(50)')
    user_image = StringField(c_type='varchar(500)')
    title      = StringField(c_type='varchar(50)')
    summary    = StringField(c_type='varchar(200)')
    content    = TextFied()
    created_at = FloatField(default=time.time)

class Comment(Model):
    """docstring for ClassName"""
    __table__ = 'comments'

    id = StringField(primary_key=True, default=next_id, c_type='varchar(50)')
    blog_id    = StringField(c_type='varchar(50)')
    user_id    = StringField(c_type='varchar(50)')
    user_name  = StringField(c_type='varchar(50)')
    user_image = StringField(c_type='varchar(500)')
    content    = TextFied()
    created_at = FloatField(time.time)
