---
layout: post
title: 解析FLEXlm lmutil lmstat输出并保存
date: 2023-10-24 23:34+0800
description: 
tags: license
giscus_comments: true
categories: icenv
---

## 数据库表设计
1. **user 表**:

| 列名      | 数据类型        | 说明       |
| --------- | --------------- | ---------- |
| id        | INTEGER PRIMARY KEY | 主键      |
| username  | TEXT            | 用户名     |


2. **server 表**:

| 列名      | 数据类型        | 说明       |
| --------- | --------------- | ---------- |
| id        | INTEGER PRIMARY KEY | 主键      |
| hostname  | TEXT            | 主机名     |


3. **vendor 表**:

| 列名               | 数据类型        | 说明       |
| ------------------ | --------------- | ---------- |
| id                 | INTEGER PRIMARY KEY | 主键      |
| vendor_daemon_name | TEXT            | 供应商守护进程名 |


4. **license_type 表**:

| 列名      | 数据类型        | 说明       |
| --------- | --------------- | ---------- |
| id        | INTEGER PRIMARY KEY | 主键      |
| type      | TEXT            | 许可类型   |


5. **feature 表**:

| 列名         | 数据类型        | 说明       |
| ------------ | --------------- | ---------- |
| id           | INTEGER PRIMARY KEY | 主键      |
| feature_name | TEXT            | 特性名称   |


6. **license_usage_log 表**:

| 列名           | 数据类型        | 说明                  |
| -------------- | --------------- | --------------------- |
| id             | INTEGER PRIMARY KEY | 主键                 |
| user_id        | INTEGER        | 用户ID，外键           |
| workstation_id | INTEGER        | 工作站ID，外键          |
| sessionid      | INTEGER        | sessionid，从日志条目解析出来的                |
| start_time     | TEXT           | 开始时间              |
| end_time       | TEXT           | 结束时间              |
| vendor_id      | INTEGER        | vendor ID，外键         |
| lic_server_id  | INTEGER        | license server ID，外键    |
| lic_type_id    | INTEGER        | license_type ID，外键        |
| feature_id     | INTEGER        | feature ID，外键           |
| additional_key | TEXT           | 部分feature有额外的key                |


每个表格通过主键和外键相互关联，为日志解析和数据存储提供结构支持。

## 初始化数据库
```python3
#!/Users/wanlinwang/spack/opt/spack/darwin-ventura-m1/apple-clang-14.0.3/python-3.10.8-b7rgkczw4yfgrkbgttbcbur3ksmwho5d/bin/python3


import sqlite3

conn = sqlite3.connect('license_logging.db')  # 创建或连接到license.db数据库
cursor = conn.cursor()

# 创建user表
cursor.execute('''
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY,
    username TEXT
)
''')

# 创建server表
cursor.execute('''
CREATE TABLE IF NOT EXISTS server (
    id INTEGER PRIMARY KEY,
    hostname TEXT
)
''')

# 创建vendor表
cursor.execute('''
CREATE TABLE IF NOT EXISTS vendor (
    id INTEGER PRIMARY KEY,
    vendor_daemon_name TEXT
)
''')

# 创建license_type表
cursor.execute('''
CREATE TABLE IF NOT EXISTS license_type (
    id INTEGER PRIMARY KEY,
    type TEXT
)
''')

# 创建feature表
cursor.execute('''
CREATE TABLE IF NOT EXISTS feature (
    id INTEGER PRIMARY KEY,
    feature_name TEXT
)
''')

# 创建license_usage_log表，它将其他表关联起来
cursor.execute('''
CREATE TABLE IF NOT EXISTS license_usage_log(
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    workstation_id INTEGER,
    sessionid INTEGER,
    start_time TEXT,
    end_time TEXT,
    vendor_id INTEGER,
    lic_server_id INTEGER,
    lic_type_id INTEGER,
    feature_id INTEGER,
    additional_key TEXT,
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(workstation_id) REFERENCES server(id),
    FOREIGN KEY(vendor_id) REFERENCES vendor(id),
    FOREIGN KEY(lic_server_id) REFERENCES server(id),
    FOREIGN KEY(lic_type_id) REFERENCES license_type(id),
    FOREIGN KEY(feature_id) REFERENCES feature(id)
)
''')

conn.commit()  # 提交创建表的操作
conn.close()  # 关闭数据库连接

```

## 定期执行，存入/更新数据库
```python3
#!/Users/wanlinwang/spack/opt/spack/darwin-ventura-m1/apple-clang-14.0.3/python-3.10.8-b7rgkczw4yfgrkbgttbcbur3ksmwho5d/bin/python3


import sqlite3
import subprocess
import re
from datetime import datetime

DB_PATH = 'license_logging.db'

def run_lmstat(CDS_LIC_FILE):
    cmd = r"lmstat -a -c {CDS_LIC_FILE}"
    return subprocess.check_output(cmd, shell=True).decode('utf-8')

def extract_data_from_output(output):
    features_data = []
    lines = output.split('\n')
    current_feature = None
    for line in lines:
        if 'Users of' in line:
            # Get the feature name
            current_feature = line.split()[2].strip(':')
            lic_type = "unknown"
        elif current_feature and current_feature in line:
            vendor_info = re.search(r'.*vendor:\s*(\w+).*', line)
            if vendor_info:
                current_vendor = vendor_info.group(1)
        elif "floating license" in line:
            lic_type = "floating license"
        elif current_feature and ', start' in line:
            # 格式"user_01 y260.ic.cn y260.ic.cn:1.0 Xcelium Single Core Engine (v21.000) (y162/5280 801), start Thu 10/19 9:57"
            user_info = re.search(r'(\w+)\s+([\w.]+)\s+[\w.]*:[\d.]+\s+[^(]*\(([\w.]+)\)\s+\(([\w]+)/(\d+)\s+(\d+)\),\s*start\s*(\w+ \d+/\d+ \d+:\d+)', line)
            if user_info:
                start_time = datetime.strptime(user_info.group(7), "%a %m/%d %H:%M").replace(year=datetime.now().year)
                if start_time > datetime.now(): start_time = start_time.replace(year=start_time.year - 1)

                features_data.append({
                    "feature": current_feature,
                    "vendor": current_vendor,
                    "lic_type": lic_type,
                    "username": user_info.group(1),
                    "workstation": user_info.group(2),
                    "version": user_info.group(3),
                    "lic_server": user_info.group(4),
                    "port": user_info.group(5),
                    "sessionid": user_info.group(6),
                    "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S")
                })
    return features_data

def get_or_insert_id(cursor, table, column, value):
    cursor.execute(f'SELECT id FROM {table} WHERE {column}=?', (value,))
    result = cursor.fetchone()
    if not result:
        cursor.execute(f'INSERT INTO {table}({column}) VALUES (?)', (value,))
        return cursor.lastrowid
    return result[0]

def update_database(data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    for entry in data:
        # Resolve foreign key dependencies
        user_id = get_or_insert_id(cursor, 'user', 'username', entry['username'])
        feature_id = get_or_insert_id(cursor, 'feature', 'feature_name', entry['feature'])
        vendor_id = get_or_insert_id(cursor, 'vendor', 'vendor_daemon_name', entry['vendor'])
        lic_type_id = get_or_insert_id(cursor, 'license_type', 'type', entry['lic_type'])
        workstation_id = get_or_insert_id(cursor, 'server', 'hostname', entry['workstation'])
        lic_server_id = get_or_insert_id(cursor, 'server', 'hostname', entry['lic_server'])

        # Check if entry exists in license_usage_log
        cursor.execute('''SELECT id FROM license_usage_log WHERE feature_id=? AND start_time=? AND sessionid=?''',
                       (feature_id, entry["start_time"], entry["sessionid"]))
        log_id = cursor.fetchone()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if log_id:
            # Update end_time
            cursor.execute('UPDATE license_usage_log SET end_time=? WHERE id=?', 
                           (timestamp, log_id[0]))
        else:
            # Insert new entry
            cursor.execute('''
                INSERT INTO license_usage_log(user_id, workstation_id, start_time, end_time, vendor_id, lic_server_id, lic_type_id, feature_id, sessionid) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                (user_id, workstation_id, entry["start_time"], timestamp, vendor_id, lic_server_id, lic_type_id, feature_id, entry["sessionid"]))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    CDS_LIC_FILE="5280@lic-server-01:5280@lic-server-02"
    all_output = run_lmstat(CDS_LIC_FILE)
    for output in re.split(r"-{8,}", all_output)
        data = extract_data_from_output(output)
        update_database(data)

```

## 测试数据
```bash
    output = """Users of Affirma_sim_analysis_env:  (Total of 8 licenses issued;  Total of 3 licenses in use)

  "Affirma_sim_analysis_env" v23.0, vendor: cdslmd, expiry: 15-jan-2024
  vendor_string: UHD:PERM
  floating license

    user_01 TENCENT64.site :11 (v16.000) (lic460/5280 101), start Wed 10/18 12:37
    user_02 server-0431840.ic.cn server-0431840.ic.cn:1.0 (v16.000) (lic460/5280 716), start Wed 10/18 17:24
    user_03 server-2381620.ic.cn server-2381620.ic.cn:4.0 (v16.000) (lic460/5280 2123), start Thu 10/19 6:56

Users of Xcelium_Single_Core:  (Total of 8 licenses issued;  Total of 3 licenses in use)

  "Xcelium_Single_Core" v21.000, vendor: cdslmd, expiry: 15-jan-2024
  vendor_string: UHD:PERM
  floating license

    user_03 TENCENT64.site :11 Xcelium Single Core Engine (v21.000) (lic460/5280 101), start Wed 10/18 12:37
    user_02 TENCENT64.site :4 Xcelium Single Core Engine (v21.000) (lic460/5280 301), start Wed 10/18 12:37
    user_01 TENCENT64.site :80 Xcelium Single Core Engine (v21.000) (lic460/5280 401), start Wed 10/18 12:37"""
```
