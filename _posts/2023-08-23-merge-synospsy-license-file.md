---
layout: post
title: merge synopsys license file
date: 2023-08-22 22-04-58 22:04:58+0800
description: 
tags: license
giscus_comments: true
categories: icenv
---



# 对Synopsys License管理

1. 修改从Synopsys获取的密钥：

   - 只能修改许可证文件中的SERVER和VENDOR行，确保SERVER行包含正确的服务器主机名，VENDOR行包含snpslmd守护程序的完整路径。
   - 任何更改都必须以ASCII文本格式保存。
   - 不要添加、删除或修改许可证文件中的任何INCREMENT行，这样做会使许可证无效。
   - 如果从Synopsys获取临时密钥，可以将其附加到现有的许可证文件中，但需要删除重复的SERVER、VENDOR和USE_SERVER行。

1. 使用sssverify实用程序验证密钥：

   - 在使用来自Synopsys的任何新密钥文件之前，运行"SCL sssverify"实用程序来检查文件中的任何错误。
   - 如果许可证文件没有错误，您将看到类似以下消息的输出："License file integrity check PASSED"。
   - 如果许可证文件损坏，您将收到相应的错误消息，并建议不使用该许可证文件。

1. 确认SCL正在提供许可证：

   - 检查SCL服务器调试日志文件以查找启动错误。
   - 确保lmgrd和snpslmd已正确启动，没有出现"SSS"错误。
   - 如果调试日志文件中存在与SSS相关的错误消息，需要采取相应的措施来解决问题。

1. 管理临时密钥：

   - 临时密钥需要SSST功能。维护一个单独的服务器来存储临时密钥，以防止其被后续的生产密钥无效化。
   - 添加或删除临时密钥时，必须作为一个块进行操作，而不是单独处理每个密钥。

这些是对License管理的一些重要事项的总结。详细的指南和步骤可以在提供的PDF文档中找到。

不像Cadence家每个hostid提供一个完整的License文件，Synopsys家的License是可合并的。这里提供一个合并脚本，供参考：

```python
#!/bin/python3

# Author: wanlinwang
# Date: 23-Aug-2023

import sys
import datetime

def is_feature_expired(feature):
    # 从INCREMENT行中获取过期日期
    fields = feature.split()
    if len(fields) > 4:
        expire_date_str = fields[4]
        try:
            expire_date = datetime.datetime.strptime(expire_date_str, '%d-%b-%Y').date()
            today = datetime.date.today()
            return expire_date < today
        except ValueError:
            return False  # 如果日期格式不正确或不存在，我们将其视为未过期
    return False

def merge_license_files(filenames):
    header_lines = []
    features = []

    for index, filename in enumerate(filenames):
        with open(filename, 'r') as f:
            content = f.read().strip()

            # 对于第一个license文件，获取所有非INCREMENT行作为header
            # 对于第二个及以后的license文件，只获取注释行
            if not header_lines or index > 0:
                for line in content.split("\n"):
                    if not line.startswith("INCREMENT"):
                        # 只从第二个及之后的文件中获取注释行
                        if index == 0 or line.startswith("#"):
                            header_lines.append(line)
                    else:
                        break

            feature_blocks = content.split("INCREMENT")  # 假设每个feature块是以INCREMENT开始
            for feature in feature_blocks[1:]:
                feature_with_prefix = "INCREMENT" + feature  # 因为我们通过INCREMENT来分割，所以需要添加回去
                if not is_feature_expired(feature_with_prefix):
                    features.append(feature_with_prefix)

    return "\n".join(header_lines + features)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python merge_licenses.py <output_file> <license_file1> [license_file2 ...]")
        sys.exit(1)
    
    output_file = sys.argv[1]
    license_files = sys.argv[2:]

    merged_content = merge_license_files(license_files)

    with open(output_file, 'w') as f:
        f.write(merged_content)
    
    print(f"Merged licenses saved to {output_file}.")
```

# 参考资料
https://www.synopsys.com/content/dam/synopsys/support/documents/licensing/scl-license-verification.pdf
