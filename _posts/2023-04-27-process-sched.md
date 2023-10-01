---
layout: post
title: 
date: 2023-04-27 16-47-12 16:47:12+0800
description: 
tags: 
giscus_comments: true
categories: 
---


构造用例
使用perf抓取

查看间隔，这里频率是250。也就是每4ms来看一次。

开启准确的调度。开启HRTICK，实际上用得少。


cat /proc/<PID>/sched
renice 调整进程优先级。

组调度。cgroup


负载均衡。



RCU是很重要的一个

RCU stall detect