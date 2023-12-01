---
layout: post
title: 新加群组如何在terminal与文件
date: 2023-11-30 21:01:00
description: 新加群组，在新开的gnome-terminal里自动生效
tags: group
categories: icenv
---

第一个视频，演示新加入的群组，可以在新开的gnome-terminal里生效。

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include video.html path="https://youtu.be/WN7R-qALXcI" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

相关定制的文件，如下
[wanlinwang@Tweak-new-group-effective-on-new-terminal-on-centos6 ~]$ cat ~/.gconf/apps/gnome-terminal/profiles/Default/%gconf.xml
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



第二个视频，演示krusader可以在生效后的gnome-terminal里，打开新群组才可以访问的文件夹。

<div class="row mt-3">
  <div class="col-sm mt-3 mt-md-0">
        {% include video.html path="https://youtu.be/nG5YelsFeAs" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

安装命令，如下
EPEL      sudo yum install epel-release
Krusader  sudo yum localinstall http://rpms.plnet.rs/plnet-centos6-x86_64/RPMS.plnet-compiled/krusader-2.3.0-0.1.beta1.el6.x86_64.rpm
Gedit     sudo yum install gedit

