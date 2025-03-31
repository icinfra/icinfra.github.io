---
layout: post
title: verilator性能优化
date: 2024-02-20 10:45+0800
description: 
tags: verilator
giscus_comments: true
categories: icenv
---

参考资料： 
1. https://veripool.org/papers/Verilator_Accelerated_OSDA2020.pdf
2. https://verilator.org/guide/latest/environment.html#cmdoption-arg-OBJCACHE verilator可以使用分布式编译器 distcc（https://github.com/distcc/distcc?tab=readme-ov-file） 来利用多机编译。
3. https://veripool.org/papers/Verilator_Fast_Free_Me_DVClub10_pres.pdf P23提到使用distcc + ccache在多机进行编译。

