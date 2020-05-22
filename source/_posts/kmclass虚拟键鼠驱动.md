---
title: kmclass虚拟键鼠驱动
tags: 
  - driver
  - Windows
comments: true
categories: 
  - products
toc: true
donate: true
keywords: kmclass,kmclassdll,c++,Windows
date: 2020-03-18
---

[kmclass](https://github.com/BestBurning/kmclass)-虚拟键鼠驱动,可配合 [kmclassdll](https://github.com/BestBurning/kmclassdll)-虚拟键鼠驱动的动态库 使用

## 编译或下载

如需使用，可以自行编译**或**下载

### 编译

建议使用[Visual Studio 2019](https://visualstudio.microsoft.com/zh-hans/vs/)进行编译

dll编译可参考 [编译dll并在python中使用ctypes调用](https://di1shuai.com/%E7%BC%96%E8%AF%91dll%E5%B9%B6%E5%9C%A8python%E4%B8%AD%E4%BD%BF%E7%94%A8ctypes%E8%B0%83%E7%94%A8.html)

### 下载

仅提供`x64`的编译文件，如需其他版本，请自行编译
- [kmclass.sys](https://github.com/BestBurning/kmclass/releases) - 驱动
- [kmclassdll.dll](https://github.com/BestBurning/kmclassdll/releases) - 动态库

## python 示例

示例文件为 [python_examples.py](https://github.com/BestBurning/kmclassdll/blob/master/python_examples.py)

1. 自行编译或下载
   - [kmclassdll.dll](https://github.com/BestBurning/kmclassdll/releases) - 动态库
   - [kmclass.sys](https://github.com/BestBurning/kmclass/releases) - 驱动

2. 修改变量路径为你的真实路径
   - `dll_path`
   - `driver_path`

```
dll_path = 'YourPath\\kmclassdll.dll'
driver_path = b'YourPath\\kmclass.sys'
```

3. 开启 **测试模式** & **禁用强制驱动签名** 模式 & **重启**

`管理员身份`打开`CMD`

```
bcdedit /set nointegritychecks on
bcdedit /set testsigning on
shutdown  -r -t 0
```

4. 重启后**管理员身份**运行

```
python python_examples.py
```

## 资料

[Windows 硬件开发人员文档](https://docs.microsoft.com/zh-cn/windows-hardware/drivers/)

[编写通用 Hello World 驱动程序 (KMDF)](https://docs.microsoft.com/zh-cn/windows-hardware/drivers/gettingstarted/writing-a-very-small-kmdf--driver)

[系统错误代码大全](https://docs.microsoft.com/zh-cn/windows/win32/debug/system-error-codes)

[预配计算机以便进行驱动程序部署和测试 (WDK 10)](https://docs.microsoft.com/zh-cn/windows-hardware/drivers/gettingstarted/provision-a-target-computer-wdk-8-1)

## 源码

[kmclass源码](https://github.com/BestBurning/kmclass)与[kmclassdll源码](https://github.com/BestBurning/kmclassdll)均开源在[Github](https://github.com/BestBurning)上,
并采用了[AGPL3.0](https://opensource.org/licenses/AGPL-3.0)开源协议
