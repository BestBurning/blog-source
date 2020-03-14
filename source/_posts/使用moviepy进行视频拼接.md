---
title: 使用moviepy进行视频拼接
tags: moviepy
comments: true
categories: technology
toc: false
keywords: moviepy,视频,拼接,python
date: 2020-03-14 17:36:51
---


起因是有很多爱奇艺转换后的视频需要拼成一个，**手工**去Mac上拼接也太**手工**了，
就写了个python脚本把具有下面结构的多个视频拼接在一起
```
videos
   | merge1
       | video1.mp4    
       | video2.mp4
	| video3.mp4
   | merge2
       | video1.mp4
       | video2.mp4
=======================
videos
   | merge1.mp4
   | merge2.mp4
	
```
主要是使用了基于`ffmpeg`的`moviepy`库
完整代码如下,需要注意的是如果使用的素材不是统一分辨率，分辨率小的会居中显示

```
from moviepy.editor import *
from natsort import natsorted
import io
import sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import os

path = 'D:\\Download\\qichche'
# qichche
#   | merge1
#       | video1.mp4    
#       | video2.mp4
#       | video3.mp4
#   | merge2
#       | video1.mp4
#       | video2.mp4
#=======================
# qichche
#   | merge1.mp4
#   | merge2.mp4
# 访问 qichche 文件夹 (假设视频都放在这里面)
for name in os.listdir(path):
    L = []

    for root, dirs, files in os.walk(path+'\\'+name):
        # 按文件名排序
        files = natsorted(files)
        # 遍历所有文件
        for file in files:
            # 如果后缀名为 .mp4
            if str(file).endswith('.mp4'):
                # 拼接成完整路径
                filePath = path+'\\'+name+'\\'+ str(file)
                # 载入视频
                print(filePath)
                video = VideoFileClip(filePath)
                print("video time: %s, width: %s, height: %s, fps: %s" % (video.duration, video.w, video.h, video.fps))
                # 添加到数组
                L.append(video)

    # #拼接视频
    final_clip = concatenate_videoclips(L,method='compose')
    # #生成目标视频文件
    #final_clip.to_videofile(path+'\\'+name+'.mp4', fps=24, remove_temp=False)
    final_clip.write_videofile(path+'\\'+name+'.mp4')
```

代码也同时贴在了[Github](https://github.com/BestBurning/video-concatenate)上