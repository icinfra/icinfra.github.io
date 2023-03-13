---
layout: post
title: OpenVPN连上去就断开，然后重连，如此反复
date: 2023-03-13 13:10:39+0800
description: OpenVPN连上去就断开，然后重连，如此反复
tags: openvpn
giscus_comments: true
categories: icenv
---

# 问题
OpenVPN连上去3秒就断开，然后重连，如此反复。
![](/assets/img/Pasted%20image%2020230313131237.png)

# 原因
OpenVPN仅支持单客户端连接。当多客户端连接时，会互相挤下线。

# 解决
将不使用的终端下线。