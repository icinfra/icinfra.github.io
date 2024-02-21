---
layout: post
title: spack bootstrap in air-gapped system
date: 2024-01-21 11:15+0800
description: 
tags: spack
giscus_comments: true
categories: icenv
---

# 背景
首次使用spack时，虽然将gmake-4.4.1.tar.gz包下载至mirror目录，但还是提示如下：
```bash
spack install gcc@13.2.0 +binutils
==> Installing gmake-4.4.1-bun3eynjvtrgzylwfldooydmcbtgsavx [1/2]
==> No binary for gmake-4.4.1-bun3eynjvtrgzylwfldooydmcbtgsavx found: installing from source
==> Error: FetchError: All fetchers failed for spack-stage-gmake-4.4.1-bun3eynjvtrgzylwfldooydmcbtgsavx
```

# 分析
需先在离线系统下`spack bootstrap`。在air-gapped system（离线系统）需要手动将bootstrap相关包准备好，否则spack会尝试去互联网取并失败。

# 步骤
在在线系统下，执行
```bash
$ spack bootstrap mirror --binary-packages /opt/bootstrap
==> Adding "clingo-bootstrap@spack+python %apple-clang target=x86_64" and dependencies to the mirror at /opt/bootstrap/local-mirror
==> Adding "gnupg@2.3: %apple-clang target=x86_64" and dependencies to the mirror at /opt/bootstrap/local-mirror
==> Adding "patchelf@0.13.1:0.13.99 %apple-clang target=x86_64" and dependencies to the mirror at /opt/bootstrap/local-mirror
==> Adding binary packages from "https://github.com/alalazo/spack-bootstrap-mirrors/releases/download/v0.1-rc.2/bootstrap-buildcache.tar.gz" to the mirror at /opt/bootstrap/local-mirror

```

将`/opt/bootstrap`目录拷贝到离线系统下，并添加，
```bash
$ spack bootstrap add --trust local-sources /opt/bootstrap/metadata/sources
$ spack bootstrap add --trust local-binaries /opt/bootstrap/metadata/binaries
```

# 效果
```bash
$ spack install gcc@13.2.0 +binutils
==> Fetching file:///tools/opensrc/spack/spack-mirror/bootstrap_cache/build_cache/linux-centos7-x86_64-gcc-10.2.1-patchelf-0.16.1-p72zyan5wrzuabtmzq7isa5mzyh6ahdp.spec.json
==> Fetching file:///tools/opensrc/spack/spack-mirror/bootstrap_cache/build_cache/linux-centos7-x86_64/gcc-10.2.1/patchelf-0.16.1/linux-centos7-x86_64-gcc-10.2.1-patchelf-0.16.1-p72zyan5wrzuabtmzq7isa5mzyh6ahdp.spack
==> Installing "patchelf@=0.16.1%gcc@=10.2.1 ldflags="-static-libstdc++ -static-libgcc"  build_system=autotools arch=linux-centos7-x86_64" from a buildcache
==> Fetching file:///tools/opensrc/spack/spack-mirror/bootstrap_cache/build_cache/linux-centos7-x86_64-gcc-10.2.1-clingo-bootstrap-spack-prqkzynv2nwko5mktitebgkeumuxkveu.spec.json
==> Fetching file:///tools/opensrc/spack/spack-mirror/bootstrap_cache/build_cache/linux-centos7-x86_64/gcc-10.2.1/clingo-bootstrap-spack/linux-centos7-x86_64-gcc-10.2.1-clingo-bootstrap-spack-prqkzynv2nwko5mktitebgkeumuxkveu.spack
==> Installing "clingo-bootstrap@=spack%gcc@=10.2.1~docs~ipo+python+static_libstdcpp build_type=Release arch=linux-centos7-x86_64" from a buildcache
==> Installing gmake-4.4.1-7xujubssqx5cedh3lnbz7nhzgn2kjpyh [1/30]
==> No binary for gmake-4.4.1-7xujubssqx5cedh3lnbz7nhzgn2kjpyh found: installing from source
```
