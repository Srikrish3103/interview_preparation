"""
Visualization utilities for roadmaps.
"""

from typing import List, Dict, Any, Optional
from datetime import date

from .core import Roadmap, Phase, Task


class RoadmapVisualizer:
    """Generate visual representations of roadmaps."""
    
    def __init__(self, roadmap: Roadmap):
        self.roadmap = roadmap
    
    def print_tree(self, show_status: bool = True, show_progress: bool = True) -> str:
        """Print a tree representation of the roadmap."""
        lines = []
        lines.append(f"📋 {self.roadmap.name}")
        if self.roadmap.description:
            lines.append(f"   {self.roadmap.description}")
        lines.append("")
        
        for i, phase in enumerate(self.roadmap.phases):
            is_last_phase = i == len(self.roadmap.phases) - 1
            phase_icon = "✅" if phase.status.value == "completed" else "🔄" if phase.status.value == "in_progress" else "⏳"
            
            lines.append(f"{phase_icon} {phase.name}")
            
            if show_progress:
                lines.append(f"   Progress: {phase.progress:.0f}%")
            
            if phase.tasks:
                for j, task in enumerate(phase.tasks):
                    is_last_task = j == len(phase.tasks) - 1
                    status_icon = self._get_status_icon(task.status)
                    
                    connector = "└──" if is_last_task else "├──"
                    lines.append(f"   {connector} {status_icon} {task.name}")
                    
                    if show_status and task.assignees:
                        lines.append(f"       👥 {', '.join(task.assignees)}")
            
            if phase.milestones:
                lines.append("   Milestones:")
                for milestone in phase.milestones:
                    achieved = "✓" if milestone.is_achieved() else "○"
                    lines.append(f"      {achieved} {milestone.name}")
            
            if not is_last_phase:
                lines.append("")
        
        return "\n".join(lines)
    
    def _get_status_icon(self, status) -> str:
        """Get emoji icon for task status."""
        icons = {
            "not_started": "⚪",
            "in_progress": "🔵",
            "blocked": "🔴",
            "completed": "🟢",
            "cancelled": "❌",
        }
        return icons.get(status.value, "⚪")
    
    def print_timeline(self) -> str:
        """Print a simple text-based timeline."""
        lines = []
        lines.append(f"Timeline: {self.roadmap.name}")
        lines.append("=" * 60)
        
        # Find date range
        all_dates = []
        for phase in self.roadmap.phases:
            if phase.start_date:
                all_dates.append(phase.start_date)
            if phase.end_date:
                all_dates.append(phase.end_date)
            for task in phase.tasks:
                if task.start_date:
                    all_dates.append(task.start_date)
                if task.end_date:
                    all_dates.append(task.end_date)
        
        if not all_dates:
            lines.append("No dates specified")
            return "\n".join(lines)
        
        min_date = min(all_dates)
        max_date = max(all_dates)
        
        # Create timeline header
        lines.append(f"{min_date.isoformat():<15} {' ' * 25} {max_date.isoformat():>15}")
        lines.append("-" * 60)
        
        for phase in self.roadmap.phases:
            lines.append(f"\n{phase.name}:")
            
            for task in phase.tasks:
                if task.start_date or task.end_date:
                    start_str = task.start_date.isoformat() if task.start_date else "?"
                    end_str = task.end_date.isoformat() if task.end_date else "?"
                    status = self._get_status_icon(task.status)
                    lines.append(f"  {status} {task.name}: {start_str} → {end_str}")
        
        return "\n".join(lines)
    
    def get_gantt_data(self) -> List[Dict[str, Any]]:
        """Get data formatted for Gantt chart libraries."""
        tasks = []
        
        for phase in self.roadmap.phases:
            for task in phase.tasks:
                task_data = {
                    "id": task.id,
                    "name": task.name,
                    "phase": phase.name,
                    "start": task.start_date.isoformat() if task.start_date else None,
                    "end": task.end_date.isoformat() if task.end_date else None,
                    "status": task.status.value,
                    "progress": 100 if task.is_complete() else (50 if task.status.value == "in_progress" else 0),
                    "dependencies": task.dependencies,
                }
                tasks.append(task_data)
        
        return tasks
    
    def print_summary(self) -> str:
        """Print a summary of the roadmap."""
        lines = []
        lines.append("=" * 50)
        lines.append(f"ROADMAP SUMMARY: {self.roadmap.name}")
        lines.append("=" * 50)
        lines.append("")
        lines.append(f"Total Phases:     {len(self.roadmap.phases)}")
        lines.append(f"Total Tasks:      {self.roadmap.total_tasks}")
        lines.append(f"Completed Tasks:  {self.roadmap.completed_tasks}")
        lines.append(f"Overall Progress: {self.roadmap.overall_progress:.1f}%")
        lines.append("")
        lines.append("Status Breakdown:")
        
        for status, count in self.roadmap.status_summary.items():
            if count > 0:
                icon = self._get_status_icon(type('obj', (object,), {'value': status})())
                lines.append(f"  {icon} {status}: {count}")
        
        lines.append("")
        lines.append("Phases:")
        for phase in self.roadmap.phases:
            lines.append(f"  • {phase.name}: {phase.progress:.0f}% complete")
        
        lines.append("=" * 50)
        return "\n".join(lines)
    
    def to_ascii_gantt(self, width: int = 60) -> str:
        """Generate an ASCII Gantt chart."""
        lines = []
        lines.append(f"Gantt Chart: {self.roadmap.name}")
        lines.append("-" * width)
        
        # Calculate bar width for progress
        bar_width = 20
        
        for phase in self.roadmap.phases:
            lines.append(f"\n{phase.name}")
            lines.append("  " + "-" * (bar_width + 10))
            
            for task in phase.tasks:
                # Calculate progress bar
                if task.is_complete():
                    filled = bar_width
                elif task.status.value == "in_progress":
                    filled = bar_width // 2
                else:
                    filled = 0
                
                empty = bar_width - filled
                bar = "█" * filled + "░" * empty
                
                status = self._get_status_icon(task.status)
                lines.append(f"  {task.name[:20]:<20} |{bar}| {status}")
        
        return "\n".join(lines)
