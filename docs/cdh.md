# CDH集群搭建

[TOC]

## 当前环境

> 一些实况和预想

### 版本

```
- system
  Centos7.3
- manager
  CM6.1
- database
  mysql5.7
```

### 机器架构

```
192.168.1.63
192.168.1.64
192.168.1.65
192.168.1.66
192.168.1.67
```

### 目录

```
- cm目录
 /opt/cloudera-manager/
- 挂载磁盘
 /data0 /data1 ... /datan
```

## 提前准备

> 方便安装
### 添加sudo权限用户

> 用于系统运维的账户

```shell
[root@localhost ~]# useradd fpx_hdp_man
[root@localhost ~]# passwd fpx_hdp_man
Changing password for user fpx_hdp_man.
New password: hdp_man
BAD PASSWORD: The password contains the user name in some form
Retype new password: hdp_man
passwd: all authentication tokens updated successfully.
[root@localhost ~]# visudo
## Next comes the main part: which users can run what software on
## which machines (the sudoers file can be shared between multiple
## systems).
## Syntax:
##
##      user    MACHINE=COMMANDS
##
## The COMMANDS section may have other options added to it.
##
## Allow root to run any commands anywhere
root    ALL=(ALL)       ALL
fpx_hdp_man     ALL=(ALL)       ALL
```



### 修改hostname

```shell
# 63
hostnamectl set-hostname hdp001
# 64
hostnamectl set-hostname hdp002
# 65
hostnamectl set-hostname hdp003
# 66
hostnamectl set-hostname hdp004
# 67
hostnamectl set-hostname hdp005
```

### 打通SSH无密钥登陆

```shell
# 回车生成无密码的密钥对
ssh-keygen -t rsa
# 添加认证文件中
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
# 设置ahthorized_keys的访问权限，并发送到所有从节点服务器上
chmod 600 ~/.ssh/authorized_keys
scp ~/.ssh/authorized_keys root@192.168.1.64:~/.ssh/
scp ~/.ssh/authorized_keys root@192.168.1.65:~/.ssh/
scp ~/.ssh/authorized_keys root@192.168.1.66:~/.ssh/
scp ~/.ssh/authorized_keys root@192.168.1.67:~/.ssh/
```

### 统一host文件

```shell
[root@hdp001 ~] cat /etc/hosts
192.168.1.63 hdp001
192.168.1.64 hdp002
192.168.1.65 hdp003
192.168.1.66 hdp004
192.168.1.67 hdp005
[root@hdp001 ~] for h in $(cat /etc/hosts | grep fpx | awk '{print $1}');do scp /etc/hosts root@${h}:/etc/hosts;done
```

在上面几步之后我们可以对下面操作进行批处理

### 挂载磁盘

```shell
# 格式化
[root@localhost ~]# fdisk /dev/sda
Welcome to fdisk (util-linux 2.23.2).

Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Device does not contain a recognized partition table
Building a new DOS disklabel with disk identifier 0x266ac5a7.

The device presents a logical sector size that is smaller than
the physical sector size. Aligning to a physical sector (or optimal
I/O) size boundary is recommended, or performance may be impacted.

Command (m for help): m
Command action
   a   toggle a bootable flag
   b   edit bsd disklabel
   c   toggle the dos compatibility flag
   d   delete a partition
   g   create a new empty GPT partition table
   G   create an IRIX (SGI) partition table
   l   list known partition types
   m   print this menu
   n   add a new partition
   o   create a new empty DOS partition table
   p   print the partition table
   q   quit without saving changes
   s   create a new empty Sun disklabel
   t   change a partition's system id
   u   change display/entry units
   v   verify the partition table
   w   write table to disk and exit
   x   extra functionality (experts only)

Command (m for help): n
Partition type:
   p   primary (0 primary, 0 extended, 4 free)
   e   extended
Select (default p): p
Partition number (1-4, default 1):  
First sector (2048-1875385007, default 2048): 
Using default value 2048
Last sector, +sectors or +size{K,M,G} (2048-1875385007, default 1875385007): 
Using default value 1875385007
Partition 1 of type Linux and of size 894.3 GiB is set

Command (m for help): p

Disk /dev/sda: 960.2 GB, 960197124096 bytes, 1875385008 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 4096 bytes
I/O size (minimum/optimal): 4096 bytes / 4096 bytes
Disk label type: dos
Disk identifier: 0x266ac5a7

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1            2048  1875385007   937691480   83  Linux

Command (m for help): w
# 刷新分区表
[root@localhost ~]# partprobe
# 设置磁盘文件格式，由于目前磁盘大小未超过2T，暂时使用ext4
[root@localhost ~]# mkfs -t ext4 /dev/sda1
mke2fs 1.42.9 (28-Dec-2013)
Discarding device blocks: done                            
Filesystem label=
OS type: Linux
Block size=4096 (log=2)
Fragment size=4096 (log=2)
Stride=0 blocks, Stripe width=0 blocks
58613760 inodes, 234422870 blocks
11721143 blocks (5.00%) reserved for the super user
First data block=0
Maximum filesystem blocks=2382364672
7155 block groups
32768 blocks per group, 32768 fragments per group
8192 inodes per group
Superblock backups stored on blocks: 
        32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208, 
        4096000, 7962624, 11239424, 20480000, 23887872, 71663616, 78675968, 
        102400000, 214990848

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (32768 blocks): done
Writing superblocks and filesystem accounting information: done 
# 挂载到系统
[root@localhost ~]# mkdir /data0
[root@localhost ~]# mount /dev/sda1 /data0
# 设置开机自动挂载
[root@localhost ~]# vi /etc/fstab
/dev/sda1               /data0                  ext4    defaults        1 2
# 检测设置是否正确
[root@localhost ~]# mount -av
/                        : ignored
/boot                    : already mounted
/boot/efi                : already mounted
/opt                     : already mounted
swap                     : ignored
/data0                   : already mounted
# 继续挂载其它盘和其它系统
echo "n




"
```

###  安装JDK

```shell
# 在配置好yum.repo本地源后
yum install oracle-j2sdk1.8-1.8.0+update141-1.x86_64
# 设置环境变量
# 测试配置是否成功
javac
```

### 配置NTP时钟同步

```shell
yum -y install ntp
# 修改server的配置文件
# 同步到client
# 启动服务
# 测试时钟同步
```

### 安装mysql

```shell
# 自行安装
wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm
rpm -ivh mysql-community-release-el7-5.noarch.rpm
yum update
yum install mysql-server mysql-client
# 设置开机启动
chkconfig mysqld on
# 创建scm库
# 添加scm账户
# 设置访问权限
# 添加外网访问权限
vi /etc/my.cnf
# 安装jdbc driver
wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.46.tar.gz
tar zxvf mysql-connector-java-5.1.46.tar.gz
mkdir -p /usr/share/java/
cp mysql-connector-java-5.1.46/mysql-connector-java-5.1.46-bin.jar /usr/share/java/mysql-connector-java.jar
```

### 关闭防火墙、selinux

```shell
# 自行解决
```


## 集群搭建

### 配置离线仓库

```shell
yum -y install httpd createrepo
service httpd start && chkconfig httpd on
# 创建本地cm源并生成RPM元数据
mkdir /var/www/html/cloudera-repos/ && cd /var/www/html/cloudera-repos/ && createrepo .

wget https://archive.cloudera.com/cm6/6.1.0/redhat7/yum/RPMS/x86_64/cloudera-manager-agent-6.1.0-769885.el7.x86_64.rpm
wget https://archive.cloudera.com/cm6/6.1.0/redhat7/yum/RPMS/x86_64/cloudera-manager-daemons-6.1.0-769885.el7.x86_64.rpm
wget https://archive.cloudera.com/cm6/6.1.0/redhat7/yum/RPMS/x86_64/cloudera-manager-server-6.1.0-769885.el7.x86_64.rpm
wget https://archive.cloudera.com/cm6/6.1.0/redhat7/yum/RPMS/x86_64/cloudera-manager-server-db-2-6.1.0-769885.el7.x86_64.rpm
wget https://archive.cloudera.com/cm6/6.1.0/redhat7/yum/RPMS/x86_64/oracle-j2sdk1.8-1.8.0+update141-1.x86_64.rpm
wget https://archive.cloudera.com/cm6/6.1.0/allkeys.asc
```

### 下载离线文件

```sh
wget https://archive.cloudera.com/cdh6/6.1.0/parcels/CDH-6.1.0-1.cdh6.1.0.p0.770702-el7.parcel
wget https://archive.cloudera.com/cdh6/6.1.0/parcels/CDH-6.1.0-1.cdh6.1.0.p0.770702-el7.parcel.sha256
wget https://archive.cloudera.com/cdh6/6.1.0/parcels/manifest.json

# 把下载的parcels放在主节点上
mkdir /opt/cloudera/parcel-repo/
mv CDH-6.1.0-1.cdh6.1.0.p0.770702-el7.parcel /opt/cloudera/parcel-repo/CDH-6.1.0-1.cdh6.1.0.p0.770702-el7.parcel
mv CDH-6.1.0-1.cdh6.1.0.p0.770702-el7.parcel.sha256 /opt/cloudera/parcel-repo/CDH-6.1.0-1.cdh6.1.0.p0.770702-el7.parcel.sha
```

### 部署安装

#### 提前适配

```shell
# 配置RPM源
# 创建目录
# master节点
yum install cloudera-manager-daemons cloudera-manager-agent cloudera-manager-server
# client节点
yum install cloudera-manager-daemons cloudera-manager-agent
# 添加开机启动
chkconfig cloudera-scm-agent on
chkconfig cloudera-scm-server on
```

#### 配置server

```shell
[root@hdp001 ~]# vi /etc/cloudera-scm-agent/config.ini
[General]
# Hostname of the CM server.
#server_host=localhost
server_host=hdp001
# Port that the CM server is listening on.
server_port=7182
```

初始化数据库，启动服务 [在每台主机都完成上面配置修改后执行]

```shell
/opt/cloudera/cm/schema/scm_prepare_database.sh [options] <databaseType> <databaseName> <databaseUser> <password>
[root@hdp001 ~]/opt/cloudera/cm/schema/scm_prepare_database.sh mysql -h hdp001 --scm-host hdp001 db uname passwd
```

启动server

```shell
service cloudera-scm-server start
```



#### 配置client

```shell
[root@hdp001 ~]# vi /etc/cloudera-scm-agent/config.ini
[General]
# Hostname of the CM server.
#server_host=localhost
server_host=hdp001
# Port that the CM server is listening on.
server_port=7182
```

启动client

```shell
service cloudera-scm-client start
```



## 服务管理

http://<server_IP>:7180

用户名：admin
密码：admin



## CDH6优化

### 虚拟内存设置

> Cloudera 建议将 /proc/sys/vm/swappiness 设置为 0

```shell
cat /etc/sysctl.conf | grep vm
# 临时关闭
echo vm.swappiness = 0 >> /etc/sysctl.conf
# 永久关闭
```



### 大内存页设置

> 大内存页禁用

```shell
echo never>/sys/kernel/mm/transparent_hugepage/defrag
echo never>/sys/kernel/mm/transparent_hugepage/enabled
```

### 配置修改

#### 1.Service Monitor

oom_heap_dump_dir 如果默认的/tmp目录空间过小，建议修改为一个空间较大的目录

```
Impala Catalog Server
oom_heap_dump_dir /tmp --> /opt/tmp
Service Monitor
oom_heap_dump_dir /tmp --> /opt/tmp
Host Monitor
oom_heap_dump_dir /tmp --> /opt/tmp
```






