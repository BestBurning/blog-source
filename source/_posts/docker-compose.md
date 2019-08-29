---
title: docker-compose
tags: Docker
comments: true
categories: [technology]
toc: false
keywords: 'docker,docker-compose,flink'
date: 2018-07-15 00:00:00
---


docker-compose 提供了基于docker编排功能
1. 创建一个空文件夹
```
mkdir docker-compose-go
cd docker-compose-go
```
2. 创建`docker-compose.yml`文件,文件内容如下
```
version: "2.1"
services:
  jobmanager:
    image: flink
    expose:
      - "6123"
    ports:
      - "8081:8081"
    command: jobmanager
    environment:
      - JOB_MANAGER_RPC_ADDRESS=jobmanager

  taskmanager:
    image: flink
    expose:
      - "6121"
      - "6122"
    depends_on:
      - jobmanager
    command: taskmanager
    links:
      - "jobmanager:jobmanager"
    environment:
      - JOB_MANAGER_RPC_ADDRESS=jobmanager

```
3. 运行,-d是后台运行
```
docker-compose up -d
```
4. 访问localhost:8081