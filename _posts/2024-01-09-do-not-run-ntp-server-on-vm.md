---
layout: post
title: 为什么不要将ntp service运行在virtual machine上？
date: 2024-01-09 11:50+0800
description: 
tags: ntp
giscus_comments: true
categories: icenv
---

# 背景
NTP是Network Time Protocal，被计算机分布式服务依赖，用来同步。一旦时间服务器与客户端时间差异较大，分布式服务通信可能出问题。

virtual machine（下文以“虚拟机”代替）以其轻量、标准化、预置快，在如今使用的越来越频繁。也有很多人使用它来提供ntp服务。

# 分析
虚拟机没有硬件时钟源，它仅由虚拟机监控程序提供服务，尽管提供了一个名为 kvm-clock 的半虚拟化驱动程序作为更准确的时钟源。此外，虚拟机也可能被暂停，或从一台宿主机漂移到另一台宿主机，这时由不同的hypervisor提供服务，导致提供的NTP不可靠。在KVM虚拟机中，NTP 服务器提供的 NTP 时间的精度和准确性不足以在无更高层 NTP 服务器的情况下提供 NTP 服务。NTP 服务器不是为在虚拟机内部运行而设计的。它需要高分辨率的系统时钟，对时钟中断的响应时间具有很高的精度。


# 参考资料
https://access.redhat.com/solutions/361803

https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/html/Virtualization_Host_Configuration_and_Guest_Installation_Guide/chap-Virtualization_Host_Configuration_and_Guest_Installation_Guide-KVM_guest_timing_management.html
