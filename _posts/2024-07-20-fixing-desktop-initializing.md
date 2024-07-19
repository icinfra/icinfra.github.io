---
layout: post
title:  解决桌面初始化问题
date:   2024-07-20 07:25:00+0800
description: 
tags: desktop
giscus_comments: true
categories: icenv
---


# 问题
启动vnc桌面，提示问题

<img width="1240" alt="image" src="https://github.com/user-attachments/assets/aa102013-88a5-44f8-8eef-2c904d830b73">


# 定位
定位到，是.cshrc的这段代码存在，导致桌面初始化异常。
```csh
[wanlin.wang@icinfra-cn-172-16-0-115 ~]$ cat .cshrc
...部分省略...
# Environment for anaconda3/4.4.0
setenv PATH /tools/oss/spack/opt/spack/linux-almalinux8-x86_64_v4/gcc-8.5.0/anaconda3-4.4.0-zpdh67mbu2fubypa6uqtgkrl5syel2hz/bin:$PATH
if ($?LD_LIBRARY_PATH) then
    setenv LD_LIBRARY_PATH /tools/oss/spack/opt/spack/linux-almalinux8-x86_64_v4/gcc-8.5.0/anaconda3-4.4.0-zpdh67mbu2fubypa6uqtgkrl5syel2hz/lib:$LD_LIBRARY_PATH
else
    setenv LD_LIBRARY_PATH /tools/oss/spack/opt/spack/linux-almalinux8-x86_64_v4/gcc-8.5.0/anaconda3-4.4.0-zpdh67mbu2fubypa6uqtgkrl5syel2hz/lib
endif
```

# 思路
用户需要在.cshrc文件里加载各种各样的工具与库路径，以期望一开桌面/terminal，所需工具立即可用。但在桌面初始化时，却导致了失败。

因此，管理员需要从.cshrc入手，检测到桌面启动时，就立即终止往下source。也可以将这部分公共代码抽出来，放到公共cshrc里，供用户在.cshrc第一行进行source。

# 解决
```csh
# For init environment modules.
source /tools/oss/spack/opt/spack/linux-almalinux8-x86_64_v4/gcc-8.5.0/environment-modules-5.4.0-uiudomq3q3xmgulxntqouamwlt6krxpa/init/csh
setenv MODULEPATH /tools/oss/spack/share/spack/modules/linux-almalinux8-x86_64_v4

# For init desktop. Here we assume "icinfra-cn-" is the desktop hostname's prefix.
if ($?SHLVL && $SHLVL == 1 && ! $?SSH_TTY && ("$HOSTNAME" =~ icinfra-cn-*)) then
    echo "Info: exiting..." >> $log_file
    exit
endif

# Environment for anaconda3/4.4.0
setenv PATH /tools/oss/spack/opt/spack/linux-almalinux8-x86_64_v4/gcc-8.5.0/anaconda3-4.4.0-zpdh67mbu2fubypa6uqtgkrl5syel2hz/bin:$PATH
if ($?LD_LIBRARY_PATH) then
    setenv LD_LIBRARY_PATH /tools/oss/spack/opt/spack/linux-almalinux8-x86_64_v4/gcc-8.5.0/anaconda3-4.4.0-zpdh67mbu2fubypa6uqtgkrl5syel2hz/lib:$LD_LIBRARY_PATH
else
    setenv LD_LIBRARY_PATH /tools/oss/spack/opt/spack/linux-almalinux8-x86_64_v4/gcc-8.5.0/anaconda3-4.4.0-zpdh67mbu2fubypa6uqtgkrl5syel2hz/lib
endif
```
