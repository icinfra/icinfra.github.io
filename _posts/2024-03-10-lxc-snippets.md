---
layout: post
title:  LXC
date:   2024-03-10 08:30:00+0800
description: 
tags: lxc
giscus_comments: true
categories: icenv
---

## lxc installation
```bash
dnf install epel-release
dnf install lxc lxc-doc lxc-templates
```

## lxc commands
```bash
lxc-ls # list all instances
DOWNLOAD_KEYSERVER="hkp://keyserver.ubuntu.com" lxc-create -n almalinux8 -B lvm --vgname vg01 --thinpool almalinux8 --fssize=20G -t download -- -d almalinux -r 8 -a amd64
lxc-start -n almalinux8 # start the instance
lxc-info -n almalinux8 # get the instance info
lxc-attach -n almalinux8 # attach to the instance
lxc-stop -n almalinux8 # stop the instance
```
注意：需创建lv给容器的根目录来运行FlexNet lic。除创建lv的方法，还可以参考文末"其它相关资料"。用以解决启动时报错：
> Cannot open daemon lock file\
> EXITING DUE TO SIGNAL 41 Exit reason 9\
> \*\*\*lmd exited with status 41 (Exited because another server was running)\
> MULTIPLE "\*\*\*lmd" license server systems running.\
> Please kill, and run lmreread
>
> This error probbly results from either:
>   1. Another copy of the license server manager (lmgrd) is running.
>   2. A prior license server manager (lmgrd) was killed with "kill -9"


## customizing config for container
```bash
vi /var/lib/lxc/almalinux8/config
# Template used to create this container: /usr/share/lxc/templates/lxc-download
# Parameters passed to the template: --dist almalinux --release 8 --arch amd64
# For additional config options, please look at lxc.container.conf(5)

# Uncomment the following line to support nesting containers:
#lxc.include = /usr/share/lxc/config/nesting.conf
# (Be aware this has security implications)


# Distribution configuration
lxc.include = /usr/share/lxc/config/common.conf
lxc.arch = x86_64

# Container specific configuration
lxc.rootfs.path = lvm:/dev/vg01/almalinux8
lxc.uts.name = almalinux8

# Network configuration
lxc.net.0.type = veth
lxc.net.0.link = virbr0
lxc.net.0.flags = up
lxc.net.0.hwaddr = 12:34:56:78:90:ab
lxc.net.0.ipv4.address = 192.168.122.2/24
lxc.net.0.ipv4.gateway = 192.168.122.1

# Mount enties
lxc.mount.entry = /software software none bind,create=dir 0 0
lxc.mount.entry = /tools tools none bind,create=dir 0 0
lxc.mount.entry = /licenses licenses none bind,create=dir 0 0
```

## Creating a bridge NIC named virbr0
```bash
# NetworkManager
nmcli con add type bridge ifname virbr0 con-name virbr0
nmcli con mod virbr0 ipv4.addresses 192.168.122.1/24 ipv4.method manual
nmcli con up virbr0
```

## Firewall(DNAT and FORWARD)
## enable ipv4 forwarding which needed by NAT
```bash
[root@lxc-host ~]# cat /proc/sys/net/ipv4/ip_forward
0
[root@lxc-host ~]# echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf 
[root@lxc-host ~]# sysctl -p
kernel.sysrq = 1
sysctl: cannot stat /proc/sys/net/ipv6/conf/all/disable_ipv6: No such file or directory
sysctl: cannot stat /proc/sys/net/ipv6/conf/default/disable_ipv6: No such file or directory
sysctl: cannot stat /proc/sys/net/ipv6/conf/lo/disable_ipv6: No such file or directory
kernel.numa_balancing = 0
kernel.shmmax = 68719476736
kernel.printk = 5
net.ipv4.ip_forward = 1
[root@lxc-host ~]# cat /proc/sys/net/ipv4/ip_forward
1
```

### iptables
```bash
# Generated by iptables-save
*raw
:PREROUTING ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
COMMIT

*mangle
:PREROUTING ACCEPT [0:0]
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
:POSTROUTING ACCEPT [0:0]
COMMIT

*nat
:PREROUTING ACCEPT [0:0]
:INPUT ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
:POSTROUTING ACCEPT [0:0]
-A PREROUTING -p tcp -m tcp --dport 5280 -j DNAT --to-destination 192.168.122.2:5280 #DNAT
-A PREROUTING -p tcp -m tcp --dport 3000 -j DNAT --to-destination 192.168.122.2:3000 #DNAT
-A POSTROUTING -o virbr0 -j MASQUERADE #DNAT
# SNAT
-A POSTROUTING -s 192.168.122.3/32 -o eth0 -j MASQUERADE
COMMIT

*filter
:INPUT ACCEPT [0:0]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
-A INPUT -p icmp -j ACCEPT
-A INPUT -i lo -j ACCEPT
-A INPUT -j REJECT --reject-with icmp-host-prohibited
# SNAT
-A FORWARD -s 192.168.122.3/32 -j ACCEPT
# DNAT
-A FORWARD -d 192.168.122.2/32 -p tcp -m tcp --dport 5280 -j ACCEPT
-A FORWARD -d 192.168.122.2/32 -p tcp -m tcp --dport 3000 -j ACCEPT
-A FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT
-A FORWARD -j REJECT --reject-with icmp-host-prohibited
-A OUTPUT -o lo -j ACCEPT
COMMIT
```

### firewalld
```bash
sysctl net.ipv4.ip_forward=1
firewall-cmd --zone=public --add-forward-port=port=5280:proto=tcp:toaddr=192.168.122.2:toport=5280 --permanent
firewall-cmd --zone=public --add-forward-port=port=3000:proto=tcp:toaddr=192.168.122.2:toport=3000 --permanent
firewall-cmd --zone=public --add-port=5280/tcp --permanent
firewall-cmd --zone=public --add-port=3000/tcp --permanent
firewall-cmd --zone=public --add-masquerade --permanent
firewall-cmd --reload
firewall-cmd --list-all
```


## 其它相关资料
来源 https://serverfault.com/q/922532 https://serverfault.com/a/1024360
```
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <dlfcn.h>
#include <string.h>

static int is_root = 0;
static int d_ino = -1;

static DIR *(*orig_opendir)(const char *name);
static int (*orig_closedir)(DIR *dirp);
static struct dirent *(*orig_readdir)(DIR *dirp);

DIR *opendir(const char *name) {
  if (strcmp(name, "/") == 0) {
    is_root = 1;
  }

  return orig_opendir(name);
}


int closedir(DIR *dirp) {
  is_root = 0;
  return orig_closedir(dirp);
}

struct dirent *readdir(DIR *dirp) {
  struct dirent *r = orig_readdir(dirp);
  if (is_root && r) {
    if (strcmp(r->d_name, ".") == 0) {
      r->d_ino = d_ino;
    } else if (strcmp(r->d_name, "..") == 0) {
      r->d_ino = d_ino;
    }
  }
  return r;
}

static __attribute__((constructor)) void init_methods() {
  orig_opendir = dlsym(RTLD_NEXT, "opendir");
  orig_closedir = dlsym(RTLD_NEXT, "closedir");
  orig_readdir = dlsym(RTLD_NEXT, "readdir");
  DIR *d = orig_opendir("/");
  struct dirent *e = orig_readdir(d);
  while (e) {
    if (strcmp(e->d_name, ".") == 0) {
      d_ino = e->d_ino;
      break;
    }
    e = orig_readdir(d);
  }
  orig_closedir(d);
  if (d_ino == -1) {
    puts("Failed to determine root directory inode number");
    exit(EXIT_FAILURE);
  }
}
```

```bash
gcc -ldl -shared -fPIC snpslmd-ld-preload.c -o snpslmd-ld-preload.so
vi snpslmd
#!/bin/sh
export LD_PRELOAD=snpslmd-ld-preload.so
exec /path/to/original_snpslmd "$@"
```
