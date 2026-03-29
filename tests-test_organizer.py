import pytest
import os
import json
from datetime import datetime
from src.organizer import StudyOrganizer

@pytest.fixture
def organizer():
    """Create a temporary organizer for testing."""
    test_organizer = StudyOrganizer("test_data.json")
    yield test_organizer
    # Cleanup
    if os.path.exists("test_data.json"):
        os.remove("test_data.json")

class TestDisciplineManagement:
    """Test cases for discipline management."""
    
    def test_add_discipline_success(self, organizer):
        """Test adding a valid discipline."""
        discipline = organizer.add_discipline("Mathematics", 4)
        assert discipline['name'] == "Mathematics"
        assert discipline['difficulty'] == 4
        assert 'id' in discipline
        assert 'created_at' in discipline
    
    def test_add_multiple_disciplines(self, organizer):
        """Test adding multiple disciplines."""
        organizer.add_discipline("Math", 4)
        organizer.add_discipline("Physics", 5)
        organizer.add_discipline("Chemistry", 3)
        
        disciplines = organizer.get_disciplines()
        assert len(disciplines) == 3
    
    def test_add_discipline_empty_name(self, organizer):
        """Test adding a discipline with empty name."""
        with pytest.raises(ValueError):
            organizer.add_discipline("", 3)
    
    def test_add_discipline_invalid_difficulty(self, organizer):
        """Test adding a discipline with invalid difficulty."""
        with pytest.raises(ValueError):
            organizer.add_discipline("Math", 0)
        
        with pytest.raises(ValueError):
            organizer.add_discipline("Math", 6)
    
    def test_add_duplicate_discipline(self, organizer):
        """Test adding duplicate discipline."""
        organizer.add_discipline("Math", 3)
        with pytest.raises(ValueError):
            organizer.add_discipline("Math", 4)
    
    def test_get_disciplines_sorted(self, organizer):
        """Test that disciplines are sorted alphabetically."""
        organizer.add_discipline("Zebra", 2)
        organizer.add_discipline("Apple", 3)
        organizer.add_discipline("Banana", 1)
        
        disciplines = organizer.get_disciplines()
        names = [d['name'] for d in disciplines]
        assert names == ["Apple", "Banana", "Zebra"]
    
    def test_get_discipline_by_id(self, organizer):
        """Test retrieving discipline by ID."""
        discipline = organizer.add_discipline("Math", 3)
        retrieved = organizer.get_discipline_by_id(discipline['id'])
        assert retrieved['name'] == "Math"
    
    def test_delete_discipline(self, organizer):
        """Test deleting a discipline."""
        discipline = organizer.add_discipline("Math", 3)
        assert organizer.delete_discipline(discipline['id'])
        assert organizer.get_discipline_by_id(discipline['id']) is None
    
    def test_delete_nonexistent_discipline(self, organizer):
        """Test deleting a non-existent discipline."""
        assert not organizer.delete_discipline(999)

class TestTaskManagement:
    """Test cases for task management."""
    
    def test_add_task_success(self, organizer):
        """Test adding a valid task."""
        discipline = organizer.add_discipline("Math", 3)
        task = organizer.add_task(
            discipline['id'],
            "Solve equations",
            "2024-04-10",
            3
        )
        assert task['description'] == "Solve equations"
        assert task['priority'] == 3
        assert task['discipline_id'] == discipline['id']
    
    def test_add_task_empty_description(self, organizer):
        """Test adding a task with empty description."""
        discipline = organizer.add_discipline("Math", 3)
        with pytest.raises(ValueError):
            organizer.add_task(discipline['id'], "", "2024-04-10", 3)
    
    def test_add_task_invalid_priority(self, organizer):
        """Test adding a task with invalid priority."""
        discipline = organizer.add_discipline("Math", 3)
        with pytest.raises(ValueError):
            organizer.add_task(discipline['id'], "Task", "2024-04-10", 0)
        
        with pytest.raises(ValueError):
            organizer.add_task(discipline['id'], "Task", "2024-04-10", 6)
    
    def test_add_task_nonexistent_discipline(self, organizer):
        """Test adding a task to non-existent discipline."""
        with pytest.raises(ValueError):
            organizer.add_task(999, "Task", "2024-04-10", 3)
    
    def test_get_tasks_sorted(self, organizer):
        """Test that tasks are sorted by due date and priority."""
        discipline = organizer.add_discipline("Math", 3)
        
        organizer.add_task(discipline['id'], "Task 1", "2024-04-15", 1)
        organizer.add_task(discipline['id'], "Task 2", "2024-04-10", 5)
        organizer.add_task(discipline['id'], "Task 3", "2024-04-10", 2)
        
        tasks = organizer.get_tasks()
        # Tasks should be sorted by due date first, then by priority (descending)
        assert tasks[0]['due_date'] == "2024-04-10"
        assert tasks[0]['priority'] == 5
    
    def test_get_pending_tasks(self, organizer):
        """Test retrieving pending tasks."""
        discipline = organizer.add_discipline("Math", 3)
        
        task1 = organizer.add_task(discipline['id'], "Task 1", "2024-04-10", 3)
        task2 = organizer.add_task(discipline['id'], "Task 2", "2024-04-15", 2)
        
        # Mark one as completed
        organizer.mark_task_completed(task1['id'])
        
        pending = organizer.get_pending_tasks()
        assert len(pending) == 1
        assert pending[0]['id'] == task2['id']
    
    def test_mark_task_completed(self, organizer):
        """Test marking a task as completed."""
        discipline = organizer.add_discipline("Math", 3)
        task = organizer.add_task(discipline['id'], "Task", "2024-04-10", 3)
        
        assert organizer.mark_task_completed(task['id'])
        tasks = organizer.get_tasks()
        assert tasks[0]['completed']
    
    def test_delete_task(self, organizer):
        """Test deleting a task."""
        discipline = organizer.add_discipline("Math", 3)
        task = organizer.add_task(discipline['id'], "Task", "2024-04-10", 3)
        
        assert organizer.delete_task(task['id'])
        assert len(organizer.get_tasks()) == 0
    
    def test_get_tasks_by_discipline(self, organizer):
        """Test retrieving tasks by discipline."""
        math = organizer.add_discipline("Math", 3)
        physics = organizer.add_discipline("Physics", 4)
        
        organizer.add_task(math['id'], "Math Task", "2024-04-10", 3)
        organizer.add_task(physics['id'], "Physics Task", "2024-04-15", 4)
        
        math_tasks = organizer.get_tasks_by_discipline(math['id'])
        assert len(math_tasks) == 1
        assert math_tasks[0]['discipline_name'] == "Math"

class TestStatistics:
    """Test cases for statistics."""
    
    def test_get_statistics(self, organizer):
        """Test getting study statistics."""
        math = organizer.add_discipline("Math", 4)
        physics = organizer.add_discipline("Physics", 5)
        
        organizer.add_task(math['id'], "Task 1", "2024-04-10", 3)
        organizer.add_task(physics['id'], "Task 2", "2024-04-15", 4)
        
        stats = organizer.get_statistics()
        assert stats['total_disciplines'] == 2
        assert stats['total_tasks'] == 2
        assert stats['pending_tasks'] == 2
        assert stats['completed_tasks'] == 0
        assert stats['average_difficulty'] == 4.5

class TestDataPersistence:
    """Test cases for data persistence."""
    
    def test_save_and_load_data(self):
        """Test saving and loading data."""
        organizer1 = StudyOrganizer("test_persistence.json")
        organizer1.add_discipline("Math", 3)
        organizer1.add_discipline("Physics", 4)
        
        # Create new organizer instance and load data
        organizer2 = StudyOrganizer("test_persistence.json")
        disciplines = organizer2.get_disciplines()
        
        assert len(disciplines) == 2
        assert disciplines[0]['name'] in ["Math", "Physics"]
        
        # Cleanup
        if os.path.exists("test_persistence.json"):
            os.remove("test_persistence.json")