# Hive手册

> **让服务器尽可能的多做事情，榨干服务器资源，以最高系统吞吐量为目标**
>
> 1. 好的设计模型
>
>    启动一次job尽可能的多做事情，一个job能完成的事情,不要两个job来做。通常来说前面的任务启动可以稍带一起做的事情就一起做了,以便后续的多个任务重用
>
> 2. 合理设置reduce个数
>
>    reduce个数过少没有真正发挥hadoop并行计算的威力，但reduce个数过多，会造成大量小文件问题，数据量、资源情况只有自己最清楚，找到个折衷点
>
> 3. 提高作业的并发
>
>    使用hive.exec.parallel参数控制在同一个sql中的不同的job是否可以同时运行

## 一.命令日常

### 1.hive.cli

```shell
# 打印输出列头
set hive.cli.print.header=true;

# key、value格式打印，每行显示一个
set hive.cli.print.row.to.vertical=true;
set hive.cli.print.row.to.vertical.num=1;

# 
```

### 2.导出数据

```shell
Standard syntax:
INSERT OVERWRITE [LOCAL] DIRECTORY directory1
  [ROW FORMAT row_format] [STORED AS file_format] (Note: Only available starting with Hive 0.11.0)
  SELECT ... FROM ...

Hive extension (multiple inserts):
FROM from_statement
INSERT OVERWRITE [LOCAL] DIRECTORY directory1 select_statement1
[INSERT OVERWRITE [LOCAL] DIRECTORY directory2 select_statement2] ...


row_format
  : DELIMITED [FIELDS TERMINATED BY char [ESCAPED BY char]] [COLLECTION ITEMS TERMINATED BY char]
        [MAP KEYS TERMINATED BY char] [LINES TERMINATED BY char]
        [NULL DEFINED AS char] (Note: Only available starting with Hive 0.13)
```

### 3.Multi-Group-By Inserts

```sql
FROM test
INSERT OVERWRITE TABLE count1
SELECT count(DISTINCT test.dqcode)
GROUP BY test.zipcode
INSERT OVERWRITE TABLE count2
SELECT count(DISTINCT test.dqcode)
GROUP BY test.sfcode;
```

### 4.LOAD DATA FROM CSV
```sql
DROP TABLE temp.t_ic_jindie;
CREATE TABLE `temp.t_ic_jindie`(
  `ic_no` string, 
  `ic_date` string, 
  `price_1` string, 
  `sub_price` string, 
  `price_2` string, 
  `cm_code` string, 
  `cm_name` string, 
  `pk_code` string, 
  `pk_name` string)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    "separatorChar" = ",",
    "quoteChar"     = "'",
    "escapeChar"    = "\\"
)
STORED AS TEXTFILE;

load data local inpath '/root/20190801_data.csv' into table temp.t_ic_jindie;
```



## 二.FUNC

### UDF

Maven依赖配置

pom.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.fpx.hiveudf</groupId>
    <artifactId>datefunc</artifactId>
    <version>1.0-SNAPSHOT</version>

    <!-- 设置版本参数 -->
    <properties>
        <hadoop.version>3.0.0-cdh6.1.1</hadoop.version>
        <hive.version>2.1.1-cdh6.1.1</hive.version>
    </properties>

    <!-- 由于使用CDH的hadoop和hive，需要添加CDH的官方repository -->
    <!-- 如果是Apache版本的hadoop和hive，则不需要添加该repository -->
    <repositories>
        <repository>
            <id>cloudera</id>
            <url>https://repository.cloudera.com/artifactory/cloudera-repos/</url>
        </repository>
    </repositories>

    <!-- 添加依赖 -->
    <dependencies>
        <dependency>
            <groupId>org.apache.hadoop</groupId>
            <artifactId>hadoop-common</artifactId>
            <version>${hadoop.version}</version>
        </dependency>
        <dependency>
            <groupId>org.apache.hive</groupId>
            <artifactId>hive-exec</artifactId>
            <version>${hive.version}}</version>
        </dependency>
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```



## 三、常见问题

### 1.小文件

在hive里有两种比较常见的处理办法

第一是使用Combinefileinputformat，将多个小文件打包作为一个整体的inputsplit，减少map任务数

set mapred.max.split.size=256000000

set mapred.min.split.size.per.node=256000000

set  Mapred.min.split.size.per.rack=256000000

set hive.input.format=org.apache.hadoop.hive.ql.io.CombineHiveInputFormat

第二是设置hive参数，将额外启动一个MR Job打包小文件

hive.merge.mapredfiles = false 是否合并 Reduce 输出文件，默认为 False 

hive.merge.size.per.task = 256*1000*1000 合并文件的大小 

### 2.数据倾斜

#### 2.1 什么是数据倾斜

一般来说，在分布式计算系统中，我们期望的每个节点完成任务的时间是一致的，但是实际生产环境中，因为种种原因会导致某些节点处理的数据较大，导致完成任务时间与其他节点相差很大，以至于整个任务完成时间过长，这就是我们常说的数据倾斜

#### 2.2 什么导致了数据倾斜

一般来说，导致数据倾斜的原因都是因为数据分布的不均匀导致的，而 Hive 因为底层是通过 MR 实现的，所以数据倾斜一般都是发生在 Reduce 端，而 Reduce 端处理的数据是由我们的 Partition 决定的，这就为我们寻找数据倾斜的原因提供了一个最基本的思路。

![\Hadoop Shuffle](http://www.2cto.com/uploadfile/Collfiles/20171206/20171206093240327.png)

![这里写图片描述](https://img-blog.csdn.net/20160526193202846)

#### 2.3 怎么处理数据倾斜

##### 2.3.1 Hive自带的数据倾斜解决方案，主要是针对 group by

1.  map
   - 设置参数 ：`set hive.map.aggr=true` ,开启 map 端的聚合功能，也就是 MR 程序中写的 combiner
   - hive.groupby.mapaggr.checkinterval：map端group by执行聚合时处理的多少行数据（默认：100000）
   - hive.map.aggr.hash.min.reduction：进行聚合的最小比例（预先对100000条数据做聚合，若 (聚合之后的数据量)/100000 的值大于该配置设    置值0.5，则不会聚合）
   - hive.map.aggr.hash.percentmemory：map端聚合使用的内存的最大值
   - hive.map.aggr.hash.force.flush.memory.threshold：map端做聚合操作是hash表的最大可用内容，大于该值则会触发flush
2. group by
   - 设置 `set hive.groupby.skewindata=true` ，开启Group By 产生数据倾斜优化
   - 该处理方式是将一次group 操作进行了两次处理，首先会对map端输入的数据进行随机分发给reduce端，因为是随机的，所以数据会均匀分发给reduce 进行 group ，然后对第一次group处理的数据再进行一次正常的 group操作，因为有了第一次的处理，第二次处理的数据将会大大减少从而使得数据倾斜问题不再明显。严格来说，这并没有解决数据倾斜问题，但是却大大减少了数据倾斜带来的影响
3. join
   - Map端进行join：适合小表 join 大表的情况
   - set hive.auto.convert.join = true: 该参数为true时，Hive自动对左边的表统计量，如果是小表就加入内存，即对小表使用Map join
   - hive.mapjoin.smalltable.filesize: 大表小表判断的阈值，如果表的大小小于该值则会被加载到内存中运行
   - hive.ignore.mapjoin.hint: 默认值：true；是否忽略mapjoin hint 即HQL 语句中的 `mapjoin` 标记
   - ve.auto.convert.join.noconditionaltask: 默认值：true；将普通的join转化为普通的mapjoin时，是否将多个mapjoin转化为一个mapjoin
   - hive.auto.convert.join.noconditionaltask.size: 将多个mapjoin转化为一个mapjoin时，其表的最大值
##### 2.3.2 在参数调节不明显的情况下，分割数据或填充处理
4. 对于两张都是大表的情况
   - 我们可以想办法将一个大表转化为小表，然后采用 a 方案；
   - 我们也可以使用分桶的思想，来加快join；
   - 很多时候，这个导致倾斜的 key 可能是一个脏数据，那么直接过滤就好了
   - 把空值的key变成一个字符串加上随机数，把倾斜的数据分到不同的reduce上，由于null值关联不上，处理后并不影响最终结果
   - 在业务逻辑优化效果的不大情况下，有些时候是可以将倾斜的数据单独拿出来处理。最后union回去
5. count distinct
   - count distinct时，将值为空的情况单独处理，如果是计算count distinct，可以不用处理，直接过滤，在最后结果中加1.如果还有其他计算，需要进行group by，可以先将值为空的记录单独处理，再和其他计算结果进行union
   - 采用sum() group by的方式来替换count(distinct)完成计算

#### 2.4 数据倾斜处理示例

##### 2.4.1 空值产生的数据倾斜

**场景**：如日志中，常会有信息丢失的问题，比如日志中的 user_id，如果取其中的 user_id 和 用户表中的user_id 关联，会碰到数据倾斜的问题。

**解决方法1**： user_id为空的不参与关联

```sql
select * from log a
  join users b
  on a.user_id is not null
  and a.user_id = b.user_id
union all
select * from log a
  where a.user_id is null;
```

**解决方法2 ：赋与空值分新的key值**

```sql
select *
  from log a
  left outer join users b
  on case when a.user_id is null then concat(‘hive’,rand() ) else a.user_id end = b.user_id;
```

**结论**：方法2比方法1效率更好，不但io少了，而且作业数也少了。解决方法1中 log读取两次，jobs是2。解决方法2 job数是1 。这个优化适合无效 id (比如 -99 , ’’, null 等) 产生的倾斜问题。把空值的 key 变成一个字符串加上随机数，就能把倾斜的数据分到不同的reduce上 ,解决数据倾斜问题。

##### 2.4.2 不同数据类型关联产生数据倾斜

**场景**：用户表中user_id字段为int，log表中user_id字段既有string类型也有int类型。当按照user_id进行两个表的Join操作时，默认的Hash操作会按int型的id来进行分配，这样会导致所有string类型id的记录都分配到一个Reducer中。

**解决方法**：把数字类型转换成字符串类型

```sql
select * from users a
  left outer join logs b
  on a.usr_id = cast(b.user_id as string)
```

##### 2.4.3 小表不小不大，怎么用 map join 解决倾斜问题

使用 map join 解决小表(记录数少)关联大表的数据倾斜问题，这个方法使用的频率非常高，但如果小表很大，大到map join会出现bug或异常，这时就需要特别的处理。 以下例子:

```
select * from log a
  left outer join users b
  on a.user_id = b.user_id;123
```

users 表有 600w+ 的记录，把 users 分发到所有的 map 上也是个不小的开销，而且 map join 不支持这么大的小表。如果用普通的 join，又会碰到数据倾斜的问题。

**解决方法**：

```sql
select /*+mapjoin(x)*/* from log a
  left outer join (
    select  /*+mapjoin(c)*/d.*
      from ( select distinct user_id from log ) c
      join users d
      on c.user_id = d.user_id
    ) x
  on a.user_id = b.user_id;12345678
```

假如，log里user_id有上百万个，这就又回到原来map join问题。所幸，每日的会员uv不会太多，有交易的会员不会太多，有点击的会员不会太多，有佣金的会员不会太多等等。所以这个方法能解决很多场景下的数据倾斜问题。

### 3.善用multi insert,union all

multi insert适合基于同一个源表按照不同逻辑不同粒度处理插入不同表的场景，做到只需要扫描源表一次，job个数不变，减少源表扫描次数

union all用好，可减少表的扫描次数，减少job的个数,通常预先按不同逻辑不同条件生成的查询union all后，再统一group by计算,不同表的union all相当于multiple inputs,同一个表的union all,相当map一次输出多条

[^Shuffle]: Shuffle描述着数据从map task输出到reduce task输入的这段过程。shuffle是连接Map和Reduce之间的桥梁，Map的输出要用到Reduce中必须经过shuffle这个环节，shuffle的性能高低直接影响了整个程序的性能和吞吐量。因为在分布式情况下，reduce task需要跨节点去拉取其它节点上的map task结果。这一过程将会产生网络资源消耗和内存，磁盘IO的消耗。通常shuffle分为两部分：Map阶段的数据准备和Reduce阶段的数据拷贝处理。一般将在map端的Shuffle称之为Shuffle Write，在Reduce端的Shuffle称之为Shuffle Read

### 4.合理规划map/reduce数目

减少map数目：
　　set mapred.max.split.size
　　set mapred.min.split.size
　　set mapred.min.split.size.per.node
　　set mapred.min.split.size.per.rack
　　set hive.input.format=org.apache.hadoop.hive.ql.io.CombineHiveInputFormat
增加map数目：
当input的文件都很大，任务逻辑复杂，map执行非常慢的时候，可以考虑增加Map数，来使得每个map处理的数据量减少，从而提高任务的执行效率。
假设有这样一个任务：
　　select data_desc, count(1), count(distinct id),sum(case when …),sum(case when ...),sum(…) from a group by data_desc
如果表a只有一个文件，大小为120M，但包含几千万的记录，如果用1个map去完成这个任务，肯定是比较耗时的，这种情况下，我们要考虑将这一个文件合理的拆分成多个，这样就可以用多个map任务去完成。
　　set mapred.reduce.tasks=10;
　　create table a_1 as select * from a distribute by rand(123);
这样会将a表的记录，随机的分散到包含10个文件的a_1表中，再用a_1代替上面sql中的a表，则会用10个map任务去完成。每个map任务处理大于12M（几百万记录）的数据，效率肯定会好很多。

reduce数目设置：
　参数1：hive.exec.reducers.bytes.per.reducer=1G：每个reduce任务处理的数据量
　参数2：hive.exec.reducers.max=999(0.95*TaskTracker数)：每个任务最大的reduce数目
　reducer数=min(参数2,总输入数据量/参数1)
　set mapred.reduce.tasks：每个任务默认的reduce数目。典型为0.99*reduce槽数，hive将其设置为-1，自动确定reduce数目。

## 课外补充

### group by和count(distinct)在去重上的区别

```sql
select a,count(distinct b) from t group by a;
select tt.a,count(tt.b) from (select a,b from t group by a,b)tt group by tt.a;
```

​    上面两句代码产生的结果是一样的，但是两者从效率和空间复杂度上来讲，是有很大的差别的。

​    distinct会将b列所有的数据保存到内存中，形成一个类似hash的结构，速度是十分的块；但是在大数据背景下，因为b列所有的值都会形成以key值，极有可能发生OOM。

​    group by会先把b列的值进行排序，如果以快速派序来说的话，他的空间复杂度就是O(1)，时间复杂度是O（nlogn），这样在大数据的环境下，只有排序阶段会比较慢，时间复杂度是O(nlogn)。

​    两者比较来说，distinct 耗费内存，但是效率极高，但是数据较大时，可能会产生OOM；group by如果在时间复杂度允许的情况下，可以展现出突出的空间复杂度的优势。

​    最后，对于Hive来说，含有distinct的HQL语句，如果遇到瓶颈，想要调优，第一时间都是想到用group by来替换distinct来实现对数据的去重。



