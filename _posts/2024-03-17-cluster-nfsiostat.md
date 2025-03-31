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

# fs to mountpoint
fs2mp = {
"192.168.10.1:/nfs001": "home",
"192.168.10.1:/nfs002": "tools",
"192.168.10.2:/nfs003": "proj",

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
    client.connect(hostname=host, username=username, port=36000)
    stdin, stdout, stderr = client.exec_command('nfsiostat 2 2')

    # 等待第一次报告的输出并忽略
    while not stdout.channel.recv_ready():
        time.sleep(1)  # 轮询等待输出
    first_output = stdout.channel.recv(1000000)  # 读取并丢弃第一次输出
    print(f"{host} 接收到第一次数据。")
    #print(first_output.decode())

    # 等待并读取第二次结果
    time.sleep(2)

    # 接收第二次
    output = b""
    while not stdout.channel.eof_received:
        try:
            chunk = stdout.channel.recv(4096)
            if not chunk:
                break
            output += chunk
        except Eception as e:
            print(f"接收第二次时发生错误{e}")
            break
    print(f"{host} 第二次结果")
    output = output.decode()
    #print(f"output {output}")
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
    # Generating the Excel file name with a timestamp
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    excel_filename = f"nfsiostat_data_{current_time}.xlsx"

    with pd.ExcelWriter(excel_filename, engine='xlsxwriter') as writer:
        workbook = writer.book
        for mount_point in df_unique['mount_point'].unique():
            df_mp = df_unique[df_unique['mount_point'] == mount_point]

            # 对每个server保留op/s最高的记录
            df_mp = df_mp.sort_values(by='op/s', ascending=False).drop_duplicates(subset=['server'], keep='first')

            # 对指定列进行降序排序
            if 'write_kB/s' in df_mp.columns and 'read_kB/s' in df_mp.columns:
                df_mp = df_mp.sort_values(by=['write_kB/s', 'read_kB/s'], ascending=[False, False])
            
            # 创建工作表并写入数据
            if mount_point in fs2mp:
                sheet_name = fs2mp[mount_point]
            else:
                sheet_name = mount_point.replace(":/", "_")[0:31]
            df_mp.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # 获取工作表对象
            worksheet = writer.sheets[sheet_name]
            
            # 锁定第一行
            worksheet.freeze_panes(1, 0)

            # 自动调整列宽
            for column in df_mp:
                column_length = max(df_mp[column].astype(str).map(len).max(), len(column))
                col_idx = df_mp.columns.get_loc(column)
                worksheet.set_column(col_idx, col_idx, column_length)
            
            # Identify numeric columns and exclude specific ones from sum calculation
            numeric_cols = df_mp.select_dtypes(include=['number']).columns
            numeric_cols = numeric_cols.drop(['read_avg RTT(ms)', 'read_avg exe(ms)', 'write_avg RTT(ms)', 'write_avg exe(ms)'], errors='ignore')  # Exclude specific columns
            sum_row = df_mp[numeric_cols].sum().to_dict()
            sum_row = {col: sum_row.get(col, '') for col in df_mp.columns}  # Include empty values for non-numeric columns
            df_sum = pd.DataFrame([sum_row])
            startrow = len(df_mp) + 1
            df_sum.to_excel(writer, sheet_name=sheet_name, startrow=startrow, index=False, header=False)
            
            # Format the sum row
            sum_format = workbook.add_format({'bold': True})
            for col_num, value in enumerate(df_sum.columns):
                worksheet.write(startrow, col_num, sum_row[value], sum_format)
    
    print(f"Data has been outputted to Excel file at {excel_filename}")

if __name__ == "__main__":
    main()
```
