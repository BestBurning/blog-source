---
title: 查看IP
tags: ip
comments: true
categories: 
    - utils
originContent: ''
toc: false
keywords: ip
date: 2020-02-14 16:46:29
---


比如想查看自己代理前后的IP

```
$ curl https://ip.cn
>> {"country": "山西省临汾市", "city": "移动"}
$ proxy
$ curl https://ip.cn # 注意不要 sudo
>> {"country": "美国", "city": "Choopa"}

```
