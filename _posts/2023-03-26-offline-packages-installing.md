---
layout: post
title: 离线自动化安装开源工具的方案探索
date: 2023-03-26 08:50:22+0800
description: 
tags: linux
giscus_comments: true
categories: icenv
---

# 背景
包括芯片设计公司在内，许多研发型公司为了数据安全与网络安全，会将其研发环境与互联网隔绝开来，从物理上禁止了数据在内外部自由流通，也禁止了来自外部的网络攻击。
安全与效率总是不能够双双完美的，这种架构保证了安全，在很多需要数据传输、访问在线服务的场景上，这种架构就给效率打了折扣。研发环境开源工具的安装与管理，就是场景之一。

# 设计方案

## Spack

离线安装与使用的Use Case
![](/assets/img/Spack%20Use%20Case.jpg)

在线安装与使用的活动图
![](/assets/img/在线Spack安装流程.jpg)

离线安装与使用的活动图
![](/assets/img/离线Spack安装流程.jpg)

部署图

# 实施方案

## 下载与初始化Spack
在centos7-9-online机器执行
下载spack，配置初始化spack
```bash
[centos@centos7-9-online os]$ git clone -c feature.manyFiles=true https://github.com/spack/spack.git
Cloning into 'spack'...
remote: Enumerating objects: 445711, done.
remote: Counting objects: 100% (331/331), done.
remote: Compressing objects: 100% (236/236), done.
remote: Total 445711 (delta 162), reused 199 (delta 46), pack-reused 445380
Receiving objects: 100% (445711/445711), 225.50 MiB | 18.27 MiB/s, done.
Resolving deltas: 100% (182172/182172), done.
[centos@localhost os]$ echo ". `readlink -f spack/share/spack/setup-env.sh`" >>  ~/.bashrc
```
将spack目录拷贝到离线环境CentOS 7.9的`/tools/os/`目录，并配置其初始化
```bash
[centos@centos7-9-offline ]$ echo ". /tools/os/spack/share/spack/setup-env.sh" >>  ~/.bashrc
```

## 安装与配置编译器
分别于centos7-9-online、centos7-9-offline的机器执行

```bash
[centos@centos7-9-online ~]$ sudo yum install -y gcc gcc-c++ gcc-gfortran #安装编译器
[centos@centos7-9-online ~]$ sudo yum install -y patch bzip2 lbzip2 readline-devel unzip #spack install时，有些基础的会被常见的包依赖。
[centos@centos7-9-online ~]$ spack compiler find
==> Added 1 new compiler to /home/centos/.spack/linux/compilers.yaml
    gcc@4.8.5
    gcc@12.2.0
==> Compilers are defined in the following files:
    /home/centos/.spack/linux/compilers.yaml
[centos@centos7-9-online ~]$ cat /home/centos/.spack/linux/compilers.yaml
compilers:
- compiler:
    spec: gcc@4.8.5
    paths:
      cc: /usr/bin/gcc
      cxx: /usr/bin/g++
      f77: /usr/bin/gfortran
      fc: /usr/bin/gfortran
    flags: {}
    operating_system: centos7
    target: x86_64
    modules: []
    environment: {}
    extra_rpaths: []
- compiler:
    spec: gcc@12.2.0
    paths:
      cc: /nfs/tools/os/gcc/12.2.0/bin/gcc
      cxx: /nfs/tools/os/gcc/12.2.0/bin/g++
      f77: /nfs/tools/os/gcc/12.2.0/bin/gfortran
      fc: /nfs/tools/os/gcc/12.2.0/bin/gfortran
    flags: {}
    operating_system: centos7
    target: x86_64
    modules: []
    environment: {}
    extra_rpaths: []
```


## mirror
在centos7-9-online机器

```bash
[centos@centos7-9-online ~]$ mkdir /local/tools/os/spack/pkgs-mirror #创建mirror目录
[centos@centos7-9-online ~]$ spack mirror create --directory /local/tools/os/spack/pkgs-mirror --dependencies vim +gtk +gui +lua +perl +python +ruby +x +cscope #这里以mirror vim为例
==> Concretizing input specs
==> Installing patchelf-0.13.1-x5afxqz2rtlfbcpghu5l542rhhbw3md7
==> No binary for patchelf-0.13.1-x5afxqz2rtlfbcpghu5l542rhhbw3md7 found: installing from source
==> Fetching https://github.com/NixOS/patchelf/releases/download/0.13.1/patchelf-0.13.1.tar.gz
==> No patches needed for patchelf
==> patchelf: Executing phase: 'autoreconf'
==> patchelf: Executing phase: 'configure'
==> patchelf: Executing phase: 'build'
==> patchelf: Executing phase: 'install'
==> patchelf: Successfully installed patchelf-0.13.1-x5afxqz2rtlfbcpghu5l542rhhbw3md7
  Stage: 31.52s.  Autoreconf: 0.00s.  Configure: 1.15s.  Build: 2.17s.  Install: 0.03s.  Total: 34.92s
[+] /home/centos/.spack/bootstrap/store/linux-centos7-x86_64/gcc-4.8.5/patchelf-0.13.1-x5afxqz2rtlfbcpghu5l542rhhbw3md7
==> Fetching https://mirror.spack.io/bootstrap/github-actions/v0.4/build_cache/linux-centos7-x86_64-gcc-10.2.1-clingo-bootstrap-spack-prqkzynv2nwko5mktitebgkeumuxkveu.spec.json
==> Fetching https://mirror.spack.io/bootstrap/github-actions/v0.4/build_cache/linux-centos7-x86_64/gcc-10.2.1/clingo-bootstrap-spack/linux-centos7-x86_64-gcc-10.2.1-clingo-bootstrap-spack-prqkzynv2nwko5mktitebgkeumuxkveu.spack
==> Installing "clingo-bootstrap@spack%gcc@10.2.1~docs~ipo+python+static_libstdcpp build_type=Release arch=linux-centos7-x86_64" from a buildcache
==> Adding package at-spi2-atk@2.38.0 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/cf/cfa008a5af822b36ae6287f18182c40c91dd699c55faa38605881ed175ca464f.tar.xz
==> Adding package at-spi2-core@2.47.90 to mirror
==> Fetching http://ftp.gnome.org/pub/gnome/sources/at-spi2-core/2.47/at-spi2-core-2.47.90.tar.xz
==> Adding package atk@2.38.0 to mirror
==> Fetching http://ftp.gnome.org/pub/gnome/sources/atk/2.38/atk-2.38.0.tar.xz
==> Adding package autoconf@2.69 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/95/954bd69b391edc12d6a4a51a2dd1476543da5c6bbf05a95b59dc0dd6fd4c2969.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/ea/eaa3f69d927a853313a0b06e2117c51adab6377a2278549b05abc5df93643e16
==> Fetching https://mirror.spack.io/_source-cache/archive/77/7793209b33013dc0f81208718c68440c5aae80e7a1c4b8d336e382525af791a7
==> Fetching https://mirror.spack.io/_source-cache/archive/35/35c449281546376449766f92d49fc121ca50e330e60fefcfc9be2af3253082c2
==> Fetching https://mirror.spack.io/_source-cache/archive/a4/a49dd5bac3b62daa0ff688ab4d508d71dbd2f4f8d7e2a02321926346161bf3ee
==> Adding package autoconf-archive@2023.02.20 to mirror
==> Fetching https://ftpmirror.gnu.org/autoconf-archive/autoconf-archive-2023.02.20.tar.xz
==> Fetching https://mirror.spack.io/_source-cache/archive/13/139214f5104f699f868dc87a14378e1e694a3c2539efa0de6f878024f3d7c66d
==> Adding package automake@1.16.5 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/07/07bd24ad08a64bc17250ce09ec56e921d6343903943e99ccf63bbf0705e34605.tar.gz
==> Adding package bdftopcf@1.1 to mirror
==> Fetching https://www.x.org/archive/individual/app/bdftopcf-1.1.tar.gz
==> Adding package berkeley-db@18.1.40 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/0c/0cecb2ef0c67b166de93732769abdeba0555086d51de1090df325e18ee8da9c8.tar.gz
==> Adding package binutils@2.40 to mirror
==> Fetching https://ftpmirror.gnu.org/binutils/binutils-2.40.tar.bz2
==> Adding package bison@3.8.2 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/06/06c9e13bdf7eb24d4ceb6b59205a4f67c2c7e7213119644430fe82fbd14a0abb.tar.gz
==> Adding package bzip2@1.0.8 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/ab/ab5a03176ee106d3f0fa90e381da478ddae405918153cca248e682cd0c4a2269.tar.gz
==> Adding package ca-certificates-mozilla@2023-01-10 to mirror
==> Fetching https://curl.se/ca/cacert-2023-01-10.pem
==> Adding package cairo@1.16.0 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/5e/5e7b29b3f113ef870d1e3ecf8adf21f923396401604bda16d44be45e66052331.tar.xz
==> Adding package cmake@3.25.2 to mirror
==> Fetching https://github.com/Kitware/CMake/releases/download/v3.25.2/cmake-3.25.2.tar.gz
==> Fetching https://github.com/Kitware/CMake/releases/download/v3.25.2/cmake-3.25.2.tar.gz
==> Adding package cscope@15.9 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/c5/c5505ae075a871a9cd8d9801859b0ff1c09782075df281c72c23e72115d9f159.tar.gz
==> Adding package curl@8.0.1 to mirror
==> Fetching http://curl.haxx.se/download/curl-8.0.1.tar.bz2
==> Adding package dbus@1.13.6 to mirror
==> Fetching https://dbus.freedesktop.org/releases/dbus/dbus-1.13.6.tar.gz
==> Adding package diffutils@3.9 to mirror
==> Fetching https://ftpmirror.gnu.org/diffutils/diffutils-3.9.tar.xz
==> Adding package docbook-xml@4.5 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/4e/4e4e037a2b83c98c6c94818390d4bdd3f6e10f6ec62dd79188594e26190dc7b4.zip
==> Adding package docbook-xsl@1.79.2 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/31/316524ea444e53208a2fb90eeb676af755da96e1417835ba5f5eb719c81fa371.tar.bz2
==> Adding package elfutils@0.189 to mirror
==> Fetching https://sourceware.org/pub/elfutils/0.189/elfutils-0.189.tar.bz2
==> Fetching https://mirror.spack.io/_source-cache/archive/d7/d786d49c28d7f0c8fc27bab39ca8714e5f4d128c7f09bb18533a8ec99b38dbf8
==> Adding package expat@2.5.0 to mirror
==> Fetching https://github.com/libexpat/libexpat/releases/download/R_2_5_0/expat-2.5.0.tar.bz2
==> Warning: Error while fetching expat@2.5.0
  All fetchers failed for spack-stage-expat-2.5.0-yfnrdymdzqycrzk6upmebtvxa2g5motq
==> Adding package findutils@4.9.0 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/a2/a2bfb8c09d436770edc59f50fa483e785b161a3b7b9d547573cb08065fd462fe.tar.xz
==> Adding package fixesproto@5.0 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/67/67865a0e3cdc7dec1fd676f0927f7011ad4036c18eb320a2b41dbd56282f33b8.tar.gz
==> Adding package flex@2.6.3 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/68/68b2742233e747c462f781462a2a1e299dc6207401dac8f0bbb316f48565c2aa.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/f8/f8b85a00849bfb58c9b68e177b369f1e060ed8758253ff8daa57a873eae7b7a5
==> Adding package font-util@1.4.0 to mirror
==> Fetching https://www.x.org/archive/individual/font/font-util-1.4.0.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/55/55861d9cf456bd717a3d30a3193402c02174ed3c0dcee828798165fe307ee324.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/63/63087cb61d17bfc9cd6f4f9359f63a3b1dd83300a31a42fd93dca084724c6afb.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/72/720b6a513894bfc09a163951ec3dd8311201e08ee40e8891547b6c129ffb5fce.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/d5/d5602f1d749ccd31d3bc1bb6f0c5d77400de0e5e3ac5abebd2a867aa2a4081a4.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/c4/c4923342f6068c83fd4f5dbcf60d671c28461300db7e2aee930c8634b1e4b74a.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/57/57c2db8824865117287d57d47f2c8cf4b2842d036c7475534b5054be69690c73.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/54/549c6ba59979da25e85c218a26e5c527c3c24ebab2c76509c1ebc34d94fae227.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/81/817703372f080d6508cf109011b17f3572ff31047559fe82d93b487ca4e4e2d9.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/45/4509703e9e581061309cf4823bffd4a93f10f48fe192a1d8be1f183fd6ab9711.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/49/493965263070a5ee2a301dfdb2e87c1ca3c00c7882bfb3dd99368565ba558ff5.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/46/46142c876e176036c61c0c24c0a689079704d5ca5b510d48c025861ee2dbf829.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/fc/fcecbfc475dfe5826d137f8edc623ba27d58d32f069165c248a013b3c566bb59.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/97/97ee77a9d8ca3e7caf0c78c386eb0b96e8a825ca3642ec035cfb83f5f2cf1475.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/61/61eb1fcfec89f7435cb92cd68712fbe4ba412ca562b1f5feec1f6daa1b8544f6.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/30/3022b6b124f4cc6aade961f8d1306f67ff42e3b7922fb2244847f287344aefea.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/a0/a0b146139363dd0a704c7265ff9cd9150d4ae7c0d248091a9a42093e1618c427.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/21/21166546b0490aa3ec73215fa4ea28d91c6027b56178800ba51426bd3d840cc3.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/ea/eaddfc6d9b32bf38c9dc87c354be3b646a385bc8d9de6e536269f6e1ca50644e.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/97/97d9c1e706938838e4134d74f0836ae9d9ca6705ecb405c9a0ac8fdcbd9c2159.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/79/79dfde93d356e41c298c2c1b9c638ec1a144f438d5146d0df6219afb1c2b8818.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/d3/d3b93f7f73a526919bf73a38e10ef4643cd541403a682a8068d54bbcdd9c7e27.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/02/02b3839ae79ba6a7750525bb3b0c281305664b95bf63b4a0baa230a277b4f928.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/c4/c43ae370932eb8a4789a5b1f9801da15228b0d4c803251785c38d82aef024a4b.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/33/3399b7586c18be509cdaeceeebf754b861faa1d8799dda1aae01aeb2a7a30f01.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/d6/d64b9bfa5fa8dedf084f1695997cc32149485d2a195c810f62a1991ab5cd5519.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/dc/dc3b8d5890480943e735e0375f0e0d8333094fcb6d6845ba321b2e39db78d148.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/9e/9e82783758e8c67a9aadaf1a7222d13418a87455e4ce0a9974fb1df0278bdf74.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/0a/0a8c77c1540dc376fb2bb5a02bd33ee5f3563fbac9fc07c7947cac462c4bb48a.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/ae/aeea5f130480a3f05149bde13d240e668d8fb4b32c02b18914fcccd1182abe72.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/50/503e70ee66af34f6ec4426c0f4ae708e9d30dafdcd58f671a87c7bf56b1952a3.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/25/254be39c09da1c4e77d2a75a2969330ee2db395120a428671c50aef3ab745fc0.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/d9/d9e86a8805b0fb78222409169d839a8531a1f5c7284ee117ff2a0af2e5016c3f.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/e8/e8c3417d89183b1fc383fb3e0f3948c0d01fabcb9edace8b7ec85eab8cdc18c4.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/38/38301bbdb6374494f30c0b44acc7052ed8fc2289e917e648ca566fc591f0a9e0.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/5e/5e05a642182ec6a77bd7cacb913d3c86b364429329a5f223b69792d418f90ae9.tar.gz
==> Adding package fontconfig@2.14.2 to mirror
==> Fetching https://www.freedesktop.org/software/fontconfig/release/fontconfig-2.14.2.tar.gz
==> Adding package fontsproto@2.1.3 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/72/72c44e63044b2b66f6fa112921621ecc20c71193982de4f198d9a29cda385c5e.tar.gz
==> Adding package freetype@2.11.1 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/f8/f8db94d307e9c54961b39a1cc799a67d46681480696ed72ecf78d4473770f09b.tar.gz
==> Adding package fribidi@1.0.12 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/0c/0cd233f97fc8c67bb3ac27ce8440def5d3ffacf516765b91c2cc654498293495.tar.xz
==> Adding package gawk@5.2.1 to mirror
==> Fetching https://ftpmirror.gnu.org/gawk/gawk-5.2.1.tar.xz
==> Adding package gdbm@1.23 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/74/74b1081d21fff13ae4bd7c16e5d6e504a4c26f7cde1dca0d963a484174bbcacd.tar.gz
==> Adding package gdk-pixbuf@2.42.10 to mirror
==> Fetching https://ftp.acc.umu.se/pub/gnome/sources/gdk-pixbuf/2.42/gdk-pixbuf-2.42.10.tar.xz
==> Adding package gettext@0.21.1 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/50/50dbc8f39797950aa2c98e939947c527e5ac9ebd2c1b99dd7b06ba33a6767ae6.tar.xz
==> Adding package glib@2.74.6 to mirror
==> Fetching https://download.gnome.org/sources/glib/2.74/glib-2.74.6.tar.xz
==> Adding package glproto@1.4.17 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/9d/9d8130fec2b98bd032db7730fa092dd9dec39f3de34f4bb03ceb43b9903dbc96.tar.gz
==> Adding package glx@1.4 to mirror
==> Adding package gmake@4.4.1 to mirror
==> Fetching https://ftpmirror.gnu.org/make/make-4.4.1.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/fe/fe5b60d091c33f169740df8cb718bf4259f84528b42435194ffe0dd5b79cd125
==> Fetching https://mirror.spack.io/_source-cache/archive/ca/ca60bd9c1a1b35bc0dc58b6a4a19d5c2651f7a94a4b22b2c5ea001a1ca7a8a7f
==> Adding package gmp@6.2.1 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/ea/eae9326beb4158c386e39a356818031bd28f3124cf915f8c5b1dc4c7a36b4d7c.tar.bz2
==> Adding package gobject-introspection@1.72.0 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/02/02fe8e590861d88f83060dd39cda5ccaa60b2da1d21d0f95499301b186beaabc.tar.xz
==> Fetching https://mirror.spack.io/_source-cache/archive/77/7700828b638c85255c87fcc317ea7e9572ff443f65c86648796528885e5b4cea
==> Adding package gperf@3.1 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/58/588546b945bba4b70b6a3a616e80b4ab466e3f33024a352fc2198112cdbb3ae2.tar.gz
==> Adding package gtkplus@3.24.29 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/f5/f57ec4ade8f15cab0c23a80dcaee85b876e70a8823d9105f067ce335a8268caa.tar.xz
==> Adding package harfbuzz@5.3.1 to mirror
==> Fetching https://github.com/harfbuzz/harfbuzz/releases/download/5.3.1/harfbuzz-5.3.1.tar.xz
==> Adding package hwloc@2.9.0 to mirror
==> Fetching https://download.open-mpi.org/release/hwloc/v2.9/hwloc-2.9.0.tar.gz
==> Adding package icu4c@66.1 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/52/52a3f2209ab95559c1cf0a14f24338001f389615bf00e2585ef3dbc43ecf0a2e.tgz
==> Fetching https://mirror.spack.io/_source-cache/archive/6b/6be0b8068b0f5047dad7f4f6f655529304f1abbc551c93223c6f41dafc1e8acc
==> Adding package inputproto@2.3.2 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/10/10eaadd531f38f7c92ab59ef0708ca195caf3164a75c4ed99f0c04f2913f6ef3.tar.gz
==> Warning: Error while fetching inputproto@2.3.2
  sha256 checksum failed for /tmp/centos/spack-stage/spack-stage-inputproto-2.3.2-lchukheykgr7ssdkzqoc6rmu5jj3bb4d/inputproto-2.3.2.tar.gz
==> Adding package intltool@0.51.0 to mirror
==> Warning: Error while fetching intltool@0.51.0
  All fetchers failed for spack-stage-intltool-0.51.0-tqjehgpvexhz6v6ctwifojbppjtcljh7
==> Adding package json-glib@1.6.6 to mirror
==> Fetching https://download.gnome.org/sources/json-glib/1.6/json-glib-1.6.6.tar.xz
==> Adding package kbproto@1.0.7 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/82/828cb275b91268b1a3ea950d5c0c5eb076c678fdf005d517411f89cc8c3bb416.tar.gz
==> Adding package libbsd@0.11.7 to mirror
==> Fetching https://libbsd.freedesktop.org/releases/libbsd-0.11.7.tar.xz
==> Adding package libcroco@0.6.13 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/76/767ec234ae7aa684695b3a735548224888132e063f92db585759b422570621d4.tar.xz
==> Adding package libedit@3.1-20210216 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/22/2283f741d2aab935c8c52c04b57bf952d02c2c02e651172f8ac811f77b1fc77a.tar.gz
==> Adding package libepoxy@1.4.3 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/0b/0b808a06c9685a62fca34b680abb8bc7fb2fda074478e329b063c1f872b826f6.tar.xz
==> Adding package libffi@3.3 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/72/72fba7922703ddfa7a028d513ac15a85c8d54c8d67f55fa5a4802885dc652056.tar.gz
==> Adding package libfontenc@1.1.7 to mirror
==> Fetching https://www.x.org/archive/individual/lib/libfontenc-1.1.7.tar.gz
==> Adding package libgcrypt@1.10.1 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/ef/ef14ae546b0084cd84259f61a55e07a38c3b53afc0f546bffcef2f01baffe9de.tar.bz2
==> Adding package libgit2@1.5.0 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/8d/8de872a0f201b33d9522b817c92e14edb4efad18dae95cf156cf240b2efff93e.tar.gz
==> Adding package libgpg-error@1.46 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/b7/b7e11a64246bbe5ef37748de43b245abd72cfcd53c9ae5e7fc5ca59f1c81268d.tar.bz2
==> Adding package libice@1.0.9 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/78/7812a824a66dd654c830d21982749b3b563d9c2dfe0b88b203cefc14a891edc0.tar.gz
==> Adding package libiconv@1.17 to mirror
==> Fetching https://ftp.gnu.org/gnu/libiconv/libiconv-1.17.tar.gz
==> Adding package libjpeg-turbo@2.1.4 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/a7/a78b05c0d8427a90eb5b4eb08af25309770c8379592bb0b8a863373128e6143f.tar.gz
==> Adding package libmd@1.0.4 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/f5/f51c921042e34beddeded4b75557656559cf5b1f2448033b4c1eec11c07e530f.tar.xz
==> Adding package libpciaccess@0.17 to mirror
==> Fetching https://www.x.org/archive/individual/lib/libpciaccess-0.17.tar.gz
==> Adding package libpng@1.6.39 to mirror
==> Fetching https://prdownloads.sourceforge.net/libpng/libpng-1.6.39.tar.xz
==> Adding package libpthread-stubs@0.4 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/50/50d5686b79019ccea08bcbd7b02fe5a40634abcfd4146b6e75c6420cc170e9d9.tar.gz
==> Adding package librsvg@2.51.0 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/89/89d32e38445025e1b1d9af3dd9d3aeb9f6fce527aeecbecf38b369b34c80c038.tar.xz
==> Adding package libsigsegv@2.14 to mirror
==> Fetching https://ftpmirror.gnu.org/libsigsegv/libsigsegv-2.14.tar.gz
==> Fetching https://ftp.gnu.org/gnu/libsigsegv/libsigsegv-2.14.tar.gz
==> Adding package libsm@1.2.3 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/1e/1e92408417cb6c6c477a8a6104291001a40b3bb56a4a60608fdd9cd2c5a0f320.tar.gz
==> Adding package libssh2@1.10.0 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/2d/2d64e90f3ded394b91d3a2e774ca203a4179f69aebee03003e5a6fa621e41d51.tar.gz
==> Adding package libtool@2.4.7 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/04/04e96c2404ea70c590c546eba4202a4e12722c640016c12b9b2f1ce3d481e9a8.tar.gz
==> Adding package libunwind@1.6.2 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/4a/4a6aec666991fb45d0889c44aede8ad6eb108071c3554fcdff671f9c94794976.tar.gz
==> Adding package libx11@1.8.4 to mirror
==> Fetching https://www.x.org/archive/individual/lib/libX11-1.8.4.tar.gz
==> Adding package libxau@1.0.8 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/c3/c343b4ef66d66a6b3e0e27aa46b37ad5cab0f11a5c565eafb4a1c7590bc71d7b.tar.gz
==> Adding package libxcb@1.14 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/a5/a55ed6db98d43469801262d81dc2572ed124edc3db31059d4e9916eb9f844c34.tar.xz
==> Adding package libxcrypt@4.4.33 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/e8/e87acf9c652c573a4713d5582159f98f305d56ed5f754ce64f57d4194d6b3a6f.tar.xz
==> Adding package libxdmcp@1.1.4 to mirror
==> Fetching https://www.x.org/archive/individual/lib/libXdmcp-1.1.4.tar.gz
==> Adding package libxext@1.3.3 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/eb/eb0b88050491fef4716da4b06a4d92b4fc9e76f880d6310b2157df604342cfe5.tar.gz
==> Adding package libxfixes@5.0.2 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/ad/ad8df1ecf3324512b80ed12a9ca07556e561b14256d94216e67a68345b23c981.tar.gz
==> Adding package libxfont@1.5.4 to mirror
==> Fetching https://www.x.org/archive/individual/lib/libXfont-1.5.4.tar.gz
==> Adding package libxft@2.3.2 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/26/26cdddcc70b187833cbe9dc54df1864ba4c03a7175b2ca9276de9f05dce74507.tar.gz
==> Adding package libxi@1.7.6 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/4e/4e88fa7decd287e58140ea72238f8d54e4791de302938c83695fc0c9ac102b7e.tar.gz
==> Adding package libxkbcommon@1.4.0 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/10/106cec5263f9100a7e79b5f7220f889bc78e7d7ffc55d2b6fdb1efefb8024031.tar.xz
==> Adding package libxkbfile@1.0.9 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/95/95df50570f38e720fb79976f603761ae6eff761613eb56f258c3cb6bab4fd5e3.tar.gz
==> Adding package libxml2@2.10.3 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/5d/5d2cc3d78bec3dbe212a9d7fa629ada25a7da928af432c93060ff5c17ee28a9c.tar.xz
==> Fetching https://mirror.spack.io/_source-cache/archive/96/96151685cec997e1f9f3387e3626d61e6284d4d6e66e0e440c209286c03e9cc7.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/3e/3e06d42596b105839648070a5921157fe284b932289ffdbfa304ddc3457e5637
==> Adding package libxpm@3.5.12 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/25/2523acc780eac01db5163267b36f5b94374bfb0de26fc0b5a7bee76649fd8501.tar.gz
==> Adding package libxrandr@1.5.0 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/1b/1b594a149e6b124aab7149446f2fd886461e2935eca8dca43fe83a70cf8ec451.tar.gz
==> Adding package libxrender@0.9.10 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/77/770527cce42500790433df84ec3521e8bf095dfe5079454a92236494ab296adf.tar.gz
==> Adding package libxslt@1.1.33 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/8e/8e36605144409df979cab43d835002f63988f3dc94d5d3537c12796db90e38c8.tar.gz
==> Adding package libxt@1.1.5 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/b5/b59bee38a9935565fa49dc1bfe84cb30173e2e07e1dcdf801430d4b54eb0caa3.tar.gz
==> Adding package libxtst@1.2.2 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/22/221838960c7b9058cd6795c1c3ee8e25bae1c68106be314bc3036a4f26be0e6c.tar.gz
==> Adding package llvm@7.1.0 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/71/71c93979f20e01f1a1cc839a247945f556fa5e63abf2084e8468b238080fd839.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/51/514926d661635de47972c7d403c9c4669235aa51e22e56d44676d2a2709179b6
==> Adding package lua@5.4.4 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/16/164c7849653b80ae67bec4b7473b884bf5cc8d2dca05653475ec2ed27b9ebf61.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/56/56ab9b90f5acbc42eb7a94cf482e6c058a63e8a1effdf572b8b2a6323a06d923.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/20/208316c2564bdd5343fa522f3b230d84bd164058957059838df7df56876cb4ae
==> Adding package m4@1.4.19 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/3b/3be4a26d825ffdfda52a56fc43246456989a3630093cced3fbddf4771ee58a70.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/fc/fc9b61654a3ba1a8d6cd78ce087e7c96366c290bc8d2c299f09828d793b853c8
==> Adding package mesa@22.1.6 to mirror
==> Fetching https://archive.mesa3d.org/mesa-22.1.6.tar.xz
==> Fetching https://mirror.spack.io/_source-cache/archive/36/36096a178070e40217945e12d542dfe80016cb897284a01114d616656c577d73
==> Adding package meson@1.0.1 to mirror
==> Fetching https://github.com/mesonbuild/meson/archive/1.0.1.tar.gz
==> Adding package mkfontdir@1.0.7 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/bc/bccc5fb7af1b614eabe4a22766758c87bfc36d66191d08c19d2fa97674b7b5b7.tar.gz
==> Adding package mkfontscale@1.2.2 to mirror
==> Fetching https://www.x.org/archive/individual/app/mkfontscale-1.2.2.tar.gz
==> Adding package mpfr@4.2.0 to mirror
==> Fetching https://ftpmirror.gnu.org/mpfr/mpfr-4.2.0.tar.bz2
==> Fetching https://ftp.gnu.org/gnu/mpfr/mpfr-4.2.0.tar.bz2
==> Fetching https://mirror.spack.io/_source-cache/archive/3f/3f80b836948aa96f8d1cb9cc7f3f55973f19285482a96f9a4e1623d460bcccf0
==> Fetching https://mirror.spack.io/_source-cache/archive/52/5230aab653fa8675fc05b5bdd3890e071e8df49a92a9d58c4284024affd27739
==> Fetching https://mirror.spack.io/_source-cache/archive/7a/7a6dd71bcda4803d6b89612706a17b8816e1acd5dd9bf1bec29cf748f3b60008
==> Fetching https://mirror.spack.io/_source-cache/archive/1a/1ae14fb3a54ae8e0faed20801970255b279eee9e5ac624891ab5d29727f0bc04
==> Fetching https://mirror.spack.io/_source-cache/archive/11/113705d5333ef0d0ad3eb136a85404ba6bd1cc524dece5ce902c536aa2e29903
==> Fetching https://mirror.spack.io/_source-cache/archive/41/4152a780b3cc6e9643283e59093b43460196d0fea9302d8c93b2496f6679f4e4
==> Fetching https://mirror.spack.io/_source-cache/archive/1b/1b9fdb515efb09a506a01e1eb307b1464455f5ca63d6c193db3a3da371ab3220
==> Adding package nasm@2.15.05 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/91/9182a118244b058651c576baa9d0366ee05983c4d4ae1d9ddd3236a9f2304997.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/ac/ac9f315d204afa6b99ceefa1fe46d4eed2b8a23c7315d32d33c0f378d930e950
==> Adding package ncurses@6.4 to mirror
==> Fetching https://ftp.gnu.org/gnu/ncurses/ncurses-6.4.tar.gz
==> Adding package ninja@1.11.1 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/31/31747ae633213f1eda3842686f83c2aa1412e0f5691d1c14dbbcc67fe7400cea.tar.gz
==> Adding package openssl@1.1.1t to mirror
==> Fetching http://www.openssl.org/source/openssl-1.1.1t.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/3f/3fdcf2d1e47c34f3a012f23306322c5a35cad55b180c9b6fb34537b55884645c
==> Adding package pango@1.50.13 to mirror
==> Fetching http://ftp.gnome.org/pub/GNOME/sources/pango/1.50/pango-1.50.13.tar.xz
==> Adding package pcre@8.45 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/4d/4dae6fdcd2bb0bb6c37b5f97c33c2be954da743985369cddac3546e3218bffb8.tar.bz2
==> Adding package pcre2@10.42 to mirror
==> Fetching https://github.com/PCRE2Project/pcre2/releases/download/pcre2-10.42/pcre2-10.42.tar.bz2
==> Adding package perl@5.36.0 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/e2/e26085af8ac396f62add8a533c3a0ea8c8497d836f0689347ac5abd7b7a4e00a.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/9d/9da50e155df72bce55cb69f51f1dbb4b62d23740fb99f6178bb27f22ebdf8a46.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/8c/8cf4302ca8b480c60ccdcaa29ec53d9d50a71d4baf469ac8c6fca00ca31e58a2
==> Fetching https://mirror.spack.io/_source-cache/archive/3b/3bbd7d6f9933d80b9571533867b444c6f8f5a1ba0575bfba1fba4db9d885a71a
==> Fetching https://mirror.spack.io/_source-cache/archive/0e/0eac10ed90aeb0459ad8851f88081d439a4e41978e586ec743069e8b059370ac
==> Adding package perl-data-dumper@2.173 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/69/697608b39330988e519131be667ff47168aaaaf99f06bd2095d5b46ad05d76fa.tar.gz
==> Adding package perl-encode-locale@1.05 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/17/176fa02771f542a4efb1dbc2a4c928e8f4391bf4078473bd6040d8f11adb0ec1.tar.gz
==> Adding package perl-extutils-config@0.008 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/ae/ae5104f634650dce8a79b7ed13fb59d67a39c213a6776cfdaa3ee749e62f1a8c.tar.gz
==> Adding package perl-extutils-helpers@0.026 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/de/de901b6790a4557cf4ec908149e035783b125bf115eb9640feb1bc1c24c33416.tar.gz
==> Adding package perl-extutils-installpaths@0.012 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/84/84735e3037bab1fdffa3c2508567ad412a785c91599db3c12593a50a1dd434ed.tar.gz
==> Adding package perl-file-listing@6.04 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/1e/1e0050fcd6789a2179ec0db282bf1e90fb92be35d1171588bd9c47d52d959cf5.tar.gz
==> Adding package perl-html-parser@3.72 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/ec/ec28c7e1d9e67c45eca197077f7cdc41ead1bb4c538c7f02a3296a4bb92f608b.tar.gz
==> Adding package perl-html-tagset@3.20 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/ad/adb17dac9e36cd011f5243881c9739417fd102fce760f8de4e9be4c7131108e2.tar.gz
==> Adding package perl-http-cookies@6.10 to mirror
==> Fetching http://search.cpan.org/CPAN/authors/id/O/OA/OALDERS/HTTP-Cookies-6.10.tar.gz
==> Adding package perl-http-daemon@6.01 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/43/43fd867742701a3f9fcc7bd59838ab72c6490c0ebaf66901068ec6997514adc2.tar.gz
==> Adding package perl-http-date@6.02 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/e8/e8b9941da0f9f0c9c01068401a5e81341f0e3707d1c754f8e11f42a7e629e333.tar.gz
==> Adding package perl-http-message@6.44 to mirror
==> Fetching http://search.cpan.org/CPAN/authors/id/O/OA/OALDERS/HTTP-Message-6.44.tar.gz
==> Adding package perl-http-negotiate@6.01 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/1c/1c729c1ea63100e878405cda7d66f9adfd3ed4f1d6cacaca0ee9152df728e016.tar.gz
==> Adding package perl-io-html@1.004 to mirror
==> Fetching http://search.cpan.org/CPAN/authors/id/C/CJ/CJM/IO-HTML-1.004.tar.gz
==> Adding package perl-libwww-perl@6.68 to mirror
==> Fetching http://search.cpan.org/CPAN/authors/id/O/OA/OALDERS/libwww-perl-6.68.tar.gz
==> Adding package perl-lwp-mediatypes@6.02 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/18/18790b0cc5f0a51468495c3847b16738f785a2d460403595001e0b932e5db676.tar.gz
==> Adding package perl-module-build@0.4232 to mirror
==> Fetching http://search.cpan.org/CPAN/authors/id/L/LE/LEONT/Module-Build-0.4232.tar.gz
==> Adding package perl-module-build-tiny@0.039 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/7d/7d580ff6ace0cbe555bf36b86dc8ea232581530cbeaaea09bccb57b55797f11c.tar.gz
==> Adding package perl-net-http@6.22 to mirror
==> Fetching http://search.cpan.org/CPAN/authors/id/O/OA/OALDERS/Net-HTTP-6.22.tar.gz
==> Adding package perl-test-needs@0.002010 to mirror
==> Fetching https://search.cpan.org/CPAN/authors/id/H/HA/HAARG/Test-Needs-0.002010.tar.gz
==> Adding package perl-try-tiny@0.28 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/f1/f1d166be8aa19942c4504c9111dade7aacb981bc5b3a2a5c5f6019646db8c146.tar.gz
==> Adding package perl-uri@1.72 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/35/35f14431d4b300de4be1163b0b5332de2d7fbda4f05ff1ed198a8e9330d40a32.tar.gz
==> Adding package perl-www-robotrules@6.02 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/46/46b502e7a288d559429891eeb5d979461dd3ecc6a5c491ead85d165b6e03a51e.tar.gz
==> Adding package perl-xml-parser@2.44 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/1a/1ae9d07ee9c35326b3d9aad56eae71a6730a73a116b9fe9e8a4758b7cc033216.tar.gz
==> Adding package pigz@2.7 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/d2/d2045087dae5e9482158f1f1c0f21c7d3de6f7cdc7cc5848bdabda544e69aa58.tar.gz
==> Adding package pixman@0.42.2 to mirror
==> Fetching https://cairographics.org/releases/pixman-0.42.2.tar.gz
==> Adding package pkgconf@1.8.0 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/ef/ef9c7e61822b7cb8356e6e9e1dca58d9556f3200d78acab35e4347e9d4c2bbaf.tar.xz
==> Adding package py-mako@1.2.2 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/37/3724869b363ba630a272a5f89f68c070352137b8fd1757650017b7e06fda163f.tar.gz
==> Adding package py-markupsafe@2.1.1 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/7f/7f91197cc9e48f989d12e4e6fbc46495c446636dfc81b9ccf50bb0ec74b91d4b.tar.gz
==> Adding package py-pip@23.0 to mirror
==> Fetching https://files.pythonhosted.org/packages/py3/p/pip/pip-23.0-py3-none-any.whl
==> Adding package py-setuptools@67.6.0 to mirror
==> Fetching https://files.pythonhosted.org/packages/py3/s/setuptools/setuptools-67.6.0-py3-none-any.whl
==> Adding package py-wheel@0.37.1 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/4b/4bdcd7d840138086126cd09254dc6195fb4fc6f01c050a1d7236f2630db1d22a
==> Adding package python@3.10.10 to mirror
==> Fetching https://www.python.org/ftp/python/3.10.10/Python-3.10.10.tgz
==> Adding package randrproto@1.5.0 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/8f/8f8a716d6daa6ba05df97d513960d35a39e040600bf04b313633f11679006fab.tar.gz
==> Adding package re2c@2.2 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/0f/0fc45e4130a8a555d68e230d1795de0216dfe99096b61b28e67c86dfd7d86bda.tar.xz
==> Adding package readline@8.2 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/3f/3feb7171f16a84ee82ca18a36d7b9be109a52c04f492a053331d7d1095007c35.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/bb/bbf97f1ec40a929edab5aa81998c1e2ef435436c597754916e6a5868f273aff7
==> Fetching https://mirror.spack.io/_source-cache/archive/68/682a465a68633650565c43d59f0b8cdf149c13a874682d3c20cb4af6709b9144
==> Fetching https://mirror.spack.io/_source-cache/archive/e5/e55be055a68cb0719b0ccb5edc9a74edcc1d1f689e8a501525b3bc5ebad325dc
==> Fetching https://mirror.spack.io/_source-cache/archive/d8/d8e5e98933cf5756f862243c0601cb69d3667bb33f2c7b751fe4e40b2c3fd069
==> Fetching https://mirror.spack.io/_source-cache/archive/36/36b0febff1e560091ae7476026921f31b6d1dd4c918dcb7b741aa2dad1aec8f7
==> Fetching https://mirror.spack.io/_source-cache/archive/94/94ddb2210b71eb5389c7756865d60e343666dfb722c85892f8226b26bb3eeaef
==> Fetching https://mirror.spack.io/_source-cache/archive/b1/b1aa3d2a40eee2dea9708229740742e649c32bb8db13535ea78f8ac15377394c
==> Fetching https://mirror.spack.io/_source-cache/archive/9a/9ac1b3ac2ec7b1bf0709af047f2d7d2a34ccde353684e57c6b47ebca77d7a376
==> Fetching https://mirror.spack.io/_source-cache/archive/87/8747c92c35d5db32eae99af66f17b384abaca961653e185677f9c9a571ed2d58
==> Fetching https://mirror.spack.io/_source-cache/archive/9e/9e43aa93378c7e9f7001d8174b1beb948deefa6799b6f581673f465b7d9d4780
==> Fetching https://mirror.spack.io/_source-cache/archive/f9/f925683429f20973c552bff6702c74c58c2a38ff6e5cf305a8e847119c5a6b64
==> Fetching https://mirror.spack.io/_source-cache/archive/ca/ca159c83706541c6bbe39129a33d63bbd76ac594303f67e4d35678711c51b753
==> Fetching https://mirror.spack.io/_source-cache/archive/1a/1a79bbb6eaee750e0d6f7f3d059b30a45fc54e8e388a8e05e9c3ae598590146f
==> Fetching https://mirror.spack.io/_source-cache/archive/39/39e304c7a526888f9e112e733848215736fb7b9d540729b9e31f3347b7a1e0a5
==> Fetching https://mirror.spack.io/_source-cache/archive/ec/ec41bdd8b00fd884e847708513df41d51b1243cecb680189e31b7173d01ca52f
==> Fetching https://mirror.spack.io/_source-cache/archive/45/4547b906fb2570866c21887807de5dee19838a60a1afb66385b272155e4355cc
==> Fetching https://mirror.spack.io/_source-cache/archive/87/877788f9228d1a9907a4bcfe3d6dd0439c08d728949458b41208d9bf9060274b
==> Warning: Error while fetching readline@8.2
  All fetchers failed for spack-stage-d0z8q77a
==> Adding package recordproto@1.14.2 to mirror
==> Fetching https://mirrors.ircam.fr/pub/x.org/individual/proto/recordproto-1.14.2.tar.gz
==> Adding package renderproto@0.11.1 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/a0/a0a4be3cad9381ae28279ba5582e679491fc2bec9aab8a65993108bf8dbce5fe.tar.gz
==> Adding package ruby@3.1.0 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/50/50a0504c6edcb4d61ce6b8cfdbddaa95707195fab0ecd7b5e92654b2a9412854.tar.gz
==> Fetching https://mirror.spack.io/_source-cache/archive/df/df68841998b7fd098a9517fe971e97890be0fc93bbe1b2a1ef63ebdea3111c80
==> Adding package rust@1.65.0 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/58/5828bb67f677eabf8c384020582b0ce7af884e1c84389484f7f8d00dd82c0038.tar.gz
==> Fetching https://static.rust-lang.org/dist/rust-1.65.0-x86_64-unknown-linux-gnu.tar.gz
==> Adding package shared-mime-info@1.9 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/5c/5c0133ec4e228e41bdf52f726d271a2d821499c2ab97afd3aa3d6cf43efcdc83.tar.xz
==> Adding package sqlite@3.40.1 to mirror
==> Fetching https://www.sqlite.org/2022/sqlite-autoconf-3400100.tar.gz
==> Adding package tar@1.34 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/03/03d908cf5768cfe6b7ad588c921c6ed21acabfb2b79b788d1330453507647aed.tar.gz
==> Adding package texinfo@7.0 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/92/9261d4ee11cdf6b61895e213ffcd6b746a61a64fe38b9741a3aaa73125b35170.tar.gz
==> Adding package unzip@6.0 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/03/036d96991646d0449ed0aa952e4fbe21b476ce994abc276e49d30e686708bd37.tar.gz
==> Adding package util-linux-uuid@2.36.2 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/f5/f5dbe79057e7d68e1a46fc04083fc558b26a49499b1b3f50e4f4893150970463.tar.gz
==> Adding package util-macros@1.19.3 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/0f/0f812e6e9d2786ba8f54b960ee563c0663ddbe2434bf24ff193f5feab1f31971.tar.bz2
==> Adding package vim@9.0.0045 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/59/594a31e96e3eda07a358db305de939ca749693b4684de9e027bfa70311b1994d.tar.gz
==> Adding package xcb-proto@1.14.1 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/f0/f04add9a972ac334ea11d9d7eb4fc7f8883835da3e4859c9afa971efdf57fcc3.tar.xz
==> Adding package xextproto@7.3.0 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/1b/1b1bcdf91221e78c6c33738667a57bd9aaa63d5953174ad8ed9929296741c9f5.tar.gz
==> Adding package xkbcomp@1.4.4 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/15/159fba6b62ef4a3fb16ef7fc4eb4fc26f3888652471ceb604c495783dda020bc.tar.gz
==> Adding package xkbdata@1.0.1 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/5b/5b43ca5219cd4022a158a8d4bfa30308ea5e16c9b5270a64589ebfe7f875f430.tar.gz
==> Adding package xmlto@0.0.28 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/2f/2f986b7c9a0e9ac6728147668e776d405465284e13c74d4146c9cbc51fd8aad3.tar.gz
==> Adding package xproto@7.0.31 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/6d/6d755eaae27b45c5cc75529a12855fed5de5969b367ed05003944cf901ed43c7.tar.gz
==> Adding package xrandr@1.5.0 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/dd/ddfe8e7866149c24ccce8e6aaa0623218ae19130c2859cadcaa4228d8bb4a46d.tar.gz
==> Adding package xtrans@1.3.5 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/b7/b7a577c1b6c75030145e53b4793db9c88f9359ac49e7d771d4385d21b3e5945d.tar.gz
==> Adding package xz@5.4.1 to mirror
==> Fetching https://prdownloads.sourceforge.net/lzmautils/files/xz-5.4.1.tar.bz2
==> Adding package zlib@1.2.13 to mirror
==> Fetching https://mirror.spack.io/_source-cache/archive/b3/b3a24de97a8fdbc835b9833169501030b8977031bcb54b3b3ac13740f846ab30.tar.gz
==> Adding package zstd@1.5.4 to mirror
==> Warning: Error while fetching zstd@1.5.4
  All fetchers failed for spack-stage-zstd-1.5.4-fcoqzia2hmo7w2ydmmagjiatpskgp7jf
==> Summary for mirror in /local/tools/os/spack/pkgs-mirror
==> Archive stats:
    0    already present
    160  added
    5    failed to fetch.
==> Error: Failed downloads:
expat@2.5.0  intltool@0.51.0  zstd@1.5.4  readline@8.2  inputproto@2.3.2
```

提示有失败。可以将传输错误的临时文件删掉，重新执行试试。完成mirror操作之后，将/local/tools/os/spack/pkgs-mirror与/home/centos/.spack(这个目录缓存好了spack bootstrap)目录传到centos7-9-offline机器，配置mirror信息，
```bash
[centos@centos7-9-offline ~]$ spack mirror add local_filesystem file:///nfs/tools/os/spack/pkgs-mirror
[centos@centos7-9-offline ~]$ cat ~/.spack/mirrors.yaml
mirrors:
  local_filesystem: file:///nfs/tools/os/spack/pkgs-mirror
```

这样，spack在离线环境就可以使用mirror过来的目录安装了
```bash
[centos@centos7-9-offline ~]$ spack install vim %gcc@12.2.0 +gtk +gui +lua +perl +python +ruby +x +cscope
```

验证



[Spack Mirrors](https://spack.readthedocs.io/en/latest/mirrors.html)