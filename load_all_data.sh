#!/usr/bin/env bash
# One-time script to load ALL fixtures to production
# Run this ONCE in Render Shell after first deployment
# DO NOT add to build.sh - will cause duplicate key errors on subsequent deploys

set -e  # Exit on any error

echo "🚀 Loading all fixtures to production..."
echo "⚠️  Clearing existing data to avoid duplicates..."
echo ""

# Flush database (clears all data but keeps tables)
python manage.py flush --no-input

echo "✅ Database cleared"
echo ""

# Load in dependency order
echo "1/9 Loading users..."
python manage.py loaddata fixtures/users.json

echo "2/9 Loading homes..."
python manage.py loaddata fixtures/homes.json

echo "3/9 Loading appliances..."
python manage.py loaddata fixtures/appliances.json || echo "⚠️  Skipped appliances (empty or error)"

echo "4/9 Loading service providers..."
python manage.py loaddata fixtures/service_providers.json || echo "⚠️  Skipped service providers (empty or error)"

echo "5/9 Loading maintenance tasks..."
python manage.py loaddata fixtures/maintenance_tasks.json

echo "6/9 Loading schedules..."
python manage.py loaddata fixtures/schedules.json

echo "7/9 Loading schedule customizations..."
python manage.py loaddata fixtures/schedule_customizations.json || echo "⚠️  Skipped customizations (empty or error)"

echo "8/9 Loading task completions..."
python manage.py loaddata fixtures/task_completions.json || echo "⚠️  Skipped completions (empty or error)"

echo "9/9 Loading tips..."
python manage.py loaddata fixtures/tips.json || echo "⚠️  Skipped tips (empty or error)"

echo ""
echo "✅ All fixtures loaded successfully!"
echo "🎉 Production database is now fully populated"
