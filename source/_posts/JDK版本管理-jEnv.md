---
title: JDK版本管理-jEnv
tags: 
  - JDK
  - jEnv
comments: true
categories: 
  - technology
toc: false
keywords: 'JDK,jEnv,版本管理,jenv'
date: 2019-10-30 17:27:32
---


# jEnv

Node可以使用nvm进行方便的管理，那Java有没有相关的管理工具呢？当然是有的，它就是[jEnv](https://www.jenv.be/)
> Manage your Java environment

## 安装
如下给出Mac和Linux下安装方式
- Mac
使用[homebrew](https://brew.sh/)进行安装
```
brew install jenv
```
- Linux
```
git clone https://github.com/gcuisinier/jenv.git ~/.jenv
```
## 环境变量以及初始化
如下给出`zsh`以及`bash`下的配置方式
- zsh
```
$ echo 'export PATH="$HOME/.jenv/bin:$PATH"' >> ~/.zshrc
$ echo 'eval "$(jenv init -)"' >> ~/.zshrc
```
- bash
```
$ echo 'export PATH="$HOME/.jenv/bin:$PATH"' >> ~/.bash_profile
$ echo 'eval "$(jenv init -)"' >> ~/.bash_profile
```

## 配置
将`JDK`加入jEnv中
### 查看JDK安装目录
Mac下的JDK安装目录在`/Library/Java/JavaVirtualMachines/`下
```
➜  ~ ll /Library/Java/JavaVirtualMachines/
total 0
drwxr-xr-x  3 root  wheel    96B 10 30 10:47 jdk-11.0.5.jdk
drwxr-xr-x  3 root  wheel    96B  8 19  2018 jdk1.8.0_181.jdk
```
### 使用`jenv add /javaPath`将各JDK版本加入jenv中
```
➜  ~ jenv add /Library/Java/JavaVirtualMachines/jdk-11.0.5.jdk/Contents/Home
oracle64-11.0.5 added
11.0.5 added
11.0 added
➜  ~ jenv add /Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home
oracle64-1.8.0.181 added
1.8.0.181 added
1.8 added
```

## 使用

### `jenv versions` - 查看JDK版本信息
```
➜  ~ jenv versions
  system
  1.8
  1.8.0.181
* 11.0 (set by /Users/shuai/.jenv/version)
  11.0.5
  oracle64-1.8.0.181
  oracle64-11.0.5
```
`*`表示当前全局默认使用的版本

### `jevn version` - 查看当前使用的JDK版本信息
```
➜  ~ jenv version
11.0 (set by /Users/shuai/.jenv/version)
➜  ~ java -version
java version "11.0.5" 2019-10-15 LTS
Java(TM) SE Runtime Environment 18.9 (build 11.0.5+10-LTS)
Java HotSpot(TM) 64-Bit Server VM 18.9 (build 11.0.5+10-LTS, mixed mode)
```

### `jenv global <version>` - 修改全局默认版本
```
➜  ~ jenv version
11.0 (set by /Users/shuai/.jenv/version)
➜  ~ jenv global 1.8
➜  ~ jenv versions
  system
* 1.8 (set by /Users/shuai/.jenv/version)
  1.8.0.181
  11.0
  11.0.5
  oracle64-1.8.0.181
  oracle64-11.0.5
```
可以看到JDK版由`11.0`切换到了`1.8`,全局默认版本信息记录在`~/.jenv/version`中

### `jenv local <version>` - 本地版本修改
通过版本修改可以为不同的项目设置不同的JDK版本
```
➜  myworld git:(master) ✗ pwd
/Users/shuai/Documents/GitRepo/mine/myworld/myworld
➜  myworld git:(master) ✗ jenv version
1.8 (set by /Users/shuai/.jenv/version)
➜  myworld git:(master) ✗ jenv local 11.0
➜  myworld git:(master) ✗ jenv version
11.0 (set by /Users/shuai/Documents/GitRepo/mine/myworld/myworld/.java-version)
➜  myworld git:(master) ✗ cd ~
➜  ~ jenv version
1.8 (set by /Users/shuai/.jenv/version)
```
可以看到在`myworld`文件夹中JDK版本被修改为了`11.0`，不过并不影响其他目录，因为`local`的JDK版本信息是记录在所修改文件下夹下的`.java-version`文件中的。

### `jenv enable-plugin export` - 启用export插件
`export`当前默认版本的`JAVA_HOME`

## 总结
使用下来的话，还是没有`nvm`那样方便，需要自己下载各种版本的JDK，需要手动添加到`jenv`中，期待其更便利化的发展