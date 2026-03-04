# OpenClaw Workspace 自动同步到GitHub脚本
# 用法：在PowerShell中运行 .\sync-to-github.ps1

Write-Host "🚀 开始同步工作空间到GitHub..." -ForegroundColor Green

# 检查Git状态
Write-Host "📊 检查Git状态..." -ForegroundColor Cyan
$status = git status --porcelain
if ($status) {
    Write-Host "📝 发现未提交的更改：" -ForegroundColor Yellow
    $status | ForEach-Object { Write-Host "  $_" }
    
    # 添加所有更改
    Write-Host "➕ 添加所有更改到暂存区..." -ForegroundColor Cyan
    git add .
    
    # 提交更改
    $commitMessage = "自动同步: " + (Get-Date -Format "yyyy-MM-dd HH:mm")
    Write-Host "💾 提交更改: $commitMessage" -ForegroundColor Cyan
    git commit -m $commitMessage
    
    # 推送到远程仓库
    Write-Host "📤 推送到远程仓库..." -ForegroundColor Cyan
    git push origin main
    
    Write-Host "✅ 同步完成！" -ForegroundColor Green
    Write-Host "🌐 GitHub Pages将在几分钟内自动更新" -ForegroundColor Yellow
} else {
    Write-Host "✅ 没有需要同步的更改" -ForegroundColor Green
}

# 显示GitHub Pages链接
Write-Host "`n🔗 GitHub Pages链接：" -ForegroundColor Cyan
Write-Host "  https://[你的用户名].github.io/[仓库名]/" -ForegroundColor Yellow
Write-Host "`n📋 重要文件链接：" -ForegroundColor Cyan
Write-Host "  • 项目进度报告: /项目进度报告.md" -ForegroundColor Yellow
Write-Host "  • 工作状态看板: /工作状态看板.md" -ForegroundColor Yellow
Write-Host "  • 知识库: /knowledge-base/" -ForegroundColor Yellow

Write-Host "`n💡 提示：可以设置定时任务自动运行此脚本" -ForegroundColor Magenta