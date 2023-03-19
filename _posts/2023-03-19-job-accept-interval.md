---
layout: post
title: LSF的JOB_ACCEP_INTERVAL介绍与使用
date: 2023-03-19 22:06:56+0800
description: 
tags: lsf
giscus_comments: true
categories: icenv
---

# 需求
研发想将job尽可能地均匀分散在集群中的执行机上，将负载均匀地分散到集群中，而不是默认的往一台调度，这台满了再往下一台调度。
如图，是默认的调度情况，连续提交的job都调度到了同一台机器，

![](/assets/img/JOB_ACCEPT_INTERVAL等于0时，前后job都调度到同一台执行机上Snipaste_2023-03-19_22-01-10.png)


# 解决
经查看手册，可以通过设定往同一台机器调度job的时间间隔，来达到将job分散到集群中的执行机的需求。
设置
```bash
[lsfadmin@lsf-server-01 lsf]$ grep JOB_ACCEPT_INTERVAL /nfs/home/lsfadmin/lsf/lsf/conf/lsbatch/myCluster01/configdir/lsb.params
#JOB_ACCEPT_INTERVAL = 0   # Interval for any host to accept a job 
JOB_ACCEPT_INTERVAL = 15  # Interval for any host to accept a job 
[lsfadmin@lsf-server-01 lsf]$ badmin reconfig
Checking configuration files ...
No errors found.
Reconfiguration initiated
```

可以看到，再连续提交三个job，分散在了三台执行机器。
![](/assets/img/JOB_ACCEPT_INTERVAL等于15时，连续提交的作业不会调度到同一台机器上Snipaste_2023-03-19_22-04-41%201.png)