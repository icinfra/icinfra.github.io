---
layout: post
title: strace与perf trace
date: 2022-09-05 22:15:00
comments: true
description: 
tags: post
categories: linux
---

## Strace
strace是众所周知的系统调用追踪工具。由于它依赖于ptrace暂停应用来获取系统调用的相关信息，这导致在使用strace过程中非常差的性能。在strace过程中，每个系统调用会暂停两次：一次是进入系统调用、一次是离开系统调用。

## perf trace
perf trace使用trace points来收集系统调用信息，在tracing过程中，应用无需被暂停。

此外，perf trace还扩展到使用eBPF程序来做syscall参数追踪。

## 案例
![syscall%20tracing](/assets/img/Snipaste_2022-09-06_11-56-44_trace-dd-command.png)