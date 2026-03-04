# GitHub仓库设置指南

## 🚀 快速开始

### 步骤1：创建GitHub仓库
1. 访问 https://github.com/new
2. 输入仓库名称：`openclaw-workspace`
3. 描述：`OpenClaw工作空间 - 项目管理和知识库`
4. **不要**初始化README、.gitignore或license
5. 点击"Create repository"

### 步骤2：配置本地仓库
```powershell
# 添加远程仓库（替换[用户名]为你的GitHub用户名）
git remote add origin https://github.com/[用户名]/openclaw-workspace.git

# 首次推送
git push -u origin main
```

### 步骤3：启用GitHub Pages
1. 进入仓库设置 → Pages
2. 源分支选择：`gh-pages`
3. 文件夹选择：`/(root)`
4. 点击Save

### 步骤4：运行同步脚本
```powershell
# 在workspace目录下运行
.\sync-to-github.ps1
```

## 🔧 详细配置

### GitHub Pages配置
- **URL格式**：`https://[用户名].github.io/openclaw-workspace/`
- **自动更新**：每次推送后自动部署
- **渲染引擎**：Jekyll（自动渲染Markdown）

### 自动同步配置
编辑 `sync-to-github.ps1` 文件：
```powershell
# 修改第28行的GitHub Pages链接
$githubPages = "https://[你的用户名].github.io/openclaw-workspace/"
```

### 桌面快捷方式配置
编辑 `create-desktop-shortcuts.ps1` 文件：
```powershell
# 修改第11-12行的GitHub链接
$githubRepo = "https://github.com/[你的用户名]/openclaw-workspace"
$githubPages = "https://[你的用户名].github.io/openclaw-workspace/"
```

## 📊 文件结构说明

```
openclaw-workspace/
├── .github/workflows/
│   └── sync-to-github.yml    # GitHub Actions工作流
├── _config.yml               # Jekyll配置
├── README.md                 # 首页
├── 项目进度报告.md           # 自动渲染
├── 工作状态看板.md           # 自动渲染
├── knowledge-base/           # 知识库
├── projects/                 # 项目文件
├── operations/               # 操作记录
├── sync-to-github.ps1        # 同步脚本
└── create-desktop-shortcuts.ps1 # 快捷方式脚本
```

## 🔔 使用说明

### 查看渲染后的页面
1. 访问：`https://[用户名].github.io/openclaw-workspace/`
2. 所有Markdown文件会自动渲染为网页
3. 支持导航和搜索

### 更新内容
1. 编辑本地文件
2. 运行 `.\sync-to-github.ps1`
3. 等待1-2分钟，GitHub Pages自动更新

### 创建桌面快捷方式
```powershell
# 以管理员身份运行
.\create-desktop-shortcuts.ps1
```

## ⚠️ 注意事项

### 文件编码
- 所有文件使用UTF-8编码
- 中文文件名可能需要在Git中特殊处理

### GitHub限制
- 免费账户：每个仓库1GB
- Pages：每月100GB流量
- Actions：每月2000分钟

### 安全性
- 不要提交敏感信息（密码、API密钥等）
- 使用.gitignore排除临时文件
- 定期备份重要数据

## 🔧 故障排除

### 问题：推送失败
```powershell
# 强制推送（谨慎使用）
git push -f origin main
```

### 问题：Pages不更新
1. 检查Actions是否运行完成
2. 等待5-10分钟
3. 清除浏览器缓存

### 问题：Markdown不渲染
1. 检查文件扩展名是否为`.md`
2. 检查文件是否在排除列表中
3. 检查_config.yml配置

## 📞 支持

如有问题：
1. 查看GitHub Actions日志
2. 检查本地Git配置
3. 联系OpenClaw支持

---

*本指南最后更新：2026-03-04*