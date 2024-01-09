---
layout: post
title: 升级ipa并保持用户原密码
date: 2024-01-09 10:50+0800
description: 
tags: ipa
giscus_comments: true
categories: icenv
---

# 背景
由于[CentOS 7/8的EOL](https://www.icinfra.cn/blog/2024/centos-7-and-8-eol/)，IC设计环境的IT底座————操作系统，其升级被提上日程。其中涉及到在旧版本操作系统上的FreeIPA的升级。

# 思考
开始，我想着在一台新操作系统上做fresh FreeIPA installation，给升级上去的操作系统使用即可。
后来，考虑在过渡期间需要维护两套FreeIPA，需要从旧FreeIPA里同步用户/群组到新FreeIPA，并且两套系统内用户的密码还不能够保持统一。从红帽官网，找了升级的相关资料，决定使用Replica的方式来使得新旧FreeIPA数据同步，也能够保持用户的密码一致，降低用户的上手成本。

# 升级方案
## 架构图
升级的过渡期间，FreeIPA master-replica架构图，如下所示：
```bash
+---------------------+            +----------------------------+
|                     |            |                            |
|   CentOS 7 VM       |            |    AlmaLinux 8 VM          |
|                     |            |                            |
|   +-------------+   |            |   +--------------------+   |
|   |             |   |            |   |                    |   |
|   | FreeIPA     |   |            |   | AlmaLinux 8        |   |
|   | Server      |   | Replication|   | Container          |   |
|   | (Master)    |   |------------>   |                    |   |
|   +-------------+   |            |   | +----------------+ |   |
|                     |            |   | |                | |   |
+---------------------+            |   | | FreeIPA        | |   |
                                   |   | | Server         | |   |
                                   |   | | (Replica)      | |   |
                                   |   | +----------------+ |   |
                                   |   |                    |   |
                                   |   +--------------------+   |
                                   |                            |
                                   +----------------------------+

```
其中，CentOS 7 VM里的是直接安装启动的FreeIPA Server。在AlmaLinux 8 VM里运行的AlmaLinux 8 Container里运行FreeIPA Server Replica。

这里使用容器来承载新FreeIPA Server，主要考虑到容器环境可以做到标准化，数据通过持久化到容器宿主机（AlmaLinux 8 VM）的目录下，再定期快照备份容器宿主机（AlmaLinux 8 VM）。

## 相关命令
暂略。

# 测试项
## 用户/群组同步
包括用户/群组的ID/Subordinate ID以及相关信息的同步。需要注意的是，CentOS 7 VM里自带的FreeIPA Server是不支持Subordinate ID的，因此需要加强对它的测试————比如在AlmaLinux 8 Container上的FreeIPA Server创建的Subordinate ID能否被持久化保存，并被正常使用。

## 域名解析

## 时间同步

## 其它项

# 参考资料
[IdM从非RHEL发行版迁移至RHEL8](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/migrating_to_identity_management_on_rhel_8/ref_migrating-to-idm-on-rhel-8-from-freeipa-on-non-rhel-linux-distributions_migrating-to-idm-from-external-sources)

[FreeIPA Replica Setup](https://www.freeipa.org/page/V4/Replica_Setup)

[IdM Replica安装](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/installing_identity_management/installing-an-ipa-replica_installing-identity-management#installing-an-idm-replica-with-integrated-dns-and-a-ca_install-replica)
