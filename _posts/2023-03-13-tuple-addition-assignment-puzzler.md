---
layout: post
title: Python tuple += 的谜题
date: 2023-03-13 22:08:53+0800
description: 
tags: python
giscus_comments: true
categories: icenv
---

Python的tuple是一个不可修改的数据类型。
```bash
>>> a = (1,2,3)
>>> a[0]
1
>>> a[0] = 11
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment
```

那么tuple里放一个list，对这个tuple里的list做扩展，是什么结果？
```bash
>>> t = (1, 2, [30, 40])
>>> t[2] += [50, 60]
```
1. t变成(1, 2, [30, 40, 50, 60])
2. 像上面那样抛出TypeError: 'tuple' object does not support item assignment
3. 1与2都不是
4. 1与2都是

答案如下，是不是出乎意料？
```bash
>>> t = (1, 2, [30, 40])
>>> t[2] += [50, 60]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'tuple' object does not support item assignment
>>> t
(1, 2, [30, 40, 50, 60])
```

通过https://pythontutor.com/visualize.html#mode=display图形化查看代码执行
![](/assets/img/Pasted%20image%2020230313222004.png)
![](/assets/img/Pasted%20image%2020230313222032.png)

使用dis模块查看s[a] += b的字节码
```bash
>>> import dis
>>> dis.dis('s[a] += b')
  1           0 LOAD_NAME                0 (s)
              2 LOAD_NAME                1 (a)
              4 DUP_TOP_TWO
              6 BINARY_SUBSCR
              8 LOAD_NAME                2 (b)
             10 INPLACE_ADD
             12 ROT_THREE
             14 STORE_SUBSCR
             16 LOAD_CONST               0 (None)
             18 RETURN_VALUE

```

> DUP_TOP_TWO: 将栈顶的两个引用复制，保持顺序
> BINARY_SUBSCR: TOS = TOS1[TOS]的实现
> ROT_THREE：将栈顶的第二、第三个元素提升一个位置，将最顶的放到第三位置。
> ROT_TWO: 将栈顶的两个元素对调


# 参考资料
https://docs.python.org/3/library/dis.html
https://learning.oreilly.com/library/view/fluent-python-2nd/9781492056348/ch02.html#tuple_puzzler
https://www.synopsys.com/blogs/software-security/understanding-python-bytecode/