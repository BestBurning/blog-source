---
title: tensorflow实践：梦幻西游人物弹窗识别（二）
tags: 
- tensorflow
- 梦幻西游
comments: true
categories: 
- technology
toc: true
keywords: tensorflow,梦幻西游,弹窗识别,python,自动点击
date: 2020-03-19 17:22:59
---

由上一篇的思路我们可以定义以下的具体实现步骤
![](http://images.di1shuai.com/FkMKDBPbKXGq3ubgfeTzt2Vtcp-N)

本篇将围绕**窗口捕获、屏幕截图、截图切分**讲述[screen.py](https://github.com/BestBurning/mhxy/blob/master/screen.py)代码

### 环境描述
[Windows](https://www.microsoft.com/zh-cn/software-download/windows10)

```
C:\Users\SF>ver
Microsoft Windows [版本 10.0.18363.720]
```

[Python](https://www.python.org/downloads/)
```
C:\Users\SF>python --version
Python 3.7.6
```

[梦幻西游](http://xyq.163.com/download/index.html?=xyqload)
```
启动方式   多标签版
分辨率     800x600
界面风格   暖风

```
![](http://images.di1shuai.com/FkW3mC0_6XGmeMxLdvqkxMGfcORg)
![](http://images.di1shuai.com/FtjEhCyk52bg347Wsn0hAre_GiZL)

### 窗口截图

主要是使用了`PyQt5`进行截图

```
hwnd_title = dict()

def get_all_hwnd(hwnd,mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd:win32gui.GetWindowText(hwnd)})

def shot():
    win32gui.EnumWindows(get_all_hwnd, 0)
    mhxy_title = ''
    for h,t in hwnd_title.items():
        if t.startswith('梦幻西游 ONLINE'):
            mhxy_title = t
            print(mhxy_title)
            hwnd = win32gui.FindWindow(None, mhxy_title)
            app = QApplication(sys.argv)
            desktop_id = app.desktop().winId()
            screen = QApplication.primaryScreen()
            img_desk = screen.grabWindow(desktop_id).toImage()
            img_sc = screen.grabWindow(hwnd).toImage()
            img_desk.save(img_desktop_path)
            img_sc.save(img_sc_path)
            print(f'img_desktop save to -> {os.path.abspath(img_desktop_path)}')
            print(f'img_mhxy save to -> {os.path.abspath(img_sc_path)}')
    if mhxy_title == '':
        print('mhxy not start')
        return False
    return True
```
于是我们在路径
```
images
  |- desktop.jpg
  |- mhxy.jpg
```
得了一张**全屏**截图以及一张梦幻的**窗口**截图

### 截图切分

得到屏幕截图后，我们将对截图进行切分
![](http://images.di1shuai.com/FuRjXMN4Cgpm9rGJe-patSpt18d6)

#### 战斗状态判断
因为进入**战斗**才会弹窗，所以首先对战斗状态进行判断
战斗状态的判断是依据了梦幻窗口最右侧**战斗标识**，不同的界面风格标识的颜色是**不同**的，我用的是**暖风**界面风格
![](http://images.di1shuai.com/Fg8Btk_CGNzOxFuoZ25BCgI4Nrbg)
![](http://images.di1shuai.com/FpwXJGD-ZAVQWmpJQCXpC55eU8t6)
战斗标识路径
```
images
  |- flag
      |- fighting_flag.jpg
```

截取相同区域的图片使用`opencv`与战斗标识进行**相似性判断**，如果相似度大于`%95`则判定为**战斗状态**
```
# 战斗截图
def fight_crop():
    util.log_title('战斗标识截图')
    return crop(c.img_sc_path,c.fighting_img_path,c.fight_shape)


# 是否在战斗
def is_fight():
    util.log_title('状态判断')
    rate = compare_image(c.fighting_flag_img_path,c.fighting_img_path)
    if rate > 0.95:
        print('战斗 状态')
        return True
    else:
        print('非战斗 状态')
        return False

# 相似性判断
def compare_image(path_image1, path_image2):

    imageA = cv.imread(path_image1)
    imageB = cv.imread(path_image2)
    grayA = cv.cvtColor(imageA, cv.COLOR_BGR2GRAY)
    grayB = cv.cvtColor(imageB, cv.COLOR_BGR2GRAY)

    (score, diff) = structural_similarity(grayA, grayB, full=True)
    print("SSIM: {}".format(score))
    return score

# 裁剪
def crop(source_path,target_path,shape):
    with Image.open(source_path) as img:

        fighting_flag_img = img.crop(shape)
        fighting_flag_img.save(target_path)
        return True    
```
截取战斗标识相同区域的路径为
```
images
  |- sub
      |- fighting.jpg
```


#### 判断是否弹窗

接下来我们开始判断是否**弹窗**，目前见到的弹窗形式有**两种**,可以使用如下两种弹窗标识去匹配梦幻窗口
![](http://images.di1shuai.com/FsDnEA61Ur_uV62uxbL4gQYtpeBs)
![](http://images.di1shuai.com/FoD8Po6Zuh31WkOSZ9_QEl-52S8P)

所以弹窗判断的思路如下
![](http://images.di1shuai.com/Fh4cAxJOIYd09wqsTIWPV9-q4MKv)


使用 [OpenCV Template Matching](https://docs.opencv.org/4.2.0/d4/dc6/tutorial_py_template_matching.html) 对梦幻窗口进行匹配，并返回**最匹配**(**得分最高**)的区域
```
def popup_sub_crop():
    util.log_title('弹窗判断')
    shape_dict = {} 
    for i in range(len(c.popup_flag_img_paths)):
        shape,score = template_match(c.popup_flag_img_paths[i],c.img_sc_path)
        shape_dict[shape] = (score,i)
    
    print(shape_dict)
    max_shape = max(shape_dict, key=shape_dict.get)
    score,i = shape_dict[max_shape]
    print(f'最大区域 {max_shape} 最终得分为 {score}' )
    if score >=3 :
        sub_shape = (
            max_shape[0]+c.popup_move_shapes[i][0],
            max_shape[1]+c.popup_move_shapes[i][1],
            max_shape[2]+c.popup_move_shapes[i][2],
            max_shape[3]+c.popup_move_shapes[i][3]
        )
        print(f'弹框区域  {sub_shape}')
        return crop(c.img_sc_path,c.popup_sub_img_path,sub_shape)
    print(f'没有弹框')
    return False


def template_match(template_path,src_path):

    
    img = cv.imread(src_path,0)
    img2 = img.copy()
    template = cv.imread(template_path,0)
    w, h = template.shape[::-1]
    methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED','cv.TM_CCORR',
                'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
    shape_dict = {}
    for meth in methods:
        img = img2.copy()
        method = eval(meth)
        # Apply template Matching
        res = cv.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)  
        # cv.rectangle(img,top_left, bottom_right, 255, 2)
        # plt.subplot(121),plt.imshow(res,cmap = 'gray')
        # plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        # plt.subplot(122),plt.imshow(img,cmap = 'gray')
        # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        # plt.suptitle(meth)
        # plt.show()
        shape = (top_left[0],top_left[1],bottom_right[0],bottom_right[1])
        # print(shape)
        if shape_dict.get(shape) == None:
            shape_dict[shape] = 1;
        else:
            shape_dict[shape] = shape_dict[shape]+1        
        max_shape = max(shape_dict, key=shape_dict.get)
    return max_shape,shape_dict[max_shape]

```




#### 切出包含4个人物的大图
这个包含四个人物的图片宽高为`360 x 120`
![](http://images.di1shuai.com/FvmxSuj1rzrJwWLb5v2ZMK5yqqYg)


```
def popup_sub_crop():
    util.log_title('弹窗判断')
    shape_dict = {} 
    for i in range(len(c.popup_flag_img_paths)):
        shape,score = template_match(c.popup_flag_img_paths[i],c.img_sc_path)
        shape_dict[shape] = (score,i)
    
    print(shape_dict)
    max_shape = max(shape_dict, key=shape_dict.get)
    score,i = shape_dict[max_shape]
    print(f'最大区域 {max_shape} 最终得分为 {score}' )
    if score >=3 :
        sub_shape = (
            max_shape[0]+c.popup_move_shapes[i][0],
            max_shape[1]+c.popup_move_shapes[i][1],
            max_shape[2]+c.popup_move_shapes[i][2],
            max_shape[3]+c.popup_move_shapes[i][3]
        )
        print(f'弹框区域  {sub_shape}')
        return crop(c.img_sc_path,c.popup_sub_img_path,sub_shape)
    print(f'没有弹框')
    return False
```
路径如下
```
images
  |- sub
      |- pop_sub.jpg  
```

#### 再切出单个人物
单个人物宽高为`90 x 120`
![](http://images.di1shuai.com/FtNE-uhRJniapeoZu-L5DTnVY-KH)

```
def crop_4():
    util.log_title('弹窗人物切分')
    w = 90
    h = 120
    for i in range(len(c.crop_4_img_names)):
        shape = (w*i, 0, w*(i+1), h)
        crop(c.popup_sub_img_path,c.crop_4_img_paths[i],shape)
```
路径如下
```
images
  |- sub
      |- 1.jpg
      |- 2.jpg  
      |- 3.jpg
      |- 4.jpg
```

#### 组合

于是我们将以上步骤组合起来
```
def task():

    print()
    if shot():                                                          ## 截图
        if image_check(c.img_sc_path,c.screen_size):                    ## 检查截图大小
            fight_crop()                                                ## 战斗标识截图
            if is_fight():                                              ## 判断是否在战斗
                if popup_sub_crop():                                    ## 弹窗识别 与 人物区域切出
                    if image_check(c.popup_sub_img_path,c.sub_size):    ## 弹窗人物截图检查
                        crop_4()                                        ## 弹窗人物切分                   
                        print()
                        return True
    return False


if __name__ == '__main__':
    task()

```
```
--------   截图    ----------

梦幻西游 ONLINE - (xxxxxxx - xxxxx[xxxxx])
img_desktop save to -> d:\gitRepo\mhxy\images\desktop.jpg
img_mhxy save to -> d:\gitRepo\mhxy\images\mhxy.jpg

--------   截图检查    ----------

        size=(812, 663)     ok

--------   战斗标识截图    ----------


--------   状态判断    ----------

SSIM: 0.9955642623257255
战斗 状态

--------   弹窗判断    ----------

{(277, 221, 457, 234): (1, 0), (334, 223, 430, 237): (4, 1)}
最大区域 (334, 223, 430, 237) 最终得分为 4
弹框区域  (252, 252, 612, 372)

--------   截图检查    ----------

        size=(360, 120)     ok

--------   弹窗人物切分    ----------


```
---
到这里，**窗口捕获、屏幕截图、截图切分**部分就已经完毕，我们再来看一下进度
![](http://images.di1shuai.com/FtKWasG4kAAin4mpYZvkkLu8Ohsl)
是不是胜利指日可待！

---
### 声明

本人无任何商业目的，仅用于学习和娱乐，[源代码](https://github.com/BestBurning/mhxy)采用了[AGPL3.0](https://opensource.org/licenses/AGPL-3.0)开源协议

本文为博主原创文章，任何人未经过博主同意不得转载