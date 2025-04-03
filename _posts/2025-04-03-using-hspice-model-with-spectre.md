---
layout: post
title: Using Hspice Model with Spectre
date: 2025-04-03 00:00:00 +0800
categories: [icenv]
tags: [analog]
---

**[经验分享] 如何在 Cadence Spectre 中使用 HSPICE 模型（含 spp 工具转换方法）**

大家好，今天分享一下在 Cadence Spectre 中使用 HSPICE 模型的一些方法，供有需要的朋友参考。

---

### ✅ 方法一：Spectre v7 及以上版本 – 直接仿真

从 Spectre v7 起，Cadence 已经支持直接仿真 HSPICE 网表。使用方式非常简单：

```bash
spectre your_netlist.sp
```

无需修改 `.sp` 网表内容，Spectre 会自动识别并执行，非常方便。

---

### ✅ 方法二：Spectre v5 用户 – 使用 spp 工具转换模型

对于使用较早版本（如 v5）的 Spectre 用户，仍可以通过 Cadence 提供的 `spp` 工具将 HSPICE 模型转换为 Spectre 可识别的格式。

#### 🔧 转换步骤如下：

1. **屏幕显示转换结果：**

   ```bash
   spp -convert < bjt.lib
   ```

2. **将结果保存为 Spectre 格式文件：**

   ```bash
   spp -convert < bjt.lib > bjt.scs
   ```

转换后生成的 `bjt.scs` 文件就是可供 Spectre 使用的模型库文件。

---

### ⚠️ 注意事项：

- `spp` 转换后生成的 `.scs` 文件中，模型引用的文件名可能需要根据实际路径手动调整。
- 并非所有 HSPICE 模型都能完美转换，遇到错误需根据 log 做相应修改。

---

如有其他经验或疑问，欢迎留言讨论！

---

### 参考文档
https://bbs.eetop.cn/thread-297147-1-1.html
