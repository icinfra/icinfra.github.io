---
layout: post
title:  集群运行nfsiostat收集信息并分析
date:   2024-03-17 20:25:00+0800
description: 
tags: storage
giscus_comments: true
categories: icenv
---

工作中偶遇到NFS Server中IO hang，这里提供一个在集群中批量运行nfsiostat命令，并收集信息保存至excel文件，按nfs server分sheet，锁定第一行，并对每一列汇总。

也可以进一步定制，定期将数据推送至ElasticSearch，记录时序数据以做进一步分析。

```python
# wanlinwang
# 2024-03-17

import re
import paramiko
import pandas as pd
from io import StringIO
from concurrent.futures import ThreadPoolExecutor

# Server information list
servers = [
"192.168.10.1",
"192.168.10.2",
]

ops_pattern = r'\b[\d.]+(?: \([\d.]+\))?|\d+ \(.*?\)'

# Execute nfsiostat and get the results
def get_nfsiostat(host, username="root"):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, port=22)
    stdin, stdout, stderr = client.exec_command('nfsiostat')
    output = stdout.read().decode()
    client.close()
    return output

# Parse nfsiostat output
def parse_nfsiostat_output(server, output):
    data = []
    output_io = StringIO(output)
    lines = output_io.readlines()
    lines = [line for line in lines if line.strip() != ""]
    for i in range(0, len(lines), 7):
        if i + 5 < len(lines):
            #mount_point = "/".join(lines[i].strip().split("/")[0:2])
            mount_point = "/".join(re.split('/| ', lines[i].strip())[0:2])
            ops_rpc = lines[i+2].strip().split()
            matches = re.findall(ops_pattern, lines[i+4])
            read_ops = [float(num) if '.' in num else int(num) for num in matches]
            matches = re.findall(ops_pattern, lines[i+6])
            write_ops = [float(num) if '.' in num else int(num) for num in matches]
            data.append({
                "server": server,
                "mount_point": mount_point,
                "op/s": ops_rpc[0],
                "rpc bklog": ops_rpc[1],
                "read_ops/s": read_ops[0], "read_kB/s": read_ops[1], "read_kB/op": read_ops[2],
                "read_retrans": read_ops[3], "read_retrans%": str(read_ops[4]) + "%", "read_avg RTT(ms)": read_ops[5], "read_avg exe(ms)": read_ops[6],
                "write_ops/s": write_ops[0], "write_kB/s": write_ops[1], "write_kB/op": write_ops[2],
                "write_retrans": write_ops[3], "write_retrans%": str(write_ops[4]) + "%", "write_avg RTT(ms)": write_ops[5], "write_avg exe(ms)": write_ops[6]
            })
    return data

# Function to fetch and parse nfsiostat output for a single server
def fetch_and_parse_nfsiostat(server):
    output = get_nfsiostat(server)
    return parse_nfsiostat_output(server, output)

# Main program using ThreadPoolExecutor for concurrency
def main():
    all_data = []
    with ThreadPoolExecutor(max_workers=len(servers)) as executor:
        futures = [executor.submit(fetch_and_parse_nfsiostat, server) for server in servers]
        for future in futures:
            all_data.extend(future.result())
    
    # Convert data to DataFrame for easier processing
    df = pd.DataFrame(all_data)
    
    # Removing duplicates, keeping only unique records
    df_unique = df.drop_duplicates()

    # Output to Excel file with different mount_points on different sheets
    excel_filename = "nfsiostat_data.xlsx"
    with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
        workbook = writer.book
        for mount_point in df_unique['mount_point'].unique():
            df_mp = df_unique[df_unique['mount_point'] == mount_point]
            
            # 对指定列进行降序排序
            if 'write_kB/s' in df_mp.columns and 'read_kB/s' in df_mp.columns:
                df_mp = df_mp.sort_values(by=['write_kB/s', 'read_kB/s'], ascending=[False, False])
            
            # 创建工作表并写入数据
            sheet_name = mount_point.replace(":/", "_")[0:31]
            df_mp.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # 获取工作表对象
            worksheet = writer.sheets[sheet_name]
            
            # 锁定第一行
            worksheet.freeze_panes(1, 0)
            
            # 寻找数字列并求和
            numeric_cols = df_mp.select_dtypes(include=['number']).columns
            sum_row = df_mp[numeric_cols].sum().to_dict()
            sum_row = {col: sum_row.get(col, '') for col in df_mp.columns}  # 包含非数字列的空值
            df_sum = pd.DataFrame([sum_row])
            df_sum.to_excel(writer, sheet_name=sheet_name, startrow=len(df_mp) + 1, index=False, header=False)
            
            # 格式化求和行
            sum_format = workbook.add_format({'bold': True})
            for col_num, value in enumerate(df_sum.columns):
                worksheet.write(len(df_mp) + 1, col_num, sum_row[value], sum_format)
    
    print(f"Data has been outputted to Excel file at {excel_filename}")

if __name__ == "__main__":
    main()
```
