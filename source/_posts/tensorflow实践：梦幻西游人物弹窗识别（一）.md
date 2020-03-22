---
title: tensorflow实践：梦幻西游人物弹窗识别（一）
tags: 
- tensorflow
- 梦幻西游
- Win10
comments: true
categories: 
- technology
toc: true
keywords: tensorflow,梦幻西游,弹窗识别,python,自动点击
date: 2020-03-19 12:31:34
---


本篇文章主要阐述**梦幻西游弹窗识别**的**背景**、**思路**，以及**成果**展示

### 背景

疫情期间和朋友重温了一下**梦幻西游**，一边可以挂机抓鬼一边可以继续敲代码，好生快活
不过有个让人很纠结的痛点就是时不时的会弹出**人物弹窗**，一天两次暂离的30个回合根本不够好吗
一会不点就会被**踢下线**，总是去点的话又会打断coding的思路
这个弹框的特点是人物分为**前后左右**四个朝向，要点击朝**前**的
![](http://images.di1shuai.com/FmDIRoW-uf7202sHP3Eky3sDT9VD)
于是我灵机一动
![](http://images.di1shuai.com/FswzKDqTRqpLW9ZJ67vyUkVFc3BU)

### 思路

通过**屏幕截图**获取到梦幻西游内的**人物窗口**，

![](http://images.di1shuai.com/FvmxSuj1rzrJwWLb5v2ZMK5yqqYg)

然后**切**分为**4块**，
![](http://images.di1shuai.com/FtNE-uhRJniapeoZu-L5DTnVY-KH)
![](http://images.di1shuai.com/Fu4P4PpvjEdWYxPwiBl0bzL-Yw-u)
![](http://images.di1shuai.com/FoRMjFWNw0ixNK6tYIwKADSQi-UX)
![](http://images.di1shuai.com/FsGV0OkNfQuog-NtJx33JRAC-IlA)

用切好的图去我们训练的**模型**中**预测**，
最后**点击可能性最大**的**区域**就好啦

![](http://images.di1shuai.com/Fl91DfaNDpCfVTf_KfZ17oaZcGcc)



### 成果

最终的成品如下图所示

![](http://images.di1shuai.com/Fhvwyz8scozJqC5rx4oFimY4nqlh)

可以看到一次预测点击的耗时是在4s左右，

[源码](https://github.com/BestBurning/mhxy)已发布到了Github上，欢迎Star

---
### 声明

本人无任何商业目的，仅用于学习和娱乐，[源代码](https://github.com/BestBurning/mhxy)采用了[AGPL3.0](https://opensource.org/licenses/AGPL-3.0)开源协议

本文为博主原创文章，任何人未经过博主同意不得转载