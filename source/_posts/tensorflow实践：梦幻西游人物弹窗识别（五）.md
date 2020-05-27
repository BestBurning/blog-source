---
title: tensorflow实践：梦幻西游人物弹窗识别（五）
tags: 
- tensorflow
- 梦幻西游
- Windows
comments: true
categories: 
- technology
toc: true
keywords: tensorflow,梦幻西游,弹窗识别,python,自动点击,图像识别,持续学习
copyright: false
date: 2020-03-21 17:53:50
---


为什么么说我们的目标是**基本**完成呢？
因为它不会**进化**呀！


![](http://images.di1shuai.com/FltgSUT4XbTNajlHvvq4FRgtNHad)

如果我们拥有**全量**的梦幻西游人物**图库**，那自然预测的准确率很高
很可惜，我们**没有**
所以只能在日常的跑镖或者打怪中去不断的**积累**图库，让神经网络不断的训练**学习**，以将**准确率**提**高**

### 预分类
于是我们按照预测的索引，将图片**分类**并保存，值得注意的是这里的分类并**不**一定**准确**，所以是**预分类**

`screen.py`
```
###  数据保存
def save_data_img(front_index):
    for i in range(len(c.crop_4_img_paths)):
        save_path = ''
        if i == front_index:
            save_path = os.path.join(c.new_front_img_dir,time_str()+'_'+str(i)+'.jpg')
        else:
            save_path = os.path.join(c.new_others_img_dir,time_str()+'_'+str(i)+'.jpg')
        shutil.copyfile(c.crop_4_img_paths[i],save_path)
```
`main.py`在获得预测索引时保存数据
```
min_index = dm.model_predict(c.crop_4_img_paths)
sc.save_data_img(min_index)
target_x , target_y = sc.find_xy_indesktop(c.crop_4_img_paths[min_index])
```
路径如下
```
images
  |- data
      |- new
          |- front
               |- xxx.jpg
               |- ...
          |- others  
               |- xxx.jpg
               |- ... 
```

### 分类
不得不说这一步是**手工**确认，去两个文件夹下确认是否都是正确的，不正确的手工移动到正确目录下
于是加入两个**输入确认**以**提醒**不要忘记，等训练**样本**比较**齐全**以后可以改为**自动**分类
```

util.log_title('图片朝向确认')
confirm = input(f'请确认路径  {os.path.abspath(c.new_front_img_dir)}   下图片朝向均为  > 前 <  : (确认后输入 Y , 输入其他退出) ')
if confirm == 'Y' or confirm == 'y':
    confirm = input(f'请确认路径  {os.path.abspath(c.new_others_img_dir)}   下图片朝向均为  > 左 右 后 < : (确认后输入 Y , 输入其他退出)')
    if confirm == 'Y' or confirm == 'y':
```
```
2020-03-21 19:12:12.623765: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cudart64_101.dll

--------   图片朝向确认    ----------

请确认路径  D:\gitRepo\mhxy\images\data\new\front   下图片朝向均为  > 前 <  : (确认后输入 Y , 输入其他退出) Y
请确认路径  D:\gitRepo\mhxy\images\data\new\others   下图片朝向均为  > 左 右 后 < : (确认后输入 Y , 输入其他退出)
```

### 移动
分类确认后，就可以将`new`目录下图片移动到训练集`train`目录中了
`main.py`
```
sc.move_new_to_train()
```

`screen.py`
```
def move_new_to_train():
    move_file(c.new_front_img_dir,c.front_img_dir)
    move_file(c.new_others_img_dir,c.others_img_dir)

def move_file(src_path,target_path):
    file_list=os.listdir(src_path)
    if len(file_list)>0:
        for file in file_list:
            shutil.move(
                os.path.join(src_path,file),
                os.path.join(target_path,file)
                )   
    print(f'{src_path} -> {target_path} 完毕')
```

### 训练

`main.py`
```
dm.base()
```
`data_model.py`
```
def base():
    if count():
        data_generator()
        model_summary()
        model_fit()
        model_save()
        return True
```

### 组合
将之前的步骤组合后
`main.py`
```
###  将新图加入训练集 并 训练模型
def move_learn():
    util.log_title('图片朝向确认')
    confirm = input(f'请确认路径  {os.path.abspath(c.new_front_img_dir)}   下图片朝向均为  > 前 <  : (确认后输入 Y , 输入其他退出) ')
    if confirm == 'Y' or confirm == 'y':
        confirm = input(f'请确认路径  {os.path.abspath(c.new_others_img_dir)}   下图片朝向均为  > 左 右 后 < : (确认后输入 Y , 输入其他退出)')
        if confirm == 'Y' or confirm == 'y':
            util.log_h1_start('开始')
            sc.move_new_to_train()
            dm.base()               
    util.log_h1_end('结束')
```

![](http://images.di1shuai.com/FncBRUv0JAJOZVvE2Bpbk79arRRU)

这样的话，每天打完以后，都可以用新的素材让自己变帅一点，哈哈哈哈哈哈

---

### 回顾

再来看看我们都经历了什么
![](http://images.di1shuai.com/FuOdQlJmiTzQMbbtZ4vXOraJL6Fp)
成就感满满!!

---

### 声明

本人无任何商业目的，仅用于学习和娱乐，[源代码](https://github.com/BestBurning/mhxy)采用了[AGPL3.0](https://opensource.org/licenses/AGPL-3.0)开源协议

本文为博主原创文章，任何人未经过博主同意不得转载