---
layout: post
title:  集群运行nfsiostat收集信息并分析
date:   2024-03-17 20:25:00+0800
description: 
tags: storage
giscus_comments: true
categories: icenv
---

工作中偶遇到NFS Server中IO hang，这里提供一个在集群中批量运行nfsiostat命令，并收集信息保存至csv文件进行分析。也可以修改下，定期将数据推送至ElasticSearch，记录时序数据以做进一步分析。

```python

import re
import paramiko
import pandas as pd
from io import StringIO

# Server information list
servers = [
    {"host": "192.168.1.10", "username": "root"},
    {"host": "192.168.1.11", "username": "root"},
]

ops_pattern = r'\b[\d.]+(?: \([\d.]+\))?|\d+ \(.*?\)'

# Execute nfsiostat and get the results
def get_nfsiostat(host, username):
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
    for i in range(0, len(lines), 9):
        if i + 8 < len(lines):
            mount_point = "/".join(lines[i+1].strip().split("/")[0:2])
            ops_rpc = lines[i+4].strip().split()
            matches = re.findall(ops_pattern, lines[i+6])
            read_ops = [float(num) if '.' in num else num for num in matches]
            matches = re.findall(ops_pattern, lines[i+8])
            write_ops = [float(num) if '.' in num else num for num in matches]
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

# Main program
def main():
    all_data = []
    for server in servers:
        output = get_nfsiostat(server['host'], server['username'])
        nfs_data = parse_nfsiostat_output(server['host'], output)
        all_data.extend(nfs_data)
    
    # Convert data to DataFrame for easier processing
    df = pd.DataFrame(all_data)
    
    # Removing duplicates, keeping only unique records
    df_unique = df.drop_duplicates()

    # Output to CSV file
    csv_filename = "nfsiostat_data.csv"
    df_unique.to_csv(csv_filename, index=False)
    print(f"Data has been outputted to CSV file at {csv_filename}")

if __name__ == "__main__":
    main()
```
