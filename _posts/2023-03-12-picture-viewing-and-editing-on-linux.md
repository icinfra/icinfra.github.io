---
layout: post
title: 在Linux下编辑图
date: 2023-03-12 18:38:18+0800
description: 在Linux下编辑图
tags: linux
giscus_comments: true
categories: icenv
---

# 需求
在Linux研发桌面下画图。
本文介绍两个常用的画图工具，第一个是满足与Windows下”画图“工具的简单需求；第二个则是满足流程图的功能需求，类似于visio。

# 方案

## gimp
它是GNU图片操作程序，信息如下所示
![[/assets/img/Pasted image 20230312203126.png]]

安装
```bash
bash-4.2# yum install -y gimp
```

运行
![[/assets/img/Pasted image 20230312204301.png]]

## draw.io
简介
它是一款免费的支持多平台的流程图工具，许可证为Apache 2.0。

下载
![[/assets/img/Pasted image 20230312205248.png]]

运行
赋予执行权限，如是root账户则加上--no-sandbox选项
![[/assets/img/Pasted image 20230312205809.png]]

