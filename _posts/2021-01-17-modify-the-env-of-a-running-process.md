---
layout: post
title: How to modify the environment of a running process in a desktop or server environment
date: 2021-01-17 08:00:00+0800
description: 
tags: process
giscus_comments: true
categories: icenv
---

If your environment initialization files are incorrect, your environment can become misconfigured. In such cases, how can you fix the environment of an existing process—especially one that doesn’t have a typical interface, like a shell process, for manual changes? A GDB script can help you.

Let’s walk through how to manipulate the PATH environment variable of an existing process. Consider a scenario where a process is created using the following script:,

![image](https://github.com/user-attachments/assets/89def87c-e083-41af-8038-4053dc2cd8d1)


Run it and get its output flushing,

![image](https://github.com/user-attachments/assets/6fbe2e42-6004-4a14-a6dc-fca05e3288c4)


So how can we fix it on the fly? Let’s write a gdb script like this,

![image](https://github.com/user-attachments/assets/686ff09f-251f-4062-9909-0f4fb7e6485b)


run it at another terminal,

![image](https://github.com/user-attachments/assets/0c00249f-faf5-45cb-9159-0e53fcff1932)


check the output from the user’s script terminal,

![image](https://github.com/user-attachments/assets/98b93b23-425b-4e68-aa04-cb0b970e8c5d)


Cheers, the broken environment was fixed.
