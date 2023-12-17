---
layout: post
title:  FreeIPA用户生命周期
date: 2023-12-17 22:00+0800
description: 
tags: ipa
giscus_comments: true
categories: icenv
---

![image](https://github.com/icinfra/icinfra.github.io/assets/32032219/5961c868-e903-4ce2-91d0-0be1df006cda)

图片来源：[User Life Cycle Operations](https://access.redhat.com/webassets/avalon/d/Red_Hat_Enterprise_Linux-7-Linux_Domain_Identity_Authentication_and_Policy_Guide-en-US/images/5dec4632c2e523d6aba195b27fb97f9a/user_lifecycle.png)

在用户生命周期管理操作中，为了管理用户的配置，管理员可以将用户账户从一个状态移动到另一个状态。新的用户账户可以作为 active 或 stage 添加，但不能作为 preserved 添加。
FreeIPA 支持以下用户生命周期管理操作：
- stage → active: 当处于 stage 状态的账户准备好被正式激活时，管理员将其移动到 active 状态。
- active → preserved: 员工离开公司后，管理员将其账户移动到 preserved 状态。
- preserved → active: 前员工重新加入公司。管理员通过将其账户从 preserved 状态移回 active 状态来恢复员工账户。
- preserved → stage: 前员工计划重新加入公司。管理员将其账户从 preserved 状态移动到 stage 状态，以准备账户的后续重新激活。

还可以从 FreeIPA 中永久删除 active、stage 和 preserved 用户。请注意，不能将 stage 用户移动到 preserved 状态，只能永久删除它们。
