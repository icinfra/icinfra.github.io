---
layout: post
title:  FreeIPA/IdM服务器（即将/已）过期的证书的处理方法
date: 2024-01-03 15:20+0800
description: 
tags: ipa
giscus_comments: true
categories: icenv
---

# 背景
FreeIPA/IdM服务器，默认Certificate Authority certificate的有效期为20年，host or service certificate有效期为2年。FreeIPA/IdM服务器在安装时，默认使用了Certmonger来auto renew证书。

# 场景
有些公司**出于安全需求，禁止了auto renew**的策略。假如没有打开auto renew，
- 如何手动更新即将过期的certificate？
- 如何手动修复已经过期的certificate？

# 更新即将过期的certificate
参考[^1]，IPA >= 4.1，在FreeIPA服务器执行`ipa-cacert-manage renew`。IPA < 4.1的例子：略。

[^1]: https://www.freeipa.org/page/Howto/CA_Certificate_Renewal

# 修复已经过期的certificate
## 测试环境
这里构建一个测试环境，模拟证书过期的场景。
- 参考[CentOS 7.9上部署高可用FreeIPA服务器](https://www.icinfra.cn/blog/2023/freeipa-ha-on-centos7/)一文，安装好FreeIPA服务器与客户端。
```bash
[centos@CentOS7-ipa-server ~]$ kinit admin
Password for admin@ICINFRA.CN: 
[centos@CentOS7-ipa-server ~]$ ipa user-find
--------------
1 user matched
--------------
  User login: admin
  Last name: Administrator
  Home directory: /home/admin
  Login shell: /bin/bash
  Principal alias: admin@ICINFRA.CN
  UID: 450000000
  GID: 450000000
  Account disabled: False
----------------------------
Number of entries returned 1
----------------------------
```

- 在FreeIPA服务器与客户端，分别操作：将时间同步服务断开，并将时间设置到将来的2年后，模拟证书过期。命令如下：
```bash
[centos@CentOS7-ipa-server ~]$ sudo date --set="`date -d '+2 years' '+%Y-%m-%d %H:%M:%S'`"
Sat Jan  3 20:36:47 EST 2026
[centos@CentOS7-ipa-server ~]$ ipa user-find
ipa: ERROR: cannot connect to 'https://ipa-server-01.icinfra.cn/ipa/json': [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:618)
[centos@CentOS7-ipa-server ~]$ sudo ipactl restart --ignore-service-failure
Restarting Directory Service
Restarting krb5kdc Service
Restarting kadmin Service
Restarting named Service
Restarting httpd Service
Failed to restart httpd Service
Forced restart, ignoring httpd Service, continuing normal operation
Restarting ipa-custodia Service
Restarting ntpd Service
Restarting pki-tomcatd Service
```

## 更新证书
在FreeIPA服务器上，执行`sudo ipa-cert-fix`修复过期的证书。
```bash
[centos@CentOS7-ipa-server ~]$ sudo ipa-cert-fix

                          WARNING

ipa-cert-fix is intended for recovery when expired certificates
prevent the normal operation of IPA.  It should ONLY be used
in such scenarios, and backup of the system, especially certificates
and keys, is STRONGLY RECOMMENDED.


The following certificates will be renewed: 

Dogtag sslserver certificate:
  Subject: CN=ipa-server-01.icinfra.cn,O=ICINFRA.CN
  Serial:  3
  Expires: 2025-12-24 01:32:38

Dogtag subsystem certificate:
  Subject: CN=CA Subsystem,O=ICINFRA.CN
  Serial:  4
  Expires: 2025-12-24 01:32:38

Dogtag ca_ocsp_signing certificate:
  Subject: CN=OCSP Subsystem,O=ICINFRA.CN
  Serial:  2
  Expires: 2025-12-24 01:32:38

Dogtag ca_audit_signing certificate:
  Subject: CN=CA Audit,O=ICINFRA.CN
  Serial:  5
  Expires: 2025-12-24 01:32:38

IPA IPA RA certificate:
  Subject: CN=IPA RA,O=ICINFRA.CN
  Serial:  7
  Expires: 2025-12-24 01:32:52

IPA Apache HTTPS certificate:
  Subject: CN=ipa-server-01.icinfra.cn,O=ICINFRA.CN
  Serial:  9
  Expires: 2026-01-04 01:33:26

IPA LDAP certificate:
  Subject: CN=ipa-server-01.icinfra.cn,O=ICINFRA.CN
  Serial:  8
  Expires: 2026-01-04 01:33:11

IPA KDC certificate:
  Subject: CN=ipa-server-01.icinfra.cn,O=ICINFRA.CN
  Serial:  10
  Expires: 2026-01-04 01:33:34

Enter "yes" to proceed: yes
Proceeding.
Renewed Dogtag sslserver certificate:
  Subject: CN=ipa-server-01.icinfra.cn,O=ICINFRA.CN
  Serial:  11
  Expires: 2027-12-25 01:47:51

Renewed Dogtag subsystem certificate:
  Subject: CN=CA Subsystem,O=ICINFRA.CN
  Serial:  12
  Expires: 2027-12-25 01:47:51

Renewed Dogtag ca_ocsp_signing certificate:
  Subject: CN=OCSP Subsystem,O=ICINFRA.CN
  Serial:  13
  Expires: 2027-12-25 01:47:52

Renewed Dogtag ca_audit_signing certificate:
  Subject: CN=CA Audit,O=ICINFRA.CN
  Serial:  14
  Expires: 2027-12-25 01:47:52

Renewed IPA IPA RA certificate:
  Subject: CN=IPA RA,O=ICINFRA.CN
  Serial:  15
  Expires: 2027-12-25 01:47:52

Renewed IPA Apache HTTPS certificate:
  Subject: CN=ipa-server-01.icinfra.cn,O=ICINFRA.CN
  Serial:  16
  Expires: 2028-01-05 01:47:52

Renewed IPA LDAP certificate:
  Subject: CN=ipa-server-01.icinfra.cn,O=ICINFRA.CN
  Serial:  17
  Expires: 2028-01-05 01:47:53

Renewed IPA KDC certificate:
  Subject: CN=ipa-server-01.icinfra.cn,O=ICINFRA.CN
  Serial:  18
  Expires: 2028-01-05 01:47:53

Becoming renewal master.
The ipa-cert-fix command was successful
[centos@CentOS7-ipa-server ~]$ sudo ipactl restart
Restarting Directory Service
Restarting krb5kdc Service
Restarting kadmin Service
Restarting named Service
Restarting httpd Service
Restarting ipa-custodia Service
Restarting ntpd Service
Restarting pki-tomcatd Service
Restarting ipa-otpd Service
Restarting ipa-dnskeysyncd Service
ipa: INFO: The ipactl command was successful
[centos@CentOS7-ipa-server ~]$ sudo ipactl status
Directory Service: RUNNING
krb5kdc Service: RUNNING
kadmin Service: RUNNING
named Service: RUNNING
httpd Service: RUNNING
ipa-custodia Service: RUNNING
ntpd Service: RUNNING
pki-tomcatd Service: RUNNING
ipa-otpd Service: RUNNING
ipa-dnskeysyncd Service: RUNNING
ipa: INFO: The ipactl command was successful
```
完成。使用`getcert list`命令查看，已经延期了。

# 参考资料
https://www.freeipa.org/page/Certificate_renewal

https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/identity_management_guide/certmonger-tracking-certs

https://frasertweedale.github.io/blog-redhat/posts/2019-12-12-certmonger-disable-auto-renew.html
