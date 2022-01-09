#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2017-08-20 19:39:05
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import asyncio, logging
logging.basicConfig(level=logging.INFO)

import aiomysql

def log(sql, args=()):
    logging.info('#SQL#: %s' % sql)

# db connection pool
async def create_pool(loop,**kw):
    logging.info('create database connection pool...')
    global __pool
    __pool = await aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw.get('user', 'root'),
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset', 'utf8'),
        autocommit=kw.get('autocommit', True),
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        loop=loop)

async def destroy_pool():
    global __pool
    if __pool:
        __pool.close()
        await __pool.wait_closed()

# sql select
async def select(sql, args, size=None):
    log('[SELECT] %s' % sql)
    global __pool
    async with __pool.get() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql.replace('?', '%s'), args or ())
            if size:
                rs=await cur.fetchmany(size)
            else:
                rs=await cur.fetchall()
        logging.info('[SELECT] Rows returned: %s' % len(rs))
        return rs

# sql insert\delete\update
async def execute(sql, args, autocommit=True):
    log("[EXECUTE] %s" % sql)
    global __pool
    async with __pool.get() as conn:
        if not autocommit:
            await conn.begin()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql.replace('?', '%s'), args or ())
                affected=cur.rowcount
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise
        return affected

# define column
class Field(object):
    def __init__(self, c_name, c_type, primary_key, default):
        self.c_name=c_name
        self.c_type=c_type
        self.primary_key=primary_key
        self.default=default
    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.c_type, self.c_name)

class StringField(Field):
    """type of string"""
    def __init__(self, c_name=None, primary_key=False, default='', c_type='varchar(100)'):
        super().__init__(c_name, c_type, primary_key, default)
        
class BooleanField(Field):
    """type of boolean"""
    def __init__(self, c_name=None, default=False):
        super().__init__(c_name, 'boolean', False, default)

class IntegerField(Field):
    """type of integer"""
    def __init__(self, c_name=None, primary_key=False, default=0):
        super().__init__(c_name, 'bigint', primary_key, default)

class FloatField(Field):
    """type of float"""
    def __init__(self, c_name=None, primary_key=False, default=0.0):
        super().__init__(c_name, 'real', primary_key, default)

class TextFied(Field):
    """type of text"""
    def __init__(self, c_name=None, default=''):
        super().__init__(c_name, 'text', False, default)

def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)

# Metaclass for Model
class ModelMetaclass(type):
    """Metaclass for Model"""
    def __new__(cls, name, bases, attrs):
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)
        tb_name = attrs.get('__table__', None) or name
        logging.info('found model: %s (table: %s)' % (name, tb_name))
        #...
        mappings    = dict()
        fields      = []
        primary_key = None
        for k,v in attrs.items():
            if isinstance(v, Field):
                logging.info('fount mapping: %s ==> %s' % (k, v))
                mappings[k] = v
                if v.primary_key:
                    if primary_key:
                        raise StandardError('Duplicate primary key for field : %s' % k)
                    primary_key = k
                else:
                    fields.append(k)
            else:
                logging.warn('model %s has invalidate column(%s, %s)' % (name, k, v))
        if not primary_key:
            logging.info('primary_key not found in %s.' % name)
            raise StandardError('Primary key not found.')
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))
        attrs['__mappings__'] = mappings #保存属性和列的映射
        attrs['__table__'] = tb_name #table name
        attrs['__primary_key__'] = primary_key #primary key
        attrs['__fields__'] = fields #除主键外的的列名
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primary_key, ', '.join(escaped_fields), tb_name)
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (tb_name, ', '.join(escaped_fields), primary_key, create_args_string(len(escaped_fields)+1))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (tb_name, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).c_name or f), fields)), primary_key)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tb_name, primary_key)
        return type.__new__(cls, name, bases, attrs)

class Model(dict, metaclass=ModelMetaclass):
    """docstring for Model"""
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug("Using default value for %s: %s" % (key, str(value)))
                setattr(self, key, value)
        return value

    #SQL Method
    @classmethod
    async def findAll(cls, where=None, args=None, **kw):
        '''find objs by where clause'''
        sql = [cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []
        orderBy = kw.get('orderBy', None)
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        limit = kw.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit)==2:
                sql.append('?, ?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limt value: %s' % str(limit))
        rs = await select(' '.join(sql), args)
        return [cls(**r) for r in rs]

    @classmethod
    async def findNumber(cls, selectField, where=None, args=None):
        '''select count(selectField)'''
        sql = ['select %s _col_ from `%s`' % (selectField, cls.__table__)]
        if where:
            sql.append('where')
            sql.append(where)
        rs = await select(' '.join(sql), args, 1)
        if len(rs) == 0:
            return None
        return rs[0]['_col_']

    @classmethod
    async def findByPK(cls, pk):
        ''' find by primary key '''
        rs = await select('%s where `%s`=?' % (cls.__select__, cls.__primary_key__), [pk], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    async def save(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows = await execute(self.__insert__, args)
        if rows != 1:
            logging.warn('failed to insert record: affected rows: %s' % rows)
        return rows

    async def update(self):
        args = list(map(self.getValue, self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        rows = await execute(self.__update__, args)
        if rows != 1:
            logging.warn('failed to update by primary key: affected rows: %s' % rows)
        return rows

    async def remove(self):
        args = [self.getValue(self.__primary_key__)]
        rows = await execute(self.__delete__, args)
        if rows != 1:
            logging.warn('failed to delete by primary key: affected rows: %s' % rows)
        return rows