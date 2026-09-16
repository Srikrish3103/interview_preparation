"""
Enumeration types for roadmap components.
"""

from enum import Enum


class Status(Enum):
    """Status of a task or phase."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    
    def __str__(self):
        return self.value


class Priority(Enum):
    """Priority levels for tasks."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4
    
    def __str__(self):
        return self.name.lower()


class PhaseType(Enum):
    """Types of phases in a roadmap."""
    PLANNING = "planning"
    DEVELOPMENT = "development"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    MAINTENANCE = "maintenance"
    RESEARCH = "research"
    DESIGN = "design"
    
    def __str__(self):
        return self.value
