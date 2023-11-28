---
layout: post
title:  git ssh通过squid proxy访问
date: 2023-11-28 17:51+0800
description: 
tags: squid
giscus_comments: true
categories: icenv
---

# 背景
现有IDC服务器A，仅可访问内网。以及一台云服务器B，可通过NAT访问外网，以及被A访问。

# 需求
A服务器需要访问github.com，做代码开发的上传下载。

<img width="278" alt="image" src="https://github.com/icinfra/icinfra.github.io/assets/32032219/d313a295-54d1-4a9f-9873-3b8ec50526d5">

# 配置squid
在B服务器上安装squid，配置/etc/squid/squid.conf，将这两行加到前面，
```bash
...
acl Safe_ports port 22 # ssh
acl SSL_ports port 22 # ssh
```

# 启动squid
```bash
systemctl enable squid --now
```

# 机器A配置git config
这里，请按照一下 corkscrew 工具，再往下配置。

![image](https://github.com/icinfra/icinfra.github.io/assets/32032219/29e95590-f8a2-4c75-bdd0-c3bf6283befa)


在github.com上配置好ssh key之后，在机器A执行成功，
```bash
git clone git@github.com/wanlinwang/test-repo
```
