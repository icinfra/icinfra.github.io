---
layout: post
title: SOCKS代理ChatGPT
date: 2023-08-04 19-36-49 19:36:49+0800
description: 
tags: 
giscus_comments: true
categories: 
---


首先，我们需要在你的Windows 10或MacOS系统上使用SSH设置SOCKS代理。然后，我们将在浏览器上安装和配置SwitchyOmega插件，以使所有访问chat.openai.com的请求都通过这个代理服务器。

### 第一步：设置SOCKS代理

#### 对于Windows 10：

1. 首先，你需要在你的Windows系统上安装SSH客户端。你可以选择使用Git Bash，它可以从[这个链接](https://git-scm.com/download/win)下载。

2. 安装完成后，打开Git Bash。

3. 在Git Bash中，输入下面的命令（用你的实际情况替换`<username>`,`<proxy-server>`和`<port>`）：  
    ```  
    ssh -D <port> -N <username>@<proxy-server>  
    ```  
    例如：  
    ```  
    ssh -D 8080 -N user@proxy-server.com  
    ```  
   这条命令将在本地的8080端口上启动一个SOCKS代理，所有通过此代理的流量都将通过`proxy-server.com`服务器传输。
   如下图所示：
   
   ![image](https://github.com/icinfra/icinfra.github.io/assets/32032219/430b374d-01ca-40a4-bab2-730e0a72423d)




5. 输入密码，如果你的服务器配置了公钥认证，可能需要提供私钥。

#### 对于MacOS：

1. 打开Terminal。

2. 输入同样的命令：  
    ```  
    ssh -D <port> -N <username>@<proxy-server>  
    ```

### 第二步：配置SwitchyOmega

1. 在Chrome或Firefox浏览器中安装SwitchyOmega插件。

2. 在浏览器的地址栏中输入`chrome://extensions/`（Chrome）或`about:addons`（Firefox），然后找到SwitchyOmega并点击“选项”。

3. 在SwitchyOmega的选项页面，点击左侧的“新建情景模式”。

4. 输入情景模式的名称，例如“SOCKS Proxy”，然后选择“代理服务器”。

5. 在“代理协议和服务器”部分，选择SOCKS5，输入`127.0.0.1`作为服务器地址，端口设置为你在第一步中选择的端口，例如`8080`。

6. 点击左侧的“自动切换”，然后在“规则列表规则”中添加一条新的规则。在“主机通配符”中输入`*.openai.com`，然后在“情景模式”中选择你刚刚创建的“SOCKS Proxy”。

7. 点击“应用选项”。

如下图所示，
![image](https://github.com/icinfra/icinfra.github.io/assets/32032219/266e65bc-ea88-49f5-9068-8061a4edec28)


现在，当你访问任何以`.openai.com`结尾的网站时，你的请求将通过你在第一步中设置的SOCKS代理服务器转发。
