---
layout: post
title:  lxc缓存到期
date:   2024-04-09 12:30:00+0800
description: 
tags: lxc
giscus_comments: true
categories: icenv
---

```bash
[root@lxc-host ~]# DOWNLOAD_KEYSERVER="hkp://keyserver.ubuntu.com" lxc-create -n slurm-master-node -t download -- -d almalinux -r 8 -a amd64 #提示过期了
The cached copy has expired, re-downloading...
Setting up the GPG keyring
ERROR: Unable to fetch GPG key from keyserver
lxc-create: slurm-master-node: lxccontainer.c: create_run_template: 1625 Failed to create container from template
lxc-create: slurm-master-node: tools/lxc_create.c: main: 331 Failed to create container slurm-master-node
[root@lxc-host ~]# date -d "@`cat /var/cache/lxc/download/almalinux/8/amd64/default/expiry`" #查看过期日期
Fri Mar 29 07:15:19 CST 2024
[root@lxc-host ~]# date -d "30 days" +%s > /var/cache/lxc/download/almalinux/8/amd64/default/expiry #更新过期日期至未来30天
[root@lxc-host ~]# DOWNLOAD_KEYSERVER="hkp://keyserver.ubuntu.com" lxc-create -n slurm-master-node -t download -- -d almalinux -r 8 -a amd64 #再次执行，即可使用cache了。
Using image from local cache
Unpacking the rootfs

---
You just created a Almalinux 8 x86_64 (20240227_23:08) container.

```
