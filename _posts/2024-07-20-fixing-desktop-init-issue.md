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
从[t]csh手册
![image](https://github.com/user-attachments/assets/acef7ad2-6b8e-45c2-b86b-ba3b76d09014)

可以看到，其初始化流程

![C Shell初始化流程 drawio](https://github.com/user-attachments/assets/f9e729c1-34af-4aa6-bf63-336fd41c68bf)


经定位，是.cshrc的这段代码存在，导致桌面初始化异常。
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
用户需要在.cshrc文件里加载各种各样的工具与库路径，以期望一开桌面/terminal，所需工具立即可用。但在桌面初始化时却导致了失败。

因此，管理员需要从.cshrc入手，检测到桌面启动时，就立即终止往下source。也可以将这部分公共代码抽出来，放到公共cshrc里，供用户在.cshrc第一行进行source。

# 解决
.cshrc样例
```csh
# For init desktop. Here we assume "icinfra-cn-" is the desktop hostname's prefix.
if ($?SHLVL && $SHLVL == 1 && ! $?SSH_TTY && ("$HOSTNAME" =~ icinfra-cn-*)) then
    exit
endif

# For init environment modules.
source /tools/oss/spack/opt/spack/linux-almalinux8-x86_64_v4/gcc-8.5.0/environment-modules-5.4.0-uiudomq3q3xmgulxntqouamwlt6krxpa/init/csh
setenv MODULEPATH /tools/oss/spack/share/spack/modules/linux-almalinux8-x86_64_v4

# For anaconda3/4.4.0
setenv PATH /tools/oss/spack/opt/spack/linux-almalinux8-x86_64_v4/gcc-8.5.0/anaconda3-4.4.0-zpdh67mbu2fubypa6uqtgkrl5syel2hz/bin:$PATH
if ($?LD_LIBRARY_PATH) then
    setenv LD_LIBRARY_PATH /tools/oss/spack/opt/spack/linux-almalinux8-x86_64_v4/gcc-8.5.0/anaconda3-4.4.0-zpdh67mbu2fubypa6uqtgkrl5syel2hz/lib:$LD_LIBRARY_PATH
else
    setenv LD_LIBRARY_PATH /tools/oss/spack/opt/spack/linux-almalinux8-x86_64_v4/gcc-8.5.0/anaconda3-4.4.0-zpdh67mbu2fubypa6uqtgkrl5syel2hz/lib
endif
```

![image](https://github.com/user-attachments/assets/036f952d-7544-4257-8699-e00a0fc33e6a)
