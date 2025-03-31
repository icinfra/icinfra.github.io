---
layout: post
title:  ontap模拟器
date:   2024-07-14 14:40:00+0800
description: 
tags: storage
giscus_comments: true
categories: icenv
---

# 一、下载模拟器

**参考《Simulate_ONTAP_9-14-1_Installation_and_Setup_Guide.pdf》P4的指导，登录网站进行下载。**

![image](https://github.com/user-attachments/assets/a5c4910e-3805-4601-b659-3799cf6e19d4)


# 二、传入pve，并解压转换

```bash
# 解压
tar -xvf vsim-netapp-DOT9.14.1-cm_nodar.ova

# 解压后的文件列表，其中ovf文件里定义了虚拟机的物理规格。
vsim-NetAppDOT-simulate-disk1.vmdk
vsim-NetAppDOT-simulate-disk2.vmdk
vsim-NetAppDOT-simulate-disk3.vmdk
vsim-NetAppDOT-simulate-disk4.vmdk
vsim-NetAppDOT-simulate.mf
vsim-NetAppDOT-simulate.ovf

# 转换vmdk为qcow2，能被导入到kvm平台。
qemu-img convert -f vmdk -O qcow2 vsim-NetAppDOT-simulate-disk1.vmdk disk1.qcow2
qemu-img convert -f vmdk -O qcow2 vsim-NetAppDOT-simulate-disk2.vmdk disk2.qcow2
qemu-img convert -f vmdk -O qcow2 vsim-NetAppDOT-simulate-disk3.vmdk disk3.qcow2
qemu-img convert -f vmdk -O qcow2 vsim-NetAppDOT-simulate-disk4.vmdk disk4.qcow2
```

# 三、查看虚拟机需求，并创建虚拟机

查看vsim-NetAppDOT-simulate.ovf文件，可以看虚拟机规格，特别的是

- 创建4个网卡，网卡类型为e1000
- IDE 控制器

![image](https://github.com/user-attachments/assets/edac64ff-f6ff-46cf-b758-af2945ca5c88)

![image](https://github.com/user-attachments/assets/78a6f853-995c-4fca-beec-f6ada0a05acc)

![image](https://github.com/user-attachments/assets/998e6654-56e7-4cdc-aacc-d4c739ba865b)


![image](https://github.com/user-attachments/assets/2a570e0d-7fc0-4067-932f-53456de24133)


![image](https://github.com/user-attachments/assets/64e50b00-d7cc-472a-8d24-b411ed01730b)


![image](https://github.com/user-attachments/assets/eb6cfe63-b9b5-4de0-8a05-f78d6eb5783a)


![image](https://github.com/user-attachments/assets/58e3db6c-7593-4b72-a747-6bce19c83827)


![image](https://github.com/user-attachments/assets/113f13ce-30a6-47d1-af7e-ee3d2a8f2434)


点完成，然后创建4个e1000的网卡

![image](https://github.com/user-attachments/assets/4ba64a94-382a-48a5-a17e-75ca01b77717)


# 四、在proxmox命令行，导入磁盘到虚拟机。随后attach并设置启动项

```bash
qm importdisk 120701001 disk1.qcow2 local-xfs
qm importdisk 120701001 disk2.qcow2 local-xfs
qm importdisk 120701001 disk3.qcow2 local-xfs
qm importdisk 120701001 disk4.qcow2 local-xfs
```

![image](https://github.com/user-attachments/assets/b56fed13-1007-4390-b8b9-87fa7e90db9c)


attach时选择ide控制器

![image](https://github.com/user-attachments/assets/deab4991-0249-496a-892c-7fb2c0c54a9f)


设置启动项

![image](https://github.com/user-attachments/assets/e006f525-e184-48b0-b2b6-47fb8b200062)


# 五、启动

![image](https://github.com/user-attachments/assets/0975cd7f-45ea-4c81-b3b4-20a63bfb3edc)


输入admin，然后执行halt命令，然后将虚拟机stop掉，重启进入到配置模式：

# 六、配置

![image](https://github.com/user-attachments/assets/d76abbf4-76e3-4cdd-bd17-a7ce6bea3ae9)


后面就可以通过web来配置了。

![image](https://github.com/user-attachments/assets/ffe6eabf-9aa8-4c03-b78e-e58e8de7c09f)


![image](https://github.com/user-attachments/assets/16f52862-d533-4be4-b5db-4b62e8d14992)


配置完毕后，自动跳到集群管理IP的web页面

![image](https://github.com/user-attachments/assets/7c4ec572-319d-4011-8f40-d562345a34fd)


![image](https://github.com/user-attachments/assets/22b0f04b-4c55-4dc6-9cbe-f2c9a9dfde35)


至此，ontap模拟器搭建完毕。

# 七、配置NetApp

## 配置许可证

![image](https://github.com/user-attachments/assets/62ca9bf4-35de-43fa-94e4-71d1cdfc7841)


贴入许可证

![image](https://github.com/user-attachments/assets/563f8a1d-3107-4b3d-9b04-238067fc0d9a)


## 准备存储

![image](https://github.com/user-attachments/assets/3bb3f6dd-4303-406c-b730-9b74049568cc)


![image](https://github.com/user-attachments/assets/4c47c7ad-6ba0-4cea-b7a5-ad9a2cb76b75)


## 配置协议

![image](https://github.com/user-attachments/assets/544adfcf-0866-4acb-9a38-91d3be8b9ef2)


![image](https://github.com/user-attachments/assets/c4a02a27-0a8b-4918-ac44-7e9c6516edc6)


## 配置存储

![image](https://github.com/user-attachments/assets/7211cbea-ab47-4947-bcde-ab490491b38a)

![image](https://github.com/user-attachments/assets/3bd2e5aa-9838-4f92-bb94-7a1b7ede7fdb)

![image](https://github.com/user-attachments/assets/a1d7a8a7-9024-4219-b80e-8e470f5ba502)


# 八、挂载使用

![image](https://github.com/user-attachments/assets/da23b0c5-fe7b-4073-a2f7-7c01ab70f852)


# 九、给svm配置LDAP

![image](https://github.com/user-attachments/assets/256ef67c-1834-445a-86d5-16ab4640feef)
