# Cadence Tools 浏览器使用指南

## 📋 概述

这是一个集成在 Jekyll 博客中的 Cadence 工具版本浏览器，可以通过多维度筛选查看 Cadence 工具的版本信息。

## 🎯 功能特性

### 多维度筛选
- **按工具筛选**: 从 219 个 Cadence 工具中选择
- **按操作系统筛选**: 支持 102 种操作系统配置
- **按类型筛选**: UPDATE、BASE、HOTFIX 等
- **关键词搜索**: 搜索版本号、描述等信息
- **状态筛选**: 已下载、导出受控等

### 展示信息
- 工具名称和工程名称
- 版本号和发布日期
- 支持的操作系统列表
- 下载文件和资源文件统计
- 详细版本描述（点击展开）

### 实时统计
- 工具总数
- 版本总数
- 操作系统总数
- 当前筛选结果数量

## 🚀 快速开始

### 1. 数据准备

首先需要从 SQLite 数据库生成 JSON 数据：

```powershell
# Windows PowerShell
python generate_tools_data.py

# 或使用便捷脚本
.\update_tools_data.ps1
```

这会生成 `_data/cadence_tools.json` 文件。

### 2. 启动 Jekyll 服务器

```bash
# 开发模式
bundle exec jekyll serve

# 或使用项目任务
./tools/run.sh
```

### 3. 访问页面

打开浏览器访问：`http://localhost:4000/tools/`

## 📁 文件结构

```
icinfra-source/
├── _data/
│   └── cadence_tools.json          # 工具数据（自动生成）
├── _tabs/
│   └── tools.md                    # 工具浏览器页面
├── cadence_tools.db                # SQLite 数据库
├── generate_tools_data.py          # 数据导出脚本
├── update_tools_data.ps1           # 更新脚本（PowerShell）
└── TOOLS_USAGE.md                  # 本文档
```

## 🔧 工作原理

### 数据流程
```
SQLite DB → Python 脚本 → JSON 文件 → Jekyll Liquid → HTML + JS
```

1. **数据库**: `cadence_tools.db` 存储原始数据
2. **导出脚本**: `generate_tools_data.py` 查询并导出为 JSON
3. **Jekyll 数据**: `_data/cadence_tools.json` 供模板使用
4. **页面模板**: `_tabs/tools.md` 使用 Liquid 模板和 JavaScript
5. **前端交互**: 纯 JavaScript 实现筛选和展示

### 技术栈
- **后端**: Python + SQLite3
- **模板引擎**: Jekyll Liquid
- **前端**: 原生 JavaScript（无额外依赖）
- **样式**: CSS（集成在页面中）

## 🎨 样式说明

页面样式完全自适应 Jekyll Chirpy 主题：
- 使用主题 CSS 变量（如 `--card-bg`, `--text-color`）
- 支持明暗主题自动切换
- 响应式设计，支持移动端

## 📊 数据更新

### 定期更新
当数据库有更新时，重新运行导出脚本：

```powershell
python generate_tools_data.py
```

### 自动化（推荐）
可以设置定时任务自动更新：

**Windows 任务计划程序**:
```powershell
# 创建任务
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-File C:\path\to\update_tools_data.ps1"
$trigger = New-ScheduledTaskTrigger -Daily -At 2am
Register-ScheduledTask -TaskName "UpdateCadenceTools" -Action $action -Trigger $trigger
```

**Cron (Linux/macOS)**:
```bash
# 添加到 crontab
0 2 * * * cd /path/to/icinfra-source && python generate_tools_data.py
```

## 🎯 使用场景

### 场景 1: 查找特定工具的所有版本
1. 在"工具"下拉框中选择工具名称
2. 查看所有版本列表
3. 点击行展开查看详细信息

### 场景 2: 查看某操作系统支持的工具
1. 在"操作系统"下拉框中选择系统
2. 查看支持该系统的所有工具和版本

### 场景 3: 查找已下载的版本
1. 勾选"仅显示已下载"
2. 查看所有已下载版本

### 场景 4: 搜索特定版本
1. 在搜索框输入版本号关键词
2. 实时显示匹配结果

### 场景 5: 组合筛选
可以组合多个筛选条件，例如：
- 工具 = "VIRTUOSO"
- 操作系统 = "LINUX RHEL 9"
- 类型 = "UPDATE"
- 已下载 = 是

## 🔍 数据模型

### JSON 结构
```json
{
  "main_releases": [
    {
      "id": 1,
      "release_name": "ASSURA 4.1",
      "engineering_name": "ASSURA41",
      "version_count": 10,
      "os_count": 12,
      "latest_date": "31-Jul-2024"
    }
  ],
  "operating_systems": [
    {
      "id": 1,
      "os_name": "LINUX RHEL 8 for 251",
      "os_family": "LINUX",
      "tool_count": 50
    }
  ],
  "sub_releases": [
    {
      "id": 1,
      "release_number": "ASSURA04.17.253",
      "release_version": null,
      "release_date": "03-Sep-2025",
      "release_type": "UPDATE",
      "platform": "LINUX",
      "downloaded": 1,
      "export_controlled": 0,
      "main_release_id": 1,
      "release_name": "ASSURA 4.1",
      "engineering_name": "ASSURA41",
      "os_ids": [1, 2, 3, 4],
      "os_names": ["LINUX RHEL 8 for 251", "LINUX RHEL 9", ...],
      "media_count": 2,
      "resource_count": 5
    }
  ],
  "stats": {
    "total_tools": 219,
    "total_releases": 824,
    "total_os": 102,
    "last_updated": "2025-10-15 01:18:49"
  }
}
```

## 🐛 故障排查

### 问题: 页面不显示数据
**解决**:
1. 检查 `_data/cadence_tools.json` 是否存在
2. 运行 `python generate_tools_data.py` 重新生成
3. 检查 JSON 格式是否正确

### 问题: 筛选不工作
**解决**:
1. 打开浏览器开发者工具查看控制台错误
2. 确认 JavaScript 没有被阻止
3. 刷新页面清除缓存

### 问题: 样式错误
**解决**:
1. 确认使用的是 Chirpy 主题
2. 检查主题版本兼容性
3. 清除浏览器缓存

## 📝 自定义

### 修改筛选字段
编辑 `_tabs/tools.md` 的筛选区域：
```html
<div class="filter-group">
  <label for="filter-custom">自定义字段</label>
  <select id="filter-custom">
    <!-- 选项 -->
  </select>
</div>
```

### 修改表格列
编辑 `<thead>` 和渲染函数中的列定义。

### 调整样式
修改 `<style>` 标签中的 CSS。

## 🔗 相关文件

- **数据库分析**: `database_analysis_report.md`
- **数据库优化**: `db_optimization_suggestions.sql`
- **实用视图**: `db_useful_views.sql`
- **命令行工具**: `query_tool.py`

## 📚 扩展功能建议

### 未来可以添加的功能
1. **导出功能**: 导出筛选结果为 CSV/Excel
2. **对比功能**: 对比不同版本的差异
3. **下载链接**: 直接显示下载链接（需要认证）
4. **变更日志**: 集成版本变更记录
5. **统计图表**: 使用 Chart.js 显示统计图表
6. **收藏功能**: 收藏常用版本（使用 localStorage）

## 💡 最佳实践

1. **定期更新数据**: 建议每天或每周更新一次
2. **备份数据库**: 更新前备份 `cadence_tools.db`
3. **版本控制**: 不要提交 `_data/cadence_tools.json` 到 Git（如果数据敏感）
4. **性能优化**: 如果数据量增大，考虑分页或虚拟滚动
5. **访问控制**: 如果数据敏感，考虑添加认证机制

## 🤝 贡献

如有改进建议或发现问题，请：
1. 在项目中创建 Issue
2. 提交 Pull Request
3. 联系维护者

## 📄 许可证

遵循项目主许可证。
