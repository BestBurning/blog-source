---
title: 编译dll并在python中使用ctypes调用
tags: python
comments: true
categories: technology
toc: false
keywords: dll,ctypes,python
date: 2020-03-17 15:01:05
---

如题，使用vs2019编译一个动态库dll，并在python中使用ctypes调用它 


## 编译dll

1. 打开[Visual Studio 2019](https://visualstudio.microsoft.com/zh-hans/vs/)创建**动态链接库dll**项目
![dll.png](http://images.di1shuai.com/FpRIlGlU-K1aI_U4wMB5-yMZE9NO)
2. 删掉`framework.h`、`dllman.cpp`
![删除前](http://images.di1shuai.com/Fl5PZ99hx10UwApWJtZkGulC1s7v)
![删除后](http://images.di1shuai.com/FhJrLX-LQeQGeThAZJQPPpW-Ov3U)
3. 删除`pch.h`中的
```
#include "framework.h"
```
4. 新建`hellodll.cpp`文件
```
#include "pch.h"
#include <stdio.h>
#include <windows.h>


extern "C" __declspec(dllexport) int __cdecl add(int a, int b);

int __cdecl  add(int a, int b)
{
    return a + b;
}
```
5. 解决方案 -> 属性，平台为`x64`,配置管理器中也为`x64`
![解决方案.png](http://images.di1shuai.com/FtfOzKDjpjX5nOYKzmxVx-df62OV)
![配置管理器.png](http://images.di1shuai.com/FmhlqS-z_d4DS1T4AFMprVQF7gNz)
6. 生成 -> 生成解决方案
![生成解决方案.png](http://images.di1shuai.com/FqhZMNn3YZPSdUU4dg-h0b4GgfEv)
![dll路径.png](http://images.di1shuai.com/FlvWlrjgdS0yJlroVawrCTf95A0M)

## 使用python中的ctypes调用
```
# -*- coding: utf-8 -*-
import ctypes

dll = ctypes.CDLL('D:\\gitRepo\\dllrun\\hellodll.dll')
print(dll)
print(dll.add(1,2))

```
输出如下
```
<CDLL 'D:\gitRepo\dllrun\hellodll.dll', handle 7ffa26370000 at 0x24c0fa23788>
3

```

