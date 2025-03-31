---
layout: post
title: License报告的方案调研与思路
date: 2023-10-23 12:34+0800
description: 
tags: license
giscus_comments: true
categories: icenv
---

https://www.openlm.com/blog/application-note-1030-openlm-license-usage-monitoring-according-to-projects-v1-8/

由于VENDOR Daemon写的REPORT LOG是加密的，无法被除FLEXnet Manager之外的其它软件打开。因此，OPENLM的项目费用统计，不是通过读取REPORT LOG来获得的，而是通过其它小技巧获得的：
* 通过给用户assign唯一的项目；
* 通过在用户的workstation部署OpenLM Agent获取，定期或者触发式弹窗让用户选择当前正在工作的project是什么；
* 后向兼容LM_PROJECT变量来获取项目信息，这个也是需要以某种方式（root部署在每台workstation的OpenLM Agent？）将用户环境中的LM_PROJECT变量以时序的方式记录下来，供生成报告时使用。
