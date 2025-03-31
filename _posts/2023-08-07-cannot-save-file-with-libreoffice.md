---
layout: post
title: libreoffice不能保存
date: 2023-08-07 16-15-00 16:15:00+0800
description: 
tags: 
giscus_comments: true
categories: icenv
---

使用`env LD_LIBRARY_PATH= /tools/opensrc/LibreOffice/7.3.0/opt/libreoffice7.3/program/soffice -env:UserInstallation=file:///tmp/wanlinwang/libreoffice7.3`无法保存文件，报错如下，

<img width="219" alt="企业微信截图_16913800075669" src="https://github.com/icinfra/icinfra.github.io/assets/32032219/8bb7e8c5-f6d1-4275-89a1-5d7ba9773a5f">


重启了TurboVNC就好了。但根因未找到。
