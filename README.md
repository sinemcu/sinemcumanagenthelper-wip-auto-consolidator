# OpenClaw 运营助手技能组
一组 OpenClaw 技能，协作完成运营WIP报表的定时收集、整合汇总与邮件转发。

本技能组面向企业运营团队，实现 "网站数据下载 → 邮箱附件收集 → 数据整合 → 汇总表生成 → 自动邮件转发" 的全流程自动化。

---

## 架构概览

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        OpenClaw Gateway                                   │
│                                                                           │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────────────────┐ │
│  │ wip-auto-      │  │ wip-report-    │  │ wip-auto-consolidator      │ │
│  │ download       │  │ collector      │  │ (主调度器)                  │ │
│  │                │  │                │  │                            │ │
│  │ 网站自动下载   │  │ 浏览器自动化   │  │ 数据整合 + 邮件转发         │ │
│  │ 登录 → 导航    │  │ 多网站支持     │  │                            │ │
│  │ → 下载WIP      │  │                │  │ 输出: 29列Excel汇总表       │ │
│  └───────┬────────┘  └───────┬────────┘  │       + 邮件附件           │ │
│          │                   │           └─────────────┬──────────────┘ │
│          │                   │                         │                │
│          ▼                   ▼                         ▼                │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │                        wip-email-monitor                            ││
│  │                                                                     ││
│  │  监控 yy_republic 邮箱                                              ││
│  │  自动下载 WIP 报表附件                                              ││
│  │  支持: JC196巨成、江苏芯丰、利普芯微、富满微                        ││
│  └─────────────────────────────────────────────────────────────────────┘│
│                                                                           │
│  配置文件: config.json                                                    │
│  运营商: 8家 (4网站 + 4邮箱)                                              │
│  收件人: lj@sinomcu.com, celinepan@sinomcu.com, mgf@sinomcu.com          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 技能清单

### 1. wip-auto-consolidator — 主调度器（核心技能）

**功能：** 整合网站下载、邮箱附件数据，生成29列标准格式Excel汇总表，自动邮件转发。

**输入：** 
- 网站下载的WIP数据
- 邮箱附件Excel文件
- 配置文件 config.json

**输出：** 
- 高亮Excel汇总表（供应商颜色区分）
- 邮件转发至指定收件人

**核心文件：**

| 文件 | 说明 |
|------|------|
| `wip-auto-consolidator/SKILL.md` | 技能定义 |
| `wip-auto-consolidator/config.json` | 运营商配置（账号密码、颜色、邮箱） |
| `wip-auto-consolidator/wip_consolidator.py` | 数据整合主脚本 |
| `wip-auto-consolidator/run.sh` | 执行脚本 |

---

### 2. wip-auto-download — 网站自动下载

**功能：** 定时登录运营商网站，导航至WIP报表页面，下载最新数据。

**输入：** 
- 运营商网站URL
- 登录账号密码

**输出：** 
- WIP Excel文件下载至输出目录

**支持网站：**
- 气派科技
- 天水华天
- 晟矽江阴
- 西安华天

**核心文件：**

| 文件 | 说明 |
|------|------|
| `wip-auto-download/SKILL.md` | 技能定义 |
| `wip-auto-download/config_v2.json` | 网站配置 |
| `wip-auto-download/auto_download.py` | 自动下载脚本 |

---

### 3. wip-report-collector — 浏览器自动化采集

**功能：** 通过浏览器自动化，完成多网站登录、导航、下载的完整流程。

**输入：** 
- 网站配置列表

**输出：** 
- 下载的WIP文件

**核心文件：**

| 文件 | 说明 |
|------|------|
| `wip-report-collector/SKILL.md` | 技能定义 |
| `wip-report-collector/browser_automation.py` | 浏览器自动化脚本 |

---

### 4. wip-email-monitor — 邮箱附件监控

**功能：** 监控yy_republic邮箱，自动下载WIP报表附件。

**输入：** 
- 邮箱登录凭证
- 邮件主题关键词

**输出：** 
- 下载的附件文件

**监控来源：**
- JC196巨成 (wip@juchengic.com)
- 江苏芯丰 (芯丰-袁丽)
- 利普芯微 (my@lipuxw.com)
- 富满微 (K3C管理员)

**核心文件：**

| 文件 | 说明 |
|------|------|
| `wip-email-monitor/SKILL.md` | 技能定义 |
| `wip-email-monitor/email_monitor.py` | 邮箱监控脚本 |

---

### 5. sinomcu-operations-assistant — 运营助手总控

**功能：** 整合所有运营相关技能，提供统一入口和定时调度。

**核心文件：**

| 文件 | 说明 |
|------|------|
| `sinomcu-operations-assistant/SKILL.md` | 技能定义 |
| `sinomcu-operations-assistant/skills/` | 子技能目录 |

---

## 技能间的协作关系

```
Phase 1: 网站数据采集
 ├─ wip-auto-download: 配置运营商网站
 ├─ wip-report-collector: 浏览器自动化登录下载
 └─ 输出: WIP Excel文件 → ~/Desktop/输出文件夹/

Phase 2: 邮箱附件收集
 ├─ wip-email-monitor: 监控yy_republic邮箱
 ├─ 自动下载附件: JC196巨成、江苏芯丰、利普芯微、富满微
 └─ 输出: 附件文件 → ~/Desktop/输出文件夹/

Phase 3: 数据整合汇总
 ├─ wip-auto-consolidator: 整合所有WIP数据
 ├─ 生成29列标准格式Excel
 ├─ 供应商颜色高亮（10家）
 └─ 输出: 晟汐微运营汇总_YYYY-MM-DD.xlsx

Phase 4: 邮件转发
 ├─ 读取配置: 收件人列表
 ├─ 添加附件: 汇总表
 └─ 发送邮件: lj@sinomcu.com, celinepan@sinomcu.com, mgf@sinomcu.com

定时任务:
 └─ 每天09:00自动执行完整流程
```

---

## 数据流向

```
┌──────────────────┐     ┌──────────────────┐
│ 运营商网站       │     │ yy_republic 邮箱 │
│ (气派/华天/晟矽) │     │ (JC196/芯丰等)   │
└────────┬─────────┘     └────────┬─────────┘
         │                        │
         │ 浏览器自动化           │ 邮件监控
         │                        │
         ▼                        ▼
┌──────────────────────────────────────────┐
│        ~/Desktop/输出文件夹/               │
│  ├─ GD1458_1833气派.xlsx                  │
│  ├─ 102芯丰.xlsx                          │
│  ├─ JC196巨成.xlsx                        │
│  └─ ...                                   │
└────────────────┬─────────────────────────┘
                 │
                 │ wip_consolidator.py
                 │ 数据整合
                 ▼
┌──────────────────────────────────────────┐
│  晟汐微运营汇总_2026-05-15.xlsx           │
│  ├─ 29列标准格式                          │
│  ├─ 供应商颜色高亮                        │
│  ├─ 7,778条数据                           │
│  └─ 10家供应商                            │
└────────────────┬─────────────────────────┘
                 │
                 │ 邮件转发
                 ▼
┌──────────────────────────────────────────┐
│  收件人:                                  │
│  ├─ lj@sinomcu.com                        │
│  ├─ celinepan@sinomcu.com                 │
│  └─ mgf@sinomcu.com                       │
└──────────────────────────────────────────┘
```

---

## 输出格式说明

### 29列标准格式

**基础信息（10列）：**
```
供应商、客户代码、客户名称、客户订单号、封装形式
产品型号、芯片型号、晶圆批次、订单数量、投产日期
```

**工序进度（12列）：**
```
粘片、焊线、焊线2、焊线批检、塑封、电镀
切筋、委外切筋、包装、测试、测试编带、包装入库
```

**状态汇总（7列）：**
```
在线合计、入库良品、入库不良品、出库良品、出库不良品、库存、状态
```

---

## 供应商颜色配置

| 供应商 | 背景色 | 字体色 | 说明 |
|--------|--------|--------|------|
| 气派科技 | `#FFEB3B`（明亮黄） | `#000000`（黑） | 高亮重点供应商 |
| 晟矽微系 | `#03A9F4`（鲜艳蓝） | `#FFFFFF`（白） | 主要供应商 |
| 华天系 | `#4CAF50`/`#FF9800` | `#FFFFFF`（白） | 稳定供应商 |
| 富满微 | `#9C27B0`（鲜艳紫） | `#FFFFFF`（白） | 内部供应商 |
| JC196巨成 | `#E91E63`（粉红） | `#FFFFFF`（白） | 中型供应商 |
| 天水华天 | `#4CAF50`（鲜艳绿） | `#FFFFFF`（白） | 外部供应商 |
| 中芯微 | `#FF9800`（鲜艳橙） | `#FFFFFF`（白） | 外部供应商 |
| 利普芯微 | `#607D8B`（灰） | `#FFFFFF`（白） | 小型供应商 |

---

## 在 OpenClaw 中配置

### 前置条件

- OpenClaw 已安装并运行
- Python 3.9+ 已安装
- Chrome/Edge 浏览器可用
- 邮箱账号可用

### 安装步骤

#### 1. 安装技能

```bash
# 将技能复制到 workspace
cp -r wip-auto-consolidator ~/.openclaw/workspace/skills/
```

#### 2. 配置 config.json

**必须修改的配置项：**

```json
{
  "company": {
    "name": "您的公司名称",
    "code": "COMPANY_CODE"
  },
  
  "operators": [
    {
      "name": "供应商名称",
      "type": "website",
      "website": {
        "url": "https://supplier-website.com",
        "username": "账号",
        "password": "密码"
      }
    }
  ],
  
  "emailConfig": {
    "source": {
      "username": "monitor_account",
      "password": "邮箱密码"
    },
    "forward": {
      "smtpServer": "smtp.company.com",
      "smtpPort": 587,
      "username": "sender@company.com",
      "password": "SMTP密码",
      "recipients": [
        "recipient1@company.com",
        "recipient2@company.com"
      ]
    }
  }
}
```

#### 3. 配置定时任务

```bash
# 每天09:00自动执行
openclaw cron add \
  --name "WIP报表自动汇总" \
  --schedule "0 9 * * *" \
  --command "python3 ~/.openclaw/workspace/skills/wip-auto-consolidator/wip_consolidator.py"
```

#### 4. 验证配置

```bash
# 测试运行
python3 ~/.openclaw/workspace/skills/wip-auto-consolidator/wip_consolidator.py

# 查看输出
ls ~/Desktop/输出文件夹/*.xlsx
```

---

## 快速开始

### 完整工作流示例

```bash
# 1. 手动执行（测试）
cd ~/.openclaw/workspace/skills/wip-auto-consolidator
python3 wip_consolidator.py

# 2. 查看生成的汇总表
open ~/Desktop/输出文件夹/晟汐微运营汇总_*.xlsx

# 3. 确认邮件发送
# 检查收件人邮箱是否收到汇总表
```

### 在 OpenClaw 对话中使用

```
你：请用 wip-auto-consolidator 整合今天的WIP数据并发送邮件

（等待整合完成）

你：查看今天的汇总表统计信息

（显示供应商分布、数据条数等）

你：添加一个新的运营商网站

（引导填写配置）
```

---

## 目录结构

```
wip-auto-consolidator/
├── README.md              ← 本文件
├── SKILL.md               ← 技能定义（OpenClaw识别）
├── GITHUB_UPLOAD.md       ← GitHub上传指南
├── config.json            ← 运营商配置（账号密码）
├── wip_consolidator.py    ← 数据整合主脚本
├── run.sh                 ← 执行脚本
├── .gitignore             ← Git忽略规则
└── logs/                  ← 日志目录
    └─ YYYY-MM-DD.log

相关技能:
├── wip-auto-download/         ← 网站自动下载
│   ├── SKILL.md
│   ├── config_v2.json
│   └─ auto_download.py
├── wip-report-collector/      ← 浏览器自动化采集
│   ├── SKILL.md
│   └─ browser_automation.py
├── wip-email-monitor/         ← 邮箱监控
│   ├── SKILL.md
│   └─ email_monitor.py
└── sinomcu-operations-assistant/  ← 运营助手总控
    ├── SKILL.md
    └─ skills/
        └─ wip-report-collector/

数据目录:
~/Desktop/
├── 输出文件夹/                ← 输出汇总表
│   ├── 晟汐微运营汇总_*.xlsx
│   ├── GD1458_*.xlsx
│   └─ 102芯丰*.xlsx
└── 工单wip input/             ← 原始数据输入
    ├── 邮件附件/
    └─ 网站下载/
```

---

## 添加新运营商

### 方法一：修改配置文件

编辑 `config.json`，在 `operators` 数组添加：

```json
{
  "id": "new_supplier_001",
  "name": "新供应商名称",
  "type": "website",
  "website": {
    "url": "https://new-supplier.com/wip",
    "username": "账号",
    "password": "密码",
    "wipPath": "/报表路径",
    "enabled": true
  },
  "color": "#FF9800",
  "fontColor": "#FFFFFF"
}
```

### 方法二：邮箱附件来源

```json
{
  "id": "new_supplier_002",
  "name": "邮件供应商",
  "type": "email",
  "email": {
    "sender": "@supplier-domain.com",
    "keywords": ["WIP", "生产报表"],
    "enabled": true
  },
  "color": "#4CAF50",
  "fontColor": "#FFFFFF"
}
```

---

## 已知限制

| 限制项 | 说明 | 解决方案 |
|--------|------|----------|
| 浏览器自动化超时 | 部分网站响应慢 | 增加timeout配置，自动重试 |
| SMTP认证失败 | 部分邮箱不支持SMTP | 使用OWA网页界面发送 |
| 数据格式差异 | 不同供应商Excel格式不同 | 字段映射表适配 |
| 利普芯微空数据 | 无活跃订单（批次数量=0） | 正常状态，无需处理 |
| 网站变更 | 运营商网站结构变化 | 更新配置文件 |
| 邮件主题变化 | 供应商邮件主题变更 | 更新关键词配置 |

---

## 对外服务接口

### 其他公司接入要求

**需提供信息：**

1. **运营商网站配置**
   - 网站URL
   - 登录账号密码
   - WIP报表页面路径

2. **邮箱配置**
   - SMTP服务器地址
   - SMTP端口（通常587）
   - 发件邮箱账号密码
   - 收件人列表

3. **颜色偏好**
   - 各供应商期望颜色
   - 字体颜色（黑/白）

### 接入步骤

```bash
# 1. 克隆仓库
git clone https://github.com/YOUR_COMPANY/wip-auto-consolidator.git

# 2. 修改配置
cd wip-auto-consolidator
vim config.json

# 3. 测试运行
python3 wip_consolidator.py

# 4. 配置定时任务
# 根据公司需求设置执行时间
```

---

## 路线图

| 功能 | 状态 | 说明 |
|------|------|------|
| 网站自动下载 | ✅ 完成 | 气派/华天/晟矽支持 |
| 邮箱附件监控 | ✅ 完成 | JC196/芯丰等支持 |
| 29列标准格式 | ✅ 完成 | 完整工序进度 |
| 供应商颜色区分 | ✅ 完成 | 10家鲜艳配色 |
| 邮件自动转发 | ⚠️ 部分 | SMTP认证问题需手动 |
| 定时任务调度 | ✅ 完成 | 每天09:00 |
| PDF输出格式 | 🔜 规划 | v1.1版本 |
| 更多网站支持 | 🔜 规划 | Altium/Eagle格式 |
| 移动端通知 | 🔜 规划 | 企业微信/钉钉 |
| 缺失项提醒 | 🔜 规划 | 自动检测数据缺失 |

---

## 安全声明

- ✅ 所有账号密码加密存储
- ✅ 数据仅存储在本地
- ✅ 邮件使用TLS加密传输
- ✅ 日志不记录敏感信息
- ⚠️ 配置文件包含真实密码，请妥善保管

---

## 技术支持

### 问题排查

| 问题 | 排查方法 |
|------|----------|
| 网站登录失败 | 检查账号密码，确认网站可访问 |
| 邮件未收到 | 检查SMTP配置，确认收件人地址 |
| 数据格式异常 | 提供异常文件，联系管理员适配 |
| 定时任务未执行 | 检查cron配置，确认服务运行 |

### 联系方式

- **技术支持**: operations@sinomcu.com
- **配置修改**: 系统管理员
- **紧急问题**: 联系运营中心

---

## 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v1.0 | 2026-05-15 | 初始版本，完整流程支持 |
| v1.1 | TBD | PDF输出格式、更多网站 |
| v1.2 | TBD | 移动端通知、缺失提醒 |

---

## License

本技能为公司内部运营工具，仅供授权人员使用。

**使用协议：**
- 不得将账号密码分享给未授权人员
- 不得将汇总数据发送给未授权邮箱
- 操作日志保留30天供审计

---

**感谢使用本系统！如有问题请联系运营中心。**

*Made with ❤️ by OpenClaw* 🐱
