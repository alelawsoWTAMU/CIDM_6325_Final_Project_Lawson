import json
from datetime import datetime

# Load existing tips
with open('fixtures/tips.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get highest PK
max_pk = max(item['pk'] for item in data)

# Blog posts to add
blog_posts = [
    {
        'pk': max_pk + 1,
        'model': 'tips.localtip',
        'fields': {
            'post_type': 'blog',
            'author': 8,  # PlumbingPro
            'title': 'Understanding Your Home Plumbing System',
            'slug': 'understanding-your-home-plumbing-system',
            'category': 'plumbing',
            'content': '<h2>How Your Plumbing System Works</h2>\n<p>Your home plumbing consists of two main systems: supply (bringing fresh water in) and drainage (removing wastewater). Understanding both helps you prevent costly repairs.</p>\n\n<h2>Common Plumbing Issues</h2>\n<ul>\n<li><strong>Dripping Faucets:</strong> Wastes 3,000 gallons/year. Usually a worn washer ($5 fix)</li>\n<li><strong>Running Toilets:</strong> Can waste 200 gallons/day. Check the flapper valve first</li>\n<li><strong>Low Water Pressure:</strong> Often caused by mineral buildup in aerators</li>\n</ul>\n\n<h2>Preventive Maintenance</h2>\n<ul>\n<li><strong>Monthly:</strong> Check for leaks under sinks</li>\n<li><strong>Quarterly:</strong> Test water pressure</li>\n<li><strong>Annually:</strong> Flush water heater to remove sediment</li>\n</ul>',
            'location': 'Expert Network',
            'climate_zone': 'all',
            'status': 'approved',
            'views': 0,
            'is_featured': False,
            'created_at': datetime.now().isoformat() + 'Z',
            'updated_at': datetime.now().isoformat() + 'Z',
            'upvotes': []
        }
    },
    {
        'pk': max_pk + 2,
        'model': 'tips.localtip',
        'fields': {
            'post_type': 'blog',
            'author': 9,  # ElectricianExpert
            'title': 'Electrical Safety for Homeowners',
            'slug': 'electrical-safety-for-homeowners',
            'category': 'electrical',
            'content': '<h2>Warning Signs of Electrical Problems</h2>\n<ul>\n<li>Flickering or dimming lights</li>\n<li>Burning smell from outlets</li>\n<li>Warm or discolored outlets</li>\n<li>Frequently tripping breakers</li>\n</ul>\n\n<h2>DIY vs Professional Work</h2>\n<h3>Safe DIY Tasks:</h3>\n<ul>\n<li>Replacing light fixtures (power off)</li>\n<li>Testing outlets with multimeter</li>\n<li>Installing GFCI outlets</li>\n</ul>\n\n<h3>Always Call an Electrician:</h3>\n<ul>\n<li>Working inside breaker panel</li>\n<li>Adding new circuits</li>\n<li>Aluminum wiring issues</li>\n<li>Generator installation</li>\n</ul>',
            'location': 'Expert Network',
            'climate_zone': 'all',
            'status': 'approved',
            'views': 0,
            'is_featured': False,
            'created_at': datetime.now().isoformat() + 'Z',
            'updated_at': datetime.now().isoformat() + 'Z',
            'upvotes': []
        }
    },
    {
        'pk': max_pk + 3,
        'model': 'tips.localtip',
        'fields': {
            'post_type': 'blog',
            'author': 10,  # RoofingSpecialist
            'title': 'Roof Maintenance: Extend Your Roof Life',
            'slug': 'roof-maintenance-extend-your-roof-life',
            'category': 'roofing',
            'content': '<h2>Seasonal Roof Inspection Checklist</h2>\n<h3>Spring:</h3>\n<ul>\n<li>Check for winter damage</li>\n<li>Inspect flashing around chimneys</li>\n<li>Look for lifted shingles</li>\n<li>Clear debris from gutters</li>\n</ul>\n\n<h3>Fall:</h3>\n<ul>\n<li>Remove leaves and branches</li>\n<li>Trim overhanging tree limbs</li>\n<li>Check roof boots and seals</li>\n<li>Ensure proper attic ventilation</li>\n</ul>\n\n<h2>Common Roof Problems</h2>\n<p><strong>Granule Loss:</strong> Excessive granules in gutters indicate aging shingles</p>\n<p><strong>Flashing Failures:</strong> Most leaks occur at flashing around chimneys and vents</p>',
            'location': 'Expert Network',
            'climate_zone': 'all',
            'status': 'approved',
            'views': 0,
            'is_featured': False,
            'created_at': datetime.now().isoformat() + 'Z',
            'updated_at': datetime.now().isoformat() + 'Z',
            'upvotes': []
        }
    },
    {
        'pk': max_pk + 4,
        'model': 'tips.localtip',
        'fields': {
            'post_type': 'blog',
            'author': 13,  # LandscapePro
            'title': 'Year-Round Landscaping Calendar',
            'slug': 'year-round-landscaping-calendar',
            'category': 'landscaping',
            'content': '<h2>Spring (March-May)</h2>\n<ul>\n<li>Remove winter debris</li>\n<li>Prune damaged branches</li>\n<li>Add fresh mulch (2-3 inches)</li>\n<li>Aerate and overseed lawn</li>\n<li>Start mower maintenance</li>\n</ul>\n\n<h2>Summer (June-August)</h2>\n<ul>\n<li>Water deeply but less frequently</li>\n<li>Deadhead flowers for continuous blooms</li>\n<li>Mow high (3-4 inches) during heat</li>\n<li>Monitor for pests</li>\n</ul>\n\n<h2>Fall (September-November)</h2>\n<ul>\n<li>Plant spring-flowering bulbs</li>\n<li>Rake leaves regularly</li>\n<li>Winterize irrigation system</li>\n<li>Apply fall fertilizer</li>\n<li>Plant trees and shrubs (best time!)</li>\n</ul>\n\n<h2>Winter (December-February)</h2>\n<ul>\n<li>Protect sensitive plants from frost</li>\n<li>Prune dormant trees</li>\n<li>Plan next year garden</li>\n<li>Service equipment</li>\n</ul>',
            'location': 'Expert Network',
            'climate_zone': 'all',
            'status': 'approved',
            'views': 0,
            'is_featured': False,
            'created_at': datetime.now().isoformat() + 'Z',
            'updated_at': datetime.now().isoformat() + 'Z',
            'upvotes': []
        }
    }
]

# Add blog posts
data.extend(blog_posts)

# Save
with open('fixtures/tips.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f'Added {len(blog_posts)} blog posts')
print(f'Total records: {len(data)}')
tips_count = len([t for t in data if t['fields']['post_type'] == 'tip'])
blogs_count = len([t for t in data if t['fields']['post_type'] == 'blog'])
print(f'Tips: {tips_count}, Blogs: {blogs_count}')
