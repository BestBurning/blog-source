---
title: Hadoop-1 安装及基本shell命令
comments: true
date: 2017-2-11
keywords: hadoop,安装
tags:
- hadoop
- BigData
categories:
- technology

---

1. 什么是hadoop
  
	- 对海量数据进行分布式处理
	- 三个核心组件：HDFS分布式文件系统、YARN运算资源调度系统、MAPREDUCE分布式运算编程框架

2. 准备工作

	- 三台linux（虚拟机亦可） server01、server02、server03
	- 三台linux以及本机ping互通
	- server01至02、03免密登陆
	- 01、02、03配置jdk
	- 去hadoop官网下载tar包[http://hadoop.apache.org/releases.html](http://hadoop.apache.org/releases.html) 

3. Hadoop安装
	- 解压后，去hadoop-x.x.x/etc/hadoop下编辑
		
	```	
	hadoop-env.sh   :   配置JAVA_HOME
	core-site.xml   :   
                    <configuration>
                        <property>
                            <name>fs.defaultFS</name>
                            <value>hdfs://server01.:9000</value>
                            <!--这里的server01是IP-->
                        </property>
                        <property>
                            <name>hadoop.tmp.dir</name>
                            <value>/home/hadoop/hdpdata</value>
                        </property>
                    </configuration>   
	后面的可以不用配置
	hdfs-site.xml   :   
                    <configuration>
                        <property>
                            <name>dfs.replication</name>
                            <value>2</value>
                        </property>
                    </configuration>
	mapred-site.xml.template    rename--> mapred-site.xml :
                    <configuration>
                        <property>
                            <name>mapreduce.framework.name</name>
                            <value>yarn</value>
                        </property>
                    </configuration>
	yarn-site.xml   :
                    <configuration>
                        <property>
                            <name>yarn.resourcemanager.hostname</name>
                            <value>server01</value>
                        </property>
                        <property>
                            <name>yarn.nodemanager.aux-services</name>
                            <value>mapreduce_shuffle</value>
                        </property>
                    </configuration>
	```
	- 配置环境变量
	
	```
	vi /etc/profile
	export HADOOP_HOME=/apps/hadoop-2.9.0
	export PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH
	source /etc/profile
	```
	- 格式化
	```
	hadoop namenode -format
	```
	- 启动namenode节点
	```
	cd hadoop-2.9.0/sbin
	hadoop-daemon.sh start namenode
	jps
	```
	- 去另一台server02启动datanode
	```
	cd hadoop-2.9.0/sbin
	hadoop-daemon.sh start datanode
	jps
	```
	- 用http测试：server01:50070 看到节点增加表示ok

4. 使用脚本一键启动
	- 启动所有dfs，配置namenode到datanode的免密登陆，在slaves中配置datanode的ip
	```
	vi hadoop-2.9.0/etc/hadoop/slaves

	删掉localhost,加入datanode的ip，如：
	server02
	server03

	cd hadoop-2.9.0/sbin
	start-dfs.sh
	```
	- 停掉所有dfs
	```
	stop-dfs.sh
	```
	- 启动所有dfs和yarn
	```
	start-all.sh		
	```
	- 停掉所有dfs和yarn
	
	```
	stop-all.sh
	```
5. shell
	hadoop-2.9.0/bin
	- 查找文件  (在网页上的最右Utilities下的Browse...下也能查看)
	```
	hadoop fs -ls /
	```
	- 存放文件
	```
	hadoop fs -put helloHadoop.txt /
	```
	- 查看文件
	```
	hadoop fs -cat /helloHadoop.txt

	```
	- 获取文件
	```
	hadoop fs -get /helloHadoop.txt

	```
	- 创建文件夹
	```
	hadoop fs -mkdir /hello
	hadoop fs -mkdir -p /hello/world

	```



