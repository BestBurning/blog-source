---
title: JVM运行参数-JDK1.8
tags: 
  - JVM
comments: true
categories: 
  - technology
toc: true
keywords: 'JVM,参数,运行,选项'
date: 2019-11-01 21:59:58
---


> 多了解些底层总归是让自己向着真相靠近

本篇文章针对的是JDK1.8下的[JVM运行选项](https://docs.oracle.com/javase/8/docs/technotes/tools/unix/java.html),不定期更新，先来看看基本选项

```
java [options] classname [args]

java [options] -jar filename [args]

options
Command-line options separated by spaces. See Options.

classname
The name of the class to be launched.

filename
The name of the Java Archive (JAR) file to be called. Used only with the -jar option.

args
The arguments passed to the main() method separated by spaces.

```

> Options
The java command supports a wide range of options that can be divided into the following categories:
Standard Options
Non-Standard Options
Advanced Runtime Options
Advanced JIT Compiler Options
Advanced Serviceability Options
Advanced Garbage Collection Options

关于选项，可以分为六类：
- 标准选项
- 非标准选项
- 高级运行时选项
- 高级JIT编译器选项
- 先进的可维修性选项
- 高级垃圾收集选项

## 标准选项

### `-d32`
使用 32 位数据模型 (如果可用)
### `-d64`    
使用 64 位数据模型 (如果可用)
### `-server`   
选择 "server" VM,默认 VM 是 server,因为您是在服务器类计算机上运行。
### `-cp <目录和 zip/jar 文件的类搜索路径>`
### `-classpath <目录和 zip/jar 文件的类搜索路径>`
用 : 分隔的目录, JAR 档案和 ZIP 档案列表, 用于搜索类文件。
### `-D<名称>=<值>`
设置系统属性
### `-verbose:[class|gc|jni]`
启用详细输出
### `-version`      
输出产品版本并退出
### `-showversion`  
输出产品版本并继续
### `-? -help`      
输出此帮助消息
### `-X`            
输出非标准选项的帮助
### `-ea[:<packagename>...|:<classname>]`
### `-enableassertions[:<packagename>...|:<classname>]`
按指定的粒度启用断言
### `-da[:<packagename>...|:<classname>]`
### `-disableassertions[:<packagename>...|:<classname>]`
禁用具有指定粒度的断言
### `-esa | -enablesystemassertions`
启用系统断言
### `-dsa | -disablesystemassertions`
禁用系统断言
### `-agentlib:<libname>[=<选项>]`
加载本机代理库 <libname>, 例如 -agentlib:hprof
另请参阅 -agentlib:jdwp=help 和 -agentlib:hprof=help
### `-agentpath:<pathname>[=<选项>]`
按完整路径名加载本机代理库
### `-javaagent:<jarpath>[=<选项>]`
加载 Java 编程语言代理, 请参阅 java.lang.instrument
### `-splash:<imagepath>`
使用指定的图像显示启动屏幕


## 非标准选项


### `-Xbatch`           
禁用后台编译
### `-Xbootclasspath/a:<以 : 分隔的目录和 zip/jar 文件>` 
附加在引导类路径末尾
### `-Xcheck:jni`       
对 JNI 函数执行其他检查
### `-Xcomp`            
在首次调用时强制编译方法
### `-Xdebug`          
为实现向后兼容而提供
### `-Xdiag`           
显示附加诊断消息
### `-Xfuture`          
启用最严格的检查，预期将来的默认值
### `-Xint`             
仅解释模式执行
### `-Xinternalversion`  
显示比 -version 选项更详细的JVM版本信息
```
➜  ~ java -Xinternalversion
Java HotSpot(TM) 64-Bit Server VM (25.181-b13) for bsd-amd64 JRE (1.8.0_181-b13), built on Jul  7 2018 01:02:31 by "java_re" with gcc 4.2.1 (Based on Apple Inc. build 5658) (LLVM build 2336.11.00)
```
### `-Xloggc:<文件>`    
将 GC 状态记录在文件中（带时间戳）
### `-Xmixed`           
混合模式执行（默认值）
### `-Xmn<大小>`        
为年轻代（新生代）设置初始和最大堆大小以字节为单位）
### `-Xms<大小>`        
设置初始 Java 堆大小
### `-Xmx<大小>`        
设置最大 Java 堆大小
### `-Xnoclassgc`       
禁用类垃圾收集
### `-Xrs`             
减少 Java/VM 对操作系统信号的使用（请参见文档）
### `-Xshare:auto`      
在可能的情况下使用共享类数据（默认值）
### `-Xshare:off`       
不尝试使用共享类数据
### `-Xshare:on`        
要求使用共享类数据，否则将失败。
### `-XshowSettings`    
显示所有设置并继续
### `-XshowSettings:all` 
显示所有设置并继续
### `-XshowSettings:locale` 
显示所有与区域设置相关的设置并继续
### `-XshowSettings:properties` 
显示所有属性设置并继续
### `-XshowSettings:vm` 
显示所有与 vm 相关的设置并继续
### `-XshowSettings:system` 
（仅 Linux）显示主机系统或容器配置并继续
### `-Xss<大小>`        
设置 Java 线程堆栈大小
### `-Xverify`          
设置字节码验证器的模式


## 高级运行时选项


## 高级JIT编译器选项


## 先进的可维修性选项


## 高级垃圾收集选项