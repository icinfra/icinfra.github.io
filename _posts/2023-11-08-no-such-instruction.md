---
layout: post
title: gcc编译时无法提示没有这样的指令
date: 2023-11-07 23:28+0800
description: 
tags: gcc
giscus_comments: true
categories: icenv
---

![image](https://github.com/icinfra/icinfra.github.io/assets/32032219/d7f3c00b-e674-4ffa-91f1-5e4a1d860dfe)

由于编译的gcc，没有将binutils编进去，从而它使用了系统下的as (binutils提供的)汇编命令。而系统下的as命令版本太低，不识别新CPU的flag。

解决方法是：重新编gcc，将新版本的binutils编进去了。
