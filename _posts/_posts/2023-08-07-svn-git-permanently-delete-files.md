---
layout: post
title: 版本库彻底删除文件
date: 2023-08-09 20-08-45 20:08:45+0800
description: 
tags: 
giscus_comments: true
categories: 
---


wanlinwang, 2023/08/08
# SVN(subversion)

## 方法一：只保留一个revision

关键点：使用svnadmin dump最新revision。

先将需要删除的文件，删除了并执行svn ci提交，然后只保留最新这个revision，如下步骤，

```bash
# step1: get younest revision number
svnlook youngest /path/to/svn/repo_dir 
# step2: hotcopy without logs
svnadmin hotcopy --clean-logs /path/to/svn/repo_dir /path/to/svn/repo_new_dir01 
# step3: dump youngest revision
svnadmin dump /path/to/svn/repo_new_dir01 -r <youngest_revision>:<youngest_revision> > /path/to/svn/repo_in_youngest_revision.dump
# step4: create new repo
svnadmin create --fs-type fsfs /path/to/svn/repo_new_dir
# step5: load repo_in_youngest_revision.dump to the new repo
svnadmin load /path/to/svn/repo_new_dir < /path/to/svn/repo_in_youngest_revision.dump 
# step6: rename the new repo to the original one
mv /path/to/svn/repo_dir /path/to/svn/repo_dir_bak20230808; mv /path/to/svn/repo_new_dir /path/to/svn/repo_dir #重命名仓库目录
```
这样，/path/to/svn/repo_dir就是处理后的仓库了。

由于subversion是针对node进行增量存储，对于没有修改的文件与目录，subversion是简单地引用早期的revision。当只dump最新版本，即svnadmin dump -r <youngest_revision_num>时，需要对每个node递归地从<youngest_revision_num>到<oldest_revision_num>去重建，是一个非常耗时的操作。

## 方法二：保留所有revision

关键点：使用svndumpfilter命令。

```bash
# step1: dump
svnadmin dump /path/to/svn/repo_dir > repo_dir.dump
# step2: svndumpfilter
cat repo_dir.dump | svndumpfilter exclude path/to/dir1 path/to/dir2 > filtered.dump 
# step3: creat new repo
svnadmin create --fs-type fsfs /path/to/svn/repo_new_dir 
# step4: load filterd.dump to the new repo
svnadmin load /path/to/svn/repo_new_dir < filtered.dump 
# step5: rename the new repo to the original one
mv /path/to/svn/repo_dir /path/to/svn/repo_dir_bak20230808; mv /path/to/svn/repo_new_dir /path/to/svn/repo_dir #重命名仓库目录
```
这样，/path/to/svn/repo_dir就是处理后的仓库了。

由于是dump全部revision，不涉及对每个node的递归重建，只涉及简单的revision遍历并根据filelist过滤，这种方法耗时相对短。

## 方法三：保留所有revision

关键点：用path-based限制访问后执行svnsync
https://subversion.apache.org/faq.html#removal

```bash
# step1: 在authz文件里，将待删掉的目录或文件定义为不可读。
# step2: 执行svnsync复制仓库。
```


| |
|:--|
|方法 |    |效果 |    |耗时 |    |备注 |    
|方法一 |    |历史revision都没了 |    |长 |    |要重新checkout一份 |    
|方法二 |    |历史revision还在 |    |短 |    |要重新checkout一份 |    
|方法三 |    |未调研 |    |未调研 |    |未调研 |    

## 结论：采用方法二

经讨论并根据以下测试，采用方法二。

测试记录：
方法一：
耗时3h
```bash

8:54    svnlook youngest test_repo_bak20230728000501
8:54    svn info file:///data/user/wanin/test_repo_bak20230728000501
8:55    svn info -r 11997 file:///data/user/wanin/test_repo_bak20230728000501
8:56    date ; svnadmin dump test_repo_bak20230728000501 -r 11998 > test_repo_dump_r11998.dmp ; date
10:05   svnadmin create --fs-type fsfs test_repo_dump_r11998_new_repo
10:06   echo 'date ; svnadmin load test_repo_dump_r11998_new_repo < test_repo_dump_r11998.dmp; date'
10:06   date
Wed Aug  9 10:06:17 CST 2023
10:06   svnadmin load test_repo_dump_r11998_new_repo < test_repo_dump_r11998.dmp ; date
Wed Aug  9 11:57:13 CST 2023
```


方法二：
耗时43m
```bash
仓库test_repo_bak20230808201044有12000个revision。
20:55   svnadmin dump test_repo_bak20230808201044 > test_repo_bak20230808201044.dump
21:14   ls test_repo_bak20230808201044.dump
21:15   cat test_repo_bak20230808201044.dump | svndumpfilter exclude `cat filelist.txt | xargs ` > test_repo_bak20230808201044_filtered.dump
21:19   svnadmin create --fs-type fsfs test_repo_bak20230808201044_filtered
21:19   cat test_repo_bak20230808201044_filtered.dump | svnadmin load test_repo_bak20230808201044_filtered
21:38   cat test_repo_bak20230808201044_filtered/db/current
```

# Git

参考这个文档
[从存储库中删除敏感数据 - GitHub 文档](https://docs.github.com/zh/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
