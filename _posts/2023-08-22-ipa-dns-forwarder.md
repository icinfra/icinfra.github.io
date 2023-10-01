---
layout: post
title: ipa dns forwarder的注意事项
date: 2023-08-22 22-04-58 22:04:58+0800
description: 
tags: ipa
giscus_comments: true
categories: icenv
---


一、global DNS forwarder，在CentOS 7.9与CentOS 8.8上，

1. 如果安装时指定了(global) DNS forwarder，安装完毕之后，使用

```bash

ipa dnsconfig-mod --forwarder=8.8.8.8

```

这样修改(global) DNS forwarder是不生效的。这可能是一个bug。



2. 如果安装时没有指定(global) DNS forwarder，安装完毕之后，使用

```bash

ipa dnsconfig-mod --forwarder=8.8.8.8

```

这样设置(global) DNS forwarder是生效的。



二、指定domain的DNS forwarder，在CentOS 7.9与CentOS 8.8上，

在安装完毕之后，使用

```bash

ipa dnsforwardzone-add google.com --skip-overlap-check --forwarder=8.8.8.8

```

这样修改，在解析 google.com 时这个DNS forwarder是生效的。

综上，1）在安装FreeIPA或IdM时，请不要指定DNS Forwarder，安装之后再设置即可；2）如果已有的FreeIPA或IdM已经设置了DNS Forwarder，但这个DNS Forwarder变得不可用，那可以使用`ipa dnsforwardzone-add google.com --skip-overlap-check --forwarder=8.8.8.8`语句为指定的域设置DNS Forwarder查询。
