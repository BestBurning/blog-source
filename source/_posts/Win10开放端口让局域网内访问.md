---
title: Win10开放端口让局域网内访问
tags: Win10
comments: true
categories: 
- technology
toc: false
keywords: win10,端口,局域网
date: 2017-03-24 00:00:00
---


之前主要注重的是博客的PC端，后来在调试移动端的时候发现手机不能访问本地调试的4000端口，What?
那么当然就是Win10的端口没有对外开放啦，So依次点击：
1. Win10安全中心(右下)
![](http://images.di1shuai.com/FrshaARMBlt5S8WXiHJj3NrLzlK6)
2. 防火墙和网络保护
![](http://images.di1shuai.com/FqDOt5XMW14HObaYm4hsNtGKMccn)
3. 高级设置
![](http://images.di1shuai.com/Fl4zTnZQNXUz1CT4Tf1NPPdc6hDh)
4. 入站规则(左上)
![](http://images.di1shuai.com/FjiN3xJheqpTyEu_tVB7YpiU9VLk)
5. 新建规则(右上)
![](http://images.di1shuai.com/FpDCCAwFkFE06N0HE_J_kYoQa7kC)
6. 端口-->下一步
![](http://images.di1shuai.com/FrCFBHJG4lemoFV5ydpou5IPHJQd)
7. 输入要开放的端口或者端口范围
![](http://images.di1shuai.com/FrgBeaZ2Ypwf9F1vAKd8d892Km5x)
8. 一路下一步最后输入自定义规则名称
9. 完成