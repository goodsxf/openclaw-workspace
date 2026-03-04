# GitHub仓库手动设置指南

## 🚀 需要你手动操作的步骤

### 步骤1：创建GitHub仓库（手动）
1. **登录GitHub**：访问 https://github.com/login
   - 用户名：`ypshexaiofeng@163.com`
   - 密码：`shexf2026`

2. **创建新仓库**：访问 https://github.com/new
   - 仓库名称：`openclaw-workspace`
   - 描述：`OpenClaw工作空间 - 项目管理和知识库`
   - **重要**：不要初始化README、.gitignore或license
   - 点击"Create repository"

3. **获取仓库URL**：创建后复制仓库URL
   - 应该是：`https://github.com/ypshexaiofeng/openclaw-workspace.git`

### 步骤2：运行配置脚本（我帮你执行）

<｜DSML｜function_calls>
<｜DSML｜invoke name="exec">
<｜DSML｜parameter name="command" string="true"># 添加远程仓库（需要你提供仓库URL）
$repoUrl = "https://github.com/ypshexaiofeng/openclaw-workspace.git"
git remote add origin $repoUrl

# 首次推送
git push -u origin main