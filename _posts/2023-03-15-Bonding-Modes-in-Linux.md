---
layout: post
title: Linux的网卡bonding模式
date: 2023-03-15 21:39:18+0800
description: 
tags: network
giscus_comments: true
categories: icenv
---

# 不同的Bonding Mode区别
网卡Bonding是一项在操作系统层面上实现的网络冗余技术。设置网卡Bonding后，内核会将多条物理链路组成一条逻辑虚拟链路，在网络层上实现高可用。

## mode 0(balance-rr)
Round-robin policy。从组内的第一个Slave接口开始，以轮询的方式将数据按顺序依次发放。该模式提供load balancing以及fault tolerance。

## mode 1(active-backup)
Active-backup policy。只有一个slave是active的。当且仅当active slave失效了，另一个slave就会变成active。bond的MAC地址只在一个端口上对外可见，避免了交换机混淆。该模式提供fault tolerance。

## mode 2(balance-xor)
基于选择的transmit hash policy传输。policy可以通过xmit_hash_policy更改。该模式提供load balancing以及fault tolerance。

## mode 3(broadcast)
在所有slave接口上都传输。该模式提供fault tolerance。

## mode 4(802.3ad)
IEEE 802.3ad Dynamic link aggregation policy。创建聚合组，共享相同的速率与工作模式。根据802.3ad规范，充分利用active aggregator里的所有slave。
对于outgoing流量的slave接口选举，是通过transmit hash policy来完成的。policy可以通过xmit_hash_policy更改。

xmit_hash_policy的值
* layer2 or 1
> hash = source MAC XOR destination MAC XOR packet type ID
> slave number = hash modulo slave count

* layer2+3 or 2
> hash = source MAC XOR destination MAC XOR packet type ID
> hash = hash XOR source IP XOR destination IP
> hash = hash XOR (hash RSHIFT 16)
> hash = hash XOR (hash RSHIFT 8)
> And then hash is reduced modulo slave count.

* layer3+4 or 3
> hash = source port, destination port (as in the header)
> hash = hash XOR source IP XOR destination IP
> hash = hash XOR (hash RSHIFT 16)
> hash = hash XOR (hash RSHIFT 8)
> And then hash is reduced modulo slave count.

该模式对硬件的要求
1. ethtool支持基础驱动，取回每个slave的速率与单双工工作模式。
2. 交换机虚支持IEEE 802.3ad Dynamic link aggregation。

列子：
![](/assets/img/Pasted%20image%2020230315230142.png)

## mode 5(balance-tlb)
发送负载均衡。不需要交换机的任何特殊支持。outgoing的流量会分布到各个slave，incoming的流量会被当前的slave接收。如果当前slave失效了，其他的slave会接管它的MAC地址。

## mode 6(balance-alb)
它包括IPv4的发送负载均衡以及接收负载均衡。不需要交换机的任何特殊支持。接收负载均衡，是通过ARP协商实现。bonding驱动拦截本机发出的ARP reply，重写source MAC地址为bond中的其中一个slave的MAC地址。如此一来，不同的对端与本机不同的MAC地址进行通信，达到接收负载均衡的效果。



# 不同的Bonding Mode对交换机的配置要求

|Bonding Mode|Configuration on the Switch|
|--|--|
|0 - balance-rr|Requires static Etherchannel enabled(not LACP-negotiated)|
|1 - active-backup|Requires autonomous ports|
|2 - balance-xor|Requires static Etherchannel enabled(not LACP-negotiated)|
|3 - broadcast|Requires static Etherchannel enabled(not LACP-negotiated)|
|4 - 802.3ad|Requires LACP-negotiated Etherchannel enabled|
|5 - balance-tlb|Requires autonomous ports|
|6 - balance-alb|Requires autonomous ports|



# 参考文献
https://www.kernel.org/doc/Documentation/networking/bonding.txt
https://www.ibm.com/docs/en/linux-on-systems?topic=recommendations-bonding-modes
https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/networking_guide/ch-configure_network_bonding