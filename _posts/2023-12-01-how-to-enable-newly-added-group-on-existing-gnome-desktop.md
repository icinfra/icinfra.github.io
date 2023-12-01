---
layout: post
title:  已开启的gnome桌面如何进入群组为新加群组且权限为770的文件夹
date: 2023-11-29 11:00+0800
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

# 脚本定制
用户只需要运行一次本脚本即可。

```bash
#!/bin/bash

# Author:      wanlinwang
# Date  :      Nov 30, 2023
# Description: This script is to make newly added group(s) available in newly created gnome-terminal on CentOS 6.10. Run me once.

# Create the custom script
cat > ~/scan_new_grp.csh << 'EOF'
#!/bin/csh
set CSHRC=~/.cshrc
if (! -e "$CSHRC") then
    touch "$CSHRC"
endif

# 获取当前用户在当前session的主群组以及全部群组
setenv primary_group  `id -gn`
set    current_groups=`id -Gn`

# 获取当前用户最新的全部群组
set login_groups=`id -Gn $USER`

# 创建临时文件，并将群组信息写入临时文件
set temp1=`mktemp`
set temp2=`mktemp`
echo $current_groups | tr ' ' '\n' | sort > $temp1
echo $login_groups | tr ' ' '\n' | sort > $temp2

# 使用comm比较文件内容
set new_group=`comm -13 $temp1 $temp2`

# 删除临时文件
rm -f $temp1
rm -f $temp2

if ("$new_group" != "") then
    # 切换群组，使其生效
    newgrp $new_group
endif
EOF

# Update the gnome-terminal configuration
mkdir -p ~/.gconf/apps/gnome-terminal/profiles/Default/
cat > ~/.gconf/apps/gnome-terminal/profiles/Default/%gconf.xml << 'EOF'
<?xml version="1.0"?>
<gconf>
	<entry name="custom_command" mtime="1701352260" type="string">
		<stringvalue>/bin/csh -c &quot; ~/scan_new_grp.csh; exec /bin/csh &quot;</stringvalue>
	</entry>
	<entry name="use_custom_command" mtime="1701352260" type="bool" value="true"/>
	<entry name="palette" mtime="1701352260" type="string">
		<stringvalue>#2E2E34343636:#CCCC00000000:#4E4E9A9A0606:#C4C4A0A00000:#34346565A4A4:#757550507B7B:#060698209A9A:#D3D3D7D7CFCF:#555557575353:#EFEF29292929:#8A8AE2E23434:#FCFCE9E94F4F:#72729F9FCFCF:#ADAD7F7FA8A8:#3434E2E2E2E2:#EEEEEEEEECEC</stringvalue>
	</entry>
	<entry name="background_color" mtime="1701352260" type="string">
		<stringvalue>#FFFFFFFFDDDD</stringvalue>
	</entry>
	<entry name="visible_name" mtime="1701352260" type="string">
		<stringvalue>Default</stringvalue>
	</entry>
	<entry name="bold_color" mtime="1701352260" type="string">
		<stringvalue>#000000000000</stringvalue>
	</entry>
	<entry name="foreground_color" mtime="1701352260" type="string">
		<stringvalue>#000000000000</stringvalue>
	</entry>
</gconf>
EOF

chmod 0755 ~/scan_new_grp.csh

# Update .cshrc
cat >> ~/.cshrc << 'EOF'
set current_group=`id -g -n`
if ( $?primary_group ) then
    if ( $primary_group != $current_group ) then
        newgrp $primary_group
    endif
endif
unset    current_group
unsetenv primary_group
EOF

# Install krusader, a file manager. If you want to use this tool, please contact your system administrator to install.
#sudo yum install epel-release
#sudo yum localinstall http://rpms.plnet.rs/plnet-centos6-x86_64/RPMS.plnet-compiled/krusader-2.3.0-0.1.beta1.el6.x86_64.rpm

```
