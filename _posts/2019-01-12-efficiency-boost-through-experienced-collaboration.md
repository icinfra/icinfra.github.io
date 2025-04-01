---
layout: post
title: 多和资深的同仁交流，就会发现惊人的效率提升
date: 2019-01-12 08:00:00+0800
description: 
tags: efficiency
giscus_comments: true
categories: icenv
---

这次《Zabbix架构分享&Promethues架构初探》培训交流会，我想做一次总结。
早在一个月前，老大就请我去调研Zabbix在大型IT架构中的使用，以及初探Promethues监控系统，并对两大监控系统做较详细的对比。
我觉得前两者在本次会议中，基本上覆盖到了。
第一点：Zabbix在大型IT结构中普遍会应用上Proxy，Agent将监控数据推送到Proxy，然后由Proxy将数据推送到Zabbix Server中。

![image](https://github.com/user-attachments/assets/e92ceb42-3035-4c12-ac2f-dc3e2df08eaa)

另一张图：
![image](https://github.com/user-attachments/assets/d30facf6-0374-4e06-8503-22acde3e2587)


第二点：Prometheus is a Cloud Native Computing Foundation member project. 下图是它的架构。让我最震撼的是它的数据获取自由性很高：支持使用别人制作好的Exporters，支持自己编写Exporter，或者使用SpringBoot埋点，还支持Short-lived jobs将metrics push到PushGateway上去。架构这么灵活，难怪能成为“CNCF第二名毕业生”。非常适合后续云化业务的监控。

![image](https://github.com/user-attachments/assets/fd3179e0-0305-4d1b-b754-ef5cd9daa7c3)


第三点仅以“Zabbix适用于物理机的监控，而Prometheus适用于云等微服务架构；Zabbix将监控数据存储在关系型数据库中，而Prometheus将监控数据存放在了时序性数据库”潦草介绍了下。
呼应题目：前两周，断断续续有花过3天左右的时间准备这个PPT和会议。使用docker搭建了Zabbix，Prometheus，Grafana来熟悉这些系统。但是没有搞清楚Prometheus是怎么去定义需要监控的指标项，可怕的是自己也没有想到要去了解这个。培训前和老大预热的时候，老大问的特仔细。问到是怎么配置监控策略的时候，我竟一脸茫然，连相关的资料看到没看过。吓得我赶紧抱佛脚。接着就了解到了有很多人针对不同的场景写好了很丰富的Exporters，如果自己的业务场景并在外面的世界不常见，找不到对应的Exporter的话，也可以使用Go、Python或Java来自行编写自己的Exporter。也可以在Java项目中埋点取指标值，如网站登录人数等。
没有交谈前，我没方向去了解，两眼一抹黑。所以所获知识甚少。若我有架构意识，也应该能想到要去查阅各个组件的协作及用法。
交谈后，就发现了自己准备的不足。加以查阅，理解，然后组织了一次较为流利的培训交流会。
