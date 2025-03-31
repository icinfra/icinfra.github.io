---
layout: post
title: new group and change directory
date: 2024-01-19 10:19+0800
description: 
tags: newgrp
giscus_comments: true
categories: icenv
---

# 介绍
newgrp启动一个新shell。用户一般会拥有多个群组。切换primary群组时会带来很多麻烦。

# 实践
如果group名字与目录名字不一样，就放这个进去到~/.cshrc文件，通过不同分支来判断。
```bash
alias new_group 'setenv NEW_MANNUALY_GROUP \!:1; exec newgrp $NEW_MANNUALY_GROUP'
if ($?NEW_MANNUALY_GROUP) then
    switch ($NEW_MANNUALY_GROUP)
    case 'group001':
        cd /project/group001/${USER} && unsetenv NEW_MANNUALY_GROUP
        breaksw
    case 'group002':
        cd /project/group002/${USER} && unsetenv NEW_MANNUALY_GROUP
        breaksw
    endsw
endif
```

如果group名字与目录名字一样，就放这段进去到~/.cshrc文件，简单：
```bash
alias new_group 'setenv NEW_MANNUALY_GROUP \!:1; exec newgrp $NEW_MANNUALY_GROUP'
if ($?NEW_MANNUALY_GROUP) then
    cd /project/${NEW_MANNUALY_GROUP}/${USER} && unsetenv NEW_MANNUALY_GROUP
endif
```

然后就可以执行 `new_grp xxxx` 来切换至`xxxx`群组了，并且还可以保持当前环境变量。
