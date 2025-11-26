"""
Management command to export all database data to fixtures.
Run this locally before deploying to backup/export your data.
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
import os


class Command(BaseCommand):
    help = 'Exports all database data to JSON fixtures'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--output-dir',
            type=str,
            default='fixtures',
            help='Directory to save fixture files',
        )
        parser.add_argument(
            '--exclude-users',
            action='store_true',
            help='Exclude user accounts from export',
        )
    
    def handle(self, *args, **options):
        output_dir = options['output_dir']
        exclude_users = options['exclude_users']
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        self.stdout.write(self.style.WARNING('📦 Exporting database to fixtures...'))
        self.stdout.write('')
        
        fixtures = []
        
        # Users and accounts
        if not exclude_users:
            fixtures.append(('auth.User', 'users.json'))
            fixtures.append(('accounts', 'accounts.json'))
        
        # Core data
        fixtures.extend([
            ('homes', 'homes.json'),
            ('maintenance.MaintenanceTask', 'maintenance_tasks.json'),
            ('maintenance.Schedule', 'schedules.json'),
            ('maintenance.TaskCompletion', 'task_completions.json'),
            ('tips', 'tips.json'),
        ])
        
        exported_count = 0
        for app_label, filename in fixtures:
            filepath = os.path.join(output_dir, filename)
            
            try:
                self.stdout.write(f'Exporting {app_label}...')
                
                # Don't use natural keys for auth.User - causes issues
                use_natural = app_label != 'auth.User'
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    if use_natural:
                        call_command(
                            'dumpdata',
                            app_label,
                            indent=2,
                            stdout=f,
                            natural_foreign=True,
                            natural_primary=True,
                        )
                    else:
                        call_command(
                            'dumpdata',
                            app_label,
                            indent=2,
                            stdout=f,
                        )
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Exported to {filepath}')
                )
                exported_count += 1
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Failed to export {app_label}: {str(e)}')
                )
        
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(f'🎉 Successfully exported {exported_count} fixture files!')
        )
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('📝 Next steps:'))
        self.stdout.write(f'   1. Commit fixtures to git: git add {output_dir}/')
        self.stdout.write('   2. Push to GitHub: git push origin Final_Project')
        self.stdout.write('   3. On Render, run: python manage.py load_all_fixtures')
