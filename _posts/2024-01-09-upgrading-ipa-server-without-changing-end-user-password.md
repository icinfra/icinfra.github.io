---
layout: post
title: 升级ipa并保持用户与群组等数据同步，降低用户上手成本
date: 2024-01-09 10:50+0800
description: 
tags: ipa
giscus_comments: true
categories: icenv
---

# 背景
由于[CentOS 7/8的EOL](https://www.icinfra.cn/blog/2024/centos-7-and-8-eol/)，IC设计环境的IT底座之一————操作系统，其升级被提上日程。其中涉及到在旧版本操作系统上的FreeIPA的升级。

# 思考
开始，计划在一台新操作系统上做fresh FreeIPA installation，给升级上去的操作系统使用即可。

后来，考虑在过渡期间需要维护两套FreeIPA，需要从旧FreeIPA里同步用户/群组到新FreeIPA，并且两套系统内用户的密码不能够保持统一。查阅了红帽官网升级的相关资料，决定使用Replica的方式来使得新旧FreeIPA数据同步，也能够保持用户的密码一致，降低用户的上手成本。

# 升级方案
## 架构图
升级的过渡期间，FreeIPA master-replica架构图，如下所示：
```bash
+---------------------+            +----------------------------+
|                     |            |                            |
|   CentOS 7 VM       |            |    AlmaLinux 8 VM          |
|                     |            |                            |
|   +-------------+   |            |   +--------------------+   |
|   |             |   |            |   |                    |   |
|   | FreeIPA     |   |            |   | AlmaLinux 8        |   |
|   | Server      |   |            |   | Container          |   |
|   | (Master)    |   |            |   |                    |   |
|   | version:    |   | Replication|   | +----------------+ |   |
|   | 4.6.8       <---------------------->                | |   |
|   +-------------+   |            |   | | FreeIPA        | |   |
|                     |            |   | | Server         | |   |
+---------------------+            |   | | (Replica)      | |   |
      |                            |   | | version:       | |   |
      |                            |   | | 4.9.12         | |   |
      |                            |   | +----------------+ |   |
      |                            |   |                    |   |
      |                            |   +--------------------+   |
      |                            |                            |
+------------+                     +----------------------------+
| Client Host|                                   |
| Group      |                                   |
| (for       |                                   |
| Master)    |                                   |
+------------+                                   |
                                        +---------------+
                                        | Client Host   |
                                        | Group         |
                                        | (for          |
                                        | Replica)      |
                                        +---------------+

```
其中，CentOS 7 VM里的是直接安装启动的FreeIPA Server。在AlmaLinux 8 VM里运行的AlmaLinux 8 Container里运行FreeIPA Server Replica。

这里使用容器来承载新FreeIPA Server，主要考虑到容器环境可以做到标准化，数据通过持久化到容器宿主机（AlmaLinux 8 VM）的目录下，再定期快照备份容器宿主机（AlmaLinux 8 VM）。

## 相关命令
```bash
# CentOS 7.9虚拟机上，安装FreeIPA Master。
sudo su -
yum install -y freeipa-server ipa-server-dns >& /dev/null
firewall-cmd --add-service={freeipa-ldap,freeipa-ldaps,dns,mountd,rpc-bind} --permanent && firewall-cmd --reload
"172.16.0.100 centos-7-ipa-server.icinfra.cn" | tee -a /etc/hosts
cp -a /etc/hosts /etc/cloud/templates/hosts.redhat.tmpl 
ipa-server-install --setup-dns --domain=icinfra.cn --realm=ICINFRA.CN --hostname=centos-7-ipa-server.icinfra.cn --admin-password=12345678 --ds-password=12345678 --no-reverse --allow-zone-overlap --auto-forwarders -U


# AlmaLinux 8虚拟机上，运行容器并初始化安装FreeIPA Replica。
sudo su -
dnf install -y podman
firewall-cmd --add-service={freeipa-ldap,freeipa-ldaps,dns,mountd,rpc-bind} --permanent && sudo firewall-cmd --reload

# 初次运行
mkdir /var/lib/ipa-data
podman run -ti --rm \
    -h almalinux-8-ipa-server.icinfra.cn \
    --net=host \
    --dns 172.16.0.100 \
    --dns-search icinfra.cn \
    -v /var/lib/ipa-data:/data:Z \
    --add-host=centos-7-ipa-server.icinfra.cn:172.16.0.100 \
    --add-host=almalinux-8-ipa-server.icinfra.cn:172.16.0.101 \
    -e TZ=Asia/Shanghai \
    freeipa/freeipa-server:almalinux-8 
        ipa-replica-install \
            --force-join \
            --setup-ca \
            --setup-dns \
            --server centos-7-ipa-server.icinfra.cn \
            --domain icinfra.cn \
            --ip-address 172.16.0.101 \
            --no-forwarders \
            --no-ntp \
            --principal admin \
            --admin-password 12345678

# 这样安装的replica，比master少了ntpd server。看下如何将这个也安装上。补充原因：由于容器实际上使用的是宿主机的时间，因此可以忽略。
# 如果因定位问题，需要在容器里执行strace，则在宿主机以及容器里，都要将selinux关掉。sudo setenforce 0

# 初始化完成之后，即/var/lib/ipa-data目录已经populated数据，下一次可以以后台的方式运行。
podman run -d --rm \
    -h almalinux-8-ipa-server.icinfra.cn \
    --net=host \
    --dns 172.16.0.100 \
    --dns-search icinfra.cn \
    -v /var/lib/ipa-data:/data:Z \
    --add-host=centos-7-ipa-server.icinfra.cn:172.16.0.100 \
    --add-host=almalinux-8-ipa-server.icinfra.cn:172.16.0.101 \
    -e TZ=Asia/Shanghai \
    freeipa/freeipa-server:almalinux-8 \
        ipa-replica-install \
            --force-join \
            --setup-ca \
            --setup-dns \
            --server centos-7-ipa-server.icinfra.cn \
            --domain icinfra.cn \
            --ip-address 172.16.0.101 \
            --no-forwarders \
            --no-ntp \
            --principal admin \
            --admin-password 12345678


# 新客户端系统加入 almalinux-8-ipa-server.icinfra.cn 这个FreeIPA
dnf install -y freeipa-client podman
cat > /etc/resolv.conf << EOF
search icinfra.cn
nameserver 172.16.0.101
EOF
ipa-client-install --force-join --hostname=almalinux-8-ipa-client.icinfra.cn --domain=icinfra.cn --server=almalinux-8-ipa-server.icinfra.cn --enable-dns-updates --principal=admin --password=12345678 -U
```

# 测试项
## 用户/群组同步
包括用户/群组的ID/Subordinate ID以及相关信息的同步。

需要注意的是，CentOS 7 VM里自带的FreeIPA Server是不支持Subordinate ID的，因此需要重点关注对它的测试————比如在AlmaLinux 8 Container上的FreeIPA Server创建的Subordinate ID能否被持久化保存，并被正常使用。

测试通过，见[打开ipa用户的subid(subordinate id)以运行rootless容器](https://www.icinfra.cn/blog/2024/subid-from-ipa/)。

## 域名解析
DNS forwarder遇到些问题，需要进一步定位。

## 时间同步
TODO

## 其它项

# 参考资料
[IdM从非RHEL发行版迁移至RHEL8](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/migrating_to_identity_management_on_rhel_8/ref_migrating-to-idm-on-rhel-8-from-freeipa-on-non-rhel-linux-distributions_migrating-to-idm-from-external-sources)

[FreeIPA Replica Setup](https://www.freeipa.org/page/V4/Replica_Setup)

[IdM Replica安装](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/installing_identity_management/installing-an-ipa-replica_installing-identity-management#installing-an-idm-replica-with-integrated-dns-and-a-ca_install-replica)
