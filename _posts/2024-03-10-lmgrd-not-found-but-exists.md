---
layout: post
title:  lmgrd not found but exists
date:   2024-03-10 08:30:00+0800
description: 
tags: lic
giscus_comments: true
categories: icenv
---

```bash
$ strace -s 512 /software/Cadence/XCELIUM/23.09/tools.lnx86/bin/64bit/lmgrd -c cadence.txt
execve("/software/Cadence/XCELIUM/23.09/tools.lnx86/bin/64bit/lmgrd", ["/software/Cadence/XCELIUM/23.09/tools.lnx86/bin/64bit/lmgrd", "-c", "cadence.txt"], 0x7fff138508d0 /* 33 vars */) = -1 ENOENT (No such file or directory)
strace: exec: No such file or directory
+++ exited with 1 +++
```

sulotion
```bash
$ dnf install lsb
```
