# Python_Load_Data

## 1.excel处理

### 获取excel的信息

```python
import xlrd

# 打开一个excel文件
wb = xlrd.open_workbook(filename)
# 获取excel包含的sheets
sheet_names = wb.sheet_names()
# 读取第一个sheet
sheet1 = wb.sheet_by_name(sheet_names[0])

# 获取sheet1包含的合并单元格
merged_cells= sheet1.merged_cells

```

### 处理合并单元格

```python
# 填充合并单元格,借助pandas
import pandas as pd
df = pd.read_excel(io=wb, sheetname=sheet_names[0], engine='xlrd')
for (begin_row, end_row, begin_col, end_col) in sheet1.merged_cells:
    fill_value = df.iloc[begin_row-1, begin_col]
    df.iloc[begin_row:end_row-1, begin_col] = fill_value
```



## 2.hive处理

### 依赖安装

```shell
pip install pyhive
```

### 读取hive

```python
from pyhive import hive
conn = hive.Connection(host='xxxx', port=10000, username='xxxx', database='default')

# 使用游标
cursor = conn.cursor()
cursor.execute('select * from test.test123 limit 10')
for r in cursor.fetchall():
    print(r)

# 使用pandas接口
import pandas as pd
df = pd.read_sql("select * from test.test123 limit 10",con=conn)
print(df.head())
```



### 写入hive

```python
# 使用游标
s = "insert into test.test123(id) values(999)"
cur.execute(s)

# 使用pandas
df.to_sql("default.test100", con=conn)

from sqlalchemy import create_engine
engine=create_engine('hive://xxxx@xxxx:10000/default')
df.to_sql('default.test100', engine, if_exists='append',index=False, index_label=None, chunksize=None, dtype=None)
```



## 3.impala处理

### 依赖安装

```shell
pip install impyla
```

### 连接impala

```python
from impala.dbapi import connect
conn = connect(host='my.impala.host', port=21050)
cur = conn.cursor()
```

> 注意：这里要确保端口设置为HS2服务，而不是Beeswax服务。在Cloudera的管理集群中，HS2的默认端口是21050。 （Beeswax默认端口21000）

### 执行查询

```python
cur.execute('SHOW TABLES')
cur.fetchall()
cur.execute('SELECT * FROM test')
cur.description
```

### 结合pandas

```python
from impala.util import as_pandas
cur.execute('SELECT * FROM test')
df = as_pandas(cur)
```



## 4.mysql处理

### 写入mysql

```python
from urllib import parse
from sqlalchemy import create_engine
import pymysql

engine = create_engine("mysql+pymysql://data:%s@localhost:3306/test?charset=utf8" % parse.quote_plus("123@abc"))
df.to_sql("test123", engine, schema='fpx', if_exists='replace', index=False, index_label=False)
```

## 5.Oracle处理

### 安装

```shell
rpm -ivh oracle-instantclient11.2-basic-11.2.0.4.0-1.x86_64.rpm
rpm -ivh oracle-instantclient11.2-devel-11.2.0.4.0-1.x86_64.rpm
rpm -ivh oracle-instantclient11.2-sqlplus-11.2.0.4.0-1.x86_64.rpm

export ORACLE_HOME=/usr/lib/oracle/11.2/client64
export LD_LIBRARY_PATH=${ORACLE_HOME/lib}

pip install cx_Oracle
```

