---
layout: post
title:  how to use different glibc
date:   2024-03-27 07:45:00+0800
description: 
tags: glibc
giscus_comments: true
categories: icenv
---

# 背景
IC设计环境需要使用大量的开源工具。快速迭代的开源工具往往在开发时依赖于高版本的库，如glibc库。但IC设计环境主流还在使用CentOS 7.9，系统自带的glibc不满足运行条件。

通常，为了满足运行条件，IT向业务提供一台自带高版本 glibc 的操作系统使用。如果仅仅为了运行小部分不常用的软件，这种方式成本较高。

# 需求
在已有的操作系统上，让软件运行依赖于高版本的glibc，但同时不能影响已有软件在系统上的运行。

# 解决
自行编译一个高版本glibc，并让软件使用它提供的链接器，以及让软件去找它提供的libc库。

## 编译

这里使用自动化包管理器spack解决诸多复杂的依赖。
```bash
$ spack install glibc
```

## 让软件使用它
### 源码重新编译
```bash
g++ main.o -o myapp ... \
   -Wl,--rpath=/path/to/newglibc_lib_dir \
   -Wl,--dynamic-linker=/path/to/newglibc_lib_dir/ld-linux.so.2
```

### 修改已编译软件
用patchelf修改，选项如下
```bash
patchelf --set-interpreter /path/to/newglibc_lib_dir/ld-linux.so.2 --set-rpath /path/to/newglibc_lib_dir/ myapp
```

# 参考资料
https://stackoverflow.com/a/44710599

https://stackoverflow.com/a/851229