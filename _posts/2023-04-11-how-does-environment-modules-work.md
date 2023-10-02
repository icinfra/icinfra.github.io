---
layout: post
title: Environment Modules是如何工作的？
date: 2023-04-11 12:35:20+0800
description: 
tags: modules
giscus_comments: true
categories: icenv
---

# 前言
Environment Modules在我们芯片研发已经耳熟能详了，那，它是如何工作的呢？
很多人对这个比较陌生，说为什么我一个.cshrc只能够在c shell里source，而一个modulefile modulename能够在多种shell环境中使用。

# 目的
本文通过对一个已经初始化好的Environment Modules环境的**module load**步骤分析，来看它是如何工作的。

# 解析

## bash环境
我们拿一个初始化好的环境，从命令开始，一步一步扒。

首先来看module命令，它是一个bash函数，它调用了bash函数_module_raw：
```bash
[centos@computing-server-133 ~]$ echo $0
-bash
[centos@computing-server-133 ~]$ type module
module is a function
module () 
{ 
    local _mlredir=1;
    if [ -n "${MODULES_REDIRECT_OUTPUT+x}" ]; then
        if [ "$MODULES_REDIRECT_OUTPUT" = '0' ]; then
            _mlredir=0;
        else
            if [ "$MODULES_REDIRECT_OUTPUT" = '1' ]; then
                _mlredir=1;
            fi;
        fi;
    fi;
    case " $@ " in 
        *' --no-redirect '*)
            _mlredir=0
        ;;
        *' --redirect '*)
            _mlredir=1
        ;;
    esac;
    if [ $_mlredir -eq 0 ]; then
        _module_raw "$@";
    else
        _module_raw "$@" 2>&1;
    fi
}
```

\_module_raw也是bash函数，它调用了tclsh程序，读入tcl脚本以及参数，生成了**更改环境**的语句，再将其作为eval的参数，对当前shell做出更改。
```bash
[centos@computing-server-133 ~]$ type _module_raw
_module_raw is a function
_module_raw () 
{ 
    eval "$(/nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/tcl-8.6.12-5rkwrb3btdklgrkshepg5cctyigmfm37/bin/tclsh '/nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/environment-modules-5.2.0-upsh6wzxsg7airzqpjayrvoapfrtgttp/libexec/modulecmd.tcl' bash "$@")";
    _mlstatus=$?;
    return $_mlstatus
}
```

我们以load tcl-8.6.12-gcc-12.2.0-5rkwrb3这个modulefile试下，
```bash
[centos@computing-server-133 ~]$ ml show tcl-8.6.12-gcc-12.2.0-5rkwrb3
-------------------------------------------------------------------
/nfs/tools/os/spack/share/spack/modules/linux-centos7-x86_64_v4/tcl-8.6.12-gcc-12.2.0-5rkwrb3:

module-whatis   {Tcl (Tool Command Language) is a very powerful but easy to learn dynamic programming language, suitable for a very wide range of uses, including web and desktop applications, networking, administration, testing and many more. Open source and business-friendly, Tcl is a mature yet evolving language that is truly cross platform, easily deployed and highly extensible.}
module          load zlib-1.2.13-gcc-12.2.0-pobtkn4
prepend-path    --delim : PATH /nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/tcl-8.6.12-5rkwrb3btdklgrkshepg5cctyigmfm37/bin
prepend-path    --delim : MANPATH /nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/tcl-8.6.12-5rkwrb3btdklgrkshepg5cctyigmfm37/man
prepend-path    --delim : MANPATH /nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/tcl-8.6.12-5rkwrb3btdklgrkshepg5cctyigmfm37/share/man
prepend-path    --delim : PKG_CONFIG_PATH /nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/tcl-8.6.12-5rkwrb3btdklgrkshepg5cctyigmfm37/lib/pkgconfig
prepend-path    --delim : CMAKE_PREFIX_PATH /nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/tcl-8.6.12-5rkwrb3btdklgrkshepg5cctyigmfm37/.
setenv          TCL_LIBRARY /nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/tcl-8.6.12-5rkwrb3btdklgrkshepg5cctyigmfm37/lib/tcl8.6
-------------------------------------------------------------------[centos@computing-server-133 ~]$ ml
No Modulefiles Currently Loaded.
[centos@computing-server-133 ~]$ /nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/tcl-8.6.12-5rkwrb3btdklgrkshepg5cctyigmfm37/bin/tclsh '/nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/environment-modules-5.2.0-upsh6wzxsg7airzqpjayrvoapfrtgttp/libexec/modulecmd.tcl' bash load tcl-8.6.12-gcc-12.2.0-5rkwrb3
PATH=/nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/tcl-8.6.12-5rkwrb3btdklgrkshepg5cctyigmfm37/bin:/nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/environment-modules-5.2.0-upsh6wzxsg7airzqpjayrvoapfrtgttp/bin:/nfs/tools/os/spack/bin:/opt/ibm/lsfsuite/lsf/10.1/linux2.6-glibc2.3-x86_64/etc:/opt/ibm/lsfsuite/lsf/10.1/linux2.6-glibc2.3-x86_64/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/centos/.local/bin:/home/centos/bin; export PATH;
__MODULES_SHARE_MANPATH=:1; export __MODULES_SHARE_MANPATH;
MANPATH=/nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/tcl-8.6.12-5rkwrb3btdklgrkshepg5cctyigmfm37/share/man:/nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/tcl-8.6.12-5rkwrb3btdklgrkshepg5cctyigmfm37/man:/nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/zlib-1.2.13-pobtkn4lnv467woi4cerdauysxm42mn2/share/man:/opt/ibm/lsfsuite/lsf/10.1/man:; export MANPATH;
__MODULES_LMPREREQ=tcl-8.6.12-gcc-12.2.0-5rkwrb3\&zlib-1.2.13-gcc-12.2.0-pobtkn4; export __MODULES_LMPREREQ;
_LMFILES_=/nfs/tools/os/spack/share/spack/modules/linux-centos7-x86_64_v4/zlib-1.2.13-gcc-12.2.0-pobtkn4:/nfs/tools/os/spack/share/spack/modules/linux-centos7-x86_64_v4/tcl-8.6.12-gcc-12.2.0-5rkwrb3; export _LMFILES_;
LOADEDMODULES=zlib-1.2.13-gcc-12.2.0-pobtkn4:tcl-8.6.12-gcc-12.2.0-5rkwrb3; export LOADEDMODULES;
CMAKE_PREFIX_PATH=/nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/tcl-8.6.12-5rkwrb3btdklgrkshepg5cctyigmfm37/.:/nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/zlib-1.2.13-pobtkn4lnv467woi4cerdauysxm42mn2/.; export CMAKE_PREFIX_PATH;
TCL_LIBRARY=/nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/tcl-8.6.12-5rkwrb3btdklgrkshepg5cctyigmfm37/lib/tcl8.6; export TCL_LIBRARY;
__MODULES_LMTAG=zlib-1.2.13-gcc-12.2.0-pobtkn4\&auto-loaded; export __MODULES_LMTAG;
PKG_CONFIG_PATH=/nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/tcl-8.6.12-5rkwrb3btdklgrkshepg5cctyigmfm37/lib/pkgconfig:/nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/zlib-1.2.13-pobtkn4lnv467woi4cerdauysxm42mn2/lib/pkgconfig; export PKG_CONFIG_PATH;
test 0;
[centos@computing-server-133 ~]$ which tclsh
/usr/bin/tclsh
```
可以看到它生成了的语句，包括了modulefile里显式对PATH、MANPATH、PKG_CONFIG_PATH、CMAKE_PREFIX_PATH等环境变量的修改，还包括了用户未定义的，对Environment Modules工具自身使用的变量做了修改。
执行完查询后，tclsh并没有被加载上。需要将这些语句传入eval，才能在当前shell环境生效，

```bash
[centos@computing-server-133 ~]$ eval `/nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/tcl-8.6.12-5rkwrb3btdklgrkshepg5cctyigmfm37/bin/tclsh '/nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/environment-modules-5.2.0-upsh6wzxsg7airzqpjayrvoapfrtgttp/libexec/modulecmd.tcl' bash load tcl-8.6.12-gcc-12.2.0-5rkwrb3`
Loading tcl-8.6.12-gcc-12.2.0-5rkwrb3
  Loading requirement: zlib-1.2.13-gcc-12.2.0-pobtkn4
[centos@computing-server-133 ~]$ which tclsh
/nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/tcl-8.6.12-5rkwrb3btdklgrkshepg5cctyigmfm37/bin/tclsh
```


## c shell环境

module是一个alias，同样地，它将生成的更改环境的语句传入eval，使得环境修改，
```bash
[centos@computing-server-133 ~]$ echo $0
csh
[centos@computing-server-133 ~]$ which module
module: 	 aliased to set _prompt=$prompt:q; set prompt=""; eval "`/nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/tcl-8.6.12-5rkwrb3btdklgrkshepg5cctyigmfm37/bin/tclsh '/nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/environment-modules-5.2.0-upsh6wzxsg7airzqpjayrvoapfrtgttp/libexec/modulecmd.tcl' csh !*:q`"; set _exit="$status"; set prompt=$_prompt:q; unset _prompt; test 0 = $_exit
```

我们以load tcl-8.6.12-gcc-12.2.0-5rkwrb3这个modulefile试下，
```bash
[centos@computing-server-133 ~]$ /nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/tcl-8.6.12-5rkwrb3btdklgrkshepg5cctyigmfm37/bin/tclsh '/nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/environment-modules-5.2.0-upsh6wzxsg7airzqpjayrvoapfrtgttp/libexec/modulecmd.tcl' csh load tcl-8.6.12-gcc-12.2.0-5rkwrb3
setenv PATH /nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/tcl-8.6.12-5rkwrb3btdklgrkshepg5cctyigmfm37/bin:/opt/ibm/lsfsuite/lsf/10.1/linux2.6-glibc2.3-x86_64/etc:/opt/ibm/lsfsuite/lsf/10.1/linux2.6-glibc2.3-x86_64/bin:/nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/environment-modules-5.2.0-upsh6wzxsg7airzqpjayrvoapfrtgttp/bin:/nfs/tools/os/spack/bin:/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin:/home/centos/.local/bin:/home/centos/bin;
setenv __MODULES_SHARE_MANPATH :1;
setenv MANPATH /nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/tcl-8.6.12-5rkwrb3btdklgrkshepg5cctyigmfm37/share/man:/nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/tcl-8.6.12-5rkwrb3btdklgrkshepg5cctyigmfm37/man:/nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/zlib-1.2.13-pobtkn4lnv467woi4cerdauysxm42mn2/share/man:/opt/ibm/lsfsuite/lsf/10.1/man:;
setenv __MODULES_LMPREREQ tcl-8.6.12-gcc-12.2.0-5rkwrb3\&zlib-1.2.13-gcc-12.2.0-pobtkn4;
setenv _LMFILES_ /nfs/tools/os/spack/share/spack/modules/linux-centos7-x86_64_v4/zlib-1.2.13-gcc-12.2.0-pobtkn4:/nfs/tools/os/spack/share/spack/modules/linux-centos7-x86_64_v4/tcl-8.6.12-gcc-12.2.0-5rkwrb3;
setenv LOADEDMODULES zlib-1.2.13-gcc-12.2.0-pobtkn4:tcl-8.6.12-gcc-12.2.0-5rkwrb3;
setenv CMAKE_PREFIX_PATH /nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/tcl-8.6.12-5rkwrb3btdklgrkshepg5cctyigmfm37/.:/nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/zlib-1.2.13-pobtkn4lnv467woi4cerdauysxm42mn2/.;
setenv TCL_LIBRARY /nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/tcl-8.6.12-5rkwrb3btdklgrkshepg5cctyigmfm37/lib/tcl8.6;
setenv __MODULES_LMTAG zlib-1.2.13-gcc-12.2.0-pobtkn4\&auto-loaded;
setenv PKG_CONFIG_PATH /nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/tcl-8.6.12-5rkwrb3btdklgrkshepg5cctyigmfm37/lib/pkgconfig:/nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/zlib-1.2.13-pobtkn4lnv467woi4cerdauysxm42mn2/lib/pkgconfig;
test 0;
Loading tcl-8.6.12-gcc-12.2.0-5rkwrb3
  Loading requirement: zlib-1.2.13-gcc-12.2.0-pobtkn4
[centos@computing-server-133 ~]$ which tclsh
/usr/bin/tclsh
```

可以看到它生成了的语句，包括了modulefile里显式对PATH、MANPATH、PKG_CONFIG_PATH、CMAKE_PREFIX_PATH等环境变量的修改，还包括了用户未定义的，对Environment Modules工具自身使用的变量做了修改。
执行完查询后，tclsh并没有被加载上。需要将这些语句传入eval，才能在当前shell环境生效，
```bash
[centos@computing-server-133 ~]$ eval `/nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/tcl-8.6.12-5rkwrb3btdklgrkshepg5cctyigmfm37/bin/tclsh '/nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/environment-modules-5.2.0-upsh6wzxsg7airzqpjayrvoapfrtgttp/libexec/modulecmd.tcl' csh load tcl-8.6.12-gcc-12.2.0-5rkwrb3`
Loading tcl-8.6.12-gcc-12.2.0-5rkwrb3
  Loading requirement: zlib-1.2.13-gcc-12.2.0-pobtkn4
[centos@computing-server-133 ~]$ which tclsh
/nfs/tools/os/spack/opt/spack/linux-centos7-x86_64_v4/gcc-12.2.0/tcl-8.6.12-5rkwrb3btdklgrkshepg5cctyigmfm37/bin/tclsh
```

# 总结
上述介绍了Environment Modules对环境的修改的原理，主要是先对tcl语句的modulefile解析，生成对应shell类型的修改语句，再通过eval语句来完成对当前shell的环境修改。

真正难得是它如何生成对环境修改的语句。后续有时间再深入探讨下。

# TODO
如何解析modulefile并生成环境更改语句。