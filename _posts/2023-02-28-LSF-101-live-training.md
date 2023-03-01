---
layout: post
title:  LSF初级在线培训
date:   2023-02-28 18:30:00+0800
description: IBM举办的LSF初级在线培训
tags: formatting links
giscus_comments: true
categories: icenv-posts
---

# 简介
今天下午，IBM举办的LSF初级在线培训。

# 纪要
## 标准版与Suit版的安装与配置
* 使用IBM certified的GPFS来安装LSF。也支持NFS，但性能稍差。也可以安装在local文件系统，但为了支持failover，建议Master安装在共享文件系统。
* Master支持在物理机或者虚拟机安装，以满足客户对混合云的部署需求。
* 标准版的cli安装，Suit版的Ansible安装
* Suit版以.bin结尾，不需先安装基础包再安装fix pack包。而标准版则两步骤分开。
* Entitlement File，标准版里需手动下载指定，而Suit版本已内置。
* 最大Node数量：标准版里技术上不限制，通过合同限制。而Suit版技术上就限制了最大Node数量。

## 周边组件支持
* RTM支持对两种License管理器使用情况的收集展示：FlexLM与RLM。
* 一个RTM支持对多个LSF集群监控。
* License Scheduler支持对两种License管理器——FlexLM与RLM的bsub rusage条件使用。
* 支持Docker作业。另，K8S在调度方面能力弱，LSF支持作为K8S的调度组件使用。
* 从_？_版本开始，支持带lockid的badmin hclose，方便管理员做不同原因的hclose操作。
* LSF RTM Server是开源的，卖服务。而RTM Poller（RTM Data Collectors）是闭源的商业产品。
* Application Center的权限模型是RBAC的。

## 如何试用？
* 自行安装社区版
* 与代理商或者原厂联系，申请私有化部署测试环境
* 在https://techzone.ibm.com/collection/ibm-spectrum-lsf-suite申请suite版本测试，自带少量Node，需注册。

## 致谢
感谢主办方以及IBM的分享。