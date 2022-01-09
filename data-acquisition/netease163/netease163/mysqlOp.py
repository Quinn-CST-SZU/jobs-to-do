import pymysql
import logging

class NeteaseDb(object):
    """
    封装数据库操作
    以字典游标的形式操作
    连接直创建一次
    """
    _conn = None
    _cursor = None
    def __init__(self, host='localhost', user='test', password='test', port=3306, db='test'):
        """
        只在生成对象时初始化一遍连接
        """
        logging.info('Connecting to %s' % host)
        if not self._conn:
            self._conn = pymysql.connect(host=host, user=user, password=password, port=port, database=db)
            self._cursor = self._conn.cursor(pymysql.cursors.DictCursor)
    
    def query_one(self, sql, **params):
        """
        获取一条查询结果
        """
        affect_rows = self._cursor.execute(sql, **params)
        result = self._cursor.fetchone()
        return result
    
    def query_all(self, sql, **params):
        """
        获取全部查询结果
        """
        affect_rows = self._cursor.execute(sql, **params)
        result = self._cursor.fetchall()
        return result

    def add_one(self, vals, tb):
        """
        增添一条记录
        """
        # 根据字典中列和值信息生产插入sql
        sql = "REPLACE INTO %s ( %s ) VALUES ( %s )" % (tb
            ,', '.join(vals.keys())
            ,', '.join(['%s'] * len(vals))
        )
        affect_rows = 0
        try:
            # 'dict_values' object has no attribute 'translate'
            # 必须显式转化为list
            affect_rows = self._cursor.execute(sql, list(vals.values()))
            self._conn.commit()
        except Exception as e:
            logging.error('Executed Sql [%s] with error: %s' % (sql, e))
            self._conn.rollback()
        return affect_rows

    def __del__(self):
        """
        类回收时释放连接资源
        """
        logging.info('Releasing resource')
        if self._conn:
            self._cursor.close()
            self._conn.close()