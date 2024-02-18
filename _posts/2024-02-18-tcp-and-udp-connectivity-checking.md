---
layout: post
title: tcp/udp连通性测试
date: 2024-02-18 09:45+0800
description: 
tags: network
giscus_comments: true
categories: icenv
---


# 背景
说起开通防火墙端口（比如FlexNet license server的端口），通常用的是TCP协议，大家通常也默认是为需要开通的端口，开通TCP协议的访问。


由于大部分服务使用了TCP协议，这样开通没问题。但是有些使用了UDP协议，导致服务无法起来，如[这篇文章](https://www.icinfra.cn/blog/2023/lsf-problems/)提到的lsf服务起不来的问题。

# 排查
说起测试端口连通性，大家也第一时间想到telnet工具。但telnet是基于TCP协议的，因此只能测试tcp的连通性，无法测试udp的连通性。

先明确服务使用了**哪些端口什么协议**，然后**使用对应的工具**，逐个测试其连通性。

## 如何测试TCP连通性？
telnet工具用法：`telnet hostname port`

nc工具用法：`nc -zv [hostname] [port]`

## 如何测试UDP连通性？
nc工具用法：`nc -zvu [hostname] [port]`


# 参考资料
https://en.wikipedia.org/wiki/Telnet  telnet是基于TCP协议的，因此只能测试tcp的连通性。
