---
layout: post
title:  time to read/write in spin disk
date:   2024-03-13 23:30:00+0800
description: 
tags: disk
giscus_comments: true
categories: icenv
---

寻道以及旋转所需时间，相加：
seek time：4～15ms
平均等half a revolution：～4ms

读写臂切换磁道时：time to 读写臂切换track，time to servo seek，time to settle onto the middle of the desired track。1）以前的设计是下一磁道的第一个 block 紧接着上一磁道最后一个 block，而读写臂切换track需要时间，切到下一磁道时，第一个block已经错过了。因此需要等它完全转一圈才能开始读取/写入；2）现在的设计，下一磁道的第一个 block 大约在上一次到最后一个 block 的 1/5 圈后。这样读写臂切换过去，大概到第一个 block的位置了。