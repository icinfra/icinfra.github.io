---
layout: post
title: 将已有的spack安装目录串起来，实现复用
date: 2023-10-24 23:34+0800
description: 
tags: spack
giscus_comments: true
categories: icenv
---

根据这里 https://spack.readthedocs.io/en/latest/chain.html 介绍，可以将一个或多个已存在的spack安装目录串起来，实现复用。
这在spack版本升级时非常有用，spack在不定期地迭代更新，但是每一个spack版本默认将包安装在其 opt/spack/ 目录下，如果想升级版本时则无法利用旧版本已安装的那些包。利用该特性，可以实现对旧版本spack已安装的包的复用。

如下所示，
```bash
cat /tools/opensrc/spack-0.20.1/etc/spack/defaults/upstreams.yaml
upstreams:
  spack-instance-1:
    install_tree: /tools/opensrc/spack-0.20.0/opt/spack
    modules:
      tcl: /tools/opensrc/spack-0.20.0/share/spack/modules
```
