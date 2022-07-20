# Jobs-TO-DO

> 该分支用来记录常用的olap查询引擎
>
> OLTP - Online Transaction Processing;事务、高可用，以每秒执行的事务和查询sql量来评估
>       (mysql/postgresql/oracle/polardb)
> 
> OLAP - OnLine Analytical Processing;数据仓库系统的主要应用，对数据一致性要求不高，侧重决策支持
>       (hive/impala/clickhouse/presto)
>
> HTAP - Hybrid Transaction / Analytical Processing;同时支持 OLTP 和 OLAP 场景，需要创新的计算存储框架，在一份数据上保证事务的同时支持实时分析，省去费时的`ETL`过程
>       (tidb-pingcap/alloydb-google/polardb-x-baidu)
>

MPP架构：Massively Parallel Processing；把大规模数据的计算和存储分布到不同的独立的节点中去做
Shuffle：数据重分区；优化方案：1.分区打乱hash join 2.小表分发到所有节点broadcast join


| 特性 | OLTP | OLAP |
| -- | --| -- |
| 数据操作特征 | 增删改查均衡 | 多是读请求，不修改已添加数据 |
| 数据处理形式 | 单条处理偏多 | 批处理偏多 |
| 数据量 | 千万级 | 亿为单位 |
| 存储格式 | 行存 | 列存 |
| 事务支持 | 支持 | 可以不支持 |
| 数据一致性要求 | 高 | 低 |
| 应用场景 | 基本的、日常的事务处理 | 分析 |
| 集群规模 | 一般单节点或少量节点 | 集群规模大 |
| 技术选型 | mysql、oracle等行存关系型数据库 | hbase、clickhouse等列存大数据存储相关技术 |

在OLAP中，查询通常分为固化查询和即席查询

- 固化查询：通过手写sql完成一些临时的数据分析需求，这类sql形式多变、逻辑复杂，对查询时间没有严格要求
- 即席查询：一些固化下来的取数、看数需求，通过数据产品的形式提供给用户，从而提高数据分析和运营的效率。这类的sql固定模式，对响应时间有较高要求

## Part01.clickhouse

> 列式存储计算的分析型数据库，适用于写少但是查询海量数据的场景
> 

### 1.1.架构介绍

- 使用**列式存储**，有更高的压缩比。相比行式存储，相同大小的空间，列式可以存储更多条数据，减少IO。
- **无需事务**，数据一致性要求低
- 需要**低频批量写入**甚至一次性写入
- **有限支持delete、update**（删除、更新操作为异步操作，需要后台compation之后才能生效）
- **向量化执行与SIMD**，对内存中的列式数据，一个batch调用一次SIMD指令。加速计算。
- ClickHouse支持更多的数据类型，如数组、Map、嵌套类型


### 1.2 其它
> 详情查看对应目录


## Part02.presto
> Presto是由Facebook开源的一个分布式的SQL即席查询引擎，用于运行交互式分析查询

### 2.1 架构介绍

#### 2.1.1.Presto有两类服务器：Coordinator和Worker

1）Coordinator

Coordinator服务器是用来解析语句，执行计划分析和管理Presto的Worker结点。Presto安装必须有一个Coordinator和多个Worker。如果用于开发环境和测试，则一个Presto实例可以同时担任这两个角色。

Coordinator跟踪每个Work的活动情况并协调查询语句的执行。Coordinator为每个查询建立模型，模型包含多个Stage，每个Stage再转为Task分发到不同的Worker上执行。

Coordinator与Worker、Client通信是通过REST API。


2）Worker

Worker是负责执行任务和处理数据。Worker从Connector获取数据。Worker之间会交换中间数据。Coordinator是负责从Worker获取结果并返回最终结果给Client。

当Worker启动时，会广播自己去发现 Coordinator，并告知 Coordinator它是可用，随时可以接受Task。

Worker与Coordinator、Worker通信是通过REST API。

#### 2.1.2.数据模型

1）Presto采取三层表结构：

- Catalog：对应某一类数据源，例如Hive的数据，或MySql的数据
- Schema：对应MySql中的数据库实例
- Table：对应MySql中的表

2）Presto的存储单元包括：

- Page：多行数据的集合，包含多个列的数据，内部仅提供逻辑行，实际以列式存储。
- Block：一列数据，根据不同类型的数据，通常采取不同的编码方式，了解这些编码方式，有助于自己的存储系统对接presto。

3）不同类型的Block：

- Array类型Block，应用于固定宽度的类型，例如int，long，double
- 可变宽度的Block，应用于String类数据
- 固定宽度的String类型的block，所有行的数据拼接成一长串Slice，每一行的长度固定。
- 字典block：对于某些列，distinct值较少，适合使用字典保存


### 2.2 其它
> 详情查看对应目录


## Part03.polardb
> 一主多从，100%兼容mysql，最大支持200TB存储的OLTP事务引擎
>
> PolarDB将计算资源及存储资源分离为DBServer及DataServer，而DataServer是一个分布式共享文件系统，使得存储空间可以突破单机存储限制
> 

### 3.1 功能介绍

- PolarDB的DBServer同样分为主从节点，主节点只有一个负责数据读写，从节点可以最多有15个，只能进行读操作。所有DBServer节点共享存储在底层DataServer中的数据。
- 计算及存储的分离使得增加从节点时不再像MySQL加从库时，需要进行数据同步。从节点的增加是瞬时的。
- MySQL的Binlog主从同步是逻辑层的数据同步，同样的SQL需要在从库再执行一遍，使得主从延迟有时会比较明显。而PolarDB主从同步使用Redo Log，Redo Log记录了在数据的物理层面修改的信息，从库可以按照Log直接对数据页进行修改，从而提高了主从同步的速度。
- 会话一致性，PolarDB使用会话一致性解决主从不同步问题。
- DataServer使用三副本及分布式一致性协议Raft保证数据的可靠性。DataServer自动进行扩容管理。

### 3.2 其它


## Part04.polardb-X

> PolarDB-X是一个真正的分布式服务。他的计算节点CN，数据节点DN都是可以进行扩容的
> 

### 4.1 功能介绍

- 相较与MySQL的服务架构，PolarDB的DBServer可以认为就是MySQL本身，而DataServer则是文件服务。而PolarDB-X的CN节点可以认为是MySQL的Server部分，DN节点为MySQL的InnoDB部分。
- 与PolarDB的主从架构不同，PolarDB-X的计算节点是完全分布式的。
- DN节点基于Paxos提供数据高可靠、强一致保障。同时通过MVCC维护分布式事务可见性。且DN支持PB级别的数据量
- PolarDB-X将数据表以水平分区的方式，分布在多个存储节点（DN）上。数据分区方式由分区函数决定，PolarDB-X支持哈希（Hash）、范围（Range）等常用的分区函数。
- PolarDB-X支持并行计算，将SQL拆分为不同的Task分配给多个CN，并行计算。

