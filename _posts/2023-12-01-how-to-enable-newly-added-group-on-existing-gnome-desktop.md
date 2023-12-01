---
layout: post
title:  已开启的gnome桌面如何进入群组为新加群组且权限为770的文件夹
date: 2023-11-29 11:00+0800
description: 
tags: group
giscus_comments: true
categories: icenv
---

# 环境说明
CentOS 6.10, Gnome, Krusader

# 效果演示

<img width="1920" alt="image" src="https://github.com/icinfra/icinfra.github.io/assets/32032219/69c5e444-1905-4b90-9ea4-3282f15d20ec">

# 文件定制
```bash
[wanlinwang@Tweak-new-group-effective-on-new-terminal-on-centos6 ~]$ cat ~/.gconf/apps/gnome-terminal/profiles/Default/%gconf.xml #gnome-terminal的启动命令定制，亦可以通过图形界面写。
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
[wanlinwang@Tweak-new-group-effective-on-new-terminal-on-centos6 ~]$ cat ~/scan_new_grp.csh
#!/bin/csh

# wanlinwang
# Nov 30, 2023

set CSHRC=~/.cshrc
if (! -e "$CSHRC") then
    touch "$CSHRC"
endif

# 获取当前用户的主群组
set primary_group=`id -gn`

# 获取当前用户的全部群组
set current_groups=`id -Gn`

# 获取登录时的群组
set login_groups=`id -Gn $USER`

# 创建临时文件
set temp1=`mktemp`
set temp2=`mktemp`

# 将群组信息写入临时文件
echo $current_groups | tr ' ' '\n' | sort > $temp1
echo $login_groups | tr ' ' '\n' | sort > $temp2

# 使用comm比较文件内容
set new_group=`comm -13 $temp1 $temp2`

# 删除临时文件
rm -f $temp1
rm -f $temp2

if ("$new_group" != "") then
    # 确保定义restore_primary_grp这个别名
    grep -q "alias restore_primary_grp newgrp " "$CSHRC"
    if ($status == 0) then
        sed -i "/alias restore_primary_grp/c\alias restore_primary_grp newgrp $primary_group" "$CSHRC"
    else
        echo "#auto added by wanlinwang.\nalias restore_primary_grp newgrp $primary_group" >> "$CSHRC"
    endif
    # 切换群组，使得生效
    newgrp $new_group
endif
[wanlinwang@Tweak-new-group-effective-on-new-terminal-on-centos6 ~]$ cat .cshrc 
# 切换到primary群组。
set current_group=`id -g -n`
set expect_group="wanlinwang"
if ( $current_group != $expect_group ) then
    newgrp $expect_group
endif
unset current_group expect_group

[wanlinwang@Tweak-new-group-effective-on-new-terminal-on-centos6 ~]$ sudo yum install epel-release
[wanlinwang@Tweak-new-group-effective-on-new-terminal-on-centos6 ~]$ sudo yum localinstall http://rpms.plnet.rs/plnet-centos6-x86_64/RPMS.plnet-compiled/krusader-2.3.0-0.1.beta1.el6.x86_64.rpm # krusader安装
```
