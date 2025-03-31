---
layout: post
title:  ChatGPT机器人
date:   2023-02-28 09:28:16+0800
description: ai chatbot
tags: formatting links
giscus_comments: true
categories: ai-posts
---

# 背景
聊天生成型预训练变换模型（英文：Chat Generative Pre-trained Transformer）简称ChatGPT，是由OpenAI开发的一个人工智能聊天机器人程序，于2022年11月推出。该程序使用基于GPT-3.5架构的大型语言模型并通过强化学习进行训练。 ChatGPT目前仍以文字方式交互，而除了可以通过人类自然对话方式进行交互，还可以用于相对复杂的语言工作，包括自动文本生成、自动问答、自动摘要等在内的多种任务。如：在自动文本生成方面，ChatGPT可以根据输入的文本自动生成类似的文本（剧本、歌曲、企划等），在自动问答方面，ChatGPT可以根据输入的问题自动生成答案。还具有编写和调试计算机程序的能力。在推广期间，所有人可以免费注册，并在登录后免费使用ChatGPT实现与AI机器人对话。
由于一些原因，大陆尚未能够访问这个有趣且强大的对话机器人。有人敏锐地识别到了商机，做起了微信聊天机器人，并做了商业化变现，据说部分粉丝多的号，成功变现超百万元。

# ChatGPT机器人有哪些
依托于微信生态的：
- 微信订阅号（公众号）
- 微信服务号（公众号）
- 微信小程序

依托于公司企业微信的：
- 企业微信机器人，服务于公司内部用户

依托于开源生态：
- 如做成VSCode插件，做自动coding、代码检查、bug修复等功能。

散兵游勇：
- 自建web，通过不同渠道引流

# 如何做ChatGPT机器人
- 无法直接访问chat.openai.com的现成客户端，如微信：
在一台能够访问chat.openai.com的服务器，租用云虚拟机或者云函数平台，运行一个机器人，这个机器人接受来自微信的请求，随后将请求forward到chat.openai.com，随后将从chat.openai.com返回的结果发回给微信。

- 自建的web：
在一台能够访问chat.openai.com的服务器，租用云虚拟机。搭建web系统，后台为chat.openai.com api，前台自行定制。

# 总结
总之，ChatGPT这阵风，很多商业大佬都开始惊慌了，纷纷all in。