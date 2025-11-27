"""
Management command to seed default step-by-step instructions for maintenance tasks.
These instructions are editable by admins in the Django admin interface.
Users can override these with custom instructions per-schedule.
"""

from django.core.management.base import BaseCommand
from maintenance.models import MaintenanceTask


class Command(BaseCommand):
    help = 'Seed default step-by-step instructions for all maintenance tasks'

    def handle(self, *args, **options):
        # Instructions dictionary: task_slug -> instructions_text
        INSTRUCTIONS = {
            'appliance-coil-cleaning': """1. Safety - Unplug appliance and allow coils to cool completely
2. Locate Coils - Find condenser/evaporator coils (usually back or bottom of unit)
3. Remove Access Panel - Use screwdriver to remove protective cover
4. Vacuum Loose Debris - Use soft brush attachment to remove dust
5. Apply Coil Cleaner - Spray commercial coil cleaner (follow product directions)
6. Let Sit - Allow cleaner to penetrate (typically 5-10 minutes)
7. Rinse Carefully - Use spray bottle or low-pressure rinse
8. Dry Completely - Allow 30+ minutes to air dry
9. Reassemble - Replace access panels and secure fasteners
10. Test - Plug in and verify normal operation""",

            'electrical-panel-inspection': """1. CAUTION - Do not touch bare wires or bus bars. Call electrician if unsure.
2. Visual Exterior Check - Look for rust, damage, or moisture on panel cover
3. Open Panel Door - Remove cover screws carefully
4. Check for Issues:
   - Burn marks or discoloration
   - Loose or frayed wires
   - Tripped breakers
   - Corrosion on connections
5. Test GFCI/AFCI Breakers - Press test button (should trip)
6. Check Labels - Ensure all circuits are properly labeled
7. Verify Amperage - Check main breaker matches service rating
8. Document Issues - Take photos of any concerns
9. Close Panel - Replace cover securely
10. Professional Help - Contact licensed electrician for any repairs""",

            'generator-exercise-service': """1. Read Manual - Review manufacturer's maintenance schedule
2. Pre-Start Check:
   - Oil level (add if low using correct grade)
   - Air filter condition
   - Fuel level and lines
   - Battery voltage
3. Exercise Run - Start and run for 15-20 minutes under load monthly
4. Monitor During Run:
   - Engine sound (listen for knocking or irregular running)
   - Exhaust color (black smoke indicates problems)
   - Voltage output with multimeter
   - Transfer switch operation if installed
5. Oil Change - Follow manufacturer intervals (typically 50-100 hours)
6. Spark Plug - Inspect and replace annually or per manual
7. Fuel System:
   - Add stabilizer if rarely used
   - Check for leaks
   - Drain old fuel if sitting over 6 months
8. Battery - Clean terminals, check voltage, charge if needed
9. Cooling System - Check coolant level (liquid-cooled models)
10. Log Maintenance - Record run time, oil changes, issues""",

            'solar-inverter-check': """1. Safety - Do not touch DC connections or open inverter while sun is out
2. Visual Inspection - Check for error lights or warnings on display
3. Read Display:
   - Current power output (watts)
   - Daily/total energy production (kWh)
   - Any fault codes
4. Check Inverter Temperature - Should be warm but not excessively hot
5. Inspect Connections:
   - Look for loose wiring
   - Check for corrosion or damage
   - Do NOT touch live DC connections
6. Verify Ventilation - Ensure air vents are clear of dust/obstructions
7. Charge Controller (if separate):
   - Check battery voltage
   - Verify charging amps
   - Look for error indicators
8. Clean Exterior - Wipe down with dry cloth (power off if needed)
9. Check Monitoring App - Verify remote monitoring is functioning
10. Document - Log output levels and any issues for trend analysis""",

            'solar-panel-cleaning': """1. Safety First:
   - Work on cool, overcast day (panels get hot)
   - Use proper ladder safety
   - Wear non-slip shoes
2. Turn Off System - Switch off inverter before cleaning
3. Initial Rinse - Use garden hose to remove loose debris
4. Prepare Cleaning Solution:
   - Mix mild soap with water
   - Do NOT use abrasive cleaners or harsh chemicals
5. Soft Wash:
   - Use soft sponge or squeegee
   - Work in sections from top to bottom
   - Avoid excessive pressure
6. Rinse Thoroughly - Remove all soap residue
7. Dry if Needed - Use soft microfiber cloth for streak-free finish
8. Inspect While Cleaning:
   - Look for cracks in glass
   - Check mounting hardware
   - Note any shading from tree growth
9. Turn System Back On
10. Monitor - Check production increase after cleaning""",

            'air-filter-inspection': """1. Locate Filter - Check return air vent or furnace compartment
2. Turn Off HVAC - Switch thermostat to OFF
3. Remove Filter - Slide out or unclip from housing
4. Inspect Condition:
   - Hold to light (should see through clean filter)
   - Check for tears or damage
   - Look for dust thickness
5. Measure Filter - Note size printed on frame (e.g., 16x20x1)
6. Check MERV Rating - Higher number = better filtration (8-13 for residential)
7. Decide Action:
   - Disposable: Replace if dust buildup visible
   - Washable: Clean monthly, replace yearly
8. Clean Washable Filter:
   - Vacuum first
   - Rinse with water spray (opposite direction of airflow arrow)
   - Dry completely (24 hours)
9. Install Properly - Arrow points toward furnace/air handler
10. Set Reminder - Check again in 30 days""",

'battery-maintenance-storage': """1. Identify Battery Type - Different care for lead-acid vs lithium vs alkaline
2. For Rechargeable Batteries:
   - Charge to 40-50% before long-term storage
   - Do not store fully charged or fully depleted
3. Lead-Acid Battery Storage:
   - Keep fully charged when storing
   - Charge every 3-6 months if not in use
   - Store in cool, dry location
4. Lithium Battery Storage:
   - Charge to 40-60%
   - Store in cool place (not freezing)
   - Check and recharge every 6 months
5. Clean Terminals:
   - Remove corrosion with baking soda solution
   - Apply terminal protector spray
6. Check Voltage - Use multimeter to verify charge state
7. Storage Environment:
   - Temperature: 40-70°F ideal
   - Low humidity
   - Away from metal objects
8. Label and Date - Mark last charge date
9. Rotate Stock - Use oldest batteries first
10. Disposal - Recycle old batteries properly (never trash)""",

            'belt-hose-inspection': """1. Engine Cool - Wait for engine to cool completely
2. Visual Inspection of Belts:
   - Look for cracks, glazing, or fraying
   - Check for oil/fluid contamination
3. Belt Tension Check:
   - Press belt with thumb (should deflect 1/2 inch)
   - Too loose: slipping and squealing
   - Too tight: bearing wear
4. Look for Misalignment - Belts should track center of pulleys
5. Inspect Hoses:
   - Squeeze to check for softness or brittleness
   - Look for bulges, cracks, or leaks
   - Check clamp tightness
6. Check Hose Connections - Look for seepage or stains at connections
7. Cooling System Hoses:
   - Upper/lower radiator hoses
   - Heater hoses
   - Bypass hoses
8. Other Hoses:
   - Power steering
   - Fuel lines
   - Vacuum lines
9. Document Issues - Note any hoses/belts near failure
10. Professional Service - Replace belts/hoses showing wear""",

            'fuel-stabilization': """1. Determine Storage Duration - Fuel degrades in 30-90 days
2. Choose Stabilizer - Select appropriate type for fuel (gas/diesel)
3. Calculate Amount - Follow label directions (typically 1 oz per 2-3 gallons)
4. Add to Nearly Full Tank - Prevents condensation
5. Run Engine - 10-15 minutes to circulate stabilized fuel through system
6. For Long Storage (6+ months):
   - Fill tank completely to prevent condensation
   - Add double dose of stabilizer
7. For Equipment Storage:
   - Option A: Add stabilizer and fill tank
   - Option B: Drain tank and carburetor completely
8. Label Tank - Note date and stabilizer added
9. Fuel Rotation - Use oldest fuel first
10. Check Before Use - Drain old fuel (1+ year) before using equipment""",

            'garden-tool-maintenance': """1. Clean All Tools:
   - Remove dirt and plant debris
   - Wash with soapy water
   - Dry completely
2. Remove Rust - Use wire brush or steel wool on any rust spots
3. Sharpen Cutting Tools:
   - Pruning shears: file at 20-degree angle
   - Shovels/hoes: file beveled edge
   - Saw blades: professional sharpening recommended
4. Oil Moving Parts:
   - Apply 3-in-1 oil to hinges
   - Work mechanisms open and closed
5. Tighten Fasteners - Check and tighten all screws, bolts, nuts
6. Sand Wooden Handles:
   - Remove splinters with sandpaper
   - Apply linseed oil for protection
7. Protect Metal Surfaces:
   - Wipe with oily rag to prevent rust
   - Store tools dry
8. Check for Damage:
   - Cracked handles
   - Bent tines
   - Loose heads
9. Organize Storage - Hang tools to prevent damage
10. Seasonal Prep - Deep clean and sharpen before spring/fall""",

            'grease-fittings-service': """1. Identify Fittings - Locate all grease fittings (zerk fittings) on equipment
2. Clean Fittings - Wipe dirt away with rag before greasing
3. Select Grease - Use manufacturer-recommended grease type
4. Load Grease Gun - Fill with appropriate grease
5. Attach to Fitting - Press coupler firmly onto zerk fitting
6. Pump Grease - Apply 2-3 pumps or until grease appears at seal
7. Watch for Overflow - Stop when you see fresh grease emerge
8. Wipe Excess - Clean off any excess grease
9. Check All Points:
   - Wheel bearings
   - Pivot points
   - Universal joints
   - Steering linkages
10. Log Service - Record date and locations serviced""",

            'implement-cleaning': """1. Safety First - Engage parking brake, turn off engine, remove keys
2. Remove Large Debris - Use brush or scraper for caked-on material
3. Pressure Wash:
   - Work from top to bottom
   - Keep nozzle 12+ inches away
   - Avoid electrical components
4. Clean Hard-to-Reach Areas - Use brushes and scrapers
5. Inspect While Cleaning:
   - Look for damage or wear
   - Check bolts and fasteners
   - Note rust spots
6. Lubricate Cleaned Parts - Apply oil to prevent rust
7. Check Blades/Tines - Sharpen or replace if damaged
8. Dry Thoroughly - Wipe down to prevent rust
9. Touch Up Paint - Address bare metal spots
10. Store Properly - Cover or store indoors if possible""",

            'mower-blade-sharpening': """1. Safety - Disconnect spark plug wire and drain fuel
2. Tilt Mower - Position carburetor side up (not air filter side)
3. Block Blade - Use wood block to prevent rotation
4. Remove Blade - Use socket wrench (mark top side with paint)
5. Clean Blade - Remove grass buildup and debris
6. Inspect for Damage - Check for cracks, bends, or excessive wear
7. Sharpen:
   - Use angle grinder or file at 30-45 degree angle
   - Follow original bevel
   - Maintain even edge on both sides
8. Balance Check:
   - Hang blade on nail through center hole
   - Should balance horizontally
   - File heavier side if needed
9. Reinstall Blade - Tighten bolt securely
10. Reconnect - Reattach spark plug wire""",

            'tire-pressure-check': """1. Check When Cold - Measure before driving (heat increases pressure)
2. Locate Recommended PSI - Check door jamb sticker or owner's manual
3. Remove Valve Cap - Keep in safe place
4. Use Pressure Gauge - Press firmly onto valve stem
5. Read Pressure - Note current PSI
6. Compare to Spec - Check against recommended pressure
7. Add Air if Low:
   - Use air compressor
   - Check frequently while filling
   - Don't overinflate
8. Release Air if High - Press valve stem center briefly
9. Recheck - Verify correct pressure
10. Replace Cap - Protect valve from dirt
11. Inspect Tires:
    - Look for cuts, bulges, or wear
    - Check tread depth
    - Note any damage""",

            'tractor-oil-filter-change': """1. Warm Up Engine - Run for 5 minutes to thin oil
2. Safety - Park on level ground, engage brake, turn off engine
3. Locate Drain Plug - Check owner's manual for location
4. Position Drain Pan - Place under drain plug
5. Remove Drain Plug - Allow oil to drain completely (10-15 minutes)
6. Remove Old Filter:
   - Use filter wrench if needed
   - Let filter drain into pan
7. Prep New Filter:
   - Apply thin layer of oil to gasket
   - Fill filter halfway with new oil
8. Install New Filter - Hand tighten until gasket contacts, then 3/4 turn more
9. Replace Drain Plug - Tighten securely with washer
10. Add New Oil - Pour recommended amount and type
11. Check Level - Use dipstick to verify
12. Run Engine - Check for leaks around filter and plug
13. Dispose - Take old oil and filter to recycling center""",

            'barn-outbuilding-inspection': """1. Exterior Inspection:
   - Check foundation for cracks or settling
   - Inspect siding for rot, damage, or gaps
   - Look for signs of pest entry
2. Roof Check:
   - Look for missing or damaged shingles/metal
   - Check for sagging or structural issues
   - Inspect flashing around chimneys and vents
3. Gutters and Drainage:
   - Clear debris from gutters
   - Verify downspouts drain away from foundation
4. Doors and Windows:
   - Check operation and alignment
   - Inspect seals and weatherstripping
   - Lubricate hinges
5. Interior Inspection:
   - Look for water stains or leaks
   - Check for signs of pests or rodents
   - Inspect electrical wiring condition
6. Structural Elements:
   - Check beams and posts for rot or damage
   - Inspect floor joists if accessible
   - Look for any sagging or shifting
7. Ventilation - Ensure vents are clear and functional
8. Document Issues - Take photos and notes
9. Plan Repairs - Prioritize safety and structural concerns
10. Schedule Maintenance - Address issues before they worsen""",

            'cold-frame-greenhouse-repair': """1. Structural Inspection:
   - Check frame for rot, rust, or damage
   - Inspect joints and connections
   - Look for loose or missing fasteners
2. Glazing Check:
   - Inspect glass/plastic for cracks
   - Check seals and caulking
   - Replace broken panes
3. Clean Glazing:
   - Wash inside and out with mild soap
   - Remove algae and buildup
   - Rinse thoroughly
4. Door/Vent Maintenance:
   - Check hinges and latches
   - Lubricate moving parts
   - Adjust alignment if needed
5. Weatherproofing:
   - Replace worn weatherstripping
   - Caulk gaps and seams
   - Check for air leaks
6. Foundation Check - Verify level and stable
7. Heating/Cooling Systems - Test if applicable
8. Sanitize Interior:
   - Clean benches and surfaces
   - Disinfect to prevent disease
9. Check Watering System - Test for leaks or clogs
10. Prepare for Season - Make repairs before planting""",

            'driveway-grading': """1. Assess Condition:
   - Identify low spots and ruts
   - Note drainage problems
   - Check for potholes
2. Clear Surface - Remove loose gravel, debris, vegetation
3. Fill Potholes:
   - Use appropriate material (gravel, asphalt patch)
   - Compact thoroughly
4. Grade to Proper Slope:
   - Crown should be higher in center
   - Slope away from buildings (2% grade)
   - Direct water to drainage areas
5. Use Proper Equipment:
   - Box blade or grader for gravel
   - Rake and tamp for small areas
6. Add Material if Needed - Spread evenly
7. Compact Surface:
   - Drive over multiple times
   - Use roller or tamper for best results
8. Create Drainage:
   - Install culverts if needed
   - Ensure water flows away
9. Edge Driveway - Define borders to prevent spreading
10. Maintenance - Regrade annually or after heavy rains""",

            'fence-line-patrol-repair': """1. Walk Entire Fence Line - Inspect all posts and wire/boards
2. Check Posts:
   - Look for rot, rust, or leaning
   - Test firmness by pushing
   - Note posts needing replacement
3. Inspect Wire Fencing:
   - Look for breaks, rust, or sagging
   - Check tension and tightness
   - Verify bottom wire isn't buried in vegetation
4. Board/Panel Fences:
   - Check for rot, cracks, or missing boards
   - Inspect fasteners (nails, screws)
   - Look for warping or splitting
5. Gates:
   - Check hinges and latches
   - Verify operation and alignment
   - Lubricate moving parts
6. Vegetation Control:
   - Clear weeds and brush from fence line
   - Trim branches touching fence
7. Make Repairs:
   - Tighten loose wire
   - Replace broken boards
   - Set leaning posts
   - Fix gates
8. Document Larger Issues - Plan for major repairs
9. Consider Upgrades - Add protection where needed
10. Schedule Next Inspection - Quarterly or seasonally""",

            'foundation-drainage-check': """1. Exterior Inspection:
   - Walk around foundation perimeter
   - Look for standing water or wet spots
   - Check for soil erosion near foundation
2. Grade Verification:
   - Ground should slope away from foundation
   - Minimum 6" drop in first 10 feet
   - Add soil if grade is incorrect
3. Gutter System:
   - Verify downspouts drain at least 5-6 feet away
   - Check for downspout extensions
   - Add splash blocks or extensions if needed
4. Foundation Drains:
   - Look for drainage tile outlets
   - Verify water is flowing (if visible)
   - Clear any blockages
5. Window Wells:
   - Check for standing water
   - Verify drain holes are clear
   - Add gravel if needed
6. Cracks and Gaps:
   - Inspect foundation for cracks
   - Check where utilities enter
   - Seal gaps with appropriate material
7. Sump Pump (if applicable):
   - Test pump operation
   - Check discharge location
8. Landscaping:
   - Keep mulch 6" from foundation
   - Trim shrubs away from house
9. Interior Signs:
   - Check basement for moisture
   - Look for water stains
   - Note musty odors
10. Document - Take photos and notes for tracking""",

            'garage-door-maintenance': """1. Visual Inspection:
   - Look for worn cables, pulleys, springs
   - Check for rust or corrosion
   - Inspect door panels for damage
2. Balance Test:
   - Disconnect opener
   - Lift door manually to waist height
   - Should stay in place (balanced)
   - If falls: springs need adjustment (call professional)
3. Lubricate Moving Parts:
   - Hinges, rollers, springs, tracks
   - Use lithium or silicone spray
   - Avoid WD-40 (attracts dirt)
4. Check Rollers:
   - Inspect for wear or chips
   - Replace if damaged
   - Ensure they roll smoothly
5. Test Auto-Reverse:
   - Place object in door path
   - Door should reverse immediately
   - Adjust sensors if needed
6. Tighten Hardware:
   - Check and tighten all bolts
   - Inspect track brackets
   - Verify roller brackets are secure
7. Weatherstripping:
   - Check bottom seal
   - Replace if cracked or torn
8. Clean Tracks - Remove debris with damp cloth
9. Test Opener:
   - Check remote batteries
   - Verify smooth operation
   - Listen for unusual noises
10. Professional Service - Schedule annual professional inspection for springs and cables""",

            'gutter-downspout-cleaning': """1. Safety Setup:
   - Use stable ladder
   - Have spotter if possible
   - Wear gloves and safety glasses
2. Remove Large Debris:
   - Scoop out leaves and sticks
   - Use gutter scoop or hands
   - Place in bucket or tarp
3. Check Downspouts:
   - Remove strainers at top
   - Look for clogs
   - Use plumber's snake if needed
4. Flush Gutters:
   - Use garden hose
   - Start at high end
   - Work toward downspouts
5. Test Flow:
   - Run water and observe
   - Check for leaks
   - Verify proper drainage
6. Inspect While Cleaning:
   - Look for rust or holes
   - Check gutter slope
   - Note loose hangers
7. Downspout Extensions:
   - Ensure attached properly
   - Verify they drain away from foundation
   - Clean extensions
8. Make Minor Repairs:
   - Tighten loose hangers
   - Apply sealant to small leaks
9. Install Gutter Guards (Optional) - Reduce future cleaning
10. Document - Note any major issues for later repair""",

            'roof-flashing-inspection': """1. Safety - Use proper ladder, harness if needed
2. Chimney Flashing:
   - Check step flashing along sides
   - Inspect counterflashing and cap
   - Look for gaps or rust
3. Vent Pipe Flashing:
   - Inspect rubber boots for cracks
   - Check sealant around base
   - Look for gaps or deterioration
4. Valley Flashing:
   - Check for damage or separation
   - Verify proper overlap
   - Look for debris accumulation
5. Skylight Flashing:
   - Inspect all four sides
   - Check for cracks in sealant
   - Look for water stains inside
6. Wall Flashing:
   - Where roof meets wall
   - Check counterflashing
   - Inspect caulking
7. Dormer Flashing - Inspect all transitions
8. Check Fasteners:
   - Look for loose or missing nails
   - Verify sealant is intact
9. Clean Debris - Remove leaves and buildup
10. Document Issues:
    - Take photos
    - Note repairs needed
    - Schedule professional service if major issues found""",

            'siding-trim-inspection': """1. Walk Perimeter - Inspect all sides of house
2. Check Siding:
   - Look for cracks, warping, or rot
   - Check for loose or missing pieces
   - Inspect caulking around windows/doors
3. Wood Siding Specific:
   - Look for peeling paint
   - Check for wood rot (use screwdriver to probe)
   - Note areas needing repainting
4. Vinyl Siding:
   - Check for cracks or holes
   - Look for fading or discoloration
   - Ensure panels are properly secured
5. Trim Boards:
   - Inspect corner boards
   - Check fascia and soffit
   - Look for rot or damage
6. Caulking:
   - Check all seams and joints
   - Inspect around penetrations
   - Recaulk gaps or cracks
7. Paint Condition:
   - Note peeling or bubbling
   - Check for mildew
   - Plan repainting if needed
8. Pest Damage:
   - Look for woodpecker holes
   - Check for insect damage
   - Note carpenter bee holes
9. Clean Mildew:
   - Use appropriate cleaner
   - Scrub affected areas
10. Document - Take photos and notes for repair planning""",

            'wood-stove-chimney-sweep': """1. SAFETY FIRST - This task requires professional service in most cases
2. Schedule Professional:
   - Hire certified chimney sweep
   - Annual cleaning recommended
   - Before heating season starts
3. Pre-Service Prep:
   - Clear area around stove
   - Cover furniture with drop cloths
   - Remove decorative items from mantle
4. What Professional Does:
   - Inspect chimney and flue
   - Remove creosote buildup
   - Check for cracks or damage
   - Inspect cap and crown
   - Test damper operation
5. DIY Maintenance (Between Professional Cleanings):
   - Remove ashes regularly
   - Check door gaskets
   - Clean glass with appropriate cleaner
   - Inspect stovepipe connections
6. Monitor for Issues:
   - Smoke backing up into room
   - Difficult to start fires
   - Excessive creosote visible
   - Strong odors when not in use
7. Safety Equipment:
   - Working smoke detectors
   - Carbon monoxide detector
   - Fire extinguisher nearby
8. Burn Proper Fuel:
   - Seasoned hardwood only
   - Never burn treated wood
   - Avoid trash or cardboard
9. Keep Records - Log cleaning dates and findings
10. Annual Inspection - Even if not used regularly""",

            'hvac-filter-replacement': """1. Turn Off System - Switch thermostat to OFF
2. Locate Filter:
   - Check return air vent
   - Look at furnace/air handler
   - May be in ceiling or wall
3. Remove Old Filter:
   - Note airflow direction arrow
   - Slide out or unclip
   - Check size printed on frame
4. Inspect Old Filter:
   - Hold to light to check dirt buildup
   - Note replacement frequency needed
5. Check Filter Size:
   - Width x Height x Depth
   - Example: 16x20x1
   - Match exactly
6. Select New Filter:
   - MERV rating (8-13 for residential)
   - Higher MERV = better filtration
   - Don't exceed system capacity
7. Install New Filter:
   - Insert with arrow pointing toward furnace
   - Ensure snug fit, no gaps
   - Secure any clips or doors
8. Turn System On - Test operation
9. Set Reminder:
   - 30 days for standard filters
   - 90 days for pleated filters
   - Check monthly in heavy-use seasons
10. Stock Spares - Keep extras on hand""",

            'hvac-professional-service': """1. Schedule Service:
   - Spring for AC
   - Fall for heating
   - Book early for best availability
2. Choose Qualified Technician:
   - Licensed and insured
   - Good reviews
   - Manufacturer-certified if applicable
3. What's Included in Service:
   - System inspection
   - Filter check/replacement
   - Coil cleaning
   - Refrigerant level check
   - Electrical connections check
   - Thermostat calibration
   - Ductwork inspection
   - Safety controls test
4. Prepare for Visit:
   - Clear access to units
   - Note any issues experienced
   - Have maintenance records available
5. During Service:
   - Ask questions
   - Request explanation of findings
   - Get recommendations in writing
6. After Service:
   - Keep service receipt
   - File warranty information
   - Note any repairs recommended
7. Address Issues Promptly - Don't delay needed repairs
8. Consider Service Plan:
   - Annual or bi-annual agreements
   - Priority scheduling
   - Discounts on repairs
9. Change Filters Between Services
10. Log Service - Track dates and work performed""",

            'window-door-weatherstripping': """1. Inspect Current Weatherstripping:
   - Check for cracks, compression, or gaps
   - Test by closing door/window and feeling for drafts
   - Use incense stick to detect air leaks
2. Measure for Replacement:
   - Measure each side separately
   - Note different types needed (top, sides, bottom)
   - Add 10% extra for mistakes
3. Select Appropriate Type:
   - V-strip (tension seal): durable, effective
   - Felt: inexpensive, less durable
   - Foam tape: easy install, moderate life
   - Door sweeps: for bottom of doors
4. Remove Old Weatherstripping:
   - Peel off adhesive types
   - Unscrew or pry out nailed strips
   - Clean surface thoroughly
5. Clean Surfaces:
   - Remove old adhesive
   - Wipe with rubbing alcohol
   - Let dry completely
6. Install New Weatherstripping:
   - Start at top, work down sides
   - Don't stretch material
   - Ensure continuous seal
   - Cut at 45-degree angles for corners
7. Install Door Sweep:
   - Adjust height to seal without dragging
   - Secure with screws
8. Test Seal:
   - Close door/window
   - Check for gaps
   - Adjust if needed
9. Interior Caulking:
   - Seal gaps between trim and wall
   - Use paintable caulk
10. Check Annually - Replace worn sections""",

            'compost-pile-turning': """1. Check Moisture:
   - Should be like wrung-out sponge
   - Add water if too dry
   - Add dry materials if too wet
2. Assess Temperature:
   - Hot center (130-150°F) is ideal
   - Cool pile needs turning
   - Use compost thermometer if available
3. Prepare Tools:
   - Pitchfork or compost aerator
   - Wheelbarrow if moving location
   - Gloves and water hose
4. Turn Pile:
   - Move outer material to center
   - Move center material to outside
   - Break up clumps
   - Mix thoroughly
5. Add Materials if Needed:
   - Green (nitrogen): grass, kitchen scraps
   - Brown (carbon): leaves, paper, straw
   - Maintain 3:1 brown to green ratio
6. Check Composition:
   - Should have variety of materials
   - Avoid meat, dairy, oils
   - Keep out diseased plants
7. Aerate:
   - Create air pockets
   - Use aerating tool if available
   - Good oxygen speeds decomposition
8. Water if Dry - Mist layers as you turn
9. Cover if Desired:
   - Tarp to retain heat
   - Cover in winter
10. Monitor:
    - Turn every 2-4 weeks
    - Check for earthy smell
    - Watch for finished compost (dark, crumbly)""",

            'cover-crop-planting': """1. Select Cover Crop:
   - Rye or wheat: winter hardiness
   - Clover: nitrogen fixing
   - Buckwheat: fast growing summer
   - Mix for multiple benefits
2. Timing:
   - Fall planting after harvest
   - Spring planting before main crop
   - 4-6 weeks before first frost
3. Prepare Soil:
   - Remove crop residue
   - Light tilling if needed
   - Level surface
4. Calculate Seed Amount:
   - Follow package rate per square foot
   - Buy 10% extra
5. Broadcast Seed:
   - Spread evenly by hand or seeder
   - Cover lightly with rake
   - Or drill seed at proper depth
6. Water if Dry - Light irrigation to germinate
7. Roll or Tamp - Ensure seed-soil contact
8. Mulch if Needed - Light straw cover in exposed areas
9. Monitor Growth:
   - Watch for germination (7-14 days)
   - Check for pests
10. Termination Planning:
    - Mow before seed heads form
    - Till under or crimp/roll
    - Allow 2-3 weeks decomposition before planting
11. Benefits Tracking:
    - Note weed suppression
    - Observe soil improvement
    - Record for future planning""",

            'fruit-tree-pruning': """1. Timing:
   - Late winter/early spring (dormant season)
   - Before buds break
   - Avoid extreme cold days
2. Gather Tools:
   - Sharp bypass pruners
   - Loppers for larger branches
   - Pruning saw
   - Disinfectant (10% bleach solution)
3. Disinfect Tools - Prevent disease spread between cuts
4. Remove Dead/Diseased Wood:
   - Cut back to healthy wood
   - Look for discoloration or cankers
5. Remove Water Sprouts:
   - Vigorous vertical shoots
   - Usually grow from base or main branches
6. Thin Crowded Branches:
   - Improve air circulation
   - Allow light penetration
   - Remove crossing branches
7. Shape Tree:
   - Maintain open center (peach) or central leader (apple)
   - Cut to outward-facing buds
   - Make clean cuts at 45-degree angle
8. Remove Suckers - Shoots growing from rootstock below graft
9. Don't Over-Prune:
   - Remove no more than 25% per year
   - Young trees: minimal pruning
10. Clean Up:
    - Remove all prunings from area
    - Dispose of diseased wood
    - Compost healthy wood""",

            'green-waste-management': """1. Separate Green Waste:
   - Grass clippings
   - Leaves and yard trimmings
   - Garden plant debris
   - Small branches
2. Composting Option:
   - Add to compost pile
   - Mix with brown materials
   - See compost-pile-turning task
3. Chipping/Shredding:
   - Use chipper for branches
   - Shred leaves for mulch
   - Create valuable material
4. Grasscycling:
   - Leave clippings on lawn
   - Return nutrients to soil
   - Reduces waste
5. Mulching:
   - Spread around plants and trees
   - 2-3 inch layer
   - Keep away from trunks
6. Municipal Collection:
   - Check local pickup schedule
   - Use designated bags or containers
   - Follow local guidelines
7. Brush Pile Management:
   - Designated area for wildlife habitat
   - Or eventual burning if permitted
8. Avoid:
   - Diseased plants in compost
   - Invasive species seeds
   - Chemically treated materials
9. Seasonal Strategy:
   - Fall leaves: compost or mulch
   - Spring cleanup: compost pile
   - Summer: grasscycle
10. Track Volume - Note patterns for planning""",

            'mulch-application': """1. Choose Mulch Type:
   - Organic: wood chips, bark, leaves, straw
   - Inorganic: gravel, stones (specific uses)
   - Consider purpose and aesthetics
2. Calculate Amount Needed:
   - Measure bed area (length × width)
   - 2-3 inches deep for most applications
   - 1 cubic yard covers ~100 sq ft at 3" deep
3. Prepare Bed:
   - Remove weeds
   - Edge bed borders
   - Water soil if dry
4. Optional Landscape Fabric:
   - For weed suppression
   - Not needed with organic mulch
5. Apply Mulch:
   - Spread evenly 2-3 inches deep
   - Keep 3-6 inches away from tree trunks
   - Keep away from building foundations
6. Around Plants:
   - Don't pile against stems
   - Create donut shape, not volcano
   - Leave breathing room
7. Slope Considerations:
   - May need thicker layer
   - Consider erosion control
8. Water After Application - Settle mulch in place
9. Edge Beds - Define clean borders
10. Maintenance:
    - Fluff annually
    - Top off as it decomposes
    - Replace every 2-3 years
11. Benefits:
    - Moisture retention
    - Weed suppression
    - Temperature regulation
    - Soil improvement""",

            'pasture-rotation': """1. Assess Current Pasture:
   - Grass height (should be 6-8 inches)
   - Plant health and diversity
   - Bare or damaged spots
2. Plan Rotation:
   - Divide pasture into sections
   - Move animals before overgrazing
   - Allow regrowth time (14-30 days)
3. Monitor Grazing Height:
   - Move animals when grass is 3-4 inches
   - Don't let them graze below 3 inches
   - Protects root system
4. Check Water Access:
   - Ensure available in new section
   - Install trough or extend system
5. Inspect Fencing:
   - Check integrity before moving animals
   - Test electric fence voltage
   - Repair any damage
6. Move Animals:
   - Use proper handling techniques
   - Count to ensure all moved
   - Observe adjustment to new area
7. Rest Previous Pasture:
   - Allow sufficient regrowth
   - Typically 2-4 weeks minimum
   - Longer in slow-growing seasons
8. Mow if Needed:
   - Cut remaining stems animals avoided
   - Promotes even regrowth
   - Control weeds
9. Monitor Soil Health:
   - Look for compaction
   - Check for erosion
   - Test soil periodically
10. Adjust Schedule:
    - Based on season and growth rate
    - More frequent moves in spring
    - Slower in summer drought""",

            'perennial-bed-maintenance': """1. Early Spring Cleanup:
   - Cut back dead foliage
   - Remove winter mulch if applied
   - Check for winter damage
2. Divide Overcrowded Plants:
   - Every 3-5 years
   - Dig up clumps
   - Separate and replant divisions
3. Add Compost:
   - 1-2 inches around plants
   - Work into top layer of soil
   - Improves nutrition and drainage
4. Mulch Application:
   - Apply 2-3 inches
   - Keep away from crowns
   - Suppress weeds and retain moisture
5. Weed Regularly:
   - Hand pull when small
   - Easier when soil is moist
   - Mulch helps prevent
6. Stake Tall Plants:
   - Install early before growth
   - Use appropriate supports
   - Tie loosely to allow movement
7. Deadhead Spent Blooms:
   - Encourages more flowers
   - Keeps beds tidy
   - Prevent unwanted seeding
8. Cut Back After Bloom:
   - Some plants benefit from trim
   - Promotes second bloom
   - Prevents disease
9. Fall Maintenance:
   - Cut back or leave for winter interest
   - Remove diseased foliage
   - Mulch tender perennials
10. Monitor for Problems:
    - Check for pests and diseases
    - Remove affected material
    - Treat if necessary""",

            'raised-bed-soil-refresh': """1. Timing:
   - Early spring before planting
   - Or fall after harvest
2. Remove Old Mulch - Compost or discard
3. Pull Weeds - Get roots to prevent regrowth
4. Test Soil:
   - pH and nutrient levels
   - Send sample to extension office
5. Add Organic Matter:
   - Compost: 1-2 inches
   - Well-rotted manure
   - Mix into top 6-8 inches
6. Amendments Based on Test:
   - Lime to raise pH
   - Sulfur to lower pH
   - Specific nutrients as needed
7. Check Soil Level:
   - Should be 2-3 inches from top
   - Add fresh soil mix if needed
8. Mix Thoroughly:
   - Turn with shovel or fork
   - Blend new with existing
   - Break up clumps
9. Water Lightly - Settle new materials
10. Apply Fresh Mulch:
    - 2-3 inches after planting
    - Straw, leaves, or wood chips
11. Crop Rotation:
    - Plan different plant families
    - Prevents disease and pest buildup
    - Balances nutrient use""",

            'seed-inventory-storage': """1. Collect All Seeds:
   - Purchased packets
   - Saved seeds
   - Sort by type
2. Check Viability:
   - Look at dates
   - Test germination if old
   - Discard non-viable seeds
3. Organize:
   - By vegetable/flower type
   - Alphabetically
   - By planting season
4. Label Clearly:
   - Variety name
   - Purchase/harvest date
   - Special notes
5. Storage Containers:
   - Airtight containers
   - Glass jars or plastic boxes
   - Envelopes within containers
6. Add Desiccant:
   - Silica gel packets
   - Keeps seeds dry
   - Replace if saturated
7. Storage Location:
   - Cool, dark, dry place
   - Consistent temperature
   - Basement or refrigerator
8. Create Inventory List:
   - Spreadsheet or notebook
   - Quantities available
   - Update after using
9. Germination Testing:
   - Place seeds on damp paper towel
   - Count sprouts after 7-10 days
   - Calculate percentage
10. Plan Purchases:
    - Review inventory before ordering
    - Note what's needed
    - Avoid duplicates""",

            'soil-testing': """1. When to Test:
   - Every 2-3 years
   - Fall or early spring
   - Before starting new garden
2. Identify Test Areas:
   - Separate samples for different areas
   - Lawn separate from garden
   - Problem areas separate
3. Gather Tools:
   - Clean bucket or bag
   - Trowel or soil probe
   - Labels
4. Collect Sample:
   - Take 10-15 cores from area
   - Depth: 6 inches for gardens, 3 for lawns
   - Mix together thoroughly
5. Remove Debris:
   - Stones, roots, grass
   - Break up clumps
6. Dry Sample:
   - Spread on newspaper
   - Air dry (don't heat)
   - Usually 24 hours
7. Package for Lab:
   - Follow lab instructions
   - Usually 1-2 cups needed
   - Label with location
8. Submit to Lab:
   - Extension office
   - Private lab
   - Include information form
9. Interpret Results:
   - pH level
   - Nutrient levels (N, P, K)
   - Organic matter content
   - Recommendations provided
10. Act on Results:
    - Apply recommended amendments
    - Adjust pH if needed
    - Plan fertilization program""",

            'composting-toilet-maintenance': """1. SAFETY - Wear gloves and follow manufacturer guidelines
2. Check Ventilation:
   - Verify fan operation
   - Clear any blockages
   - Ensure proper airflow
3. Monitor Moisture:
   - Should not be too wet or dry
   - Add bulking agent if too wet
   - Add water if too dry
4. Add Bulking Material:
   - Sawdust, coconut coir, or peat moss
   - After each use or as needed
   - Maintains proper carbon balance
5. Rotate/Turn Contents:
   - If composting chamber design
   - Mix to aerate
   - Promotes decomposition
6. Check Temperature:
   - Should feel warm to touch
   - Indicates active composting
7. Empty Solids Chamber:
   - Follow manufacturer schedule
   - Typically 2-6 months
   - Let compost cure per guidelines
8. Empty Liquids Container:
   - More frequently than solids
   - Dilute and use as fertilizer
   - Or dispose per local regulations
9. Clean Seat and Surfaces:
   - Use mild, eco-friendly cleaner
   - Wipe down regularly
10. Inspect Seals:
    - Check gaskets
    - Ensure no odor leaks
    - Replace if damaged""",

            'leak-fixture-check': """1. Under Sinks:
   - Check pipes and connections
   - Look for water stains
   - Feel for dampness
   - Inspect cabinet bottom
2. Toilets:
   - Listen for running water
   - Add food coloring to tank
   - Check bowl for color (indicates leak)
   - Inspect base for water
3. Faucets:
   - Check for drips
   - Inspect under-sink connections
   - Look for corrosion
4. Water Heater:
   - Check temperature/pressure valve
   - Inspect tank base for moisture
   - Look for rust or corrosion
5. Washing Machine:
   - Check hose connections
   - Inspect hoses for cracks
   - Look at floor around machine
6. Dishwasher:
   - Check door seal
   - Inspect floor around unit
   - Look under sink for leaks at connection
7. Exposed Pipes:
   - Basement/crawl space pipes
   - Check joints and valves
   - Feel for moisture
8. Water Meter Test:
   - Turn off all water use
   - Check meter
   - Wait 1-2 hours
   - Check again (movement indicates leak)
9. Document Issues:
   - Take photos
   - Note location and severity
10. Repair or Call Plumber - Address leaks promptly""",

            'septic-system-pumping': """1. Schedule Professional Service:
   - Every 3-5 years typical
   - More often if needed
   - Licensed septic service company
2. Locate Tank and Access:
   - Find tank location
   - Uncover access lids
   - May need to dig to expose
3. Before Service:
   - Locate system diagram
   - Note any recent problems
   - Avoid driving over septic field
4. During Pumping:
   - Professional will inspect tank
   - Pump all solids and liquids
   - Check baffles and filters
   - Inspect for cracks or damage
5. Ask Questions:
   - Condition of system
   - Recommendations
   - When to pump again
6. Get Written Report:
   - Date of service
   - Findings
   - Recommendations
7. Regular Maintenance:
   - Don't flush non-biodegradables
   - Limit garbage disposal use
   - Conserve water
   - Don't use harsh chemicals
8. Inspect Drain Field:
   - No standing water
   - No soggy areas
   - Grass not overly green
9. Records:
   - Keep pumping records
   - Track system age
   - Note any repairs
10. Warning Signs Between Pumpings:
    - Slow drains
    - Odors
    - Sewage backup
    - Wet areas in yard""",

            'sump-pump-test': """1. Safety - Unplug pump before inspection
2. Inspect Pump:
   - Check for debris
   - Look for rust or damage
   - Verify intact power cord
3. Check Float Switch:
   - Lift manually
   - Should move freely
   - Not stuck or tangled
4. Reconnect Power
5. Pour Water Test:
   - Pour 5 gallons water into pit
   - Float should rise
   - Pump should activate
   - Water should discharge
6. Listen for Noises:
   - Grinding or rattling indicates problem
   - Should run smoothly
7. Check Discharge Line:
   - Verify water exits away from foundation
   - At least 10-20 feet away
   - Check for freezing in winter
8. Test Check Valve:
   - Prevents backflow
   - Listen for slam when pump stops
   - Replace if defective
9. Inspect Battery Backup (if equipped):
   - Check battery charge
   - Test backup system operation
10. Clean Pit:
    - Remove debris
    - Clear inlet screen
    - Rinse pit if needed
11. Schedule:
    - Test quarterly
    - Before rainy season
    - After long dry periods""",

            'water-heater-flush': """1. Turn Off Power/Gas:
   - Electric: breaker off
   - Gas: turn to pilot
   - Wait for water to cool (2+ hours)
2. Turn Off Cold Water Supply - Valve at top of heater
3. Connect Hose:
   - Attach to drain valve at bottom
   - Run to floor drain or outside
4. Open Pressure Release Valve - At top of tank
5. Open Drain Valve - Let water flow out
6. Flush Tank:
   - Turn cold water on briefly
   - Stirs up sediment
   - Repeat until water runs clear
7. Close Drain Valve - When done flushing
8. Fill Tank:
   - Turn on cold water supply
   - Leave hot water faucet open
   - Wait for steady flow
9. Purge Air:
   - Run hot water at faucet until steady
   - Close faucet
   - Check for leaks
10. Close Pressure Release Valve
11. Restore Power/Gas:
    - Turn breaker on (electric)
    - Return gas to on position
12. Check Operation - Water should heat in 30-60 minutes
13. Schedule - Flush annually to extend life""",

            'fire-extinguisher-check': """1. Visual Inspection:
   - Check pressure gauge (needle in green)
   - Look for physical damage
   - Verify pin and seal intact
2. Accessibility:
   - Not blocked by items
   - Easily visible
   - Within reach
3. Proper Mounting:
   - Hung on bracket
   - Height appropriate (3-5 feet)
   - Secure and stable
4. Inspection Tag:
   - Check last professional inspection date
   - Should be annually
   - Update as needed
5. Shake Extinguisher - Prevents settling of agent
6. Check Hose and Nozzle:
   - Not cracked or clogged
   - Moves freely
7. Verify Type for Location:
   - Kitchen: Class K or ABC
   - Garage/workshop: ABC
   - Electrical areas: Class C or ABC
8. Know How to Use - PASS method:
   - Pull pin
   - Aim at base of fire
   - Squeeze handle
   - Sweep side to side
9. Schedule Professional Service:
   - Annual inspection required
   - Recharge after use
   - Replace after 5-15 years
10. Document Check:
    - Date inspected
    - Any issues found
    - Action taken""",

            'radon-testing': """1. Purchase Test Kit:
   - Short-term (2-7 days)
   - Long-term (90+ days preferred)
   - Available at hardware stores
   - Or hire professional
2. Test Timing:
   - Fall/winter typically shows highest levels
   - Keep windows/doors closed 12 hours before
   - Avoid high humidity days
3. Select Location:
   - Lowest lived-in level
   - Not basement if unused
   - Typical living areas
4. Placement:
   - 20 inches from floor
   - Away from walls, windows, doors
   - No drafts or high humidity areas
5. Follow Instructions Exactly:
   - Exposure time critical
   - Don't move detector
   - Note start/end times
6. Maintain Closed-House Conditions:
   - Normal entry/exit only
   - Don't air out house
   - Close windows/doors
7. Send to Lab:
   - Follow kit instructions
   - Include all information
   - Keep copy of paperwork
8. Interpret Results:
   - 4 pCi/L or higher: action recommended
   - 2-4 pCi/L: consider remediation
   - Below 2: acceptable
9. If High Levels:
   - Retest to confirm
   - Hire mitigation specialist
   - Install venting system
10. Retest Every 2 Years - Or after renovations""",

            'rodent-pest-proofing': """1. Exterior Inspection:
   - Walk perimeter of home
   - Look for entry points
   - Check foundation, walls, roof
2. Seal Gaps:
   - Fill holes 1/4 inch or larger
   - Use steel wool and caulk
   - Cover larger openings with metal mesh
3. Foundation Cracks:
   - Fill with concrete or mortar
   - Check basement walls
4. Doors and Windows:
   - Install or replace weatherstripping
   - Add door sweeps
   - Repair damaged screens
5. Utility Entry Points:
   - Seal around pipes, wires, cables
   - Use expanding foam or caulk
   - Add metal collars if needed
6. Vents:
   - Cover with 1/4-inch mesh screen
   - Check attic, crawl space, and dryer vents
   - Ensure screens intact
7. Roof and Soffits:
   - Repair damaged areas
   - Check where pipes exit
   - Inspect roof vents
8. Garage Doors:
   - Install threshold seal
   - Check sides for gaps
9. Remove Attractants:
   - Store food in sealed containers
   - Keep trash in sealed bins
   - Clean up fallen fruit/birdseed
   - Remove clutter and nesting material
10. Vegetation Management:
    - Trim branches away from house
    - Keep shrubs 3 feet from foundation
    - Remove debris piles""",

            'cistern-cleaning': """1. Schedule Service:
   - Every 3-5 years
   - Before water quality degrades
   - Professional recommended
2. Empty Cistern:
   - Pump out water
   - Save for irrigation if possible
3. Safety First:
   - CONFINED SPACE - Professional required
   - Proper ventilation essential
   - Never enter alone
4. Inspect Before Cleaning:
   - Check for cracks
   - Look for algae growth
   - Note sediment accumulation
5. Scrub Interior:
   - Use stiff brush
   - Non-toxic cleaner
   - Reach all surfaces
6. Remove Sediment:
   - Pump or shovel out
   - Dispose properly
7. Rinse Thoroughly:
   - Multiple rinses
   - Pump out rinse water
   - Until water runs clear
8. Disinfect:
   - Use chlorine solution (follow EPA guidelines)
   - Let sit for 24 hours
   - Typically 1/4 cup bleach per 5 gallons capacity
9. Final Rinse:
   - Pump out chlorinated water
   - Refill and drain again
   - Test for chlorine residual
10. Inspect and Test:
    - Check screens and filters
    - Test water quality
    - Make any needed repairs
11. Refill - From clean source""",

            'irrigation-winterization': """1. Timing - Before first hard freeze (when temps reach 25°F)
2. Turn Off Water Supply - Locate and close main valve to system
3. Drain Method Depends on System:
   - Manual drain: open valves at low points
   - Auto drain: should drain automatically
   - Blow-out: requires air compressor
4. Blow-Out Method (Most Effective):
   - HIRE PROFESSIONAL recommended
   - Requires proper air compressor (80-100 PSI)
   - Can damage system if done incorrectly
5. If DIY Blow-Out:
   - Connect compressor to system
   - Close backflow preventer
   - Open each zone valve individually
   - Run compressed air until mist (not water) appears
   - Don't exceed 80 PSI for poly pipe, 50 PSI for PVC
6. Drain Backflow Preventer:
   - Open test cocks
   - Remove caps
   - Drain all water
7. Insulate Above-Ground Components:
   - Wrap backflow preventer
   - Insulate valve boxes
   - Use foam insulation
8. Controller Adjustment:
   - Turn off but keep power
   - Or switch to "rain" mode
   - Saves programming
9. Drain Pumps:
   - If well-supplied system
   - Follow manufacturer instructions
10. Document - Note any issues for spring startup""",

            'well-water-testing': """1. Test Frequency:
   - Annual minimum
   - After repairs or flooding
   - If taste/odor/color changes
   - If anyone becomes ill
2. Select Tests:
   - Basic: bacteria, nitrates, pH
   - Optional: arsenic, lead, pesticides
   - Consult local extension office
3. Find Lab:
   - State-certified lab
   - Local health department may provide
   - Get sterile sample bottles
4. Collection Instructions:
   - Follow lab directions exactly
   - Timing is critical
   - Usually specific faucet type
5. Bacterial Test Collection:
   - Remove aerator from faucet
   - Disinfect faucet with bleach
   - Let water run 2-3 minutes
   - Fill sterile bottle (don't touch inside)
   - Cap immediately
6. Chemical Test Collection:
   - Often no disinfection needed
   - Let water run until cold
   - Fill bottles as directed
7. Keep Sample Cold - Ice in cooler for transport
8. Deliver Promptly:
   - Within 6 hours for bacteria
   - Follow lab timing requirements
9. Interpret Results:
   - Lab will provide report
   - Compare to EPA standards
   - Note any exceedances
10. Take Action if Needed:
    - Coliform bacteria: disinfect well
    - High nitrates: investigate source
    - Other issues: consult well professional
11. Keep Records - Track results over time"""
        }

        updated_count = 0
        skipped_count = 0
        notfound_count = 0
        
        for slug, instructions in INSTRUCTIONS.items():
            try:
                task = MaintenanceTask.objects.get(slug=slug)
                
                # Only update if currently empty
                if not task.step_by_step or len(task.step_by_step.strip()) == 0:
                    task.step_by_step = instructions.strip()
                    task.save()
                    updated_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Updated: {task.title}')
                    )
                else:
                    skipped_count += 1
                    self.stdout.write(
                        self.style.WARNING(f'- Skipped (has existing): {task.title}')
                    )
                    
            except MaintenanceTask.DoesNotExist:
                notfound_count += 1
                self.stdout.write(
                    self.style.ERROR(f'✗ Task not found: {slug}')
                )
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS(f'\nSummary:'))
        self.stdout.write(f'  Updated: {updated_count} tasks')
        self.stdout.write(f'  Skipped: {skipped_count} tasks (already had instructions)')
        self.stdout.write(f'  Not Found: {notfound_count} tasks')
        self.stdout.write('\n✓ These instructions can be edited by admins in the Django admin')
        self.stdout.write('✓ Users can override with custom instructions per schedule\n')
