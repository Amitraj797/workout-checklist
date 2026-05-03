# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python script that generates a styled PDF workout plan (6-day push/pull split) with exercise images sourced from the [free-exercise-db](https://github.com/yuhonas/free-exercise-db). The script downloads exercise images on demand, caches them locally, and produces a multi-page A4 PDF with warm-ups, exercises (with alternates), cardio finishers, and cool-downs for each day.

## Running

```bash
python generate_workout_pdf.py
```

Dependencies: `fpdf2`, `Pillow`, `requests`. No requirements file exists — install manually via `pip install fpdf2 Pillow requests`.

Output: `Workout_Plan_6Day_Split.pdf`

## Architecture

- **`generate_workout_pdf.py`** — single-file project, everything lives here
- **`EXERCISE_MAP` dict** — maps display names (used in the PDF) to canonical names in the free-exercise-db. This is the main thing to edit when adding/changing exercises.
- **`WorkoutPDF` class** (extends `FPDF`) — handles all PDF layout: headers/footers, section titles, exercise cards with dual images (primary + alternate), warm-up/cooldown/cardio tables, and generic `simple_table`.
- **`build_pdf(db)`** — orchestrates the full PDF page-by-page. Each day's section is self-contained within this function.
- **Image pipeline**: `load_exercise_db()` fetches/caches the exercise JSON → `find_exercise()` does fuzzy name matching → `download_image()` fetches and thumbnails to 200x200 JPEG → `create_placeholder()` generates a labeled placeholder if download fails.
- **`exercise_images/`** — cached downloaded images and `exercises.json` (the full exercise DB). Safe to delete for a fresh download.
- **`exercise_urls.json`** — pre-resolved image URLs (reference/lookup, not used by the script).

## Key Patterns

- Every exercise in the PDF has a primary and an alternate, both with images. When adding an exercise, add entries for both the primary and alternate name in `EXERCISE_MAP`.
- Image filenames are derived from exercise display names with special characters stripped. Changing a display name in `EXERCISE_MAP` will cause a re-download.
- The exercise DB is cached to `exercise_images/exercises.json` — delete it to force a refresh from GitHub.
- Hardcoded absolute paths (`IMG_DIR`, `OUTPUT_PDF`) at the top of the file need updating if the project moves.
