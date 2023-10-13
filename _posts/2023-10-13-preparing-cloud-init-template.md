---
layout: post
title: cloud-init模板镜像的创建与使用
date: 2023-10-13 09:00:00
description: 
tags: pve
categories: cloud
featured: true
---

# Abstract
本文介绍，在Proxmox Virtual Environment（pve）上，cloud-init模板镜像的创建与使用。

# Steps
## Prepare a VM
这里使用CentOS 7.9.2209虚拟机
![image](https://github.com/icinfra/icinfra.github.io/assets/32032219/79857b17-ecd3-409a-b591-283117f93d70)

## Install cloud-init
```bash
apt-get install cloud-init
```

## Add Cloud-Init CD-ROM drive
Shutdown the VM. Execute blow code snippet on pve host,
```bash
qm set 10071 --ide2 local-xfs:cloudinit
qm set 10071 --boot order=scsi0
qm template 10071
```

## Deploying Cloud-Init Templates
```
qm clone 10071 171 --name CentOS-7-9-001
qm set 171 --sshkey ~/.ssh/id_rsa.pub
qm set 171 --ipconfig0 ip=172.16.0.171/24,gw=172.16.0.1
```
