---
title: Druid-数据迁移(HDFS)
tags:
- Druid
- BigData
keywords: Druid,数据迁移,insert-segment-to-db
comments: true
categories:
- technology
originContent: >-
  ## 环境描述

  - 两套`Druid`集群:`Druid-A`(source)、`Druid-B`(target)

  - 两套`HDFS`集群:`HDFS-A`、`HDFS-B`

  - `Druid`元数据存在`MySQL`中

  - 两套`HDFS`集群互通，记得在source中配置target的Host


  ## 目标描述

  - 将`Druid-A`中的数据迁移到`Druid-B`中


  ## 操作描述

  1. `HDFS`中的数据迁移,以`HDFS-A`中存储的两天的`segmnets`为例

  ```

  hadoop distcp
  hdfs://HDFS-A:8020/druid/segments/api_request_us/20180531T000000.000Z_20180601T000000.000Z
  hdfs://HDFS-A:8020/druid/segments/api_request_us/20180601T000000.000Z_20180602T000000.000Z
  webhdfs://HDFS-B:50070/druid/segments/api_request_us

  ```

  2. 确保`Druid`机器为安全的状态（对要插入的段无写操作，建议down掉`KIS`)

  3. 在`Druid`目录(阿里为`/usr/lib/druid-current`)中启动`insert-segment-to-db`

  ```

  java -Ddruid.metadata.storage.type=mysql
  -Ddruid.metadata.storage.connector.connectURI=jdbc\:mysql\://localhost\:3306/druid
  -Ddruid.metadata.storage.connector.user=root
  -Ddruid.metadata.storage.connector.password=pwd
  -Ddruid.extensions.loadList=[\"mysql-metadata-storage\",\"druid-hdfs-storage\"]
  -Ddruid.storage.type=hdfs -cp "$DRUID_HOME/lib/*" io.druid.cli.Main tools
  insert-segment-to-db --workingDir
  hdfs://HDFS-B:8020/druid/segments/api_request_us



  p.s.

  > druid.metadata.storage.connector.connectURI 为JDBC URL

  > druid.metadata.storage.connector.user       为用户名

  > druid.metadata.storage.connector.password   为密码

  > workingDir 可指定到具体那一天的目录也可以在dataSource的目录

  e.g. /druid/segments/api_request_us/20180601T000000.000Z_20180602T000000.000Z

  ```

  可参考[官网的链接](http://druid.io/docs/latest/operations/insert-segment-to-db.html)

  4.
  若发现`FileNotFound`,将`HDFS`的`core-site.xml`放置到`Druid`配置文件的`_commom中`(阿里为`/etc/ecm/druid-conf`)
toc: false
date: 2018-12-06 16:54:29
---


## 环境描述
- 两套`Druid`集群:`Druid-A`(source)、`Druid-B`(target)
- 两套`HDFS`集群:`HDFS-A`、`HDFS-B`
- `Druid`元数据存在`MySQL`中
- 两套`HDFS`集群互通，记得在source中配置target的Host

## 目标描述
- 将`Druid-A`中的数据迁移到`Druid-B`中

## 操作描述
1. `HDFS`中的数据迁移,以`HDFS-A`中存储的两天的`segmnets`为例
```
hadoop distcp hdfs://HDFS-A:8020/druid/segments/api_request_us/20180531T000000.000Z_20180601T000000.000Z hdfs://HDFS-A:8020/druid/segments/api_request_us/20180601T000000.000Z_20180602T000000.000Z webhdfs://HDFS-B:50070/druid/segments/api_request_us
```
2. 确保`Druid`机器为安全的状态（对要插入的段无写操作，建议down掉`KIS`)
3. 在`Druid`目录(阿里为`/usr/lib/druid-current`)中启动`insert-segment-to-db`,可参考[官网的链接](http://druid.io/docs/latest/operations/insert-segment-to-db.html)
```
java -Ddruid.metadata.storage.type=mysql -Ddruid.metadata.storage.connector.connectURI=jdbc\:mysql\://localhost\:3306/druid -Ddruid.metadata.storage.connector.user=root -Ddruid.metadata.storage.connector.password=pwd -Ddruid.extensions.loadList=[\"mysql-metadata-storage\",\"druid-hdfs-storage\"] -Ddruid.storage.type=hdfs -cp "$DRUID_HOME/lib/*" io.druid.cli.Main tools insert-segment-to-db --workingDir hdfs://HDFS-B:8020/druid/segments/api_request_us


p.s.
> druid.metadata.storage.connector.connectURI 为JDBC URL
> druid.metadata.storage.connector.user       为用户名
> druid.metadata.storage.connector.password   为密码
> workingDir 可指定到具体那一天的目录也可以在dataSource的目录
e.g. /druid/segments/api_request_us/20180601T000000.000Z_20180602T000000.000Z
```
4. 若发现`FileNotFound`,将`HDFS`的`core-site.xml`放置到`Druid`配置文件的`_commom中`(阿里为`/etc/ecm/druid-conf`)
