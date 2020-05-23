---
title: 腾讯云cdn刷新
tags: 
  - command-util
comments: true
categories: 
  - products
toc: true
donate: true
keywords: 腾讯云,cdn,刷新
date: 2020-04-07
---


在[e.coding.net](https://e.coding.net/)上用官方提供的[demo](https://codes-farm.coding.net/p/html-cos-demo/d/html-cos-demo/git)自动将`博客代码`推至**腾讯COS**后，发现涉及云函数刷新CDN的地方计费方式过于恐怖，所以用自己的方式去刷新CDN


## 前置步骤

直到`刷新CDN`之前与[demo](https://codes-farm.coding.net/p/html-cos-demo/d/html-cos-demo/git)保持一致


## 刷新cdn

在`coding`->`项目`中`构建`设置中添加一步`刷新CDN`:

```
pipeline {
  agent any
  stages {
    stage('检出') {
      steps {
        checkout([
          $class: 'GitSCM',
          branches: [[name: env.GIT_BUILD_REF]],
          userRemoteConfigs: [[url: env.GIT_REPO_URL, credentialsId: env.CREDENTIALS_ID]]
        ])
      }
    }
    stage('部署到腾讯云存储') {
      steps {
        echo '部署中...'
        sh 'coscmd config -a $TENCENT_SECRET_ID -s $TENCENT_SECRET_KEY -b $TENCENT_BUCKET -r $TENCENT_REGION'
        sh 'rm -rf .git'
        sh 'coscmd upload -r ./ /'
        echo '部署完成'
      }
    }
    stage('刷新CDN') {
      steps {
        echo '准备刷新'
        sh 'git clone https://github.com/BestBurning/tencentcloud.git'
        dir(path: './tencentcloud') {
          sh 'mvn clean package '
          sh 'java -jar ./target/tencentcloud-1.0-SNAPSHOT.jar $TENCENT_SECRET_ID $TENCENT_SECRET_KEY $TENCENT_REGION https://yourdomain/'
        }
        echo '刷新完毕'
      }
    }
  }
}
```

![](http://images.di1shuai.com/FozG5fBtNAd0NMEifDnGiTixubYN)


## 参数说明

```
java -jar ./target/tencentcloud-1.0-SNAPSHOT.jar $TENCENT_SECRET_ID $TENCENT_SECRET_KEY $TENCENT_REGION urlIndex1 urlIndex2 urlIndex3 ...

e.g.
java -jar ./target/tencentcloud-1.0-SNAPSHOT.jar $TENCENT_SECRET_ID $TENCENT_SECRET_KEY $TENCENT_REGION https://di1shuai.com/
```

1. `$TENCENT_SECRET_ID` - 腾讯云`SECRET_ID`
2. `$TENCENT_SECRET_KEY` - 腾讯云`SECRET_KEY`
3. `$TENCENT_REGION` - 腾讯云区域
4. `>=4`的参数均为要刷新的`目录`

## 单独使用

```
git clone https://github.com/BestBurning/tencentcloud.git
mvn clean package 
java -jar ./target/tencentcloud-1.0-SNAPSHOT.jar $TENCENT_SECRET_ID $TENCENT_SECRET_KEY $TENCENT_REGION https://yourdomain/
```

## 源码

[cdn刷新源码](https://github.com/BestBurning/tencentcloud)开源在[Github](https://github.com/BestBurning)

## 开源协议

采用[MIT](https://github.com/BestBurning/tencentcloud/blob/master/LICENSE)开源协议