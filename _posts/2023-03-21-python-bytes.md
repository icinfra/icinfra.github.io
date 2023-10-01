---
layout: post
title: Python bytes的单个元素与slice
date: 2023-03-21 21:59:32+0800
description: 
tags: python
giscus_comments: true
categories: icenv
---

```python
wanlinwang@MacBook-Pro ~ % python3 
Python 3.10.8 (main, Mar 17 2023, 21:21:21) [Clang 14.0.0 (clang-1400.0.29.202)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> cafe = bytes('café', encoding='utf_8')
>>> cafe
b'caf\xc3\xa9'
>>> cafe[0]
99
>>> cafe[:1]
b'c'
>>> type(cafe[0])
<class 'int'>
>>> type(cafe[:1])
<class 'bytes'>
>>> 
```

Python bytes的单个元素与slice，不是同一种类型。bytes的单个元素，是一个范围是0到255的整数；而bytes的slice同样是bytes，即使slice的长度是1。