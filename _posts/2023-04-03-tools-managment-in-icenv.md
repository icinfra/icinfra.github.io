---
layout: post
title: EDA工具与开源工具的管理
date: 2023-04-03 20:20:25+0800
description: 
tags: tool
giscus_comments: true
categories: icenv
---


## 介绍

在IC设计中，常用的商业EDA厂商包括Cadence、Synopsys和Mentor Graphics等，常见的工具包括：

- Virtuoso：用于模拟、布局、物理验证等
- Encounter：用于综合、布局、时序分析等
- PrimeTime：用于时序分析和优化
- Design Compiler：用于综合
- IC Compiler：用于布局和物理验证
- XCELIUM：高性能的仿真器，用于数字设计验证

在IC设计中，常用的开源EDA工具包括：

- Magic：用于布局和物理验证
- Qflow：用于综合、布局和物理验证
- OpenROAD：用于综合、布局和物理验证
- Yosys：用于逻辑综合和验证
- Verilator：用于仿真和验证

EDA工具在设计流程中扮演着至关重要的角色，可以帮助设计人员提高设计效率和设计质量。通过EDA工具，设计人员可以对电路进行仿真、综合、布局、布线、逻辑验证、物理验证、测试等多个模块的分析和处理，从而可在设计的早期阶段发现和解决问题，提高设计的可靠性和正确性。此外，EDA工具还可以帮助设计人员优化电路的性能和功耗，提高电路的可靠性和可维护性，缩短设计周期和降低设计成本。

除了EDA工具，IC设计环境还可能使用其他的一些开源工具，比如：

- Python, Perl, TCL等：用于脚本编写、文本与数据处理、EDA工具的控制
- SVN, Git：用于版本控制和代码管理
- Make：用于自动化构建和编译
- Mariadb, Elasticsearch等：数据库工具
- Grafana, Kibana等：数据可视化工具

这些开源工具可以帮助IC设计流程中的数据版本管理、数据存储与展示、业务流程定制等。例如，Python、Perl、TCL等脚本语言可以用于脚本编写、文本与数据处理以及EDA工具的控制。SVN、Git等版本控制工具可以用于代码管理，Make可以用于自动化构建和编译。此外，Mariadb、Elasticsearch等数据库工具和Grafana、Kibana等数据可视化工具也可以用于IC设计环境中的数据管理和展示。

## EDA工具的管理

注：这里介绍商业EDA工具

- 管理EDA工具的过程

它可以分为以下几个步骤：

1. **EDA工具的选型**：
    
    首先，需要根据项目的需求和具体情况来选择合适的EDA工具。在选型过程中，需要考虑多个因素，如EDA工具的功能、性能、稳定性、可维护性、成本等。同时，也需要考虑到EDA工具的适用性和可扩展性，以便在未来的设计过程中更好地应对新的需求和挑战。此外，还应考虑国际形势，尤其是高尖企业，受制裁后工具许可与AE支持的不可持续性。如有国产化替代工具可在满足需求的情况下引入替代，降低可能被制裁产生的影响。
    
2. **EDA工具的调试和维护**：
    
    在EDA工具的使用过程中，难免会遇到各种问题，如崩溃、错误、性能下降等。因此，在使用EDA工具的过程中，需要对其进行调试和维护。调试和维护的过程包括：
    
    - 发现并记录问题
    - 分析和定位问题
    - 解决问题
    - 验证和测试解决方案
    - 文档记录和分享经验

只有通过这些步骤的循环迭代，才能保证EDA工具的稳定性和可靠性，从而更好地支持IC设计的整个流程。但像小设计团队的EDA工具选型，比较简单：能用就行，遇到问题再换。原因有二，一是没有足够的人力与时间去做详细的选型，二是没有太多的历史项目，因此很少文档记录与经验积累。

1. **EDA工具的环境管理：**以c shell为例（这是IC设计最常用的shell之一），大概会经历几个阶段：
    - .cshrc阶段：
        
        小团队，往往会以.cshrc文件开始定制，将shell的初始化、项目环境、工具环境以及License的初始化都放在.cshrc文件里
        
    - project cshrc阶段：
        
        随着团队的增长，每个人的.cshrc会出现各不相同的情况，容易出现各种问题。这时会将公共的设置，抽出来放到project.cshrc文件。
        
    - Environment Modules阶段：
        
        随着项目数量的增长，此时单纯地拷贝.cshrc与project.cshrc必然要出问题了。可以借助Environment Modules，它可以帮助IC设计环境中的工具环境管理。
        
        Environment Modules是一类开源工具，它有两种实现（TCL与Lua），TCL实现得较早用户量多。可以在Unix/Linux系统中管理用户环境，包括环境变量、路径、别名等。在IC设计环境中，可以使用Environment Modules来管理不同版本的EDA工具和其他开源工具的环境，以及不同的项目环境。通过使用Environment Modules，可以避免环境变量和路径的冲突，使得不同的工具和项目可以协调工作。
        
        我们常用它来做工具环境初始化，包括工具变量设置，alias，工具冲突自动卸载；项目环境初始化，包括项目变量与路径设置，工具组合设置，研发目录初始化等。
        
    - Environment Modules + Wrapper 或 Environment Modules + 定制ELF文件 + Wrapper阶段
        
        问题：IC设计环境的工具数量众多，同时加载的工具越多，命令与共享库冲突概率越大。但是人都是有惰性的，可能要用的都加载上（不做选择，全都要），只做加法，不做减法。有些做的好的厂商，如Cadence，它避免了用户去做共享库路径的设置，只要求用户设置可执行命令路径到PATH变量。但有些厂商做的烂一些，连共享库都与可执行命令放在同一个文件夹下。
        
        方案：通过Wrapper，将启动命令需要的环境，在Wrapper中定制好。通过Wrapper启动命令；还可以定制ELF文件的rpath，将其需要的共享库所在路径写进去。这两种方式，可有效地避免工具中的共享库路径暴露在shell环境中，降低了共享库冲突的概率。
        
    1. EDA工具的生命周期管理
        
        使用EDA工具，我们一般关注安装与配置，不关注删除。随着时间的推移，一些老旧的工具版本不再使用，这时可以走下架或归档流程。
        

## 开源工具的管理

注：这里说的开源工具，叫开源包更合适。我们这里只介绍非操作系统仓库提供的开源包，因为操作系统仓库提供的开源包，安装与管理相对容易。

- 开源工具的选型
    
    开源工具一般是由研发用户提申请，管理员确认后安装。由于开源工具很自由，内部使用对选型不做太多的限制。
    
    但在做软件集成产品，对外出售或对外提供服务的，则需要考虑开源工具的许可。各种开源许可的介绍：
    
    开源许可证是规定开源软件使用和发布条件的法律条款，其核心目的是保证开源软件的源代码和衍生作品能够被其他人自由地使用、修改和发布。常见的开源许可证包括：
    
    - GPL（GNU通用公共许可证）
    - LGPL（GNU宽通用公共许可证）
    - BSD（Berkeley软件分发许可证）
    - MIT（麻省理工学院许可证）
    - Apache许可证
    
    GPL和LGPL是最为严格的开源许可证，要求所有使用和发布的软件都必须采用GPL或LGPL协议，也就是说，必须在源代码的基础上进行发布，不允许闭源或专有化。BSD和MIT许可证则相对宽松，只要求在软件中包含许可证和版权声明即可，可以闭源或专有化。Apache许可证则介于两者之间，要求在修改和发布软件时必须保留许可证和版权声明，但可以闭源或专有化。
    
    在选择开源许可证时，需要根据具体情况来进行选择，考虑到软件的商业价值、使用范围、安全性、社区支持等因素。同时，还需要注意开源许可证之间的兼容性，避免出现不兼容的情况。例如，GPL和LGPL许可证是“传染性”的，意味着如果一个软件采用了GPL或LGPL许可证，那么其衍生作品也必须采用相同的许可证，否则就会出现不兼容的情况。
    
    更详细的介绍可以参考[阮一峰的博客](http://www.ruanyifeng.com/blog/2011/05/how_to_choose_free_software_licenses.html)。
    
- 开源工具的调试和维护
    
    开源工具由于没有AE的支持（也有例外的，如红帽的RHEL订阅服务），安装调试与维护均需靠使用方自己完成。如果有编译GCC或者QT的同学，就会深有体会。
    
    这里介绍两款自动化的开源包管理器：
    
    ### Spack
    
    [Spack](https://spack.readthedocs.io/en/latest/)是一个灵活的开源软件包管理器，它可以管理多个版本的软件包，支持多种不同的平台和架构。Spack使用类似于Linux软件包管理器的命令行界面，可以方便地安装、升级、卸载和配置软件包。Spack还支持模块化设计，可以方便地管理和加载不同版本的软件包和依赖库。
    
    ### EasyBuild
    
    [EasyBuild](https://easybuild.io/)是一个开源的软件包管理器，它可以自动化地构建和安装软件包。EasyBuild支持多种不同的平台和架构，可以自动解决依赖关系并构建软件包。EasyBuild还提供了一个易于使用的命令行界面和Python API，可以方便地管理和定制软件包的构建过程。EasyBuild还支持模块化设计，可以方便地管理和加载不同版本的软件包和依赖库。
    
    这两款开源包管理器都可以用于IC设计环境中的开源工具管理，可以提高工作效率，降低管理成本。
    
    常见的yum，pip包管理器，每平台上源码与二进制是1:1关系，二进制要尽可能地可移植，整个生态系统用相同的工具链（编译器与运行时共享库）。不是对每个CPU微架构做优化的，性能优化让步于可移植性。
    
    相比之下，Spack与EasyBuild这两款开源包管理器有什么优势？后者可以支持在同一个目录下，多CPU架构，多操作系统，多编译器，多工具版本共存，并且使用Python为用户提供了易用的框架来增加自己想要管理的包。
%20%20%20%20%20![](/assets/img/Pasted%20image%2020230405221952.png)
    
    我个人在工作做使用Spack，对Spack的基础功能，[离线使用](https://www.icinfra.cn/blog/2023/offline-packages-installing/)等有经验积累。Spack安装的开源包，它自动做了依赖包的DAG生成、安装与设置，并且通过[rpath](https://spack.readthedocs.io/en/latest/packaging_guide.html#handling-rpaths)设置了共享库路径。Spack还可以enable [Environment Modules](https://spack.readthedocs.io/en/latest/module_file_support.html#write-a-configuration-file)的TCL and/or Lua实现，通过其一的方式来加载。Spack除了可管理开源社区的包，还可以将自己开发的[包用Spack管理](https://spack.readthedocs.io/en/latest/packaging_guide.html#packaging-guide)。

Spack管理超过6700个包，[数据来源](https://spack-tutorial.readthedocs.io/en/latest/_downloads/f2db2edf0050d1d82fdcd0d89cc6cd48/spack-cineca23-tutorial-slides.pdf)
%20%20%20%20![](/assets/img/Untitled.png)

Mirror机制：解决离线IC研发环境的开源包管理
%20%20%20%20![](/assets/img/Untitled%201.png)
    

Spack concretizer：（依赖生成器）借助了clingo工具。[clingo的介绍](https://potassco.org/doc/start/)，[在线体验](https://potassco.org/clingo/run/)。



## 结论

- 总结EDA工具和开源工具的管理
- 展望EDA工具和开源工具在未来的发展