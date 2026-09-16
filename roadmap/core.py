"""
Core components for roadmap management.
"""

from datetime import date, datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from uuid import uuid4

from .enums import Status, Priority, PhaseType


@dataclass
class Task:
    """Represents a single task in the roadmap."""
    name: str
    description: str = ""
    status: Status = Status.NOT_STARTED
    priority: Priority = Priority.MEDIUM
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    dependencies: List[str] = field(default_factory=list)  # List of task IDs
    tags: List[str] = field(default_factory=list)
    id: str = field(default_factory=lambda: str(uuid4())[:8])
    assignees: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        if isinstance(self.status, str):
            self.status = Status(self.status)
        if isinstance(self.priority, str):
            self.priority = Priority[self.priority.upper()]
    
    def is_complete(self) -> bool:
        return self.status == Status.COMPLETED
    
    def add_dependency(self, task_id: str):
        """Add a dependency on another task."""
        if task_id not in self.dependencies:
            self.dependencies.append(task_id)
    
    def remove_dependency(self, task_id: str):
        """Remove a dependency."""
        if task_id in self.dependencies:
            self.dependencies.remove(task_id)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": str(self.status),
            "priority": str(self.priority),
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "dependencies": self.dependencies,
            "tags": self.tags,
            "assignees": self.assignees,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """Create a Task from a dictionary."""
        return cls(
            id=data.get("id", str(uuid4())[:8]),
            name=data["name"],
            description=data.get("description", ""),
            status=data.get("status", Status.NOT_STARTED),
            priority=data.get("priority", Priority.MEDIUM),
            start_date=datetime.fromisoformat(data["start_date"]).date() if data.get("start_date") else None,
            end_date=datetime.fromisoformat(data["end_date"]).date() if data.get("end_date") else None,
            dependencies=data.get("dependencies", []),
            tags=data.get("tags", []),
            assignees=data.get("assignees", []),
        )


@dataclass
class Milestone:
    """Represents a milestone in the roadmap."""
    name: str
    description: str = ""
    target_date: Optional[date] = None
    completed_date: Optional[date] = None
    tasks: List[str] = field(default_factory=list)  # List of task IDs
    id: str = field(default_factory=lambda: str(uuid4())[:8])
    
    def is_achieved(self) -> bool:
        return self.completed_date is not None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert milestone to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "target_date": self.target_date.isoformat() if self.target_date else None,
            "completed_date": self.completed_date.isoformat() if self.completed_date else None,
            "tasks": self.tasks,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Milestone":
        """Create a Milestone from a dictionary."""
        return cls(
            id=data.get("id", str(uuid4())[:8]),
            name=data["name"],
            description=data.get("description", ""),
            target_date=datetime.fromisoformat(data["target_date"]).date() if data.get("target_date") else None,
            completed_date=datetime.fromisoformat(data["completed_date"]).date() if data.get("completed_date") else None,
            tasks=data.get("tasks", []),
        )


@dataclass
class Phase:
    """Represents a phase containing multiple tasks."""
    name: str
    description: str = ""
    phase_type: PhaseType = PhaseType.DEVELOPMENT
    tasks: List[Task] = field(default_factory=list)
    milestones: List[Milestone] = field(default_factory=list)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    id: str = field(default_factory=lambda: str(uuid4())[:8])
    
    def __post_init__(self):
        if isinstance(self.phase_type, str):
            self.phase_type = PhaseType(self.phase_type)
    
    @property
    def progress(self) -> float:
        """Calculate phase completion percentage."""
        if not self.tasks:
            return 0.0
        completed = sum(1 for t in self.tasks if t.is_complete())
        return (completed / len(self.tasks)) * 100
    
    @property
    def status(self) -> Status:
        """Determine overall phase status."""
        if not self.tasks:
            return Status.NOT_STARTED
        
        all_complete = all(t.is_complete() for t in self.tasks)
        any_in_progress = any(t.status == Status.IN_PROGRESS for t in self.tasks)
        any_blocked = any(t.status == Status.BLOCKED for t in self.tasks)
        
        if all_complete:
            return Status.COMPLETED
        elif any_blocked:
            return Status.BLOCKED
        elif any_in_progress:
            return Status.IN_PROGRESS
        else:
            return Status.NOT_STARTED
    
    def add_task(self, task: Task):
        """Add a task to this phase."""
        self.tasks.append(task)
    
    def remove_task(self, task_id: str):
        """Remove a task by ID."""
        self.tasks = [t for t in self.tasks if t.id != task_id]
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert phase to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "phase_type": str(self.phase_type),
            "tasks": [t.to_dict() for t in self.tasks],
            "milestones": [m.to_dict() for m in self.milestones],
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "progress": self.progress,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Phase":
        """Create a Phase from a dictionary."""
        phase = cls(
            id=data.get("id", str(uuid4())[:8]),
            name=data["name"],
            description=data.get("description", ""),
            phase_type=data.get("phase_type", PhaseType.DEVELOPMENT),
            start_date=datetime.fromisoformat(data["start_date"]).date() if data.get("start_date") else None,
            end_date=datetime.fromisoformat(data["end_date"]).date() if data.get("end_date") else None,
        )
        phase.tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
        phase.milestones = [Milestone.from_dict(m) for m in data.get("milestones", [])]
        return phase


class Roadmap:
    """Main class representing a complete roadmap."""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.phases: List[Phase] = []
        self.created_at: datetime = datetime.now()
        self.updated_at: datetime = datetime.now()
        self.id: str = str(uuid4())[:8]
    
    def add_phase(self, phase: Phase):
        """Add a phase to the roadmap."""
        self.phases.append(phase)
        self.updated_at = datetime.now()
    
    def remove_phase(self, phase_id: str):
        """Remove a phase by ID."""
        self.phases = [p for p in self.phases if p.id != phase_id]
        self.updated_at = datetime.now()
    
    def get_phase(self, phase_id: str) -> Optional[Phase]:
        """Get a phase by ID."""
        for phase in self.phases:
            if phase.id == phase_id:
                return phase
        return None
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID across all phases."""
        for phase in self.phases:
            task = phase.get_task(task_id)
            if task:
                return task
        return None
    
    def find_task_by_name(self, name: str) -> Optional[Task]:
        """Find a task by name (case-insensitive)."""
        for phase in self.phases:
            for task in phase.tasks:
                if task.name.lower() == name.lower():
                    return task
        return None
    
    @property
    def total_tasks(self) -> int:
        """Total number of tasks in the roadmap."""
        return sum(len(p.tasks) for p in self.phases)
    
    @property
    def completed_tasks(self) -> int:
        """Number of completed tasks."""
        return sum(sum(1 for t in p.tasks if t.is_complete()) for p in self.phases)
    
    @property
    def overall_progress(self) -> float:
        """Overall completion percentage."""
        if self.total_tasks == 0:
            return 0.0
        return (self.completed_tasks / self.total_tasks) * 100
    
    @property
    def status_summary(self) -> Dict[str, int]:
        """Summary of task statuses."""
        summary = {str(s): 0 for s in Status}
        for phase in self.phases:
            for task in phase.tasks:
                summary[str(task.status)] += 1
        return summary
    
    def validate_dependencies(self) -> List[str]:
        """Validate that all task dependencies exist."""
        errors = []
        all_task_ids = set()
        
        # Collect all task IDs
        for phase in self.phases:
            for task in phase.tasks:
                all_task_ids.add(task.id)
        
        # Check dependencies
        for phase in self.phases:
            for task in phase.tasks:
                for dep_id in task.dependencies:
                    if dep_id not in all_task_ids:
                        errors.append(f"Task {task.id} has invalid dependency: {dep_id}")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert roadmap to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "phases": [p.to_dict() for p in self.phases],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "overall_progress": self.overall_progress,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Roadmap":
        """Create a Roadmap from a dictionary."""
        roadmap = cls(
            name=data["name"],
            description=data.get("description", ""),
        )
        roadmap.id = data.get("id", str(uuid4())[:8])
        roadmap.phases = [Phase.from_dict(p) for p in data.get("phases", [])]
        return roadmap
    
    def __repr__(self):
        return f"Roadmap(name='{self.name}', phases={len(self.phases)}, progress={self.overall_progress:.1f}%)"
