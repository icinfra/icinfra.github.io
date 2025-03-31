---
layout: post
title: lsf运行问题
date: 2023-03-20 20:08:15+0800
description: 
tags: lsf
giscus_comments: true
categories: icenv
---


问题1：

`sinit: ls_getmastername() failed. Server host LIM configuration is not ready yet.`

`res/get_hostInfo: ls_gethostinfo() failed. Slave LIM configuration is not ready yet.`

![](/assets/img/Pasted%20image%2020230320200849.png)

master到执行机的udp端口不通导致问题（在执行机的input方向，**开了来自于master的tcp连接，但没开udp连接**）。

![image](https://github.com/icinfra/icinfra.github.io/assets/32032219/fd5934ed-87ea-436b-b197-e179c0a1116b)

从执行机到master通信失败导致的问题（在执行机的output方向，禁止掉了去往master的连接）。

参考资料： https://www.ibm.com/support/pages/configure-firewall-ports-lsf-management-node-platform-rtm-monitoring ，其中LSF_LIM_PORT要允许访问UDP协议。
