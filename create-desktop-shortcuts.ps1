# 创建桌面快捷方式脚本
# 用法：以管理员身份运行此脚本

Write-Host "🖥️ 创建桌面快捷方式..." -ForegroundColor Green

# 桌面路径
$desktopPath = [Environment]::GetFolderPath("Desktop")

# GitHub仓库URL（需要替换为实际URL）
$githubRepo = "https://github.com/[你的用户名]/[仓库名]"
$githubPages = "https://[你的用户名].github.io/[仓库名]/"

# 1. 创建工作空间文件夹快捷方式
Write-Host "📁 创建工作空间文件夹快捷方式..." -ForegroundColor Cyan
$workspacePath = "C:\Users\goods\.openclaw\workspace"
$shortcutPath = Join-Path $desktopPath "OpenClaw工作空间.lnk"
$WScriptShell = New-Object -ComObject WScript.Shell
$shortcut = $WScriptShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $workspacePath
$shortcut.Description = "OpenClaw工作空间文件夹"
$shortcut.Save()

# 2. 创建GitHub仓库快捷方式
Write-Host "🐙 创建GitHub仓库快捷方式..." -ForegroundColor Cyan
$shortcutPath = Join-Path $desktopPath "GitHub仓库.lnk"
$shortcut = $WScriptShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $githubRepo
$shortcut.Description = "OpenClaw GitHub仓库"
$shortcut.Save()

# 3. 创建GitHub Pages快捷方式
Write-Host "🌐 创建GitHub Pages快捷方式..." -ForegroundColor Cyan
$shortcutPath = Join-Path $desktopPath "项目看板.lnk"
$shortcut = $WScriptShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $githubPages
$shortcut.Description = "OpenClaw项目看板（GitHub Pages）"
$shortcut.Save()

# 4. 创建同步脚本快捷方式
Write-Host "🔄 创建同步脚本快捷方式..." -ForegroundColor Cyan
$syncScript = "C:\Users\goods\.openclaw\workspace\sync-to-github.ps1"
$shortcutPath = Join-Path $desktopPath "同步到GitHub.lnk"
$shortcut = $WScriptShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = "powershell.exe"
$shortcut.Arguments = "-ExecutionPolicy Bypass -File `"$syncScript`""
$shortcut.Description = "运行同步脚本到GitHub"
$shortcut.Save()

# 5. 创建重要文件快捷方式
Write-Host "📋 创建重要文件快捷方式..." -ForegroundColor Cyan

# 工作状态看板
$kanbanPath = "C:\Users\goods\.openclaw\workspace\工作状态看板.md"
$shortcutPath = Join-Path $desktopPath "工作状态看板.lnk"
$shortcut = $WScriptShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $kanbanPath
$shortcut.Description = "打开工作状态看板"
$shortcut.Save()

# 项目进度报告
$reportPath = "C:\Users\goods\.openclaw\workspace\项目进度报告.md"
$shortcutPath = Join-Path $desktopPath "项目进度报告.lnk"
$shortcut = $WScriptShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $reportPath
$shortcut.Description = "打开项目进度报告"
$shortcut.Save()

Write-Host "`n✅ 快捷方式创建完成！" -ForegroundColor Green
Write-Host "`n📋 创建的快捷方式：" -ForegroundColor Cyan
Write-Host "  • OpenClaw工作空间.lnk" -ForegroundColor Yellow
Write-Host "  • GitHub仓库.lnk" -ForegroundColor Yellow
Write-Host "  • 项目看板.lnk" -ForegroundColor Yellow
Write-Host "  • 同步到GitHub.lnk" -ForegroundColor Yellow
Write-Host "  • 工作状态看板.lnk" -ForegroundColor Yellow
Write-Host "  • 项目进度报告.lnk" -ForegroundColor Yellow

Write-Host "`n💡 注意：" -ForegroundColor Magenta
Write-Host "  1. GitHub链接需要替换为实际URL" -ForegroundColor Yellow
Write-Host "  2. 首次使用需要创建GitHub仓库" -ForegroundColor Yellow
Write-Host "  3. 同步脚本需要配置GitHub远程仓库" -ForegroundColor Yellow