---
layout: post
title: chat.openai.com提示Unable to load history
date: 2023-11-08 23:00+0800
description: 
tags: chatgpt
giscus_comments: true
categories: icenv
---

今天chat.openai.com登录后，提示Unable to load history

<img width="283" alt="image" src="https://github.com/icinfra/icinfra.github.io/assets/32032219/7294fb08-91e1-4f6d-8759-46e0c8cefd17">

打开F12发现很多403 forbidden的：原来是访问的部分URI，被openai block了。

解决方法：VPS访问openai之间，再用WARP套一层，openai没那么容易去封WARP如此大的公网IP池。
