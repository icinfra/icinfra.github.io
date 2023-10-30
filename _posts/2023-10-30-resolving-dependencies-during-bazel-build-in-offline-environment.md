---
layout: post
title: 离线环境bazel构建，如何解决外部依赖？
date: 2023-10-30 16:53+0800
description: 
tags: bazel
giscus_comments: true
categories: icenv
---

# bazel外部依赖的解决步骤

1. 在项目根目录执行`bazel fetch //... `，将所有外部依赖抓到本地的cache目录（`~/.cache/bazel`）下。将该目录传到内网服务器的对应目录。

2. 如https://github.com/chipsalliance/riscv-dv 这个项目，其`remotejdk11_linux`没有被步骤1下载，手动下载好到一个目录`/path/to/dependencies`。将该目录传到内网服务器。

3. 在内网服务器，执行构建命令 `bazel build --cxxopt='-std=c++17' --distdir=/path/to/dependencies //...` 



# 踩过的坑
步骤1还可以逐个识别需要下载的包，放到一个目录下，然后在WORKSPACE中定义的依赖的url将互联网地址（http[s]://开头的）修改到本地文件地址（file://开头的）。但是这个可操作性不强，直接依赖尚可识别，但是间接依赖不好弄，还得一个个弄。

# 参考资料

https://bazel.build/run/build?hl=zh-cn#fetching-external-dependencies

https://bazel.build/reference/command-line-reference?hl=zh-cn#analyze-profile-options
