---
layout: post
title: Python的双端队列
date: 2023-03-13 18:20:56+0800
description: 
tags: python
giscus_comments: true
categories: icenv
---

# 介绍
双端队列允许两端进行元素的增加或删除操作。Python collections.deque是一个线程安全的双端队列。当队列满了，从一端插入元素，另一端的最后一个元素会被丢弃。

# 实验
```bash
[wanlinwang@computing-server-01 ~]$ python3
Python 3.10.8 (main, Mar 12 2023, 22:29:09) [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from collections import deque
>>> dq = deque(range(10), maxlen=10) #创建最大长度为10的双端队列
>>> dq
deque([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], maxlen=10)
>>> dq.rotate(3) #向右滚动3个元素，最右端的会依次放到最左端。
>>> dq
deque([7, 8, 9, 0, 1, 2, 3, 4, 5, 6], maxlen=10)
>>> dq.rotate(-4) #向左移动4个元素，最左端的会依次放到最右端。
>>> dq
deque([1, 2, 3, 4, 5, 6, 7, 8, 9, 0], maxlen=10)
>>> dq.appendleft(-1) #在左端，增加一个元素-1，可以看到最右端的元素被丢弃了。
>>> dq
deque([-1, 1, 2, 3, 4, 5, 6, 7, 8, 9], maxlen=10)
>>> dq.extend([11,22,33]) #在右端扩展3个元素，可以看到最左的3个元素被丢弃了。
>>> dq
deque([3, 4, 5, 6, 7, 8, 9, 11, 22, 33], maxlen=10)
>>> dq.extendleft([10,20,30,40]) #在左端扩展4个元素，可以看到最右的4个元素被丢弃了。
>>> dq
deque([40, 30, 20, 10, 3, 4, 5, 6, 7, 8], maxlen=10)
```

