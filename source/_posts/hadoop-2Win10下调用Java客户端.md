---
title: Hadoop-2 Win10下调用Java客户端
comments: true
date: 2017-2-12
keywords: hadoop,Java,win10
tags:
- hadoop
- bigdata
categories:
- technology

---

1. win10开发环境准备工作
    - 方式1 ：
        - 解压tar包
        - 配置环境变量HADOOP_HOME,并将%HADOOP_HOME%\bin加入Path
        - 获取win下的hadoop相关文件:[https://wiki.apache.org/hadoop/WindowsProblems](https://wiki.apache.org/hadoop/WindowsProblems)
        - 将相关文件加入%HADOOP_HOME%\bin中
    ----------------------------
    - 方式2 (慎用)：
        - 自己编译win下的hadoop包，参考:[http://blog.csdn.net/changge458/article/details/53576178](http://blog.csdn.net/changge458/article/details/53576178)
        - 解压tar
        - 配置环境变量HADOOP_HOME,并将%HADOOP_HOME%\bin加入Path
2. maven依赖
```
       <dependency>
            <groupId>org.apache.hadoop</groupId>
            <artifactId>hadoop-hdfs</artifactId>
            <version>2.9.0</version>
        </dependency>
        <dependency>
            <groupId>org.apache.hadoop</groupId>
            <artifactId>hadoop-client</artifactId>
            <version>2.9.0</version>
        </dependency>
        
        <dependency>
            <groupId>junit</groupId>
            <artifactId>junit</artifactId>
            <version>4.12</version>
        </dependency>
```
3. API调用
```
package com.diyishuai.hadoop.hdfs;


import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.junit.Before;
import org.junit.Test;

import java.io.IOException;
import java.net.URI;

public class HdfsClientDemo {


    FileSystem fs = null;

    @Before
    public void init() throws Exception{
        Configuration conf = new Configuration();
//        conf.set("fs.defaultFS","hdfs://server01:9000");

        fs = FileSystem.get(new URI("hdfs://server01:9000"),conf,"root");
    }

    @Test
    public void testUpload() throws IOException {
        fs.copyFromLocalFile(new Path("C:\\Users\\Administrator\\Downloads\\apache-maven-3.5.2-bin.zip"),new Path("/hihi.txt"));
    }

    @Test
    public void testDownload() throws IOException {
        fs.copyToLocalFile(new Path("/hihi.txt"),new Path("C:\\Users\\Administrator\\Downloads\\hihi-from-down.txt"));
    }

}

```
今天编译win的hadoop包消耗了些元气，各种等啊等！
代码放在github上了，[https://github.com/BestBurning/myworld/tree/master/hadoop](https://github.com/BestBurning/myworld/tree/master/hadoop)
