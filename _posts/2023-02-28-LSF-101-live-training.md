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

今天下午，IBM举办的LSF初级在线培训。Agenda如下

* Basic of LSF and architecture
* Overview of LSF Family products
* LSF and LSF Suite installation
* LSF License Scheduler
* Use PAC to submit and manager jobs
* Use RTM to monitor LSF cluster
* Q&A

# 内容

## IBM Spectrum LSF支持各种工作负载的调度

* 传统的HPC/HTC（batch&Interactive）作业
* 容器化作业
* 大数据作业
* 机器学习作业

## IBM Spectrum LSF对（云上云下）各种共享（异构）资源的管理

* Power
* x86
* Linux on z
* SPARC
* Arm
* containers
* 存储（Flash，Disk，and Tape）

## LSF术语

|角色|数量|说明|
|-|-|-|
|Client|一个或多个|作为提交机，可以是Linux，或者是Windows|
|master host|一个master host，一个或多个master candidate host|可以作为提交机与执行机。也可以CLOSED使得它不作为提交机、执行机，专机专用，避免工作负载影响了LSF master的调度|
|server host|一个或多个|可以作为提交机与执行机。它也可以是一个master cadidate host|
|job||提交：从提交机提交到master host放到Queue并PEND<br/>调度：被调度器调度到执行机，通常占用1个slot<br/>执行：执行机接收到job后开始执行|


## LSF架构
Master与Host的各种服务之间的联系。待补充图。

* 所有机器有LIM进程
> host上的LIM进程会收集当前node的负载、资源使用情况，有哪些资源，比如CPU型号、OS版本等，定期发送给master的LIM。这样master就知道所有这些主机的情况。用户也可以通过elim（plugin module）来自定义监控，如温度等等。

* 所有机器有SBD进程
> 当作业提交到master时，会在MBD、MBSCHD里排队。MBD是集群里最重要的核心组件，它会把master LIM里收集到host的信息拿到，并且知道集群里排队作业的情况，进行作业与资源的匹配、派遣到执行机。host的SBD会根据用户指定的命令行，将作业运行起来，直到作业结束。

* 守护进程异常处理
> 当host的守护进程宕掉之后，master就无法收集host的信息，此时host将会被标为unavail的状态。在最新的RHEL里，有一个lsf的patch，它使用systemd来管理lsf的守护进程，当lsf守护进程宕掉后，systemd自动将它重启起来。

* job
> LSF对job没有特殊要求，只要它能够在单机上运行，那么它就可以在LSF集群里执行，不需要做过多的集成。假设master与host没有共享文件系统的话，可以设置将job的输出拷贝回提交机。

## IBM Spectrum LSF Family

有很多add-on，如

* Application Center
> web页面

* Process Manager

* License Scheduler
> EDA License是非常昂贵的，基于FlexLM或RLM的，结合License调度，达到License的最大化使用。

* Data Manager
> 在on-premise LSF资源不够时，将job弹到云上，此时借助Data Manager来决定哪些数据是需要传上去给job使用的。

* Resource Connector
> 多集群时使用。在on-premise LSF资源不够时，到客户指定的云上去动态申请机器并将其加到现有的LSF集群，用来跑作业。当作业跑完后释放资源。

* Explorer
> 监控集群的使用情况。定期产生报表，是否要扩缩容。

## Editions

### IBM Spectrum LSF Community Edition

* Community Edition可扩展到10个节点，最大job数2,500个；

### IBM Spectrum LSF Suite Editions

商业有三个版本，功能越来越强大：

* Workgroup可扩展到 128 个节点，最大job数25,000个；
* HPC可扩展至 1,024 个节点，最大job数250,000个；
* Enterprise的节点与job数量没有限制。

### 版本号介绍

* 10.1.0.13 的10.1.0为major release，13为fix pack（每0.5~1年一次）。

## 安装与配置

### 标准版安装与使用
* 确定用于安装LSF的服务器是什么CPU架构，什么操作系统；
* 在IBM passport advantage上面下载对应的安装包
> - lsf10.1_lsfinstall.tar.Z(Passport Advantage)
> - lsf10.1_OS-Spec.tar.Z(Passport Advantage)
> - lsf10.1_OS-Spec-build-number.tar.Z(Fix Central)
> - platform_lsf_std_entitlement.dat  \#许可证，如果无许可证，安装完之后是社区版。
* 解压
* 修改配置文件install.config
* 安装，建议在共享文件系统（如Spectrum Scale，即原来的GPFS，可被深度集成的，如每作业占用文件系统大小；或NFS）下安装，命令如下

```bash
$ ./lsfinstall -f install.config
$ $LSF_ENVDIR/../10.1/install/patchinstall </path/to/fp>
```

* 安装最新的fix pack（截止至发稿，是FP13。于2022年中旬发布）。请注意，最新的fix pack已经包含当前major release的所有fix pack了，不需要将FP1...FP12都补上，直接打FP13即可。

LSF启动的服务以及默认端口

|LSF Master|LSF Server|Port|Desc|
|--|--|--|--|
|lim|lim|7869|Load Information Manager|
|pim|pim||Process information Manager|
|res|res|6878|Remote Execution Server|
|sbatchd|sbatchd|6882|Slave Batch Daemon|
|mbatchd||6881|Master Batch Daemon|
|mbschd|||Master Batch Scheduler|

* 用户初始化
> `source /path/to/lsf/conf/cshrc.lsf #for csh`

> `. /path/to/lsf/conf/profile.lsf # for bash`

初始化完了之后，执行`which bsub`可以验证是否初始化成功。


注意：
* LSF安装后不支持cluster name修改。
* 使用IBM certified的GPFS来安装LSF。也支持NFS，但性能稍差。也可以安装在local文件系统，但为了支持failover，建议Master安装在共享文件系统。
* Master支持在物理机或者虚拟机安装，以满足客户对混合云的部署需求。
* 标准版的cli安装，Suit版的Ansible安装
* Suit版以.bin结尾，不需先安装基础包再安装fix pack包。而标准版则两步骤分开。
* Entitlement File，标准版里需手动下载指定，而Suit版本已内置。
* 最大Node数量：标准版里技术上不限制，通过合同限制。而Suit版技术上就限制了最大Node数量。

## 高级特性

* 从_？_版本开始，支持带lockid的badmin hclose，方便管理员做不同原因的hclose操作。
* 有Workload Template功能，便于用户根据不同业务类型，快速上手LSF的使用。
* 提供用户各种终端交互，包括cli，web，mobile以及api等。
* process manager支持flow的定制

## 周边组件支持

* RTM（Report, Track, and Monitor）支持对两种License管理器使用情况的收集展示：FlexLM与RLM。
* 一个RTM支持对多个LSF集群监控。
* License Scheduler支持对两种License管理器——FlexLM与RLM的bsub rusage条件使用。
* 支持Docker作业。另，K8S在调度方面能力弱，LSF支持作为K8S的调度组件使用。
* LSF RTM Server是开源的，卖服务。而RTM Poller（RTM Data Collectors）是闭源的商业产品，采集存储的数据结构相对稳定，字段一般只增不减，方便客户基于该数据源做定制化聚合与展示。
* Application Center的权限模型是RBAC的。
* LSF管理数据存放在MeraiDB，作业日志存放在ElasticSearch里。

## 如何试用？

* 自行安装社区版
* 与代理商或者原厂联系，申请私有化部署测试环境
* 在<https://techzone.ibm.com/collection/ibm-spectrum-lsf-suite>申请suite版本测试，自带少量Node，需注册。

# Q&A

* lsadmin与admin的区别是？
> The lsadmin command controls the operation of the lim and res daemons.
> The badmin command controls the operation of the mbatchd and sbatchd daemons.

# 致谢

感谢主办方以及IBM的分享。

# 参考资料

1. <https://www.ibm.com/docs/en/spectrum-lsf/10.1.0?topic=linux-preparing-your-systems-installation> for Integrating LDAP with LSF.

2. <https://www.ibm.com/docs/en/spectrum-lsf-rtm/10.1.0?topic=alerts-setting-up-email-server-notifications> for settings up email server notifications for RTM.

3. <https://www.ibm.com/docs/en/spectrum-lsf/10.1.0?topic=limits-specify-resource-usage> for specifying resource usage limits.

4. <https://www.ibm.com/docs/en/spectrum-lsf/10.1.0?topic=resources-define-ncpusprocessors-cores-threads> for ncpus definition.

5. <https://www.ibm.com/docs/en/spectrum-lsf/10.1.0?topic=migrate-upgrade> for migrating or upgrading LSF.

6. <https://www.ibm.com/docs/en/slsfh/10.2.0?topic=updating-installation-scenarios>

7.
