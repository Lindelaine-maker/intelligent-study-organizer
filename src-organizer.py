from datetime import datetime
from typing import List, Dict, Optional
import json
import os

class StudyOrganizer:
    """
    Class responsible for organizing disciplines and tasks.
    """
    
    def __init__(self, data_file: str = "data/study_data.json"):
        self.data_file = data_file
        self.disciplines = []
        self.tasks = []
        self.next_discipline_id = 1
        self.next_task_id = 1
        self._ensure_data_dir()
        self._load_data()
    
    def _ensure_data_dir(self):
        """Ensure the data directory exists."""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
    
    def _load_data(self):
        """Load data from JSON file if it exists."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.disciplines = data.get('disciplines', [])
                    self.tasks = data.get('tasks', [])
                    self.next_discipline_id = max([d['id'] for d in self.disciplines], default=0) + 1
                    self.next_task_id = max([t['id'] for t in self.tasks], default=0) + 1
            except Exception as e:
                print(f"Error loading data: {e}")
    
    def _save_data(self):
        """Save data to JSON file."""
        try:
            data = {
                'disciplines': self.disciplines,
                'tasks': self.tasks
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def add_discipline(self, name: str, difficulty: int) -> Dict:
        """
        Add a new discipline to the organizer.
        
        Args:
            name (str): Name of the discipline
            difficulty (int): Difficulty level (1-5)
        
        Returns:
            Dict: The created discipline object
        
        Raises:
            ValueError: If name is empty or difficulty is out of range
        """
        if not name or not name.strip():
            raise ValueError("Discipline name cannot be empty")
        
        if not 1 <= difficulty <= 5:
            raise ValueError("Difficulty must be between 1 and 5")
        
        # Check for duplicates
        if any(d['name'].lower() == name.lower() for d in self.disciplines):
            raise ValueError(f"Discipline '{name}' already exists")
        
        discipline = {
            'id': self.next_discipline_id,
            'name': name.strip(),
            'difficulty': difficulty,
            'created_at': datetime.now().isoformat()
        }
        self.disciplines.append(discipline)
        self.next_discipline_id += 1
        self._save_data()
        return discipline
    
    def get_disciplines(self) -> List[Dict]:
        """Get all disciplines."""
        return sorted(self.disciplines, key=lambda x: x['name'])
    
    def get_discipline_by_id(self, discipline_id: int) -> Optional[Dict]:
        """Get a discipline by ID."""
        return next((d for d in self.disciplines if d['id'] == discipline_id), None)
    
    def delete_discipline(self, discipline_id: int) -> bool:
        """
        Delete a discipline by ID.
        
        Args:
            discipline_id (int): The ID of the discipline to delete
        
        Returns:
            bool: True if deleted, False if not found
        """
        original_length = len(self.disciplines)
        self.disciplines = [d for d in self.disciplines if d['id'] != discipline_id]
        
        if len(self.disciplines) < original_length:
            # Also delete associated tasks
            self.tasks = [t for t in self.tasks if t.get('discipline_id') != discipline_id]
            self._save_data()
            return True
        return False
    
    def add_task(self, discipline_id: int, description: str, due_date, priority: int) -> Dict:
        """
        Add a new task to a discipline.
        
        Args:
            discipline_id (int): ID of the discipline
            description (str): Task description
            due_date: Due date of the task
            priority (int): Priority level (1-5)
        
        Returns:
            Dict: The created task object
        
        Raises:
            ValueError: If parameters are invalid
        """
        if not description or not description.strip():
            raise ValueError("Task description cannot be empty")
        
        if not 1 <= priority <= 5:
            raise ValueError("Priority must be between 1 and 5")
        
        discipline = self.get_discipline_by_id(discipline_id)
        if not discipline:
            raise ValueError(f"Discipline with ID {discipline_id} not found")
        
        task = {
            'id': self.next_task_id,
            'discipline_id': discipline_id,
            'discipline_name': discipline['name'],
            'description': description.strip(),
            'due_date': str(due_date),
            'priority': priority,
            'created_at': datetime.now().isoformat(),
            'completed': False
        }
        self.tasks.append(task)
        self.next_task_id += 1
        self._save_data()
        return task
    
    def get_tasks(self) -> List[Dict]:
        """Get all tasks sorted by due date and priority."""
        return sorted(
            self.tasks, 
            key=lambda x: (x['due_date'], -x['priority'])
        )
    
    def get_tasks_by_discipline(self, discipline_id: int) -> List[Dict]:
        """Get tasks for a specific discipline."""
        return [t for t in self.get_tasks() if t['discipline_id'] == discipline_id]
    
    def get_pending_tasks(self) -> List[Dict]:
        """Get all pending tasks sorted by priority and due date."""
        pending = [t for t in self.tasks if not t['completed']]
        return sorted(pending, key=lambda x: (x['due_date'], -x['priority']))
    
    def mark_task_completed(self, task_id: int) -> bool:
        """Mark a task as completed."""
        task = next((t for t in self.tasks if t['id'] == task_id), None)
        if task:
            task['completed'] = True
            self._save_data()
            return True
        return False
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID."""
        original_length = len(self.tasks)
        self.tasks = [t for t in self.tasks if t['id'] != task_id]
        
        if len(self.tasks) < original_length:
            self._save_data()
            return True
        return False
    
    def get_statistics(self) -> Dict:
        """Get study statistics."""
        return {
            'total_disciplines': len(self.disciplines),
            'total_tasks': len(self.tasks),
            'pending_tasks': len(self.get_pending_tasks()),
            'completed_tasks': len([t for t in self.tasks if t['completed']]),
            'average_difficulty': sum(d['difficulty'] for d in self.disciplines) / len(self.disciplines) if self.disciplines else 0
        }