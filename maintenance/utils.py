"""
Utility module for intelligent schedule generation and optimization.
Implements seasonal adjustments, climate zone multipliers, and smart scheduling.
"""

from datetime import datetime, date, timedelta
from django.db.models import Count, Q
from maintenance.models import MaintenanceTask, Schedule, TaskCompletion


class ScheduleOptimizer:
    """
    Optimizes maintenance schedule generation with:
    - Seasonal awareness
    - Climate zone intelligence
    - Historical completion patterns
    - Task priority scoring
    """
    
    # Climate zone difficulty multipliers
    CLIMATE_MULTIPLIERS = {
        'tropical': 1.3,      # High humidity, more frequent maintenance
        'dry': 1.1,           # Dust, UV exposure
        'temperate': 1.0,     # Baseline
        'continental': 1.2,   # Extreme temperature swings
        'polar': 1.5,         # Harsh winters, freeze-thaw cycles
        'midwest': 1.2,
        'northeast': 1.3,
        'southeast': 1.3,     # High humidity, hurricanes
        'southwest': 1.1,     # Dry heat
        'northwest': 1.1,     # Mild, rainy
    }
    
    # Current season mapping (Northern Hemisphere)
    SEASON_MONTHS = {
        'spring': [3, 4, 5],
        'summer': [6, 7, 8],
        'fall': [9, 10, 11],
        'winter': [12, 1, 2],
    }
    
    @classmethod
    def get_current_season(cls):
        """Get the current season based on the current month."""
        current_month = datetime.now().month
        for season, months in cls.SEASON_MONTHS.items():
            if current_month in months:
                return season
        return 'any'
    
    @classmethod
    def get_seasonal_tasks(cls, queryset, prioritize_current=True):
        """
        Filter tasks by seasonal priority.
        If prioritize_current=True, boost tasks matching current season.
        """
        current_season = cls.get_current_season()
        
        if prioritize_current:
            # Prioritize tasks for current season or 'any' season
            seasonal_tasks = queryset.filter(
                Q(seasonal_priority=current_season) | 
                Q(seasonal_priority='any')
            )
            return seasonal_tasks
        
        return queryset
    
    @classmethod
    def get_climate_adjustment_factor(cls, home):
        """
        Calculate maintenance frequency multiplier based on climate zone.
        Returns: float multiplier (1.0 = standard, >1.0 = more frequent)
        """
        return cls.CLIMATE_MULTIPLIERS.get(home.climate_zone, 1.0)
    
    @classmethod
    def calculate_task_priority(cls, task, home, user):
        """
        Calculate priority score for a task based on multiple factors.
        Higher score = higher priority.
        
        Factors:
        - Seasonal match (bonus points)
        - Home age vs task applicability
        - Overdue status (if previously scheduled)
        - Historical completion rate
        """
        score = 50  # Base score
        
        # Seasonal bonus (+20 points if matches current season)
        current_season = cls.get_current_season()
        if task.seasonal_priority == current_season:
            score += 20
        elif task.seasonal_priority == 'any':
            score += 5
        
        # Home age relevance (+10 points)
        home_age = home.get_age()
        if home_age > 20 and task.applies_to_old_homes:
            score += 10
        elif home_age <= 20 and task.applies_to_new_homes:
            score += 10
        
        # Check for overdue tasks (huge bonus: +50 points)
        overdue_schedules = Schedule.objects.filter(
            home=home,
            tasks=task,
            scheduled_date__lt=date.today(),
            is_completed=False
        )
        if overdue_schedules.exists():
            score += 50
        
        # Historical completion rate (bonus for never-done tasks: +15 points)
        completion_count = TaskCompletion.objects.filter(
            schedule__home=home,
            schedule__tasks=task
        ).count()
        if completion_count == 0:
            score += 15  # Never done before
        
        # Climate zone urgency
        climate_factor = cls.get_climate_adjustment_factor(home)
        if climate_factor > 1.2:  # Extreme climate
            score += 10
        
        return score
    
    @classmethod
    def generate_next_due_date(cls, task, home, base_date=None):
        """
        Calculate the next due date for a task based on frequency and climate.
        Applies climate zone adjustments.
        """
        if base_date is None:
            base_date = date.today()
        
        # Base frequency mapping to days
        frequency_days = {
            'weekly': 7,
            'monthly': 30,
            'quarterly': 90,
            'biannual': 180,
            'annual': 365,
            'biennial': 730,
            'as_needed': 365,  # Default to annual for as-needed
        }
        
        base_days = frequency_days.get(task.frequency, 365)
        
        # Apply climate adjustment (reduces days between tasks in harsh climates)
        climate_factor = cls.get_climate_adjustment_factor(home)
        adjusted_days = int(base_days / climate_factor)
        
        next_due = base_date + timedelta(days=adjusted_days)
        return next_due
    
    @classmethod
    def get_recommended_tasks(cls, home, limit=None):
        """
        Get top recommended tasks for a home, sorted by priority score.
        Returns: list of (task, priority_score) tuples
        """
        # Get all applicable tasks
        tasks = MaintenanceTask.objects.filter(is_active=True)
        
        # Filter by seasonal relevance
        tasks = cls.get_seasonal_tasks(tasks)
        
        # Filter by home characteristics
        home_age = home.get_age()
        applicable_tasks = []
        
        for task in tasks:
            # Age requirements
            if home_age > 20 and not task.applies_to_old_homes:
                continue
            if home_age <= 20 and not task.applies_to_new_homes:
                continue
            
            # Feature requirements
            if task.requires_basement and not home.has_basement:
                continue
            if task.requires_attic and not home.has_attic:
                continue
            if task.requires_hvac and not home.has_hvac:
                continue
            if task.requires_septic and not home.has_septic:
                continue
            
            applicable_tasks.append(task)
        
        # Calculate priority scores
        task_priorities = [
            (task, cls.calculate_task_priority(task, home, home.owner))
            for task in applicable_tasks
        ]
        
        # Sort by priority (highest first)
        task_priorities.sort(key=lambda x: x[1], reverse=True)
        
        if limit:
            task_priorities = task_priorities[:limit]
        
        return task_priorities
    
    @classmethod
    def generate_annual_schedule(cls, home):
        """
        Generate a full year of scheduled tasks, distributed across months.
        Returns: list of (task, scheduled_date) tuples
        """
        today = date.today()
        schedule_items = []
        
        # Get all applicable tasks
        task_priorities = cls.get_recommended_tasks(home)
        
        # Distribute tasks across the year
        for task, priority in task_priorities:
            # Calculate next due date
            next_due = cls.generate_next_due_date(task, home, today)
            
            # Don't schedule more than 1 year out
            if (next_due - today).days <= 365:
                schedule_items.append((task, next_due, priority))
        
        # Sort by date
        schedule_items.sort(key=lambda x: x[1])
        
        return schedule_items
