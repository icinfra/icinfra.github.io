---
layout: post
title: ssh时提示no matching host key type found. Their offer：rsa-sha2-512,rsa-sha2-256
date: 2023-11-09 09:56+0800
description: 
tags: ssh
giscus_comments: true
categories: icenv
---

![image](https://github.com/icinfra/icinfra.github.io/assets/32032219/efa4d0dd-93f1-4c86-91ae-8fa70939106d)

遇到这样提示时，可以手动指定HostKeyAlgorithms，
```bash
while true; do ssh -N -D 1080 -i /drives/c/Users/wanlinwang/.ssh/id_rsa -o HostKeyAlgorithms=+rsa-sha2-512 wanlinwang@open; done
```
