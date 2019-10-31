---
title: JVM内存模型-JDK1.8
tags: JVM
comments: true
categories: 
  - technology
toc: false
keywords: 'JVM内存模型,JDK1.8,JVM'
originContent: ''
date: 2019-10-31 17:58:13
---

> 多了解些底层总归是让自己向着真相靠近

![JVM内存模型](http://images.di1shuai.com/FslTfNYYumM3oe19oFvV6vWoKZa_)

JVM内存模型主要如上图所示
  - 线程私有
    - 程序计数器
    - 虚拟机栈
    - 本地方法栈
  - 线程共享
    - 堆
    - 元数据区 
    - 直接内存

### 程序计数器

线程私有，指向当前线程正在执行的字节码的行号。
如果当前线程执行的是native方法，那么此时是本地方法在工作所以不需要Java去进行记录，其值为Null。


### 虚拟机栈

线程私有，是Java方法执行的内存模型。Java栈中存放的是一个个栈帧，栈帧包括
  - 局部变量表
  - 操作数栈
  - 动态链接
  - 方法返回地址


### 本地方法栈

线程私有，功能与Java虚拟机栈十分相似，区别在于其服务于虚拟机使用的native方法。

### 堆
![堆](https://img-blog.csdn.net/2018031000051841?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvYnJ1Y2UxMjg=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)

线程共享，堆的主要作用是存放对象实例，也是管理最复杂的一个区域，空间分配如下：
  - Young Generation (1/3堆空间)
    - Eden (8/10 Young)
    - From (1/10 Young)
    - To (1/10 Young)
  - Old Generation  (2/3堆空间)

### 元数据区

从1.8开始，元数据区取代了1.7的永久代，作用是存放虚拟机加载的类信息、静态变量，常量等


### 直接内存

JDK1.4引入了NIO，它可以使用Native函数直接分配堆外内存。