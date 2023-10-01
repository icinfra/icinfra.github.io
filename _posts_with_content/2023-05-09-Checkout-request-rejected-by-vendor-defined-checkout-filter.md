---
layout: post
title: Checkout request rejected by vendor-defined checkout filter报错
date: 2023-05-10 08-43-45 08:43:45+0800
description: 
tags: license
giscus_comments: true
categories: icenv
---

# 问题
软件运行报错
```bash
Checkout request rejected by vendor-defined checkout filter
Feature: Proto********S-RT
License path: 27020@hostname
FlexNet Licensing error:-53,234


Please choose another license.
```

# 原因
https://docs.flexera.com/fnmea/2020r1/ConceptGuide/Content/helplibrary/License_Denials.htm 可获得该报错的解释，`The application has a built-in test for the license that failed and rejected the license checkout.` 。

# 解决
在License Server侧，执行`lmutil lmreread -c <license.txt>`一下license file解决。