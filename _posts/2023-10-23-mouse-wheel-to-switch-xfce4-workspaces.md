---
layout: post
title: 鼠标滚轮切换xfce4 workspace
date: 2023-10-23 12:34+0800
description: 
tags: xfce4
giscus_comments: true
categories: icenv
---

在xfce4桌面，鼠标滚轮禁止切换workspace：

## 命令行设置
```bash
$ xfconf-query -c xfwm4 -l | grep workspace
/general/cycle_workspaces
/general/scroll_workspaces
/general/toggle_workspaces
/general/workspaces_count
/general/workspaces_names
/general/wrap_workspaces
$ xfconf-query -c xfwm4 -p /general/scroll_workspaces
true
$ xfconf-query -c xfwm4 -p /general/scroll_workspaces -s false
```

## 图形化设置
![截图_1698030251259](https://github.com/icinfra/icinfra.github.io/assets/32032219/57bad2bf-437e-48cf-b757-427db75b262f)
