---
layout: post
title: 如何禁止普通用户关闭lmgrd?
date: 2022-08-30 22:47::21
comments: true
description: 
tags: post
categories: license
---

## 问题
License管理员以lmgrd启动的license进程，普通用户从本地或远程，能通过`lmutil lmdown`命令将其关闭掉。不仅如此，普通用户还有权限运行lmutil的子命令lmreread与lmremove命令。真是头大，普通用户权限咋这么大？

## 解决
通过查[资料](https://knowledge.autodesk.com/zh-hans/support/alias-products/learn-explore/caas/CloudHelp/cloudhelp/2015/CHS/Alias-Reference/files/GUID-6386AE3D-EC0C-48EA-87D0-B57948CF59E5-htm.html)可以看到，有两种选项能够使得lmgrd的运行更安全。

* 方法一

启动lmgrd时，加上`-local`选项，限制lmdown与lmreread命令只能从运行lmgrd的这台机器上发起。由于限制了使用机器，如果license机器是专用机器，则这样就很安全了。\
如果license机器不是专用机器，则方法一也不够安全，则继续看方法二。

* 方法二

启动lmgrd时，加上`-2 -p`选项，限制默认为root用户的 FLEXlm 管理员使用 lmdown、lmreread 和 lmremove。如果存在一个名为“lmadmin”的 Unix 组，则限制该组的成员使用。如果超级用户不是该组的成员，则该帐户无法使用上述任何实用程序。“-p”选项可以在 FLEXlm v2.4 以及更高版本中使用。\
由于方法二是赋予操作权限给指定用户或组，它没有限制机器，因此在保证安全的前提下，又给与了管理员足够的灵活性——不必专门登录到License机器来执行这三个命令。
