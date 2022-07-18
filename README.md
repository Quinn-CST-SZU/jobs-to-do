# Jobs-TO-DO

> 该分支用来记录常用的olap查询引擎
>
> OLTP - Online Transaction Processing;事物、高可用，以每秒执行的食物和查询sql量来评估
> 
> OLAP - OnLine Analytical Processing;数据仓库系统的主要应用，对数据一致性要求不高，侧重决策支持


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
> 
### P1.1.架构介绍

### P2.2 其它
> 详情查看对应目录


## Part02.presto
> Presto是由Facebook开源的一个分布式的SQL即席查询引擎，用于运行交互式分析查询

### P2.1 架构介绍

#### P2.1.1.Presto有两类服务器：Coordinator和Worker

1）Coordinator

Coordinator服务器是用来解析语句，执行计划分析和管理Presto的Worker结点。Presto安装必须有一个Coordinator和多个Worker。如果用于开发环境和测试，则一个Presto实例可以同时担任这两个角色。

Coordinator跟踪每个Work的活动情况并协调查询语句的执行。Coordinator为每个查询建立模型，模型包含多个Stage，每个Stage再转为Task分发到不同的Worker上执行。

Coordinator与Worker、Client通信是通过REST API。


2）Worker

Worker是负责执行任务和处理数据。Worker从Connector获取数据。Worker之间会交换中间数据。Coordinator是负责从Worker获取结果并返回最终结果给Client。

当Worker启动时，会广播自己去发现 Coordinator，并告知 Coordinator它是可用，随时可以接受Task。

Worker与Coordinator、Worker通信是通过REST API。

#### P2.1.2.数据模型

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


### P2.2 其它
> 详情查看对应目录


## Part03.polardb
> 


