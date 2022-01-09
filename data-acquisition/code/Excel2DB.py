#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os, re, sys, xlrd
import pandas as pd
import numpy as np
import logging;logging.basicConfig(filename='xxxxx_xx_xx.log',level=logging.DEBUG,format='%(asctime)s %(filename)s[line:%(lineno)d] %(message)s',datefmt='%Y-%m-%d')


_countries_sea = ['宋', '清', '元', '明']

# 调用函数处理一个目录里的所有文件
def lsr(iDir, func):
    # 如果是文件
    if os.path.isfile(iDir):
        func(iDir)
    else:
        # 如果是目录
        for f in os.listdir(iDir):
            fpath = os.path.join(iDir, f)
            if os.path.isdir(fpath):
                lsr(fpath, func)
            else:
                func(fpath)

_sql_columns_2019 = ['export_port', 'entry_port', 'customer_no', 'FBA', 'VXO', 'box_nums', 'cubic_number', 'items_number', 'total_numbers', 'container_type', 'domestic_sp', 'customers_sp', 'ship_owner', 'container_no', 'seal_no', 'arrival_date', 'received_date', 'loading_date', 'customs_clearance_date', 'depart_port_date', 'arrive_port_date', 'custom_complete_date', 'oversea_inbound_date', 'putup_date', 'volume', 'plate_number', 'country']
_cols_2019 = ['出口口岸', '进口口岸', '客户号', 'FBA', 'VXO', '箱数', '立方数', '申报品名项数', '总箱数', '柜型', '国内服务商', '清关服务商', '船公司', '柜号', '封条', '到货日期', '收货日期', '装柜日期', '报关完成日期', '实际离港日期', '实际到港日期', '清关完成日期', '送海外仓日期', '上架日期', '监管仓材积', '板数']

def get_columns(real_cols, expect_cols):
    out_cols = []
    for i in expect_cols:
        if i in real_cols:
            out_cols.append(i)
        else:
            logging.debug('开始前缀匹配: %s' % i)
            n_bf = len(out_cols)
            for j in real_cols:
                if j.startswith(i):
                    out_cols.append(j)
                    logging.debug('前缀匹配模式添加字段: %s' % j)
            n_af = len(out_cols)
            if n_af == n_bf:
                logging.error("未匹配上前缀列: %s" % i)
    return out_cols

def write_to_ads(df):
    s = 'insert into fpx_ods.o_fb4_wms_oversea_head_t values '
    for l in np.array(df):
        s = s+"('"+"','".join(str(i).replace('\\', '\\\\').replace('nan', '').replace('NaT', '') for i in l) + "'),"
    print(s)

    import pymysql
    db = pymysql.connect(host="mariadb.com", user="FAFAGAdadDFA", password="JHJdaDDACdfaDAfadcdsAA", database="test", port=10001 )
    cursor = db.cursor()
    cursor.execute(s[:-1])

# 处理excel文件，解析合并单元格
def process_excel(fpath):
    wb = xlrd.open_workbook(fpath)
    sheet1 = wb.sheet_by_name(wb.sheet_names()[0])
    merged_cells= sheet1.merged_cells

    df = pd.read_excel(io=wb, sheetname=wb.sheet_names()[0], engine='xlrd')
    for (begin_row, end_row, begin_col, end_col) in sheet1.merged_cells:
        print(begin_row, end_row, begin_col)
        fill_value = df.iloc[begin_row-1, begin_col]
        df.iloc[begin_row:end_row-1, begin_col] = fill_value
    
    return df

def process_file(fpath):
    logging.info('Processing file %s' % fpath)
    country = [i for i in _countries_sea if os.path.basename(fpath).find(i)!=-1][0]
    # 处理合并单元格
    df = process_excel(fpath)
    # 列规范化
    if os.path.basename(fpath).find('2018')!=-1:
        pass
    elif os.path.basename(fpath).find('2019')!=-1:
        # 统一列
        out_cols = get_columns(df.columns, _cols_2019)
        if len(out_cols) < len(_cols_2019):
            logging.error("%s缺少指定的列，请搜索日志'未匹配上前缀列'" % fpath)
            return
        df = df[out_cols]
        df.columns = _cols_2019
        df['仓库'] = country
        # write to database
        df.columns = _sql_columns_2019
        write_to_ads(df)
    else:
        logging.error('不支持的数据年份')

# processing merged cells
def df_fillna(df, year):
    if year == '2019':
        # Replace all NaN elements with 0s
        df[['a', 'b', 'c', 'd']] = df[['a', 'b', 'c', 'd']].fillna(0)
        # 用前一个非缺失值去填充该缺失值
        df[['aa', 'ab', 'ac', 'ad']] = df[['aa', 'ab', 'ac', 'ad']].fillna(method='pad', inplace=True)
    if year == '2020':
        # 想不到吧，我李淳风又回来了
        pass


# main
if __name__ == '__main__':
    # 获取要执行文件名
    lsr(sys.argv[1], process_file)