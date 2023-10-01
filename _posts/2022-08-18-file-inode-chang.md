---
layout: post
title: 为什么文件被vim、sed命令修改后，其inode也变了？
date: 2022-08-19 00:00:00+0800
comments: true
description: vim、sed命令修改后，其inode也变了
tags: post
categories: linux
---




## 问题

为什么文件被vim、sed命令修改后，其inode也变了？



## 思路

inode变化了，那我们可以看下inode的变化情况。本文以vim为例子。



## 分析

1. 安装inotifywait工具
2. 监控将要操作的文件的父目录

   本例子，我要使用vim修改~/.bashrc的内容，因此我用以下命令监控~/目录

   ```
   ubuntu@ip-172-31-85-138:~$ inotifywait -mr ~/
   ```

3. 在另外一个terminal里，运行vim修改~/.bashrc
4. 查看步骤2的terminal的变化

   ```
   /home/ubuntu/ MOVED_FROM .bashrc
   /home/ubuntu/ MOVED_TO .bashrc~
   /home/ubuntu/ CREATE .bashrc
   /home/ubuntu/ OPEN .bashrc
   /home/ubuntu/ MODIFY .bashrc
   /home/ubuntu/ MODIFY .bashrc
   /home/ubuntu/ ATTRIB .bashrc
   /home/ubuntu/ CLOSE_WRITE,CLOSE .bashrc
   /home/ubuntu/ ATTRIB .bashrc
   /home/ubuntu/ MODIFY .bashrc.swp
   /home/ubuntu/ DELETE .bashrc~
   /home/ubuntu/ CLOSE_WRITE,CLOSE .bashrc.swp
   /home/ubuntu/ DELETE .bashrc.swp
   ^C
   ```

从监控可以看到，vim修改文件时，原文件会被重命名为.bashrc~，创建一个新的.bashrc进行修改。修改完毕后.bashrc~还会被删掉。

由此可见，.bashrc文件已经不是当初那个文件了，而是新建的文件。怪不得inode号都改变了。



## 延伸

sed也是类似的原理，编辑时会生成一个中间文件，操作完毕后会将中间文件rename成被操作的那个文件名