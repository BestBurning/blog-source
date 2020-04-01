---
title: 各种命令行代理
tags: 
    - npm
    - 代理
comments: true
categories: 
    - technology
originContent: ''
toc: false
keywords: 命令行,代理,Mac,Windows,npm
date: 2020-02-14 16:46:29
---

### Mac Linux terminal 

1. 修改`.zshrc`
```
vim ~/.zshrc
```

2. 在`alias`区块下添加如下内容，代理地址记得填写你自己的
```
alias proxy="
    export http_proxy=socks5://127.0.0.1:1090;
    export https_proxy=socks5://127.0.0.1:1090;
    export all_proxy=socks5://127.0.0.1:1090;
    export no_proxy=socks5://127.0.0.1:1090;
    export HTTP_PROXY=socks5://127.0.0.1:1090;
    export HTTPS_PROXY=socks5://127.0.0.1:1090;
    export ALL_PROXY=socks5://127.0.0.1:1090;
    export NO_PROXY=socks5://127.0.0.1:1090;"
alias unproxy="
    unset http_proxy;
    unset https_proxy;
    unset all_proxy;
    unset no_proxy;
    unset HTTP_PROXY;
    unset HTTPS_PROXY;
    unset ALL_PROXY;
    unset NO_PROXY"
```
3. 测试一下
```
$ curl https://ip.cn
>> {"country": "山西省临汾市", "city": "移动"}

$ proxy

$ curl https://ip.cn
>> {"country": "美国", "city": "Choopa"}

$ unproxy

$ curl https://ip.cn
>> {"country": "山西省临汾市", "city": "移动"}
```

### Windows

代理
```
set http_proxy=http://localhost:1080
set https_proxy=http://localhost:1080
```

复原
```
set http_proxy=
set https_proxy=
```


### npm

代理
```
npm config set https-proxy http://server:port
```

复原
```
npm config delete https-proxy
```

