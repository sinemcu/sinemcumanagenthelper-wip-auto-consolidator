# GitHub上传指南

## 方法一：通过GitHub网页创建（推荐）

### 步骤：

1. **登录GitHub**
   - 访问 https://github.com
   - 登录您的账号

2. **创建新仓库**
   - 点击右上角 "+" → "New repository"
   - Repository name: `wip-auto-consolidator`
   - Description: `运营WIP报表自动化汇总系统 - 定时收集WIP数据，自动整合转发`
   - 选择 Public 或 Private
   - ❌ 不要勾选 "Initialize with README"（已本地创建）
   - 点击 "Create repository"

3. **获取远程地址**
   - 创建后页面显示两种地址：
     - HTTPS: `https://github.com/YOUR_USERNAME/wip-auto-consolidator.git`
     - SSH: `git@github.com:YOUR_USERNAME/wip-auto-consolidator.git`

4. **添加远程仓库并推送**

```bash
cd ~/.openclaw/workspace/skills/wip-auto-consolidator

# 使用HTTPS（替换YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/wip-auto-consolidator.git
git push -u origin main

# 或使用SSH（推荐）
git remote add origin git@github.com:YOUR_USERNAME/wip-auto-consolidator.git
git push -u origin main
```

---

## 方法二：使用Git命令创建

```bash
cd ~/.openclaw/workspace/skills/wip-auto-consolidator

# 添加远程仓库（替换YOUR_USERNAME）
git remote add origin https://github.com/YOUR_USERNAME/wip-auto-consolidator.git

# 推送代码
git push -u origin main

# 如果提示输入密码，使用GitHub Personal Access Token
# 创建Token: GitHub → Settings → Developer settings → Personal access tokens
```

---

## 推送后的操作

### 1. 确认上传成功

访问仓库页面：
```
https://github.com/YOUR_USERNAME/wip-auto-consolidator
```

确认文件列表包含：
- ✅ SKILL.md
- ✅ README.md  
- ✅ config.json
- ✅ wip_consolidator.py
- ✅ run.sh

### 2. 设置仓库描述

在仓库Settings中添加：
- Website: 公司官网（可选）
- Topics: `automation`, `wip`, `operations`, `excel`, `email`

### 3. 添加协作者（可选）

Settings → Collaborators → Add people
添加运营团队成员

---

## 更新维护

### 后续更新流程

```bash
cd ~/.openclaw/workspace/skills/wip-auto-consolidator

# 修改文件后提交
git add .
git commit -m "Update: 添加新运营商配置"
git push
```

---

## 分享给其他公司

### 其他公司使用方式

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/wip-auto-consolidator.git

# 修改配置
cd wip-auto-consolidator
# 编辑 config.json，替换运营商信息和邮箱配置

# 测试运行
python3 wip_consolidator.py
```

---

**如有问题请参考README.md或联系运营中心**