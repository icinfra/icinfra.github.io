---
layout: post
title: XDG_DATA_DIRS变量导致im-chooser不正常
date: 2023-04-26 19:38:12+0800
description: 
tags: im
giscus_comments: true
categories: icenv
---

# 问题描述
CentOS 7.9桌面用户，重新登录的vnc会话，运行im-chooser无法在右上角唤起输入法选择器。


# 问题定位
通过二分排除法定位到是spack安装的vim的modulefile里，好几句设置XDG_DATA_DIRS语句导致，
```bash
prepend-path XDG_DATA_DIRS "/tools/opensrc/spack/opt/spack/linux-tlinux2-icelake/gcc-11.2.0/atk-2.36.0-44etyekjnugxjiz6tblr7zddv5igvzn2/share"
```

# 问题根因
TODO


# 参考资料
1. XDG_DATA_DIRS变量介绍： https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
2. CentOS 7.9桌面用户安装中文输入法：https://blog.csdn.net/thesre/article/details/125595496