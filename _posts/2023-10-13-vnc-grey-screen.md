---
layout: post
title: vnc灰屏
date: 2023-10-13 10:13:00
description: 
tags: vnc
categories: 
featured: true
---

在Ubuntu 18服务器上，从root账号的terminal里，执行su user01，然后执行vncserver启动一个vnc桌面。从vncviewer去连接时提示Failed to connect to socket /run/user/0/bus: Permission denied，
![image](https://github.com/icinfra/icinfra.github.io/assets/32032219/dd4be61a-cdf7-46e2-a2dd-2adf7df7ac6a)

![image](https://github.com/icinfra/icinfra.github.io/assets/32032219/50f285a3-47df-4cfc-b527-10a94c1704d7)

并且屏幕是灰屏的，
![image](https://github.com/icinfra/icinfra.github.io/assets/32032219/f0746ef7-1534-4923-9024-5a7d4d9d26f9)

这个问题是因为你从 root 用户切换到 user01 时，某些环境变量（特别是关于 D-Bus 的）没有被正确地设置。这导致 VNC 试图连接到 root 用户的 D-Bus 会话，而不是 user01 的会话。

为了解决这个问题，你可以尝试以下步骤：

1. **使用完整的登录 shell 切换到 user01**:
    当你使用 `su user01` 时，你只是简单地切换到了 user01，但没有加载 user01 的完整环境。为了加载完整的环境，你应该使用以下命令：
    ```bash
    su -l user01
    ```

2. **手动设置 `XDG_RUNTIME_DIR`**:
    如果上述方法不起作用，你可以尝试手动设置 `XDG_RUNTIME_DIR` 环境变量。这个变量通常指向 `/run/user/<UID>`，其中 `<UID>` 是用户的 UID。
    ```bash
    export XDG_RUNTIME_DIR=/run/user/$(id -u)
    ```

3. **启动 VNC 服务器**:
    在设置了正确的环境变量之后，你可以尝试再次启动 VNC 服务器。

4. **考虑使用 `vncserver` 的完整路径**:
    有时，确保你使用的是正确的 `vncserver` 也很重要。你可以使用 `which vncserver` 来查找其完整路径，然后使用该路径来启动它。

5. **检查 VNC 日志**:
    如果你仍然遇到问题，你应该检查 VNC 的日志文件，通常位于 `~/.vnc/` 目录下。这可能会给你更多关于问题的线索。

6. **确保 D-Bus 正在运行**:
    你可以使用以下命令来检查 D-Bus 是否正在为 user01 运行：
    ```bash
    ps aux | grep dbus | grep user01
    ```

希望这些步骤能帮助你解决问题！
