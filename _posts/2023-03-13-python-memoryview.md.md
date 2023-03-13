---
layout: post
title: Python Memoryview
date: 2023-03-13 10:36:42+0800
description: 什么是Python Memoryview，可以用在什么地方Z？
tags: python
giscus_comments: true
categories: icenv
---

# memoryview
根据 [MemoryView objects](https://docs.python.org/3/c-api/memoryview.html) 介绍，memoryview对象暴露了C层次的buffer interface作为Python对象，可以被传递到任何其它对象。

# 实验

## 一
透过本实验，可以看到memoryview.cast()方法可以不修改位来改变读取与写入的单位，它返回另一个memoryview对象，但与原memoryview是共享内存的。
```bash
[wanlinwang@computing-server-01 ~]$ python3
Python 3.10.8 (main, Mar 12 2023, 22:29:09) [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from array import array
>>> octets = array('B', range(6))
>>> octets
array('B', [0, 1, 2, 3, 4, 5])
>>> m1 = memoryview(octets)
>>> ml
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'ml' is not defined. Did you mean: 'm1'?
>>> m1
<memory at 0x7f2af10db880>
>>> m1.tolist()
[0, 1, 2, 3, 4, 5]
>>> m2 = m1.cast('B', [2,3])
>>> m2.tolist()
[[0, 1, 2], [3, 4, 5]]
>>> m3 = m1.cast('B', [3,2])
>>> m3.tolist()
[[0, 1], [2, 3], [4, 5]]
>>> octets
array('B', [0, 1, 2, 3, 4, 5])
>>> m2[1,1] = 22
>>> m2.tolist()
[[0, 1, 2], [3, 22, 5]]
>>> m3[1,1] = 33
>>> m3.tolist()
[[0, 1], [2, 33], [22, 5]]
>>> octets
array('B', [0, 1, 2, 33, 22, 5])
>>>
```


## 二


```bash
[wanlinwang@computing-server-01 ~]$ python3
Python 3.10.8 (main, Mar 12 2023, 22:29:09) [GCC 4.8.5 20150623 (Red Hat 4.8.5-44)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import array
>>> numbers = array.array('h', [-2,-1,0,1,2])
>>> memv = memoryview(numbers)
>>> len(memv)
5
>>> memv[0]
-2
>>> memv_oct = memv.cast('B')
>>> memv_oct.tolist()
[254, 255, 255, 255, 0, 0, 1, 0, 2, 0]
>>> memv_oct[5] = 4
>>> numbers
array('h', [-2, -1, 1024, 1, 2])
>>> ```

