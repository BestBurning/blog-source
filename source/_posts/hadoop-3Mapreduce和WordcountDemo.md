---
title: Hadoop-3 Mapreduce和Wordcount
comments: true
date: 2017-2-13
keywords: hadoop,mapreduce,wordcount
tags:
- hadoop
- mapreduce
- bigdata
categories:
- technology

---
1. 场景描述
存在像
```
diyishuai hello hi hadoop
spark kafka flume zookeeper
...
```
这样的单词，现在要用空格把他们分离开，并统计每个单词出现的次数
2. 编码
    - mapper
    - reducer  
代码见-->[https://github.com/BestBurning/myworld/tree/master/hadoop/src/main/java/com/diyishuai/hadoop/mr/wcdemo](https://github.com/BestBurning/myworld/tree/master/hadoop/src/main/java/com/diyishuai/hadoop/mr/wcdemo)
3. 打包并上传到一个datanode客户端
4. 启动hdsf和yarn(已经启动的可以略过)
```
start-dsf.sh
start-yarn.sh
```
5. 在hdfs创建目标目录并存入待分析文件
```
hadoop fs -mkdir -p /wordcount/input
hadoop fs -put LICENSE.txt NOTICE.txt README.txt /wordcount/input
```
6. 在[http://server01:50070](http://server01:50070)中check一下，之后要运行的wordcount可在[http://server01:8088](http://server01:8088)中看到
7. 运行wordcount
```
hadoop jar wordcount.jar com.diyishuai.hadoop.mr.wcdemo.WordcountDriver /wordcount/input /wordcount/output
```
8. 可以在hdsf的/wordcount/output中查看运行结果
9. 问题
如果遇到这个
```
Container [pid=3058,containerID=container_1515314973658_0001_01_000005] is running beyond virtual memory limits. Current usage: 107.9 MB of 1 GB physical memory used; 2.1 GB of 2.1 GB virtual memory used. Killing container.
```
在全部节点的hadoop-2.x.x/etc/hadoop/mapre-site.xml配置文件中添加
```
<property>
　　<name>mapreduce.map.memory.mb</name>
　　<value>1536</value>
</property>
<property>
　　<name>mapreduce.map.java.opts</name>
　　<value>-Xmx1024M</value>
</property>

```
并重启yarn
