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
        
        Priority Tiers:
        - 90-100: Critical safety and system failures
        - 70-89: Important preventive maintenance
        - 50-69: Regular upkeep and seasonal tasks
        - 30-49: Optional improvements and long-term maintenance
        """
        # Start with frequency-based priority
        frequency_scores = {
            'weekly': 40,      # High frequency = lower base priority
            'monthly': 50,
            'quarterly': 60,
            'biannual': 70,
            'annual': 75,
            'biennial': 60,
            'as_needed': 50,
        }
        score = frequency_scores.get(task.frequency, 50)
        
        # Safety tasks get highest priority
        if task.category == 'safety':
            score += 30  # Safety is critical
        
        # Essential systems get high priority
        elif task.category in ['hvac', 'plumbing', 'electrical']:
            score += 20
        
        # Structural and exterior protection
        elif task.category in ['exterior']:
            score += 15
        
        # Equipment and yard maintenance
        elif task.category in ['yard', 'appliances']:
            score += 5
        
        # Seasonal bonus (prioritize current season tasks)
        current_season = cls.get_current_season()
        if task.seasonal_priority == current_season:
            score += 15  # Reduced from 20
        elif task.seasonal_priority == 'any':
            score += 3   # Reduced from 5
        
        # Home age relevance (older homes need more attention)
        home_age = home.get_age()
        if home_age > 50 and task.applies_to_old_homes:
            score += 8  # Significant age
        elif home_age > 20 and task.applies_to_old_homes:
            score += 5
        elif home_age <= 20 and task.applies_to_new_homes:
            score += 3
        
        # Overdue tasks (massive priority boost)
        overdue_schedules = Schedule.objects.filter(
            home=home,
            tasks=task,
            scheduled_date__lt=date.today(),
            is_completed=False
        )
        if overdue_schedules.exists():
            score += 40  # Critical - already overdue!
        
        # Never completed tasks get small boost
        completion_count = TaskCompletion.objects.filter(
            schedule__home=home,
            schedule__tasks=task
        ).count()
        if completion_count == 0:
            score += 5  # Reduced from 15
        
        # Harsh climate increases priority slightly
        climate_factor = cls.get_climate_adjustment_factor(home)
        if climate_factor > 1.2:
            score += 5  # Reduced from 10
        
        return min(score, 100)  # Cap at 100
    
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
            
            # Basic feature requirements
            if task.requires_basement and not home.has_basement:
                continue
            if task.requires_attic and not home.has_attic:
                continue
            if task.requires_hvac and not home.has_hvac:
                continue
            if task.requires_septic and not home.has_septic:
                continue
            
            # Filter tasks based on home systems and features
            # Energy systems
            if 'solar' in task.title.lower() or 'solar' in task.description.lower():
                if not home.has_solar_panels:
                    continue
            if 'generator' in task.title.lower() or 'generator' in task.description.lower():
                if not home.has_generator:
                    continue
            if 'battery bank' in task.title.lower() or 'battery bank' in task.description.lower():
                if not home.has_battery_bank:
                    continue
            if 'wood stove' in task.title.lower() or 'chimney' in task.title.lower():
                if not home.has_wood_stove:
                    continue
            
            # Water systems
            if 'sump pump' in task.title.lower():
                if not home.has_sump_pump:
                    continue
            if 'composting toilet' in task.title.lower():
                if not home.has_composting_toilet:
                    continue
            if 'rainwater' in task.title.lower() or 'cistern' in task.title.lower():
                if not home.has_rainwater_collection:
                    continue
            if 'irrigation' in task.title.lower() and 'winteriz' in task.title.lower():
                if not home.has_irrigation_system:
                    continue
            
            # Property features
            if 'fence' in task.title.lower() or 'fencing' in task.title.lower():
                if not home.has_fencing:
                    continue
            if 'barn' in task.title.lower() or 'outbuilding' in task.title.lower():
                if not home.has_barn_outbuilding:
                    continue
            if 'greenhouse' in task.title.lower() or 'cold frame' in task.title.lower():
                if not home.has_greenhouse:
                    continue
            if 'fruit tree' in task.title.lower() or 'orchard' in task.title.lower():
                if not home.has_fruit_trees:
                    continue
            if 'garden' in task.title.lower() or 'raised bed' in task.title.lower() or 'compost' in task.title.lower():
                if not home.has_garden_beds:
                    continue
            if 'pasture' in task.title.lower():
                if not home.has_pasture:
                    continue
            if 'driveway' in task.title.lower() and 'gravel' in task.description.lower():
                if home.driveway_type != 'gravel':
                    continue
            
            # Equipment
            if 'tractor' in task.title.lower():
                if not home.has_tractor:
                    continue
            if 'mower' in task.title.lower() and 'blade' in task.title.lower():
                if not home.has_riding_mower:
                    continue
            if 'chainsaw' in task.title.lower():
                if not home.has_chainsaw:
                    continue
            if 'implement' in task.title.lower() or 'plow' in task.title.lower() or 'disc' in task.title.lower():
                if not home.has_farm_implements:
                    continue
            
            # If task passed all filters, it's applicable
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
    def get_optimal_month_for_task(cls, task, start_date=None):
        """
        Determine the optimal month(s) to schedule a task based on seasonal priority.
        Returns: list of preferred month numbers (1-12)
        """
        if start_date is None:
            start_date = date.today()
        
        # Map seasons to month numbers
        season_months = {
            'spring': [3, 4, 5],
            'summer': [6, 7, 8],
            'fall': [9, 10, 11],
            'winter': [12, 1, 2],
            'any': list(range(1, 13)),  # All months
        }
        
        preferred_months = season_months.get(task.seasonal_priority, list(range(1, 13)))
        
        # Filter to future months only (from start_date onwards)
        current_month = start_date.month
        current_year = start_date.year
        
        # Build list of (year, month) tuples for next 12 months
        future_months = []
        for i in range(12):
            month = (current_month + i - 1) % 12 + 1
            year = current_year + (current_month + i - 1) // 12
            if month in preferred_months:
                future_months.append((year, month))
        
        return future_months
    
    @classmethod
    def distribute_tasks_by_frequency(cls, tasks, home, start_date=None):
        """
        Intelligently distribute tasks across 12 months based on frequency and season.
        Returns: dict mapping task to list of scheduled dates
        """
        if start_date is None:
            start_date = date.today()
        
        task_schedule = {}
        
        for task, priority in tasks:
            dates = []
            
            # Get preferred months for this task
            preferred_months = cls.get_optimal_month_for_task(task, start_date)
            
            if task.frequency == 'weekly':
                # Schedule weekly: pick first preferred month, then every 7 days
                if preferred_months:
                    year, month = preferred_months[0]
                    first_date = date(year, month, 1)
                    for week in range(52):
                        scheduled_date = first_date + timedelta(weeks=week)
                        if (scheduled_date - start_date).days <= 365:
                            dates.append(scheduled_date)
                
            elif task.frequency == 'monthly':
                # Schedule monthly: one date per month, preferring seasonal months
                for i in range(12):
                    month = (start_date.month + i - 1) % 12 + 1
                    year = start_date.year + (start_date.month + i - 1) // 12
                    
                    # Use 1st of each month
                    scheduled_date = date(year, month, 1)
                    
                    # Boost priority if in preferred season
                    if (year, month) in preferred_months:
                        dates.append(scheduled_date)
                    elif task.seasonal_priority == 'any':
                        dates.append(scheduled_date)
                
            elif task.frequency == 'quarterly':
                # Schedule quarterly: 4 times per year in appropriate seasons
                if preferred_months:
                    # Pick 4 evenly spaced months from preferred months
                    selected_months = preferred_months[:4] if len(preferred_months) >= 4 else preferred_months
                    for year, month in selected_months:
                        scheduled_date = date(year, month, 15)  # Mid-month
                        dates.append(scheduled_date)
                else:
                    # Fallback: every 3 months starting from start_date
                    for i in range(4):
                        scheduled_date = start_date + timedelta(days=i * 90)
                        dates.append(scheduled_date)
                
            elif task.frequency == 'biannual':
                # Schedule biannual: 2 times per year in appropriate seasons
                if preferred_months and len(preferred_months) >= 2:
                    # Pick first and middle of preferred months
                    year1, month1 = preferred_months[0]
                    year2, month2 = preferred_months[len(preferred_months) // 2]
                    dates.append(date(year1, month1, 15))
                    dates.append(date(year2, month2, 15))
                else:
                    # Fallback: 6 months apart
                    dates.append(start_date + timedelta(days=30))
                    dates.append(start_date + timedelta(days=210))
                
            elif task.frequency == 'annual':
                # Schedule annual: once in the best season
                # Spread tasks evenly across the preferred season to avoid bunching
                if preferred_months:
                    # Use task ID to deterministically select a month within the season
                    # This ensures consistent scheduling and even distribution
                    month_index = task.id % len(preferred_months)
                    year, month = preferred_months[month_index]
                    
                    # Also vary the day within the month (1st, 8th, 15th, 22nd)
                    day = 1 + ((task.id // len(preferred_months)) % 4) * 7
                    scheduled_date = date(year, month, min(day, 28))  # Cap at 28 for safety
                    dates.append(scheduled_date)
                else:
                    # Fallback: 30 days from start
                    dates.append(start_date + timedelta(days=30))
                
            elif task.frequency == 'biennial':
                # Schedule biennial: once every 2 years
                if preferred_months:
                    year, month = preferred_months[0]
                    scheduled_date = date(year, month, 15)
                    dates.append(scheduled_date)
                else:
                    dates.append(start_date + timedelta(days=60))
            
            else:  # as_needed
                # Schedule as_needed: once in appropriate season
                if preferred_months:
                    year, month = preferred_months[0]
                    scheduled_date = date(year, month, 15)
                    dates.append(scheduled_date)
                else:
                    dates.append(start_date + timedelta(days=45))
            
            # Store all dates for this task
            task_schedule[task] = dates
        
        return task_schedule
    
    @classmethod
    def generate_annual_schedule(cls, home):
        """
        Generate a full year of scheduled tasks, intelligently distributed across months.
        Uses frequency and seasonal priority for smart date assignment.
        Returns: list of (task, scheduled_date, priority) tuples
        """
        today = date.today()
        schedule_items = []
        
        # Get all applicable tasks with priorities
        task_priorities = cls.get_recommended_tasks(home)
        
        # Distribute tasks intelligently across the year
        task_schedule = cls.distribute_tasks_by_frequency(task_priorities, home, today)
        
        # Flatten into schedule items
        for task, dates in task_schedule.items():
            # Find priority for this task
            priority = next((p for t, p in task_priorities if t.id == task.id), 50)
            
            for scheduled_date in dates:
                # Only include dates within next 365 days
                if (scheduled_date - today).days <= 365 and scheduled_date >= today:
                    schedule_items.append((task, scheduled_date, priority))
        
        # Sort by date
        schedule_items.sort(key=lambda x: x[1])
        
        return schedule_items
