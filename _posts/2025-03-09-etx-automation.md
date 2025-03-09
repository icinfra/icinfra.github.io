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
![alt text](https://github.com/icinfra/icinfra.github.io/assets/img/etx-automation-image.png)
注：省略部分截图

# etxsvr EULA
分别访问 etx_servers 的管理后台（如第一台，是 https://172.31.0.130:8443/etx/admin），然后同意 EULA。
![alt text](https://github.com/icinfra/icinfra.github.io/assets/img/etx-automation-image-1.png)
![alt text](https://github.com/icinfra/icinfra.github.io/assets/img/etx-automation-image-2.png)
![alt text](https://github.com/icinfra/icinfra.github.io/assets/img/etx-automation-image-3.png)
![alt text](https://github.com/icinfra/icinfra.github.io/assets/img/etx-automation-image-4.png)

# etxsvr配置
## License
![alt text](https://github.com/icinfra/icinfra.github.io/assets/img/etx-automation-image-6.png)

## Authentication
![alt text](https://github.com/icinfra/icinfra.github.io/assets/img/etx-automation-image-7.png)

## Profile
![alt text](https://github.com/icinfra/icinfra.github.io/assets/img/etx-automation-image-9.png)

# etxcn 安装
```
[root@rockylinux-9-5-mgmt ansible-std]# ansible-playbook -i inventory.ini playbooks/deploy_etxcn.yml --ask-pass --ask-vault-pass
SSH password: 
Vault password: 
```
![alt text](https://github.com/icinfra/icinfra.github.io/assets/img/etx-automation-image-5.png)
注：省略部分截图

![alt text](https://github.com/icinfra/icinfra.github.io/assets/img/etx-automation-image-8.png)

至此，可以用域账户，使用刚才建立的 Profile 接入了。