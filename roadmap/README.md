# Roadmap Python Package

A comprehensive Python package for creating, managing, and visualizing project roadmaps.

## Features

- **Create Roadmaps**: Define phases, tasks, and milestones with ease
- **Track Progress**: Monitor completion status at task, phase, and roadmap levels
- **Manage Dependencies**: Set up task dependencies to ensure proper sequencing
- **Priority Management**: Assign priorities (Low, Medium, High, Critical) to tasks
- **Team Assignment**: Assign team members to tasks
- **Multiple Export Formats**: Export to JSON, YAML, CSV, Mermaid diagrams, and Markdown
- **Visualization**: Generate tree views, timelines, and ASCII Gantt charts

## Installation

```bash
pip install roadmap  # Or use the local package
```

For local development:
```bash
cd /workspace
export PYTHONPATH=/workspace:$PYTHONPATH
```

## Quick Start

```python
from datetime import date
from roadmap import Roadmap, Phase, Task, Milestone, Status, Priority
from roadmap.enums import PhaseType

# Create a roadmap
roadmap = Roadmap(
    name="Product Launch",
    description="Roadmap for our new product"
)

# Create a phase
phase = Phase(
    name="Phase 1: Planning",
    phase_type=PhaseType.PLANNING,
    start_date=date(2024, 1, 1),
    end_date=date(2024, 3, 31)
)

# Add tasks
task = Task(
    name="Market Research",
    description="Analyze market trends",
    status=Status.IN_PROGRESS,
    priority=Priority.HIGH,
    assignees=["Alice", "Bob"]
)
phase.add_task(task)

# Add milestone
phase.milestones.append(Milestone(
    name="Planning Complete",
    target_date=date(2024, 3, 31)
))

# Add phase to roadmap
roadmap.add_phase(phase)

# View progress
print(f"Overall Progress: {roadmap.overall_progress:.1f}%")
```

## Visualization

```python
from roadmap.visualize import RoadmapVisualizer

visualizer = RoadmapVisualizer(roadmap)

# Print tree view
print(visualizer.print_tree())

# Print summary
print(visualizer.print_summary())

# Generate ASCII Gantt chart
print(visualizer.to_ascii_gantt())
```

## Export Options

```python
from roadmap.export import RoadmapExporter

exporter = RoadmapExporter(roadmap)

# Export to different formats
json_str = exporter.to_json()
csv_str = exporter.to_csv()
mermaid_str = exporter.to_mermaid()
markdown_str = exporter.to_markdown()

# Save to files
exporter.save_json("roadmap.json")
exporter.save_csv("tasks.csv")
exporter.save_mermaid("diagram.mmd")
exporter.save_markdown("documentation.md")

# Export all formats at once
exporter.export_all("./output", prefix="my_roadmap")
```

## API Reference

### Core Classes

#### `Roadmap`
Main class representing a complete roadmap.
- `name`: Roadmap name
- `description`: Optional description
- `phases`: List of Phase objects
- `overall_progress`: Completion percentage
- `total_tasks`: Total number of tasks
- `completed_tasks`: Number of completed tasks
- `status_summary`: Dict of status counts

#### `Phase`
Represents a phase containing multiple tasks.
- `name`: Phase name
- `phase_type`: Type from PhaseType enum
- `tasks`: List of Task objects
- `milestones`: List of Milestone objects
- `progress`: Completion percentage
- `status`: Overall phase status

#### `Task`
Represents a single task.
- `name`: Task name
- `description`: Optional description
- `status`: Status from Status enum
- `priority`: Priority from Priority enum
- `start_date`, `end_date`: Optional dates
- `dependencies`: List of dependent task IDs
- `assignees`: List of assigned team members
- `tags`: List of tags

#### `Milestone`
Represents a milestone.
- `name`: Milestone name
- `target_date`: Planned completion date
- `completed_date`: Actual completion date (if achieved)

### Enums

#### `Status`
- `NOT_STARTED`
- `IN_PROGRESS`
- `BLOCKED`
- `COMPLETED`
- `CANCELLED`

#### `Priority`
- `LOW`
- `MEDIUM`
- `HIGH`
- `CRITICAL`

#### `PhaseType`
- `PLANNING`
- `RESEARCH`
- `DESIGN`
- `DEVELOPMENT`
- `TESTING`
- `DEPLOYMENT`
- `MAINTENANCE`

## Example Output

### Tree View
```
📋 Product Development Roadmap

✅ Phase 1: Research & Planning
   Progress: 100%
   ├── 🟢 Market Research
   └── 🟢 Requirements Gathering

🔄 Phase 2: Development
   Progress: 25%
   ├── 🟢 Architecture Design
   ├── 🔵 Backend Implementation
   └── ⚪ API Integration
```

### ASCII Gantt
```
Phase 2: Development
  ------------------------------
  Architecture Design  |████████████████████| 🟢
  Backend Implementati |██████████░░░░░░░░░░| 🔵
  API Integration      |░░░░░░░░░░░░░░░░░░░░| ⚪
```

## License

MIT License
