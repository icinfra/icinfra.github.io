---
layout: post
title: 如何安装GCC？
date: 2022-09-02 22:15:00
comments: true
description: 
tags: post
categories: linux spack
---

## 安装GCC
```bash
./configure --prefix=/path/to/gcc
make
make install
```
相信大家在Linux下安装GCC都是一个难忘的回忆。笔者也经历过缺依赖，编好几个小时才发现错误。


## 重读文档
[文档](https://gcc.gnu.org/wiki/InstallingGCC)中描述，安装GCC是有几个必要依赖的，它们是GMP, MPFR and MPC。

> If it provides sufficiently recent versions, use your OS package management system to install the support libraries in standard system locations. For Debian-based systems, including Ubuntu, you should install the packages libgmp-dev, libmpfr-dev and libmpc-dev. For RPM-based systems, including Fedora and SUSE, you should install gmp-devel, mpfr-devel and libmpc-devel (or mpc-devel on SUSE) packages. The packages will install the libraries and headers in standard system directories so they can be found automatically when building GCC.
>
> Alternatively, after extracting the GCC source archive, simply run the ./contrib/download_prerequisites script in the GCC source directory. That will download the support libraries and create symlinks, causing them to be built automatically as part of the GCC build process. Set GRAPHITE_LOOP_OPT=no in the script if you want to build GCC without ISL, which is only needed for the optional Graphite loop optimizations.
>
> The difficult way, which is not recommended, is to download the sources for GMP, MPFR and MPC, then configure and install each of them in non-standard locations, then configure GCC with --with-gmp=/some/silly/path/gmp --with-mpfr=/some/silly/path/mpfr --with-mpc=/some/silly/path/mpc, then be forced to set LD_LIBRARY_PATH=/some/silly/path/gmp/lib:/some/silly/path/mpfr/lib:/some/silly/path/mpc/lib in your environment forever. This is silly and causes major problems for anyone who doesn't understand how dynamic linkers find libraries at runtime. Do not do this. If building GCC fails when using any of the --with-gmp or --with-mpfr or --with-mpc options then you probably shouldn't be using them.

如上面摘抄的所示，有三种方式可以将依赖准备好。

* 第一种是使用系统自带的包管理器，将依赖安装，这时这些依赖都将安装到系统默认的目录下；
* 第二种是执行GCC目录下的`./contrib/download_prerequisites` 脚本，将依赖的源码包下载下来，随GCC一起编译安装；
* 第三种，不推荐的方式，分别安装好，然后以`--with-gmp=/some/silly/path/gmp --with-mpfr=/some/silly/path/mpfr --with-mpc=/some/silly/path/mpc`  的这种方式指定。

## 其他自动化方法
1. 系统的包管理器安装GCC
发行版的系统，均提供了自己的包管理器。CentOS提供了yum，Ubuntu提供了apt等等。使用操作系统自带的包管理器，可以很方便地将GCC安装上。缺点是，它只能安装包管理器仓库里提供的版本，不能随心所欲。

2. 使用spack包管理器
spack包管理器是一个强大的包管理器。安装开源库是一个NP问题，靠人工解决依赖很麻烦，像spack这种提前定义好依赖关系，自动生成单向无环图，可以一键完成人工要画几小时、几天甚至无法完成的依赖关系安装。

3. easybuild包管理器
同spack一样，easybuild也是类似功能的包管理器。

## 其他案例
左工的案例 https://mp.weixin.qq.com/s/vNfM571Gxw1UUIGgehZ1hQ