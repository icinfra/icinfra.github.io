---
layout: post
title: 获取git仓库的tags列表
date: 2023-11-03 22:28+0800
description: 
tags: github
giscus_comments: true
categories: icenv
---


```python
#!/bin/env python3


import requests
from datetime import datetime

def get_versions(owner, repo):
    url = f'https://api.github.com/repos/riscv-collab/riscv-gnu-toolchain/tags'
    response = requests.get(url)
    response.raise_for_status()  # Check for errors
    tags = response.json()
    print(f"Total number of tags is {len(tags)}")

    for tag in tags:
        tag_name = tag['name']
        try:
            tag_date = datetime.strptime(tag_name, "%Y.%m.%d")
            if tag_date >= datetime.strptime("2023.09.01", "%Y.%m.%d"):
                commit_sha = tag['commit']['sha']
                print(f'    version(')
                print(f'        "{tag_name}",')
                print(f'        tag="{tag_name}",')
                print(f'        commit="{commit_sha}",')
                print(f'        submodules=True,')
                print(f'    )')
        except:
            pass

# Replace 'owner' and 'repo' with the GitHub repository owner and name
owner = 'owner'
repo = 'repo'
get_versions(owner, repo)
```
