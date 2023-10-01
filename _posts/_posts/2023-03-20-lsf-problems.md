---
layout: post
title: lsf运行问题
date: 2023-03-20 20:08:15+0800
description: 
tags: lsf
giscus_comments: true
categories: icenv
---



![](/assets/img/Pasted%20image%2020230320200849.png)
master到执行机的udp端口不通导致问题（在执行机的input方向，开了来自于master的tcp连接，没开udp连接）。

![](/assets/img/Pasted%20image%2020230320200840.png)
从执行机到master通信失败导致的问题（在执行机的output方向，禁止掉了去往master的连接）。