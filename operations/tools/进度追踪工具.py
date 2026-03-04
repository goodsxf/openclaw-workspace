#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
进度追踪工具 - 自动计算项目进度和风险预警
"""

import os
import json
import yaml
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

class ProgressTracker:
    """进度追踪器"""
    
    def __init__(self, workspace_path: str = "."):
        self.workspace = Path(workspace_path)
        self.projects_dir = self.workspace / "projects"
        
    def scan_projects(self) -> List[Dict[str, Any]]:
        """扫描所有项目"""
        projects = []
        
        # 扫描所有分类目录
        for category_dir in self.projects_dir.iterdir():
            if category_dir.is_dir() and not category_dir.name.startswith("_"):
                # 扫描分类下的项目
                for project_dir in category_dir.iterdir():
                    if project_dir.is_dir() and project_dir.name.startswith("PROJECT-"):
                        project_info = self.analyze_project(project_dir, category_dir.name)
                        projects.append(project_info)
        
        return projects
    
    def analyze_project(self, project_dir: Path, category: str) -> Dict[str, Any]:
        """分析单个项目进度"""
        project_info = {
            "id": project_dir.name,
            "name": project_dir.name.replace("PROJECT-", "").replace("-", " "),
            "category": category,
            "path": str(project_dir.relative_to(self.workspace)),
            "status": "unknown",
            "progress": 0,
            "risks": [],
            "milestones": [],
            "last_updated": None,
            "next_report": None
        }
        
        # 检查项目概要文件
        summary_file = project_dir / "00-项目概要.md"
        if summary_file.exists():
            content = summary_file.read_text(encoding="utf-8")
            project_info.update(self.parse_summary(content))
        
        # 检查目标追踪文件
        goals_file = project_dir / "01-目标分解" / "目标追踪.md"
        if goals_file.exists():
            content = goals_file.read_text(encoding="utf-8")
            project_info.update(self.parse_goals(content))
        
        # 计算总体进度
        project_info["progress"] = self.calculate_progress(project_info)
        
        # 确定项目状态
        project_info["status"] = self.determine_status(project_info)
        
        return project_info
    
    def parse_summary(self, content: str) -> Dict[str, Any]:
        """解析项目概要文件"""
        info = {}
        
        # 提取项目状态
        if "项目状态：" in content:
            lines = content.split("\n")
            for line in lines:
                if "项目状态：" in line:
                    status = line.split("：")[1].strip()
                    info["summary_status"] = status
        
        # 提取最后更新
        if "最近更新：" in content:
            lines = content.split("\n")
            for line in lines:
                if "最近更新：" in line:
                    parts = line.split("：")[1].strip().split(" by ")
                    if len(parts) == 2:
                        info["last_updated"] = parts[0].strip()
        
        # 提取下次汇报
        if "下次汇报：" in content:
            lines = content.split("\n")
            for line in lines:
                if "下次汇报：" in line:
                    info["next_report"] = line.split("：")[1].strip()
        
        return info
    
    def parse_goals(self, content: str) -> Dict[str, Any]:
        """解析目标追踪文件"""
        info = {
            "goals": [],
            "risks": [],
            "milestones": []
        }
        
        lines = content.split("\n")
        current_section = None
        
        for line in lines:
            # 检测章节
            if line.startswith("### "):
                current_section = line[4:].strip()
            
            # 解析目标进度表
            elif "| 目标 | 总进度 |" in line:
                current_section = "goals_table"
            
            # 解析风险表
            elif "| 风险等级 | 问题描述 |" in line:
                current_section = "risks_table"
            
            # 解析里程碑
            elif "| 项目 | 里程碑 |" in line:
                current_section = "milestones_table"
            
            # 处理表格数据
            elif current_section == "goals_table" and "|" in line and "目标" not in line:
                parts = [p.strip() for p in line.split("|") if p.strip()]
                if len(parts) >= 5:
                    goal_info = {
                        "name": parts[0],
                        "progress": self.parse_percentage(parts[1]),
                        "weekly_progress": parts[2],
                        "risk": parts[3],
                        "next_check": parts[4]
                    }
                    info["goals"].append(goal_info)
            
            # 处理风险数据
            elif current_section == "risks_table" and "|" in line and "风险等级" not in line:
                parts = [p.strip() for p in line.split("|") if p.strip()]
                if len(parts) >= 6:
                    risk_info = {
                        "level": parts[0],
                        "description": parts[1],
                        "impact": parts[2],
                        "solution": parts[3],
                        "owner": parts[4],
                        "deadline": parts[5]
                    }
                    info["risks"].append(risk_info)
            
            # 处理里程碑数据
            elif current_section == "milestones_table" and "|" in line and "项目" not in line:
                parts = [p.strip() for p in line.split("|") if p.strip()]
                if len(parts) >= 5:
                    milestone_info = {
                        "project": parts[0],
                        "name": parts[1],
                        "planned": parts[2],
                        "actual": parts[3],
                        "status": parts[4]
                    }
                    info["milestones"].append(milestone_info)
        
        return info
    
    def parse_percentage(self, text: str) -> float:
        """解析百分比文本"""
        text = text.strip()
        if "%" in text:
            try:
                return float(text.replace("%", "").strip())
            except ValueError:
                return 0.0
        return 0.0
    
    def calculate_progress(self, project_info: Dict[str, Any]) -> float:
        """计算项目总体进度"""
        if "goals" in project_info and project_info["goals"]:
            # 计算所有目标的平均进度
            total = sum(goal["progress"] for goal in project_info["goals"])
            return total / len(project_info["goals"])
        
        # 如果没有目标数据，根据状态估算
        status = project_info.get("summary_status", "")
        if "已完成" in status:
            return 100.0
        elif "进行中" in status:
            return 50.0
        elif "待开始" in status:
            return 0.0
        else:
            return 0.0
    
    def determine_status(self, project_info: Dict[str, Any]) -> str:
        """确定项目状态"""
        progress = project_info["progress"]
        
        if progress >= 100:
            return "completed"
        elif progress > 0:
            return "in_progress"
        else:
            return "not_started"
    
    def generate_dashboard(self, projects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """生成仪表板数据"""
        dashboard = {
            "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "total_projects": len(projects),
            "by_status": {
                "in_progress": 0,
                "completed": 0,
                "not_started": 0
            },
            "by_category": {},
            "active_projects": [],
            "pending_decisions": 0,
            "upcoming_milestones": [],
            "high_risks": []
        }
        
        for project in projects:
            # 统计状态
            status = project["status"]
            dashboard["by_status"][status] = dashboard["by_status"].get(status, 0) + 1
            
            # 统计分类
            category = project["category"]
            dashboard["by_category"][category] = dashboard["by_category"].get(category, 0) + 1
            
            # 活跃项目（进行中）
            if status == "in_progress":
                dashboard["active_projects"].append({
                    "id": project["id"],
                    "name": project["name"],
                    "category": category,
                    "progress": project["progress"],
                    "status": "进行中"
                })
            
            # 高风险项目
            if project.get("risks"):
                high_risks = [r for r in project["risks"] if "🔴" in r.get("level", "")]
                if high_risks:
                    dashboard["high_risks"].append({
                        "project": project["name"],
                        "risks": high_risks
                    })
            
            # 近期里程碑
            if project.get("milestones"):
                for milestone in project["milestones"]:
                    if milestone.get("status") in ["🟡 进行中", "🔴 待开始"]:
                        dashboard["upcoming_milestones"].append({
                            "project": project["name"],
                            "milestone": milestone["name"],
                            "planned": milestone["planned"],
                            "status": milestone["status"]
                        })
        
        return dashboard
    
    def update_project_panel(self, dashboard: Dict[str, Any]):
        """更新项目管理面板"""
        panel_path = self.workspace / "项目管理面板.md"
        if not panel_path.exists():
            print(f"项目管理面板不存在: {panel_path}")
            return
        
        content = panel_path.read_text(encoding="utf-8")
        
        # 更新最后更新时间
        if "**最后更新：**" in content:
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if "**最后更新：**" in line:
                    lines[i] = f"**最后更新：** {dashboard['last_updated']}"
                    break
            content = "\n".join(lines)
        
        # 更新项目概览
        if "### 项目总数：" in content:
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if "### 项目总数：" in line:
                    # 更新项目总数
                    lines[i] = f"### 项目总数：{dashboard['total_projects']}"
                    
                    # 更新状态统计
                    if i+1 < len(lines) and "- **进行中：**" in lines[i+1]:
                        lines[i+1] = f"- **进行中：** {dashboard['by_status']['in_progress']}"
                    if i+2 < len(lines) and "- **已暂停：**" in lines[i+2]:
                        lines[i+2] = f"- **已暂停：** 0"
                    if i+3 < len(lines) and "- **已完成：**" in lines[i+3]:
                        lines[i+3] = f"- **已完成：** {dashboard['by_status']['completed']}"
                    if i+4 < len(lines) and "- **待启动：**" in lines[i+4]:
                        lines[i+4] = f"- **待启动：** {dashboard['by_status']['not_started']}"
                    break
            content = "\n".join(lines)
        
        # 更新分类统计
        if "### 分类统计" in content:
            lines = content.split("\n")
            for i, line in enumerate(lines):
                if "### 分类统计" in line:
                    # 清空原有分类统计行
                    j = i + 1
                    while j < len(lines) and lines[j].startswith("- "):
                        lines[j] = ""
                        j += 1
                    
                    # 添加新的分类统计
                    for category, count in dashboard["by_category"].items():
                        category_name = category.replace("category-", "").replace("-", " ")
                        lines.insert(i+1, f"- **{category_name}：** {count}个项目")
                    break
            content = "\n".join(lines)
        
        # 写入更新后的内容
        panel_path.write_text(content, encoding="utf-8")
        print(f"项目管理面板已更新: {panel_path}")
    
    def run(self):
        """运行进度追踪"""
        print("开始扫描项目进度...")
        
        # 扫描所有项目
        projects = self.scan_projects()
        print(f"找到 {len(projects)} 个项目")
        
        # 生成仪表板数据
        dashboard = self.generate_dashboard(projects)
        
        # 输出摘要
        print("\n📊 项目进度摘要:")
        print(f"  项目总数: {dashboard['total_projects']}")
        print(f"  进行中: {dashboard['by_status']['in_progress']}")
        print(f"  已完成: {dashboard['by_status']['completed']}")
        print(f"  待开始: {dashboard['by_status']['not_started']}")
        
        print("\n📦 分类统计:")
        for category, count in dashboard["by_category"].items():
            category_name = category.replace("category-", "").replace("-", " ")
            print(f"  {category_name}: {count}个项目")
        
        if dashboard["active_projects"]:
            print("\n🎯 活跃项目:")
            for project in dashboard["active_projects"]:
                print(f"  • {project['name']} ({project['category']}): {project['progress']:.1f}%")
        
        if dashboard["high_risks"]:
            print("\n⚠️ 高风险项目:")
            for risk_info in dashboard["high_risks"]:
                print(f"  • {risk_info['project']}: {len(risk_info['risks'])}个高风险")
        
        # 更新项目管理面板
        self.update_project_panel(dashboard)
        
        # 保存仪表板数据
        dashboard_path = self.workspace / "operations" / "reports" / "dashboard.json"
        dashboard_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(dashboard_path, "w", encoding="utf-8") as f:
            json.dump(dashboard, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 进度追踪完成")
        print(f"  仪表板数据已保存: {dashboard_path}")
        print(f"  项目管理面板已更新")

def main():
    """主函数"""
    tracker = ProgressTracker()
    tracker.run()

if __name__ == "__main__":
    main()