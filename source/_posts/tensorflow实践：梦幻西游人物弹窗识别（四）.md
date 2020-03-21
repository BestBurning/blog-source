---
title: tensorflow实践：梦幻西游人物弹窗识别（四）
tags: 
- tensorflow
- 梦幻西游
comments: true
categories: 
- technology
toc: true
keywords: tensorflow,梦幻西游,弹窗识别,python,自动点击,图像识别,虚拟鼠标驱动
date: 2020-03-21 10:36:29
---


在[上一篇文章](https://di1shuai.com/tensorflow%E5%AE%9E%E8%B7%B5%EF%BC%9A%E6%A2%A6%E5%B9%BB%E8%A5%BF%E6%B8%B8%E4%BA%BA%E7%89%A9%E5%BC%B9%E7%AA%97%E8%AF%86%E5%88%AB%EF%BC%88%E4%B8%89%EF%BC%89.html)中我们已经能够预测切分好的一组照片，现在只需要**点击**被预测的**区域中心**就好了
我们将按以下思路进行
![](http://images.di1shuai.com/FpZrIhU_FWqG837tyzBUtR4l-f55)

本篇将围绕**截图匹配、点击中心坐标**讲述[main.py](https://github.com/BestBurning/mhxy/blob/master/main.py)、[screen.py](https://github.com/BestBurning/mhxy/blob/master/screen.py)、[auto.py](https://github.com/BestBurning/mhxy/blob/master/auto.py)、[keymouse.py](https://github.com/BestBurning/mhxy/blob/master/keymouse.py)代码

### 环境描述
由于**鼠标点击**使用了[kmclassdll](https://github.com/BestBurning/kmclassdll)，所以需要开启 **测试模式** & **禁用强制驱动签名** 并 **重启**

`管理员身份`打开`CMD`
```
bcdedit /set nointegritychecks on
bcdedit /set testsigning on
shutdown  -r -t 0
```

### 截图匹配
使用预测图片**索引**去找到对应**图片**，于是使用这张被预测的图片去**桌面截图**中匹配，并返回匹配到的**区域中心**
![](http://images.di1shuai.com/FkCp-lFd4RqmtYf-H1iCqMfMFNgd)

`main.py`
```
min_index = dm.model_predict(c.crop_4_img_paths)
target_x , target_y = sc.find_xy_indesktop(c.crop_4_img_paths[min_index])
```
`screen.py`
```
def find_xy_indesktop(template_path):
    util.log_title('坐标查找')
    shape,score = template_match(template_path,c.img_desktop_path)
    print(f'最高得分区域 {shape} 得分为 {score}')
    if score >= 3:
        x = (shape[2]+shape[0])//2
        y = (shape[3]+shape[1])//2
        print(f'中心点坐标为 {(x,y)}')
        return x,y
    else:
        print(f'所有区域得分均小于3，匹配失败')
        return 0,0

```
```
--------   模型预测    ----------

2020-03-21 15:57:49.720468: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cublas64_10.dll
2020-03-21 15:57:50.521308: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cudnn64_7.dll
2020-03-21 15:57:52.768875: W tensorflow/stream_executor/gpu/redzone_allocator.cc:312] Internal: Invoking GPU asm compilation is supported on Cuda non-Windows platforms only
Relying on driver to perform ptx compilation. This message will be only logged once.
[4.032246, 6.499766, 5.2396355, 33.076145]
 预测结果为 第 > 1 < 张图片

--------   坐标查找    ----------

最高得分区域 (340, 300, 430, 420) 得分为 4
中心点坐标为 (385, 360)
```
### 点击区域中心



接下来就是把鼠标**移**到**目标点**，再**点击**一下就好了！

是不是**很简单**！**！**！**！**！

![](http://images.di1shuai.com/FoFyAQ7RQg-ShqxfQWBQk6vntrdw)

#### 移至目标点

于是我使用`pyautogui`**移动** -> **目标点**

```
pyautogui.moveTo(target_x , target_y)
```

![](http://images.di1shuai.com/FoHxcmn5OS9Bob9F0auLFM78eUSB)
咦？它怎么**没有**移到**对应**位置！！每次它都是移到目标点**附近**
于是我把梦幻窗口**移开**，移动，**Work**！
把梦幻窗口**挪回来**，移动，**No** Work！
经过研究
原来
梦幻窗口内的坐标并**不**是**真实**的坐标，他的真实坐标可以用**CE**读取**内存基址**来获取
这个**CE**是什么？
全拼`Cheat Engine`，中文`作弊引擎`
![](http://images.di1shuai.com/Fl4S5PlZN7kYeSzMvjgxNNjBvG2H)

![](http://images.di1shuai.com/Fputsx1KWvkik4u8YUiTd6yozimN)

于是我用了另一种思路——**二**次**逼**近：

**第一次**移动到目标点**附近**，然后用**梦幻鼠标标识**去**匹配此时桌面**截图，这样就能获得**此时**鼠标的**真实位置**
**第二次**鼠标使用**相对位移**移到目标点，搞定~
![](http://images.di1shuai.com/FvsfJcYbrsVcz9aN7dWEH15viVdp)

![](http://images.di1shuai.com/FrksXgrWXjrHVweU9RMy0wpaw1zK)
`main.py`
```
auto.move_to(target_x,target_y)
if sc.shot():
	now_x,now_y =  sc.find_mouse_in_desktop()
	move_x = target_x-now_x+c.mouse_move_shape[0]
	move_y = target_y-now_y+c.mouse_move_shape[1]
	auto.move_rel_click(move_x, move_y)
```
`screen.py`
```
def find_mouse_in_desktop():    
    img = cv.imread(c.img_desktop_path,0)
    img2 = img.copy()
    template = cv.imread(c.mouse_flag_img_path,0)
    w, h = template.shape[::-1]
    
    img = img2.copy()
    shape_list = []
    threshold = 0.85
    res = cv.matchTemplate(img,template,cv.TM_CCOEFF_NORMED)
    loc = np.where( res >= threshold)
    x = 10000
    y = 10000
    for pt in zip(*loc[::-1]):
        top_left = pt
        bottom_right = (top_left[0] + w, top_left[1] + h)  
        shape = (top_left[0],top_left[1],bottom_right[0],bottom_right[1])
        shape_list.append(shape)
        new_x = (shape[2]+shape[0])//2
        if new_x < x :        
            x = new_x
            y = (shape[3]+shape[1])//2

    print(f'中心点坐标为 {(x,y)}')
    return x,y

```

#### 点击

终于，终于，咦？
你们能明白鼠标都移到脸上了，可它就是**点不下去**的**痛苦**吗！
![](http://images.di1shuai.com/Fk0iyfOpffKFnPSU9w1_W3THTBQz)

为什么呢？

简单来说很多游戏使用的并不是`win32`的事件读取输入方式，而是去系统**内核**读取的**驱动**的输入，这样既可以保证**低时延**也可以**屏蔽作弊**

![](http://images.di1shuai.com/Fvk18oJf6uPNnvucvd0KBHgUcOIx)

既然是**内核驱动**读取
![](http://images.di1shuai.com/FoxRGNcSWgzkf0XzEXiZYCGlnR77)

[Windows 硬件开发人员文档](https://docs.microsoft.com/zh-cn/windows-hardware/drivers/)
[编写通用 Hello World 驱动程序 (KMDF)](https://docs.microsoft.com/zh-cn/windows-hardware/drivers/gettingstarted/writing-a-very-small-kmdf--driver)
[系统错误代码大全](https://docs.microsoft.com/zh-cn/windows/win32/debug/system-error-codes)
[预配计算机以便进行驱动程序部署和测试 (WDK 10)](https://docs.microsoft.com/zh-cn/windows-hardware/drivers/gettingstarted/provision-a-target-computer-wdk-8-1)
经过**一系列**学习，**成功**编译~别人~开源的驱动代码 [kmclass](https://github.com/BestBurning/kmclass)
![](http://images.di1shuai.com/Fm5ewStPmrMrni8Jsw3D9M0VFlUj)

![](http://images.di1shuai.com/Fqa104oQYpMc9Va5lHpOghHKmPYD)
`keymouse.py` 即为调用驱动的动态库，在使用前请注意开篇的**环境描述**
```
driver = None

def load_driver():
    global driver
    driver = CDLL(c.kmclass_dll_path)
    driver.LoadNTDriver(c.driver_name,bytes(c.kmclass_driver_path,encoding="utf8"))
    driver.SetHandle()

def _move_rel(x, y):
    driver.MouseMoveRELATIVE(x,y)


if __name__ == '__main__' : 

    load_driver()
    _move_rel(111,44)
```
现在我们用`pyautogui`移动，用`kmclass`点击
`auto.py`
```
def move_rel_click(x,y):
    t('相对移动 点击')
    move_rel(x,y)
    time.sleep(random.random()/20)
    km._left_button_down()
    time.sleep(random.random()/5)
    km._left_button_up()
```
成了！

### 组合

我们把以上步骤组合起来
`main.py`
```
### 自动点击弹框
def auto_click():
    util.log_h1(f'前置准备')
    if sc.dir_check():
        auto.open_driver()
        dm.model_load()
        while(True):
            util.log_h1_start(f'开始')
            start_time = time.time()
            if sc.task():
                min_index = dm.model_predict(c.crop_4_img_paths)
                target_x , target_y = sc.find_xy_indesktop(c.crop_4_img_paths[min_index])
                if target_x == 0 and target_y == 0:
                    util.log_title('匹配失败')
                else:
                    auto.move_to(target_x,target_y)
                    if sc.shot():
                        now_x,now_y =  sc.find_mouse_in_desktop()
                        move_x = target_x-now_x+c.mouse_move_shape[0]
                        move_y = target_y-now_y+c.mouse_move_shape[1]
                        auto.move_rel_click(move_x, move_y)
            end_time = time.time()
            cost_time = end_time - start_time
            util.log_h1_end(f'结束 耗时 %.3f' % cost_time)
            time.sleep(3)

if __name__ == '__main__':
    auto_click()

```
```
=============================================================
====================    开始    =========================



--------   截图    ----------

梦幻西游 ONLINE - (xxxx[xxxx] - xxxx[xxxx])
img_desktop save to -> D:\gitRepo\mhxy\images\desktop.jpg
img_mhxy save to -> D:\gitRepo\mhxy\images\mhxy.jpg

--------   截图检查    ----------

                size=(812, 663)         ok

--------   战斗标识截图    ----------


--------   状态判断    ----------

SSIM: 0.9954736185008931
战斗 状态

--------   弹窗判断    ----------

{(279, 251, 459, 264): (2, 0), (336, 253, 432, 267): (4, 1)}
最大区域 (336, 253, 432, 267) 最终得分为 4
弹框区域  (254, 282, 614, 402)

--------   截图检查    ----------

                size=(360, 120)         ok

--------   弹窗人物切分    ----------



--------   模型预测    ----------

2020-03-21 15:57:49.720468: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cublas64_10.dll
2020-03-21 15:57:50.521308: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cudnn64_7.dll
2020-03-21 15:57:52.768875: W tensorflow/stream_executor/gpu/redzone_allocator.cc:312] Internal: Invoking GPU asm compilation is supported on Cuda non-Windows platforms only
Relying on driver to perform ptx compilation. This message will be only logged once.
[-4.032246, 6.499766, 5.2396355, 33.076145]
 预测结果为 第 > 1 < 张图片

--------   坐标查找    ----------

最高得分区域 (340, 300, 430, 420) 得分为 4
中心点坐标为 (385, 360)
move to - > (385, 360)

--------   截图    ----------

梦幻西游 ONLINE - (xxx[xxx] - xxxxxx[xxxxxxx])
img_desktop save to -> D:\gitRepo\mhxy\images\desktop.jpg
img_mhxy save to -> D:\gitRepo\mhxy\images\mhxy.jpg
中心点坐标为 (389, 380)

--------   相对移动 点击    ----------

move rel - > (12, -5)

================    结束 耗时 6.018    ===================
=============================================================
```

---

### 回顾
到这里，我们的目标已经**基本**完毕
![](http://images.di1shuai.com/Fo8_Kl6JeYnguB5APjcmhkHIZdd_)
为什么说是**基本**呢?

---
### 声明

本人无任何商业目的，仅用于学习和娱乐，[源代码](https://github.com/BestBurning/mhxy)采用了[AGPL3.0](https://opensource.org/licenses/AGPL-3.0)开源协议

本文为博主原创文章，任何人未经过博主同意不得转载