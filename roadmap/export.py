"""
Export functionality for roadmaps.
Supports JSON, YAML, CSV, and Mermaid diagram formats.
"""

import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

from .core import Roadmap, Phase, Task


class RoadmapExporter:
    """Handles exporting roadmaps to various formats."""
    
    def __init__(self, roadmap: Roadmap):
        self.roadmap = roadmap
    
    def to_json(self, indent: int = 2) -> str:
        """Export roadmap as JSON string."""
        return json.dumps(self.roadmap.to_dict(), indent=indent)
    
    def save_json(self, filepath: str):
        """Save roadmap to a JSON file."""
        with open(filepath, 'w') as f:
            f.write(self.to_json())
    
    def to_yaml(self) -> str:
        """Export roadmap as YAML string."""
        try:
            import yaml
            return yaml.dump(self.roadmap.to_dict(), default_flow_style=False, sort_keys=False)
        except ImportError:
            raise ImportError("PyYAML is required for YAML export. Install with: pip install pyyaml")
    
    def save_yaml(self, filepath: str):
        """Save roadmap to a YAML file."""
        with open(filepath, 'w') as f:
            f.write(self.to_yaml())
    
    def to_csv(self) -> str:
        """Export tasks as CSV string."""
        lines = ["id,name,description,status,priority,start_date,end_date,phase,tags,assignees"]
        
        for phase in self.roadmap.phases:
            for task in phase.tasks:
                row = [
                    task.id,
                    f'"{task.name}"',
                    f'"{task.description.replace(chr(10), " ")}"',
                    str(task.status),
                    str(task.priority),
                    task.start_date.isoformat() if task.start_date else "",
                    task.end_date.isoformat() if task.end_date else "",
                    phase.name,
                    f'"{";".join(task.tags)}"',
                    f'"{";".join(task.assignees)}"',
                ]
                lines.append(",".join(row))
        
        return "\n".join(lines)
    
    def save_csv(self, filepath: str):
        """Save tasks to a CSV file."""
        with open(filepath, 'w') as f:
            f.write(self.to_csv())
    
    def to_mermaid(self) -> str:
        """Generate Mermaid.js gantt diagram from roadmap."""
        lines = ["gantt", "    title " + self.roadmap.name, "    dateFormat  YYYY-MM-DD", ""]
        
        for phase in self.roadmap.phases:
            lines.append(f"    section {phase.name}")
            
            for task in phase.tasks:
                status_marker = ""
                if task.status.value == "completed":
                    status_marker = "done"
                elif task.status.value == "in_progress":
                    status_marker = "active"
                elif task.status.value == "blocked":
                    status_marker = "crit"
                
                start = task.start_date.isoformat() if task.start_date else "2024-01-01"
                end = task.end_date.isoformat() if task.end_date else "2024-12-31"
                
                lines.append(f"    {task.name} :{status_marker}, {start}, {end}")
        
        return "\n".join(lines)
    
    def save_mermaid(self, filepath: str):
        """Save Mermaid diagram to a file."""
        with open(filepath, 'w') as f:
            f.write(self.to_mermaid())
    
    def to_markdown(self) -> str:
        """Generate Markdown documentation of the roadmap."""
        lines = [
            f"# {self.roadmap.name}",
            "",
            self.roadmap.description,
            "",
            f"**Overall Progress:** {self.roadmap.overall_progress:.1f}%",
            f"**Total Tasks:** {self.roadmap.total_tasks}",
            f"**Completed Tasks:** {self.roadmap.completed_tasks}",
            "",
            "---",
            "",
        ]
        
        for phase in self.roadmap.phases:
            lines.append(f"## {phase.name}")
            lines.append("")
            lines.append(phase.description or "No description provided.")
            lines.append("")
            lines.append(f"**Type:** {phase.phase_type.value}")
            lines.append(f"**Progress:** {phase.progress:.1f}%")
            lines.append("")
            
            if phase.start_date:
                lines.append(f"**Start Date:** {phase.start_date.isoformat()}")
            if phase.end_date:
                lines.append(f"**End Date:** {phase.end_date.isoformat()}")
            lines.append("")
            
            if phase.tasks:
                lines.append("### Tasks")
                lines.append("")
                lines.append("| ID | Task | Status | Priority | Assignees |")
                lines.append("|---|------|--------|----------|-----------|")
                
                for task in phase.tasks:
                    assignees = ", ".join(task.assignees) if task.assignees else "Unassigned"
                    lines.append(
                        f"| {task.id} | {task.name} | {task.status.value} | {task.priority.name} | {assignees} |"
                    )
                lines.append("")
            
            if phase.milestones:
                lines.append("### Milestones")
                lines.append("")
                for milestone in phase.milestones:
                    achieved = "✓" if milestone.is_achieved() else "○"
                    lines.append(f"- {achieved} **{milestone.name}** - {milestone.description}")
                lines.append("")
            
            lines.append("---")
            lines.append("")
        
        return "\n".join(lines)
    
    def save_markdown(self, filepath: str):
        """Save Markdown documentation to a file."""
        with open(filepath, 'w') as f:
            f.write(self.to_markdown())
    
    def export_all(self, output_dir: str, prefix: Optional[str] = None):
        """Export roadmap to all supported formats."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        name = prefix or self.roadmap.name.lower().replace(" ", "_")
        
        self.save_json(str(output_path / f"{name}.json"))
        self.save_csv(str(output_path / f"{name}_tasks.csv"))
        self.save_mermaid(str(output_path / f"{name}.mmd"))
        self.save_markdown(str(output_path / f"{name}.md"))
        
        try:
            self.save_yaml(str(output_path / f"{name}.yaml"))
        except ImportError:
            pass  # Skip YAML if PyYAML not installed
        
        return list(output_path.glob(f"{name}*"))
