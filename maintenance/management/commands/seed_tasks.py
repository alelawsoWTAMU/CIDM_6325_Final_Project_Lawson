"""
Management command to seed the database with sample maintenance tasks.
Demonstrates Chapter 17 - Command Your App from Matt Layman's book.
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from maintenance.models import MaintenanceTask


class Command(BaseCommand):
    help = 'Seeds the database with sample maintenance tasks'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing tasks before seeding',
        )
    
    def handle(self, *args, **options):
        if options['clear']:
            count = MaintenanceTask.objects.all().count()
            MaintenanceTask.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Deleted {count} existing tasks'))
        
        tasks_data = [
            {
                'title': 'Change HVAC Filter',
                'category': 'hvac',
                'description': 'Replace your HVAC air filter to maintain efficiency and air quality.',
                'frequency': 'monthly',
                'difficulty': 'beginner',
                'estimated_time': 15,
                'tools_required': 'New filter (check size), Screwdriver (sometimes)',
                'step_by_step': '''1. Turn off HVAC system
2. Locate the air filter (usually near the return air duct or furnace)
3. Note the size printed on the old filter
4. Remove the old filter
5. Insert new filter (check arrow direction for airflow)
6. Turn system back on
7. Mark your calendar for next month''',
                'safety_notes': 'Turn off the system before replacing the filter.',
                'requires_hvac': True,
            },
            {
                'title': 'Clean Gutters',
                'category': 'exterior',
                'description': 'Remove leaves and debris from gutters to prevent water damage.',
                'frequency': 'biannual',
                'difficulty': 'intermediate',
                'estimated_time': 120,
                'tools_required': 'Ladder, Work gloves, Garden hose, Bucket or tarp, Safety goggles',
                'step_by_step': '''1. Set up ladder safely on level ground
2. Wear gloves and safety goggles
3. Scoop out leaves and debris by hand
4. Place debris in bucket or drop onto tarp below
5. Flush gutters with garden hose
6. Check downspouts are clear
7. Inspect for damage or leaks''',
                'safety_notes': 'Use a sturdy ladder and have someone spot you. Never lean too far to the side.',
                'applies_to_old_homes': True,
                'applies_to_new_homes': True,
            },
            {
                'title': 'Test Smoke and Carbon Monoxide Detectors',
                'category': 'safety',
                'description': 'Ensure all safety detectors are functioning properly.',
                'frequency': 'monthly',
                'difficulty': 'beginner',
                'estimated_time': 10,
                'tools_required': 'Step stool or ladder, Replacement batteries (if needed)',
                'step_by_step': '''1. Press the test button on each detector
2. Listen for the alarm sound
3. Replace batteries if needed (usually 9V)
4. Replace any detectors older than 10 years
5. Keep a log of test dates''',
                'safety_notes': 'Never disable a detector. Replace batteries immediately if low.',
            },
            {
                'title': 'Inspect and Clean Dryer Vent',
                'category': 'appliances',
                'description': 'Prevent fire hazards by keeping dryer vents clean.',
                'frequency': 'quarterly',
                'difficulty': 'intermediate',
                'estimated_time': 45,
                'tools_required': 'Dryer vent brush or vacuum attachment, Screwdriver',
                'step_by_step': '''1. Unplug the dryer
2. Pull dryer away from wall
3. Disconnect vent hose from dryer
4. Use brush or vacuum to clean lint from hose
5. Clean exterior vent opening
6. Reconnect and test''',
                'safety_notes': 'Lint buildup is a fire hazard. Do not operate dryer with damaged vent.',
            },
            {
                'title': 'Test Garage Door Safety Features',
                'category': 'exterior',
                'description': 'Ensure garage door auto-reverse is functioning to prevent injuries.',
                'frequency': 'monthly',
                'difficulty': 'beginner',
                'estimated_time': 10,
                'tools_required': '2x4 board or similar object',
                'step_by_step': '''1. Open garage door fully
2. Place board flat on ground in door's path
3. Press button to close door
4. Door should reverse when it contacts board
5. If it doesn't reverse, adjust sensitivity or call professional''',
                'safety_notes': 'Never place yourself under a moving garage door during testing.',
            },
            {
                'title': 'Flush Water Heater',
                'category': 'plumbing',
                'description': 'Remove sediment buildup to extend water heater life and efficiency.',
                'frequency': 'annual',
                'difficulty': 'intermediate',
                'estimated_time': 60,
                'tools_required': 'Garden hose, Bucket, Work gloves',
                'step_by_step': '''1. Turn off power/gas to water heater
2. Turn off cold water supply
3. Let water cool for several hours
4. Connect hose to drain valve
5. Open drain valve and pressure relief valve
6. Drain until water runs clear
7. Close valves and refill tank
8. Turn power back on''',
                'safety_notes': 'Water will be hot. Allow adequate cooling time. Turn off power before draining.',
            },
            {
                'title': 'Inspect Roof for Damage',
                'category': 'exterior',
                'description': 'Check for missing shingles, leaks, or damage from weather.',
                'frequency': 'biannual',
                'difficulty': 'advanced',
                'estimated_time': 90,
                'tools_required': 'Binoculars (for ground inspection), Ladder, Camera',
                'step_by_step': '''1. Inspect from ground with binoculars first
2. Look for missing, cracked, or curled shingles
3. Check flashing around chimneys and vents
4. Inspect attic for water stains or daylight
5. Take photos of any damage
6. Call professional if repairs needed''',
                'safety_notes': 'Roof work is dangerous. Consider hiring a professional for close inspection.',
            },
            {
                'title': 'Seal Windows and Doors',
                'category': 'interior',
                'description': 'Improve energy efficiency by sealing air leaks.',
                'frequency': 'annual',
                'difficulty': 'beginner',
                'estimated_time': 120,
                'tools_required': 'Caulk gun, Weatherstripping, Foam sealant',
                'step_by_step': '''1. Inspect all windows and doors for drafts
2. Clean surfaces to be sealed
3. Apply new caulk to gaps around window frames
4. Install or replace weatherstripping on doors
5. Use foam sealant for larger gaps
6. Check for improvement with candle/incense smoke test''',
                'safety_notes': 'Work in well-ventilated area when using sealants.',
            },
            {
                'title': 'Clean Range Hood Filter',
                'category': 'appliances',
                'description': 'Remove grease buildup for better ventilation and fire safety.',
                'frequency': 'quarterly',
                'difficulty': 'beginner',
                'estimated_time': 30,
                'tools_required': 'Dish soap, Degreaser, Hot water, Scrub brush',
                'step_by_step': '''1. Remove filter from range hood
2. Soak in hot soapy water for 10 minutes
3. Apply degreaser if needed
4. Scrub with brush
5. Rinse thoroughly
6. Dry completely before reinstalling''',
                'safety_notes': 'Ensure filter is completely dry before reinstalling to prevent electrical issues.',
            },
            {
                'title': 'Test Sump Pump',
                'category': 'plumbing',
                'description': 'Ensure sump pump is working to prevent basement flooding.',
                'frequency': 'quarterly',
                'difficulty': 'beginner',
                'estimated_time': 15,
                'tools_required': 'Bucket of water',
                'step_by_step': '''1. Locate sump pump in basement
2. Pour bucket of water into sump pit
3. Watch for pump to activate automatically
4. Verify water is pumped out
5. Listen for unusual noises
6. Check outlet pipe for blockages''',
                'safety_notes': 'Never touch pump while it is running. Keep area around pump clear.',
                'requires_basement': True,
            },
            {
                'title': 'Winterize Outdoor Faucets',
                'category': 'seasonal',
                'description': 'Prevent frozen pipe damage by winterizing outdoor faucets.',
                'frequency': 'annual',
                'difficulty': 'intermediate',
                'estimated_time': 30,
                'tools_required': 'Faucet covers, Wrench',
                'step_by_step': '''1. Shut off water supply to outdoor faucets
2. Open outdoor faucets to drain remaining water
3. Leave faucets open during winter
4. Install insulated faucet covers
5. Drain and store garden hoses
6. Consider installing frost-free faucets''',
                'safety_notes': 'Complete before first hard freeze to prevent pipe bursts.',
            },
            {
                'title': 'Clean Refrigerator Coils',
                'category': 'appliances',
                'description': 'Improve efficiency and extend appliance life by cleaning coils.',
                'frequency': 'biannual',
                'difficulty': 'beginner',
                'estimated_time': 30,
                'tools_required': 'Vacuum with brush attachment, Coil brush, Screwdriver',
                'step_by_step': '''1. Unplug refrigerator
2. Pull refrigerator away from wall (if needed)
3. Locate coils (back or bottom)
4. Remove any cover panel
5. Vacuum dust and debris from coils
6. Use coil brush for stubborn buildup
7. Replace panel and plug back in''',
                'safety_notes': 'Always unplug before cleaning. Be gentle with coils to avoid damage.',
            },
        ]
        
        created_count = 0
        for task_data in tasks_data:
            slug = slugify(task_data['title'])
            task, created = MaintenanceTask.objects.get_or_create(
                slug=slug,
                defaults=task_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created task: {task.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Task already exists: {task.title}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully seeded {created_count} maintenance tasks!')
        )
