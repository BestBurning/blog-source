---
title: 世界真快-Maven更换阿里云仓库
comments: true
date: 2017-2-03
keywords: maven,阿里云仓库
tags:
- maven
categories:
- technology

---

每次拉一个像hadoop这种项目，maven中央仓库慢的整个世界都不好了，然而自从换了阿里云的仓库以后，步行改飞行了！！！爽！！！
在maven安装目录的conf下的setting.xml中配置mirrors
```
<mirror>  
  <id>alimaven</id>  
  <name>aliyun maven</name>  
  <url>https://maven.aliyun.com/repository/public</url>  
  <mirrorOf>central</mirrorOf>  
</mirror>  
```
