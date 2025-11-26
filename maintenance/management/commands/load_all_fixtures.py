"""
Management command to load all fixtures in the correct order.
This seeds the production database with all data from local development.
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
import os


class Command(BaseCommand):
    help = 'Loads all fixture data in the correct order'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--fixtures-dir',
            type=str,
            default='fixtures',
            help='Directory containing fixture files',
        )
    
    def handle(self, *args, **options):
        fixtures_dir = options['fixtures_dir']
        
        # Order matters - respect foreign key dependencies
        fixtures = [
            'users.json',
            'user_profiles.json',
            'expert_profiles.json',
            'homes.json',
            'maintenance_tasks.json',
            'schedules.json',
            'task_completions.json',
            'tips.json',
        ]
        
        self.stdout.write(self.style.WARNING('⚠️  This will load data into the database.'))
        self.stdout.write(self.style.WARNING('    Existing data with same IDs may be updated.'))
        self.stdout.write('')
        
        loaded_count = 0
        for fixture_file in fixtures:
            fixture_path = os.path.join(fixtures_dir, fixture_file)
            
            if not os.path.exists(fixture_path):
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Skipping {fixture_file} (not found)')
                )
                continue
            
            try:
                self.stdout.write(f'Loading {fixture_file}...')
                call_command('loaddata', fixture_path, verbosity=0)
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Loaded {fixture_file}')
                )
                loaded_count += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Failed to load {fixture_file}: {str(e)}')
                )
        
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(f'🎉 Successfully loaded {loaded_count} fixture files!')
        )
