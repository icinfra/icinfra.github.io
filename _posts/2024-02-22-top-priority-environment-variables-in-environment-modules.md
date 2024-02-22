---
layout: post
title:  环境变量的高优先级值
date:   2024-02-22 12:00:00+0800
description: 
tags: modules
giscus_comments: true
categories: icenv
---

将路径保持在最前面，有两种方式：
1. 官网的方式：https://modules.readthedocs.io/en/latest/cookbook/top-priority-values.html

2. 我设计的方式：在有命令冲突的modulefile里，如xcelium里，加上这段使得indago工具的PATH变量在前面，优先级更高。这样，运行的indago命令是来自于indago工具目录的indago。
```tclsh
if { [ info exists env(LOADEDMODULES) ] } {
    set loaded_module_list [ split $env(LOADEDMODULES) ":"]
    foreach modulefile $loaded_module_list {
        if {[regexp {^(indago|VDEBUG)} $modulefile]} {
            module swap --not-req $modulefile #--not-req以便允许用户切换版本。如果不加，其依赖关系将阻止用户切换版本。
            break
        }
    }
}
```
