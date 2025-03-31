---
layout: post
title: merge synopsys license file
date: 2023-08-22 22-04-58 22:04:58+0800
description: 
tags: license
giscus_comments: true
categories: icenv
---



# 对Synopsys License File的管理

1. 修改从Synopsys获取的密钥：

   - 只能修改许可证文件中的SERVER和VENDOR行，确保SERVER行包含正确的服务器主机名，VENDOR行包含snpslmd守护程序的完整路径。
   - 任何更改都必须以ASCII文本格式保存。
   - 不要添加、删除或修改许可证文件中的任何INCREMENT行，这样做会使License无效。
   - 如果从Synopsys获取临时密钥，可以将其附加到现有购买的License文件中，但需要删除重复的SERVER、VENDOR和USE_SERVER行。

1. 使用sssverify程序验证密钥：

   - 在使用来自Synopsys的任何新密钥文件之前，运行"SCL sssverify"实用程序来检查文件中的任何错误。
   - 如果License文件没有错误，您将看到类似以下消息的输出："License file integrity check PASSED"。
   - 如果License文件损坏，您将收到相应的错误消息，并建议不使用该License文件。

1. 确认SCL正在提供License Feature：

   - 检查SCL服务器调试日志文件以查找启动错误。
   - 确保lmgrd和snpslmd已正确启动，没有出现"SSS"错误。
   - 如果调试日志文件中存在与SSS相关的错误消息，需要采取相应的措施来解决问题。多个Synopsys License被管理员合并完后，经常出现如下错误。请确保每个License File含[0,1]个SSS feature块，以及[0,n]个SSST feature块。
     ![image](https://github.com/icinfra/icinfra.github.io/assets/32032219/315ab578-6172-4dfa-a9c8-5effea716657)


1. 管理临时密钥：

   - 临时密钥需要SSST功能。最好放在单独的服务器，以防止其被后续的生产密钥覆盖。
   - 添加或删除临时密钥时，必须作为一个块进行操作，而不是单独处理每个密钥。

这些是对License管理的一些重要事项的总结。详细的指南和步骤可以在提供的PDF文档中找到。

不像Cadence家每个hostid提供一个完整的License文件，Synopsys家的License是可合并的（一个购买的，与一个或多个临时的合并，除此之外的其余场景避免合并）。这里提供合并脚本，供参考：

新版本
```python3
#!/bin/env python3
# Author: wanlinwang
# Date: 27-Dec-2023
# Synopsys License文件合并，遵循：合并后的文件，保留最多一个有效期内的SSS及其feature，保留零个或多个有效期内的SSST及其feature。

# 程序流程图
"""
+---------------------------+
| Parse Command Line Args   |
| - Use argparse            |
| - Accept -i and -o flags  |
+---------------------------+
             |
             V
+---------------------------+
| Read and Parse License    |
| Files                     |
| - Read each input file    |
| - Split into feature      |
|   blocks                  |
| - Parse for name, trans-  |
|   action ID, and exp. date|
+---------------------------+
             |
             V
+---------------------------+
| Process and Merge         |
| Features                  |
| - Classify as SSS or SSST |
| - Keep latest non-expired |
|   SSS & related features  |
| - Keep all non-expired    |
|   SSST & related features |
+---------------------------+
             |
             V
+---------------------------+
| Output Merged License     |
| Content                   |
| - Write to specified      |
|   output file             |
+---------------------------+
"""

import argparse
import re
from datetime import datetime

def parse_feature_block(block):
    feature_name_and_expiration_date = re.search(r"INCREMENT (\w+) \w+ \S+ (\d{2}-\w{3}-\d{4})", block)
    transaction_id_match = re.search(r"SN=[RT]K:[\w-]+:[\w-]+:(\d+)", block)

    feature_name    = feature_name_and_expiration_date.group(1) if feature_name_and_expiration_date else None
    expiration_date = feature_name_and_expiration_date.group(2) if feature_name_and_expiration_date else None
    transaction_id  = transaction_id_match.group(1) if transaction_id_match else None

    expiration_date = datetime.strptime(expiration_date, "%d-%b-%Y") if expiration_date else None

    return {
        "name": feature_name,
        "transaction_id": transaction_id,
        "expiration_date": expiration_date,
        "block": block
    }

def parse_license_file(file_content):
    blocks = re.split(r'(?<!#)INCREMENT', file_content)[1:]
    blocks = [f"INCREMENT {b.strip()}" for b in blocks]
    return [parse_feature_block(block) for block in blocks]

def is_block_expired(block):
    return block['expiration_date'] and datetime.now() > block['expiration_date']

def merge_features(license_files_contents):
    all_blocks = []
    for file_content in license_files_contents:
        all_blocks.extend(parse_license_file(file_content))

    sss_blocks = [b for b in all_blocks if b['name'] == 'SSS' and not is_block_expired(b)]
    ssst_blocks = [b for b in all_blocks if b['name'] == 'SSST' and not is_block_expired(b)]

    # Keep only the latest SSS block
    if sss_blocks:
        latest_sss = max(sss_blocks, key=lambda b: b['expiration_date'])
        sss_transaction_id = latest_sss['transaction_id']
        sss_related_blocks = [b for b in all_blocks if b['transaction_id'] == sss_transaction_id]
    else:
        sss_related_blocks = []

    # Keep all non-expired SSST blocks and their associated features
    ssst_transaction_ids = set(b['transaction_id'] for b in ssst_blocks)
    ssst_related_blocks = [b for b in all_blocks if b['transaction_id'] in ssst_transaction_ids]

    merged_content = [b['block'] for b in sss_related_blocks + ssst_related_blocks]

    return "\n".join(merged_content)

def main():
    parser = argparse.ArgumentParser(description="Merge Synopsys license files.")
    parser.add_argument('-i', '--input', nargs='+', required=True, help="Input license files")
    parser.add_argument('-o', '--output', required=True, help="Output merged license file")

    args = parser.parse_args()
    license_files = args.input
    output_file = args.output

    license_contents = [open(file_path, 'r').read() for file_path in license_files]

    merged_license = merge_features(license_contents)
    with open(output_file, "w") as f:
        f.write(merged_license)

if __name__ == "__main__":
    main()

```

旧版本
```python
#!/bin/python3

# Author: wanlinwang
# Date: 23-Aug-2023
# 本程序对未到期的feature进行合并。TODO：尚未考虑多个SSS与SSST块的场景，26-Dec-2023

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
[Synopsys License Verification](https://www.synopsys.com/content/dam/synopsys/support/documents/licensing/scl-license-verification.pdf)
