---
layout: post
title: spack打开modules
date: 2023-05-07 17-13-22 17:13:22+0800
description: 
tags: spack
giscus_comments: true
categories: icenv
---

# 背景
spack是HPC使用最广的包管理器之一。
最近行业内朋友频繁遇到一个问题：在使用新版本spack安装完工具后，未生成工具的modulefile。

# 解决
根据官网介绍，
https://spack.readthedocs.io/en/latest/module_file_support.html#write-a-configuration-file

![](/assets/img/Pasted%20image%2020230507171645.png)

可以打开tcl、lmod或者二者都打开。