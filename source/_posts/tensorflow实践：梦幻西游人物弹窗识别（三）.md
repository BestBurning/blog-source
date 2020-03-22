---
title: tensorflow实践：梦幻西游人物弹窗识别（三）
tags: 
- tensorflow
- 梦幻西游
- Win10
comments: true
categories: 
- technology
toc: true
keywords: tensorflow,梦幻西游,弹窗识别,python,自动点击,图像识别,卷积神经网络
date: 2020-03-20 15:34:25
---


终于来到了预测的时候了，我们将按以下思路进行
![](http://images.di1shuai.com/FpEUuMIj7eUHPEXYd4RNLpgy0l7Y)

本篇将围绕**训练集准备、模型训练、保存、读取、预测**讲述[data_model.py](https://github.com/BestBurning/mhxy/blob/master/data_model.py)代码

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

[Tensorflow](https://www.tensorflow.org/install)
```
C:\Users\SF>python
Python 3.7.6 (tags/v3.7.6:43364a7ae0, Dec 19 2019, 00:42:30) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import tensorflow as tf
2020-03-19 23:42:50.170828: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cudart64_101.dll
>>> tf.__version__
'2.1.0'
```

[CUDA](https://developer.nvidia.com/cuda-downloads)
```
C:\Users\SF>nvcc --version
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2019 NVIDIA Corporation
Built on Wed_Oct_23_19:32:27_Pacific_Daylight_Time_2019
Cuda compilation tools, release 10.2, V10.2.89

```

[cuDNN](https://developer.nvidia.com/cudnn)
```
C:\tools\cuda\include\cudnn.h

...
#define CUDNN_MAJOR 7

#define CUDNN_MINOR 6
#define CUDNN_PATCHLEVEL 5
#define CUDNN_VERSION (CUDNN_MAJOR * 1000 + CUDNN_MINOR * 100 + CUDNN_PATCHLEVEL)
...
```

[梦幻西游](http://xyq.163.com/download/index.html?=xyqload)
```
启动方式   多标签版
分辨率     800x600
界面风格   暖风

```
![](http://images.di1shuai.com/FkW3mC0_6XGmeMxLdvqkxMGfcORg)
![](http://images.di1shuai.com/FtjEhCyk52bg347Wsn0hAre_GiZL)


### 明确问题
在所有的事情开始之前，我们首先应该**明确**我们要处理一个怎样的**问题**：
**前、后左右**的朝向识别朝**前**的
![](http://images.di1shuai.com/FtyqTsE6LkqznePhEKYi_7nXlYGq)

也就是说只有**两种**分类 ： **前** 和 **其他**
于是我们开始处理一个**二分类**问题：**front**、**others**
所以我们准备构建一个**卷积神经网络**

### 训练集准备

原始图库我用的是[15年的梦幻素材](http://www.6m5m.com/service-sid-6066.html)，然后将他们过滤，背景加色，丢弃A通道，格式由`tga`转换为`jpeg`以后，按照**front**和**others**分类在两个文件夹，于是有了我们的**训练集**
```
images
  |- data
  	  |- train
		   |-front
			   |- xxx.jpg
			   |- ...
		   |-others
			   |- xxx.jpg
			   |- ...
```
![](http://images.di1shuai.com/Flq0Dx7IluKUI3AWy7rKXqb1K0Vq)


验证集是我在日常跑镖中积累的一丢丢图，勉强用作**验证集**
```
images
  |- data
  	  |- validation
		   |-front
			   |- xxx.jpg
			   |- ...
		   |-others
			   |- xxx.jpg
			   |- ...
```
![](http://images.di1shuai.com/FpME3kGg4QQDJr1VH4EVc69wu06V)

以上图集**开源**在[Github](https://github.com/BestBurning/mhxy/releases)上，你可以**直接使用**它来作为你的训练集和测试集

### 模型训练

#### 进行统计

```
def sumNum(dir_path):
    num = 0
    for lb in os.listdir(dir_path):
        for im_name in os.listdir(os.path.join(dir_path,lb)):
            num += 1
    return num

def count():
    t('统计')
    global total_train, total_val, epochs
    total_train = sumNum(c.train_dir)
    total_val = sumNum(c.validation_dir)
    epochs = math.ceil(total_train/batch_size)
    print('训练集标签 :',os.listdir(c.train_dir))
    print('训练集图片个数 :' , total_train)
    print("验证集个数 :", total_val)
    print(f'每批次训练个数: {batch_size}, 共进行 {epochs} 轮训练')
    if total_train == 0:
        print('样本为0 无法训练')
        return False
    return True
```
```
--------   统计    ----------

训练集标签 : ['front', 'others']
训练集图片个数 : 5570
验证集个数 : 128
每批次训练个数: 128, 共要进行 44 轮训练
```

#### 构建数据生成器
```
def data_generator():
    t('数据生成器')
    global train_data_gen,val_data_gen

    train_image_generator = ImageDataGenerator(rescale=1./255) # Generator for our training data
    validation_image_generator = ImageDataGenerator(rescale=1./255) # Generator for our validation data

    train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                           directory=c.train_dir,
                                                           shuffle=True,
                                                           target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                           class_mode='binary')
    val_data_gen = validation_image_generator.flow_from_directory(batch_size=batch_size,
                                                              directory=c.validation_dir,
                                                              target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                              class_mode='binary')
```
```
--------   数据生成器    ----------

Found 5570 images belonging to 2 classes.
Found 128 images belonging to 2 classes.
```
#### 模型编译统计
```
def model_summary():
    t('模型编译统计')
    global model 
    model = Sequential([
        Conv2D(16, (3,3), padding='same', activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH ,3)),
        MaxPooling2D((2, 2)),
        Conv2D(32, (3,3), padding='same', activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3,3), padding='same', activation='relu'),
        MaxPooling2D(),
        Flatten(),
        Dense(64, activation='relu'),
        Dense(1)
    ])
    model.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])
    model.summary()
```
```
--------   模型编译统计    ----------

2020-03-20 18:40:39.575508: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library nvcuda.dll
2020-03-20 18:40:39.647045: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1555] Found device 0 with properties: 
pciBusID: 0000:03:00.0 name: GeForce GTX 1060 5GB computeCapability: 6.1
coreClock: 1.7335GHz coreCount: 10 deviceMemorySize: 5.00GiB deviceMemoryBandwidth: 149.16GiB/s
2020-03-20 18:40:39.648857: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cudart64_101.dll
2020-03-20 18:40:39.710717: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cublas64_10.dll
2020-03-20 18:40:39.770435: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cufft64_10.dll
2020-03-20 18:40:39.786318: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library curand64_10.dll
2020-03-20 18:40:39.840028: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cusolver64_10.dll
2020-03-20 18:40:39.871203: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cusparse64_10.dll
2020-03-20 18:40:39.980945: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cudnn64_7.dll
2020-03-20 18:40:39.983037: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1697] Adding visible gpu devices: 0
2020-03-20 18:40:39.989541: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1555] Found device 0 with properties: 
pciBusID: 0000:03:00.0 name: GeForce GTX 1060 5GB computeCapability: 6.1
coreClock: 1.7335GHz coreCount: 10 deviceMemorySize: 5.00GiB deviceMemoryBandwidth: 149.16GiB/s
2020-03-20 18:40:39.990720: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cudart64_101.dll
2020-03-20 18:40:39.991293: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cublas64_10.dll
2020-03-20 18:40:39.991914: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cufft64_10.dll
2020-03-20 18:40:39.992447: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library curand64_10.dll
2020-03-20 18:40:39.993014: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cusolver64_10.dll
2020-03-20 18:40:39.993495: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cusparse64_10.dll
2020-03-20 18:40:39.994060: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cudnn64_7.dll
2020-03-20 18:40:39.996657: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1697] Adding visible gpu devices: 0
2020-03-20 18:40:42.996316: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1096] Device interconnect StreamExecutor with strength 1 edge matrix:
2020-03-20 18:40:42.996882: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1102]      0 
2020-03-20 18:40:42.997242: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1115] 0:   N 
2020-03-20 18:40:43.003355: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1241] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 3833 MB memory) -> physical GPU (device: 0, name: GeForce GTX 1060 5GB, pci bus id: 0000:03:00.0, compute capability: 6.1)
Model: "sequential"
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
conv2d (Conv2D)              (None, 100, 100, 16)      448       
_________________________________________________________________
max_pooling2d (MaxPooling2D) (None, 50, 50, 16)        0         
_________________________________________________________________
conv2d_1 (Conv2D)            (None, 50, 50, 32)        4640      
_________________________________________________________________
max_pooling2d_1 (MaxPooling2 (None, 25, 25, 32)        0         
_________________________________________________________________
conv2d_2 (Conv2D)            (None, 25, 25, 64)        18496     
_________________________________________________________________
max_pooling2d_2 (MaxPooling2 (None, 12, 12, 64)        0         
_________________________________________________________________
flatten (Flatten)            (None, 9216)              0         
_________________________________________________________________
dense (Dense)                (None, 64)                589888    
_________________________________________________________________
dense_1 (Dense)              (None, 1)                 65        
=================================================================
Total params: 613,537
Trainable params: 613,537
Non-trainable params: 0
_________________________________________________________________
```
#### 开始训练
```

def model_fit():
    t('开始训练')

    global model,epochs,train_data_gen,total_train,batch_size,val_data_gen,total_val

    history = model.fit_generator(
        train_data_gen,
        steps_per_epoch=total_train // batch_size,
        epochs=epochs,
        validation_data=val_data_gen,
        validation_steps=total_val // batch_size
    )
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']

    loss=history.history['loss']
    val_loss=history.history['val_loss']

    epochs_range = range(epochs)

    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.show()

```

#### 模型保存

```
def model_save():
    t('模型保存')
    global model
    model.save(c.model_path)
    print(f'model save -> {c.model_path}') 
```
```
--------   模型保存    ----------
model save -> D:\gitRepo\mhxy\model\mhxy.h5
```

#### 运行结果

将以上过程组装后运行
```
def base():
    if count():
        data_generator()
        model_summary()
        model_fit()
	model_save()
        return True

if __name__ == '__main__':
    base()
    t('结束')
```

于是我们在`model`目录下生成了`mhxy.h5`模型文件
```
model
  |- mhxy.h5
```
### 模型读取
```
def model_load():
    t('模型读取')
    print(c.model_path)
    global model
    model = keras.models.load_model(c.model_path)
    model.summary()
```
```
--------   模型读取    ----------

model\mhxy.h5
2020-03-20 21:57:38.730370: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library nvcuda.dll
2020-03-20 21:57:38.794436: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1555] Found device 0 with properties: 
pciBusID: 0000:03:00.0 name: GeForce GTX 1060 5GB computeCapability: 6.1
coreClock: 1.7335GHz coreCount: 10 deviceMemorySize: 5.00GiB deviceMemoryBandwidth: 149.16GiB/s
2020-03-20 21:57:38.796527: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cudart64_101.dll
2020-03-20 21:57:38.821242: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cublas64_10.dll
2020-03-20 21:57:38.836458: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cufft64_10.dll
2020-03-20 21:57:38.843690: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library curand64_10.dll
2020-03-20 21:57:38.857073: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cusolver64_10.dll
2020-03-20 21:57:38.864317: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cusparse64_10.dll
2020-03-20 21:57:38.879320: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cudnn64_7.dll
2020-03-20 21:57:38.881830: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1697] Adding visible gpu devices: 0
2020-03-20 21:57:38.886175: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1555] Found device 0 with properties: 
pciBusID: 0000:03:00.0 name: GeForce GTX 1060 5GB computeCapability: 6.1
coreClock: 1.7335GHz coreCount: 10 deviceMemorySize: 5.00GiB deviceMemoryBandwidth: 149.16GiB/s
2020-03-20 21:57:38.887320: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cudart64_101.dll
2020-03-20 21:57:38.887871: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cublas64_10.dll
2020-03-20 21:57:38.888409: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cufft64_10.dll
2020-03-20 21:57:38.888968: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library curand64_10.dll
2020-03-20 21:57:38.889514: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cusolver64_10.dll
2020-03-20 21:57:38.890090: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cusparse64_10.dll
2020-03-20 21:57:38.890651: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cudnn64_7.dll
2020-03-20 21:57:38.892737: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1697] Adding visible gpu devices: 0
2020-03-20 21:57:39.833100: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1096] Device interconnect StreamExecutor with strength 1 edge matrix:
2020-03-20 21:57:39.833639: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1102]      0 
2020-03-20 21:57:39.834024: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1115] 0:   N 
2020-03-20 21:57:39.835939: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1241] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 3833 MB memory) -> physical GPU (device: 0, name: GeForce GTX 1060 5GB, pci bus id: 0000:03:00.0, compute capability: 6.1)
Model: "sequential"
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
conv2d (Conv2D)              (None, 100, 100, 16)      448       
_________________________________________________________________
max_pooling2d (MaxPooling2D) (None, 50, 50, 16)        0         
_________________________________________________________________
conv2d_1 (Conv2D)            (None, 50, 50, 32)        4640      
_________________________________________________________________
max_pooling2d_1 (MaxPooling2 (None, 25, 25, 32)        0         
_________________________________________________________________
conv2d_2 (Conv2D)            (None, 25, 25, 64)        18496     
_________________________________________________________________
max_pooling2d_2 (MaxPooling2 (None, 12, 12, 64)        0         
_________________________________________________________________
flatten (Flatten)            (None, 9216)              0         
_________________________________________________________________
dense (Dense)                (None, 64)                589888    
_________________________________________________________________
dense_1 (Dense)              (None, 1)                 65        
=================================================================
Total params: 613,537
Trainable params: 613,537
Non-trainable params: 0
_________________________________________________________________

```
### 进行预测
```
def model_predict(paths):
    t('模型预测')
    global model
    imgs = [load_and_preprocess_image(path) for path in paths]
    imgs =  tf.convert_to_tensor(imgs)
    predictions = model.predict(imgs)
    predictions = [row[0] for row in predictions]
    min_index = predictions.index(min(predictions))
    print(f' 预测结果为 第 > {min_index + 1} < 张图片')
    return min_index

def preprocess_image(image):
  image = tf.image.decode_jpeg(image, channels=3)
  image = tf.image.resize(image, [IMG_WIDTH, IMG_HEIGHT])
  image /= 255.0  # normalize to [0,1] range
  return image

def load_and_preprocess_image(path):
  image = tf.io.read_file(path)
  return preprocess_image(image)
```
`model.predict(imgs)`预测了一组照片，返回值为一组照片的**可能行**数组，值越**小(负)**越倾向于**front**，值越**大(正)**越倾向于**others**

于是我们**读取模型**并**预测**[上一篇文章](https://di1shuai.com/tensorflow%E5%AE%9E%E8%B7%B5%EF%BC%9A%E6%A2%A6%E5%B9%BB%E8%A5%BF%E6%B8%B8%E4%BA%BA%E7%89%A9%E5%BC%B9%E7%AA%97%E8%AF%86%E5%88%AB%EF%BC%88%E4%BA%8C%EF%BC%89.html)已经切出来的一组照片
```
model_load()
model_predict(c.crop_4_img_paths)
```
![](http://images.di1shuai.com/FtNE-uhRJniapeoZu-L5DTnVY-KH)
![](http://images.di1shuai.com/Fu4P4PpvjEdWYxPwiBl0bzL-Yw-u)
![](http://images.di1shuai.com/FoRMjFWNw0ixNK6tYIwKADSQi-UX)
![](http://images.di1shuai.com/FsGV0OkNfQuog-NtJx33JRAC-IlA)
```
--------   模型预测    ----------

2020-03-20 22:32:18.551882: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cublas64_10.dll
2020-03-20 22:32:18.915562: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cudnn64_7.dll
2020-03-20 22:32:20.185335: W tensorflow/stream_executor/gpu/redzone_allocator.cc:312] Internal: Invoking GPU asm compilation is supported on Cuda non-Windows platforms only
Relying on driver to perform ptx compilation. This message will be only logged once.
[11.985916, 10.617589, 1.425591, -2.6980643]
 预测结果为 第 > 4 < 张图片<

--------   结束    ----------

```

![](http://images.di1shuai.com/FhafeoF-EUhcVGl_l_lxRrzNHytm)

---

### 回顾

到这里，我们关于**预测**部分的内容就已经完毕，回头看看我们走过的路
![](http://images.di1shuai.com/FkislI5cz5t4U_-ezCJsHh4rTuKy)
是不是胜利在望！

---
### 声明

本人无任何商业目的，仅用于学习和娱乐，[源代码](https://github.com/BestBurning/mhxy)采用了[AGPL3.0](https://opensource.org/licenses/AGPL-3.0)开源协议

本文为博主原创文章，任何人未经过博主同意不得转载