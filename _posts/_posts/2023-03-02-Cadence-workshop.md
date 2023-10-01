---
layout: post
title:  Cadence workshop 20230302
date:   2023-03-02 09:55:00+0800
description: 20230302举办“【深圳线下】开始报名！HPC 芯片全流程验证解决方案专场研讨会 – 深圳站”
tags: workshop
giscus_comments: true
categories: icenv-posts
---

# 一、提升仿真速度
业界仿真工具的功能类似，拼性能。

## 5X Xcelium MC App
这个成熟吗？加速门级DFT仿真。
Test suite latency受制于最长的那个case。通过MC将它切分到多核运行。追求效率与资源的平衡。
ARM-Based or X86-based
将没有依赖性的拆分，会引入一些overhead。
在SingleCore时加选项，可以生成profile，来评估哪些可以加速。
DFT可以考虑用MC做加速。


## 5X Xcelium ML App
通过机器学习来提升回归吞吐。模型是自己训练还是厂家提供？
需要安装额外的ML安装包，依赖于vmanager做集成。正在做无vmnanager的集成，下半年推出。
达到同样的效果，会做精简。降低回归时间。很多case是冗余的，随机种子很多是伪随机。随机空间更加优化。

以收敛率，生成更好的随机空间，随机变量。
节省资源，释放更多的资源。

Bug Hunting。

通过随机的。如果是定向的则没有意义。

## 5X Advanced Build Tech
并行编译、增量编译（改动不大的，做成snapshot）。
很多IP是固定的，没有必要每次都编译。 增量编译。编testcase，再花两分钟将它链到固定的部分。
语法检查，并行编译，所有的编译好的文件，做一个elaboration。


## 10X Save/Restore and dynamic Test Load
所有人都从那个点开始，用**UVM的动态重载功能**。在run的时候可以override。
base testcase，跑完save snapshot（非常大、复杂的状态集）。开始case的时候对base testcase考量，这样初始化只需要跑一些。
如果case已经建好，再去拆就比较麻烦了，因为每个case都例化了一个UVM environment了。


# Full Power Solution
略