import pytest
from datetime import time
from src.scheduler import StudyScheduler

@pytest.fixture
def scheduler():
    """Create a scheduler instance for testing."""
    return StudyScheduler()

@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    disciplines = [
        {'id': 1, 'name': 'Mathematics', 'difficulty': 4},
        {'id': 2, 'name': 'Physics', 'difficulty': 5},
        {'id': 3, 'name': 'Chemistry', 'difficulty': 3},
    ]
    
    tasks = [
        {
            'id': 1,
            'discipline_id': 1,
            'discipline_name': 'Mathematics',
            'description': 'Solve equations',
            'due_date': '2024-04-10',
            'priority': 5,
            'completed': False
        },
        {
            'id': 2,
            'discipline_id': 2,
            'discipline_name': 'Physics',
            'description': 'Study mechanics',
            'due_date': '2024-04-12',
            'priority': 4,
            'completed': False
        },
        {
            'id': 3,
            'discipline_id': 3,
            'discipline_name': 'Chemistry',
            'description': 'Lab report',
            'due_date': '2024-04-15',
            'priority': 3,
            'completed': False
        },
    ]
    
    return disciplines, tasks

class TestScheduleGeneration:
    """Test cases for schedule generation."""
    
    def test_generate_schedule_basic(self, scheduler, sample_data):
        """Test basic schedule generation."""
        disciplines, tasks = sample_data
        schedule = scheduler.generate_schedule(
            tasks,
            disciplines,
            hours_per_day=4,
            start_time=time(18, 0)
        )
        
        assert isinstance(schedule, dict)
        assert len(schedule) == 7  # 7 days of week
        assert all(day in schedule for day in scheduler.days_of_week)
    
    def test_schedule_respects_hours_per_day(self, scheduler, sample_data):
        """Test that schedule respects hours per day limit."""
        disciplines, tasks = sample_data
        hours_per_day = 3
        schedule = scheduler.generate_schedule(
            tasks,
            disciplines,
            hours_per_day=hours_per_day,
            start_time=time(18, 0)
        )
        
        minutes_per_day = hours_per_day * 60
        for day, activities in schedule.items():
            total_minutes = sum(a['duration_minutes'] for a in activities)
            assert total_minutes <= minutes_per_day
    
    def test_schedule_orders_by_priority(self, scheduler, sample_data):
        """Test that tasks are scheduled by priority."""
        disciplines, tasks = sample_data
        schedule = scheduler.generate_schedule(
            tasks,
            disciplines,
            hours_per_day=4,
            start_time=time(18, 0)
        )
        
        # Get all scheduled activities
        all_activities = []
        for activities in schedule.values():
            all_activities.extend(activities)
        
        # Check that higher priority tasks appear first
        if len(all_activities) >= 2:
            assert all_activities[0]['priority'] >= all_activities[1]['priority']
    
    def test_schedule_with_empty_tasks(self, scheduler, sample_data):
        """Test schedule generation with empty tasks."""
        disciplines, _ = sample_data
        schedule = scheduler.generate_schedule([], disciplines, 4, time(18, 0))
        
        # All days should be empty
        assert all(len(activities) == 0 for activities in schedule.values())
    
    def test_schedule_with_empty_disciplines(self, scheduler, sample_data):
        """Test schedule generation with empty disciplines."""
        _, tasks = sample_data
        schedule = scheduler.generate_schedule(tasks, [], 4, time(18, 0))
        
        # All days should be empty
        assert all(len(activities) == 0 for activities in schedule.values())
    
    def test_schedule_start_time(self, scheduler, sample_data):
        """Test that schedule respects start time."""
        disciplines, tasks = sample_data
        start_time = time(20, 0)
        schedule = scheduler.generate_schedule(
            tasks,
            disciplines,
            hours_per_day=4,
            start_time=start_time
        )
        
        # Find first activity
        for activities in schedule.values():
            if activities:
                first_activity = activities[0]
                # Should start at or after the specified time
                time_parts = first_activity['time'].split(':')
                hour = int(time_parts[0])
                assert hour >= start_time.hour

class TestScheduleRetrieval:
    """Test cases for schedule retrieval."""
    
    def test_get_schedule(self, scheduler, sample_data):
        """Test retrieving the generated schedule."""
        disciplines, tasks = sample_data
        generated = scheduler.generate_schedule(
            tasks,
            disciplines,
            hours_per_day=4,
            start_time=time(18, 0)
        )
        
        retrieved = scheduler.get_schedule()
        assert generated == retrieved
    
    def test_get_today_schedule(self, scheduler, sample_data):
        """Test retrieving today's schedule."""
        disciplines, tasks = sample_data
        scheduler.generate_schedule(
            tasks,
            disciplines,
            hours_per_day=4,
            start_time=time(18, 0)
        )
        
        today_schedule = scheduler.get_today_schedule()
        assert isinstance(today_schedule, list)

class TestScheduleExport:
    """Test cases for schedule export."""
    
    def test_export_to_csv(self, scheduler, sample_data):
        """Test exporting schedule to CSV."""
        import os
        import csv
        
        disciplines, tasks = sample_data
        scheduler.generate_schedule(
            tasks,
            disciplines,
            hours_per_day=4,
            start_time=time(18, 0)
        )
        
        # Export
        assert scheduler.export_schedule_to_csv("test_schedule.csv")
        
        # Verify file was created
        assert os.path.exists("test_schedule.csv")
        
        # Cleanup
        os.remove("test_schedule.csv")