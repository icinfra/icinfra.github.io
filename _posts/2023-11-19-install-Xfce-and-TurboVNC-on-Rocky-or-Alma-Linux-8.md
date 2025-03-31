---
layout: post
title: Rocky/Alma Linux 8 上安装图形化界面
date: 2023-11-09 09:56+0800
description: 
tags: xfce
giscus_comments: true
categories: icenv
---

## XFCE桌面环境
XFCE 桌面环境作为通用桌面环境 (CDE) 的一个分支而创建，体现了模块化和可重用性的传统 Unix 哲学。您可以在几乎任何版本的 Linux 上安装 XFCE，包括 Rocky Linux。

它也是最易于与替代窗口管理器（例如 Awesome 或 i3）结合使用的桌面环境之一。然而，此过程将帮助您启动并运行 Rocky Linux 和更典型的 XFCE 安装。

## 先决条件
工作站或笔记本电脑
希望运行 XFCE 作为桌面而不是默认的 GNOME 桌面

## 安装 Rocky Linux 最小化
在本节中，您需要成为 root 用户，或者能够sudo提升您的权限。

在安装 Rocky Linux 时，我们使用了以下几组软件包：
* Minimal
* Standard

## 运行系统更新
首先，运行服务器更新命令。系统将重建存储库缓存。通过这种方式，系统 cab 可以识别可用的包。

```bash
dnf update
```


## 启用dnf仓库
您需要 EPEL 存储库中的 XFCE 非官方存储库才能在 Rocky 8.x 版本上运行。

通过输入以下内容启用此dnf仓库：
```bash
dnf install epel-release
```
回答“Y”即可安装。

您还需要 Powertools 和 lightdm 仓库。现在启用这些：

```bash
dnf config-manager --set-enabled powertools
dnf copr enable stenstorp/lightdm
```
同样，您将看到有关dnf仓库库的警告消息。继续并回答Y提示。

## 检查群内可用的环境和工具
现在dnf仓库已启用，请运行以下命令来检查所有内容。

首先，检查您的存储库列表：

```bash
dnf repolist
```
您应该得到以下信息，显示所有已启用的存储库：

```bash
appstream                                                        Rocky Linux 8 - AppStream
baseos                                                           Rocky Linux 8 - BaseOS
copr:copr.fedorainfracloud.org:stenstorp:lightdm                 Copr repo for lightdm owned by stenstorp
epel                                                             Extra Packages for Enterprise Linux 8 - x86_64
epel-modular                                                     Extra Packages for Enterprise Linux Modular 8 - x86_64
extras                                                           Rocky Linux 8 - Extras
powertools                                                       Rocky Linux 8 - PowerTools
```
运行以下命令来检查 XFCE：

```bash
dnf grouplist
```
您应该在列表底部看到“Xfce”。

再运行`dnf update`一次以确保所有启用的存储库都读入系统。

## 安装包
要安装 XFCE，请运行：

```bash
dnf groupinstall "xfce"
```
还要安装 `lightdm`：

```bash
dnf install lightdm
```
## 最后步骤
gdm在`dnf groupinstall "xfce"`期间添加并启用，需要禁用它：

```bash
systemctl disable gdm
```
现在您可以启用`lightdm`：

```bash
sed -r -i 's#^user-sessions=.*#user-sessions=xfce#g' /etc/lightdm/lightdm.conf
systemctl enable lightdm --now
```
您需要在启动后告诉系统仅使用图形用户界面。将默认目标系统设置为GUI界面：

```bash
systemctl set-default graphical.target
```
然后重新启动：

```bash
reboot
```
您最终应该在 XFCE GUI 中看到登录提示，当您登录时，您将拥有所有 XFCE 环境。

## 命令集合
```bash
# 安装xfce环境
dnf update
dnf install epel-release
dnf config-manager --set-enabled powertools
dnf copr enable stenstorp/lightdm
dnf groupinstall "xfce"
dnf groupinstall "Fonts"
dnf install lightdm
systemctl disable gdm

sed -r -i 's#^user-sessions=.*#user-sessions=xfce#g' /etc/lightdm/lightdm.conf
systemctl enable lightdm --now

# 安装TurboVNC
TIMESTAMP=`date +%Y%m%d%H%M%S`
 
yum -y install wget
yum -y install perl
 
# firewalld
systemctl disable firewalld --now
 
# selinux
sed -i_bak`date +%Y%m%d%H%M%S` \
    's/^\s*SELINUX=.*/SELINUX=disabled/g' \
/etc/selinux/config
 
# add a file to disable non-privilege users' powermanagement
mkdir -p /etc/xdg/xfce4/kiosk
cat > /etc/xdg/xfce4/kiosk/kioskrc << EOF
[xfce4-session]
Shutdown=root
EOF
 
# setup for TurboVNC
wget https://raw.githubusercontent.com/TurboVNC/repo/main/TurboVNC.repo -O /etc/yum.repos.d/TurboVNC.repo
yum -y install turbovnc
 
# modify conf for TurboVNC
sed -i_bak${TIMESTAMP} \
    -e 's/#\s*$wm = .*/$wm = "xfce";/g' \
    -e 's/#\s*$serverArgs = .*/$serverArgs = "-listen tcp";/g' \
    -e 's/#\s*$securityTypes = .*/$securityTypes = "TLSOtp, TLSPlain, X509Otp, X509Plain,OTP, UnixLogin, Plain";/g' \
    /etc/turbovncserver.conf
 
sed -i_bak${TIMESTAMP} \
    -e 's/^#\s*permitted-security-types = .*/permitted-security-types =  TLSOtp, TLSPlain, X509Otp, X509Plain, OTP/g' \
    /etc/turbovncserver-security.conf
 
# modify conf for ssh and sshd
echo "AcceptEnv DISPLAY" >> /etc/ssh/sshd_config
systemctl restart sshd
echo "SendEnv   DISPLAY" >> /etc/ssh/ssh_config
 
# swicth to grahphical
systemctl set-default graphical.target
systemctl isolate graphical.target

reboot
```


## 结论
XFCE 是一个具有简单界面的轻量环境。它是 Rocky Linux 上默认 GNOME 桌面的替代方案。

## 资料
https://docs.rockylinux.org/guides/desktop/xfce_installation/
