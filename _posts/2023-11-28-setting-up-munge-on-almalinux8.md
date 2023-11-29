---
layout: post
title: 在多台almalinux8上配置MUNGE
date: 2023-11-28 16:00+0800
description: 
tags: munge
giscus_comments: true
categories: icenv
---

# 背景
[MUNGE](https://dun.github.io/munge/)(MUNGE Uid 'N' Gid Emporium) 是一种用于创建和验证凭证的身份验证服务。 它被设计为具有高度可扩展性，可在 HPC 集群环境中使用。 它允许进程验证具有公共用户和组的主机组中另一个本地或远程进程的 UID 和 GID。 这些主机形成一个由共享加密密钥定义的安全领域。 此安全领域内的客户端可以创建和验证凭据，而无需使用 root 权限、保留端口或特定于平台的方法。

Slurm集群可以利用MUNGE来使得提交的任务以提交者的身份，在执行机执行。

# 环境
机器

<img width="367" alt="image" src="https://github.com/icinfra/icinfra.github.io/assets/32032219/3e36504a-0405-4730-ade4-72700063b889">


# 系统下
在ldap上创建munge账号

## 安装
```bash
[root@offline-almalinux8-194-computing cloud-user]# dnf install --disablerepo=TurboVNC munge
```

## 配置
生成key，并放到共享目录，以供各个机器读取，
```bash
[root@offline-almalinux8-194-computing ~]# create-munge-key
[root@offline-almalinux8-194-computing ~]# mv /etc/munge/munge.key /home/munge/
```

## 运行
在集群的每台机器运行，
```bash
[root@offline-almalinux8-***-computing ~]# sudo -u munge munged --key-file=/home/munge/munge.key
[root@offline-almalinux8-***-computing ~]# ps -ef|grep '[m]unged'
munge       4682       1  0 10:22 ?        00:00:00 munged --key-file=/home/munge/munge.key
```

## 停止
```bash
[root@offline-almalinux8-***-computing ~]# sudo -u munge munged --stop
```

# 非系统下
## 安装
我们使用spack来安装munge，请注意需要将状态文件夹设置到/var或一个本地目录，因为每台机器运行都要维持状态。由于使用cloud-user安装的，运行时会检测整个安装目录的ownership，因此这里也用cloud-user来运行munge。
```bash
[cloud-user@offline-almalinux8-193-computing ~]$ spack install munge localstatedir=/var %gcc@=13.2.0
[+] /tools/OSS/spack/opt/spack/linux-almalinux8-zen4/gcc-13.2.0/bzip2-1.0.8-wjafdi26ghg2ostgp6fre2jtufxgtole
[+] /tools/OSS/spack/opt/spack/linux-almalinux8-zen4/gcc-13.2.0/libgpg-error-1.47-akx562yeurfuc3q3mwdsm2vq3cpbiaaz
[+] /tools/OSS/spack/opt/spack/linux-almalinux8-zen4/gcc-13.2.0/zlib-ng-2.1.4-uyqju5xvdx5h3acp5q3wuczoejvypzqr
[+] /tools/OSS/spack/opt/spack/linux-almalinux8-zen4/gcc-13.2.0/libgcrypt-1.10.3-zeoosgjkjxum2rg4eooio3wg5fc2i2jm
[+] /tools/OSS/spack/opt/spack/linux-almalinux8-zen4/gcc-13.2.0/openssl-3.1.3-vh3m7mfa7a5nnbkmhctiukwnz5ugffna
[+] /tools/OSS/spack/opt/spack/linux-almalinux8-zen4/gcc-13.2.0/munge-0.5.15-oska4u2fxfsz2c3xhhexoznkzbmckeh5
```

## 配置
生成key
```bash
[cloud-user@offline-almalinux8-193-computing ~]$ /tools/OSS/spack/opt/spack/linux-almalinux8-zen4/gcc-13.2.0/munge-0.5.15-oska4u2fxfsz2c3xhhexoznkzbmckeh5/sbin/mungekey --verbose
mungekey: Info: Created "/tools/OSS/spack/opt/spack/linux-almalinux8-zen4/gcc-13.2.0/munge-0.5.15-oska4u2fxfsz2c3xhhexoznkzbmckeh5/etc/munge/munge.key" with 1024-bit key
```

创建状态文件夹
```bash
[cloud-user@offline-almalinux8-193-computing ~]$ sudo mkdir -p -m 0700 /var/lib/munge /var/log/munge
[cloud-user@offline-almalinux8-193-computing ~]$ sudo mkdir -p -m 0755 /var/run/munge
[cloud-user@offline-almalinux8-193-computing ~]$ sudo chown cloud-user /var/lib/munge /var/log/munge /var/run/munge
```

## 运行
```bash
[cloud-user@offline-almalinux8-193-computing ~]$ /tools/OSS/spack/opt/spack/linux-almalinux8-zen4/gcc-13.2.0/munge-0.5.15-oska4u2fxfsz2c3xhhexoznkzbmckeh5/sbin/munged
```

## 停止
```bash
[cloud-user@offline-almalinux8-193-computing ~]$ /tools/OSS/spack/opt/spack/linux-almalinux8-zen4/gcc-13.2.0/munge-0.5.15-oska4u2fxfsz2c3xhhexoznkzbmckeh5/sbin/munged --stop
```

# 验证
munge输出到文本，然后unmunge解密
```bash
munge -n > munge.txt
unmunge < munge.txt
```

输出到管道，然后unmunge解密
```bash
[admin@offline-almalinux8-195-computing cloud-user]$  /tools/OSS/spack/opt/spack/linux-almalinux8-zen4/gcc-13.2.0/munge-0.5.15-oska4u2fxfsz2c3xhhexoznkzbmckeh5/bin/munge -n |  /tools/OSS/spack/opt/spack/linux-almalinux8-zen4/gcc-13.2.0/munge-0.5.15-oska4u2fxfsz2c3xhhexoznkzbmckeh5/bin/unmunge 
STATUS:          Success (0)
ENCODE_HOST:     offline-almalinux8-195-computing.icinfra.cn (127.0.0.1)
ENCODE_TIME:     2023-11-28 02:43:13 -0500 (1701157393)
DECODE_TIME:     2023-11-28 02:43:13 -0500 (1701157393)
TTL:             300
CIPHER:          aes128 (4)
MAC:             sha256 (5)
ZIP:             none (0)
UID:             admin (1451400000)
GID:             admins (1451400000)
LENGTH:          0
```
可以看到，成功了。

# 参考资料
https://dun.github.io/munge/

https://github.com/dun/munge/wiki/Installation-Guide#securing-the-installation

https://github.com/dun/munge/wiki/Man-7-munge
