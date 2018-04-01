---
title: SSH免密登陆
comments: true
date: 2017-1-11
keywords: SSH,免密登陆,Linux
tags:
- Linux
categories:
- technology

---

1.  目标
A登陆到B不需要密码
```


now:
    A  --->pwssword--->B

will:
    A  ---> B


```
2.  原理
A生成公钥私钥对,A的公钥用于表明自己的身份，然后将A的公钥发送给B，加入B的验证列表
```


      A                      B
  |       |    
private  public  --------->  authorized_keys

```
3.  做法
```
A:
ssh-keygen
ssh-copy-id B
```
