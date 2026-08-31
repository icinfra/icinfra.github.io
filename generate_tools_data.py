"""
生成 Cadence Tools 数据用于 Jekyll 展示
将 SQLite 数据库导出为 JSON 格式，供 Jekyll 页面使用
"""

import sqlite3
import json
import sys
from pathlib import Path

DB_PATH = 'cadence_tools.db'
OUTPUT_DIR = Path('_data')

def export_data():
    """导出数据库数据为 JSON"""
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    # 1. 导出主版本列表
    print("导出主版本列表...")
    cursor = conn.execute("""
        SELECT 
            mr.id,
            mr.release_name,
            mr.engineering_name,
            COUNT(DISTINCT sr.id) as version_count,
            COUNT(DISTINCT sros.os_id) as os_count,
            MAX(sr.release_date) as latest_date
        FROM main_release mr
        LEFT JOIN sub_release sr ON mr.id = sr.main_release_id
        LEFT JOIN sub_release_os sros ON sr.id = sros.sub_release_id
        GROUP BY mr.id
        ORDER BY mr.release_name
    """)
    
    main_releases = [dict(row) for row in cursor.fetchall()]
    
    # 2. 导出操作系统列表
    print("导出操作系统列表...")
    cursor = conn.execute("""
        SELECT 
            os.id,
            os.os_name,
            os.os_family,
            COUNT(DISTINCT sr.main_release_id) as tool_count
        FROM operating_system os
        LEFT JOIN sub_release_os sros ON os.id = sros.os_id
        LEFT JOIN sub_release sr ON sros.sub_release_id = sr.id
        GROUP BY os.id
        ORDER BY os.os_family, os.os_name
    """)
    
    operating_systems = [dict(row) for row in cursor.fetchall()]
    
    # 3. 导出完整版本信息（带关联）
    print("导出完整版本信息...")
    cursor = conn.execute("""
        SELECT 
            sr.id,
            sr.release_number,
            sr.release_version,
            sr.release_date,
            sr.release_type,
            sr.platform,
            sr.downloaded,
            sr.export_controlled,
            sr.main_release_id,
            mr.release_name,
            mr.engineering_name,
            GROUP_CONCAT(DISTINCT sros.os_id) as os_ids,
            GROUP_CONCAT(DISTINCT os.os_name) as os_names,
            COUNT(DISTINCT mu.id) as media_count,
            COUNT(DISTINCT ru.id) as resource_count
        FROM sub_release sr
        JOIN main_release mr ON sr.main_release_id = mr.id
        LEFT JOIN sub_release_os sros ON sr.id = sros.sub_release_id
        LEFT JOIN operating_system os ON sros.os_id = os.id
        LEFT JOIN media_url mu ON sr.id = mu.sub_release_id
        LEFT JOIN resource_url ru ON sr.id = ru.sub_release_id
        GROUP BY sr.id
        ORDER BY mr.release_name, sr.release_date DESC
    """)
    
    sub_releases = []
    for row in cursor.fetchall():
        data = dict(row)
        # 转换 os_ids 为数组
        if data['os_ids']:
            data['os_ids'] = [int(x) for x in data['os_ids'].split(',')]
        else:
            data['os_ids'] = []
        # 转换 os_names 为数组
        if data['os_names']:
            data['os_names'] = data['os_names'].split(',')
        else:
            data['os_names'] = []
        sub_releases.append(data)
    
    # 4. 导出统计信息
    print("生成统计信息...")
    stats = {
        'total_tools': len(main_releases),
        'total_releases': len(sub_releases),
        'total_os': len(operating_systems),
        'last_updated': None
    }
    
    # 获取最新更新时间
    cursor = conn.execute("SELECT MAX(created_at) as last_update FROM sub_release")
    row = cursor.fetchone()
    if row and row['last_update']:
        stats['last_updated'] = row['last_update']
    
    conn.close()
    
    # 确保输出目录存在
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # 写入 JSON 文件
    print("\n写入 JSON 文件...")
    
    with open(OUTPUT_DIR / 'cadence_tools.json', 'w', encoding='utf-8') as f:
        json.dump({
            'main_releases': main_releases,
            'operating_systems': operating_systems,
            'sub_releases': sub_releases,
            'stats': stats
        }, f, indent=2, ensure_ascii=False)
    
    print(f"✓ 主版本: {len(main_releases)} 个")
    print(f"✓ 操作系统: {len(operating_systems)} 个")
    print(f"✓ 子版本: {len(sub_releases)} 个")
    print(f"\n数据已导出到: {OUTPUT_DIR / 'cadence_tools.json'}")

if __name__ == '__main__':
    try:
        export_data()
    except FileNotFoundError:
        print(f"错误: 找不到数据库文件 '{DB_PATH}'")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)
