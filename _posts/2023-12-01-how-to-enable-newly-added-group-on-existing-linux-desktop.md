---
layout: post
title:  
date: 2023-11-30 11:00+0800
description: 
tags: group
giscus_comments: true
categories: icenv
---

# 场景说明
令芯片设计环境的研发人员经常头疼的一件事，维护完群组后，无法在Linux桌面生效。支持人员频繁接到这样的case，只能建议ta：
- run 'newgrp newly-added-group-name', or
- logout the vnc and login again.

在遵循Linux桌面设计范式的前提下，本文我们尽量做到让用户无感地让新加群组生效。

# 环境说明
CentOS 6.10, Gnome, Krusader

# 效果演示
定制完毕后，
- **新开terminal，新群组就生效了**。无需用户做任何操作。
- **在新开terminal里打开krusader，可以浏览与编辑文件**。

<img width="1920" alt="image" src="https://github.com/icinfra/icinfra.github.io/assets/32032219/69c5e444-1905-4b90-9ea4-3282f15d20ec">

# 代码示例
## 新terminal生效新群组
用户只需要运行一次本脚本即可。也可以管理员将~/.flush_groups.csh文件放至NFS，用户家目录.cshrc文件去source即可。

```bash
#!/bin/bash

# Author:      wanlinwang
# Date  :      Nov 30, 2023
# Description: This script is to make newly added group(s) available in newly created gnome-terminal on CentOS 6.10. Run me once.


# Update .cshrc.
CSHRC=~/.cshrc
if [ ! -f "$CSHRC" ]; then
    touch "$CSHRC"
fi
# The line to add if it doesn't exist
LINE="source ~/.flush_groups.csh"
if ! grep -Fxq "$LINE" "$CSHRC"; then
    # If the line doesn't exist, add it to the file
    echo "$LINE" >> "$CSHRC"
fi


# Add ~/.flush_groups.csh
cat > ~/.flush_groups.csh << 'EOF'
#!/bin/csh

# Writen by wanlinwang.
# Date: Dec 1, 2023
# Description: 支持自动将新增群组刷新到新terminal中，对研发人员透明。提升研发人员效率，降低支持工作量。

if ( ! $?new_grp_array) then

    # 获取当前用户在当前session的主群组以及全部群组
    setenv primary_group  `id -gn`
    set    current_groups=`sh -c 'id -Gn 2> /dev/null'`
    
    # 获取当前用户最新的全部群组
    set login_groups=`sh -c 'id -Gn $USER 2> /dev/null'`
    
    # 创建临时文件，并将群组信息写入临时文件
    set temp1=`mktemp`
    set temp2=`mktemp`
    echo $current_groups | tr ' ' '\n' | sort > $temp1
    echo $login_groups | tr ' ' '\n' | sort > $temp2
    
    # 使用comm比较文件内容
    #set new_group=`comm -13 $temp1 $temp2`
    setenv new_grp_array `comm -13 $temp1 $temp2 | tr '\n' ' '`
    
    # 删除临时文件
    rm -f $temp1 $temp2
endif

# iterate new_grp_array
if ("$new_grp_array" != "") then
    set new_group=`echo $new_grp_array | awk '{print $1}'`
    setenv new_grp_array `echo $new_grp_array | awk '{$1=""; print $0}' | sed 's/^[ \t]*//'`

    if ("$new_group" != "") then
        # 切换群组，使其生效
        exec newgrp $new_group
    endif
else
    set current_group=`id -gn`
    if ( $?primary_group ) then
        if ( "$primary_group" != "$current_group" ) then
            exec newgrp $primary_group
        endif
    endif
    unset current_group
    unsetenv primary_group
endif

unsetenv new_grp_array

EOF

```

## krusader
按需，需要联网。如果离线环境则手动下载回来安装。
```bash
# Install krusader, a file manager. If you want to use this tool, please contact your system administrator to install.
sudo yum install epel-release
sudo yum localinstall http://rpms.plnet.rs/plnet-centos6-x86_64/RPMS.plnet-compiled/krusader-2.3.0-0.1.beta1.el6.x86_64.rpm
```
