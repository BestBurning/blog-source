---
title: JVM工具之jinfo
tags: 
  - JVM
  - jinfo
comments: true
categories: 
  - technology
toc: false
keywords: 'jinfo,JVM工具,JVM'
date: 2019-10-30 21:24:20
---


[jinfo](https://docs.oracle.com/javase/8/docs/technotes/tools/unix/jinfo.html#BCGEBFDD)是JDK自带的工具,可以：
  - 查看Java程序的扩展参数
  - 动态修改JVM参数
  - 在系统崩溃时从core文件中得知Java程序的配置信息

## 命令

```
➜  myworld git:(master) ✗ jinfo -h
Usage:
    jinfo [option] <pid>
        (to connect to running process)
    jinfo [option] <executable <core>
        (to connect to a core file)
    jinfo [option] [server_id@]<remote server IP or hostname>
        (to connect to remote debug server)

where <option> is one of:
    -flag <name>         to print the value of the named VM flag
    -flag [+|-]<name>    to enable or disable the named VM flag
    -flag <name>=<value> to set the named VM flag to the given value
    -flags               to print VM flags
    -sysprops            to print Java system properties
    <no option>          to print both of the above
    -h | -help           to print this help message
```

### 参数说明
  - `pid`为JVM进程ID，可以通过`jps -l`来查找对应的`pid`
  - executable core 产生core dump文件

### Option
  
  - `-flag <name>` 输出对应名称的参数
  - `-flag [+|-]<name>` 动态开启或者关闭对应名称的参数
  - `-flag <name>=<value>` 动态设定对应名称的参数
  - `-flags` 输出全部的参数
  - `-sysprops` 输出系统属性
  - `<no option>` 输出全部的参数和系统属性

### Code

代码都放在了GitHub上:
[Demo类代码](https://github.com/BestBurning/myworld/blob/master/java/src/main/java/com/diyishuai/gc/HelloJVM.java)
[执行脚本](https://github.com/BestBurning/myworld/blob/master/java/src/main/resources/jinfo.sh)
```
public class HelloJVM {

    public static void main(String[] args) throws InterruptedException {
        System.out.println("RUN HelloJVM");
        TimeUnit.SECONDS.sleep(Integer.MAX_VALUE);
    }

}

```

### `jinfo -flag <name> <pid>` - 输出对应名称的参数

```
➜  classes git:(master) ✗ java -XX:+PrintClassHistogram com.diyishuai.gc.HelloJVM &
➜  classes git:(master) ✗ jps -l | grep HelloJVM
2282 com.diyishuai.gc.HelloJVM
➜  classes git:(master) ✗ jinfo -flag PrintClassHistogram 2282
-XX:+PrintClassHistogram
```



### `jinfo -flag [+|-]<name> <pid>` 动态开启或者关闭对应名称的参数

```
➜  classes git:(master) ✗ jinfo -flag PrintClassHistogram 2282
-XX:+PrintClassHistogram
➜  classes git:(master) ✗ jinfo -flag -PrintClassHistogram 2282
➜  classes git:(master) ✗ jinfo -flag PrintClassHistogram 2282
-XX:-PrintClassHistogram
```
可以看到`PrintClassHistogram`已经被修改为`-(false)`


### `jinfo -flag <name>=<value> <pid>` 动态设定对应名称的参数

```
➜  classes git:(master) ✗ jinfo -flag CMSWaitDuration  2282
-XX:CMSWaitDuration=2000
➜  classes git:(master) ✗ jinfo -flag CMSWaitDuration=1999  2282
➜  classes git:(master) ✗ jinfo -flag CMSWaitDuration  2282
-XX:CMSWaitDuration=1999
```
注意：并不是所有参数都可以动态调整的,在[Oracle官网](https://www.oracle.com/partners/campaign/vmoptions-jsp-140102.html)中有一段
> Flags marked as manageable are dynamically writeable through the JDK management interface (com.sun.management.HotSpotDiagnosticMXBean API) and also through JConsole

注明了被标记为`manageable`的参数可以被动态修改，即`JDK1.8`的如下参数:
```
➜  classes git:(master) ✗ java -XX:+PrintFlagsInitial | grep manageable
     intx CMSAbortablePrecleanWaitMillis            = 100                                 {manageable}
     intx CMSTriggerInterval                        = -1                                  {manageable}
     intx CMSWaitDuration                           = 2000                                {manageable}
     bool HeapDumpAfterFullGC                       = false                               {manageable}
     bool HeapDumpBeforeFullGC                      = false                               {manageable}
     bool HeapDumpOnOutOfMemoryError                = false                               {manageable}
    ccstr HeapDumpPath                              =                                     {manageable}
    uintx MaxHeapFreeRatio                          = 70                                  {manageable}
    uintx MinHeapFreeRatio                          = 40                                  {manageable}
     bool PrintClassHistogram                       = false                               {manageable}
     bool PrintClassHistogramAfterFullGC            = false                               {manageable}
     bool PrintClassHistogramBeforeFullGC           = false                               {manageable}
     bool PrintConcurrentLocks                      = false                               {manageable}
     bool PrintGC                                   = false                               {manageable}
     bool PrintGCDateStamps                         = false                               {manageable}
     bool PrintGCDetails                            = false                               {manageable}
     bool PrintGCID                                 = false                               {manageable}
     bool PrintGCTimeStamps                         = false                               {manageable}
```

`JDK11`的如下参数:
```
➜  myworld git:(master) ✗ java -XX:+PrintFlagsInitial | grep manageable
     intx CMSAbortablePrecleanWaitMillis           = 100                                    {manageable} {default}
     intx CMSTriggerInterval                       = -1                                     {manageable} {default}
     intx CMSWaitDuration                          = 2000                                   {manageable} {default}
     bool HeapDumpAfterFullGC                      = false                                  {manageable} {default}
     bool HeapDumpBeforeFullGC                     = false                                  {manageable} {default}
     bool HeapDumpOnOutOfMemoryError               = false                                  {manageable} {default}
    ccstr HeapDumpPath                             =                                        {manageable} {default}
    uintx MaxHeapFreeRatio                         = 70                                     {manageable} {default}
    uintx MinHeapFreeRatio                         = 40                                     {manageable} {default}
     bool PrintClassHistogram                      = false                                  {manageable} {default}
     bool PrintConcurrentLocks                     = false                                  {manageable} {default}

```


### `jinfo -flags <pid>` 输出全部的参数

```
➜  classes git:(master) ✗ jinfo -flags 4689
VM Flags:
-XX:CICompilerCount=3 -XX:InitialHeapSize=134217728 -XX:MaxHeapSize=2147483648 -XX:MaxNewSize=715653120 -XX:MinHeapDeltaBytes=524288 -XX:NewSize=44564480 -XX:OldSize=89653248 -XX:+UseCompressedClassPointers -XX:+UseCompressedOops -XX:+UseFastUnorderedTimeStamps -XX:+UseParallelGC
```
有木有注意到`pid`从`2282`变成了`4689`,那是因为用`JDK1.8`执行的时候发生了下面的错误并且导致进程结束:
```
➜  classes git:(master) ✗ jinfo -flags 2282
Attaching to process ID 2282, please wait...
Error attaching to process: sun.jvm.hotspot.debugger.DebuggerException: Can't attach symbolicator to the process
sun.jvm.hotspot.debugger.DebuggerException: sun.jvm.hotspot.debugger.DebuggerException: Can't attach symbolicator to the process
	at sun.jvm.hotspot.debugger.bsd.BsdDebuggerLocal$BsdDebuggerLocalWorkerThread.execute(BsdDebuggerLocal.java:169)
	at sun.jvm.hotspot.debugger.bsd.BsdDebuggerLocal.attach(BsdDebuggerLocal.java:287)
	at sun.jvm.hotspot.HotSpotAgent.attachDebugger(HotSpotAgent.java:671)
	at sun.jvm.hotspot.HotSpotAgent.setupDebuggerDarwin(HotSpotAgent.java:659)
	at sun.jvm.hotspot.HotSpotAgent.setupDebugger(HotSpotAgent.java:341)
	at sun.jvm.hotspot.HotSpotAgent.go(HotSpotAgent.java:304)
	at sun.jvm.hotspot.HotSpotAgent.attach(HotSpotAgent.java:140)
	at sun.jvm.hotspot.tools.Tool.start(Tool.java:185)
	at sun.jvm.hotspot.tools.Tool.execute(Tool.java:118)
	at sun.jvm.hotspot.tools.JInfo.main(JInfo.java:138)
	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
	at java.lang.reflect.Method.invoke(Method.java:498)
	at sun.tools.jinfo.JInfo.runTool(JInfo.java:108)
	at sun.tools.jinfo.JInfo.main(JInfo.java:76)
Caused by: sun.jvm.hotspot.debugger.DebuggerException: Can't attach symbolicator to the process
	at sun.jvm.hotspot.debugger.bsd.BsdDebuggerLocal.attach0(Native Method)
	at sun.jvm.hotspot.debugger.bsd.BsdDebuggerLocal.access$100(BsdDebuggerLocal.java:65)
	at sun.jvm.hotspot.debugger.bsd.BsdDebuggerLocal$1AttachTask.doit(BsdDebuggerLocal.java:278)
	at sun.jvm.hotspot.debugger.bsd.BsdDebuggerLocal$BsdDebuggerLocalWorkerThread.run(BsdDebuggerLocal.java:144)
```
通过多方查证这是个[Bug](https://bugs.java.com/bugdatabase/view_bug.do?bug_id=8160376),切换到`JDK11`解决了，切换`JDK`可以参考——[JDK版本管理-jEnv](https://di1shuai.com/JDK%E7%89%88%E6%9C%AC%E7%AE%A1%E7%90%86-jEnv.html)
### `jinfo -sysprops <pid>` - 输出系统属性
```
➜  classes git:(master) ✗ jinfo -sysprops 4913
Java System Properties:
#Wed Oct 30 21:49:54 CST 2019
java.runtime.name=Java(TM) SE Runtime Environment
sun.boot.library.path=/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib
java.vm.version=25.181-b13
gopherProxySet=false
java.vm.vendor=Oracle Corporation
java.vendor.url=http\://java.oracle.com/
path.separator=\:
java.vm.name=Java HotSpot(TM) 64-Bit Server VM
file.encoding.pkg=sun.io
user.country=CN
sun.java.launcher=SUN_STANDARD
sun.os.patch.level=unknown
java.vm.specification.name=Java Virtual Machine Specification
user.dir=/Users/shuai/Documents/GitRepo/mine/myworld/myworld
java.runtime.version=1.8.0_181-b13
java.awt.graphicsenv=sun.awt.CGraphicsEnvironment
java.endorsed.dirs=/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/endorsed
os.arch=x86_64
java.io.tmpdir=/var/folders/3j/ktww_n8n447775zlllrnc1540000gn/T/
line.separator=\n
socksProxyPort=1090
java.vm.specification.vendor=Oracle Corporation
os.name=Mac OS X
sun.jnu.encoding=UTF-8
java.library.path=/Users/shuai/Library/Java/Extensions\:/Library/Java/Extensions\:/Network/Library/Java/Extensions\:/System/Library/Java/Extensions\:/usr/lib/java\:.
java.specification.name=Java Platform API Specification
java.class.version=52.0
sun.management.compiler=HotSpot 64-Bit Tiered Compilers
os.version=10.15
http.nonProxyHosts=127.0.0.1|192.168.0.0/16|*.192.168.0.0/16|10.0.0.0/8|*.10.0.0.0/8|localhost|*.localhost
user.home=/Users/shuai
user.timezone=Asia/Shanghai
java.awt.printerjob=sun.lwawt.macosx.CPrinterJob
file.encoding=UTF-8
java.specification.version=1.8
java.class.path=/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/charsets.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/deploy.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/cldrdata.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/dnsns.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/jaccess.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/jfxrt.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/localedata.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/nashorn.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/sunec.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/sunjce_provider.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/sunpkcs11.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/zipfs.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/javaws.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/jce.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/jfr.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/jfxswt.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/jsse.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/management-agent.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/plugin.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/resources.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/rt.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/lib/ant-javafx.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/lib/dt.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/lib/javafx-mx.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/lib/jconsole.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/lib/packager.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/lib/sa-jdi.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/lib/tools.jar\:/Users/shuai/Documents/GitRepo/mine/myworld/myworld/java/target/classes\:/Users/shuai/Library/Application Support/JetBrains/Toolbox/apps/IDEA-U/ch-0/192.6817.14/IntelliJ IDEA.app/Contents/lib/idea_rt.jar
user.name=shuai
socksProxyHost=127.0.0.1
java.vm.specification.version=1.8
sun.java.command=com.diyishuai.gc.HelloJVM
java.home=/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre
sun.arch.data.model=64
user.language=zh
java.specification.vendor=Oracle Corporation
awt.toolkit=sun.lwawt.macosx.LWCToolkit
java.vm.info=mixed mode
java.version=1.8.0_181
java.ext.dirs=/Users/shuai/Library/Java/Extensions\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext\:/Library/Java/Extensions\:/Network/Library/Java/Extensions\:/System/Library/Java/Extensions\:/usr/lib/java
sun.boot.class.path=/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/resources.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/rt.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/sunrsasign.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/jsse.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/jce.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/charsets.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/jfr.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/classes
java.vendor=Oracle Corporation
file.separator=/
java.vendor.url.bug=http\://bugreport.sun.com/bugreport/
sun.io.unicode.encoding=UnicodeBig
sun.cpu.endian=little
socksNonProxyHosts=127.0.0.1|192.168.0.0/16|*.192.168.0.0/16|10.0.0.0/8|*.10.0.0.0/8|localhost|*.localhost
ftp.nonProxyHosts=127.0.0.1|192.168.0.0/16|*.192.168.0.0/16|10.0.0.0/8|*.10.0.0.0/8|localhost|*.localhost
sun.cpu.isalist=
```

### `jinfo <pid>` - 输出当前JVM进程的全部参数和系统属性
```
➜  classes git:(master) ✗ jinfo  4913
Java System Properties:
#Wed Oct 30 21:52:27 CST 2019
java.runtime.name=Java(TM) SE Runtime Environment
sun.boot.library.path=/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib
java.vm.version=25.181-b13
gopherProxySet=false
java.vm.vendor=Oracle Corporation
java.vendor.url=http\://java.oracle.com/
path.separator=\:
java.vm.name=Java HotSpot(TM) 64-Bit Server VM
file.encoding.pkg=sun.io
user.country=CN
sun.java.launcher=SUN_STANDARD
sun.os.patch.level=unknown
java.vm.specification.name=Java Virtual Machine Specification
user.dir=/Users/shuai/Documents/GitRepo/mine/myworld/myworld
java.runtime.version=1.8.0_181-b13
java.awt.graphicsenv=sun.awt.CGraphicsEnvironment
java.endorsed.dirs=/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/endorsed
os.arch=x86_64
java.io.tmpdir=/var/folders/3j/ktww_n8n447775zlllrnc1540000gn/T/
line.separator=\n
socksProxyPort=1090
java.vm.specification.vendor=Oracle Corporation
os.name=Mac OS X
sun.jnu.encoding=UTF-8
java.library.path=/Users/shuai/Library/Java/Extensions\:/Library/Java/Extensions\:/Network/Library/Java/Extensions\:/System/Library/Java/Extensions\:/usr/lib/java\:.
java.specification.name=Java Platform API Specification
java.class.version=52.0
sun.management.compiler=HotSpot 64-Bit Tiered Compilers
os.version=10.15
http.nonProxyHosts=127.0.0.1|192.168.0.0/16|*.192.168.0.0/16|10.0.0.0/8|*.10.0.0.0/8|localhost|*.localhost
user.home=/Users/shuai
user.timezone=Asia/Shanghai
java.awt.printerjob=sun.lwawt.macosx.CPrinterJob
file.encoding=UTF-8
java.specification.version=1.8
java.class.path=/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/charsets.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/deploy.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/cldrdata.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/dnsns.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/jaccess.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/jfxrt.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/localedata.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/nashorn.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/sunec.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/sunjce_provider.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/sunpkcs11.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/zipfs.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/javaws.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/jce.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/jfr.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/jfxswt.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/jsse.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/management-agent.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/plugin.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/resources.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/rt.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/lib/ant-javafx.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/lib/dt.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/lib/javafx-mx.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/lib/jconsole.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/lib/packager.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/lib/sa-jdi.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/lib/tools.jar\:/Users/shuai/Documents/GitRepo/mine/myworld/myworld/java/target/classes\:/Users/shuai/Library/Application Support/JetBrains/Toolbox/apps/IDEA-U/ch-0/192.6817.14/IntelliJ IDEA.app/Contents/lib/idea_rt.jar
user.name=shuai
socksProxyHost=127.0.0.1
java.vm.specification.version=1.8
sun.java.command=com.diyishuai.gc.HelloJVM
java.home=/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre
sun.arch.data.model=64
user.language=zh
java.specification.vendor=Oracle Corporation
awt.toolkit=sun.lwawt.macosx.LWCToolkit
java.vm.info=mixed mode
java.version=1.8.0_181
java.ext.dirs=/Users/shuai/Library/Java/Extensions\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext\:/Library/Java/Extensions\:/Network/Library/Java/Extensions\:/System/Library/Java/Extensions\:/usr/lib/java
sun.boot.class.path=/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/resources.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/rt.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/sunrsasign.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/jsse.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/jce.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/charsets.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/jfr.jar\:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/classes
java.vendor=Oracle Corporation
file.separator=/
java.vendor.url.bug=http\://bugreport.sun.com/bugreport/
sun.io.unicode.encoding=UnicodeBig
sun.cpu.endian=little
socksNonProxyHosts=127.0.0.1|192.168.0.0/16|*.192.168.0.0/16|10.0.0.0/8|*.10.0.0.0/8|localhost|*.localhost
ftp.nonProxyHosts=127.0.0.1|192.168.0.0/16|*.192.168.0.0/16|10.0.0.0/8|*.10.0.0.0/8|localhost|*.localhost
sun.cpu.isalist=

VM Flags:
-XX:CICompilerCount=3 -XX:InitialHeapSize=134217728 -XX:MaxHeapSize=2147483648 -XX:MaxNewSize=715653120 -XX:MinHeapDeltaBytes=524288 -XX:NewSize=44564480 -XX:OldSize=89653248 -XX:+UseCompressedClassPointers -XX:+UseCompressedOops -XX:+UseFastUnorderedTimeStamps -XX:+UseParallelGC

VM Arguments:
jvm_args: -javaagent:/Users/shuai/Library/Application Support/JetBrains/Toolbox/apps/IDEA-U/ch-0/192.6817.14/IntelliJ IDEA.app/Contents/lib/idea_rt.jar=55087:/Users/shuai/Library/Application Support/JetBrains/Toolbox/apps/IDEA-U/ch-0/192.6817.14/IntelliJ IDEA.app/Contents/bin -Dfile.encoding=UTF-8
java_command: com.diyishuai.gc.HelloJVM
java_class_path (initial): /Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/charsets.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/deploy.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/cldrdata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/dnsns.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/jaccess.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/jfxrt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/localedata.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/nashorn.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/sunec.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/sunjce_provider.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/sunpkcs11.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/ext/zipfs.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/javaws.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/jce.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/jfr.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/jfxswt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/jsse.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/management-agent.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/plugin.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/resources.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/jre/lib/rt.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home/lib/ant-javafx.jar:/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home
Launcher Type: SUN_STANDARD
```

## 总结
jinfo工具可以查看JVM进程参数，可以查看单个或者全部，也可以动态修改JVM参数，不过动态修改的参数是有限的，在`JDK1.8`下，`jinfo -flags <pid>`存在严重的BUG会导致进程结束。