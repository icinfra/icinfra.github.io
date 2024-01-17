---
layout: post
title: Registry作为pull through cache服务器
date: 2024-01-17 16:30+0800
description: 
tags: registry
giscus_comments: true
categories: icenv
---

# 背景
容器在risc-v社区比较流行。这里介绍容器在研发环境的实践，能够单向拉取镜像运行，不能推送。

```bash
+------------------------------------+        +------------------------------+       +-----------+
| Upstream Docker                    |        | Pull-Through Cache           |       | Client    |
| Registry                           |        | Docker Registry              |       | (host001) |
| (https://registry-1.docker.io)     | -----> | (registry.icinfra.cn:5000)   | ----> |           |
+------------------------------------+        +------------------------------+       +-----------+
```

# 配置
## Pull-Through Cache Docker Registry
根据 https://docs.docker.com/docker-hub/mirror/#run-a-registry-as-a-pull-through-cache 介绍，配置`/etc/docker/registry/config.yml`文件里的`proxy.remoteurl`为外部registry。

registry容器可以通过传入REGISTRY_PROXY_REMOTEURL环境变量来完成配置，命令如下：
```bash
podman run -d -p 5000:5000 --name registry-cache -e REGISTRY_PROXY_REMOTEURL=https://registry-1.docker.io registry:2
```

## Client
在客户端侧配置registry地址，让podman或docker命令使用。
```bash
cat > ~/.config/containers/registries.conf <<EOF
[registries.insecure]
 registries = ['registry.icinfra.cn:5000']
EOF
```

完毕。

# 附
1. https://distribution.github.io/distribution/about/configuration/ 这里提到，podman push到pull-through cache是不支持的。满足“禁止用户push”的需求。
2. 容器镜像层不能放在NFS，用户数据可以通过-v映射NFS目录进去使用。
3. 需要打开subordinate ID。
