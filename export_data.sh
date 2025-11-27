#!/usr/bin/env bash
# Export all database data to fixtures

echo "Exporting database to fixtures..."

# Export all data in order (respecting foreign key dependencies)
python manage.py dumpdata accounts.User --indent 2 > fixtures/users.json
python manage.py dumpdata homes.Home --indent 2 > fixtures/homes.json
python manage.py dumpdata homes.Appliance --indent 2 > fixtures/appliances.json
python manage.py dumpdata homes.ServiceProvider --indent 2 > fixtures/service_providers.json
python manage.py dumpdata maintenance.MaintenanceTask --indent 2 > fixtures/maintenance_tasks.json
python manage.py dumpdata maintenance.Schedule --indent 2 > fixtures/schedules.json
python manage.py dumpdata maintenance.ScheduleTaskCustomization --indent 2 > fixtures/schedule_customizations.json
python manage.py dumpdata maintenance.ScheduleTaskCompletion --indent 2 > fixtures/task_completions.json
python manage.py dumpdata tips.LocalTip --indent 2 > fixtures/tips.json

echo "✅ Data exported to fixtures/ directory"
echo "To load on production:"
echo "  python manage.py loaddata fixtures/users.json"
echo "  python manage.py loaddata fixtures/homes.json"
echo "  python manage.py loaddata fixtures/appliances.json"
echo "  python manage.py loaddata fixtures/service_providers.json"
echo "  python manage.py loaddata fixtures/maintenance_tasks.json"
echo "  python manage.py loaddata fixtures/schedules.json"
echo "  python manage.py loaddata fixtures/schedule_customizations.json"
echo "  python manage.py loaddata fixtures/task_completions.json"
echo "  python manage.py loaddata fixtures/tips.json"
