---
layout: post
title:  ETX 自动化安装
date:   2025-03-09 12:00:00+0800
description: 
tags: etx
giscus_comments: true
categories: icenv
---

# inventory
```
[centos_hosts]
centos110 ansible_host=172.31.0.110
centos111 ansible_host=172.31.0.111
centos112 ansible_host=172.31.0.112
centos113 ansible_host=172.31.0.113

[rocky_hosts]
rocky120 ansible_host=172.31.0.120
rocky121 ansible_host=172.31.0.121
rocky122 ansible_host=172.31.0.122
rocky123 ansible_host=172.31.0.123
rocky130 ansible_host=172.31.0.130
rocky131 ansible_host=172.31.0.131
rocky132 ansible_host=172.31.0.132
rocky133 ansible_host=172.31.0.133

[etx_servers]
rocky130
rocky120
rocky121
centos110

[etx_nodes]
centos112
rocky122
rocky132
```

# Collection
```
[root@rockylinux-9-5-mgmt ansible-std]# tree -L 2
.
├── ansible.cfg
├── galaxy.yml
├── group_vars
│   ├── etx_nodes.yml
│   └── etx_servers.yml
├── inventory.ini
├── playbooks
│   ├── deploy_etxcn.yml
│   ├── deploy_etxsvr.yml
│   ├── response.etxcn.txt
│   └── test_delete_error_nodes.yml
├── roles
│   ├── etxcn_deployment
│   ├── etxcn_purge_error_nodes
│   ├── etxsvr_api_key
│   ├── etxsvr_deployment
│   ├── join_ad
│   ├── linux_prep
│   └── mount_iso
└── vault.yml

10 directories, 10 files
```

# etxsvr 安装
```
ansible-playbook -i inventory.ini playbooks/deploy_etxsvr.yml --ask-pass
SSH password: 
```
![image](https://github.com/user-attachments/assets/3044c370-e747-4d88-a072-37ed31e7058a)

注：省略部分截图

# etxsvr EULA
分别访问 etx_servers 的管理后台（如第一台，是 https://172.31.0.130:8443/etx/admin），然后同意 EULA。
![image](https://github.com/user-attachments/assets/bc2d9169-8339-4a30-b7c9-83d9bf4307f4)
![image](https://github.com/user-attachments/assets/20e4d3b0-0941-43ee-a299-ab855f8423eb)
![image](https://github.com/user-attachments/assets/4593be2b-3de6-4a87-b456-1bdf55e59e57)
![image](https://github.com/user-attachments/assets/596dafb0-fd63-4105-ad90-501c04b140ec)


# etxsvr配置
## License
![image](https://github.com/user-attachments/assets/80edcd6d-79e9-432c-b3d5-34f8c16b6f83)


## Authentication
![image](https://github.com/user-attachments/assets/a75124a5-864a-406d-9864-90ea73548e7a)


## Profile
![image](https://github.com/user-attachments/assets/f2e0180a-dfd0-453d-b0b8-39d3e9c93cac)


# etxcn 安装
```
[root@rockylinux-9-5-mgmt ansible-std]# ansible-playbook -i inventory.ini playbooks/deploy_etxcn.yml --ask-pass --ask-vault-pass
SSH password: 
Vault password: 
```
![image](https://github.com/user-attachments/assets/943af876-4159-496b-8436-19b506345346)

注：省略部分截图

![image](https://github.com/user-attachments/assets/f6082803-f95c-4b87-bc80-1ccfd2c7cfb6)


至此，可以用域账户，使用刚才建立的 Profile 接入了。
