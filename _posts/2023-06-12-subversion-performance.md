---
layout: post
title: 
date: 2023-06-12 21-46-33 21:46:33+0800
description: 
tags: svn
giscus_comments: true
categories: icenv
---

# 背景
据作者了解，截止至本文写作，芯片研发业务大多在使用CentOS/RHEL 7，其中7.9是final版本，使用的最多。还有些因历史项目与老旧工具版本，在使用CentOS/RHEL 5或者6的。

在这些环境下，IT部署svn，一般是直接`yum install subversion`进行安装的。以CentOS 7.9为例，安装的是1.7.14版本的svn。


软件在迭代升级过程中，除修复bug，新增feature，还有很重要的一点是带来性能提升。subversion也不例外，可以参考wandisco公司做的benchmark[^1]。

[^1]: http://live.wandisco.com/Fuhrmann_SVNlive2014%20Benchmarking%20SVN.pdf

# 实验
由wandisco公司提供的benchmark可以得到规律：subversion版本越高，获得的性能越强。我们用自己的环境做实验，当前版本1.7.14 vs. 最新稳定版本1.14.1。

环境说明

| 序号 | 环境一 | 环境二 |
| ------ | ------ | ------ |
| 服务器 | CentOS 7.9 | CentOS 7.9 |
| SVN Server | 1.14.1 | 1.7.14 |
| SVN Client | 1.14.1 | 1.7.14 |
| 测试仓库所属业务 | 验证 | 验证 |
| checkout仓库node数量 |  |  |
| checkout仓库rev数量 | 14885 | 14885 |
| update rev至 | 15669 | 15669 |


实验数据

| 序号 | 环境一 | 环境二 | 时间%降低至 |
| ------ | ------ | ------ | ------ |
| co | 63.470u 22.431s | 110.595u 24.920s | 63% |
| co | 63.467u 22.718s | 113.484u 25.144s | 62% |
| up | 44.089u 16.353s | 84.621u 19.304s | 58% |
| up | 43.856u 16.083s | 83.391u 19.075s | 58% |


# 结论

在常见的checkout与upadte场景下，svn 1.14.1比1.7.14性能更强——耗时降低至60%左右。

鉴于实验结论，我们可以将svn升级到新版本以获得更优的性能。
