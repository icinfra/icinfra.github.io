---
layout: post
title:  NFS AUTH_SYS 16 groups limitation
date:   2024-03-30 19:12:00+0800
description: 
tags: nfs
giscus_comments: true
categories: icenv
---

# 背景
NFS使用AUTH_SYS时有16群组限制，使用AUTH_GSS时有32群组限制。

很多IC设计公司，使用AUTH_SYS方式，都有遇到超过16个群组无法使用的问题。

# 分析
## 问题现象
```bash
[wanlinwang@VM-AlmaLinux8-tmpl-wanlinwang ~]$ id #从返回结果可知，q是第16群组，r是第17群组。
uid=1001(wanlinwang) gid=1001(p) groups=1001(p),1002(system),1003(b),1004(c),1005(d),1006(e),1007(f),1008(h),1009(i),1010(j),1011(k),1012(l),1013(m),1014(n),1015(o),1016(q),1017(r),1018(s),1019(a),1020(z)
[wanlinwang@VM-AlmaLinux8-tmpl-wanlinwang ~]$ ls -ld /tools/{testq,a}
drwxrwx--- 2 root r 2 Mar 31 11:16 /tools/a
drwxrwx--- 2 root q 2 Mar 31 11:16 /tools/testq
[wanlinwang@VM-AlmaLinux8-tmpl-wanlinwang ~]$ cd /tools/a
-bash: cd: /tools/a: Permission denied
[wanlinwang@VM-AlmaLinux8-tmpl-wanlinwang ~]$ cd /tools/testq
[wanlinwang@VM-AlmaLinux8-tmpl-wanlinwang testq]$ 

```

## RPC包分析
认证方式是AUTH_UNIX（AUTH_SYS），只传递了16个群组。

<img width="985" alt="image" src="https://github.com/icinfra/icinfra.github.io/assets/32032219/a0573e83-3f9c-4ec0-b45e-657f376582b1">

## 源码分析
从RFC5531 authsys_parms数据结构可看出，gids数组大小为16，
```c
         struct authsys_parms {
            unsigned int stamp;
            string machinename<255>;
            unsigned int uid;
            unsigned int gid;
            unsigned int gids<16>;
         };
```

# 解决方案
## 自建NFS

<img width="1176" alt="image" src="https://github.com/icinfra/icinfra.github.io/assets/32032219/9f4f1be8-713b-4d64-94ca-fa2258f927be">

rpc.mountd daemon是NFS(v2,v3) MOUNT协议的服务侧实现。从管理员命令mountd的手册可以看到，`-g, --manage-gids`选项可以从name service查询确定group ids，而不使用NFS client提供的用户的group ids。因此，在导出文件系统时，调整mountd的选项，并配置好适当的name service以供查询。

而NFS v4的nfsd没有提到该选项，尚不清楚选项与行为如何。

## NetApp
1）必须为NFS Vserver配置LDAP或NIS并使其正常运行。也可以本地SVM UID与群组成员文件。

2）LDAP或NIS服务器必须 为所有用户配置关联的组。

3）配置ns-switch包含 LDAP 或 NIS 进来，
```bash
vs1::> set -privilege advanced
Warning: These advanced commands are potentially dangerous; use
         them only when directed to do so by NetApp personnel.
Do you want to continue? {y|n}: y

vs1::*> vserver services name-service ns-switch modify -vserver <svm_name> -database passwd -sources files,nis
vs1::*> vserver services name-service ns-switch modify -vserver <svm_name> -database group  -sources files,nis
vs1::*> vserver services name-service ns-switch show
```

4）通过这两个选项，来打开超过16群组的支持。

<img width="963" alt="image" src="https://github.com/icinfra/icinfra.github.io/assets/32032219/21a28943-c730-4099-ac97-afd5abfc0fde">

```bash
vs1::> set -privilege advanced
Warning: These advanced commands are potentially dangerous; use
         them only when directed to do so by NetApp personnel.
Do you want to continue? {y|n}: y

vs1::*> vserver nfs modify -vserver vs1 -auth-sys-extended-groups enabled -extended-groups-limit 512

vs1::*> vserver nfs show -vserver vs1 -fields auth-sys-extended-groups,extended-groups-limit
vserver auth-sys-extended-groups extended-groups-limit
------- ------------------------ ---------------------
vs1     enabled                  512
```

5）调整缓存失效期限（可选）

某用户打开了NetApp对超过16群组的支持，超过16群组的用户，假设群组是先前已经加好的，则work；假设群组是刚加入的，则不work。

经过分析，是Name Service缓存、凭据缓存失效期限过长。而用户验证时，在新加群组几分钟内去验证的，此时缓存还是旧的，因此不work。可根据业务容忍度，适当地调整缓存失效时间。

与群组相关的，我们有三种缓存时间可以调整，分别是**name-service cache**，**vserver cached-cred-negative-ttl**，**vserver cached-cred-positive-ttl**。

查询命令：
```bash
vs1::*> vserver services name-service cache group-membership settings show -vserver <svm_name> #初始值为2小时。
vs1::*> vserver nfs show -vserver <svm_name> -fields cache-cred-negative-ttl #初始值为2小时。
vs1::*> vserver nfs show -vserver <svm_name> -fields cache-cred-positive-ttl #初始值为24小时。
```

修改命令
```bash
vs1::*> vserver services name-service cache group-membership settings modify -grplist-ttl 15m #修改为15min。
vs1::*> vserver nfs modify -vserver <svm_name> -cached-cred-negative-ttl 900000 #单位：毫秒，等于15min。
vs1::*> vserver nfs modify -vserver <svm_name> -cached-cred-positive-ttl 900000 #单位：毫秒，等于15min。
```
修改完再使用查询命令，查看是否已更改。

验证命令
```bash
vs1::*> vserver services name-service cache group-membership show -vserver <svm_name> -user <username>
vs1::*> vserver services name-service getxxbyy getgrlist -node <node_name> -vserver <svm_name> -use-cache true  -username <username>
vs1::*> vserver services name-service getxxbyy getgrlist -node <node_name> -vserver <svm_name> -use-cache false -username <username>
vs1::*> vserver nfs credentials show -node <node_name> -vserver <svm_name> -unix-user-name <username>
```

# 总结
不改NFS RPC传输的数据结构，而是服务端去Name Service查一下。这同时也解决了用户新群组在旧VNC Session不生效的问题：即使用户在terminal里执行groups没显示到新群组，但用户能访问新群组才有权限访问的目录，因为检查群组的这个步骤在服务端完成。

# 参考资料:
https://thinksystem.lenovofiles.com/storage/help/index.jsp?topic=%2Fnfs_file_access_reference_guide%2F1D3D018C-DF37-4C87-A789-58526A46B1A9_.html

https://www.netapp.com/pdf.html?item=/media/10720-tr-4067.pdf

https://kb.netapp.com/onprem/ontap/da/NAS/How_does_AUTH_SYS_Extended_Groups_change_NFS_authentication

https://datatracker.ietf.org/doc/html/rfc5531 P25 defines authsys_parms data structure, which limit the number of secondary groups up to 16.

https://access.redhat.com/articles/625273

https://docs.netapp.com/us-en/ontap/nfs-config/configure-name-service-switch-table-task.html

https://kb.netapp.com/onprem/ontap/da/NAS/NFS_access_is_getting_denied_after_enabling_auth-sys-extended-groups

# 致谢
感谢EDACAD社区同学的对于该问题激烈讨论与分享。
