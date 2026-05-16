#!/usr/bin/env python3
"""
Generate v3.html - Complete workout tracker with animated GIF images
Uses base64-encoded images from exercise_images/ directory
"""

import os
import base64
import json
from pathlib import Path

# Paths
BASE_DIR = Path("/Users/amitraj/Desktop/Test")
IMG_DIR = BASE_DIR / "exercise_images"
OUTPUT = BASE_DIR / "v3.html"

def image_name_to_filename(name):
    """Convert display name to image filename"""
    # Remove parentheses, replace / and spaces with underscore
    name = name.replace("(", "").replace(")", "")
    name = name.replace("/", "_").replace(" ", "_")
    return name

def find_image(name):
    """Find image file (gif or jpg) for exercise name"""
    base = image_name_to_filename(name)

    # Try .gif first (animated), then .jpg
    for ext in ['.gif', '.jpg']:
        path = IMG_DIR / f"{base}{ext}"
        if path.exists():
            return path

    # Try without trailing chars
    for ext in ['.gif', '.jpg']:
        # Try removing trailing dots/dashes
        variants = [
            base.rstrip('._-'),
            base.replace('__', '_'),
        ]
        for variant in variants:
            path = IMG_DIR / f"{variant}{ext}"
            if path.exists():
                return path

    return None

def image_to_data_uri(path):
    """Convert image to base64 data URI"""
    if not path or not path.exists():
        return ""

    with open(path, 'rb') as f:
        data = f.read()

    mime = "image/gif" if path.suffix == ".gif" else "image/jpeg"
    b64 = base64.b64encode(data).decode('ascii')
    return f"data:{mime};base64,{b64}"

def build_image_map():
    """Build mapping of exercise names to data URIs"""
    print("Building image map...")

    # List of all exercise names from v3 plan
    exercises = [
        # Monday
        "Incline Dumbbell Press", "Incline Machine Press",
        "Flat Dumbbell Press", "Chest Press Machine",
        "Cable Fly (Mid/Low-to-High)", "Cable Fly Mid_Low-to-High", "Pec Deck",
        "Rope Pushdown", "V-Bar Pushdown",
        "Overhead Rope Extension", "Single-Arm Cable Pushdown",
        "Cable Lateral Raise", "DB Lateral Raise",

        # Tuesday
        "Leg Press", "Hack Squat",
        "Seated Leg Curl", "Lying Leg Curl",
        "Leg Extension", "Walking Lunges",
        "Machine Shoulder Press", "Seated DB Press",
        "Standing Calf Raise", "Leg Press Calf Raise",
        "Seated Calf Raise", "DB Standing Calf Raise",
        "Dead Bug", "Reverse Crunch",
        "Pallof Press", "Banded Pallof Press",

        # Wednesday
        "Lat Pulldown", "Assisted Pull-Up",
        "Chest-Supported Row", "Seated Cable Row",
        "Face Pulls", "Reverse Pec Deck",
        "Incline Dumbbell Curl", "Machine Preacher Curl",
        "Hammer Curl", "Cable Hammer Curl",
        "Reverse Curl", "DB Hammer Curl",

        # Friday
        "Incline Machine Press", "Incline Dumbbell Press",
        "Chest Press Machine", "Flat Dumbbell Press",
        "DB Floor Press",
        "Pec Deck", "Cable Fly Mid_Low-to-High",
        "V-Bar Pushdown", "Rope Pushdown",
        "Overhead Cable Extension", "DB Overhead Extension",

        # Saturday
        "Romanian Deadlift (RDL)", "Cable Pull-Through",
        "Hip Thrust", "Glute Bridge",
        "Bulgarian Split Squat", "Reverse Lunge",
        "Seated Cable Row", "Machine Row",
        "Rear Delt Cable Fly", "Seated Rear Delt Raise",
        "Spider Curl", "Preacher Curl Machine",
        "Incline Dumbbell Curl", "Concentration Curl",
        "Cable Hammer Curl", "DB Cross-Body Hammer Curl",
        "Hanging Knee Raise", "Captain's Chair Knee Raise",
        "Cable Crunch", "Ab Crunch Machine",

        # Saturday extra
        "Seated Calf Raise", "DB Standing Calf Raise",

        # Warm-ups (exact names matching GIF filenames)
        "Shoulder rolls", "Band pull-aparts",
        "Wall slides (scapular activation)",
        "External rotations (light band/DB)",
        "Leg swings (front-back + side-side)", "Leg swings (front-back)",
        "Bodyweight squats", "Glute bridges",
        "Cat-cow", "Cat-cow mobility",
        "Scapular pulldown", "Band rows", "Dead hang",
        "Walking lunges (bodyweight)", "Hip mobility circles",

        # Stretches
        "Doorway chest stretch", "Overhead tricep stretch",
        "Cross-body shoulder stretch", "Child's pose stretch",
        "Seated hamstring stretch", "Standing quad stretch",
        "Kneeling hip flexor stretch", "Figure-4 glute stretch",
        "Wall calf stretch", "Kneeling lat prayer stretch",
        "Wall bicep stretch",
        "Wrist flexor/forearm stretch",
        "Open book thoracic rotations",
    ]

    img_map = {}
    for name in exercises:
        path = find_image(name)
        if path:
            uri = image_to_data_uri(path)
            img_map[name] = uri
            print(f"  ✓ {name} -> {path.name}")
        else:
            print(f"  ✗ {name} -> NOT FOUND")
            img_map[name] = ""

    return img_map

# Build image map
IMAGE_MAP = build_image_map()

def img(name):
    """Get data URI for exercise name"""
    return IMAGE_MAP.get(name, "")

# HTML generation starts here
print("\nGenerating v3.html...")

html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>6-Day Workout Plan v3 - Push/Pull/Legs Split</title>
<style>
:root {
  --primary: #1e3c78;
  --accent: #2d6cdf;
  --success: #1a8a4a;
  --warning: #c45a20;
  --danger: #c0392b;
  --bg: #f5f7fa;
  --card: #ffffff;
  --text: #1a1a2e;
  --muted: #6b7280;
  --border: #e2e8f0;
  --radius: 12px;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; padding: 0; -webkit-tap-highlight-color: transparent; }
.container { max-width: 800px; margin: 0 auto; padding: 16px; }

.cover { background: linear-gradient(135deg, #1e3c78 0%, #2d6cdf 100%); color: white; padding: 40px 20px; text-align: center; border-radius: 0 0 24px 24px; margin-bottom: 20px; }
.cover h1 { font-size: 28px; font-weight: 800; margin-bottom: 4px; }
.cover p { font-size: 14px; opacity: 0.85; }
.cover .badges { display: flex; gap: 8px; justify-content: center; margin-top: 16px; flex-wrap: wrap; }
.cover .badge { background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 20px; font-size: 12px; }

.day-section { background: var(--card); border-radius: var(--radius); margin: 16px 0; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
.day-header { padding: 16px 20px; font-size: 18px; font-weight: 700; color: white; cursor: pointer; display: flex; justify-content: space-between; align-items: center; user-select: none; -webkit-user-select: none; touch-action: manipulation; -webkit-tap-highlight-color: transparent; }
.day-header .arrow { transition: transform 0.3s; font-size: 14px; }
.day-header.collapsed .arrow { transform: rotate(-90deg); }
.day-content { padding: 0 16px 16px; overflow-x: auto; -webkit-overflow-scrolling: touch; }
.day-content.hidden { display: none; }

.day-mon .day-header { background: #1e3c78; }
.day-tue .day-header { background: #1a6b3a; }
.day-wed .day-header { background: #7c3aed; }
.day-thu .day-header { background: #b45309; }
.day-fri .day-header { background: #be185d; }
.day-sat .day-header { background: #0f766e; }
.day-sun .day-header { background: #64748b; }

.sub-header { font-size: 15px; font-weight: 700; margin: 16px 0 8px; padding: 8px 12px; border-radius: 8px; display: flex; align-items: center; gap: 8px; }
.sub-header.warmup { background: #ecfdf5; color: #065f46; }
.sub-header.muscle { background: #eff6ff; color: #1e3a8a; }
.sub-header.cardio { background: #fef2f2; color: #991b1b; }
.sub-header.cooldown { background: #f5f3ff; color: #5b21b6; }

.exercise-card { background: #f8fafc; border: 1px solid var(--border); border-radius: 10px; padding: 12px; margin: 8px 0; }
.ex-header { display: flex; align-items: flex-start; gap: 10px; }
.ex-num { background: var(--primary); color: white; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 14px; flex-shrink: 0; }
.ex-info { flex: 1; }
.ex-name { font-weight: 700; font-size: 14px; }
.ex-meta { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 4px; }
.tag { font-size: 11px; padding: 2px 8px; border-radius: 12px; font-weight: 600; }
.tag.sets { background: #d1fae5; color: #065f46; }
.tag.rest { background: #f3f4f6; color: #6b7280; }
.tag.rir { background: #fee2e2; color: #991b1b; }
.tag.technique-drop { background: #f59e0b; color: #fff; font-size: 9px; padding: 1px 6px; }
.tag.technique-failure { background: #dc2626; color: #fff; font-size: 9px; padding: 1px 6px; }
.tag.technique-superset { background: #7c3aed; color: #fff; font-size: 9px; padding: 1px 6px; }
.superset-block { border-left: 4px solid #7c3aed; background: #f5f3ff; border-radius: 10px; padding: 4px 0 4px 8px; margin: 8px 0; }
.superset-label { font-size: 10px; font-weight: 700; color: #7c3aed; padding: 4px 8px; display: inline-block; }

.ex-images { display: flex; gap: 8px; margin: 10px 0; justify-content: center; }
.ex-img-wrap { text-align: center; flex: 1; max-width: 180px; }
.ex-img-wrap img { width: 100%; height: 160px; object-fit: contain; background: #fff; border: 2px solid var(--border); border-radius: 8px; cursor: pointer; }
.ex-img-wrap.alt img { border-color: #fed7aa; }
.img-label { display: block; font-size: 10px; font-weight: 600; margin-top: 2px; color: var(--muted); }
.ex-img-wrap.alt .img-label { color: var(--warning); }

.ex-toggle { display: flex; gap: 0; margin: 8px 0 4px; border: 2px solid var(--accent); border-radius: 8px; overflow: hidden; width: fit-content; }
.toggle-btn { padding: 4px 14px; font-size: 11px; font-weight: 700; border: none; cursor: pointer; background: #fff; color: var(--accent); transition: all 0.2s; }
.toggle-btn.active { background: var(--accent); color: #fff; }
.toggle-btn:first-child { border-right: 1px solid var(--accent); }
.ex-img-wrap.dimmed img { opacity: 0.3; filter: grayscale(80%); }
.ex-alt { font-size: 12px; color: var(--warning); margin: 4px 0; }
.ex-note { font-size: 11px; color: var(--danger); font-style: italic; }

.ex-breathing { font-size: 12px; color: #0369a1; background: #f0f9ff; padding: 6px 10px; border-radius: 6px; margin: 8px 0 4px; border-left: 3px solid #0ea5e9; }
.breathing-hint { display: block; font-size: 11px; color: #0369a1; margin-top: 2px; font-style: italic; }

.set-tracker { margin: 8px 0 0; padding: 8px; background: #fff; border: 1px solid var(--border); border-radius: 8px; }
.set-rest { font-size: 11px; color: #7c3aed; padding: 2px 0 2px 30px; font-weight: 600; }
.set-tag { font-size: 9px; padding: 1px 6px; border-radius: 10px; font-weight: 700; margin-left: 4px; display: inline-block; vertical-align: middle; line-height: 16px; }
.set-tag.rir { background: #fee2e2; color: #991b1b; }
.set-tag.drop { background: #f59e0b; color: #fff; }
.set-tag.failure { background: #dc2626; color: #fff; }
.set-tag.superset { background: #7c3aed; color: #fff; }
.add-set-btn { display: flex; align-items: center; justify-content: center; gap: 4px; margin-top: 6px; padding: 6px; background: #f0fdf4; border: 1px dashed #86efac; border-radius: 8px; color: #16a34a; font-size: 12px; font-weight: 600; cursor: pointer; transition: background 0.2s; }
.add-set-btn:hover { background: #dcfce7; }
.add-set-btn svg { width: 16px; height: 16px; }

.checklist { margin: 8px 0; }
.check-item { display: flex; align-items: center; gap: 10px; padding: 8px 0; font-size: 13px; cursor: pointer; border-bottom: 1px solid #f1f5f9; -webkit-tap-highlight-color: transparent; }
.check-item:last-child { border-bottom: none; }
.check-item input[type="checkbox"] { -webkit-appearance: checkbox; appearance: checkbox; margin: 0; width: 20px; height: 20px; min-width: 20px; min-height: 20px; accent-color: var(--success); flex-shrink: 0; cursor: pointer; touch-action: manipulation; }
.check-item span { flex: 1; }
.check-item.checked span { text-decoration: line-through; color: var(--muted); }

.ref-img { width: 60px; height: 60px; object-fit: cover; border-radius: 8px; border: 2px solid var(--border); flex-shrink: 0; cursor: pointer; pointer-events: auto; }

.confirm-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 10000; justify-content: center; align-items: center; }
.confirm-modal.active { display: flex; }
.confirm-box { background: #fff; border-radius: 16px; padding: 24px; max-width: 320px; width: 90%; text-align: center; box-shadow: 0 8px 30px rgba(0,0,0,0.25); }
.confirm-box h3 { font-size: 16px; color: #c0392b; margin-bottom: 8px; }
.confirm-box p { font-size: 13px; color: #4a5568; margin-bottom: 20px; line-height: 1.5; }
.confirm-btns { display: flex; gap: 10px; justify-content: center; }
.confirm-btns button { padding: 10px 28px; border-radius: 10px; font-size: 14px; font-weight: 700; border: none; cursor: pointer; }
.confirm-yes { background: #ef4444; color: #fff; }
.confirm-yes:active { background: #dc2626; }
.confirm-no { background: #e2e8f0; color: #1a1a2e; }
.confirm-no:active { background: #cbd5e1; }
.img-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.85); z-index: 9999; justify-content: center; align-items: center; cursor: pointer; -webkit-tap-highlight-color: transparent; }
.img-modal.active { display: flex; }
.img-modal img { max-width: 98vw; max-height: 95vh; object-fit: contain; border-radius: 12px; background: #fff; padding: 10px; }

.progress-bar { width: 100%; height: 6px; background: #e2e8f0; border-radius: 3px; margin: 8px 0; overflow: hidden; }
.progress-fill { height: 100%; background: var(--success); border-radius: 3px; transition: width 0.3s; }
.progress-text { font-size: 11px; color: var(--muted); text-align: right; }

.reset-btn { background: none; border: 1px solid var(--border); color: var(--muted); font-size: 11px; padding: 4px 12px; border-radius: 6px; cursor: pointer; margin: 8px 0; }
.reset-btn:hover { background: #fef2f2; color: var(--danger); border-color: var(--danger); }

.timer-btn { display: inline-block; background: #0ea5e9; color: #fff; font-size: 11px; font-weight: 700; padding: 2px 10px; border-radius: 12px; cursor: pointer; margin-left: 6px; border: none; vertical-align: middle; line-height: 20px; }
.timer-btn:active { background: #0284c7; }
.set-rest .timer-btn { background: #7c3aed; }
.set-rest .timer-btn:active { background: #6d28d9; }

.set-inputs { display: flex; gap: 6px; margin-top: 6px; align-items: center; flex-wrap: wrap; }
.set-inputs label { font-size: 10px; color: var(--muted); font-weight: 600; display: flex; flex-direction: column; align-items: center; gap: 1px; }
.set-inputs input[type="number"] { width: 52px; padding: 4px 2px; font-size: 12px; border: 1px solid var(--border); border-radius: 6px; text-align: center; background: #fff; -moz-appearance: textfield; }
.set-inputs input[type="number"]::-webkit-inner-spin-button,
.set-inputs input[type="number"]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
.set-inputs input[type="number"]:focus { outline: 2px solid var(--accent); border-color: var(--accent); }
.set-inputs input[type="number"]::placeholder { color: #c0c7d0; font-size: 11px; }
.set-prev { font-size: 10px; color: #7c3aed; font-weight: 600; margin-left: auto; white-space: nowrap; }

.export-bar { display: flex; gap: 8px; justify-content: center; margin: 0 0 16px; flex-wrap: wrap; }
.export-btn { background: linear-gradient(135deg,#1e3c78,#2d6cdf); color: #fff; border: none; padding: 8px 18px; border-radius: 10px; font-size: 13px; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 6px; }
.export-btn:active { opacity: 0.85; }
.export-btn.secondary { background: linear-gradient(135deg,#065f46,#1a8a4a); }
.export-btn.danger { background: linear-gradient(135deg,#991b1b,#c0392b); }

.floating-timer { position: fixed; bottom: 20px; right: 20px; background: #1e293b; color: #fff; border-radius: 16px; padding: 12px 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); z-index: 9998; display: none; flex-direction: column; align-items: center; gap: 6px; min-width: 180px; }
.floating-timer.active { display: flex; }
.timer-label { font-size: 11px; color: #94a3b8; text-align: center; max-width: 160px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.timer-display { font-size: 36px; font-weight: 800; font-variant-numeric: tabular-nums; letter-spacing: 2px; }
.timer-display.warning { color: #f59e0b; }
.timer-display.done { color: #22c55e; }
.timer-controls { display: flex; gap: 8px; }
.timer-controls button { border: none; border-radius: 8px; padding: 6px 16px; font-size: 13px; font-weight: 700; cursor: pointer; }
.timer-play { background: #22c55e; color: #fff; }
.timer-play:active { background: #16a34a; }
.timer-pause { background: #f59e0b; color: #fff; }
.timer-pause:active { background: #d97706; }
.timer-stop { background: #ef4444; color: #fff; }
.timer-stop:active { background: #dc2626; }

@media (max-width: 600px) {
  .container { padding: 6px; }
  .cover { padding: 20px 12px; }
  .cover h1 { font-size: 20px; }
  .cover p { font-size: 12px; }
  .badges { gap: 4px; }
  .badge { font-size: 10px; padding: 3px 8px; }
  .day-header { font-size: 14px; padding: 12px 14px; }
  .day-content { padding: 10px; }
  .sub-header { font-size: 13px; padding: 6px 10px; }
  .exercise-card { padding: 10px; }
  .ex-name { font-size: 13px; }
  .ex-header { gap: 8px; }
  .ex-num { width: 26px; height: 26px; font-size: 12px; }
  .ex-images { flex-direction: column; align-items: center; }
  .ex-img-wrap { max-width: 90%; }
  .ex-img-wrap img { height: 200px; }
  .ex-alt { font-size: 11px; }
  .ex-note { font-size: 10px; }
  .ex-breathing { font-size: 11px; padding: 5px 8px; }
  .tag { font-size: 10px; padding: 2px 6px; }
  .check-item { padding: 10px 0; font-size: 13px; gap: 8px; }
  .check-item input[type="checkbox"] { width: 22px; height: 22px; min-width: 22px; min-height: 22px; }
  .ref-img { width: 50px; height: 50px; }
  .set-tracker { padding: 6px; }
  .set-inputs { gap: 3px; flex-wrap: wrap; }
  .set-inputs input[type="number"] { width: 44px; font-size: 11px; padding: 4px 2px; }
  .set-prev { font-size: 9px; }
  .add-set-btn { font-size: 11px; padding: 5px; }
  .superset-block { padding: 4px 0 4px 6px; }
  .superset-label { font-size: 9px; padding: 3px 6px; }

  .profile-table td { padding: 6px 8px; font-size: 12px; }
  .profile-table td:first-child { width: 35%; }
  .info-table { font-size: 11px; }
  .info-table th { padding: 6px; font-size: 11px; }
  .info-table td { padding: 6px; }
  .info-table td, .info-table th { word-break: break-word; }

  .floating-timer { bottom: 10px; right: 10px; padding: 10px 12px; min-width: 150px; border-radius: 12px; }
  .timer-display { font-size: 28px; }
  .timer-label { font-size: 10px; max-width: 130px; }
  .timer-btns button { font-size: 11px; padding: 5px 10px; }

  .confirm-box { padding: 16px; max-width: 280px; }
  .confirm-box h3 { font-size: 15px; }
  .confirm-box p { font-size: 12px; margin-bottom: 14px; }
  .confirm-btns button { padding: 8px 20px; font-size: 13px; }
  .img-modal img { max-width: 96vw; max-height: 90vh; padding: 4px; }

  .reset-btn { font-size: 12px; padding: 8px 16px; }
  .export-bar { gap: 6px; }
  .export-btn { padding: 8px 14px; font-size: 12px; }
  .set-line { gap: 6px; }
}

@media (max-width: 370px) {
  .container { padding: 4px; }
  .day-content { padding: 8px; }
  .exercise-card { padding: 8px; }
  .ex-name { font-size: 12px; }
  .tag { font-size: 9px; padding: 1px 5px; }
  .set-inputs input[type="number"] { width: 40px; font-size: 10px; }
  .info-table th, .info-table td { padding: 4px; font-size: 10px; }
  .profile-table td { padding: 5px 6px; font-size: 11px; }
  .export-btn { padding: 6px 10px; font-size: 11px; }
}

@media print {
  .day-content.hidden { display: block !important; }
  .day-header .arrow { display: none; }
  .exercise-card { break-inside: avoid; }
  .reset-btn { display: none; }
}

.profile-table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 13px; }
.profile-table td { padding: 8px 12px; border-bottom: 1px solid var(--border); }
.profile-table td:first-child { font-weight: 600; width: 40%; color: var(--muted); }
.info-table { width: 100%; border-collapse: collapse; font-size: 13px; margin: 8px 0; }
.info-table th { background: var(--primary); color: white; padding: 8px; text-align: left; font-size: 12px; }
.info-table td { padding: 8px; border-bottom: 1px solid var(--border); }
.info-table tr:nth-child(even) td { background: #f8fafc; }
.table-scroll { overflow-x: auto; -webkit-overflow-scrolling: touch; margin: 8px 0; }
</style>
</head>
<body>

<div class="cover">
  <h1>6-DAY WORKOUT PLAN <small style="font-size:14px;background:rgba(255,255,255,0.2);padding:2px 10px;border-radius:8px;">v3</small></h1>
  <p>Push/Pull/Legs Split &middot; Hypertrophy Focus &middot; Animated Exercise Guides</p>
  <div class="badges">
    <span class="badge">Progressive Overload Tracking</span>
    <span class="badge">Chest Strength + Hypertrophy</span>
    <span class="badge">Auto Rest Timer</span>
  </div>
</div>

<div class="container">

<!-- PROFILE & OVERVIEW -->
<div class="day-section">
  <div class="day-header" style="background:#374151" onclick="toggle(this)">Profile & Overview <span class="arrow">&#9660;</span></div>
  <div class="day-content">
    <table class="profile-table">
      <tr><td>Age / Sex</td><td>32 / Male</td></tr>
      <tr><td>Weight / Height</td><td>66 kg / 165 cm</td></tr>
      <tr><td>Body Fat</td><td>~27-29%</td></tr>
      <tr><td>Goal</td><td>Chest growth + Arm/forearm size + Belly fat reduction + Aesthetics</td></tr>
      <tr><td>Injuries</td><td>Tailbone discomfort (cardio), Posterior knee discomfort</td></tr>
      <tr><td>Equipment</td><td>Full Gym</td></tr>
      <tr><td>Schedule</td><td>Push/Pull/Legs — Mon-Sat training, Sunday rest</td></tr>
    </table>
  </div>
</div>

<!-- INJURY AWARENESS -->
<div class="day-section">
  <div class="day-header" style="background:#c0392b" onclick="toggle(this)">Injury Awareness & Safety Rules <span class="arrow">&#9660;</span></div>
  <div class="day-content">
    <div class="sub-header" style="background:#fef2f2;color:#991b1b">Tailbone Discomfort</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>Avoid exercises that aggravate tailbone (seated positions)</span></div>
      <div class="check-item"><input type="checkbox"><span>Change cardio modality if tailbone pain worsens (try cycling)</span></div>
      <div class="check-item"><input type="checkbox"><span>Use padding on hard seats/benches</span></div>
      <div class="check-item"><input type="checkbox"><span>Stop any exercise causing severe tailbone pain</span></div>
    </div>
    <div class="sub-header" style="background:#fef2f2;color:#991b1b">Posterior Knee Discomfort</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>Choose pain-free leg press/squat options</span></div>
      <div class="check-item"><input type="checkbox"><span>Replace Bulgarian Split Squat with leg press if knee discomfort</span></div>
      <div class="check-item"><input type="checkbox"><span>Controlled tempo on all leg exercises — no bouncing</span></div>
      <div class="check-item"><input type="checkbox"><span>If worsening knee pain — switch to pain-free variant or skip</span></div>
    </div>
  </div>
</div>

<!-- TRAINING GUIDE -->
<div class="day-section">
  <div class="day-header" style="background:#1e3a5f" onclick="toggle(this)">Training Guide — Weekly Split, Rules & Intensity <span class="arrow">&#9660;</span></div>
  <div class="day-content">
    <div class="sub-header muscle">Weekly Split</div>
    <table class="info-table">
      <tr><th>Day</th><th>Focus</th><th>Type</th><th>Time</th></tr>
      <tr><td>Monday</td><td>Push A</td><td>Chest Strength</td><td>~75 min</td></tr>
      <tr><td>Tuesday</td><td>Legs + Shoulders A</td><td>Quads + Shoulders</td><td>~75 min</td></tr>
      <tr><td>Wednesday</td><td>Pull A</td><td>Back Width + Biceps</td><td>~70 min</td></tr>
      <tr><td>Thursday</td><td>Active Recovery</td><td>Mobility/Cardio</td><td>~30 min</td></tr>
      <tr><td>Friday</td><td>Push B</td><td>Chest Hypertrophy</td><td>~75 min</td></tr>
      <tr><td>Saturday</td><td>Legs + Pull B</td><td>Posterior Chain + Arms</td><td>~80 min</td></tr>
      <tr><td>Sunday</td><td colspan="3">FULL REST</td></tr>
    </table>

    <div class="sub-header muscle">Failure Training Rules</div>
    <table class="info-table">
      <tr><th>Exercise Type</th><th>Rule</th></tr>
      <tr><td><strong>Compound lifts</strong> (Incline DB Press, Leg Press, RDL, Rows)</td><td>Stop 1-2 reps before failure. Do NOT go to failure.</td></tr>
      <tr><td><strong>Isolation lifts</strong> (Cable Fly, Pec Deck, Lateral Raise, Curls, Pushdowns)</td><td>Final set can safely go to failure.</td></tr>
    </table>

    <div class="sub-header muscle">Drop Set Rules</div>
    <table class="info-table">
      <tr><th>Use Drop Sets On (Final Set Only)</th><th>Do NOT Drop Set</th></tr>
      <tr><td>Cable Lateral Raise, Pec Deck</td><td>RDL, Leg Press</td></tr>
      <tr><td>Rope Pushdowns, Cable Curls</td><td>Heavy DB Presses</td></tr>
      <tr><td>Hammer Curls, Leg Extension</td><td>Hip Thrusts</td></tr>
    </table>

    <div class="sub-header muscle">Superset Rules</div>
    <table class="info-table">
      <tr><th>Rule</th><th>Details</th></tr>
      <tr><td>Use supersets for</td><td>Isolation exercises and time efficiency</td></tr>
      <tr><td>Avoid supersets on</td><td>Heavy compound lifts</td></tr>
    </table>

    <div class="sub-header muscle" style="margin-top:20px">Intensity Technique Guide</div>
    <table class="info-table">
      <tr><th>Element</th><th>What It Means</th></tr>
      <tr><td><span class="tag rir">RIR: 2</span></td><td>Reps In Reserve — stop 2 reps before failure</td></tr>
      <tr><td><span class="tag technique-drop">DROP</span></td><td>Drop Set — last set, reduce weight 30-40%, immediately do more reps</td></tr>
      <tr><td><span class="tag technique-failure">FAILURE</span></td><td>Go to Failure — last set, keep going until you can't with good form</td></tr>
      <tr><td><span class="tag technique-superset">SUPERSET</span></td><td>Superset — do both exercises back-to-back, no rest between them</td></tr>
    </table>

    <div class="sub-header muscle">Rep Ranges & Rest</div>
    <table class="info-table">
      <tr><th>Type</th><th>Reps</th><th>Rest</th></tr>
      <tr><td>Heavy compound movements</td><td>6-10 reps</td><td>90-120 sec</td></tr>
      <tr><td>Hypertrophy movements</td><td>10-15 reps</td><td>60-90 sec</td></tr>
      <tr><td>Isolation movements</td><td>12-15 reps</td><td>45-75 sec</td></tr>
    </table>
  </div>
</div>
'''

# Now generate each day's content
# I'll create a helper function to generate exercise cards

def exercise_card(num, name, alt, sets, reps, rest, rir, note, breathing, primary_img, alt_img, superset=False, drop=False, failure=False):
    """Generate an exercise card HTML"""

    # Parse sets to get initial count (e.g., "2-3 x 12-15" -> 2 sets, "3 x 10-12" -> 3 sets)
    set_count = int(sets.split('-')[0]) if '-' in sets else int(sets.split()[0])

    # Technique tags
    tech_tags = ""
    if drop:
        tech_tags += '<span class="tag technique-drop">DROP</span>'
    if failure:
        tech_tags += '<span class="tag technique-failure">FAILURE</span>'
    if superset:
        tech_tags += '<span class="tag technique-superset">SUPERSET</span>'

    safe_name = name.replace("'", "\\'").replace('"', '&quot;')
    safe_alt = alt.replace("'", "\\'").replace('"', '&quot;')

    html = f'''
    <div class="exercise-card" data-primary="{safe_name}" data-alt="{safe_alt}">
      <div class="ex-header"><span class="ex-num">{num}</span><div class="ex-info"><div class="ex-name">{name}</div><div class="ex-meta"><span class="tag sets">{sets} x {reps}</span><span class="tag rest">Rest: {rest}</span><span class="tag rir">RIR: {rir}</span>{tech_tags}</div></div></div>
      <div class="ex-toggle"><button class="toggle-btn active" data-choice="primary" onclick="toggleExercise(this)">Primary</button><button class="toggle-btn" data-choice="alt" onclick="toggleExercise(this)">Alternate</button></div>
      <div class="ex-images">'''

    if primary_img:
        html += f'<div class="ex-img-wrap"><img src="{primary_img}" alt="{name}" loading="lazy"><span class="img-label">Primary</span></div>'

    if alt_img:
        html += f'<div class="ex-img-wrap alt"><img src="{alt_img}" alt="{alt}" loading="lazy"><span class="img-label">Alternate</span></div>'

    html += f'''</div>
      <div class="ex-alt"><strong>Alt:</strong> {alt}</div>
      <div class="ex-note">{note}</div>
      <div class="ex-breathing">{breathing}</div>
      <div class="set-tracker">'''

    # Generate set checkboxes
    for i in range(1, set_count + 1):
        html += f'<div class="check-item"><input type="checkbox"><span>Set {i} - {reps} reps</span></div>\n'
        if i < set_count:
            html += f'<div class="set-rest">Rest {rest}</div>\n'

    html += '''</div>
    </div>
'''
    return html

# Continue generating the HTML...
# For brevity, I'll include the key structure and first day, then the pattern repeats

html_content += '''
<!-- ==================== MONDAY ==================== -->
<div class="day-section day-mon" id="day-mon">
  <div class="day-header" onclick="toggle(this)">Monday - Push A (Chest Strength Focus) <span class="arrow">&#9660;</span></div>
  <div class="day-content">

    <div class="progress-bar"><div class="progress-fill" style="width:0%"></div></div>
    <div class="progress-text">0 / 0 completed</div>

    <div class="sub-header warmup">Warm-Up (8-10 min)</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>Light treadmill walk or cycling - 5 min<br><small class="breathing-hint">Breathe naturally through nose</small></span></div>
'''

# Add warm-up images if available
if img("Shoulder rolls"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Shoulder rolls")}" alt="Shoulder rolls" loading="lazy"><span>Shoulder rolls - 10 reps<br><small class="breathing-hint">Breathe naturally on each rotation</small></span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>Shoulder rolls - 10 reps<br><small class="breathing-hint">Breathe naturally on each rotation</small></span></div>\n'

if img("Band pull-aparts"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Band pull-aparts")}" alt="Band pull-aparts" loading="lazy"><span>Band pull-aparts - 15 reps<br><small class="breathing-hint">Exhale: pull band apart | Inhale: return</small></span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>Band pull-aparts - 15 reps<br><small class="breathing-hint">Exhale: pull band apart | Inhale: return</small></span></div>\n'

if img("Wall slides (scapular activation)"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Wall slides (scapular activation)")}" alt="Wall slides" loading="lazy"><span>Wall slides (scapular activation) - 10 reps<br><small class="breathing-hint">Exhale: slide arms up | Inhale: slide down</small></span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>Wall slides (scapular activation) - 10 reps<br><small class="breathing-hint">Exhale: slide arms up | Inhale: slide down</small></span></div>\n'

if img("External rotations (light band/DB)"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("External rotations (light band/DB)")}" alt="External rotations" loading="lazy"><span>External rotations (light band/DB) - 12 reps each<br><small class="breathing-hint">Exhale: rotate outward | Inhale: return</small></span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>External rotations (light band/DB) - 12 reps each<br><small class="breathing-hint">Exhale: rotate outward | Inhale: return</small></span></div>\n'

html_content += '''    </div>

    <div class="sub-header muscle">Chest + Shoulders + Triceps (6 exercises)</div>
'''

# Monday exercises
html_content += exercise_card(
    1, "Incline Dumbbell Press", "Incline Machine Press",
    "4", "6-10", "90-120s", "1-2",
    "Priority chest movement. Controlled eccentric.",
    "Inhale: lower to upper chest | Exhale: press up",
    img("Incline Dumbbell Press"), img("Incline Machine Press")
)

html_content += exercise_card(
    2, "Flat Dumbbell Press", "Chest Press Machine",
    "3", "8-10", "90s", "1-2",
    "Controlled stretch at bottom.",
    "Inhale: lower to chest | Exhale: press up",
    img("Flat Dumbbell Press"), img("Chest Press Machine")
)

# SUPERSET - Chest + Shoulders
html_content += '''
    <div class="superset-block"><span class="superset-label">SUPERSET</span>
'''

html_content += exercise_card(
    "3A", "Cable Fly (Mid/Low-to-High)", "Pec Deck",
    "3", "12-15", "60s", "2",
    "Slow eccentric. Squeeze at peak contraction.",
    "Inhale: open arms | Exhale: squeeze together",
    img("Cable Fly Mid_Low-to-High"), img("Pec Deck"),
    superset=True
)

html_content += exercise_card(
    "3B", "Cable Lateral Raise", "DB Lateral Raise",
    "3", "12-15", "60s", "1-2",
    "Focus on side delts. Light weight, strict form.",
    "Exhale: raise arms | Inhale: lower",
    img("Cable Lateral Raise"), img("DB Lateral Raise"),
    superset=True
)

html_content += '''    </div>
'''

# SUPERSET - Triceps
html_content += '''
    <div class="superset-block"><span class="superset-label">SUPERSET</span>
'''

html_content += exercise_card(
    "4A", "Rope Pushdown", "V-Bar Pushdown",
    "3", "12-15", "60s", "1-2",
    "Elbows pinned. Full extension.",
    "Exhale: push down | Inhale: let rope rise",
    img("Rope Pushdown"), img("V-Bar Pushdown"),
    superset=True
)

html_content += exercise_card(
    "4B", "Overhead Rope Extension", "Single-Arm Cable Pushdown",
    "3", "12-15", "60s", "1-2",
    "Long head stretch. Controlled movement.",
    "Exhale: extend arms overhead | Inhale: lower behind head",
    img("Overhead Rope Extension"), img("Single-Arm Cable Pushdown"),
    superset=True
)

html_content += '''    </div>
'''

# Monday cardio and stretching
html_content += '''
    <div class="sub-header cardio">Cardio Finisher (15-20 min)</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>Incline treadmill walk or cycling - 15-20 min | HR: 120-140 BPM<br><small class="breathing-hint">Breathe steadily through nose</small></span></div>
    </div>

    <div class="sub-header cooldown">Post-Workout Stretching (5 min)</div>
    <div class="checklist">
'''

if img("Doorway chest stretch"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Doorway chest stretch")}" alt="Doorway chest stretch" loading="lazy"><span>Doorway chest stretch 30s<br><small class="breathing-hint">Inhale deeply | Exhale: lean in</small></span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>Doorway chest stretch 30s<br><small class="breathing-hint">Inhale deeply | Exhale: lean in</small></span></div>\n'

if img("Overhead tricep stretch"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Overhead tricep stretch")}" alt="Overhead tricep stretch" loading="lazy"><span>Overhead tricep stretch 30s<br><small class="breathing-hint">Exhale: pull elbow deeper</small></span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>Overhead tricep stretch 30s<br><small class="breathing-hint">Exhale: pull elbow deeper</small></span></div>\n'

if img("Cross-body shoulder stretch"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Cross-body shoulder stretch")}" alt="Cross-body shoulder stretch" loading="lazy"><span>Cross-body shoulder stretch 30s<br><small class="breathing-hint">Exhale: pull arm closer</small></span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>Cross-body shoulder stretch 30s<br><small class="breathing-hint">Exhale: pull arm closer</small></span></div>\n'

child_pose_img = img("Child's pose stretch")
if child_pose_img:
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{child_pose_img}" alt="Childs pose stretch" loading="lazy"><span>Child\'s pose stretch 45s<br><small class="breathing-hint">Exhale: sink hips deeper</small></span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>Child\'s pose stretch 45s<br><small class="breathing-hint">Exhale: sink hips deeper</small></span></div>\n'

html_content += '''    </div>
    <button class="reset-btn" onclick="resetDay(this)">Reset Day</button>
  </div>
</div>
'''

# For the sake of keeping this manageable, I'll add a simplified version of the remaining days
# In production, you'd fully generate each day following the same pattern

# Tuesday - Legs + Shoulders A
html_content += '''
<!-- ==================== TUESDAY ==================== -->
<div class="day-section day-tue" id="day-tue">
  <div class="day-header" onclick="toggle(this)">Tuesday - Legs + Shoulders A <span class="arrow">&#9660;</span></div>
  <div class="day-content">

    <div class="progress-bar"><div class="progress-fill" style="width:0%"></div></div>
    <div class="progress-text">0 / 0 completed</div>

    <div class="sub-header warmup">Warm-Up (8-10 min)</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>Cycling (easy pace) - 5 min</span></div>
'''

if img("Leg swings (front-back + side-side)"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Leg swings (front-back + side-side)")}" alt="Leg swings" loading="lazy"><span>Leg swings (front-back + side-side) - 10 each leg</span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>Leg swings (front-back + side-side) - 10 each leg</span></div>\n'

if img("Bodyweight squats"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Bodyweight squats")}" alt="Bodyweight squats" loading="lazy"><span>Bodyweight squats - 15 reps</span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>Bodyweight squats - 15 reps</span></div>\n'

if img("Glute bridges"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Glute bridges")}" alt="Glute bridges" loading="lazy"><span>Glute bridges - 15 reps</span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>Glute bridges - 15 reps</span></div>\n'

if img("Walking lunges (bodyweight)"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Walking lunges (bodyweight)")}" alt="Walking lunges" loading="lazy"><span>Walking lunges (bodyweight) - 10 each leg</span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>Walking lunges (bodyweight) - 10 each leg</span></div>\n'

if img("Cat-cow mobility"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Cat-cow mobility")}" alt="Cat-cow mobility" loading="lazy"><span>Cat-cow mobility - 10 reps</span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>Cat-cow mobility - 10 reps</span></div>\n'

html_content += '''    </div>

    <div class="sub-header muscle">Legs + Shoulders + Calves + Core (8 exercises)</div>
'''

tuesday_exercises = [
    (1, "Leg Press", "Hack Squat", "4", "8-12", "90-120s", "1-2", "Choose pain-free option for knee.",
     "Inhale: lower weight | Exhale: press up", "Leg Press", "Hack Squat", False, False, False),
    (2, "Seated Leg Curl", "Lying Leg Curl", "3", "10-12", "60s", "1-2", "Controlled tempo. Full ROM.",
     "Exhale: curl | Inhale: lower", "Seated Leg Curl", "Lying Leg Curl", False, False, False),
    (3, "Leg Extension", "Walking Lunges", "3", "12-15", "60s", "1", "Last set drop set. Squeeze at top.",
     "Exhale: extend | Inhale: lower", "Leg Extension", "Walking Lunges", False, True, False),
    (4, "Machine Shoulder Press", "Seated DB Press", "3", "8-10", "90s", "1-2", "Shoulder-safe pressing.",
     "Exhale: press up | Inhale: lower", "Machine Shoulder Press", "Seated DB Press", False, False, False),
    (5, "Standing Calf Raise", "Leg Press Calf Raise", "3", "12-15", "45s", "1-2", "Full stretch at bottom.",
     "Exhale: raise | Inhale: lower", "Standing Calf Raise", "Leg Press Calf Raise", False, False, False),
    (6, "Seated Calf Raise", "DB Standing Calf Raise", "2", "12-15", "45s", "1-2", "Targets soleus.",
     "Exhale: raise | Inhale: lower", "Seated Calf Raise", "DB Standing Calf Raise", False, False, False),
    (7, "Dead Bug", "Reverse Crunch", "2", "10 each side", "45s", "2", "Deep core activation.",
     "Exhale: extend limbs | Inhale: return", "Dead Bug", "Reverse Crunch", False, False, False),
    (8, "Pallof Press", "Banded Pallof Press", "2", "10 each side", "45s", "2", "Anti-rotation.",
     "Exhale: press out | Inhale: return", "Pallof Press", "Banded Pallof Press", False, False, False),
]

for ex in tuesday_exercises:
    html_content += exercise_card(ex[0], ex[1], ex[2], ex[3], ex[4], ex[5], ex[6], ex[7], ex[8],
                                   img(ex[9]), img(ex[10]), ex[11], ex[12], ex[13])

html_content += '''
    <div class="sub-header cardio">Cardio (5-10 min)</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>Easy cycling (or skip) - 5-10 min | Very light only. NO intense incline treadmill.</span></div>
    </div>

    <div class="sub-header cooldown">Post-Workout Stretching</div>
    <div class="checklist">
'''

stretches = [
    ("Seated hamstring stretch", "30s"),
    ("Standing quad stretch", "30s"),
    ("Kneeling hip flexor stretch", "30s"),
    ("Figure-4 glute stretch", "30s"),
    ("Wall calf stretch", "30s"),
]

for stretch_name, duration in stretches:
    if img(stretch_name):
        html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img(stretch_name)}" alt="{stretch_name}" loading="lazy"><span>{stretch_name} {duration}</span></div>\n'
    else:
        html_content += f'      <div class="check-item"><input type="checkbox"><span>{stretch_name} {duration}</span></div>\n'

html_content += '''    </div>
    <button class="reset-btn" onclick="resetDay(this)">Reset Day</button>
  </div>
</div>
'''

# Due to length constraints, I'll now add the remaining days in a more compact form
# Wednesday, Thursday, Friday, Saturday, Sunday following the same pattern...

# WEDNESDAY
html_content += '''
<!-- ==================== WEDNESDAY ==================== -->
<div class="day-section day-wed" id="day-wed">
  <div class="day-header" onclick="toggle(this)">Wednesday - Pull A (Back Width + Biceps) <span class="arrow">&#9660;</span></div>
  <div class="day-content">
    <div class="progress-bar"><div class="progress-fill" style="width:0%"></div></div>
    <div class="progress-text">0 / 0 completed</div>

    <div class="sub-header warmup">Warm-Up</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>Rowing machine or cycling - 5 min</span></div>
'''

if img("Scapular pulldown"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Scapular pulldown")}" alt="Scapular pulldown" loading="lazy"><span>Scapular pulldown - 12 reps</span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>Scapular pulldown - 12 reps</span></div>\n'

if img("Band rows"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Band rows")}" alt="Band rows" loading="lazy"><span>Band rows - 15 reps</span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>Band rows - 15 reps</span></div>\n'

if img("Cat-cow"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Cat-cow")}" alt="Cat-cow" loading="lazy"><span>Cat-cow - 10 reps</span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>Cat-cow - 10 reps</span></div>\n'

if img("Dead hang"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Dead hang")}" alt="Dead hang" loading="lazy"><span>Dead hang - 15 sec</span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>Dead hang - 15 sec</span></div>\n'

html_content += '''    </div>
    <div class="sub-header muscle">Back + Biceps (6 exercises)</div>
'''

# Back standalone exercises
wed_back = [
    (1, "Lat Pulldown", "Assisted Pull-Up", "4", "8-12", "90s", "1-2", "Squeeze shoulder blades.",
     "Exhale: pull down | Inhale: extend arms", "Lat Pulldown", "Assisted Pull-Up"),
    (2, "Chest-Supported Row", "Seated Cable Row", "3", "8-12", "90s", "1-2", "Lower-back friendly.",
     "Exhale: pull to chest | Inhale: extend", "Chest-Supported Row", "Seated Cable Row"),
]

for ex in wed_back:
    html_content += exercise_card(ex[0], ex[1], ex[2], ex[3], ex[4], ex[5], ex[6], ex[7], ex[8],
                                   img(ex[9]), img(ex[10]))

# SUPERSET 1 - Back + Biceps
html_content += '''
    <div class="superset-block"><span class="superset-label">SUPERSET</span>
'''

html_content += exercise_card(
    "3A", "Face Pulls", "Reverse Pec Deck",
    "3", "12-15", "60s", "2",
    "Pull to forehead. Posture + rear delts.",
    "Exhale: pull rope | Inhale: return",
    img("Face Pulls"), img("Reverse Pec Deck"),
    superset=True
)

html_content += exercise_card(
    "3B", "Hammer Curl", "Cable Hammer Curl",
    "3", "10-12", "60s", "1-2",
    "Forearm + brachialis focus.",
    "Exhale: curl | Inhale: lower",
    img("Hammer Curl"), img("Cable Hammer Curl"),
    superset=True
)

html_content += '''    </div>
'''

# SUPERSET 2 - Biceps
html_content += '''
    <div class="superset-block"><span class="superset-label">SUPERSET</span>
'''

html_content += exercise_card(
    "4A", "Incline Dumbbell Curl", "Machine Preacher Curl",
    "3", "10-12", "60s", "1-2",
    "Deep stretch. Light weight.",
    "Exhale: curl up | Inhale: lower",
    img("Incline Dumbbell Curl"), img("Machine Preacher Curl"),
    superset=True
)

html_content += exercise_card(
    "4B", "Reverse Curl", "DB Hammer Curl",
    "2", "12-15", "60s", "2",
    "Forearm thickness.",
    "Exhale: curl | Inhale: lower",
    img("Reverse Curl"), img("DB Hammer Curl"),
    superset=True
)

html_content += '''    </div>
'''

html_content += '''
    <div class="sub-header cardio">Cardio</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>Cycling or incline treadmill walk - 15-20 min | Moderate intensity only.</span></div>
    </div>
    <div class="sub-header cooldown">Stretching</div>
    <div class="checklist">
'''

wed_stretches = [
    ("Kneeling lat prayer stretch", "30s"),
    ("Wall bicep stretch", "30s"),
    ("Wrist flexor/forearm stretch", "20s"),
    ("Seated hamstring stretch", "30s"),
    ("Child's pose stretch", "45s"),
]

for stretch_name, duration in wed_stretches:
    if img(stretch_name):
        html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img(stretch_name)}" alt="{stretch_name}" loading="lazy"><span>{stretch_name} {duration}</span></div>\n'
    else:
        html_content += f'      <div class="check-item"><input type="checkbox"><span>{stretch_name} {duration}</span></div>\n'

html_content += '''    </div>
    <button class="reset-btn" onclick="resetDay(this)">Reset Day</button>
  </div>
</div>
'''

# THURSDAY - Active Recovery
html_content += '''
<!-- ==================== THURSDAY ==================== -->
<div class="day-section day-thu" id="day-thu">
  <div class="day-header" onclick="toggle(this)">Thursday - Active Recovery <span class="arrow">&#9660;</span></div>
  <div class="day-content">
    <div class="progress-bar"><div class="progress-fill" style="width:0%"></div></div>
    <div class="progress-text">0 / 0 completed</div>

    <div class="sub-header cooldown">Recovery Info</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>20-30 minutes easy walking OR easy cycling</span></div>
      <div class="check-item"><input type="checkbox"><span>No heavy lifting</span></div>
      <div class="check-item"><input type="checkbox"><span>Focus on recovery, mobility, and flexibility</span></div>
    </div>

    <div class="sub-header cooldown">Mobility Routine</div>
    <div class="checklist">
'''

thursday_mobility = [
    ("Seated hamstring stretch", "30 sec each side"),
    ("Kneeling hip flexor stretch", "30 sec each side"),
    ("Figure-4 glute stretch", "30 sec each side"),
    ("Wall calf stretch", "30 sec each side"),
    ("Cat-cow", "10 reps"),
    ("Child's pose stretch", "45 sec"),
    ("Open book thoracic rotations", "10 each side"),
]

for mob_name, mob_duration in thursday_mobility:
    if img(mob_name):
        html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img(mob_name)}" alt="{mob_name}" loading="lazy"><span>{mob_name} - {mob_duration}</span></div>\n'
    else:
        html_content += f'      <div class="check-item"><input type="checkbox"><span>{mob_name} - {mob_duration}</span></div>\n'

html_content += '''    </div>
    <button class="reset-btn" onclick="resetDay(this)">Reset Day</button>
  </div>
</div>
'''

# FRIDAY - Push B
html_content += '''
<!-- ==================== FRIDAY ==================== -->
<div class="day-section day-fri" id="day-fri">
  <div class="day-header" onclick="toggle(this)">Friday - Push B (Chest Hypertrophy Focus) <span class="arrow">&#9660;</span></div>
  <div class="day-content">
    <div class="progress-bar"><div class="progress-fill" style="width:0%"></div></div>
    <div class="progress-text">0 / 0 completed</div>

    <div class="sub-header warmup">Warm-Up (8-10 min)</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>Light treadmill walk or cycling - 5 min</span></div>
'''

if img("Shoulder rolls"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Shoulder rolls")}" alt="Shoulder rolls" loading="lazy"><span>Shoulder rolls - 10 reps</span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>Shoulder rolls - 10 reps</span></div>\n'

if img("Band pull-aparts"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Band pull-aparts")}" alt="Band pull-aparts" loading="lazy"><span>Band pull-aparts - 15 reps</span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>Band pull-aparts - 15 reps</span></div>\n'

if img("Wall slides (scapular activation)"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Wall slides (scapular activation)")}" alt="Wall slides" loading="lazy"><span>Wall slides (scapular activation) - 10 reps</span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>Wall slides (scapular activation) - 10 reps</span></div>\n'

if img("External rotations (light band/DB)"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("External rotations (light band/DB)")}" alt="External rotations" loading="lazy"><span>External rotations (light band/DB) - 12 reps each</span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>External rotations (light band/DB) - 12 reps each</span></div>\n'

html_content += '''    </div>

    <div class="sub-header muscle">Chest + Shoulders + Triceps (7 exercises)</div>
'''

friday_exercises = [
    (1, "Incline Machine Press", "Incline Dumbbell Press", "4", "8-12", "90s", "1-2", "Machine for stability.",
     "Exhale: press | Inhale: lower", "Incline Machine Press", "Incline Dumbbell Press", False, False, False),
    (2, "Chest Press Machine", "Flat Dumbbell Press", "3", "10-12", "60s", "2", "Mind-muscle connection.",
     "Exhale: press | Inhale: lower", "Chest Press Machine", "Flat Dumbbell Press", False, False, False),
    (3, "Flat Dumbbell Press", "DB Floor Press", "2", "8-10", "60s", "1-2", "Additional chest overload.",
     "Inhale: lower | Exhale: press", "Flat Dumbbell Press", "DB Floor Press", False, False, False),
]

for ex in friday_exercises:
    html_content += exercise_card(ex[0], ex[1], ex[2], ex[3], ex[4], ex[5], ex[6], ex[7], ex[8],
                                   img(ex[9]), img(ex[10]), ex[11], ex[12], ex[13])

html_content += '''
    <div class="superset-block"><span class="superset-label">SUPERSET</span>
'''

html_content += exercise_card(
    "4A", "Pec Deck", "Cable Fly (Mid/Low-to-High)",
    "3", "12-15", "60s", "1",
    "Controlled squeeze.",
    "Inhale: open | Exhale: squeeze",
    img("Pec Deck"), img("Cable Fly Mid_Low-to-High"),
    superset=True
)

html_content += exercise_card(
    "4B", "Cable Lateral Raise", "DB Lateral Raise",
    "3", "12-15", "60s", "1-2",
    "Side delt isolation.",
    "Exhale: raise | Inhale: lower",
    img("Cable Lateral Raise"), img("DB Lateral Raise"),
    superset=True
)

html_content += '''    </div>
'''

html_content += '''
    <div class="superset-block"><span class="superset-label">SUPERSET</span>
'''

html_content += exercise_card(
    "5A", "V-Bar Pushdown", "Rope Pushdown",
    "3", "12-15", "60s", "1-2",
    "Full lockout.",
    "Exhale: push down | Inhale: return",
    img("V-Bar Pushdown"), img("Rope Pushdown"),
    superset=True
)

html_content += exercise_card(
    "5B", "Overhead Cable Extension", "DB Overhead Extension",
    "3", "12-15", "60s", "1-2",
    "Long head stretch.",
    "Exhale: extend | Inhale: lower",
    img("Overhead Cable Extension"), img("DB Overhead Extension"),
    superset=True
)

html_content += '''    </div>
'''

html_content += '''
    <div class="sub-header cardio">Cardio</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>Moderate cycling (preferred) - 15-20 min | Cycling preferred.</span></div>
    </div>
    <div class="sub-header cooldown">Stretching</div>
    <div class="checklist">
'''

fri_stretches = [
    ("Doorway chest stretch", "30s"),
    ("Cross-body shoulder stretch", "30s"),
    ("Overhead tricep stretch", "30s"),
]

for stretch_name, duration in fri_stretches:
    if img(stretch_name):
        html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img(stretch_name)}" alt="{stretch_name}" loading="lazy"><span>{stretch_name} {duration}</span></div>\n'
    else:
        html_content += f'      <div class="check-item"><input type="checkbox"><span>{stretch_name} {duration}</span></div>\n'

html_content += '''    </div>
    <button class="reset-btn" onclick="resetDay(this)">Reset Day</button>
  </div>
</div>
'''

# SATURDAY - Legs + Pull B
html_content += '''
<!-- ==================== SATURDAY ==================== -->
<div class="day-section day-sat" id="day-sat">
  <div class="day-header" onclick="toggle(this)">Saturday - Legs + Pull B <span class="arrow">&#9660;</span></div>
  <div class="day-content">
    <div class="progress-bar"><div class="progress-fill" style="width:0%"></div></div>
    <div class="progress-text">0 / 0 completed</div>

    <div class="sub-header warmup">Warm-Up</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>Cycling (easy pace) - 5 min</span></div>
'''

if img("Glute bridges"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Glute bridges")}" alt="Glute bridges" loading="lazy"><span>Glute bridges - 15 reps</span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>Glute bridges - 15 reps</span></div>\n'

if img("Leg swings (front-back)"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Leg swings (front-back)")}" alt="Leg swings" loading="lazy"><span>Leg swings (front-back) - 10 each leg</span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>Leg swings (front-back) - 10 each leg</span></div>\n'

if img("Bodyweight squats"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Bodyweight squats")}" alt="Bodyweight squats" loading="lazy"><span>Bodyweight squats - 15 reps</span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>Bodyweight squats - 15 reps</span></div>\n'

if img("Hip mobility circles"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Hip mobility circles")}" alt="Hip mobility circles" loading="lazy"><span>Hip mobility circles - 10 each direction</span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>Hip mobility circles - 10 each direction</span></div>\n'

html_content += '''    </div>

    <div class="sub-header muscle">Legs + Back + Biceps + Calves + Core (11 exercises)</div>
'''

sat_pre_superset = [
    (1, "Romanian Deadlift (RDL)", "Cable Pull-Through", "3", "8-10", "90-120s", "1-2", "Do NOT go to failure.",
     "Inhale: hinge down | Exhale: stand up", "Romanian Deadlift (RDL)", "Cable Pull-Through", False, False, False),
    (2, "Hip Thrust", "Glute Bridge", "3", "10-12", "90s", "1-2", "Full glute squeeze at top.",
     "Exhale: thrust up | Inhale: lower", "Hip Thrust", "Glute Bridge", False, False, False),
    (3, "Bulgarian Split Squat", "Reverse Lunge", "2", "10 each", "60s", "2", "Replace with leg press if knee discomfort.",
     "Inhale: lower | Exhale: drive up", "Bulgarian Split Squat", "Reverse Lunge", False, False, False),
    (4, "Seated Cable Row", "Machine Row", "3", "10-12", "60s", "1-2", "Posture support.",
     "Exhale: pull | Inhale: extend", "Seated Cable Row", "Machine Row", False, False, False),
]

for ex in sat_pre_superset:
    html_content += exercise_card(ex[0], ex[1], ex[2], ex[3], ex[4], ex[5], ex[6], ex[7], ex[8],
                                   img(ex[9]), img(ex[10]), ex[11], ex[12], ex[13])

html_content += '''
    <div class="superset-block"><span class="superset-label">SUPERSET</span>
'''

html_content += exercise_card(
    "5A", "Rear Delt Cable Fly", "Seated Rear Delt Raise",
    "3", "12-15", "60s", "2",
    "Rear delt + posture. Light weight.",
    "Exhale: fly back | Inhale: return",
    img("Rear Delt Cable Fly"), img("Seated Rear Delt Raise"),
    superset=True
)

html_content += exercise_card(
    "5B", "Spider Curl", "Preacher Curl Machine",
    "3", "10-12", "60s", "1-2",
    "Strict form, no momentum.",
    "Exhale: curl | Inhale: lower",
    img("Spider Curl"), img("Preacher Curl Machine"),
    superset=True
)

html_content += '''    </div>
'''

html_content += exercise_card(
    6, "Incline Dumbbell Curl", "Concentration Curl",
    "2", "10-12", "60s", "2",
    "Stretch-focused. Fuller long-head development.",
    "Exhale: curl | Inhale: lower",
    img("Incline Dumbbell Curl"), img("Concentration Curl")
)

html_content += '''
    <div class="superset-block"><span class="superset-label">SUPERSET</span>
'''

html_content += exercise_card(
    "7A", "Cable Hammer Curl", "DB Cross-Body Hammer Curl",
    "2", "12", "60s", "1-2",
    "Forearm + brachialis focus.",
    "Exhale: curl | Inhale: lower",
    img("Cable Hammer Curl"), img("DB Cross-Body Hammer Curl"),
    superset=True
)

html_content += exercise_card(
    "7B", "Seated Calf Raise", "DB Standing Calf Raise",
    "2", "12-15", "45s", "1-2",
    "Targets soleus. Paired for time efficiency.",
    "Exhale: raise | Inhale: lower",
    img("Seated Calf Raise"), img("DB Standing Calf Raise"),
    superset=True
)

html_content += '''    </div>
'''

sat_core = [
    (8, "Hanging Knee Raise", "Captain's Chair Knee Raise", "2", "10", "45s", "2", "Controlled.",
     "Exhale: raise knees | Inhale: lower", "Hanging Knee Raise", "Captain's Chair Knee Raise", False, False, False),
    (9, "Cable Crunch", "Ab Crunch Machine", "2", "12-15", "45s", "2", "Upper abs focus.",
     "Exhale: crunch | Inhale: extend", "Cable Crunch", "Ab Crunch Machine", False, False, False),
]

for ex in sat_core:
    html_content += exercise_card(ex[0], ex[1], ex[2], ex[3], ex[4], ex[5], ex[6], ex[7], ex[8],
                                   img(ex[9]), img(ex[10]), ex[11], ex[12], ex[13])

html_content += '''
    <div class="sub-header cardio">Cardio</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>Easy walk only (optional) - 5-10 min | NO intense cardio.</span></div>
    </div>
    <div class="sub-header cooldown">Stretching</div>
    <div class="checklist">
'''

sat_stretches = [
    ("Seated hamstring stretch", "30s"),
    ("Figure-4 glute stretch", "30s"),
    ("Kneeling hip flexor stretch", "30s"),
    ("Child's pose stretch", "45s"),
    ("Wall calf stretch", "30s"),
]

for stretch_name, duration in sat_stretches:
    if img(stretch_name):
        html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img(stretch_name)}" alt="{stretch_name}" loading="lazy"><span>{stretch_name} {duration}</span></div>\n'
    else:
        html_content += f'      <div class="check-item"><input type="checkbox"><span>{stretch_name} {duration}</span></div>\n'

html_content += '''    </div>
    <button class="reset-btn" onclick="resetDay(this)">Reset Day</button>
  </div>
</div>
'''

# SUNDAY - Full Rest
html_content += '''
<!-- ==================== SUNDAY ==================== -->
<div class="day-section day-sun" id="day-sun">
  <div class="day-header" onclick="toggle(this)">Sunday - Full Rest <span class="arrow">&#9660;</span></div>
  <div class="day-content">
    <div class="progress-bar"><div class="progress-fill" style="width:0%"></div></div>
    <div class="progress-text">0 / 0 completed</div>

    <div class="sub-header cooldown">Recovery Checklist</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>Focus on recovery, mobility, hydration, and sleep</span></div>
      <div class="check-item"><input type="checkbox"><span>Optional: Easy walking or light stretching</span></div>
      <div class="check-item"><input type="checkbox"><span>Meal preparation for the week ahead</span></div>
      <div class="check-item"><input type="checkbox"><span>Hydrate - 3-4 liters of water</span></div>
      <div class="check-item"><input type="checkbox"><span>Sleep - aim for 7-8 hours</span></div>
      <div class="check-item"><input type="checkbox"><span>No gym work</span></div>
    </div>
    <button class="reset-btn" onclick="resetDay(this)">Reset Day</button>
  </div>
</div>
'''

# PROGRESSIVE OVERLOAD
html_content += '''
<!-- PROGRESSIVE OVERLOAD -->
<div class="day-section">
  <div class="day-header" style="background:#374151" onclick="toggle(this)">Progressive Overload Rules <span class="arrow">&#9660;</span></div>
  <div class="day-content">
    <p style="font-size:13px;color:var(--muted);margin-bottom:8px"><strong>Very important for chest and arm growth.</strong></p>
    <table class="info-table">
      <tr><th>Phase</th><th>What to Do</th></tr>
      <tr><td>Week 1</td><td>e.g. 15kg DB × 8 reps — Learn movements, focus on form</td></tr>
      <tr><td>Week 2</td><td>e.g. 15kg DB × 10 reps — Add reps with same weight</td></tr>
      <tr><td>Week 3</td><td>e.g. 17.5kg DB × 8 reps — Increase weight, reset reps</td></tr>
      <tr><td>Ongoing</td><td>Small progression over time builds muscle. Patience is key.</td></tr>
      <tr><td>Every 6-8 wks</td><td>Deload week — reduce weight, sets, and intensity for 1 week</td></tr>
    </table>
    <p style="font-size:12px;color:var(--muted);margin-top:8px">Keep workouts 75-100 mins max.</p>
  </div>
</div>

<!-- NUTRITION -->
<div class="day-section">
  <div class="day-header" style="background:#374151" onclick="toggle(this)">Nutrition Targets <span class="arrow">&#9660;</span></div>
  <div class="day-content">
    <table class="info-table">
      <tr><th>Macro</th><th>Daily Target</th><th>Notes</th></tr>
      <tr><td>Calories</td><td>1,900-2,200 kcal</td><td>Adjust based on progress</td></tr>
      <tr><td>Protein</td><td>120-140g/day</td><td>Very important for muscle growth (~2g/kg)</td></tr>
      <tr><td>Water</td><td>3-4 liters</td><td>More if sweating heavily</td></tr>
    </table>
  </div>
</div>

<!-- CARDIO RULES -->
<div class="day-section">
  <div class="day-header" style="background:#374151" onclick="toggle(this)">Cardio Rules <span class="arrow">&#9660;</span></div>
  <div class="day-content">
    <table class="info-table">
      <tr><th>Best Options</th><th>Avoid</th></tr>
      <tr><td>Cycling</td><td>Excessive HIIT</td></tr>
      <tr><td>Incline walk (moderate)</td><td>Long stairmaster sessions</td></tr>
      <tr><td>Elliptical</td><td>Intense incline treadmill after leg day</td></tr>
    </table>
  </div>
</div>

<!-- WARNING SIGNS -->
<div class="day-section">
  <div class="day-header" style="background:#c0392b" onclick="toggle(this)">Warning Signs — When to Stop & Switch <span class="arrow">&#9660;</span></div>
  <div class="day-content">
    <table class="info-table">
      <tr><th>Warning Sign</th><th>Action</th></tr>
      <tr><td>Sharp pain</td><td>Stop immediately — switch to alternate exercise</td></tr>
      <tr><td>Worsening knee pain</td><td>Switch to pain-free variant or skip</td></tr>
      <tr><td>Severe tailbone pain</td><td>Change cardio modality (try cycling)</td></tr>
      <tr><td>Strength drops continuously</td><td>Consider deload or extra rest day</td></tr>
      <tr><td>Fatigue becomes excessive</td><td>Reduce volume/intensity, check sleep</td></tr>
      <tr><td>Sleep worsens badly</td><td>Scale back training, prioritize recovery</td></tr>
    </table>
  </div>
</div>

<!-- EXPECTED RESULTS -->
<div class="day-section">
  <div class="day-header" style="background:#1a4a32" onclick="toggle(this)">Expected Results Timeline <span class="arrow">&#9660;</span></div>
  <div class="day-content">
    <table class="info-table">
      <tr><th>Timeline</th><th>Expected Changes</th></tr>
      <tr><td>8-12 weeks</td><td>Better chest fullness, slight waist reduction, improved arm size, better stamina</td></tr>
      <tr><td>4-6 months</td><td>Noticeable physique transformation, reduced belly fat, better shoulder/chest separation, stronger arms/forearms</td></tr>
      <tr><td>6-10 months</td><td>Body fat near 15-17%, strong aesthetic improvement, much leaner waist, visible muscularity</td></tr>
    </table>
    <p style="font-size:13px;color:var(--muted);margin-top:12px;font-style:italic"><strong>The most important factor is: CONSISTENCY over many months.</strong></p>
  </div>
</div>
'''

# Close container
html_content += '''
</div><!-- /container -->
'''

# Add modals and floating timer
html_content += '''
<div id="imgModal" class="img-modal" role="dialog">
  <img id="imgModalImg" src="" alt="Exercise reference">
</div>

<div id="confirmModal" class="confirm-modal" role="dialog">
  <div class="confirm-box">
    <h3>Timer Still Running!</h3>
    <p>Are you sure you want to uncheck this? The rest timer is still counting down.</p>
    <div class="confirm-btns">
      <button class="confirm-no" id="confirmNo">No, Keep It</button>
      <button class="confirm-yes" id="confirmYes">Yes, Stop Timer</button>
    </div>
  </div>
</div>

<div id="setOrderModal" class="confirm-modal" role="dialog">
  <div class="confirm-box">
    <h3>Complete Previous Set First!</h3>
    <p id="setOrderMsg">You need to finish Set 1 before moving to the next set.</p>
    <div class="confirm-btns">
      <button class="confirm-no" id="setOrderOk" style="background:#1e3c78;color:#fff;">Got It</button>
    </div>
  </div>
</div>

<div id="restTimerModal" class="confirm-modal" role="dialog">
  <div class="confirm-box">
    <h3>Rest Timer Running!</h3>
    <p>Wait for your rest period to finish before starting the next set.</p>
    <div class="confirm-btns">
      <button class="confirm-no" id="restTimerOk" style="background:#7c3aed;color:#fff;">Got It</button>
    </div>
  </div>
</div>

<div id="resetModal" class="confirm-modal" role="dialog">
  <div class="confirm-box">
    <h3>Reset This Day?</h3>
    <p>This will uncheck all exercises and sets for this day. Your progress will be lost.</p>
    <div class="confirm-btns">
      <button class="confirm-no" id="resetNo">Cancel</button>
      <button class="confirm-yes" id="resetYes">Yes, Reset</button>
    </div>
  </div>
</div>

<div id="weekResetModal" class="confirm-modal" role="dialog">
  <div class="confirm-box">
    <h3>Reset Entire Week?</h3>
    <p>This will archive all workout data for this week and then clear every day. Your data will be saved to the Weekly Log before reset.</p>
    <div class="confirm-btns">
      <button class="confirm-no" id="weekResetNo">Cancel</button>
      <button class="confirm-yes" id="weekResetYes">Yes, Reset Week</button>
    </div>
  </div>
</div>

<div id="floatingTimer" class="floating-timer">
  <div class="timer-label" id="timerLabel">Timer</div>
  <div class="timer-display" id="timerDisplay">0:00</div>
  <div class="timer-controls">
    <button class="timer-play" id="timerPlayBtn" onclick="timerToggle()">Start</button>
    <button class="timer-stop" onclick="timerStop()">Close</button>
  </div>
</div>
'''

# Now add the complete JavaScript from v2 (with v3 localStorage keys)
# I'll read the rest of the v2 file to get the complete JS
print("\nReading v2 JavaScript...")

with open("/tmp/v2_full.html", 'r') as f:
    v2_content = f.read()

# Extract JavaScript section (everything after <script> tag)
js_start = v2_content.find('<script>')
js_end = v2_content.find('</script>')
if js_start != -1 and js_end != -1:
    javascript = v2_content[js_start+8:js_end]
    # Replace v2 localStorage keys with v3
    javascript = javascript.replace('workout-checklist-v3', 'workout-v3-checklist')
    javascript = javascript.replace('workout-overload-v1', 'workout-v3-overload')
    javascript = javascript.replace('workout-overload-history', 'workout-v3-overload-history')
    javascript = javascript.replace('workout-weekly-log', 'workout-v3-weekly-log')
    javascript = javascript.replace('workout-week-start', 'workout-v3-week-start')
    javascript = javascript.replace('workout-last-archived-cycle', 'workout-v3-last-archived-cycle')

    # Replace tick-based timer with timestamp-based timer that survives screen lock
    old_timer = '''var timerInterval = null;
var timerSeconds = 0;
var timerRunning = false;
var timerTarget = 0;'''

    new_timer = '''var timerInterval = null;
var timerSeconds = 0;
var timerRunning = false;
var timerTarget = 0;
var timerEndTime = 0;'''

    javascript = javascript.replace(old_timer, new_timer)

    old_start = '''function startTimer(seconds, label) {
  clearInterval(timerInterval);
  timerTarget = seconds;
  timerSeconds = seconds;
  timerRunning = true;
  timerLabel.textContent = label || 'Timer';
  timerPlayBtn.textContent = 'Pause';
  timerPlayBtn.className = 'timer-pause';
  timerDisplay.className = 'timer-display';
  timerWidget.classList.add('active');
  renderTimer();
  timerInterval = setInterval(tickTimer, 1000);
}'''

    new_start = '''function startTimer(seconds, label) {
  clearInterval(timerInterval);
  timerTarget = seconds;
  timerSeconds = seconds;
  timerEndTime = Date.now() + seconds * 1000;
  timerRunning = true;
  timerLabel.textContent = label || 'Timer';
  timerPlayBtn.textContent = 'Pause';
  timerPlayBtn.className = 'timer-pause';
  timerDisplay.className = 'timer-display';
  timerWidget.classList.add('active');
  renderTimer();
  timerInterval = setInterval(tickTimer, 250);
}'''

    javascript = javascript.replace(old_start, new_start)

    old_tick = '''function tickTimer() {
  if (!timerRunning) return;
  timerSeconds--;
  renderTimer();
  if (timerSeconds <= 5 && timerSeconds > 0) {
    timerDisplay.className = 'timer-display warning';
  }
  if (timerSeconds <= 0) {
    clearInterval(timerInterval);
    timerRunning = false;
    timerDisplay.className = 'timer-display done';
    timerDisplay.textContent = 'DONE!';
    timerPlayBtn.textContent = 'Restart';
    timerPlayBtn.className = 'timer-play';
    try {
      var ac = new (window.AudioContext || window.webkitAudioContext)();
      var o = ac.createOscillator();
      var g = ac.createGain();
      o.connect(g); g.connect(ac.destination);
      o.frequency.value = 800;
      g.gain.value = 0.3;
      o.start(); o.stop(ac.currentTime + 0.3);
      setTimeout(function() {
        var o2 = ac.createOscillator();
        var g2 = ac.createGain();
        o2.connect(g2); g2.connect(ac.destination);
        o2.frequency.value = 1000;
        g2.gain.value = 0.3;
        o2.start(); o2.stop(ac.currentTime + 0.3);
      }, 350);
    } catch(e) {}
  }
}'''

    new_tick = '''function tickTimer() {
  if (!timerRunning) return;
  var remaining = Math.ceil((timerEndTime - Date.now()) / 1000);
  if (remaining < 0) remaining = 0;
  timerSeconds = remaining;
  renderTimer();
  if (timerSeconds <= 5 && timerSeconds > 0) {
    timerDisplay.className = 'timer-display warning';
  }
  if (timerSeconds <= 0) {
    clearInterval(timerInterval);
    timerRunning = false;
    timerDisplay.className = 'timer-display done';
    timerDisplay.textContent = 'DONE!';
    timerPlayBtn.textContent = 'Restart';
    timerPlayBtn.className = 'timer-play';
    try {
      var ac = new (window.AudioContext || window.webkitAudioContext)();
      var o = ac.createOscillator();
      var g = ac.createGain();
      o.connect(g); g.connect(ac.destination);
      o.frequency.value = 800;
      g.gain.value = 0.3;
      o.start(); o.stop(ac.currentTime + 0.3);
      setTimeout(function() {
        var o2 = ac.createOscillator();
        var g2 = ac.createGain();
        o2.connect(g2); g2.connect(ac.destination);
        o2.frequency.value = 1000;
        g2.gain.value = 0.3;
        o2.start(); o2.stop(ac.currentTime + 0.3);
      }, 350);
    } catch(e) {}
  }
}'''

    javascript = javascript.replace(old_tick, new_tick)

    old_toggle = '''function timerToggle() {
  if (timerDisplay.textContent === 'DONE!') {
    startTimer(timerTarget, timerLabel.textContent);
    return;
  }
  if (timerRunning) {
    timerRunning = false;
    clearInterval(timerInterval);
    timerPlayBtn.textContent = 'Start';
    timerPlayBtn.className = 'timer-play';
  } else {
    timerRunning = true;
    timerPlayBtn.textContent = 'Pause';
    timerPlayBtn.className = 'timer-pause';
    timerInterval = setInterval(tickTimer, 1000);
  }
}'''

    new_toggle = '''function timerToggle() {
  if (timerDisplay.textContent === 'DONE!') {
    startTimer(timerTarget, timerLabel.textContent);
    return;
  }
  if (timerRunning) {
    timerRunning = false;
    clearInterval(timerInterval);
    timerPlayBtn.textContent = 'Start';
    timerPlayBtn.className = 'timer-play';
  } else {
    timerEndTime = Date.now() + timerSeconds * 1000;
    timerRunning = true;
    timerPlayBtn.textContent = 'Pause';
    timerPlayBtn.className = 'timer-pause';
    timerInterval = setInterval(tickTimer, 250);
  }
}'''

    javascript = javascript.replace(old_toggle, new_toggle)

    # Patch exportCSV to use getActiveExerciseName instead of .ex-name
    javascript = javascript.replace(
        "var exName = card.querySelector('.ex-name');\n    var name = exName ? exName.textContent.trim() : '';",
        "var name = getActiveExerciseName(card);"
    )

    # Add exercise toggle JS at the end
    toggle_js = '''

// Exercise primary/alternate toggle
var EX_SEL_KEY = 'workout-v3-exercise-selection';

function loadExerciseSelections() {
  try { return JSON.parse(localStorage.getItem(EX_SEL_KEY)) || {}; } catch(e) { return {}; }
}

function saveExerciseSelections(sel) {
  localStorage.setItem(EX_SEL_KEY, JSON.stringify(sel));
}

function getActiveExerciseName(card) {
  var sel = loadExerciseSelections();
  var key = buildExerciseKey(card);
  var choice = sel[key] || 'primary';
  if (choice === 'alt') {
    return card.getAttribute('data-alt') || card.querySelector('.ex-name').textContent.trim();
  }
  return card.getAttribute('data-primary') || card.querySelector('.ex-name').textContent.trim();
}

function toggleExercise(btn) {
  var card = btn.closest('.exercise-card');
  var choice = btn.getAttribute('data-choice');
  var toggleDiv = btn.parentElement;
  var btns = toggleDiv.querySelectorAll('.toggle-btn');
  for (var i = 0; i < btns.length; i++) btns[i].classList.remove('active');
  btn.classList.add('active');

  var imgs = card.querySelectorAll('.ex-img-wrap');
  for (var j = 0; j < imgs.length; j++) imgs[j].classList.remove('dimmed');
  if (choice === 'primary' && imgs.length > 1) {
    imgs[1].classList.add('dimmed');
  } else if (choice === 'alt' && imgs.length > 0) {
    imgs[0].classList.add('dimmed');
  }

  var sel = loadExerciseSelections();
  sel[buildExerciseKey(card)] = choice;
  saveExerciseSelections(sel);
}

function restoreExerciseSelections() {
  var sel = loadExerciseSelections();
  var cards = document.querySelectorAll('.exercise-card[data-primary]');
  for (var i = 0; i < cards.length; i++) {
    var key = buildExerciseKey(cards[i]);
    var choice = sel[key];
    if (choice === 'alt') {
      var altBtn = cards[i].querySelector('.toggle-btn[data-choice="alt"]');
      if (altBtn) toggleExercise(altBtn);
    }
  }
}

restoreExerciseSelections();
'''

    javascript += toggle_js

    html_content += '<script>\n' + javascript + '\n</script>\n'

# Close HTML
html_content += '''
</body>
</html>
'''

# Write the file
print(f"\nWriting {OUTPUT}...")
with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"\n✓ Generated {OUTPUT}")
print(f"File size: {len(html_content) / 1024:.1f} KB")
print(f"Images embedded: {len([v for v in IMAGE_MAP.values() if v])} / {len(IMAGE_MAP)}")
print("\nDone! Open v3.html in your browser to test.")
