"""
Roadmap - A comprehensive Python package for creating, managing, and visualizing project roadmaps.

This package provides tools to:
- Define roadmap phases, tasks, and milestones
- Manage dependencies between tasks
- Track progress and status
- Export roadmaps to various formats (JSON, YAML, Mermaid, etc.)
- Generate timeline visualizations
"""

__version__ = "0.1.0"
__author__ = "Roadmap Team"

from .core import Roadmap, Phase, Task, Milestone
from .enums import Status, Priority

__all__ = [
    "Roadmap",
    "Phase", 
    "Task",
    "Milestone",
    "Status",
    "Priority",
]
