---
title: 使用Hexo打造自己的个人博客
comments: true
date: 2016-08-20 07:45:22
keywords: Hexo,博客
tags: 
- Hexo
categories: 
- technology
---
Now we can use hexo,github and your domain to make a site like here.
You must prepare something:
- hexo 
- github account 
- your domain 

### Use Hexo 
1. Install node
hexo used node so we must install node before all,I use homebrew in Mac:
```
brew install node
```
2. Create blog folder and  install hexo :
```
mkdir blog
cd blog
npm install hexo-cli -g
```
3. Test hexo :
```
hexo server
```
then you can visit [http://localhost:4000](http://localhost:4000) to see your hexo blog
all config info in _config.yml

### Use github domain mapping your blog
now we will use usename.github.io domain mapping your blog
1. create your io repository 
create it and the repository name must be **user_name.github.io**,user_name is your github user name
like me [https://github.com/BestBurning](https://github.com/BestBurning) so my user name is **BestBurning** and my io domain repo is **BestBurning.github.io**
2. mapping your local blog
change _config.yml
```
vi _config.yml
```
at the bottom，you can find **deploy**,make it like 
```
deploy:
    type: git
    repo: https://github.com/BestBurning/BestBurning.github.io.git
    branch: master
```
save and exec command 
```
npm install hexo-deployer-git --save
hexo deploy
```
then you can visit your io domain like [bestburning.github.io](https://bestburning.github.io)

### Mapping your own domain to github.io domain 

[diyishuai.cn](http://diyishuai.cn) is my domain , and if you visit it will redirect to [bestburning.github.io](https://bestburning.github.io) 
1. Use your domain analyze to your user_name.github.io
	- add CNAME with www to point user_name.github.io
	- add A with @ to point io domian ip
2. at blog/soruce folder ,touch file named CNAME
```
vi blog/CNAME
```
add your domain to it
```
diyishuai.cn
```
deploy it
```
hexo deploy
```
3. then you can visit [diyishuai.cn](http://diyishuai.cn) to visit your blog

---
hexo have some themes you can select it ,good luck!
