---
layout: post
title: 使用Python自动化运维ipset与iptables
date: 2022-08-30 22:15:00
comments: true
description: 
tags: post
categories: python
---

## 配置文件

```yaml
host-rules:
- name: normal_computing 
  conf: # 正式员工使用的研发运算机规则
    type: ip
    need_create_ipset: true
    need_create_iptables: true
    hosts: # 主机列表
      - 192.168.1.2
      - 192.168.1.4
      - 172.31.86.213
      - 192.168.1.5
    input: # INPUT方向规则
      - dport: 22,5600
        peer: # INPUT方向规则的来源
        - type: ipset
          value: normal_computing
        - type: ipset
          value: win_jump_server
        - type: ip
          value: 8.8.8.8
    output: # OUTPUT方向规则
      - peer:
          - type: ipset
            value: network_monitor_subnet
      - peer:
          - type: ipset
            value: domain_names
      - peer:
          - type: ipset
            value: normal_computing
      - peer:
          - type: ipset
            value: outsourcing_computing
      - peer:
          - type: ipset
            value: cfs
      - dport: 22
        peer:
          - type: ipset
            value: normal_computing

- name: network_monitor_subnet
  conf:
    type: ip,port
    need_create_ipset: true
    need_create_iptables: false
    hosts:
      - name: 192.168.100.1
        port: tcp:8888

           
- name: outsourcing_computing
  conf: # 外包员工使用的研发运算机规则
    type: ip
    need_create_ipset: true
    need_create_iptables: true
    hosts: # 主机列表
      - 192.168.1.11
    input: # INPUT方向规则
      - dport: 22,5600
        peer: # INPUT方向规则的来源
        - type: ipset
          value: normal_computing
        - type: ipset
          value: win_jump_server

- name: cadence_lic_hosts
  conf: # c家lic
    type: ip
    need_create_ipset: false
    need_create_iptables: true
    hosts:
      - 172.31.86.213
    input: # INPUT方向规则
      - dport: 3000,5280
        peer: # INPUT方向规则的来源
        - type: ipset
          value: normal_computing
        - type: ipset
          value: outsourcing_computing
        - type: ipset
          value: n_gate_subnets

- name: svn_hosts
  conf:
    type: ip
    need_create_ipset: false
    need_create_iptables: true
    hosts:
      - 192.168.1.2
    input: # INPUT方向规则
      - dport: 1690:1697,1699
        peer: # INPUT方向规则的来源
        - type: ipset
          value: normal_computing
      - dport: 1698
        peer: # INPUT方向规则的来源
        - type: ipset
          value: outsourcing_computing

- name: n_gate_subnets
  conf:
    type: net
    need_create_ipset: true
    need_create_iptables: false
    hosts:
      - 172.16.0.1/24
      - 172.16.1.1/24

- name: win_jump_server
  conf:
    type: ip
    need_create_ipset: true
    need_create_iptables: false
    hosts:
      - 1.1.1.1
      - 1.1.1.2

- name: jump_server
  conf:
    type: net
    need_create_ipset: true
    need_create_iptables: false
    hosts:
      - 2.2.2.0/24
      - 2.2.3.0/24

- name: cfs
  conf:
    type: ip,port
    need_create_ipset: true
    need_create_iptables: false
    hosts:
      - name: 1.2.3.4
        port: tcp:111
      - name: 1.2.3.4
        port: tcp:2049

- name: domain_names
  conf:
    type: dns,port
    need_create_ipset: true
    need_create_iptables: false
    hosts:
      - name: mirrors.tencent.com
        port: tcp:80
      - name: mirrors.tecentyun.com
        port: tcp:443
```

## 生成脚本
```python
"""
Author: wanlinwang
Date: 24-Aug-2022 19:00-23:00
Description: 自动化维护iptables与ipset
"""

import yaml
import tempfile
from netifaces import interfaces, ifaddresses, AF_INET
import subprocess
import re
import filecmp


def ip4_addresses():
    ip_list = []
    for interface in interfaces():
        # 有些接口没有IP，使用try跳过它。
        try:
            for link in ifaddresses(interface)[AF_INET]:
                ip=link['addr']
                #去掉本地地址，去掉192.开头的私有地址。
                if ip.startswith('192.') or ip == '127.0.0.1':
                    continue
                ip_list.append(ip)
        except:
            pass
    return ip_list


def dig_domainname_to_ips(domain_name):
    entries = subprocess.run(['dig', '+short', domain_name], stdout=subprocess.PIPE)
    return entries.stdout.decode('utf-8')


def check_if_ip(ip_str):
    if re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip_str):
        return True
    else:
        return False


def create_ipset(set_name, entry_list, set_type, write_file):
    """
    生成ipset配置文件，应用命令如下：
            ipset restore -f ./ipset.conf --exist
    """
    # print('entry_list', entry_list)
    if set_type == 'dns,port':
        set_type = 'ip,port'
        rst_list = []
        for entry in entry_list:
            ip_list = dig_domainname_to_ips(entry['name']).split('\n')
            ip_list.sort()
            for item in ip_list:
                # 只添加是ip的条目
                if check_if_ip(item):
                    rst_list.append(item + "," + entry['port'])
        entry_list = rst_list
    elif set_type == 'ip,port':
        rst_list = []
        for entry in entry_list:
            rst_list.append(entry['name'] + "," + entry['port'])
        entry_list = rst_list


    set_tmp_name = set_name + "_tmp"
    print(f"""
####################################################
create  {set_name}     hash:{set_type} family inet hashsize 1024 maxelem 65536
create  {set_tmp_name} hash:{set_type} family inet hashsize 1024 maxelem 65536
destroy {set_tmp_name}
create  {set_tmp_name} hash:{set_type} family inet hashsize 1024 maxelem 65536\
    """, file=write_file)

    for entry in entry_list:
        print(f"add {set_tmp_name} {entry}", file=write_file)

    print(f"""\
swap {set_tmp_name} {set_name}
destroy {set_tmp_name}
####################################################
    """, file=write_file)


def generate_iptables_entry(direction, ip_type, ips, ipset_dict, ports=None):
    entry = ['-A']
    match_set_arg = ''
    if direction == 'input':
        entry.append('INPUT')
        if ip_type.startswith('ipset'):
            match_set_arg = 'src'
    elif direction == 'output':
        entry.append('OUTPUT')
        if ip_type.startswith('ipset'):
            match_set_arg = 'dst'
            if ipset_dict[ips] == 'ip,port':
                match_set_arg = 'dst,dst'
    else:
        print(f"Error with {direction}")
    
    entry.append(f'-p tcp')
    if ip_type == 'ip':
        entry.append(f'-s {ips}')
    elif ip_type.startswith('ipset'):
        entry.append(f'-m set --match-set {ips} {match_set_arg}')
    else:
        print(f'Error with ip_type {ip_type}')
    # if ip_type == 'ip':
    #     entry.append(f'-s {ips}')
    # elif ip_type.startswith('ipset'):
    #     ip_type = ip_type.replace('ipset,')
    #     if ip_type == 'ip':
    #         entry.append(f'-m set --match-set {ips} {match_set_arg}')
    #     elif ip_type == 'ip,port':
    #         entry.append(f'-m set --match-set {ips} dst,dst')
    # else:
    #     print(f'Error with ip_type {ip_type}')

    if ports:
        if ip_type == 'ipset,ip,port':
            raise 'Conflict with ipset'
        entry.append(f'--dport {ports}')
    
    entry.append(f'-j ACCEPT')

    return ' '.join(entry)


if __name__ == "__main__":
    ipset_conf_tmp    = tempfile.NamedTemporaryFile(mode='w+', prefix='ipset.conf_', dir='./', delete=False)
    iptables_conf_tmp = tempfile.NamedTemporaryFile(mode='w+', prefix='iptables_',   dir='./', delete=False)
    current_host_ips = ip4_addresses()
    print("current host ip", current_host_ips)

    # 将默认开通的iptables条目先写上。

    with open("./config.yml", 'r') as yml:
        conf = yaml.safe_load(yml)
        # print(json.dumps(conf,indent=2))
        # print(conf['host-rules'])
        ipset_type_dict = dict()
        for host_rule in conf['host-rules']:
            # print(json.dumps(host_rule, indent=2))
            host_rule_name = host_rule['name']
            host_rule_conf = host_rule['conf']
            host_rule_conf_type = host_rule_conf['type']
            # 步骤一：首先完成ipset的创建。Done
            if 'need_create_ipset' in host_rule_conf and host_rule_conf['need_create_ipset']:
                create_ipset(host_rule_name, host_rule_conf['hosts'], host_rule_conf_type, ipset_conf_tmp)
                if host_rule_conf_type == 'dns,port':
                    host_rule_conf_type = 'ip,port'
                ipset_type_dict[host_rule_name] = host_rule_conf_type
            
        for host_rule in conf['host-rules']:
            host_rule_name = host_rule['name']
            host_rule_conf = host_rule['conf']
            # 步骤二：然后判断本机属于哪个rule下面，将对应的rule都生成一遍。TODO
            if 'need_create_iptables' in host_rule_conf and host_rule_conf['need_create_iptables']:
                
                for current_ip in current_host_ips:
                    # print(host_rule_conf)
                    # print(host_rule_conf['hosts'])
                    if 'hosts' not in host_rule_conf:
                        print(f'hosts not in {host_rule_name}, please check.')
                        continue
                    if current_ip in host_rule_conf['hosts']:
                        # 分析文件条目
                        # 分析input的
                        for direction in ['input', 'output']:
                            if direction not in host_rule_conf:
                                print(f'{direction} not in {host_rule_name}, please check.')
                            else:
                                for d in host_rule_conf[direction]:
                                    # print('direction', d)
                                    dports = None
                                    if 'dport' in d:
                                        dports = d['dport']

                                    if 'peer' not in d:
                                        print(f'{direction} peer not in {host_rule_name}, please check.')
                                        continue
                                    else:
                                        for item in d['peer']:
                                            ip_type = item['type']
                                            value = item['value']
                                            
                                            # 生成iptables INPUT条目
                                            # print("=============")
                                            print(generate_iptables_entry(direction, ip_type, value, ipset_type_dict, dports), file=iptables_conf_tmp)
    
            # 步骤三：最后再将default的DROP规则写上。TODO


    # 步骤四：生成好ipset.conf与iptables两个文件，与生产环境的文件做对比，
    # 如有变则应用它，并将日志写到日志文件里。TODO
    ipset_conf_tmp.close()
    iptables_conf_tmp.close()
    if not filecmp.cmp(ipset_conf_tmp.name, 'ipset.conf'):
        # ipset.conf有更新，执行更新操作
        pass

    if not filecmp.cmp(iptables_conf_tmp.name, 'iptables'):
        # iptables文件有更新，执行更新操作
        pass
```
