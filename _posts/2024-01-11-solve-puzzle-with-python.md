---
layout: post
title: 用Python猜谜
date: 2024-01-11 23:20+0800
description: 
tags: python
giscus_comments: true
categories: icenv
---

这里，记录一个比较有趣的谜题解决方法。

# 谜题
![image](https://github.com/icinfra/icinfra.github.io/assets/32032219/da1af0c3-3ff2-4c9f-9bec-9611c4099d71)

谜题出现于20240111，**疯狂星期四**。
![image](https://github.com/icinfra/icinfra.github.io/assets/32032219/3c6f5a25-c6a8-4807-b35d-142f806e7d61)



# 思路
编程来解决这个问题。

```python3
#!/usr/bin/env python3

# 定义线索
clues = [
    ("ABC", (1, True)),   # A B C - 一个数字正确且位置正确
    ("AEF", (1, False)),  # A E F - 一个数字正确但位置不正确
    ("CKA", (2, False)),  # C K A - 两个数字正确但位置都不正确
    ("DEB", (0, False)),  # D E B - 所有数字都不正确
    ("BDK", (1, False))   # B D K - 一个数字正确但位置不正确
]

# 定义可能的数字
digits = "ABCDEFGHK"  # 可能的数字，排除了未提到的

# 生成所有可能的三字母组合
from itertools import permutations

# 初始化一个列表来保存可能的组合
possible_combinations = [''.join(p) for p in permutations(digits, 3)]

# 检查组合是否符合线索的函数
def check_combination(combination, clue):
    digit_correct, position_correct = clue[1]
    # 计算有多少数字是正确且位置正确的
    correct_digits_and_positions = sum(1 for i in range(3) if combination[i] == clue[0][i])
    # 计算有多少数字是正确的，不考虑位置
    correct_digits = sum(1 for c in clue[0] if c in combination)
    
    # 根据线索进行检查
    if position_correct:
        return correct_digits_and_positions == digit_correct
    else:
        if digit_correct == 0:
            return correct_digits == 0
        return correct_digits == digit_correct and correct_digits_and_positions == 0

# 通过每条线索过滤可能的组合
for clue in clues:
    possible_combinations = [comb for comb in possible_combinations if check_combination(comb, clue)]

print(possible_combinations)
```

<img width="329" alt="image" src="https://github.com/icinfra/icinfra.github.io/assets/32032219/3059bc70-3d85-4b0b-acdd-9f8aaafff34d">
