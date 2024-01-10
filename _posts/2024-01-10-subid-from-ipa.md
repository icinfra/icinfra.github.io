---
layout: post
title: 升级ipa并保持用户与群组等数据同步，降低用户上手成本
date: 2024-01-10 11:30+0800
description: 
tags: ipa
giscus_comments: true
categories: icenv
---

# 背景
前面文章[升级ipa](https://www.icinfra.cn/blog/2024/upgrading-ipa-server-without-changing-end-user-password/)介绍了如何将ipa从CentOS 7上的旧版本迁移至AlmaLinux 8上的新版本。这里我们来看看如何使用AlmaLinux 8上的FreeIPA新版本的subid功能。

# 步骤
## FreeIPA服务端配置
<img width="1789" alt="image" src="https://github.com/icinfra/icinfra.github.io/assets/32032219/9cf91777-121c-463b-a246-58a580b39ff7">

## FreeIPA客户端配置
```bash
[root@almalinux-8-ipa-client ~]#  grep subid /etc/nsswitch.conf
subid: sss
```

## 验证
```bash
[root@almalinux-8-ipa-client ~]# su - wanlinwang
Last login: Wed Jan 10 02:36:13 EST 2024 on pts/0
[wanlinwang@almalinux-8-ipa-client ~]$ podman pull bosybox
✔ docker.io/library/bosybox:latest
Trying to pull docker.io/library/bosybox:latest...
Error: initializing source docker://bosybox:latest: reading manifest latest in docker.io/library/bosybox: requested access to the resource is denied
[wanlinwang@almalinux-8-ipa-client ~]$ podman run busybox date
Resolved "busybox" as an alias (/etc/containers/registries.conf.d/000-shortnames.conf)
Trying to pull docker.io/library/busybox:latest...
Getting image source signatures
Copying blob a307d6ecc620 done  
Error: copying system image from manifest list: writing blob: adding layer with blob "sha256:a307d6ecc6205dfa11d2874af9adb7e3fc244a429e00e8e3df90534d4cf0f3f8": processing tar file(potentially insufficient UIDs or GIDs available in user namespace (requested 65534:65534 for /home): Check /etc/subuid and /etc/subgid if configured locally and run "podman system migrate": lchown /home: invalid argument): exit status 1
[wanlinwang@almalinux-8-ipa-client ~]$ podman system migrate
[wanlinwang@almalinux-8-ipa-client ~]$ podman run busybox date
ERRO[0000] cannot find UID/GID for user wanlinwang: no subuid ranges found for user "wanlinwang" in /etc/subuid - check rootless mode in man pages. 
WARN[0000] Using rootless single mapping into the namespace. This might break some images. Check /etc/subuid and /etc/subgid for adding sub*ids if not using a network user 
Resolved "busybox" as an alias (/etc/containers/registries.conf.d/000-shortnames.conf)
Trying to pull docker.io/library/busybox:latest...
Getting image source signatures
Copying blob a307d6ecc620 done  
Error: copying system image from manifest list: writing blob: adding layer with blob "sha256:a307d6ecc6205dfa11d2874af9adb7e3fc244a429e00e8e3df90534d4cf0f3f8": processing tar file(potentially insufficient UIDs or GIDs available in user namespace (requested 65534:65534 for /home): Check /etc/subuid and /etc/subgid if configured locally and run "podman system migrate": lchown /home: invalid argument): exit status 1
[wanlinwang@almalinux-8-ipa-client ~]$ exit
logout
[root@almalinux-8-ipa-client ~]# vi /etc/nsswitch.conf
[root@almalinux-8-ipa-client ~]# grep subid /etc/nsswitch.conf
subid:      sss
[root@almalinux-8-ipa-client ~]# su - wanlinwang
Last login: Wed Jan 10 02:39:28 EST 2024 on pts/0
[wanlinwang@almalinux-8-ipa-client ~]$ podman run busybox date
Resolved "busybox" as an alias (/etc/containers/registries.conf.d/000-shortnames.conf)
Trying to pull docker.io/library/busybox:latest...
Getting image source signatures
Copying blob a307d6ecc620 done  
Error: copying system image from manifest list: writing blob: adding layer with blob "sha256:a307d6ecc6205dfa11d2874af9adb7e3fc244a429e00e8e3df90534d4cf0f3f8": processing tar file(potentially insufficient UIDs or GIDs available in user namespace (requested 65534:65534 for /home): Check /etc/subuid and /etc/subgid if configured locally and run "podman system migrate": lchown /home: invalid argument): exit status 1
[wanlinwang@almalinux-8-ipa-client ~]$ podman system migrate #在/etc/nsswitch.conf配置文件里增加了subid:sss后，需要执行podman system migrate后podman run才生效。
[wanlinwang@almalinux-8-ipa-client ~]$ podman run busybox date #生效了。
Resolved "busybox" as an alias (/etc/containers/registries.conf.d/000-shortnames.conf)
Trying to pull docker.io/library/busybox:latest...
Getting image source signatures
Copying blob a307d6ecc620 done  
Copying config 9211bbaa0d done  
Writing manifest to image destination
Wed Jan 10 07:40:58 UTC 2024

```

# 资料
https://access.redhat.com/solutions/6784071 如何配置使用ipa subid来源

https://access.redhat.com/solutions/6961540 只能允许一种subid来源
