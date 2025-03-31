---
layout: post
title: mill工具的proxy设置
date: 2024-01-15 16:30+0800
description: 
tags: mill
giscus_comments: true
categories: icenv
---

# 背景
新Scala构建工具mill正在流行。很多Scala开发环境是内网环境，访问互联网需要通过proxy。

# 问题
用户设置了http_proxy与https_proxy变量，执行mill构建Scala工程时卡住。

![image](https://github.com/icinfra/icinfra.github.io/assets/32032219/ee7932fa-092b-4016-b516-1c46665c7819)

# 解决
假设http proxy的主机与端口为 your-proxy-server.com:8080，则按照以下步骤来让mill使用proxy：

1. 在构建环境，设置环境变量JAVA_OPTS="-Dhttp.proxyHost=your-proxy-server.com -Dhttp.proxyPort=8080 -Dhttps.proxyHost=your-proxy-server.com -Dhttps.proxyPort=8080"
2. 在调用mill时，加上`-i`选项。
