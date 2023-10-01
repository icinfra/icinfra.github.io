---
layout: post
title: Python pillow修图
date: 2023-05-07 10-47-38 10:47:38+0800
description: 
tags: python
giscus_comments: true
categories: icenv
---


# 背景
以指定参数去调用Grafana可视化界面API生成图片。但API未提供修改图片（如title或其它区域）的功能，直接作为报告发送可能传达的信息不够清晰。

# 步骤
## 获取图片
按照[本文](https://www.icinfra.cn/blog/2023/rendering-image-from-grafana-panel/)的步骤获取图片（数值已马赛克）：

![](/assets/img/Pasted%20image%2020230507110045.png)

## 修图需求
1. 将title修改掉；
2. total Mean去掉，不重要。

## 编码
先安装好pillow模块

`pip3 install pillow`

然后码
```python
#!/usr/bin/env python3

# wanlinwang
# 07-May-2023
# 处理500x250的图片，修改标题，再抹掉部分信息。


from PIL import Image, ImageFont, ImageDraw


filename="/Users/wanlinwang/image_processing/过去30天的License使用报告_20230407000000_to_20230507000000_raw.png"
filename_dst="/Users/wanlinwang/image_processing/过去30天的License使用报告_20230407000000_to_20230507000000_dest.png"

im = Image.open(filename)
W, H = im.size

title_font = ImageFont.truetype('/Users/wanlinwang/image_processing/fonts/NotoSerifSC-Black.otf', 25)
image_editable = ImageDraw.Draw(im)
title_text="过去30天的License使用报告"

# (x0, y0, x1, y1), 填充黑色，抹掉原title
image_editable.rectangle((0, 0, W, 36), fill="black")
# 加上新title
image_editable.text((W/2, 0), title_text, (237, 230, 211), anchor='ma', font=title_font)
# (x0, y0, x1, y1), 填充黑色，抹掉total Mean
image_editable.rectangle((135, 222, W,  H), fill="black")

# 保存图片文件
im.save(filename_dst)
```

# 效果
![](/assets/img/Pasted%20image%2020230507110141.png)

# 参考资料
1. ImageDraw.text()锚点参数说明：https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html#PIL.ImageDraw.ImageDraw.text
2. 获取图片像素点，在Windows上可以使用**画图**打开图片，将鼠标停留在图片任意像素点，即可在左下方显示像素点的坐标位置。在MacOS暂未找到方法，欢迎留言。
