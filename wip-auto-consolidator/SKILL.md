---
name: wip-auto-consolidator
description: "运营WIP报表自动化汇总系统。定时从运营网站和邮箱收集WIP数据，自动整合成总表，通过邮箱转发给指定人员。支持灵活添加新运营商。"
---

# 运营WIP报表自动化汇总系统

## 技能描述

**完整自动化工作流：**

```
定时触发 → 网站WIP下载 → 邮箱附件收集 → 数据整合汇总 → 高亮Excel生成 → 自动邮件转发
```

---

## 核心功能

### 📊 1. 网站WIP自动下载

- 登录各运营商网站
- 自动下载WIP报表（Excel格式）
- 支持动态添加新运营商
- 失败自动跳过并记录日志

### 📧 2. 邮箱附件自动收集

- 登录指定邮箱（yy_republic）
- 搜索WIP报表邮件
- 自动下载附件
- 按供应商分类存储

### 🔄 3. 数据汇总整合

- 统一29列输出格式
- 包含完整工序列（粘片→包装入库）
- 按供应商颜色区分
- 状态智能高亮

### 📨 4. 自动邮件转发

- 通过指定邮箱转发汇总表
- 支持多个收件人
- 自动添加时间戳和说明

---

## 输出格式（29列）

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

## 配置文件

### config.json 结构

```json
{
  "version": "1.0",
  "company": {
    "name": "公司名称",
    "code": "公司代码"
  },
  
  "operators": [
    {
      "id": "operator_001",
      "name": "运营商名称",
      "type": "website|email",
      "website": {
        "url": "https://...",
        "username": "账号",
        "password": "密码",
        "wipPath": "报表路径",
        "enabled": true
      },
      "email": {
        "sender": "@domain.com",
        "keywords": ["WIP", "报表"]
      }
    }
  ],
  
  "emailConfig": {
    "source": {
      "server": "mail.sinomcu.com",
      "username": "yy_republic",
      "password": "密码",
      "protocol": "owa"
    },
    "forward": {
      "server": "smtp.sinomcu.com",
      "port": 587,
      "username": "yy_republic",
      "password": "密码",
      "recipients": [
        "lj@sinomcu.com",
        "celinepan@sinomcu.com",
        "mgf@sinomcu.com"
      ]
    }
  },
  
  "output": {
    "dir": "~/Desktop/输出文件夹",
    "filenameTemplate": "运营WIP汇总_{date}.xlsx"
  },
  
  "schedule": {
    "cron": "0 9 * * *",
    "timezone": "Asia/Shanghai"
  }
}
```

---

## 定时任务

**执行时间：** 每天 09:00（可配置）

**任务流程：**
1. 网站数据下载（约5-10分钟）
2. 邮箱附件收集（约2-3分钟）
3. 数据整合汇总（约1-2分钟）
4. 邮件转发发送（即时）

---

## 使用方法

### 🤖 自动执行

每天定时自动执行，无需手动操作。

### 💬 对话触发

```
"执行运营WIP汇总"
"收集今天的WIP报表"
"转发汇总表给相关人员"
"添加新的运营商配置"
```

### 🔧 脚本执行

```bash
python3 ~/.openclaw/workspace/skills/wip-auto-consolidator/wip_consolidator.py
```

---

## 添加新运营商

### 方法一：修改配置文件

编辑 `config.json`，在 `operators` 数组中添加：

```json
{
  "id": "operator_new",
  "name": "新运营商名称",
  "type": "website",
  "website": {
    "url": "https://新运营商网站.com",
    "username": "账号",
    "password": "密码",
    "wipPath": "/报表路径",
    "enabled": true
  }
}
```

### 方法二：对话式添加

```
"添加新运营商：XX公司，网站是xxx.com，账号是xxx，密码是xxx"
```

---

## 高亮规则

### 供应商颜色（鲜艳配色）

| 供应商 | 背景色 | 字体颜色 |
|--------|--------|----------|
| 气派科技 | 🟡 明亮黄 | 黑色 |
| 晟矽微系 | 🔵 鲜艳蓝 | 白色 |
| 华天系 | 🟢/🟠 鲜艳绿/橙 | 白色 |
| 其他 | 🔴/🟣 粉红/紫 | 白色 |

### 状态高亮

- ✅ **已完成/已结批**：亮绿色 + 白色加粗字体
- 🔄 **在线生产**：亮黄色 + 黑色加粗字体
- 📦 **已发货**：亮绿色 + 白色加粗字体

---

## 文件结构

```
wip-auto-consolidator/
├── SKILL.md               # 技能说明
├── README.md              # 使用说明（对外接口）
├── config.json            # 配置文件
├── wip_consolidator.py    # 主脚本
├── email_sender.py        # 邮件发送模块
├── website_downloader.py  # 网站下载模块
├── data_processor.py      # 数据处理模块
└── logs/
    └── YYYY-MM-DD.log
```

---

## 错误处理

| 错误类型 | 处理方式 |
|----------|----------|
| 网站登录失败 | 跳过该站点，记录日志，继续其他站点 |
| 邮箱连接失败 | 使用已下载文件继续汇总，记录警告 |
| 数据格式异常 | 尝试自动适配，失败则跳过该文件 |
| 邮件发送失败 | 保存本地副本，记录失败日志 |

---

## 技术栈

| 模块 | 技术 |
|------|------|
| 网站下载 | Playwright + browser tool |
| 邮箱操作 | OWA/EWS API |
| 数据处理 | pandas, openpyxl |
| 邮件发送 | SMTP |
| 定时任务 | OpenClaw cron |

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0 | 2026-05-15 | 初始版本，支持网站+邮箱+转发完整流程 |

---

## 作者备注

本技能为运营团队设计的完整自动化解决方案：

**核心价值：**
- ✅ 每天自动执行，无需人工干预
- ✅ 统一数据格式，便于分析
- ✅ 自动邮件转发，及时通知相关人员
- ✅ 支持动态添加新运营商
- ✅ 完整错误处理和日志记录
- ✅ 可对外提供服务接口

**适用场景：**
- 生产运营数据汇总
- 供应链进度监控
- 跨供应商数据整合
- 自动化报表分发

喵~ 🐱