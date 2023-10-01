---
layout: post
title: EDA软件与开源软件的管理
date: 2023-07-15 17-44-42 17:44:42+0800
description: 
tags: 
giscus_comments: true
categories: icenv
---




# EDA软件与开源软件的管理

随着集成电路设计技术的发展，EDA (Electronic Design Automation) 工具在设计流程中扮演着关键的角色。此外，开源软件也在IC设计中提供了许多优势，包括在处理代码、构建工具和进行数据分析等方面的便利。本文主要对芯片设计环境主要的两类工具——EDA工具和开源软件的管理展开讨论。

## 一、简介

商业EDA厂商包括 Cadence、Synopsys、Mentor Graphics（已被西门子收购）、华大九天、芯华章等。常见的工具有 Virtuoso（用于模拟、布局、物理验证等）、Innovus（用于综合、布局、时序分析等）、PrimeTime（用于时序分析和优化）、Design Compiler（用于综合）、IC Compiler（用于布局和物理验证）以及 XCELIUM（高性能的仿真器，用于数字设计验证）等。

开源EDA工具包括 Magic（用于布局和物理验证）、Qflow（用于综合、布局和物理验证）、OpenROAD（用于综合、布局和物理验证）、Yosys（用于逻辑综合和验证）以及 Verilator（用于仿真和验证）等。

除了EDA工具，IC设计环境还可能使用一些开源工具，比如 Python, Perl, TCL 等用于脚本编写、文本与数据处理、EDA工具的控制；SVN, Git 用于版本控制和代码管理；Make 用于自动化构建和编译；Mariadb, Elasticsearch 等数据库工具；以及 Grafana, Kibana 等数据可视化工具。


## 二、EDA工具的管理

在管理EDA工具时，需要考虑以下几个方面：目录规划、选型、调试与维护、License管理以及环境管理。

### 目录规划

单平台、单OS（最常见的工具目录结构） `/tools/<VENDOR>/<TOOL>/<VERSION>` 

涉及多平台、单OS， `/tools/x86_64/<VENDOR>/<TOOL>/<VERSION>` 或 `/tools/aarch64/<VENDOR>/<TOOL>/<VERSION>` 的

涉及多平台、多OS，
`/tools/x86_64/CentOS7/<VENDOR>/<TOOL>/<VERSION>`  `/tools/aarch64/CentOS7/<VENDOR>/<TOOL>/<VERSION>` 

这里最主要的考虑点是兼容性与存储效率。如果优先兼容性，那么每个平台、每个OS分开是最好的；在没有去重功能的存储上，如果优先考虑存储效率，则层级往少规划，遇到不兼容时再采用modulefile分支来判断加载。
 

### 选型

选择EDA工具需要考虑功能、性能、稳定性、使用难易度、成本等因素。此外，还需要考虑可能的国际制裁、行业市场占有率、厂商服务质量等因素。

### 调试与维护

厂商在针对bug修复、新特性增加时，用户通常需要配合跑特定任务做测试，以实现软件的迭代升级。

### License管理

商业EDA工具，常用的License管理器：
* FlexLM ,
* RLM(Reprise License Manager),
* LM-X

FlexLM的options file支持丰富的个人、群组以及项目配额管理功能。如RTM、OpenLM、in-house tool等进行使用情况存储与数据分析以及日志解析与定期采样。

### 环境管理

可能经历的阶段包括
* .\*shrc阶段
* Project \*shrc阶段
* Environment Modules阶段
* Environment Modules + Wrapper
* Environment Modules + ELF定制 + Wrapper阶段

## 三、开源工具的管理

在管理开源工具时，也需要考虑目录规划、选型、安装调试与维护以及环境管理等方面。

### 目录规划

手动安装的工具，目录规划遵循上述的规则。包管理器安装的工具，目录由包管理器决定。

### 选型

一般是由研发用户提申请，管理员确认后安装。由于开源工具相对自由，内部使用对选型不做太多的限制。但在做软件集成产品，涉及到对外出售或对外提供服务的，则选型时须考虑其许可证，例如
* GPL（GNU通用公共许可证）
* LGPL（GNU宽通用公共许可证）
* BSD（Berkeley软件分发许可证）
* MIT（麻省理工学院许可证）
* Apache许可证


### 安装调试与维护

由于没有AE的支持（也有如红帽的RHEL订阅服务可提供技术支持服务），安装调试与维护均需靠使用方自己，以及借助上游社区完成。可以手动安装调试与维护，也可以借助 Spack（或Easybuild等）包管理器自动化安装。

### 环境管理

如果是手动安装，则手动制作modulefile，由Environment Modules进行管理。如果是自动安装，如Spack，可以使用spack内置的加载卸载命令管理环境，也可以enable TCL/Lmod Environment Modules，在安装时自动生成modulefile，用Environment Modules进行管理。

## 性能优化
* 对工具目录（大部分是只读场景）所在FS做FS-Cache加速工具的加载；
* 对工具环境文件（modulefile）进行缓存，加速工具环境的初始化；
* 对工具命令环境的最精确设置，避免大量的无效路径查找导致的耗时；
* 在兼容、稳定版本的范围内，选最新的工具版本。

## 结语

管理EDA工具和开源软件是一项复杂的任务，涉及到许多因素，包括工具的选型、目录规划、安装与调试、许可证管理以及环境管理等。通过对这些因素的深入理解和有效管理，可以更好地利用这些工具，提高IC设计的效率和质量。


## 参考资料
http://www.ruanyifeng.com/blog/2011/05/how_to_choose_free_software_licenses.html 阮一峰写的开源License介绍