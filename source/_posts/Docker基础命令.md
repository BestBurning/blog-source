---
title: Docker基础命令
tags: Docker
comments: true
categories: [technology]
originContent: ''
toc: false
keywords: 'Docker,Dockerfile'
date: 2019-07-13 00:00:00
---


# Docker 

### 命令

```

docker image ls
查看镜像


docker pull java:8 
docker pull tomcat
下载镜像,:后为版本号,如果不指定版本号，默认为lastest


docker run --name tom -d -p 80:8080 tomcat
镜像运行 --name 命名 -d 后台启动 -p  端口映射，前为宿主机端口，后为镜像端口 

docker container logs tom
查看容器tom的日志

docker ps -a
查看所有容器


docker start xxx
启动容器


docker stop xxx
停止容器


docker rm -f xxx
强制删除容器

docker exec -it xxx /bin/bash
进入正在运行的容器并且开启交互模式终端

docker cp 主机文件路径 xxx:容器路径
主机中的文件拷贝到容器
docker cp xxx:容器路径 主机文件路径
容器中的文件拷贝到主机


docker container inspect xxx
查看容器的元信息

docker commit -m "备注" -a "作者" 容器名 镜像名:TAG
docker commit -m "我的tomcat" -a "Bruce" tom bruce/tomcat:1.0
基于已有的容器创建镜像

```

## Dockerfile

```
FROM java:8
# 基于哪个版本的镜像构建

ENV IMPLY_HOME /usr/local/imply
# 环境变量  

RUN mkdir -p "$IMPLY_HOME"
# 执行命令

ADD imply-3.0.8.tar.gz imply-3.0.8/
# 添加文件，并自动解压

RUN ln -s $IMPLY_HOME/imply-3.0.8 imply-3.0.8/current

WORKDIR $IMPLY_HOME/current
# 工作目录

EXPOSE 9095
# 开放端口

CMD ["bin/supervise","-c","conf/supervise/quickstart.conf"]
# 构建容器后调用，也就是在容器启动时才进行调用。
```

docker build -t bruce/imply:3.0.8 .