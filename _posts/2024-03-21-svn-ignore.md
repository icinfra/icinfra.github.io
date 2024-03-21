---
layout: post
title:  svn ignore设置
date:   2024-03-21 10:25:00+0800
description: 
tags: svn
giscus_comments: true
categories: icenv
---



svn(subversion)关于ignore的设置，在文末的参考资料中搜global-ignores，可以看到用户**没有做任何设置的情况下，默认忽略了一些后缀文件**。

如果需要不忽略：
- 可以通过显示地加上 --no-ignore 选项。或者，
- 修改 ~/.subversion/config 全局文件。或者，
- svn propset svn:ignore来设置一个目录下直接文件，svn propset svn:global-ignores 来设置一个目录树下的所有文件。


### 参考资料
https://svnbook.red-bean.com/nightly/en/svn.advanced.confarea.html#svn.advanced.confarea.opts.config
