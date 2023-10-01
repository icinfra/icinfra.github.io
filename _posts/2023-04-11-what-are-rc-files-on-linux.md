---
layout: post
title: Linux下的rc file是什么？
date: 2023-04-11 14:49:31+0800
description: 
tags: linux
giscus_comments: true
categories: icenv
---

# 问题
我们经常看到.cshrc，.bashrc这些“rc file”，它们为什么被称为“rc file”？

# 介绍

在Linux系统中，rc file是一个用于配置shell环境的文件。"rc"通常代表"run commands"或"resource configuration"，因此rc文件也称为运行命令或资源配置文件。据信它起源于 1965 年左右的 MIT 兼容时间共享系统 (CTSS) 的 runcom 工具。

不同的shell可能有不同的rc文件名和位置。以下是一些常见的Linux shell及其对应的rc文件：

- Bash shell：`~/.bashrc`
- Zsh shell：`~/.zshrc`
- Ksh shell：`~/.kshrc`
- Csh shell：`~/.cshrc`
- Tcsh shell：`~/.tcshrc`

当用户登录Linux系统时，shell会读取其对应的rc文件，并执行其中包含的命令和配置。这些命令和配置可以包括设置环境变量、定义别名、加载模块、设置提示符等。

用户可以编辑其rc文件来自定义其shell环境。例如，可以添加自定义的别名，以便更快速地执行常用的命令，或者添加环境变量以定制其工作环境。

需要注意的是，rc文件是shell启动时自动执行的，因此在编辑rc文件时要小心，确保不会意外地执行危险的命令或配置。