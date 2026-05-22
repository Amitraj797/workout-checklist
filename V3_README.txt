===============================================================
V3 WORKOUT TRACKER - COMPLETE INTERACTIVE HTML
===============================================================

FILE LOCATION:
/Users/amitraj/Desktop/Test/v3.html

FILE SIZE: 6.1 MB (includes 76 embedded animated GIF images)

HOW TO USE:
1. Open v3.html in any modern web browser (Chrome, Firefox, Safari, Edge)
2. The page will auto-expand today's workout day
3. Click any day header to expand/collapse
4. Check off exercises and sets as you complete them
5. All data saves automatically to browser localStorage

===============================================================
WORKOUT PLAN STRUCTURE
===============================================================

MONDAY - Push A (Chest Strength Focus)
  • 5 exercises + 1 superset (4A + 4B)
  • Focus: Heavy chest pressing, triceps, side delts
  • Color: Blue (#1e3c78)

TUESDAY - Legs + Shoulders A
  • 9 exercises (legs, shoulders, calves, abs)
  • Focus: Leg press, curls, extensions, shoulder press
  • Color: Green (#1a6b3a)

WEDNESDAY - Pull A (Back Width + Biceps)
  • 6 exercises
  • Focus: Lat pulldown, rows, face pulls, curls
  • Color: Purple (#7c3aed)

THURSDAY - Active Recovery
  • No lifting
  • 7-item mobility routine with stretching
  • Color: Orange (#b45309)

FRIDAY - Push B (Chest Hypertrophy Focus)
  • 6 exercises + 1 superset (5A + 5B)
  • Focus: Machine pressing, pec deck, triceps
  • Color: Pink (#be185d)

SATURDAY - Legs + Pull B
  • 10 exercises (RDLs, hip thrusts, rows, curls, abs)
  • Focus: Hamstrings, glutes, back, biceps
  • Color: Teal (#0f766e)

SUNDAY - Full Rest
  • Recovery checklist
  • No training
  • Color: Gray (#64748b)

===============================================================
FEATURES
===============================================================

EXERCISE TRACKING:
  ✓ Per-set checkboxes with completion tracking
  ✓ Weight / Reps / RIR input fields per set
  ✓ "Add Set" button to dynamically add more sets
  ✓ Set order enforcement (must complete Set 1 before Set 2)
  ✓ Progress bar showing completion percentage per day

IMAGES:
  ✓ Animated GIF exercise demonstrations
  ✓ Click any image to view fullscreen
  ✓ Primary and alternate exercise images
  ✓ Warm-up and stretching GIF thumbnails

TIMER:
  ✓ Floating rest timer with audio beep when done
  ✓ Auto-starts after completing a set
  ✓ Pause/Resume/Close controls
  ✓ Visual countdown with color changes (warning at 5s)

PROGRESSIVE OVERLOAD:
  ✓ Week and cycle tracking (3-week cycles)
  ✓ Target reps displayed per cycle week
  ✓ Previous cycle data shown for comparison
  ✓ Automatic cycle archiving

TECHNIQUE TAGS:
  ✓ RIR (Reps In Reserve) per set
  ✓ DROP (drop set on last set)
  ✓ FAILURE (go to failure on last set)
  ✓ SUPERSET (paired exercises)

EXPORT & RESET:
  ✓ Export This Week CSV - current week's data
  ✓ Export All History CSV - full cycle history
  ✓ Export Weekly Log CSV - archived workout logs
  ✓ Reset Day - clears one day (archives first)
  ✓ Reset Week - clears all days (archives first)

BREATHING CUES:
  ✓ Inhale/exhale instructions on every exercise
  ✓ Breathing hints on warm-ups and stretches

===============================================================
DATA STORAGE
===============================================================

All data is stored in browser localStorage with "workout-v3-" prefix:
  • workout-v3-checklist - checkbox states
  • workout-v3-overload - current week weight/reps/RIR
  • workout-v3-overload-history - previous cycles
  • workout-v3-weekly-log - archived workout logs
  • workout-v3-week-start - start date of week 1
  • workout-v3-last-archived-cycle - tracking variable

Data persists between browser sessions but is local to the browser.
No cloud sync - backup by exporting CSVs regularly.

===============================================================
KEYBOARD & INTERACTION
===============================================================

  • Click day header → Expand/collapse day
  • Click exercise image → View fullscreen
  • Click checkbox → Mark set complete (auto-starts timer)
  • Click "Add Set" → Add another set to exercise
  • Click anywhere on fullscreen image → Close modal
  • Enter weight/reps/RIR → Auto-saves to localStorage

===============================================================
TECHNICAL NOTES
===============================================================

  • Single self-contained HTML file (no external dependencies)
  • Works offline once loaded
  • 76 images embedded as base64 data URIs
  • 2,214 lines of HTML, CSS, and JavaScript
  • Compatible with all modern browsers
  • Mobile responsive (optimized for phone/tablet)
  • No server or database required

===============================================================
WORKOUT PHILOSOPHY (FROM PLAN)
===============================================================

SPLIT: Push/Pull/Legs with chest emphasis
FREQUENCY: 6 days/week, 1 rest day
INTENSITY: Progressive overload with 3-week cycles
TECHNIQUES: Drop sets, failure sets, supersets on isolation
REST: 45-120 seconds depending on exercise
CARDIO: 15-20 min post-workout (optional on active recovery)

===============================================================
GENERATED BY
===============================================================

Script: /Users/amitraj/Desktop/Test/generate_v3_html.py
Date: May 16, 2026
Images from: /Users/amitraj/Desktop/Test/exercise_images/

To regenerate, run:
  python3 generate_v3_html.py

===============================================================
