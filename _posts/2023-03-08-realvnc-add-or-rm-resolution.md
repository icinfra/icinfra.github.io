---
layout: post
title:  REALVNC如何增加或删除分辨率配置？
date:   2023-03-08 12:50:00+0800
description: REALVNC增加或删除分辨率配置
tags: linux vnc
giscus_comments: true
categories: icenv-posts
---

# 问题
用户设置1920x1080的分辨率，屏幕崩溃，画面乱了。

# 解决
去掉有问题的配置。

查看到两个1920x1080的配置<br/>
![xrandr -q结果](/assets/img/realvnc分辨率Snipaste_2023-03-08_13-08-11.png)

使用xrandr删掉有问题的这个<br/>
![xrandr --delmode](/assets/img/xrandr删除分辨率失败Snipaste_2023-03-08_13-14-04.png)

报错。经[google](https://bugs.freedesktop.org/show_bug.cgi?id=10369#c2)，说的是xrandr无法删除由X managed的mode。

从X[REALVNC手册]侧删除。(https://help.realvnc.com/hc/en-us/articles/360016058212-How-do-I-adjust-the-screen-resolution-of-a-virtual-desktop-under-Linux-#realvnc-dummy-driver-0-3)里，说/etc/X11/vncserver-virtual-dummy.conf，如果是较早的版本则是/etc/X11/vncserver-virtual.conf文件。将有问题的配置，从这个文件里移除，可将冲突的那个1920x1080删除，问题解决。

