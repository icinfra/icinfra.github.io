---
layout: post
title: rootless容器与NFS
date: 2024-01-12 23:10+0800
description: 
tags: container
giscus_comments: true
categories: icenv
---

很多人都对rootless Podman感兴趣。此工具允许您构建、安装和使用容器，而无需用户以 root 身份运行，也不需要用户在其系统上拥有大型 root 运行守护程序。相反，Podman（默认情况下）将容器映像存储在用户的主目录中。Podman 利用**用户命名空间**来执行此操作，因为大多数容器映像在映像中都有多个 UID。

但是，一个不起作用的问题是将这些映像存储在基于 NFS 的主目录中。

## 为什么 Podman 不支持 NFS 上的存储？

首先，对于大多数场景，rootless Podman 可以很好地与 NFS 卷配合使用。效果不佳的场景是将容器映像存储驻留在 NFS 挂载点上。

当用户尝试拉取映像或安装 RPM 包时，这个问题最容易理解。让我们来看看当用户尝试使用rootless Podman 在文件系统上安装 tarball 或 RPM 包时会发生什么。

在我们的示例中，我将使用 UID 为 1000 的用户，其中的 UID 映射设置如下所示：`/etc/subuid`

```plaintext
wanlinwang:100000:65536
```

结果如下所示：

```shell
$ podman unshare cat /proc/self/uid_map  
      0              1000                 1  
      1              100000             65536
```

现在，在容器内部，我想安装该软件包。该软件包将以 root 用户和 UID 为 60 的用户身份安装文件。这意味着，在主目录上安装包的容器的根进程会尝试运行如下内容：

```shell
$ chown 60:60 /var/www/html/index.html
```

当这种情况发生在本地文件系统上时，内核会检查两件事。首先，它检查 UID 60 和 GID 60 是否映射在用户命名空间内。其次，它决定了执行 chowning 的过程是否具有DAC_OVERRIDE能力。

由于该进程未以 UID 60 的形式运行，因此它必须能够覆盖正常的 UID/GID 权限。容器内部的进程以 root 身份运行时以 UID 1000 运行，当容器内以 UID 60 运行时，它实际上是主机上的 uid 100059。请注意，我只谈论用户命名空间DAC_OVERRIDE，这意味着容器内部的进程可以覆盖映射到用户命名空间（例如容器）的 UID/GID。

此设置适用于所有本地文件系统，因为本地内核可以做出决策。在处理 NFS 时，您必须满足本地内核和远程内核的要求。

从远程 NFS 服务器内核的角度来看待这个问题。远程内核看到一个进程以 UID 1000（容器中的根）身份运行，尝试将 1000 拥有的文件更改owner到 UID 100059（容器内的 UID 60）。远程内核拒绝此访问。

NFS 协议没有用户命名空间的概念，也无法知道作为 UID 1000 运行的进程是否合二为一。NFS 服务器也无法知道客户端进程是否DAC_OVERRIDE用户命名空间，以及 UID 100059是否映射到同一用户命名空间。

现在，如果您有一个在 NFS 共享上创建文件的正常进程，并且没有利用用户命名空间功能，则一切正常。当容器内的进程需要在 NFS 共享上执行需要特殊功能访问的操作时，问题就出现了。在这种情况下，远程内核将不知道该功能，并且很可能会拒绝访问。

## 如何使 NFS 与无根 Podman 一起工作？

有几种方法可以在 NFS 共享上设置用户的主目录以使用无根 Podman。

### 方法一
可以将文件中的`graphroot`标志配置为非 NFS 目录。例如，更改：`~/.config/containers/storage.conf`

```plaintext
[storage]  
driver = "overlay"  
runroot = "/run/user/1000"  
graphroot = "/home/wanlinwang/.local/share/containers/storage"
```

为

```plaintext
[storage]  
driver = "overlay"  
runroot = "/run/user/1000"  
graphroot = "/var/tmp/wanlinwang/containers/storage
```

此更改将使得在容器中拉取和创建的映像在家目录之外的其他目录上进行处理。

但该方法有一个缺点，就是无法在多台机器同时使用容器映像。如果需要在由多台服务器组成的集群中跑一个容器映像的多个实例，则需要在每台机器上都拉取该容器映像。


### 方法二
另一种选择是创建磁盘映像并将其挂载到目录中。您可以使用如下脚本：`~/.local/share/containers`

```bash
truncate -s 10g /home/wanlinwang/xfs.img  
mkfs.xfs -m reflink=1 /home/wanlinwang/xfs.img
```

然后，您可以在具有家目录的计算机上，执行如下操作：

```shell
$ mount /home/myuser/xfs.img /home/myuser/.local/share/containers
```

## 结论

rootless和root Podman 非常适合作为卷挂载的远程网络共享，包括 NFS 共享。但是，开箱即用的rootless Podman 在 NFS 主目录中可能无法正常工作，因为该协议无法理解用户命名空间。幸运的是，只需稍作配置更改，就可以在 NFS 主目录上使用rootless Podman。

## 参考资料

https://www.redhat.com/sysadmin/rootless-podman-nfs

https://opensource.com/article/18/12/podman-and-user-namespaces

https://opensource.com/users/rhatdan  红帽工程师的主页，容器相关的

https://opensource.com/article/19/5/shortcomings-rootless-containers  rootless容器的缺点

https://github.com/containers/podman/blob/main/rootless.md  rootless容器的缺点
