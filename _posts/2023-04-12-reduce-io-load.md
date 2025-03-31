---
layout: post
title: 降低Environment Modules的I/O Load
date: 2023-04-12 12:34:10+0800
description: 
tags: modules
giscus_comments: true
categories: icenv
---

# 背景
前司在全球拥有多个数据中心，每个数据中心有多个集群。其中，单个集群的运算机达4位数台物理机的规模。

在大量的验证任务跑起来时，经常会遇到NFS卡死的问题，用户敲一个ls命令会卡个几十秒或者根本就无响应。
问题从业务部门爆发之后，CAD与IT部门之间，互相丢锅——
1. CAD埋怨IT提供的存储性能太低，正常的业务需求都满足不了；
2. 而IT则埋怨CAD没有引导好业务，将很多不必要的I/O操作避免掉。

# 分析
分析下来，二者责任都有——
1. CAD确实没有深入定制业务的流程工具与脚本，任由发展。另有CAD自己开发的脚本、工具，也不注意性能。
2. IT将项目目录与tool目录放在了同一机头，没有将问题域隔开。加上CAD的各种依赖的环境，业务在项目目录下ls，还得要去tool目录下读取一堆东西。

# 解决（或缓解）
针对不同的根因，我们分别展开了讨论，并形成了解决方案。由于涉及的点太多，有机会再一一展开。

本文我们重点来看Environment Modules在降低I/O Load可以有哪些方法实现。

## 在当时（约2020年）
开源社区的Environment Modules TCL版实现，常用的功能都实现了，但还未关注性能。我们环境中的MODULEPATH路径下，共有约**5000**个modulefile文件，每次执行module av时，要去MODULEPATH路径下遍历，并且读取每个文件的第一行判断是否存在Magic cookie，以决定该文件是否为有效的modulefile文件。

当时刚好跟着李智慧学习了缓存架构，我们针对Environment Modules TCL版如何能够使用缓存展开了架构讨论，并且形成了可行方案——
1. 每次安装完工具后，EDA管理员将module av的结果以指定的格式存放到一个文本文件（缓存文件）
2. 用户执行我们包装后的module av命令，这个命令不会去遍历整个MODULEPATH路径，而是只读取步骤1生成的缓存文件。
这个缓存架构，将module av命令，从**用户每次对目录的递归遍历以及几千文件的读取**，转成了**管理员一次对目录的递归遍历以及几千文件的读取**+**用户每次只读取一个缓存文件**，极大地提升了用户的体验。

## 在现在（2023.04.12）
开源社区的Environment Modules TCL版实现，性能也被关注了。从官网可以看到有几种I/O Load的优化：
* Modules Tcl extension library

	使用针对与Modules优化的Tcl扩展库，它可以减少不需要的`ioctl`, `fcntl`与`readlink`系统调用；`getents`的数量也被降到了50%；因为在尝试打开文件前不检查文件，`stat`数量也大幅降低。
* rc文件往根层级迁移
	
	这里讲到，将每个深层次的.modulerc与.version文件，全部提取到MODULEPATH的根层级来。这样它能够大大降低`access`, `stat`, `open`, `read` and `close`的数量。
* 不检查Magic Cookie
	
	前面我们提到，它为了识别文件是否是有效的modulefile，会读取第一行来判断。而实际上我们生产环境在MODULEPATH路径下放的，基本上都是modulefile。因此为了性能提升，我们可以将Magic Cookie的检查去掉，以此来减少open，read与close等系统调用的数量。
* 虚拟modules
	
	这是一种缓存方案，将modulefile的路径，以指定的命令缓存到.modulerc文件里。在执行module av时读取到.modulerc就能够知道该目录下所有的modulefile路径了，因此节省了遍历与读取的那些操作。
* Module cache
	
	这也是一种缓存方案，使用module cachebuild命令在MODULEPATH的每个路径下分别创建缓存文件。在执行module av时看到该缓存文件，直接读取该文件。因此节省了遍历与读取的那些操作。不过这个方案是在MODULEPATH的每个路径下生成缓存文件，与我之前只产生一个缓存文件的方案相比——它仍然需要读取多个文件，不过性能已经非常接近了。

# 总结
略。