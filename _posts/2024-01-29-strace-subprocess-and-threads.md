---
layout: post
title: strace命令追踪子进程以及多线程
date: 2024-01-29 10:15+0800
description: 
tags: strace
giscus_comments: true
categories: icenv
---

# 多线程
strace命令，可以使用`-f`来追踪`-p <PID>`指定进程的所有线程。

# 子进程
对于子进程呢，strace是如何追踪的？

strace命令，可以使用`-f`来追踪被追踪时新创建的子进程，而不会追踪原来已经创建了的子进程。因此，如果需要追踪一个已经启动的进程的所有子进程，需要分别将子进程ID用`-p <PID>`传进来追踪。
