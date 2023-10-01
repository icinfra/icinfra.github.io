---
layout: post
title: 限制用户直接访问lsf执行机
date: 2023-03-22 09:57:58+0800
description: 
tags: lsf
giscus_comments: true
categories: icenv
---

# 需求
禁止用户直接访问LSF执行机，以实现LSF执行机的用户进程都来自于LSF的调度，确保使用的公平性，以及方便管理员管理。

# 实现
1. https://www.ibm.com/docs/en/spectrum-lsf/10.1.0?topic=bsub-about-interactive-jobs  //将队列配置为batch-only，以禁止用户提交interactive的job
2. https://www.ibm.com/docs/en/spectrum-lsf/10.1.0?topic=cluster-restrict-user-access-remote-hosts  //禁止普通用户执行lsrun, lsgrun与lsmake
3. 每台机器的sshd配置，禁止普通用户登录。

三个步骤组合起来，可以满足需求。但interactive往往是必须的，因此可以细化队列的管理，允许个别队列的interactive。