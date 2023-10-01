---
layout: post
title: 从Grafana获取panel图片
date: 2023-05-06 09-23-19 09:23:19+0800
description: 
tags: report
giscus_comments: true
categories: icenv
---


# 前言
日常工作，有这样的需求：以指定的时间区间以及变量，获得Grafana panel图，并将多张图以邮件的方式发送到领导。

# 步骤

1. 先创建API key
![](/assets/img/Pasted%20image%2020230506092820.png)

2. 获得Panel的图片链接
打开Dashboard，在需要生成图片的Panel上，点击下拉->Share，
![](/assets/img/Pasted%20image%2020230506093819.png)

![](/assets/img/Pasted%20image%2020230506100824.png)

如果未安装Grafana image render plugin，则点击并按照提示安装，安装完毕后如下图所示，
![](/assets/img/Pasted%20image%2020230506100911.png)

复制“Direct link rendered image”链接。

3. 在Python里，请求步骤2获得的链接，将response.content以二进制保存到文件里，该文件即是图片文件。此外，如果需要对图片进行**部分遮盖**、**写文字**，可以使用pillow模块。