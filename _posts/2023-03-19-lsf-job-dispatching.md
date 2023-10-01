---
layout: post
title: LSF如何将job分散到集群运行
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


# 解决方案


## 方案一：基于执行机接收时间间隔
经查看手册[^1]，

> JOB_ACCEPT_INTERVAL=integer[ S | s | M | m ]
> 
> where S | s indicates that the value is in seconds and M | m indicates that the value is in minutes.
> If you set a unit (seconds or minutes), the value that you specify determines how long to wait after dispatching a job to a host before dispatching a second job to the same host.
> 
> If you do not set a unit, the value you specify is multiplied by the value of lsb.params MBD_SLEEP_TIME (60 seconds by default). The result of the calculation is the number of seconds to wait after dispatching a job to a host, before dispatching a second job to the same host.
> 
> If 0 (zero), a host may accept more than one job. By default, there is no limit to the total number of jobs that can run on a host, so if this parameter is set to 0, a very large number of jobs might be dispatched to a host all at once. This can overload your system to the point that it will be unable to create any more processes. It is not recommended to set this parameter to 0.
> 
> JOB_ACCEPT_INTERVAL set at the queue level (lsb.queues) overrides JOB_ACCEPT_INTERVAL set at the cluster level (lsb.params).

可以通过调整同一台执行机接收job的时间间隔，来达到将job分散到集群中的执行机的需求。

[^1]: https://www.ibm.com/docs/en/spectrum-lsf/10.1.0?topic=lsbparams-job-accept-interval

设置
```bash
[lsfadmin@lsf-server-01 lsf]$ grep JOB_ACCEPT_INTERVAL /nfs/home/lsfadmin/lsf/lsf/conf/lsbatch/myCluster01/configdir/lsb.params
#JOB_ACCEPT_INTERVAL = 0   # Interval for any host to accept a job 
JOB_ACCEPT_INTERVAL = 1  # 语法：JOB_ACCEPT_INTERVAL=integer[ S | s | M | m ]。 如果未指定单位，则该时间等于该数值乘以MBD_SLEEP_TIME，而MBD_SLEEP_TIME缺省值是60秒，在安装时会被设定为10秒。
[lsfadmin@lsf-server-01 lsf]$ badmin reconfig
Checking configuration files ...
No errors found.
Reconfiguration initiated
[lsfadmin@lsf-server-01 ~]$ bparams -l| grep MBD_SLEEP_TIME
    MBD_SLEEP_TIME = 10 (seconds)
    JOB_ACCEPT_INTERVAL = 1 (* MBD_SLEEP_TIME)
```


在10秒内，连续提交三个job，可以看到它们分散在了三台执行机器。
![](/assets/img/JOB_ACCEPT_INTERVAL等于15时，连续提交的作业不会调度到同一台机器上Snipaste_2023-03-19_22-04-41%201.png)

## 方案二：基于主机指标
经查看手册[^2]，RES_REQ的order string介绍如下，

[^2]: https://www.ibm.com/docs/en/spectrum-lsf/10.1.0?topic=strings-order-string

> The order string allows the selected hosts to be sorted according to the values of resources. The values of r15s, r1m, and r15m used for sorting are the normalized load indices that are returned by lsload -N.
>
> The order string is used for host sorting and selection. The ordering begins with the rightmost index in the order string and proceeds from right to left. The hosts are sorted into order based on each load index, and if more hosts are available than were requested, the LIM drops the least desirable hosts according to that index. The remaining hosts are then sorted by the next index.
>
> After the hosts are sorted by the leftmost index in the order string, the final phase of sorting orders the hosts according to their status, with hosts that are currently not available for load sharing (that is, not in the ok state) listed at the end.
>
> Because the hosts are sorted again for each load index, only the host status and the leftmost index in the order string actually affect the order in which hosts are listed. The other indices are only used to drop undesirable hosts from the list.
>
> When sorting is done on each index, the direction in which the hosts are sorted (increasing versus decreasing values) is determined by the default order returned by lsinfo for that index. This direction is chosen such that after sorting, by default, the hosts are ordered from best to worst on that index.
>
> When used with a cu string, the preferred compute unit order takes precedence. Within each compute unit hosts are ordered according to the order string requirements.

如果order string里有多个指标，则**从右到左**依次处理，上一个指标排序后的输出成为下一个指标排序的输入，直到最左的指标排序完成，选出合适的执行机进行调度。

LSF的RES_REQ order string默认是r15s:pg，如下图所示，

![](/assets/img/Pasted%20image%2020230319225247.png)

在pg指标排序完之后，再r15s排序，最优的胜出。

**回到本文的需求**，想将job调度到slot可用数量多的，可以这样设置
```bash
[lsfadmin@lsf-server-01 lsf]$ grep DEFAULT_RESREQ_ORDER ./conf/lsbatch/myCluster01/configdir/lsb.params
DEFAULT_RESREQ_ORDER = slots
[lsfadmin@lsf-server-01 lsf]$ badmin reconfig
Checking configuration files ...
No errors found.
Reconfiguration initiated
```

连续提交三个job上去，看下效果，

![](/assets/img/Pasted%20image%2020230319231331.png)