from datetime import datetime, timedelta, time
from typing import List, Dict, Optional
import pandas as pd

class StudyScheduler:
    """
    Class responsible for generating intelligent study schedules.
    """
    
    def __init__(self):
        self.schedule = {}
        self.days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    def generate_schedule(
        self, 
        tasks: List[Dict], 
        disciplines: List[Dict], 
        hours_per_day: float,
        start_time: time,
        num_days: int = 7
    ) -> Dict[str, List[Dict]]:
        """
        Generate an intelligent study schedule based on tasks and available time.
        
        Args:
            tasks (List[Dict]): List of pending tasks to schedule
            disciplines (List[Dict]): List of disciplines with difficulty levels
            hours_per_day (float): Hours available for study per day
            start_time (time): Start time for studying
            num_days (int): Number of days to generate schedule for
        
        Returns:
            Dict: Schedule organized by day of week
        """
        schedule = {day: [] for day in self.days_of_week}
        
        if not tasks or not disciplines:
            return schedule
        
        # Sort tasks by priority (descending) and due date (ascending)
        sorted_tasks = sorted(
            tasks, 
            key=lambda x: (-x['priority'], x['due_date'])
        )
        
        # Create a difficulty map for disciplines
        difficulty_map = {d['name']: d['difficulty'] for d in disciplines}
        
        # Convert start_time to minutes
        start_minutes = start_time.hour * 60 + start_time.minute
        minutes_per_day = int(hours_per_day * 60)
        session_duration = 60  # 1 hour per session
        
        day_index = 0
        current_day_minutes = 0
        
        for task in sorted_tasks:
            discipline_name = task.get('discipline_name', 'Unknown')
            difficulty = difficulty_map.get(discipline_name, 3)
            
            # Calculate estimated time based on difficulty
            base_time = 60
            time_multiplier = 1 + (difficulty - 1) * 0.25
            estimated_minutes = int(base_time * time_multiplier)
            
            # Find available slot
            while current_day_minutes + estimated_minutes > minutes_per_day and day_index < num_days:
                day_index += 1
                current_day_minutes = 0
            
            if day_index >= num_days:
                break
            
            # Calculate actual time for this session
            session_minutes = min(session_duration, estimated_minutes)
            
            # Format time
            total_minutes = start_minutes + current_day_minutes
            hours = (total_minutes // 60) % 24
            minutes = total_minutes % 60
            end_minutes = total_minutes + session_minutes
            end_hours = (end_minutes // 60) % 24
            end_mins = end_minutes % 60
            
            time_str = f"{int(hours):02d}:{int(minutes):02d}"
            end_time_str = f"{int(end_hours):02d}:{int(end_mins):02d}"
            
            # Add to schedule
            current_day = self.days_of_week[day_index]
            schedule[current_day].append({
                'id': task.get('id'),
                'time': time_str,
                'end_time': end_time_str,
                'discipline': discipline_name,
                'task': task['description'],
                'priority': task['priority'],
                'duration_minutes': session_minutes
            })
            
            current_day_minutes += session_minutes
        
        self.schedule = schedule
        return schedule
    
    def get_schedule(self) -> Dict[str, List[Dict]]:
        """Get the current schedule."""
        return self.schedule
    
    def get_today_schedule(self) -> List[Dict]:
        """Get today's schedule."""
        today = datetime.now().strftime('%A')
        return self.schedule.get(today, [])
    
    def export_schedule_to_csv(self, filename: str = "schedule.csv") -> bool:
        """Export schedule to CSV file."""
        try:
            data = []
            for day, activities in self.schedule.items():
                for activity in activities:
                    data.append({
                        'Day': day,
                        'Time': activity['time'],
                        'End Time': activity['end_time'],
                        'Discipline': activity['discipline'],
                        'Task': activity['task'],
                        'Priority': activity['priority'],
                        'Duration (min)': activity['duration_minutes']
                    })
            
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False, encoding='utf-8')
            return True
        except Exception as e:
            print(f"Error exporting schedule: {e}")
            return False