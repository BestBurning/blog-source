---
title: Hexo免密部署到github
comments: true
date: 2017-3-03
keywords: Hexo,免密部署,github
tags:
- Linux
- Hexo
- github
categories:
- technology

---
每次用Hexo部署的时候，都要输入用户名和密码，太麻烦了，所以做一下免密登陆就很方便了
- 原理可以参考本站[《SSH免密登陆》](http://di1shuai.com/SSH免密登陆.html)
- 做法
1.  生成公钥
```
ssh-keygen
```
2.  复制 ~/.ssh/id_rsa.pub内的内容 --> 登陆github --> Setting --> SSH keys 
3.  验证
```
ssh -T git@github.com
```
看到You've successfully authenticated免密成功，快去hexo d吧！

