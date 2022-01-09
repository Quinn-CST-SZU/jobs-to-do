# 命令整理

[TOC]

## 一.sqoop

### 1 安装

### 2 使用

#### 2.1使用说明

查看sqoop命令说明

```shell
$ sqoop help
usage: sqoop COMMAND [ARGS]

Available commands:
  codegen            Generate code to interact with database records
  create-hive-table  Import a table definition into Hive
  eval               Evaluate a SQL statement and display the results
  export             Export an HDFS directory to a database table
  help               List available commands
  import             Import a table from a database to HDFS
  import-all-tables  Import tables from a database to HDFS
  list-databases     List available databases on a server
  list-tables        List available tables in a database
  version            Display version information

See 'sqoop help COMMAND' for information on a specific command.
```

使用别名来代替 `sqoop (toolname)`：

```shell
$ sqoop-import
```

使用 `--options-file` 来传入一个文件，使用这种方式可以重用一些配置参数：

```shell
$ sqoop --options-file /home/jf/import.cfg --table TEST
```

#### 2.2导入数据到hdfs

使用 sqoop-import 命令可以从关系数据库导入数据到 hdfs

| 参数                              | 说明 |
| :-------------------------------- | :--------------------------------|
| `--append`                        | 将数据追加到hdfs中已经存在的dataset中。使用该参数，sqoop将把数据先导入到一个临时目录中，然后重新给文件命名到一个正式的目录中，以避免和该目录中已存在的文件重名。 |
| `--as-avrodatafile`               | 将数据导入到一个Avro数据文件中\| |
| `--as-sequencefile`               | 将数据导入到一个sequence文件中 |
| `--as-textfile`                   | 将数据导入到一个普通文本文件中，生成该文本文件后，可以在hive中通过sql语句查询出结果。 |
| `--boundary-query <statement>`    | 边界查询，也就是在导入前先通过SQL查询得到一个结果集，然后导入的数据就是该结果集内的数据，格式如：`--boundary-query 'select id,no from t where id = 3'`，表示导入的数据为id=3的记录，或者 `select min(<split-by>), max(<split-by>) from <table name>`，注意查询的字段中不能有数据类型为字符串的字段，否则会报错 |
| `--columns<col,col>`              | 指定要导入的字段值，格式如：`--columns id,username`          |
| `--direct`                        | 直接导入模式，使用的是关系数据库自带的导入导出工具。官网上是说这样导入会更快 |
| `--direct-split-size`             | 在使用上面direct直接导入的基础上，对导入的流按字节数分块，特别是使用直连模式从PostgreSQL导入数据的时候，可以将一个到达设定大小的文件分为几个独立的文件。 |
| `--inline-lob-limit`              | 设定大对象数据类型的最大值                                   |
| `-m,--num-mappers`                | 启动N个map来并行导入数据，默认是4个，最好不要将数字设置为高于集群的节点数 |
| `--query，-e <sql>`               | 从查询结果中导入数据，该参数使用时必须指定`–target-dir`、`–hive-table`，在查询语句中一定要有where条件且在where条件中需要包含 `\$CONDITIONS`，示例：`--query 'select * from t where \$CONDITIONS ' --target-dir /tmp/t –hive-table t` |
| `--split-by <column>`             | 表的列名，用来切分工作单元，一般后面跟主键ID                 |
| `--table <table-name>`            | 关系数据库表名，数据从该表中获取 |
| `--delete-target-dir`             | 删除目标目录 |
| `--target-dir <dir>`              | 指定hdfs路径 |
| `--warehouse-dir <dir>`           | 与 `--target-dir` 不能同时使用，指定数据导入的存放目录，适用于hdfs导入，不适合导入hive目录 |
| `--where`                         | 从关系数据库导入数据时的查询条件，示例：`--where "id = 2"`   |
| `-z,--compress`                   | 压缩参数，默认情况下数据是没被压缩的，通过该参数可以使用gzip压缩算法对数据进行压缩，适用于SequenceFile, text文本文件, 和Avro文件 |
| `--compression-codec`             | Hadoop压缩编码，默认是gzip                                   |
| `--null-string <null-string>`     | 可选参数，如果没有指定，则字符串null将被使用                 |
| `--null-non-string <null-string>` | 可选参数，如果没有指定，则字符串null将被使用\|               |

示例程序：

```shell
sqoop import \
--connect jdbc:mysql://192.168.56.121:3306/metastore \
--username hiveuser \
--password redhat \
--table TBLS \
--columns "tbl_id,create_time" \
--where "tbl_id > 1" \
--target-dir /user/hive/result
```

使用 sql 语句查询时，需要指定 `$CONDITIONS`

```shell
$ sqoop import \
--connect jdbc:mysql://192.168.56.121:3306/metastore \
--username hiveuser \
--password redhat \
--query 'SELECT * from TBLS where \$CONDITIONS ' \
--split-by tbl_id -m 4 \
--target-dir /user/hive/result
```

指定文件输出格式

```shell
$ sqoop import \
--connect jdbc:mysql://192.168.56.121:3306/metastore \
--username hiveuser \
--password redhat \
--table TBLS \
--fields-terminated-by "\t" \
--lines-terminated-by "\n" \
--delete-target-dir  \
--target-dir /user/hive/result
```

指定空字符串

```shell
$ sqoop import \
--connect jdbc:mysql://192.168.56.121:3306/metastore \
--username hiveuser \
--password redhat \
--table TBLS \
--fields-terminated-by "\t" \
--lines-terminated-by "\n" \
--delete-target-dir \
--null-string '\\N' \
--null-non-string '\\N' \
--target-dir /user/hive/result
```

指定压缩

```shell
$ sqoop import \
--connect jdbc:mysql://192.168.56.121:3306/metastore \
--username hiveuser \
--password redhat \
--table TBLS \
--fields-terminated-by "\t" \
--lines-terminated-by "\n" \
--delete-target-dir \
--null-string '\\N' \
--null-non-string '\\N' \
--compression-codec "com.hadoop.compression.lzo.LzopCodec" \
--target-dir /user/hive/result
```

可选的文件参数如下表:

| 参数                              | 说明           |
| :-------------------------------- | :--------------------------------|
| `--enclosed-by <char>`            | 给字段值前后加上指定的字符，比如双引号，示例：`--enclosed-by '\"'`，显示例子："3","jimsss","dd@dd.com" |
| `--escaped-by <char>`             | 给双引号作转义处理，如字段值为"测试"，经过 `--escaped-by "\\"` 处理后，在hdfs中的显示值为：`\"测试\"`，对单引号无效 |
| `--fields-terminated-by <char>`   | 设定每个字段是以什么符号作为结束的，默认是逗号，也可以改为其它符号，如句号`.`，示例如：`--fields-terminated-by` |
| `--lines-terminated-by <char>`    | 设定每条记录行之间的分隔符，默认是换行串，但也可以设定自己所需要的字符串，示例如：`--lines-terminated-by "#"` 以#号分隔 |
| `--mysql-delimiters`              | Mysql默认的分隔符设置，字段之间以`,`隔开，行之间以换行`\n`隔开，默认转义符号是`\`，字段值以单引号`'`包含起来。 |
| `--optionally-enclosed-by <char>` | enclosed-by是强制给每个字段值前后都加上指定的符号，而`--optionally-enclosed-by`只是给带有双引号或单引号的字段值加上指定的符号，故叫可选的 |

#### 2.3 创建hive表

> 生成与关系数据库表的表结构对应的HIVE表

| 参数                  | 说明                                                  |
| :-------------------- | :----------------------------------------- |
| `--hive-home <dir>`   | Hive的安装目录，可以通过该参数覆盖掉默认的hive目录 |
| `--hive-overwrite`    | 覆盖掉在hive表中已经存在的数据 |
| `--create-hive-table` | 默认是false，如果目标表已经存在了，那么创建任务会失败|
| `--hive-table`        | 后面接要创建的hive表|
| `--table`             | 指定关系数据库表名|
| `--hive-import`       | 导入到hive|

示例：

```shell
$ sqoop create-hive-table \
--connect jdbc:mysql://192.168.56.121:3306/metastore \
--username hiveuser \
--password redhat \
--table TBLS 
```

执行下面的命令会将 mysql 中的数据导入到 hdfs 中，然后创建一个hive 表，最后再将 hdfs 上的文件移动到 hive 表的目录下面

```shell
$ sqoop import \
--connect jdbc:mysql://192.168.56.121:3306/metastore \
--username hiveuser \
--password redhat \
--table TBLS \
--fields-terminated-by "\t" \
--lines-terminated-by "\n" \
--hive-import \
--hive-overwrite \
--create-hive-table \
--hive-table dw_srclog.TBLS \
--delete-target-dir
```



#### 2.4 增量导入

| 参数 | 说明 |
| :--------------------- | :---------------------------------------------------- |
| `--check-column (col)` | 用来作为判断的列名，如id|
| `--incremental (mode)` | append：追加，比如对大于last-value指定的值之后的记录进行追加导入。lastmodified：最后的修改时间，追加last-value指定的日期之后的记录 |
| `--last-value (value)` | 指定自从上次导入后列的最大值（大于该指定的值），也可以自己设定某一值 |

如：增量导入数据到 hive 中， mode=append

```shell
$ bin/sqoop import \
--connect jdbc:mysql://hadoop102:3306/company \
--username root \
--password 000000 \
--table staff \
--num-mappers 1 \
--fields-terminated-by "\t" \
--target-dir /user/hive/warehouse/staff_hive \
--check-column id \
--incremental append \
--last-value 3
```

**尖叫提示**： append 不能与–hive-等参数同时使用（Append mode for hive imports is not yetsupported. Please remove the parameter –append-mode）

```shell
先在 mysql 中建表并插入几条数据：
mysql> create table company.staff_timestamp(id int(4), name varchar(255), sex varchar(255),
last_modified timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE
CURRENT_TIMESTAMP);

mysql> insert into company.staff_timestamp (id, name, sex) values(1, 'AAA', 'female');
mysql> insert into company.staff_timestamp (id, name, sex) values(2, 'BBB', 'female');

先导入一部分数据：
bin/sqoop import \
--connect jdbc:mysql://hadoop102:3306/company \
--username root \
--password 000000 \
--table staff_timestamp \
--delete-target-dir \
--m 1
再增量导入一部分数据：
mysql> insert into company.staff_timestamp (id, name, sex) values(3, 'CCC', 'female');
$ bin/sqoop import \
--connect jdbc:mysql://hadoop102:3306/company \
--username root \
--password 000000 \
--table staff_timestamp \
--check-column last_modified \
--incremental lastmodified \
--last-value "2018-06-28 22:20:38" \
--m 1 \
--append
```

**尖叫提示：** 使用 lastmodified 方式导入数据要指定增量数据是要–append（追加）还是要–merge-key（合并）

**尖叫提示：** last-value 指定的值是会包含于增量导入的数据中

#### 2.5 合并hdfs文件

> 将HDFS中不同目录下面的数据合在一起，并存放在指定的目录中

| 参数                   | 说明      |
| :--------------------- | :--------------------|
| `--new-data <path>`    | Hdfs中存放数据的一个目录，该目录中的数据是希望在合并后能优先保留的，原则上一般是存放越新数据的目录就对应这个参数。 |
| `--onto <path>`        | Hdfs中存放数据的一个目录，该目录中的数据是希望在合并后能被更新数据替换掉的，原则上一般是存放越旧数据的目录就对应这个参数。 |
| `--merge-key <col>`    | 合并键，一般是主键ID |
| `--jar-file <file>`    | 合并时引入的jar包，该jar包是通过Codegen工具生成的jar包       |
| `--class-name <class>` | 对应的表名或对象名，该class类是包含在jar包中的。 |
| `--target-dir <path>`  | 合并后的数据在HDFS里的存放目录 |

```shell
sqoop merge \
–new-data /test/p1/person \
–onto /test/p2/person \
–target-dir /test/merged \
–jar-file /opt/data/sqoop/person/Person.jar \
–class-name Person \
–merge-key id
```

其中，`–class-name` 所指定的 class 名是对应于 Person.jar 中的 Person 类，而 Person.jar 是通过 Codegen 生成的

### 参考资料

[Sqoop User Guide](https://sqoop.apache.org/docs/1.4.2/SqoopUserGuide.html)

## 二.hadoop

### 1.概述

所有的hadoop命令均由bin/hadoop脚本引发。不指定参数运行hadoop脚本会打印所有命令的描述。

用法：hadoop [--config confdir] [COMMAND] [GENERIC_OPTIONS] [COMMAND_OPTIONS]

### 2.常规选项

下面的选项被 [dfsadmin](http://hadoop.apache.org/docs/r1.0.4/cn/commands_manual.html#dfsadmin), [fs](http://hadoop.apache.org/docs/r1.0.4/cn/commands_manual.html#fs), [fsck](http://hadoop.apache.org/docs/r1.0.4/cn/commands_manual.html#fsck)和 [job](http://hadoop.apache.org/docs/r1.0.4/cn/commands_manual.html#job)支持。 应用程序要实现 [Tool](http://hadoop.apache.org/core/docs/r0.18.2/api/org/apache/hadoop/util/Tool.html)来支持 [常规选项](http://hadoop.apache.org/core/docs/r0.18.2/api/org/apache/hadoop/util/GenericOptionsParser.html)。

|          GENERIC_OPTION           |                             描述                             |
| :-------------------------------: | :----------------------------------------------------------: |
|    -conf <configuration file>     |                   指定应用程序的配置文件。                   |
|        -D <property=value>        |                 为指定property指定值value。                  |
|    -fs <local\|namenode:port>     |                        指定namenode。                        |
|   -jt <local\|jobtracker:port>    | 指定job tracker。只适用于[job](http://hadoop.apache.org/docs/r1.0.4/cn/commands_manual.html#job)。 |
|    -files <逗号分隔的文件列表>    | 指定要拷贝到map reduce集群的文件的逗号分隔的列表。 只适用于[job](http://hadoop.apache.org/docs/r1.0.4/cn/commands_manual.html#job)。 |
|   -libjars <逗号分隔的jar列表>    | 指定要包含到classpath中的jar文件的逗号分隔的列表。 只适用于[job](http://hadoop.apache.org/docs/r1.0.4/cn/commands_manual.html#job)。 |
| -archives <逗号分隔的archive列表> | 指定要被解压到计算节点上的档案文件的逗号分割的列表。 只适用于[job](http://hadoop.apache.org/docs/r1.0.4/cn/commands_manual.html#job)。 |

### 3.用户命令

#### 3.1 archive

创建一个hadoop档案文件。参考 [Hadoop Archives](http://hadoop.apache.org/docs/r1.0.4/cn/hadoop_archives.html).

用法：hadoop archive -archiveName NAME \<src>* \<dest>

|     命令选项      |                    描述                    |
| :---------------: | :----------------------------------------: |
| -archiveName NAME |            要创建的档案的名字。            |
|        src        | 文件系统的路径名，和通常含正则表达的一样。 |
|       dest        |          保存档案文件的目标目录。          |

#### 3.2 distcp

递归地拷贝文件或目录。参考[DistCp指南](http://hadoop.apache.org/docs/r1.0.4/cn/distcp.html)以获取等多信息。

用法：hadoop distcp \<srcurl> \<desturl>

| 命令选项 |  描述   |
| :------: | :-----: |
|  srcurl  |  源Url  |
| desturl  | 目标Url |

#### 3.3 fs

用法：hadoop fs [[GENERIC_OPTIONS](http://hadoop.apache.org/docs/r1.0.4/cn/commands_manual.html#常规选项)] [COMMAND_OPTIONS]

运行一个常规的文件系统客户端。

各种命令选项可以参考[HDFS Shell指南](http://hadoop.apache.org/docs/r1.0.4/cn/hdfs_shell.html)。

#### 3.4 fsck

运行HDFS文件系统检查工具。参考[Fsck](http://hadoop.apache.org/docs/r1.0.4/cn/hdfs_user_guide.html#fsck)了解更多。

用法：hadoop fsck [[GENERIC_OPTIONS](http://hadoop.apache.org/docs/r1.0.4/cn/commands_manual.html#常规选项)] <path> [-move | -delete | -openforwrite] [-files [-blocks [-locations | -racks]]]

|   命令选项    |              描述               |
| :-----------: | :-----------------------------: |
|    <path>     |        检查的起始目录。         |
|     -move     |    移动受损文件到/lost+found    |
|    -delete    |         删除受损文件。          |
| -openforwrite |      打印出写打开的文件。       |
|    -files     |     打印出正被检查的文件。      |
|    -blocks    |       打印出块信息报告。        |
|  -locations   |    打印出每个块的位置信息。     |
|    -racks     | 打印出data-node的网络拓扑结构。 |

#### 3.5 jar

运行jar文件。用户可以把他们的Map Reduce代码捆绑到jar文件中，使用这个命令执行。

用法：hadoop jar <jar> [mainClass] args...

streaming作业是通过这个命令执行的。参考[Streaming examples](http://hadoop.apache.org/docs/r1.0.4/cn/streaming.html#其他例子)中的例子。

Word count例子也是通过jar命令运行的。参考[Wordcount example](http://hadoop.apache.org/docs/r1.0.4/cn/mapred_tutorial.html#用法)。

#### 3.6 job

用于和Map Reduce作业交互和命令。

用法：hadoop job [[GENERIC_OPTIONS](http://hadoop.apache.org/docs/r1.0.4/cn/commands_manual.html#常规选项)] [-submit <job-file>] | [-status <job-id>] | [-counter <job-id> <group-name> <counter-name>] | [-kill <job-id>] | [-events <job-id> <from-event-#> <#-of-events>] | [-history [all] <jobOutputDir>] | [-list [all]] | [-kill-task <task-id>] | [-fail-task <task-id>]

|                   命令选项                    |                             描述                             |
| :-------------------------------------------: | :----------------------------------------------------------: |
|              -submit <job-file>               |                           提交作业                           |
|               -status <job-id>                |           打印map和reduce完成百分比和所有计数器。            |
| -counter <job-id> <group-name> <counter-name> |                       打印计数器的值。                       |
|                -kill <job-id>                 |                        杀死指定作业。                        |
| -events <job-id> <from-event-#> <#-of-events> |          打印给定范围内jobtracker接收到的事件细节。          |
|         -history [all] <jobOutputDir>         | -history <jobOutputDir> 打印作业的细节、失败及被杀死原因的细节。更多的关于一个作业的细节比如成功的任务，做过的任务尝试等信息可以通过指定[all]选项查看。 |
|                  -list [all]                  |      -list all显示所有作业。-list只显示将要完成的作业。      |
|             -kill-task <task-id>              |          杀死任务。被杀死的任务不会不利于失败尝试。          |
|             -fail-task <task-id>              |          使任务失败。被失败的任务会对失败尝试不利。          |

#### 3.7 pipes

运行pipes作业。

用法：hadoop pipes [-conf <path>] [-jobconf <key=value>, <key=value>, ...] [-input <path>] [-output <path>] [-jar <jar file>] [-inputformat <class>] [-map <class>] [-partitioner <class>] [-reduce <class>] [-writer <class>] [-program <executable>] [-reduces <num>]

|                命令选项                |         描述          |
| :------------------------------------: | :-------------------: |
|              -conf <path>              |      作业的配置       |
| -jobconf <key=value>, <key=value>, ... | 增加/覆盖作业的配置项 |
|             -input <path>              |       输入目录        |
|             -output <path>             |       输出目录        |
|            -jar <jar file>             |       Jar文件名       |
|          -inputformat <class>          |     InputFormat类     |
|              -map <class>              |      Java Map类       |
|          -partitioner <class>          |   Java Partitioner    |
|            -reduce <class>             |     Java Reduce类     |
|            -writer <class>             |   Java RecordWriter   |
|         -program <executable>          |    可执行程序的URI    |
|             -reduces <num>             |      reduce个数       |

#### 3.8 version

打印版本信息。

用法：hadoop version

### 4.管理命令

hadoop集群管理员常用的命令

#### 4.1 balancer

运行集群平衡工具。管理员可以简单的按Ctrl-C来停止平衡过程。参考[Rebalancer](http://hadoop.apache.org/docs/r1.0.4/cn/hdfs_user_guide.html#Rebalancer)了解更多。

用法：hadoop balancer [-threshold <threshold>]

|        命令选项        |                  描述                  |
| :--------------------: | :------------------------------------: |
| -threshold <threshold> | 磁盘容量的百分比。这会覆盖缺省的阀值。 |

#### 4.2 daemonlog

获取或设置每个守护进程的日志级别。

用法：hadoop daemonlog -getlevel <host:port> <name> 
用法：hadoop daemonlog -setlevel <host:port> <name> <level>

|               命令选项               |                             描述                             |
| :----------------------------------: | :----------------------------------------------------------: |
|     -getlevel <host:port> <name>     | 打印运行在<host:port>的守护进程的日志级别。这个命令内部会连接http://<host:port>/logLevel?log=<name> |
| -setlevel <host:port> <name> <level> | 设置运行在<host:port>的守护进程的日志级别。这个命令内部会连接http://<host:port>/logLevel?log=<name> |

#### 4.3 datanode

运行一个HDFS的datanode。

用法：hadoop datanode [-rollback]

| 命令选项  |                             描述                             |
| :-------: | :----------------------------------------------------------: |
| -rollback | 将datanode回滚到前一个版本。这需要在停止datanode，分发老的hadoop版本之后使用。 |

#### 4.4 dfsadmin

运行一个HDFS的dfsadmin客户端。

用法：hadoop dfsadmin [[GENERIC_OPTIONS](http://hadoop.apache.org/docs/r1.0.4/cn/commands_manual.html#常规选项)] [-report] [-safemode enter | leave | get | wait] [-refreshNodes] [-finalizeUpgrade] [-upgradeProgress status | details | force] [-metasave filename] [-setQuota <quota> <dirname>...<dirname>] [-clrQuota <dirname>...<dirname>] [-help [cmd]]

|                  命令选项                   |                             描述                             |
| :-----------------------------------------: | :----------------------------------------------------------: |
|                   -report                   |              报告文件系统的基本信息和统计信息。              |
|   -safemode enter \| leave \| get \| wait   | 安全模式维护命令。安全模式是Namenode的一个状态，这种状态下，Namenode  1. 不接受对名字空间的更改(只读) 2. 不复制或删除块 Namenode会在启动时自动进入安全模式，当配置的块最小百分比数满足最小的副本数条件时，会自动离开安全模式。安全模式可以手动进入，但是这样的话也必须手动关闭安全模式。 |
|                -refreshNodes                | 重新读取hosts和exclude文件，更新允许连到Namenode的或那些需要退出或入编的Datanode的集合。 |
|              -finalizeUpgrade               | 终结HDFS的升级操作。Datanode删除前一个版本的工作目录，之后Namenode也这样做。这个操作完结整个升级过程。 |
| -upgradeProgress status \| details \| force |  请求当前系统的升级状态，状态的细节，或者强制升级操作进行。  |
|             -metasave filename              | 保存Namenode的主要数据结构到hadoop.log.dir属性指定的目录下的<filename>文件。对于下面的每一项，<filename>中都会一行内容与之对应 1. Namenode收到的Datanode的心跳信号 2. 等待被复制的块 3. 正在被复制的块 4. 等待被删除的块 |
|   -setQuota <quota> <dirname>...<dirname>   | 为每个目录 <dirname>设定配额<quota>。目录配额是一个长整型整数，强制限定了目录树下的名字个数。 命令会在这个目录上工作良好，以下情况会报错： 1. N不是一个正整数，或者 2. 用户不是管理员，或者 3. 这个目录不存在或是文件，或者 4. 目录会马上超出新设定的配额。 |
|       -clrQuota <dirname>...<dirname>       | 为每一个目录<dirname>清除配额设定。 命令会在这个目录上工作良好，以下情况会报错： 1. 这个目录不存在或是文件，或者 2. 用户不是管理员。 如果目录原来没有配额不会报错。 |
|                 -help [cmd]                 | 显示给定命令的帮助信息，如果没有给定命令，则显示所有命令的帮助信息。 |

#### 4.5 jobtracker

运行MapReduce job Tracker节点。

用法：hadoop jobtracker

#### 4.6 namenode

运行namenode。有关升级，回滚，升级终结的更多信息请参考[升级和回滚](http://hadoop.apache.org/docs/r1.0.4/cn/hdfs_user_guide.html#升级和回滚)。

用法：hadoop namenode [-format] | [-upgrade] | [-rollback] | [-finalize] | [-importCheckpoint]

|     命令选项      |                             描述                             |
| :---------------: | :----------------------------------------------------------: |
|      -format      | 格式化namenode。它启动namenode，格式化namenode，之后关闭namenode。 |
|     -upgrade      |     分发新版本的hadoop后，namenode应以upgrade选项启动。      |
|     -rollback     | 将namenode回滚到前一版本。这个选项要在停止集群，分发老的hadoop版本后使用。 |
|     -finalize     | finalize会删除文件系统的前一状态。最近的升级会被持久化，rollback选项将再不可用，升级终结操作之后，它会停掉namenode。 |
| -importCheckpoint | 从检查点目录装载镜像并保存到当前检查点目录，检查点目录由fs.checkpoint.dir指定。 |

#### 4.7 secondarynamenode

运行HDFS的secondary namenode。参考[Secondary Namenode](http://hadoop.apache.org/docs/r1.0.4/cn/hdfs_user_guide.html#Secondary+NameNode)了解更多。

用法：hadoop secondarynamenode [-checkpoint [force]] | [-geteditsize]

|      命令选项       |                             描述                             |
| :-----------------: | :----------------------------------------------------------: |
| -checkpoint [force] | 如果EditLog的大小 >= fs.checkpoint.size，启动Secondary namenode的检查点过程。 如果使用了-force，将不考虑EditLog的大小。 |
|    -geteditsize     |                      打印EditLog大小。                       |

#### 4.8 tasktracker

运行MapReduce的task Tracker节点。

用法：hadoop tasktracker