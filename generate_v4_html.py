#!/usr/bin/env python3
"""
Generate v4.html - Body Recomposition Workout Tracker
6-Day split with animated GIF images, progressive overload, rest timer
"""

import os
import base64
import json
import urllib.request
from pathlib import Path

# Paths
BASE_DIR = Path("/Users/amitraj/Desktop/Test")
IMG_DIR = BASE_DIR / "exercise_images"
OUTPUT = BASE_DIR / "v4.html"

# New images to download if missing
NEW_IMAGES = {
    "Wrist Curl": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/Palms-Up_Dumbbell_Wrist_Curl_Over_A_Bench/0.jpg",
    "Farmers Carry": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/Farmers_Walk/0.jpg",
    "Push-Ups": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/Push-Up_Wide/0.jpg",
    "One-Arm Dumbbell Row": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/One-Arm_Dumbbell_Row/0.jpg",
    "Wrist Roller": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/Wrist_Roller/0.jpg",
    "Stomach Vacuum": "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/Stomach_Vacuum/0.jpg",
}


def download_new_images():
    """Download new exercise images that don't exist yet"""
    for name, url in NEW_IMAGES.items():
        filename = name.replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")
        target = IMG_DIR / f"{filename}.jpg"
        if target.exists():
            continue
        print(f"  Downloading {name}...")
        try:
            urllib.request.urlretrieve(url, target)
            print(f"  ✓ Saved {target.name}")
        except Exception as e:
            print(f"  ✗ Failed to download {name}: {e}")


def image_name_to_filename(name):
    """Convert display name to image filename"""
    name = name.replace("(", "").replace(")", "")
    name = name.replace("/", "_").replace(" ", "_")
    return name


def find_image(name):
    """Find image file (gif or jpg) for exercise name"""
    base = image_name_to_filename(name)

    for ext in ['.gif', '.jpg']:
        path = IMG_DIR / f"{base}{ext}"
        if path.exists():
            return path

    for ext in ['.gif', '.jpg']:
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

    exercises = [
        # Day 1 - Push A
        "Incline Dumbbell Press", "Incline Machine Press",
        "Chest Press Machine", "Flat Dumbbell Press",
        "Cable Fly Mid_Low-to-High", "Pec Deck",
        "Seated DB Press", "Machine Shoulder Press",
        "DB Lateral Raise", "Cable Lateral Raise",
        "Rope Pushdown", "V-Bar Pushdown",
        "Overhead Rope Extension", "Single-Arm Cable Pushdown",
        "Push-Ups",

        # Day 2 - Legs + Shoulders
        "Leg Press", "Hack Squat",
        "Romanian Deadlift (RDL)", "Cable Pull-Through",
        "Walking Lunges", "Bulgarian Split Squat",
        "Lying Leg Curl", "Seated Leg Curl",
        "Leg Extension",
        "Standing Calf Raise", "Leg Press Calf Raise",
        "Rear Delt Cable Fly", "Seated Rear Delt Raise",
        "Reverse Pec Deck",

        # Day 3 - Pull A
        "Lat Pulldown", "Assisted Pull-Up",
        "Chest-Supported Row", "Seated Cable Row",
        "Machine Row",
        "Hammer Curl", "Cable Hammer Curl", "DB Hammer Curl",
        "Cable Curl",
        "Reverse Curl",
        "Wrist Curl",
        "Farmers Carry",
        "Incline Dumbbell Curl", "Machine Preacher Curl",

        # Day 5 - Push B
        "DB Floor Press",
        "One-Arm Dumbbell Row",

        # Day 6 - Pull B + Arms
        "Concentration Curl",
        "Wrist Roller",
        "Dead hang",

        # Core
        "Dead Bug", "Reverse Crunch",
        "Stomach Vacuum",
        "Cat-cow", "Cat-cow mobility",
        "Forearm plank", "Side plank",

        # Warm-ups
        "Shoulder rolls", "Band pull-aparts",
        "Wall slides (scapular activation)",
        "External rotations (light band/DB)",
        "Leg swings (front-back + side-side)", "Leg swings (front-back)",
        "Bodyweight squats", "Glute bridges",
        "Scapular pulldown", "Band rows",
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

    cable_curl_path = IMG_DIR / "Cable_single-arm_curl.jpg"
    if cable_curl_path.exists():
        img_map["Cable Curl"] = image_to_data_uri(cable_curl_path)
        print(f"  ✓ Cable Curl -> Cable_single-arm_curl.jpg (manual override)")

    return img_map


# Download new images first
print("Checking for new images to download...")
download_new_images()

# Build image map
IMAGE_MAP = build_image_map()


def img(name):
    """Get data URI for exercise name"""
    return IMAGE_MAP.get(name, "")


# HTML generation
print("\nGenerating v4.html...")

html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>6-Day Body Recomposition Plan v4</title>
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
.sub-header.core { background: #fff7ed; color: #9a3412; }

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
.tag.technique-warmup { background: #2563eb; color: #fff; font-size: 9px; padding: 1px 6px; }
.warmup-set { background: #eff6ff; border-left: 3px solid #2563eb; padding: 6px 10px; margin: 2px 0; font-size: 12px; color: #1e40af; border-radius: 4px; }
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
  <h1>BODY RECOMPOSITION <small style="font-size:14px;background:rgba(255,255,255,0.2);padding:2px 10px;border-radius:8px;">v4</small></h1>
  <p>6-Day Split &middot; Flat Stomach + Chest Growth + Bigger Arms + Wider Shoulders</p>
  <div class="badges">
    <span class="badge">Progressive Overload</span>
    <span class="badge">Body Recomposition</span>
    <span class="badge">Auto Rest Timer</span>
    <span class="badge">Daily Core</span>
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
      <tr><td>Goal</td><td>Body Recomposition — Flat stomach + Chest growth + Bigger biceps/forearms + Wider shoulders</td></tr>
      <tr><td>Injuries</td><td>Old right elbow injury, Previous left clavicle fracture, Mild knee discomfort, Tailbone discomfort (cardio)</td></tr>
      <tr><td>Equipment</td><td>Full Gym</td></tr>
      <tr><td>Schedule</td><td>6 days training, 1 rest day</td></tr>
      <tr><td>Approach</td><td>Lose fat slowly + Build muscle simultaneously</td></tr>
    </table>
  </div>
</div>

<!-- IMPORTANT RULES -->
<div class="day-section">
  <div class="day-header" style="background:#c0392b" onclick="toggle(this)">Important Rules & Safety <span class="arrow">&#9660;</span></div>
  <div class="day-content">
    <div class="sub-header muscle">Progressive Overload (Every 1-2 Weeks)</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>Increase weight slightly OR</span></div>
      <div class="check-item"><input type="checkbox"><span>Increase reps OR</span></div>
      <div class="check-item"><input type="checkbox"><span>Improve form</span></div>
    </div>

    <div class="sub-header muscle">Intensity Guide</div>
    <table class="info-table">
      <tr><th>Exercise Type</th><th>Rule</th></tr>
      <tr><td><strong>Compound lifts</strong> (Bench, Leg Press, RDL, Rows)</td><td>Stop with 1-2 reps left in tank</td></tr>
      <tr><td><strong>Isolation lifts</strong> (Curls, Lateral Raises, Pushdowns)</td><td>Final set can go near failure</td></tr>
    </table>

    <div class="sub-header muscle">Superset Rules</div>
    <table class="info-table">
      <tr><th>Use Supersets On</th><th>NEVER Superset</th></tr>
      <tr><td>Shoulders, Arms, Forearms, Chest isolation</td><td>Heavy bench press, Incline DB press</td></tr>
      <tr><td>Exercises where form stays clean</td><td>Leg press, RDL, Heavy rows</td></tr>
    </table>

    <div class="sub-header" style="background:#fef2f2;color:#991b1b">Cardio Goal</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>8000-10000 daily steps OR 20-25 min incline walk after workouts</span></div>
    </div>

    <div class="sub-header" style="background:#fef2f2;color:#991b1b">Injury Awareness</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span><strong>Old right elbow</strong> — avoid straight bar curls, prefer cables/dumbbells, neutral grip</span></div>
      <div class="check-item"><input type="checkbox"><span><strong>Left clavicle fracture</strong> — avoid fixed-bar pressing (Smith machine), prefer machine press or dumbbells</span></div>
      <div class="check-item"><input type="checkbox"><span>Mild knee discomfort — choose pain-free leg variants, controlled tempo</span></div>
      <div class="check-item"><input type="checkbox"><span>Tailbone discomfort — use padding, try cycling if seated cardio hurts</span></div>
      <div class="check-item"><input type="checkbox"><span>Sharp pain = STOP immediately and switch to alternate</span></div>
    </div>
  </div>
</div>

<!-- INJURY-AWARE TRAINING RULES -->
<div class="day-section">
  <div class="day-header" style="background:#dc2626" onclick="toggle(this)">Injury-Aware Training Rules <span class="arrow">&#9660;</span></div>
  <div class="day-content">
    <p style="font-size:13px;color:var(--muted);margin-bottom:12px"><strong>Customized for: Old right elbow injury + Previous left clavicle fracture</strong></p>
    <div class="sub-header" style="background:#fef2f2;color:#991b1b">Golden Rules</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span><strong>Prefer dumbbells and cables over barbells</strong> — free movement path reduces joint stress</span></div>
      <div class="check-item"><input type="checkbox"><span><strong>Neutral grip preference</strong> for pressing and pulling — easier on elbow and shoulder</span></div>
      <div class="check-item"><input type="checkbox"><span><strong>Never force painful range of motion</strong> — partial ROM is better than injury</span></div>
      <div class="check-item"><input type="checkbox"><span><strong>Controlled hypertrophy style</strong> — moderate weight, smooth reps, NOT ego lifting</span></div>
      <div class="check-item"><input type="checkbox"><span><strong>Prioritize rear delts + upper back</strong> for posture and shoulder health</span></div>
      <div class="check-item"><input type="checkbox"><span><strong>If pain: STOP immediately</strong> — reduce weight, modify ROM, or switch to alternate exercise</span></div>
    </div>
    <div class="sub-header" style="background:#ecfdf5;color:#065f46">Joint-Safe Exercise Selection</div>
    <table class="info-table">
      <tr><th>Joint</th><th>Avoid</th><th>Prefer</th></tr>
      <tr><td><strong>Right Elbow</strong></td><td>Straight barbell curls, skull crushers, heavy preacher curls</td><td>Cable curls, hammer curls, DB curls, neutral grip</td></tr>
      <tr><td><strong>Left Clavicle/AC Joint</strong></td><td>Fixed-path barbell pressing, heavy dips, upright rows</td><td>Machine press, DB press, cable flies, lateral raises</td></tr>
    </table>
    <div class="sub-header" style="background:#eff6ff;color:#1e40af">Pre-Workout Shoulder Prep (5 min — EVERY Upper Body Day)</div>
    <table class="info-table">
      <tr><th>Exercise</th><th>Sets × Reps</th><th>Purpose</th></tr>
      <tr><td>Band Pull-Aparts</td><td>2 × 20</td><td>Scapular stability</td></tr>
      <tr><td>External Rotations</td><td>2 × 15 each arm</td><td>Rotator cuff activation</td></tr>
      <tr><td>Wall Slides</td><td>2 × 15</td><td>Scapular wall activation</td></tr>
      <tr><td>Arm Circles</td><td>20 forward + 20 backward</td><td>Shoulder mobility</td></tr>
    </table>
  </div>
</div>

<!-- TRAINING GUIDE -->
<div class="day-section">
  <div class="day-header" style="background:#1e3a5f" onclick="toggle(this)">Training Guide — Weekly Split & Techniques <span class="arrow">&#9660;</span></div>
  <div class="day-content">
    <div class="sub-header muscle">Weekly Split</div>
    <table class="info-table">
      <tr><th>Day</th><th>Focus</th><th>Type</th><th>Time</th></tr>
      <tr><td>Day 1</td><td>Push A</td><td>Upper Chest Focus</td><td>~70 min</td></tr>
      <tr><td>Day 2</td><td>Legs + Shoulders</td><td>Quads + Hams + Delts</td><td>~75 min</td></tr>
      <tr><td>Day 3</td><td>Pull A</td><td>Back Width + Biceps + Forearms</td><td>~75 min</td></tr>
      <tr><td>Day 4</td><td>Active Recovery + Core</td><td>Mobility/Cardio/Core</td><td>~45 min</td></tr>
      <tr><td>Day 5</td><td>Push B</td><td>Chest Hypertrophy + Delts</td><td>~70 min</td></tr>
      <tr><td>Day 6</td><td>Pull B + Arms</td><td>Back + Arms Specialization</td><td>~75 min</td></tr>
      <tr><td>Day 7</td><td colspan="3">FULL REST</td></tr>
    </table>

    <div class="sub-header muscle">Intensity Technique Guide</div>
    <table class="info-table">
      <tr><th>Element</th><th>What It Means</th></tr>
      <tr><td><span class="tag rir">RIR: 2</span></td><td>Reps In Reserve — stop 2 reps before failure</td></tr>
      <tr><td><span class="tag technique-warmup">WARM-UP</span></td><td>Warm-Up Sets — lighter sets before working weight to prep joints/tendons</td></tr>
      <tr><td><span class="tag technique-failure">FAILURE</span></td><td>Go to Failure — last set, keep going until you can't with good form</td></tr>
      <tr><td><span class="tag technique-superset">SUPERSET</span></td><td>Superset — do both exercises back-to-back, no rest between them</td></tr>
    </table>

    <div class="sub-header muscle">Rep Ranges & Rest</div>
    <table class="info-table">
      <tr><th>Type</th><th>Reps</th><th>Rest</th></tr>
      <tr><td>Heavy compounds</td><td>8-10 reps</td><td>90-120 sec</td></tr>
      <tr><td>Hypertrophy</td><td>10-12 reps</td><td>60-90 sec</td></tr>
      <tr><td>Isolation</td><td>12-20 reps</td><td>45-60 sec</td></tr>
    </table>
  </div>
</div>
'''


def exercise_card(num, name, alt, sets, reps, rest, rir, note, breathing, primary_img, alt_img, superset=False, drop=False, failure=False, warmup_sets=0):
    """Generate an exercise card HTML"""
    set_count = int(str(sets).split('-')[0]) if '-' in str(sets) else int(str(sets).split()[0])

    tech_tags = ""
    if warmup_sets > 0:
        tech_tags += '<span class="tag technique-warmup">WARM-UP</span>'
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

    if warmup_sets >= 2:
        html += '<div class="warmup-set"><input type="checkbox"> Warm-Up Set 1 — 50% weight × 12 reps</div>\n'
        html += '<div class="warmup-set"><input type="checkbox"> Warm-Up Set 2 — 75% weight × 8 reps</div>\n'
    elif warmup_sets == 1:
        html += '<div class="warmup-set"><input type="checkbox"> Warm-Up Set — light weight × 10 reps</div>\n'

    for i in range(1, set_count + 1):
        html += f'<div class="check-item"><input type="checkbox"><span>Set {i} - {reps} reps</span></div>\n'
        if i < set_count:
            html += f'<div class="set-rest">Rest {rest}</div>\n'

    html += '''</div>
    </div>
'''
    return html


def mcgill_big3_section():
    """McGill Big 3 — pre-workout spine stability activation"""
    html = '''
    <div class="sub-header" style="background:#f0fdf4;color:#166534">McGill Big 3 (5 min — Spine Stability)</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>Bird Dog — 3 x 8 each side<br><small class="breathing-hint">Exhale: extend arm + opposite leg | Inhale: return. Keep hips level.</small></span></div>
'''
    if img("Side plank"):
        html += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Side plank")}" alt="Side plank" loading="lazy"><span>Side Plank — 3 x 20-30 sec each side<br><small class="breathing-hint">Breathe steadily, stack hips, brace core</small></span></div>\n'
    else:
        html += '      <div class="check-item"><input type="checkbox"><span>Side Plank — 3 x 20-30 sec each side<br><small class="breathing-hint">Breathe steadily, stack hips, brace core</small></span></div>\n'

    html += '''      <div class="check-item"><input type="checkbox"><span>Modified Curl-Up — 3 x 10<br><small class="breathing-hint">Hands under lower back, lift head/shoulders only 1-2 inches. Exhale: curl up | Inhale: lower</small></span></div>
    </div>
'''
    return html


def core_finisher_section():
    """Post-workout core finisher — flatten stomach exercises"""
    html = '''
    <div class="sub-header core">Core Finisher (5-10 min — Flatten Stomach)</div>
    <div class="checklist">
'''
    if img("Stomach Vacuum"):
        html += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Stomach Vacuum")}" alt="Vacuum breathing" loading="lazy"><span>Vacuum Breathing — 5 mins<br><small class="breathing-hint">Exhale fully, pull navel to spine, hold 10-15 sec, repeat</small></span></div>\n'
    else:
        html += '      <div class="check-item"><input type="checkbox"><span>Vacuum Breathing — 5 mins<br><small class="breathing-hint">Exhale fully, pull navel to spine, hold 10-15 sec, repeat</small></span></div>\n'

    if img("Forearm plank"):
        html += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Forearm plank")}" alt="Plank" loading="lazy"><span>Plank — 3 x 45 sec<br><small class="breathing-hint">Breathe steadily, squeeze core tight</small></span></div>\n'
    else:
        html += '      <div class="check-item"><input type="checkbox"><span>Plank — 3 x 45 sec<br><small class="breathing-hint">Breathe steadily, squeeze core tight</small></span></div>\n'

    if img("Dead Bug"):
        html += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Dead Bug")}" alt="Dead bugs" loading="lazy"><span>Dead Bugs — 3 x 12<br><small class="breathing-hint">Exhale: extend limbs | Inhale: return to start</small></span></div>\n'
    else:
        html += '      <div class="check-item"><input type="checkbox"><span>Dead Bugs — 3 x 12<br><small class="breathing-hint">Exhale: extend limbs | Inhale: return to start</small></span></div>\n'

    if img("Cat-cow"):
        html += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Cat-cow")}" alt="Cat-cow stretch" loading="lazy"><span>Cat-Cow Stretch — 2 mins<br><small class="breathing-hint">Inhale: arch back | Exhale: round spine</small></span></div>\n'
    else:
        html += '      <div class="check-item"><input type="checkbox"><span>Cat-Cow Stretch — 2 mins<br><small class="breathing-hint">Inhale: arch back | Exhale: round spine</small></span></div>\n'

    html += '    </div>\n'
    return html


def core_routine_section():
    """Legacy wrapper — returns McGill Big 3 + Core Finisher combined (used by Day 4/7)"""
    return mcgill_big3_section() + core_finisher_section()


def warmup_item(name, detail):
    """Generate a warm-up checklist item with image if available"""
    if img(name):
        return f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img(name)}" alt="{name}" loading="lazy"><span>{detail}</span></div>\n'
    return f'      <div class="check-item"><input type="checkbox"><span>{detail}</span></div>\n'


def stretch_items(stretches):
    """Generate stretch checklist items"""
    html = ''
    for name, duration in stretches:
        if img(name):
            html += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img(name)}" alt="{name}" loading="lazy"><span>{name} {duration}</span></div>\n'
        else:
            html += f'      <div class="check-item"><input type="checkbox"><span>{name} {duration}</span></div>\n'
    return html


# ==================== DAY 1 — PUSH A ====================
html_content += '''
<!-- ==================== DAY 1 ==================== -->
<div class="day-section day-mon" id="day-mon">
  <div class="day-header" onclick="toggle(this)">Day 1 — Push A (Upper Chest Focus) <span class="arrow">&#9660;</span></div>
  <div class="day-content">
    <div class="progress-bar"><div class="progress-fill" style="width:0%"></div></div>
    <div class="progress-text">0 / 0 completed</div>

    <div class="sub-header warmup">Light Cardio Warm-Up (5 min)</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>Incline treadmill walk — 5 mins<br><small class="breathing-hint">Breathe naturally through nose, increase blood flow</small></span></div>
    </div>

    <div class="sub-header warmup">Dynamic Mobility (5 min — Shoulder Prep)</div>
    <div class="checklist">
'''
html_content += warmup_item("Shoulder rolls", "Arm circles — 20 reps<br><small class=\"breathing-hint\">Breathe naturally on each rotation</small>")
html_content += warmup_item("Band pull-aparts", "Band pull-aparts — 2x20 reps<br><small class=\"breathing-hint\">Exhale: pull apart | Inhale: return</small>")
html_content += warmup_item("External rotations (light band/DB)", "External rotations — 2x15 each arm<br><small class=\"breathing-hint\">Exhale: rotate out | Inhale: return</small>")
html_content += warmup_item("Wall slides (scapular activation)", "Wall slides — 2x15<br><small class=\"breathing-hint\">Exhale: slide up | Inhale: slide down</small>")
html_content += '''      <div class="check-item"><input type="checkbox"><span>Arm Circles — 20 forward + 20 backward<br><small class="breathing-hint">Breathe naturally</small></span></div>
    </div>
'''

html_content += mcgill_big3_section()

html_content += '''
    <div class="sub-header muscle">Main Workout (7 exercises + 2 supersets)</div>
'''

# Day 1 standalone exercises
html_content += exercise_card(
    1, "Incline Dumbbell Press", "Incline Machine Press",
    "4", "8-10", "90-120s", "1-2",
    "Priority chest movement. Controlled eccentric.",
    "Inhale: lower to upper chest | Exhale: press up",
    img("Incline Dumbbell Press"), img("Incline Machine Press"),
    warmup_sets=2
)

html_content += exercise_card(
    2, "Seated DB Press", "Machine Shoulder Press",
    "3", "10-12", "90s", "1-2",
    "Shoulders = priority. Do them fresh for width.",
    "Exhale: press up | Inhale: lower to ears",
    img("Seated DB Press"), img("Machine Shoulder Press"),
    warmup_sets=1
)

html_content += exercise_card(
    3, "Chest Press Machine", "Flat Dumbbell Press",
    "4", "8-10", "90s", "1-2",
    "Controlled stretch at bottom. Mind-muscle connection.",
    "Inhale: lower to chest | Exhale: press up",
    img("Chest Press Machine"), img("Flat Dumbbell Press")
)

# SUPERSET 1 - Lateral Raise + Rope Pushdown
html_content += '''
    <div class="superset-block"><span class="superset-label">SUPERSET — Shoulder width + Arm pump</span>
'''

html_content += exercise_card(
    "4A", "DB Lateral Raise", "Cable Lateral Raise",
    "4", "15-20", "60s", "1-2",
    "Light weight, strict form. Side delt isolation.",
    "Exhale: raise arms to sides | Inhale: lower",
    img("DB Lateral Raise"), img("Cable Lateral Raise"),
    superset=True, failure=True
)

html_content += exercise_card(
    "4B", "Rope Pushdown", "V-Bar Pushdown",
    "4", "12-15", "60s", "1-2",
    "Elbows pinned. Full extension.",
    "Exhale: push down | Inhale: let rope rise",
    img("Rope Pushdown"), img("V-Bar Pushdown"),
    superset=True
)

html_content += '''    </div>
'''

# SUPERSET 2 - Cable Fly + Push-Ups
html_content += '''
    <div class="superset-block"><span class="superset-label">SUPERSET — Chest finisher</span>
'''

html_content += exercise_card(
    "5A", "Low-to-High Cable Fly", "Pec Deck",
    "3", "12-15", "60s", "2",
    "Slow eccentric. Squeeze at peak contraction.",
    "Inhale: open arms | Exhale: squeeze together",
    img("Cable Fly Mid_Low-to-High"), img("Pec Deck"),
    superset=True
)

html_content += exercise_card(
    "5B", "Push-Ups", "Incline Push-Ups",
    "3", "near failure", "60s", "0",
    "Go to near failure. Great chest finisher.",
    "Inhale: lower chest to floor | Exhale: push up",
    img("Push-Ups"), img("Push-Ups"),
    superset=True, failure=True
)

html_content += '''    </div>
'''

html_content += exercise_card(
    6, "Overhead Rope Extension", "Single-Arm Cable Pushdown",
    "3", "12-15", "60s", "1-2",
    "Long head stretch. Controlled movement.",
    "Exhale: extend arms overhead | Inhale: lower behind head",
    img("Overhead Rope Extension"), img("Single-Arm Cable Pushdown")
)

# Day 1 Core Finisher + Cardio + Stretching
html_content += core_finisher_section()

html_content += '''
    <div class="sub-header cardio">Post-Workout Cardio (15-20 min)</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>Incline treadmill walk — 15-20 min | Very effective for belly fat post-workout<br><small class="breathing-hint">Moderate pace, slightly breathless but can still talk</small></span></div>
    </div>

    <div class="sub-header cooldown">Stretching (5 min)</div>
    <div class="checklist">
'''

html_content += stretch_items([
    ("Doorway chest stretch", "30s"),
    ("Cross-body shoulder stretch", "30s"),
    ("Overhead tricep stretch", "30s"),
])

html_content += '''    </div>
    <button class="reset-btn" onclick="resetDay(this)">Reset Day</button>
  </div>
</div>
'''

# ==================== DAY 2 — LEGS + SHOULDERS ====================
html_content += '''
<!-- ==================== DAY 2 ==================== -->
<div class="day-section day-tue" id="day-tue">
  <div class="day-header" onclick="toggle(this)">Day 2 — Legs + Shoulders <span class="arrow">&#9660;</span></div>
  <div class="day-content">
    <div class="progress-bar"><div class="progress-fill" style="width:0%"></div></div>
    <div class="progress-text">0 / 0 completed</div>

    <div class="sub-header warmup">Light Cardio Warm-Up (5 min)</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>Cycling — 5 mins<br><small class="breathing-hint">Easy pace, warm up legs</small></span></div>
    </div>

    <div class="sub-header warmup">Dynamic Mobility (5 min — Legs + Hips)</div>
    <div class="checklist">
'''
html_content += warmup_item("Bodyweight squats", "Bodyweight squats — 15 reps<br><small class=\"breathing-hint\">Inhale: squat down | Exhale: stand up</small>")
html_content += warmup_item("Leg swings (front-back + side-side)", "Leg swings — 10 each leg<br><small class=\"breathing-hint\">Breathe naturally</small>")
html_content += warmup_item("Hip mobility circles", "Hip mobility circles<br><small class=\"breathing-hint\">Controlled circles, both directions</small>")
html_content += '''    </div>
'''

html_content += mcgill_big3_section()

html_content += '''
    <div class="sub-header muscle">Main Workout (8 exercises + 2 supersets)</div>
'''

# Day 2 standalone exercises
html_content += exercise_card(
    1, "Leg Press", "Hack Squat",
    "4", "10-12", "90-120s", "1-2",
    "Choose pain-free option for knee. Full ROM.",
    "Inhale: lower weight | Exhale: press up",
    img("Leg Press"), img("Hack Squat"),
    warmup_sets=2
)

html_content += exercise_card(
    2, "Romanian Deadlift (RDL)", "Cable Pull-Through",
    "4", "8-10", "90-120s", "1-2",
    "Do NOT go to failure. Feel hamstring stretch.",
    "Inhale: hinge down | Exhale: stand up",
    img("Romanian Deadlift (RDL)"), img("Cable Pull-Through"),
    warmup_sets=1
)

html_content += exercise_card(
    3, "Walking Lunges", "Bulgarian Split Squat",
    "3", "12 steps each", "60s", "2",
    "Controlled. Replace if knee discomfort.",
    "Inhale: step and lower | Exhale: drive up",
    img("Walking Lunges"), img("Bulgarian Split Squat")
)

html_content += exercise_card(
    4, "Lying Leg Curl", "Seated Leg Curl",
    "3", "12-15", "60s", "1-2",
    "Full ROM. Squeeze hamstrings at peak.",
    "Exhale: curl | Inhale: lower",
    img("Lying Leg Curl"), img("Seated Leg Curl")
)

# SUPERSET 1 - Leg Extension + Calf Raise
html_content += '''
    <div class="superset-block"><span class="superset-label">SUPERSET</span>
'''

html_content += exercise_card(
    "5A", "Leg Extension", "Walking Lunges",
    "3", "15", "60s", "1",
    "Squeeze at top. Controlled tempo.",
    "Exhale: extend | Inhale: lower",
    img("Leg Extension"), img("Walking Lunges"),
    superset=True, failure=True
)

html_content += exercise_card(
    "5B", "Standing Calf Raise", "Leg Press Calf Raise",
    "3", "15-20", "60s", "1-2",
    "Full stretch at bottom. Slow eccentric.",
    "Exhale: raise | Inhale: lower",
    img("Standing Calf Raise"), img("Leg Press Calf Raise"),
    superset=True
)

html_content += '''    </div>
'''

# SUPERSET 2 - Rear Delt + Cable Lateral (rear delts first for posture/clavicle)
html_content += '''
    <div class="superset-block"><span class="superset-label">SUPERSET — Shoulder aesthetics (posture first)</span>
'''

html_content += exercise_card(
    "6A", "Rear Delt Cable Fly", "Seated Rear Delt Raise",
    "4", "15", "60s", "2",
    "Rear delts first — posture + clavicle mechanics.",
    "Exhale: fly back | Inhale: return",
    img("Rear Delt Cable Fly"), img("Seated Rear Delt Raise"),
    superset=True
)

html_content += exercise_card(
    "6B", "Cable Lateral Raise", "DB Lateral Raise",
    "4", "15-20", "60s", "1-2",
    "Constant tension. Light weight, strict form.",
    "Exhale: raise arms | Inhale: lower",
    img("Cable Lateral Raise"), img("DB Lateral Raise"),
    superset=True, failure=True
)

html_content += '''    </div>
'''

# Day 2 Core Finisher + Cardio + Stretching
html_content += core_finisher_section()

html_content += '''
    <div class="sub-header cardio">Post-Workout Cardio (15 min)</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>Incline walk or cycling — 15 min<br><small class="breathing-hint">Moderate pace, slightly breathless but can still talk</small></span></div>
    </div>

    <div class="sub-header cooldown">Stretching (5 min)</div>
    <div class="checklist">
'''

html_content += stretch_items([
    ("Seated hamstring stretch", "30s"),
    ("Standing quad stretch", "30s"),
    ("Kneeling hip flexor stretch", "30s"),
    ("Wall calf stretch", "30s"),
])

html_content += '''    </div>
    <button class="reset-btn" onclick="resetDay(this)">Reset Day</button>
  </div>
</div>
'''

# ==================== DAY 3 — PULL A ====================
html_content += '''
<!-- ==================== DAY 3 ==================== -->
<div class="day-section day-wed" id="day-wed">
  <div class="day-header" onclick="toggle(this)">Day 3 — Pull A (Back Width + Biceps + Forearms) <span class="arrow">&#9660;</span></div>
  <div class="day-content">
    <div class="progress-bar"><div class="progress-fill" style="width:0%"></div></div>
    <div class="progress-text">0 / 0 completed</div>

    <div class="sub-header warmup">Light Cardio Warm-Up (5 min)</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>Rowing machine — 5 mins<br><small class="breathing-hint">Easy pace, engage back</small></span></div>
    </div>

    <div class="sub-header warmup">Dynamic Mobility (5 min — Back + Scapula)</div>
    <div class="checklist">
'''
html_content += warmup_item("Band rows", "Band rows — 20 reps<br><small class=\"breathing-hint\">Exhale: pull | Inhale: return</small>")
html_content += warmup_item("Scapular pulldown", "Scapular pull movements — 12 reps<br><small class=\"breathing-hint\">Exhale: pull scapulae down | Inhale: release</small>")
html_content += warmup_item("Band pull-aparts", "Band pull-aparts — 2x20 reps<br><small class=\"breathing-hint\">Exhale: pull apart | Inhale: return</small>")
html_content += warmup_item("External rotations (light band/DB)", "External rotations — 2x15 each arm<br><small class=\"breathing-hint\">Exhale: rotate out | Inhale: return</small>")
html_content += warmup_item("Wall slides (scapular activation)", "Wall slides — 2x15<br><small class=\"breathing-hint\">Exhale: slide up | Inhale: slide down</small>")
html_content += '''      <div class="check-item"><input type="checkbox"><span>Arm Circles — 20 forward + 20 backward<br><small class="breathing-hint">Breathe naturally</small></span></div>
    </div>
'''

html_content += mcgill_big3_section()

html_content += '''
    <div class="sub-header muscle">Main Workout (9 exercises + 2 supersets)</div>
'''

# Day 3 standalone exercises
html_content += exercise_card(
    1, "Lat Pulldown", "Assisted Pull-Up",
    "4", "10-12", "90s", "1-2",
    "Squeeze shoulder blades. Full stretch at top.",
    "Exhale: pull down | Inhale: extend arms",
    img("Lat Pulldown"), img("Assisted Pull-Up"),
    warmup_sets=2
)

html_content += exercise_card(
    2, "Chest-Supported Row", "Seated Cable Row",
    "4", "10", "90s", "1-2",
    "Lower-back friendly. Pull to lower chest.",
    "Exhale: pull to chest | Inhale: extend",
    img("Chest-Supported Row"), img("Seated Cable Row"),
    warmup_sets=1
)

html_content += exercise_card(
    3, "Assisted Pull-Up", "Lat Pulldown",
    "3", "max reps", "90s", "0",
    "Neurologically demanding — do fresher. Use assist as needed.",
    "Exhale: pull up | Inhale: lower",
    img("Assisted Pull-Up"), img("Lat Pulldown"),
    failure=True
)

html_content += exercise_card(
    4, "Seated Cable Row", "Machine Row",
    "3", "12", "60s", "1-2",
    "Neutral grip. Squeeze at peak.",
    "Exhale: pull | Inhale: extend arms",
    img("Seated Cable Row"), img("Machine Row")
)

html_content += exercise_card(
    5, "Cable Curl", "Machine Preacher Curl",
    "4", "10-12", "60s", "1-2",
    "Constant tension. Elbow-friendly. No fixed bar stress.",
    "Exhale: curl up | Inhale: lower",
    img("Cable Curl"), img("Machine Preacher Curl")
)

# SUPERSET 1 - Hammer + Reverse Curl (forearm growth)
html_content += '''
    <div class="superset-block"><span class="superset-label">SUPERSET — Forearm growth</span>
'''

html_content += exercise_card(
    "6A", "Hammer Curl", "Cable Hammer Curl",
    "4", "12", "60s", "1-2",
    "Forearm + brachialis focus.",
    "Exhale: curl | Inhale: lower",
    img("Hammer Curl"), img("Cable Hammer Curl"),
    superset=True
)

html_content += exercise_card(
    "6B", "Reverse Curl", "DB Hammer Curl",
    "4", "15", "60s", "2",
    "Forearm thickness. Light weight.",
    "Exhale: curl | Inhale: lower",
    img("Reverse Curl"), img("DB Hammer Curl"),
    superset=True, failure=True
)

html_content += '''    </div>
'''

# SUPERSET 2 - Wrist Curl + Farmer's Carry
html_content += '''
    <div class="superset-block"><span class="superset-label">SUPERSET — Grip + Forearms</span>
'''

html_content += exercise_card(
    "7A", "Wrist Curl", "Reverse Wrist Curl",
    "3", "15-20", "45s", "2",
    "Wrist flexion. Controlled tempo.",
    "Exhale: curl wrists up | Inhale: lower",
    img("Wrist Curl"), img("Wrist Curl"),
    superset=True
)

html_content += exercise_card(
    "7B", "Farmers Carry", "Dead Hang",
    "3", "30-40 sec", "45s", "1",
    "Heavy dumbbells. Grip tight, shoulders back.",
    "Breathe steadily throughout walk",
    img("Farmers Carry"), img("Dead hang"),
    superset=True
)

html_content += '''    </div>
'''

# Day 3 Core Finisher + Cardio + Stretching
html_content += core_finisher_section()

html_content += '''
    <div class="sub-header cardio">Post-Workout Cardio (15-20 min)</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>Incline treadmill walk — 15-20 min<br><small class="breathing-hint">Moderate pace, effective for recomposition post-workout</small></span></div>
    </div>

    <div class="sub-header cooldown">Stretching (5 min)</div>
    <div class="checklist">
'''

html_content += stretch_items([
    ("Kneeling lat prayer stretch", "30s"),
    ("Wall bicep stretch", "30s"),
    ("Wrist flexor/forearm stretch", "20s"),
])

html_content += '''    </div>
    <button class="reset-btn" onclick="resetDay(this)">Reset Day</button>
  </div>
</div>
'''

# ==================== DAY 4 — ACTIVE RECOVERY + CORE ====================
html_content += '''
<!-- ==================== DAY 4 ==================== -->
<div class="day-section day-thu" id="day-thu">
  <div class="day-header" onclick="toggle(this)">Day 4 — Active Recovery + Core <span class="arrow">&#9660;</span></div>
  <div class="day-content">
    <div class="progress-bar"><div class="progress-fill" style="width:0%"></div></div>
    <div class="progress-text">0 / 0 completed</div>
'''

html_content += core_routine_section()

html_content += '''
    <div class="sub-header cardio">Cardio (Choose One)</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>Brisk walking — 45 mins</span></div>
      <div class="check-item"><input type="checkbox"><span>OR Cycling — 30 mins</span></div>
      <div class="check-item"><input type="checkbox"><span>OR Incline treadmill — 30 mins</span></div>
    </div>

    <div class="sub-header cooldown">Mobility & Stretching</div>
    <div class="checklist">
'''

html_content += warmup_item("Cat-cow", "Cat-Cow — 2 mins<br><small class=\"breathing-hint\">Inhale: arch | Exhale: round</small>")
html_content += warmup_item("Child's pose stretch", "Child's Pose — 1 min<br><small class=\"breathing-hint\">Exhale: sink deeper</small>")
html_content += warmup_item("Kneeling hip flexor stretch", "Hip Flexor Stretch — 2 mins<br><small class=\"breathing-hint\">Exhale: lean forward gently</small>")
html_content += warmup_item("Seated hamstring stretch", "Hamstring Stretch — 2 mins<br><small class=\"breathing-hint\">Exhale: reach forward</small>")
html_content += warmup_item("Open book thoracic rotations", "Thoracic Rotation Stretch — 2 mins<br><small class=\"breathing-hint\">Exhale: rotate and open</small>")

html_content += '''      <div class="check-item"><input type="checkbox"><span>Cobra Stretch — 1 min<br><small class="breathing-hint">Inhale: rise up | Exhale: relax into stretch</small></span></div>
    </div>

    <div class="sub-header core">Extra Core Work</div>
    <div class="checklist">
'''

if img("Forearm plank"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Forearm plank")}" alt="Plank" loading="lazy"><span>Plank — 3 x 1 min<br><small class="breathing-hint">Steady breathing, tight core</small></span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>Plank — 3 x 1 min<br><small class="breathing-hint">Steady breathing, tight core</small></span></div>\n'

if img("Side plank"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Side plank")}" alt="Side plank" loading="lazy"><span>Side Plank — 3 x 30 sec each side<br><small class="breathing-hint">Stack hips, engage obliques</small></span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>Side Plank — 3 x 30 sec each side<br><small class="breathing-hint">Stack hips, engage obliques</small></span></div>\n'

if img("Dead Bug"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Dead Bug")}" alt="Dead bugs" loading="lazy"><span>Dead Bugs — 3 x 15<br><small class="breathing-hint">Exhale: extend | Inhale: return</small></span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>Dead Bugs — 3 x 15<br><small class="breathing-hint">Exhale: extend | Inhale: return</small></span></div>\n'

if img("Stomach Vacuum"):
    html_content += f'      <div class="check-item"><input type="checkbox"><img class="ref-img" src="{img("Stomach Vacuum")}" alt="Vacuum" loading="lazy"><span>Vacuum Breathing — 5 mins<br><small class="breathing-hint">Exhale fully, pull navel to spine, hold</small></span></div>\n'
else:
    html_content += '      <div class="check-item"><input type="checkbox"><span>Vacuum Breathing — 5 mins<br><small class="breathing-hint">Exhale fully, pull navel to spine, hold</small></span></div>\n'

html_content += '''    </div>
    <button class="reset-btn" onclick="resetDay(this)">Reset Day</button>
  </div>
</div>
'''

# ==================== DAY 5 — PUSH B ====================
html_content += '''
<!-- ==================== DAY 5 ==================== -->
<div class="day-section day-fri" id="day-fri">
  <div class="day-header" onclick="toggle(this)">Day 5 — Push B (Chest Hypertrophy + Delts) <span class="arrow">&#9660;</span></div>
  <div class="day-content">
    <div class="progress-bar"><div class="progress-fill" style="width:0%"></div></div>
    <div class="progress-text">0 / 0 completed</div>

    <div class="sub-header warmup">Light Cardio Warm-Up (5 min)</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>Treadmill walk — 5 mins<br><small class="breathing-hint">Easy pace, increase blood flow</small></span></div>
    </div>

    <div class="sub-header warmup">Dynamic Mobility (5 min — Shoulder Prep)</div>
    <div class="checklist">
'''
html_content += warmup_item("Band pull-aparts", "Band pull-aparts — 2x20 reps<br><small class=\"breathing-hint\">Exhale: pull apart | Inhale: return</small>")
html_content += warmup_item("External rotations (light band/DB)", "External rotations — 2x15 each arm<br><small class=\"breathing-hint\">Exhale: rotate out | Inhale: return</small>")
html_content += warmup_item("Wall slides (scapular activation)", "Wall slides — 2x15<br><small class=\"breathing-hint\">Exhale: slide up | Inhale: slide down</small>")
html_content += '''      <div class="check-item"><input type="checkbox"><span>Arm Circles — 20 forward + 20 backward<br><small class="breathing-hint">Breathe naturally</small></span></div>
    </div>
'''

html_content += mcgill_big3_section()

html_content += '''
    <div class="sub-header muscle">Main Workout (7 exercises + 2 supersets)</div>
'''

# Day 5 standalone exercises
html_content += exercise_card(
    1, "Incline Machine Press", "Chest Press Machine",
    "4", "10", "90s", "1-2",
    "Guided path, easier on clavicle/AC joint. Controlled eccentric.",
    "Inhale: lower to upper chest | Exhale: press up",
    img("Incline Machine Press"), img("Chest Press Machine"),
    warmup_sets=2
)

html_content += exercise_card(
    2, "Flat Dumbbell Press", "Chest Press Machine",
    "4", "10-12", "90s", "1-2",
    "Controlled stretch at bottom.",
    "Inhale: lower to chest | Exhale: press up",
    img("Flat Dumbbell Press"), img("Chest Press Machine"),
    warmup_sets=1
)

# SUPERSET 1 - Pec Deck + Push-Ups (chest pump)
html_content += '''
    <div class="superset-block"><span class="superset-label">SUPERSET — Huge chest pump</span>
'''

html_content += exercise_card(
    "3A", "Pec Deck", "Low-to-High Cable Fly",
    "3", "15", "60s", "1",
    "Controlled squeeze at peak.",
    "Inhale: open arms | Exhale: squeeze together",
    img("Pec Deck"), img("Cable Fly Mid_Low-to-High"),
    superset=True
)

html_content += exercise_card(
    "3B", "Push-Ups", "Incline Push-Ups",
    "3", "near failure", "60s", "0",
    "Go to near failure each set.",
    "Inhale: lower | Exhale: push up",
    img("Push-Ups"), img("Push-Ups"),
    superset=True, failure=True
)

html_content += '''    </div>
'''

# SUPERSET 2 - Lateral Raise + Rear Delt (broader shoulders)
html_content += '''
    <div class="superset-block"><span class="superset-label">SUPERSET — Broader shoulders</span>
'''

html_content += exercise_card(
    "4A", "DB Lateral Raise", "Cable Lateral Raise",
    "5", "15-20", "60s", "1-2",
    "5 sets for width. Light weight, strict form.",
    "Exhale: raise to sides | Inhale: lower",
    img("DB Lateral Raise"), img("Cable Lateral Raise"),
    superset=True, failure=True
)

html_content += exercise_card(
    "4B", "Rear Delt Cable Fly", "Reverse Pec Deck",
    "4", "15", "60s", "2",
    "Rear delt roundness.",
    "Exhale: fly back | Inhale: return",
    img("Rear Delt Cable Fly"), img("Reverse Pec Deck"),
    superset=True
)

html_content += '''    </div>
'''

html_content += exercise_card(
    5, "Rope Pushdown", "V-Bar Pushdown",
    "3", "15", "60s", "1-2",
    "Elbows pinned. Full lockout.",
    "Exhale: push down | Inhale: return",
    img("Rope Pushdown"), img("V-Bar Pushdown"),
    failure=True
)

# Day 5 Core Finisher + Cardio + Stretching
html_content += core_finisher_section()

html_content += '''
    <div class="sub-header cardio">Post-Workout Cardio (20 min)</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>Stairmaster or incline walk — 20 min<br><small class="breathing-hint">Moderate pace, excellent for recomposition after supersets</small></span></div>
    </div>

    <div class="sub-header cooldown">Stretching (5 min)</div>
    <div class="checklist">
'''

html_content += stretch_items([
    ("Doorway chest stretch", "30s"),
    ("Cross-body shoulder stretch", "30s"),
    ("Overhead tricep stretch", "30s"),
])

html_content += '''    </div>
    <button class="reset-btn" onclick="resetDay(this)">Reset Day</button>
  </div>
</div>
'''

# ==================== DAY 6 — PULL B + ARMS ====================
html_content += '''
<!-- ==================== DAY 6 ==================== -->
<div class="day-section day-sat" id="day-sat">
  <div class="day-header" onclick="toggle(this)">Day 6 — Pull B + Arms Specialization <span class="arrow">&#9660;</span></div>
  <div class="day-content">
    <div class="progress-bar"><div class="progress-fill" style="width:0%"></div></div>
    <div class="progress-text">0 / 0 completed</div>

    <div class="sub-header warmup">Light Cardio Warm-Up (5 min)</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>Rowing — 5 mins<br><small class="breathing-hint">Easy pace, engage back</small></span></div>
    </div>

    <div class="sub-header warmup">Dynamic Mobility (5 min — Back + Arms)</div>
    <div class="checklist">
'''
html_content += warmup_item("Band pull-aparts", "Band pull-aparts — 2x20 reps<br><small class=\"breathing-hint\">Exhale: pull apart | Inhale: return</small>")
html_content += warmup_item("External rotations (light band/DB)", "External rotations — 2x15 each arm<br><small class=\"breathing-hint\">Exhale: rotate out | Inhale: return</small>")
html_content += warmup_item("Wall slides (scapular activation)", "Wall slides — 2x15<br><small class=\"breathing-hint\">Exhale: slide up | Inhale: slide down</small>")
html_content += '''      <div class="check-item"><input type="checkbox"><span>Arm Circles — 20 forward + 20 backward<br><small class="breathing-hint">Breathe naturally</small></span></div>
      <div class="check-item"><input type="checkbox"><span>Wrist mobility circles<br><small class="breathing-hint">Both directions, 10 each</small></span></div>
    </div>
'''

html_content += mcgill_big3_section()

html_content += '''
    <div class="sub-header muscle">Main Workout (10 exercises + 3 supersets)</div>
'''

# Day 6 standalone exercises
html_content += exercise_card(
    1, "One-Arm Dumbbell Row", "Chest-Supported Row",
    "4", "10", "90s", "1-2",
    "Full stretch at bottom, squeeze at top.",
    "Exhale: pull to hip | Inhale: lower",
    img("One-Arm Dumbbell Row"), img("Chest-Supported Row"),
    warmup_sets=2
)

html_content += exercise_card(
    2, "Lat Pulldown", "Assisted Pull-Up",
    "4", "12", "60s", "1-2",
    "Neutral grip. Squeeze lats.",
    "Exhale: pull down | Inhale: extend",
    img("Lat Pulldown"), img("Assisted Pull-Up"),
    warmup_sets=1
)

html_content += exercise_card(
    3, "Seated Cable Row", "Machine Row",
    "3", "12", "60s", "1-2",
    "Close grip. Mid-back focus.",
    "Exhale: pull | Inhale: extend",
    img("Seated Cable Row"), img("Machine Row")
)

# SUPERSET 1 - Incline Curl + Rope Pushdown (arm growth)
html_content += '''
    <div class="superset-block"><span class="superset-label">SUPERSET — Classic arm growth</span>
'''

html_content += exercise_card(
    "4A", "Incline Dumbbell Curl", "Concentration Curl",
    "4", "12", "60s", "1-2",
    "Deep stretch. Light weight.",
    "Exhale: curl up | Inhale: lower fully",
    img("Incline Dumbbell Curl"), img("Concentration Curl"),
    superset=True
)

html_content += exercise_card(
    "4B", "Rope Pushdown", "V-Bar Pushdown",
    "4", "15", "60s", "1-2",
    "Full extension. Elbows pinned.",
    "Exhale: push down | Inhale: return",
    img("Rope Pushdown"), img("V-Bar Pushdown"),
    superset=True
)

html_content += '''    </div>
'''

# SUPERSET 2 - Hammer + Reverse Curl (brachialis + forearms)
html_content += '''
    <div class="superset-block"><span class="superset-label">SUPERSET — Brachialis + Forearms</span>
'''

html_content += exercise_card(
    "5A", "Hammer Curl", "Cable Hammer Curl",
    "3", "12", "60s", "1-2",
    "Brachialis focus. Neutral grip.",
    "Exhale: curl | Inhale: lower",
    img("Hammer Curl"), img("Cable Hammer Curl"),
    superset=True
)

html_content += exercise_card(
    "5B", "Reverse Curl", "DB Hammer Curl",
    "3", "15", "60s", "2",
    "Forearm extensor focus.",
    "Exhale: curl | Inhale: lower",
    img("Reverse Curl"), img("DB Hammer Curl"),
    superset=True, failure=True
)

html_content += '''    </div>
'''

# SUPERSET 3 - Grip work first, then wrist isolation
html_content += '''
    <div class="superset-block"><span class="superset-label">SUPERSET — Grip + Forearms (grip-intensive first)</span>
'''

html_content += exercise_card(
    "6A", "Dead Hang", "Farmers Carry",
    "3", "max time", "45s", "0",
    "Grip-intensive first — avoids wrist fatigue limiting carries.",
    "Breathe steadily, relax shoulders",
    img("Dead hang"), img("Farmers Carry"),
    superset=True, failure=True
)

html_content += exercise_card(
    "6B", "Wrist Roller", "Wrist Curl",
    "3", "3 rounds", "45s", "1",
    "Wrist isolation last. Roll up and down.",
    "Breathe steadily throughout",
    img("Wrist Roller"), img("Wrist Curl"),
    superset=True
)

html_content += '''    </div>
'''

# Day 6 Core Finisher + Cardio + Stretching
html_content += core_finisher_section()

html_content += '''
    <div class="sub-header cardio">Post-Workout Cardio (20 min)</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>Incline treadmill walk — 20 min<br><small class="breathing-hint">Moderate pace, post-workout fat burning zone</small></span></div>
    </div>

    <div class="sub-header cooldown">Stretching (5 min)</div>
    <div class="checklist">
'''

html_content += stretch_items([
    ("Kneeling lat prayer stretch", "30s"),
    ("Wall bicep stretch", "30s"),
    ("Wrist flexor/forearm stretch", "20s"),
    ("Cross-body shoulder stretch", "30s"),
])

html_content += '''    </div>
    <button class="reset-btn" onclick="resetDay(this)">Reset Day</button>
  </div>
</div>
'''

# ==================== DAY 7 — FULL REST ====================
html_content += '''
<!-- ==================== DAY 7 ==================== -->
<div class="day-section day-sun" id="day-sun">
  <div class="day-header" onclick="toggle(this)">Day 7 — Full Rest <span class="arrow">&#9660;</span></div>
  <div class="day-content">
    <div class="progress-bar"><div class="progress-fill" style="width:0%"></div></div>
    <div class="progress-text">0 / 0 completed</div>
'''

html_content += core_routine_section()

html_content += '''
    <div class="sub-header cooldown">Recovery Checklist</div>
    <div class="checklist">
      <div class="check-item"><input type="checkbox"><span>Optional: Light walking</span></div>
      <div class="check-item"><input type="checkbox"><span>Optional: Stretching / Mobility work</span></div>
      <div class="check-item"><input type="checkbox"><span>Hydrate — 3-4 liters of water</span></div>
      <div class="check-item"><input type="checkbox"><span>Sleep — aim for 7-8 hours</span></div>
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
    <p style="font-size:13px;color:var(--muted);margin-bottom:8px"><strong>Very important for chest, arm, and shoulder growth.</strong></p>
    <table class="info-table">
      <tr><th>Phase</th><th>What to Do</th></tr>
      <tr><td>Week 1</td><td>e.g. 15kg DB x 8 reps — Learn movements, focus on form</td></tr>
      <tr><td>Week 2</td><td>e.g. 15kg DB x 10 reps — Add reps with same weight</td></tr>
      <tr><td>Week 3</td><td>e.g. 17.5kg DB x 8 reps — Increase weight, reset reps</td></tr>
      <tr><td>Ongoing</td><td>Small progression over time. Every 1-2 weeks increase weight OR reps OR improve form.</td></tr>
      <tr><td>Every 6-8 wks</td><td>Deload week — reduce weight, sets, and intensity for 1 week</td></tr>
    </table>
  </div>
</div>

<!-- NUTRITION -->
<div class="day-section">
  <div class="day-header" style="background:#374151" onclick="toggle(this)">Nutrition — Body Recomposition <span class="arrow">&#9660;</span></div>
  <div class="day-content">
    <p style="font-size:13px;color:var(--muted);margin-bottom:8px"><strong>You do NOT need aggressive weight loss. Aim: lose fat slowly + build muscle simultaneously.</strong></p>
    <table class="info-table">
      <tr><th>Macro</th><th>Daily Target</th><th>Notes</th></tr>
      <tr><td>Calories</td><td>1,700-1,900 kcal</td><td>Slight deficit for fat loss</td></tr>
      <tr><td>Protein</td><td>120-140g/day</td><td>Very important for muscle growth</td></tr>
      <tr><td>Fiber</td><td>25-35g/day</td><td>For gut health and satiety</td></tr>
      <tr><td>Water</td><td>3-4 liters</td><td>More if sweating heavily</td></tr>
    </table>

    <div class="sub-header" style="background:#ecfdf5;color:#065f46;margin-top:16px">Best Foods for Your Goal</div>
    <table class="info-table">
      <tr><th>Keep (Good)</th><th>Limit (Bad)</th></tr>
      <tr><td>Oats, Whey protein</td><td>Alcohol frequently</td></tr>
      <tr><td>Curd, Paneer</td><td>Sugary snacks</td></tr>
      <tr><td>Moong / Chana</td><td>Overeating weekends</td></tr>
      <tr><td>Papaya, Banana (pre-workout)</td><td>Fried foods</td></tr>
      <tr><td>High protein milk</td><td></td></tr>
    </table>
  </div>
</div>

<!-- EXPECTED RESULTS -->
<div class="day-section">
  <div class="day-header" style="background:#1a4a32" onclick="toggle(this)">Expected Results Timeline <span class="arrow">&#9660;</span></div>
  <div class="day-content">
    <table class="info-table">
      <tr><th>Timeline</th><th>Expected Changes</th></tr>
      <tr><td>4 weeks</td><td>Tighter waist, less bloating, better energy</td></tr>
      <tr><td>8-12 weeks</td><td>Visible chest improvement, arm growth, flatter stomach</td></tr>
      <tr><td>4-6 months</td><td>Major physique transformation possible</td></tr>
    </table>
    <p style="font-size:13px;color:var(--muted);margin-top:12px;font-style:italic"><strong>This plan suits your current body shape much better than a generic bodybuilding split. CONSISTENCY is key.</strong></p>
  </div>
</div>
'''

# Close container
html_content += '''
</div><!-- /container -->
'''

# Modals and floating timer
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

# JavaScript - embedded directly (no external dependency)
html_content += '''<script>

function toggle(header) {
  var content = header.nextElementSibling;
  header.classList.toggle('collapsed');
  content.classList.toggle('hidden');
}

function updateCheckedClass(checkbox) {
  var item = checkbox.closest('.check-item');
  if (item) {
    if (checkbox.checked) { item.classList.add('checked'); }
    else { item.classList.remove('checked'); }
  }
}

function updateProgress(section) {
  var checkboxes = section.querySelectorAll('.day-content input[type="checkbox"]');
  var checked = 0;
  for (var i = 0; i < checkboxes.length; i++) {
    if (checkboxes[i].checked) checked++;
  }
  var total = checkboxes.length;
  var bar = section.querySelector('.progress-fill');
  var text = section.querySelector('.progress-text');
  if (bar && text) {
    bar.style.width = total ? (checked / total * 100) + '%' : '0%';
    text.textContent = checked + ' / ' + total + ' completed';
  }
}

var WEEKLY_LOG_KEY = 'workout-v4-weekly-log';

function loadWeeklyLog() {
  try { return JSON.parse(localStorage.getItem(WEEKLY_LOG_KEY)) || []; } catch(e) { return []; }
}

function saveWeeklyLog(log) {
  try { localStorage.setItem(WEEKLY_LOG_KEY, JSON.stringify(log)); } catch(e) {}
}

function archiveDayBeforeReset(section) {
  var dayId = section.id || 'unknown';
  var dayNames = {
    'day-mon': 'Day 1', 'day-tue': 'Day 2', 'day-wed': 'Day 3',
    'day-thu': 'Day 4', 'day-fri': 'Day 5', 'day-sat': 'Day 6', 'day-sun': 'Day 7'
  };
  var dayName = dayNames[dayId] || dayId;
  var now = new Date();
  var dateStr = now.toISOString().split('T')[0];
  var timeStr = now.toTimeString().split(' ')[0].substring(0, 5);
  var data = loadOverloadData();
  var exercises = [];

  var cards = section.querySelectorAll('.exercise-card');
  for (var c = 0; c < cards.length; c++) {
    var card = cards[c];
    var name = getActiveExerciseName(card);
    var exKey = buildExerciseKey(card);
    var sets = card.querySelectorAll('.set-tracker .check-item');
    var setsData = [];
    var hasData = false;

    for (var s = 0; s < sets.length; s++) {
      var cb = sets[s].querySelector('input[type="checkbox"]');
      var done = cb ? cb.checked : false;
      var setKey = exKey + '::set' + (s + 1);
      var w = data[setKey + '::weight'] || '';
      var r = data[setKey + '::reps'] || '';
      var ri = data[setKey + '::rir'] || '';
      if (done || w || r || ri) hasData = true;
      setsData.push({ set: s + 1, done: done, weight: w, reps: r, rir: ri });
    }

    if (hasData) {
      exercises.push({ name: name, sets: setsData });
    }
  }

  if (exercises.length === 0) return;

  var log = loadWeeklyLog();
  log.push({
    date: dateStr, time: timeStr, day: dayName,
    week: getWeekNumber(),
    cycle: Math.floor((getWeekNumber() - 1) / 3) + 1,
    exercises: exercises
  });
  saveWeeklyLog(log);
}

var resetModal = document.getElementById('resetModal');
var resetYes = document.getElementById('resetYes');
var resetNo = document.getElementById('resetNo');
var pendingResetSection = null;

function resetDay(btn) {
  pendingResetSection = btn.closest('.day-section');
  resetModal.classList.add('active');
}

resetYes.addEventListener('click', function() {
  resetModal.classList.remove('active');
  if (pendingResetSection) {
    archiveDayBeforeReset(pendingResetSection);
    var checkboxes = pendingResetSection.querySelectorAll('input[type="checkbox"]');
    for (var i = 0; i < checkboxes.length; i++) {
      checkboxes[i].checked = false;
      updateCheckedClass(checkboxes[i]);
    }
    updateProgress(pendingResetSection);
    saveState();
    if (timerRunning) timerStop();
    pendingResetSection = null;
  }
}, false);

resetNo.addEventListener('click', function() {
  resetModal.classList.remove('active');
  pendingResetSection = null;
}, false);

var weekResetModal = document.getElementById('weekResetModal');
var weekResetYes = document.getElementById('weekResetYes');
var weekResetNo = document.getElementById('weekResetNo');

weekResetYes.addEventListener('click', function() {
  weekResetModal.classList.remove('active');
  var sections = document.querySelectorAll('.day-section[id]');
  for (var i = 0; i < sections.length; i++) {
    archiveDayBeforeReset(sections[i]);
    var checkboxes = sections[i].querySelectorAll('input[type="checkbox"]');
    for (var j = 0; j < checkboxes.length; j++) {
      checkboxes[j].checked = false;
      updateCheckedClass(checkboxes[j]);
    }
    updateProgress(sections[i]);
  }
  saveState();
  if (timerRunning) timerStop();
}, false);

weekResetNo.addEventListener('click', function() {
  weekResetModal.classList.remove('active');
}, false);

(function moveResetButtons() {
  var buttons = document.querySelectorAll('.reset-btn');
  for (var i = 0; i < buttons.length; i++) {
    var btn = buttons[i];
    var section = btn.closest('.day-content');
    if (!section) continue;
    var progressText = section.querySelector('.progress-text');
    if (progressText) {
      progressText.parentNode.insertBefore(btn, progressText.nextSibling);
    }
  }
})();

function saveState() {
  var state = {};
  var sections = document.querySelectorAll('.day-section[id]');
  for (var s = 0; s < sections.length; s++) {
    var section = sections[s];
    var id = section.id;
    var checks = [];
    var cbs = section.querySelectorAll('input[type="checkbox"]');
    for (var i = 0; i < cbs.length; i++) {
      checks.push(cbs[i].checked);
    }
    state[id] = checks;
  }
  try { localStorage.setItem('workout-v4-checklist', JSON.stringify(state)); } catch(e) {}
}

function loadState() {
  try {
    var state = JSON.parse(localStorage.getItem('workout-v4-checklist'));
    if (!state) return;
    var sections = document.querySelectorAll('.day-section[id]');
    for (var s = 0; s < sections.length; s++) {
      var section = sections[s];
      var id = section.id;
      if (state[id]) {
        var checkboxes = section.querySelectorAll('input[type="checkbox"]');
        for (var i = 0; i < state[id].length; i++) {
          if (checkboxes[i]) {
            checkboxes[i].checked = state[id][i];
            updateCheckedClass(checkboxes[i]);
          }
        }
        updateProgress(section);
      }
    }
  } catch(e) {}
}

function startTimerFromBtn(btn) {
  var secs = parseInt(btn.getAttribute('data-seconds'));
  var label = btn.getAttribute('data-label') || 'Timer';
  if (secs > 0) startTimer(secs, label);
}

function autoStartTimer(checkbox) {
  if (!checkbox.checked) return;
  var item = checkbox.closest('.check-item');
  if (!item) return;

  var setTracker = item.closest('.set-tracker');
  if (setTracker) {
    var next = item.nextElementSibling;
    if (next && next.classList.contains('set-rest')) {
      var btn = next.querySelector('.timer-btn');
      if (btn) startTimerFromBtn(btn);
      return;
    }
    var card = setTracker.closest('.exercise-card');
    if (card) {
      var restTag = card.querySelector('.tag.rest');
      var restSecs = restTag ? parseSeconds(restTag.textContent) : 0;
      if (restSecs > 0) {
        var nextCard = card.nextElementSibling;
        while (nextCard && !nextCard.classList.contains('exercise-card') && !nextCard.classList.contains('superset-block')) {
          nextCard = nextCard.nextElementSibling;
        }
        if (nextCard && nextCard.classList.contains('superset-block')) {
          nextCard = nextCard.querySelector('.exercise-card');
        }
        if (nextCard) {
          var nextName = nextCard.querySelector('.ex-name');
          var label = 'Rest before ' + (nextName ? nextName.textContent : 'next exercise');
          startTimer(restSecs, label);
        }
      }
    }
    return;
  }

  var ownBtn = item.querySelector('.timer-btn');
  if (ownBtn) { startTimerFromBtn(ownBtn); return; }
  var checklist = item.closest('.checklist');
  if (checklist) {
    var next2 = item.nextElementSibling;
    while (next2) {
      if (next2.classList.contains('check-item')) {
        var nextBtn = next2.querySelector('.timer-btn');
        if (nextBtn) { startTimerFromBtn(nextBtn); return; }
        break;
      }
      next2 = next2.nextElementSibling;
    }
  }
}

var confirmModal = document.getElementById('confirmModal');
var confirmYes = document.getElementById('confirmYes');
var confirmNo = document.getElementById('confirmNo');
var pendingUncheckCb = null;

var setOrderModal = document.getElementById('setOrderModal');
var setOrderMsg = document.getElementById('setOrderMsg');
var setOrderOk = document.getElementById('setOrderOk');

function showUncheckWarning(cb) {
  pendingUncheckCb = cb;
  cb.checked = true;
  updateCheckedClass(cb);
  confirmModal.classList.add('active');
}

function checkSetOrder(cb) {
  if (!cb.checked) return true;
  var item = cb.closest('.check-item');
  if (!item) return true;
  var tracker = item.closest('.set-tracker');
  if (!tracker) return true;
  var sets = tracker.querySelectorAll('.check-item');
  for (var i = 0; i < sets.length; i++) {
    if (sets[i] === item) break;
    var prevCb = sets[i].querySelector('input[type="checkbox"]');
    if (prevCb && !prevCb.checked) {
      cb.checked = false;
      updateCheckedClass(cb);
      setOrderMsg.textContent = 'You need to finish Set ' + (i + 1) + ' before moving to the next set.';
      setOrderModal.classList.add('active');
      return false;
    }
  }
  return true;
}

var restTimerModal = document.getElementById('restTimerModal');
var restTimerOk = document.getElementById('restTimerOk');

setOrderOk.addEventListener('click', function() { setOrderModal.classList.remove('active'); }, false);
restTimerOk.addEventListener('click', function() { restTimerModal.classList.remove('active'); }, false);

confirmYes.addEventListener('click', function() {
  confirmModal.classList.remove('active');
  if (pendingUncheckCb) {
    pendingUncheckCb.checked = false;
    updateCheckedClass(pendingUncheckCb);
    var section = pendingUncheckCb.closest('.day-section[id]');
    if (section) updateProgress(section);
    saveState();
    timerStop();
    pendingUncheckCb = null;
  }
}, false);

confirmNo.addEventListener('click', function() {
  confirmModal.classList.remove('active');
  if (pendingUncheckCb) {
    var section = pendingUncheckCb.closest('.day-section[id]');
    if (section) updateProgress(section);
    saveState();
    pendingUncheckCb = null;
  }
}, false);

function handleCheckbox(cb) {
  if (cb.checked && timerRunning) {
    cb.checked = false;
    updateCheckedClass(cb);
    restTimerModal.classList.add('active');
    return;
  }
  if (cb.checked && !checkSetOrder(cb)) return;
  if (!cb.checked && timerRunning) { showUncheckWarning(cb); return; }
  updateCheckedClass(cb);
  var section = cb.closest('.day-section[id]');
  if (section) updateProgress(section);
  saveState();
  autoStartTimer(cb);
}

document.addEventListener('change', function(e) {
  if (e.target && e.target.type === 'checkbox') handleCheckbox(e.target);
}, false);

document.addEventListener('click', function(e) {
  if (e.target.type === 'checkbox') return;
  var span = e.target.closest('.check-item > span');
  if (!span) return;
  if (e.target.tagName === 'IMG') return;
  if (e.target.type === 'number') return;
  if (e.target.tagName === 'LABEL') return;
  if (e.target.tagName === 'BUTTON') return;
  if (e.target.closest('.set-inputs')) return;
  var item = span.closest('.check-item');
  if (!item) return;
  var cb = item.querySelector('input[type="checkbox"]');
  if (cb) { cb.checked = !cb.checked; handleCheckbox(cb); }
}, false);

function expandToday() {
  var days = ['day-sun','day-mon','day-tue','day-wed','day-thu','day-fri','day-sat'];
  var today = days[new Date().getDay()];
  var allSections = document.querySelectorAll('.day-section');
  for (var i = 0; i < allSections.length; i++) {
    var section = allSections[i];
    var header = section.querySelector('.day-header');
    var content = section.querySelector('.day-content');
    if (section.id === today) {
      header.classList.remove('collapsed');
      content.classList.remove('hidden');
    } else {
      header.classList.add('collapsed');
      content.classList.add('hidden');
    }
  }
}

function initProgress() {
  var sections = document.querySelectorAll('.day-section[id]');
  for (var i = 0; i < sections.length; i++) updateProgress(sections[i]);
}

loadState();
initProgress();
expandToday();

var modal = document.getElementById('imgModal');
var modalImg = document.getElementById('imgModalImg');
var allImages = document.querySelectorAll('.ref-img, .ex-img-wrap img');
for (var i = 0; i < allImages.length; i++) {
  allImages[i].addEventListener('click', function(e) {
    e.stopPropagation(); e.preventDefault();
    modalImg.src = this.src;
    modal.classList.add('active');
  }, false);
}
modal.addEventListener('click', function() { modal.classList.remove('active'); modalImg.src = ''; }, false);

// === FLOATING TIMER (timestamp-based, survives screen lock) ===
var timerInterval = null;
var timerSeconds = 0;
var timerRunning = false;
var timerTarget = 0;
var timerEndTime = 0;
var timerWidget = document.getElementById('floatingTimer');
var timerDisplay = document.getElementById('timerDisplay');
var timerLabel = document.getElementById('timerLabel');
var timerPlayBtn = document.getElementById('timerPlayBtn');

function startTimer(seconds, label) {
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
}

function tickTimer() {
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
      o.frequency.value = 800; g.gain.value = 0.3;
      o.start(); o.stop(ac.currentTime + 0.3);
      setTimeout(function() {
        var o2 = ac.createOscillator();
        var g2 = ac.createGain();
        o2.connect(g2); g2.connect(ac.destination);
        o2.frequency.value = 1000; g2.gain.value = 0.3;
        o2.start(); o2.stop(ac.currentTime + 0.3);
      }, 350);
    } catch(e) {}
  }
}

function renderTimer() {
  var m = Math.floor(timerSeconds / 60);
  var s = timerSeconds % 60;
  timerDisplay.textContent = m + ':' + (s < 10 ? '0' : '') + s;
}

function timerToggle() {
  if (timerDisplay.textContent === 'DONE!') { startTimer(timerTarget, timerLabel.textContent); return; }
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
}

function timerStop() {
  clearInterval(timerInterval);
  timerRunning = false;
  timerSeconds = 0;
  timerWidget.classList.remove('active');
}

function parseSeconds(text) {
  var m = text.match(/(\\d+)\\s*min/);
  if (m) return parseInt(m[1]) * 60;
  m = text.match(/(\\d+)\\s*s/);
  if (m) return parseInt(m[1]);
  return 0;
}

// === PROGRESSIVE OVERLOAD ===
var PO_KEY = 'workout-v4-overload';
var PO_HISTORY_KEY = 'workout-v4-overload-history';

function getWeekNumber() {
  var start = localStorage.getItem('workout-v4-week-start');
  if (!start) {
    var d = new Date();
    d.setDate(d.getDate() - d.getDay() + 1);
    start = d.toISOString().split('T')[0];
    localStorage.setItem('workout-v4-week-start', start);
  }
  var startDate = new Date(start);
  var now = new Date();
  var diff = Math.floor((now - startDate) / (7 * 24 * 60 * 60 * 1000));
  return diff + 1;
}

function getCycleWeek() { return ((getWeekNumber() - 1) % 3) + 1; }
function getTargetReps(cycleWeek) { if (cycleWeek === 1) return 10; if (cycleWeek === 2) return 11; return 12; }

function loadOverloadData() { try { return JSON.parse(localStorage.getItem(PO_KEY)) || {}; } catch(e) { return {}; } }
function saveOverloadData(data) { try { localStorage.setItem(PO_KEY, JSON.stringify(data)); } catch(e) {} }
function loadOverloadHistory() { try { return JSON.parse(localStorage.getItem(PO_HISTORY_KEY)) || {}; } catch(e) { return {}; } }
function saveOverloadHistory(data) { try { localStorage.setItem(PO_HISTORY_KEY, JSON.stringify(data)); } catch(e) {} }

function buildExerciseKey(card) {
  var name = card.querySelector('.ex-name');
  var section = card.closest('.day-section');
  var dayId = section ? section.id : 'unknown';
  return dayId + '::' + (name ? name.textContent.trim() : 'ex');
}

function injectOverloadInputs() {
  var weekNum = getWeekNumber();
  var cycleWeek = getCycleWeek();
  var targetReps = getTargetReps(cycleWeek);
  var data = loadOverloadData();
  var history = loadOverloadHistory();
  var cycleNum = Math.floor((weekNum - 1) / 3) + 1;

  var cards = document.querySelectorAll('.exercise-card');
  for (var c = 0; c < cards.length; c++) {
    var card = cards[c];
    var exKey = buildExerciseKey(card);
    if (!data[exKey]) data[exKey] = {};

    var prevCycleKey = 'cycle' + (cycleNum - 1);
    var prev = (history[exKey] && history[exKey][prevCycleKey]) ? history[exKey][prevCycleKey] : null;

    var sets = card.querySelectorAll('.set-tracker .check-item');
    for (var s = 0; s < sets.length; s++) {
      var setItem = sets[s];
      var setKey = exKey + '::set' + (s + 1);

      var row = document.createElement('div');
      row.className = 'set-inputs';

      var weightLabel = document.createElement('label');
      weightLabel.innerHTML = 'kg';
      var weightInput = document.createElement('input');
      weightInput.type = 'number'; weightInput.min = '0'; weightInput.step = '0.5'; weightInput.placeholder = '\\u2014';
      weightInput.setAttribute('data-key', setKey + '::weight');
      if (data[setKey + '::weight'] !== undefined) weightInput.value = data[setKey + '::weight'];
      weightLabel.insertBefore(weightInput, weightLabel.firstChild);

      var repsLabel = document.createElement('label');
      repsLabel.innerHTML = 'reps';
      var repsInput = document.createElement('input');
      repsInput.type = 'number'; repsInput.min = '0'; repsInput.step = '1'; repsInput.placeholder = targetReps;
      repsInput.setAttribute('data-key', setKey + '::reps');
      if (data[setKey + '::reps'] !== undefined) repsInput.value = data[setKey + '::reps'];
      repsLabel.insertBefore(repsInput, repsLabel.firstChild);

      var rirLabel = document.createElement('label');
      rirLabel.innerHTML = 'RIR';
      var rirInput = document.createElement('input');
      rirInput.type = 'number'; rirInput.min = '0'; rirInput.max = '5'; rirInput.step = '1'; rirInput.placeholder = '2';
      rirInput.setAttribute('data-key', setKey + '::rir');
      if (data[setKey + '::rir'] !== undefined) rirInput.value = data[setKey + '::rir'];
      rirLabel.insertBefore(rirInput, rirLabel.firstChild);

      row.appendChild(weightLabel);
      row.appendChild(repsLabel);
      row.appendChild(rirLabel);

      if (prev && prev['set' + (s+1)]) {
        var prevInfo = document.createElement('span');
        prevInfo.className = 'set-prev';
        prevInfo.textContent = 'Prev: ' + (prev['set'+(s+1)].weight || '\\u2014') + 'kg \\u00d7 ' + (prev['set'+(s+1)].reps || '\\u2014');
        row.appendChild(prevInfo);
      }

      setItem.appendChild(row);
    }
  }

  saveOverloadData(data);

  document.addEventListener('input', function(e) {
    if (e.target.type === 'number' && e.target.getAttribute('data-key')) {
      var d = loadOverloadData();
      d[e.target.getAttribute('data-key')] = e.target.value === '' ? undefined : parseFloat(e.target.value);
      saveOverloadData(d);
    }
  }, false);
}

function addWeekBanner() {
  var weekNum = getWeekNumber();
  var cycleWeek = getCycleWeek();
  var targetReps = getTargetReps(cycleWeek);
  var cycleNum = Math.floor((weekNum - 1) / 3) + 1;

  var banner = document.createElement('div');
  banner.style.cssText = 'background:linear-gradient(135deg,#7c3aed,#2d6cdf);color:#fff;padding:12px 20px;border-radius:12px;margin:0 0 16px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;font-size:13px;';
  banner.innerHTML = '<div><strong>Week ' + weekNum + '</strong> (Cycle ' + cycleNum + ', Week ' + cycleWeek + '/3)</div>' +
    '<div style="display:flex;gap:12px;align-items:center;">' +
    '<span style="background:rgba(255,255,255,0.2);padding:3px 10px;border-radius:8px;font-weight:700;">Target: ' + targetReps + ' reps</span>' +
    '<span style="font-size:11px;opacity:0.85;">' +
    (cycleWeek === 3 ? 'Next week: increase weight, reset to 10 reps' : 'Next week: ' + getTargetReps(cycleWeek + 1) + ' reps') +
    '</span></div>';
  var container = document.querySelector('.container');
  var firstSection = container.querySelector('.day-section');
  container.insertBefore(banner, firstSection);
}

function archiveCycleIfNeeded() {
  var weekNum = getWeekNumber();
  var cycleNum = Math.floor((weekNum - 1) / 3) + 1;
  var lastArchived = localStorage.getItem('workout-v4-last-archived-cycle');
  if (lastArchived && parseInt(lastArchived) >= cycleNum - 1) return;
  if (cycleNum <= 1) return;

  var data = loadOverloadData();
  var history = loadOverloadHistory();
  var prevCycleKey = 'cycle' + (cycleNum - 1);
  var cards = document.querySelectorAll('.exercise-card');
  for (var c = 0; c < cards.length; c++) {
    var card = cards[c];
    var exKey = buildExerciseKey(card);
    var sets = card.querySelectorAll('.set-tracker .check-item');
    if (!history[exKey]) history[exKey] = {};
    if (!history[exKey][prevCycleKey]) history[exKey][prevCycleKey] = {};
    for (var s = 0; s < sets.length; s++) {
      var setKey = exKey + '::set' + (s + 1);
      history[exKey][prevCycleKey]['set' + (s + 1)] = {
        weight: data[setKey + '::weight'] || null,
        reps: data[setKey + '::reps'] || null,
        rir: data[setKey + '::rir'] || null
      };
    }
  }
  saveOverloadHistory(history);
  localStorage.setItem('workout-v4-last-archived-cycle', '' + (cycleNum - 1));
}

archiveCycleIfNeeded();
injectOverloadInputs();
addWeekBanner();

function exportCSV() {
  var weekNum = getWeekNumber();
  var cycleNum = Math.floor((weekNum - 1) / 3) + 1;
  var data = loadOverloadData();
  var rows = [['Day', 'Exercise', 'Set', 'Weight (kg)', 'Reps', 'RIR', 'Week', 'Cycle']];
  var dayNames = { 'day-mon': 'Day 1', 'day-tue': 'Day 2', 'day-wed': 'Day 3', 'day-thu': 'Day 4', 'day-fri': 'Day 5', 'day-sat': 'Day 6' };

  var cards = document.querySelectorAll('.exercise-card');
  for (var c = 0; c < cards.length; c++) {
    var card = cards[c];
    var section = card.closest('.day-section');
    var dayId = section ? section.id : '';
    var dayName = dayNames[dayId] || dayId;
    var name = getActiveExerciseName(card);
    var exKey = buildExerciseKey(card);
    var sets = card.querySelectorAll('.set-tracker .check-item');
    for (var s = 0; s < sets.length; s++) {
      var setKey = exKey + '::set' + (s + 1);
      var w = data[setKey + '::weight'];
      var r = data[setKey + '::reps'];
      var ri = data[setKey + '::rir'];
      if (w !== undefined || r !== undefined || ri !== undefined) {
        rows.push([dayName, name, 'Set ' + (s+1), w || '', r || '', ri || '', weekNum, cycleNum]);
      }
    }
  }

  if (rows.length === 1) { alert('No workout data to export yet.'); return; }
  var csv = rows.map(function(r) { return r.map(function(v) { return '"' + String(v).replace(/"/g, '""') + '"'; }).join(','); }).join('\\n');
  var blob = new Blob([csv], { type: 'text/csv' });
  var url = URL.createObjectURL(blob);
  var a = document.createElement('a');
  a.href = url; a.download = 'workout_v4_week' + weekNum + '.csv'; a.click();
  URL.revokeObjectURL(url);
}

function exportFullHistory() {
  var data = loadOverloadData();
  var history = loadOverloadHistory();
  var weekNum = getWeekNumber();
  var dayNames = { 'day-mon': 'Day 1', 'day-tue': 'Day 2', 'day-wed': 'Day 3', 'day-thu': 'Day 4', 'day-fri': 'Day 5', 'day-sat': 'Day 6' };
  var rows = [['Day', 'Exercise', 'Set', 'Cycle', 'Weight (kg)', 'Reps', 'RIR']];

  var cards = document.querySelectorAll('.exercise-card');
  for (var c = 0; c < cards.length; c++) {
    var card = cards[c];
    var section = card.closest('.day-section');
    var dayId = section ? section.id : '';
    var dayName = dayNames[dayId] || dayId;
    var name = getActiveExerciseName(card);
    var exKey = buildExerciseKey(card);
    var sets = card.querySelectorAll('.set-tracker .check-item');
    var exHistory = history[exKey] || {};
    var cycleKeys = Object.keys(exHistory).sort();
    for (var ck = 0; ck < cycleKeys.length; ck++) {
      var cycleData = exHistory[cycleKeys[ck]];
      var cycleLabel = cycleKeys[ck].replace('cycle', 'Cycle ');
      for (var s = 0; s < sets.length; s++) {
        var sd = cycleData['set' + (s + 1)];
        if (sd) rows.push([dayName, name, 'Set ' + (s+1), cycleLabel, sd.weight || '', sd.reps || '', sd.rir || '']);
      }
    }
    var currentCycle = Math.floor((weekNum - 1) / 3) + 1;
    for (var s2 = 0; s2 < sets.length; s2++) {
      var setKey = exKey + '::set' + (s2 + 1);
      var w = data[setKey + '::weight']; var r = data[setKey + '::reps']; var ri = data[setKey + '::rir'];
      if (w !== undefined || r !== undefined || ri !== undefined) {
        rows.push([dayName, name, 'Set ' + (s2+1), 'Cycle ' + currentCycle + ' (current)', w || '', r || '', ri || '']);
      }
    }
  }

  if (rows.length === 1) { alert('No data yet!'); return; }
  var csv = rows.map(function(r) { return r.map(function(v) { return '"' + String(v).replace(/"/g, '""') + '"'; }).join(','); }).join('\\n');
  var blob = new Blob([csv], { type: 'text/csv' });
  var url = URL.createObjectURL(blob); var a = document.createElement('a');
  a.href = url; a.download = 'workout_v4_full_history.csv'; a.click(); URL.revokeObjectURL(url);
}

function exportWeeklyLog() {
  var log = loadWeeklyLog();
  if (!log.length) { alert('No weekly log data yet. Data is saved when you reset a day.'); return; }
  var rows = [['Date', 'Time', 'Day', 'Week', 'Cycle', 'Exercise', 'Set', 'Completed', 'Weight (kg)', 'Reps', 'RIR']];
  for (var i = 0; i < log.length; i++) {
    var entry = log[i];
    for (var e = 0; e < entry.exercises.length; e++) {
      var ex = entry.exercises[e];
      for (var s = 0; s < ex.sets.length; s++) {
        var set = ex.sets[s];
        rows.push([entry.date, entry.time, entry.day, entry.week, entry.cycle, ex.name, 'Set ' + set.set, set.done ? 'Yes' : 'No', set.weight, set.reps, set.rir]);
      }
    }
  }
  var csv = rows.map(function(r) { return r.map(function(v) { return '"' + String(v).replace(/"/g, '""') + '"'; }).join(','); }).join('\\n');
  var blob = new Blob([csv], { type: 'text/csv' });
  var url = URL.createObjectURL(blob); var a = document.createElement('a');
  a.href = url; a.download = 'workout_v4_weekly_log.csv'; a.click(); URL.revokeObjectURL(url);
}

function resetWeek() {
  var sections = document.querySelectorAll('.day-section[id]');
  var hasData = false;
  for (var i = 0; i < sections.length; i++) {
    var cbs = sections[i].querySelectorAll('input[type="checkbox"]:checked');
    if (cbs.length > 0) { hasData = true; break; }
  }
  if (!hasData) { alert('No workout data to reset this week.'); return; }
  weekResetModal.classList.add('active');
}

function addExportButtons() {
  var bar = document.createElement('div');
  bar.className = 'export-bar';
  bar.innerHTML = '<button class="export-btn" onclick="exportCSV()">&#128229; Export This Week</button>' +
    '<button class="export-btn secondary" onclick="exportFullHistory()">&#128202; Export All History</button>' +
    '<button class="export-btn" style="background:linear-gradient(135deg,#7c3aed,#a855f7)" onclick="exportWeeklyLog()">&#128203; Export Weekly Log</button>' +
    '<button class="export-btn" style="background:linear-gradient(135deg,#dc2626,#ef4444);margin-top:6px;width:100%" onclick="resetWeek()">&#128260; Reset Entire Week</button>';
  var container = document.querySelector('.container');
  var firstSection = container.querySelector('.day-section');
  container.insertBefore(bar, firstSection);
}
addExportButtons();

function injectSetTags() {
  var cards = document.querySelectorAll('.exercise-card');
  for (var c = 0; c < cards.length; c++) {
    var card = cards[c];
    var meta = card.querySelector('.ex-meta');
    if (!meta) continue;
    var rirEl = meta.querySelector('.tag.rir');
    var rir = rirEl ? rirEl.textContent.trim() : '';
    var hasDrop = !!meta.querySelector('.tag.technique-drop');
    var hasFailure = !!meta.querySelector('.tag.technique-failure');
    var hasSuperset = !!meta.querySelector('.tag.technique-superset');
    var setItems = card.querySelectorAll('.set-tracker .check-item');
    var totalSets = setItems.length;
    for (var s = 0; s < totalSets; s++) {
      var span = setItems[s].querySelector('span');
      if (!span) continue;
      var tags = '';
      if (rir) tags += '<span class="set-tag rir">' + rir + '</span>';
      if (hasSuperset) tags += '<span class="set-tag superset">SUPERSET</span>';
      if (s === totalSets - 1) {
        if (hasDrop) tags += '<span class="set-tag drop">DROP</span>';
        if (hasFailure) tags += '<span class="set-tag failure">FAILURE</span>';
      }
      if (tags) span.innerHTML = span.innerHTML + ' ' + tags;
    }
  }
}
injectSetTags();

function addSetToExercise(btn) {
  var tracker = btn.closest('.set-tracker');
  if (!tracker) return;
  var card = tracker.closest('.exercise-card');
  if (!card) return;
  var checkItems = tracker.querySelectorAll('.check-item');
  var lastItem = checkItems[checkItems.length - 1];
  if (!lastItem) return;
  var newNum = checkItems.length + 1;
  var lastSpan = lastItem.querySelector('span');
  var lastText = lastSpan ? lastSpan.textContent.replace(/Set \\d+/, '').trim() : '';
  var repsText = lastText.replace(/^-\\s*/, '');
  var restDivs = tracker.querySelectorAll('.set-rest');
  var restText = 'Rest 60s';
  if (restDivs.length > 0) restText = restDivs[restDivs.length - 1].childNodes[0].textContent.trim();

  var meta = card.querySelector('.ex-meta');
  var rirEl = meta ? meta.querySelector('.tag.rir') : null;
  var rir = rirEl ? rirEl.textContent.trim() : '';
  var hasDrop = meta ? !!meta.querySelector('.tag.technique-drop') : false;
  var hasFailure = meta ? !!meta.querySelector('.tag.technique-failure') : false;
  var hasSuperset = meta ? !!meta.querySelector('.tag.technique-superset') : false;

  var oldLastTags = lastItem.querySelectorAll('.set-tag.drop, .set-tag.failure');
  for (var t = 0; t < oldLastTags.length; t++) oldLastTags[t].remove();

  var newRest = document.createElement('div');
  newRest.className = 'set-rest';
  newRest.textContent = restText;
  var restSecs = parseSeconds(restText);
  if (restSecs > 0) {
    var rbtn = document.createElement('span');
    rbtn.className = 'timer-btn'; rbtn.style.cursor = 'default'; rbtn.style.opacity = '0.7';
    rbtn.textContent = restSecs + 's';
    rbtn.setAttribute('data-seconds', restSecs);
    rbtn.setAttribute('data-label', 'Rest between sets');
    newRest.appendChild(rbtn);
  }

  var tags = '';
  if (rir) tags += ' <span class="set-tag rir">' + rir + '</span>';
  if (hasSuperset) tags += ' <span class="set-tag superset">SUPERSET</span>';
  if (hasDrop) tags += ' <span class="set-tag drop">DROP</span>';
  if (hasFailure) tags += ' <span class="set-tag failure">FAILURE</span>';

  var newItem = document.createElement('div');
  newItem.className = 'check-item';
  newItem.innerHTML = '<input type="checkbox"><span>Set ' + newNum + ' - ' + repsText + tags + '</span>';

  var exKey = buildExerciseKey(card);
  var setKey = exKey + '::set' + newNum;
  var data = loadOverloadData();
  var weekNum = getWeekNumber();
  var cycleWeek = getCycleWeek();
  var targetReps = getTargetReps(cycleWeek);
  var cycleNum = Math.floor((weekNum - 1) / 3) + 1;
  var history = loadOverloadHistory();
  var prevCycleKey = 'cycle' + (cycleNum - 1);
  var prev = (history[exKey] && history[exKey][prevCycleKey]) ? history[exKey][prevCycleKey] : null;

  var row = document.createElement('div');
  row.className = 'set-inputs';
  var weightLabel = document.createElement('label'); weightLabel.innerHTML = 'kg';
  var weightInput = document.createElement('input');
  weightInput.type = 'number'; weightInput.min = '0'; weightInput.step = '0.5'; weightInput.placeholder = '\\u2014';
  weightInput.setAttribute('data-key', setKey + '::weight');
  weightLabel.insertBefore(weightInput, weightLabel.firstChild);

  var repsLabel = document.createElement('label'); repsLabel.innerHTML = 'reps';
  var repsInput = document.createElement('input');
  repsInput.type = 'number'; repsInput.min = '0'; repsInput.step = '1'; repsInput.placeholder = targetReps;
  repsInput.setAttribute('data-key', setKey + '::reps');
  repsLabel.insertBefore(repsInput, repsLabel.firstChild);

  var rirLabel = document.createElement('label'); rirLabel.innerHTML = 'RIR';
  var rirInput = document.createElement('input');
  rirInput.type = 'number'; rirInput.min = '0'; rirInput.max = '5'; rirInput.step = '1'; rirInput.placeholder = '2';
  rirInput.setAttribute('data-key', setKey + '::rir');
  rirLabel.insertBefore(rirInput, rirLabel.firstChild);

  row.appendChild(weightLabel); row.appendChild(repsLabel); row.appendChild(rirLabel);
  if (prev && prev['set' + newNum]) {
    var prevInfo = document.createElement('span');
    prevInfo.className = 'set-prev';
    prevInfo.textContent = 'Prev: ' + (prev['set' + newNum].weight || '\\u2014') + 'kg \\u00d7 ' + (prev['set' + newNum].reps || '\\u2014');
    row.appendChild(prevInfo);
  }
  newItem.querySelector('span').appendChild(row);
  tracker.insertBefore(newRest, btn);
  tracker.insertBefore(newItem, btn);

  var tagSets = card.querySelector('.tag.sets');
  if (tagSets) {
    var match = tagSets.textContent.match(/^(\\d+)(\\s*x\\s*)(.*)/);
    if (match) tagSets.textContent = newNum + match[2] + match[3];
  }
  updateProgress(card.closest('.day-section'));
}

function injectAddSetButtons() {
  var trackers = document.querySelectorAll('.set-tracker');
  for (var i = 0; i < trackers.length; i++) {
    var addBtn = document.createElement('div');
    addBtn.className = 'add-set-btn';
    addBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg> Add Set';
    addBtn.addEventListener('click', function() { addSetToExercise(this); });
    trackers[i].appendChild(addBtn);
  }
}
injectAddSetButtons();

function injectTimerButtons() {
  var checkItems = document.querySelectorAll('.checklist .check-item span');
  for (var i = 0; i < checkItems.length; i++) {
    var span = checkItems[i];
    var prev = span.closest('.checklist').previousElementSibling;
    if (prev && prev.classList.contains('warmup')) continue;
    var text = span.textContent || '';
    var secs = parseSeconds(text);
    if (secs > 0) {
      var btn = document.createElement('span');
      btn.className = 'timer-btn'; btn.style.cursor = 'default'; btn.style.opacity = '0.7';
      btn.textContent = secs >= 60 ? Math.floor(secs/60) + 'm' : secs + 's';
      btn.setAttribute('data-seconds', secs);
      var labelText = text.split('\\n')[0].trim();
      if (labelText.length > 40) labelText = labelText.substring(0, 40) + '...';
      btn.setAttribute('data-label', labelText);
      var breathing = span.querySelector('.breathing-hint');
      if (breathing) span.insertBefore(btn, breathing);
      else span.appendChild(btn);
    }
  }

  var restItems = document.querySelectorAll('.set-rest');
  for (var j = 0; j < restItems.length; j++) {
    var rest = restItems[j];
    var restText = rest.textContent || '';
    var restSecs = parseSeconds(restText);
    if (restSecs > 0) {
      var rbtn = document.createElement('span');
      rbtn.className = 'timer-btn'; rbtn.style.cursor = 'default'; rbtn.style.opacity = '0.7';
      rbtn.textContent = restSecs + 's';
      rbtn.setAttribute('data-seconds', restSecs);
      rbtn.setAttribute('data-label', 'Rest between sets');
      rest.appendChild(rbtn);
    }
  }
}
injectTimerButtons();

// Exercise primary/alternate toggle
var EX_SEL_KEY = 'workout-v4-exercise-selection';

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
  if (choice === 'primary' && imgs.length > 1) imgs[1].classList.add('dimmed');
  else if (choice === 'alt' && imgs.length > 0) imgs[0].classList.add('dimmed');

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

</script>

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
print("\nDone! Open v4.html in your browser to test.")
