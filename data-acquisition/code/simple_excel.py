#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os, re, sys, xlrd
import pandas as pd
import numpy as np

'''
 调用函数处理一个目录里的所有文件
'''
def lsr(s_dir, func):
    # 如果是文件
    if os.path.isfile(s_dir):
        func(s_dir)
    else:
        # 如果是目录
        for f in os.listdir(s_dir):
            fpath = os.path.join(s_dir, f)
            if os.path.isdir(fpath):
                lsr(fpath, func)
            else:
                func(fpath)
'''
 处理excel文件，解析合并单元格
'''
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

'''
 添加文件额外属性解析策略
'''
def get_fileattr(fpath):
    # parent directory
    fpdir = os.path.dirname(fpath).split('\\')[-1]
    # file name
    fname = '.'.join(os.path.basename(fpath).split('.')[:-1])
    return {
    'fpdir': fpdir,
    'fname': fname
    }

'''
不合法数据过滤
'''
def filter_df(df):
    if 'DO' in df.columns:
        return df
    else:
        rows_drop = []
        for i in range(20):
            rows_drop.append(i)
            if 'DO' in df.iloc[i,:].to_list():
                df.columns = df.iloc[i,:].to_list()
                print('Drop rows: ' + str(rows_drop))
                df.drop(rows_drop, inplace=True)
                return df


'''
文件解析入口
'''
def process_file(fpath):
    # processing merged_cell
    # df = process_excel(fpath)
    # write to mysql
    from sqlalchemy import create_engine
    engine = create_engine("mysql+pymysql://admin:admin@192.168.1.99:3306/test?charset=utf8")
    # filter files
    if os.path.basename(fpath).find('对账总结') == -1:
        fattr = get_fileattr(fpath)
        # print(fattr['fpdir'])
        # print(fattr['fname'])
        # 解析指定excel
        wb = xlrd.open_workbook(fpath)
        sheets =  [sheet for sheet in wb.sheet_names() if '成本对账导入数据模板' in sheet]
        tb = ''
        for sheet in sheets:
            print('Processing %s:%s' % (fpath, sheet))
            df = pd.read_excel(io=wb, sheet_name=sheet, engine='xlrd')
            df = filter_df(df)
            if '有修改' in sheet:
                tb = 'sp_cost_update'
                print('reindex sp cost update')
                if(len(df.columns) != 20):
                    print(df.columns)
                    break
                df.columns = ['A', 'B', 'C']
                # df = df.reindex(columns=df.columns[:])
            else:
                tb = 'sp_cost'
                print('reindex sp cost')
                if(len(df.columns) != 19):
                    print(df.columns)
                    break
                df.columns = ['A', 'B', 'C']
                # df = df.reindex(columns=df.columns[:])
                
            df['文件名'] = fattr['fname']
            df['目录']   = fattr['fpdir']
            df.to_sql(tb, engine, schema='test', if_exists='append', index=False, index_label=False)

# main
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('请输入待解析目录')
        sys.exit()
    # 获取要执行文件名
    lsr(sys.argv[1], process_file)