---
layout: post
title: CentOS 7.9上的FreeIPA HA 架构
date: 2023-08-09 20-49-19 20:49:19+0800
description: 
tags: freeipa
giscus_comments: true
categories: icenv
---

## 机器
在proxmox virtual environment的虚拟机，

<img width="445" alt="image" src="https://github.com/icinfra/icinfra.github.io/assets/32032219/d4c52512-f679-4573-8b21-f253e2d19ba1">


## 防火墙
在master与replica上执行，
```bash
sudo firewall-cmd --add-service={freeipa-ldap,freeipa-ldaps,dns,mountd,rpc-bind} --permanent && sudo firewall-cmd --reload

```

## 包安装
在master与replica上执行，
```bash
sudo yum install -y freeipa-server ipa-server-dns

```

## ipa server配置
如果上游DNS没有设置master与replica的解析记录，则我们在master与replica/etc/hosts加上映射关系，
```bash
sudo tee -a /etc/hosts > /dev/null <<EOF
172.16.0.188 ipa-server-01.icinfra.cn
172.16.0.189 ipa-server-02.icinfra.cn
EOF

sudo cp -a /etc/hosts /etc/cloud/templates/hosts.redhat.tmpl

```


配置HA Master，
```bash
sudo ipa-server-install --setup-dns --domain=icinfra.cn --realm=ICINFRA.CN --hostname=ipa-server-01.icinfra.cn --admin-password=Secret123 --ds-password=Secret123 --no-reverse --allow-zone-overlap --auto-forwarders -U

```

```bash
==============================================================================
Setup complete

Next steps:
	1. You must make sure these network ports are open:
		TCP Ports:
		  * 80, 443: HTTP/HTTPS
		  * 389, 636: LDAP/LDAPS
		  * 88, 464: kerberos
		  * 53: bind
		UDP Ports:
		  * 88, 464: kerberos
		  * 53: bind
		  * 123: ntp

	2. You can now obtain a kerberos ticket using the command: 'kinit admin'
	   This ticket will allow you to use the IPA tools (e.g., ipa user-add)
	   and the web user interface.

Be sure to back up the CA certificates stored in /root/cacert.p12
These files are required to create replicas. The password for these
files is the Directory Manager password
[centos@vm-centos7-9-188 ~]$ 
```


配置HA replica，
```bash
sudo tee /etc/resolv.conf > /dev/null <<EOF
# 这里设置master为DNS服务器，在ipa-client-install时才会加入DNS记录，否则不加入。
nameserver 172.16.0.188
search icinfra.cn
EOF
sudo ipa-client-install --domain=icinfra.cn --server=ipa-server-01.icinfra.cn --hostname=ipa-server-02.icinfra.cn --enable-dns-updates -p admin -w Secret123 -U
sudo ipa-replica-install --setup-dns --auto-forwarders -p Secret123
sudo ipa-ca-install -p Secret123

```
<img width="1700" alt="image" src="https://github.com/icinfra/icinfra.github.io/assets/32032219/6c9f1020-01de-49d5-9bb3-1df7f7c67ac9">



## 客户端配置
```bash
sudo tee /etc/resolv.conf > /dev/null <<EOF
# 这里设置master与replica为DNS服务器，在ipa-client-install时才会加入DNS记录，否则不加入。
nameserver 172.16.0.188
nameserver 172.16.0.189
search icinfra.cn
EOF
sudo yum install -y ipa-client
sudo ipa-client-install --server=ipa-server-01.icinfra.cn --server=ipa-server-02.icinfra.cn --domain=icinfra.cn -p admin -w Secret123 -U

```
<img width="1700" alt="image" src="https://github.com/icinfra/icinfra.github.io/assets/32032219/44fd89ec-fe2d-4bea-af41-9be5efbbc619">



# 参考资料
https://blog.csdn.net/thesre/article/details/117791657
https://blog.csdn.net/thesre/article/details/124896546
