import os
import json
import requests
from io import BytesIO
from PIL import Image
from fpdf import FPDF

EXERCISES_JSON_URL = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/dist/exercises.json"
IMAGE_BASE_URL = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/"
IMG_DIR = "/Users/amitraj/Desktop/Test/exercise_images"
OUTPUT_PDF = "/Users/amitraj/Desktop/Test/Workout_Plan_v3.pdf"

EXERCISE_MAP = {
    # Chest
    "Incline Dumbbell Press": "incline dumbbell press",
    "Flat Dumbbell Press": "dumbbell bench press",
    "Cable Fly (Mid/Low-to-High)": "cable crossover",
    "Incline Machine Press": "leverage incline chest press",
    "Chest Press Machine": "machine bench press",
    "Pec Deck": "butterfly",
    "DB Floor Press": "dumbbell floor press",

    # Triceps
    "Rope Pushdown": "triceps pushdown - rope attachment",
    "Overhead Rope Extension": "cable rope overhead triceps extension",
    "V-Bar Pushdown": "triceps pushdown - v-bar attachment",
    "Overhead Cable Extension": "triceps overhead extension with rope",
    "Single-Arm Cable Pushdown": "cable one arm tricep extension",
    "DB Overhead Extension": "standing dumbbell triceps extension",

    # Shoulders
    "Cable Lateral Raise": "one-arm side laterals",
    "DB Lateral Raise": "side lateral raise",
    "Machine Shoulder Press": "cable shoulder press",
    "Seated DB Press": "dumbbell shoulder press",
    "Rear Delt Cable Fly": "cable rear delt fly",
    "Seated Rear Delt Raise": "seated bent-over rear delt raise",

    # Back
    "Lat Pulldown": "close-grip front lat pulldown",
    "Assisted Pull-Up": "band assisted pull-up",
    "Chest-Supported Row": "dumbbell incline row",
    "Seated Cable Row": "seated cable rows",
    "Face Pulls": "face pull",
    "Reverse Pec Deck": "reverse machine flyes",
    "Machine Row": "leverage iso row",

    # Biceps
    "Incline Dumbbell Curl": "incline dumbbell curl",
    "Hammer Curl": "hammer curls",
    "Reverse Curl": "reverse barbell curl",
    "Cable Hammer Curl": "cable hammer curls - rope attachment",
    "Spider Curl": "spider curl",
    "Machine Preacher Curl": "machine preacher curls",
    "Concentration Curl": "concentration curls",
    "Preacher Curl Machine": "preacher curl",
    "DB Cross-Body Hammer Curl": "cross body hammer curl",
    "DB Hammer Curl": "alternate hammer curl",

    # Legs - Quads
    "Leg Press": "leg press",
    "Hack Squat": "hack squat",
    "Leg Extension": "leg extensions",
    "Walking Lunges": "bodyweight walking lunge",

    # Legs - Hamstrings/Glutes
    "Seated Leg Curl": "seated leg curl",
    "Lying Leg Curl": "lying leg curls",
    "Romanian Deadlift (RDL)": "romanian deadlift",
    "Cable Pull-Through": "band good morning (pull through)",
    "Hip Thrust": "barbell hip thrust",
    "Glute Bridge": "barbell glute bridge",
    "Bulgarian Split Squat": "split squats",
    "Reverse Lunge": "dumbbell rear lunge",

    # Calves
    "Standing Calf Raise": "standing calf raises",
    "Seated Calf Raise": "seated calf raise",
    "Leg Press Calf Raise": "calf press on the leg press machine",
    "DB Standing Calf Raise": "standing dumbbell calf raise",

    # Core
    "Dead Bug": "dead bug",
    "Reverse Crunch": "reverse crunch",
    "Pallof Press": "pallof press",
    "Banded Pallof Press": "pallof press with rotation",
    "Hanging Knee Raise": "hanging leg raise",
    "Cable Crunch": "cable crunch",
    "Captain's Chair Knee Raise": "knee/hip raise on parallel bars",
    "Ab Crunch Machine": "ab crunch machine",

    # Warm-Up
    "Shoulder rolls": "shoulder circles",
    "Band pull-aparts": "band pull apart",
    "Bodyweight squats": "bodyweight squat",
    "Glute bridges": "butt lift (bridge)",
    "Wall slides (scapular activation)": "scapular pull-up",
    "External rotations (light band/DB)": "external rotation with band",
    "Cat-cow mobility": "cat stretch",
    "Cat-cow": "cat stretch",
    "Scapular pulldown": "scapular pull-up",
    "Walking lunges (bodyweight)": "bodyweight walking lunge",
    "Band rows": "band pull apart",
    "Inchworms": "inchworm",
    "Leg swings (front-back + side-side)": "standing hip flexors",
    "Leg swings (front-back)": "standing hip flexors",
    "Leg swings": "standing hip flexors",
    "Hip mobility circles": "standing hip circles",
    "Single-leg glute bridge": "single leg glute bridge",
    "Dead hang": "hanging leg raise",
    "Light treadmill walk or cycling": "treadmill walking",
    "Cycling (easy pace)": "stationary bike",
    "Rowing machine or cycling": "rowing machine",

    # Stretches
    "Doorway chest stretch": "dynamic chest stretch",
    "Cross-body shoulder stretch": "shoulder stretch",
    "Overhead tricep stretch": "overhead triceps",
    "Child's pose stretch": "child's pose",
    "Seated hamstring stretch": "seated floor hamstring stretch",
    "Standing quad stretch": "all fours quad stretch",
    "Kneeling hip flexor stretch": "kneeling hip flexor",
    "Figure-4 glute stretch": "kettlebell figure 8",
    "Wall calf stretch": "calf stretch hands against wall",
    "Kneeling lat prayer stretch": "child's pose",
    "Wall bicep stretch": "standing biceps stretch",
    "Wrist flexor/forearm stretch": "kneeling forearm stretch",
    "Open book thoracic rotations": "torso rotation",
    "Child's pose": "child's pose",
    "Standing hip flexor stretch": "standing hip flexors",
    "Chest stretch": "behind head chest stretch",
    "Hamstring stretch": "hamstring stretch",
    "Plank": "plank",
}


def load_exercise_db():
    cache = os.path.join(IMG_DIR, "exercises.json")
    if os.path.exists(cache):
        with open(cache) as f:
            return json.load(f)
    r = requests.get(EXERCISES_JSON_URL)
    r.raise_for_status()
    data = r.json()
    os.makedirs(IMG_DIR, exist_ok=True)
    with open(cache, "w") as f:
        json.dump(data, f)
    return data


def find_exercise(db, name):
    name_lower = name.lower().strip()
    for ex in db:
        if ex["name"].lower() == name_lower:
            return ex
    for ex in db:
        if name_lower in ex["name"].lower() or ex["name"].lower() in name_lower:
            return ex
    return None


def download_raw_image(image_path):
    url = IMAGE_BASE_URL + image_path
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            img = Image.open(BytesIO(r.content))
            img = img.convert("RGBA")
            img.thumbnail((200, 200), Image.LANCZOS)
            return img
    except Exception as e:
        print(f"  Failed to download {url}: {e}")
    return None


def get_exercise_image(db, exercise_name):
    mapped = EXERCISE_MAP.get(exercise_name)
    if not mapped:
        mapped = exercise_name

    ex = find_exercise(db, mapped)
    if not ex or not ex.get("images"):
        return None

    safe_name = exercise_name.replace("/", "_").replace(" ", "_").replace("(", "").replace(")", "")

    gif_path = os.path.join(IMG_DIR, safe_name + ".gif")
    if os.path.exists(gif_path):
        return gif_path

    jpg_path = os.path.join(IMG_DIR, safe_name + ".jpg")
    if os.path.exists(jpg_path):
        return jpg_path

    frames = []
    for img_rel in ex["images"]:
        frame = download_raw_image(img_rel)
        if frame:
            frames.append(frame.convert("RGB"))

    if len(frames) >= 2:
        frames[0].save(
            gif_path, save_all=True, append_images=frames[1:],
            duration=700, loop=0, optimize=True,
        )
        return gif_path
    elif len(frames) == 1:
        frames[0].save(jpg_path, "JPEG", quality=80)
        return jpg_path
    return None


def create_placeholder(exercise_name):
    safe_name = exercise_name.replace("/", "_").replace(" ", "_").replace("(", "").replace(")", "")
    target = os.path.join(IMG_DIR, safe_name + "_placeholder.jpg")
    if os.path.exists(target):
        return target
    img = Image.new("RGB", (200, 200), (230, 235, 245))
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    draw.rectangle([5, 5, 195, 195], outline=(180, 190, 210), width=2)
    lines = exercise_name.split(" ")
    text_lines = []
    current = ""
    for w in lines:
        if len(current + " " + w) < 18:
            current = (current + " " + w).strip()
        else:
            if current:
                text_lines.append(current)
            current = w
    if current:
        text_lines.append(current)
    y = 80
    for line in text_lines:
        draw.text((20, y), line, fill=(100, 100, 120))
        y += 18
    img.save(target, "JPEG", quality=80)
    return target


class WorkoutPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 6, "6-Day Workout Plan  |  Push/Pull/Legs  |  Chest & Arm Focus", align="C")
            self.ln(4)
            self.set_draw_color(200, 200, 200)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title, r=30, g=60, b=120):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(r, g, b)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(r, g, b)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)
        self.set_text_color(0, 0, 0)

    def sub_title(self, title, r=50, g=50, b=50):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(r, g, b)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(1)

    def bullet(self, text):
        self.set_font("Helvetica", "", 9)
        self.multi_cell(0, 5, "  - " + text)
        self.ln(0.5)

    def _technique_badge(self, x, y, label):
        colors = {
            "DROP": (240, 160, 40),
            "FAILURE": (220, 50, 50),
            "SUPERSET": (130, 60, 180),
        }
        for tag in ["DROP", "FAILURE", "SUPERSET"]:
            if tag in label:
                self.set_font("Helvetica", "B", 6)
                tw = self.get_string_width(tag) + 3
                r, g, b = colors[tag]
                self.set_fill_color(r, g, b)
                self.set_xy(x, y)
                self.set_text_color(255, 255, 255)
                self.cell(tw, 4, tag, fill=True, align="C")
                x += tw + 1.5
        self.set_text_color(0, 0, 0)
        return x

    def exercise_with_image(self, num, name, alternate, sets, rest, rir, technique, note, img_path, alt_img_path):
        IMG_W = 22
        IMG_H = 22

        needed_h = IMG_H + 22
        if self.get_y() + needed_h > self.h - 15:
            self.add_page()

        y_start = self.get_y()

        self.set_fill_color(240, 245, 255)
        self.rect(10, y_start, 190, needed_h, "F")
        self.set_draw_color(200, 210, 230)
        self.rect(10, y_start, 190, needed_h, "D")

        self.set_xy(12, y_start + 2)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(30, 60, 120)
        self.cell(8, 8, str(num))

        self.set_xy(22, y_start + 2)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(0, 0, 0)
        self.cell(80, 5, name)

        if technique:
            self._technique_badge(104, y_start + 2, technique)

        self.set_xy(22, y_start + 7)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(30, 100, 30)
        self.cell(30, 5, sets)
        self.set_text_color(120, 120, 120)
        self.set_font("Helvetica", "", 8)
        self.cell(20, 5, "Rest: " + rest)
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(180, 50, 50)
        self.cell(20, 5, "RIR: " + rir)

        self.set_xy(22, y_start + 12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 80, 30)
        self.cell(5, 5, "Alt: ")
        self.set_font("Helvetica", "", 8)
        self.cell(80, 5, alternate)

        if note:
            self.set_xy(22, y_start + 17)
            self.set_font("Helvetica", "I", 7)
            self.set_text_color(80, 80, 100)
            self.multi_cell(90, 3.5, note)

        if img_path and os.path.exists(img_path):
            self.image(img_path, x=125, y=y_start + 2, w=IMG_W, h=IMG_H)
        else:
            self.set_draw_color(200, 200, 200)
            self.rect(125, y_start + 2, IMG_W, IMG_H, "D")
            self.set_xy(126, y_start + 10)
            self.set_font("Helvetica", "I", 6)
            self.set_text_color(180, 180, 180)
            self.cell(IMG_W - 2, 4, "Primary", align="C")

        self.set_xy(125, y_start + IMG_H + 3)
        self.set_font("Helvetica", "", 5.5)
        self.set_text_color(80, 80, 80)
        self.cell(IMG_W, 3, "Primary", align="C")

        if alt_img_path and os.path.exists(alt_img_path):
            self.image(alt_img_path, x=152, y=y_start + 2, w=IMG_W, h=IMG_H)
        else:
            self.set_draw_color(200, 200, 200)
            self.rect(152, y_start + 2, IMG_W, IMG_H, "D")
            self.set_xy(153, y_start + 10)
            self.set_font("Helvetica", "I", 6)
            self.set_text_color(180, 180, 180)
            self.cell(IMG_W - 2, 4, "Alternate", align="C")

        self.set_xy(152, y_start + IMG_H + 3)
        self.set_font("Helvetica", "", 5.5)
        self.set_text_color(150, 80, 30)
        self.cell(IMG_W, 3, "Alternate", align="C")

        self.set_draw_color(220, 225, 235)
        self.line(12, y_start + needed_h, 198, y_start + needed_h)

        self.set_xy(10, y_start + needed_h + 1)
        self.set_text_color(0, 0, 0)

    def superset_block(self, ex1_args, ex2_args, get_img):
        CARD_H = 22 + 22
        LABEL_H = 6
        total_h = LABEL_H + CARD_H * 2 + 2

        if self.get_y() + total_h > self.h - 15:
            self.add_page()

        block_y = self.get_y()

        self.set_fill_color(245, 240, 255)
        self.rect(10, block_y, 190, total_h, "F")

        self.set_draw_color(130, 60, 180)
        self.set_line_width(1.2)
        self.rect(10, block_y, 190, total_h, "D")
        self.set_line_width(0.2)

        self.set_draw_color(130, 60, 180)
        self.set_line_width(2)
        self.line(10, block_y, 10, block_y + total_h)
        self.set_line_width(0.2)

        self.set_xy(14, block_y + 1)
        self.set_font("Helvetica", "B", 7)
        self.set_fill_color(130, 60, 180)
        self.set_text_color(255, 255, 255)
        self.cell(22, 4.5, "SUPERSET", fill=True, align="C")
        self.set_text_color(0, 0, 0)

        self.set_xy(10, block_y + LABEL_H)
        num, name, alt, sets, rest, rir, technique, note = ex1_args
        self.exercise_with_image(num, name, alt, sets, rest, rir, technique, note, get_img(name), get_img(alt))

        num, name, alt, sets, rest, rir, technique, note = ex2_args
        self.exercise_with_image(num, name, alt, sets, rest, rir, technique, note, get_img(name), get_img(alt))

        self.set_xy(10, block_y + total_h + 1)

    def warmup_table_with_images(self, exercises, get_img):
        IMG_W = 14
        IMG_H = 14
        ROW_H = max(IMG_H + 2, 8)
        widths_text = [8, 72, 72]
        total_text_w = sum(widths_text)

        self.set_fill_color(80, 130, 80)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 8)
        for w, h in zip([8, 72, 72, 38], ["#", "Exercise", "Duration / Reps", "Image"]):
            self.cell(w, 7, h, border=1, fill=True, align="C")
        self.ln()
        self.set_text_color(0, 0, 0)

        for i, ex in enumerate(exercises):
            if self.get_y() + ROW_H > self.h - 15:
                self.add_page()
            y_start = self.get_y()
            self.set_font("Helvetica", "", 7.5)
            if i % 2 == 0:
                self.set_fill_color(240, 248, 240)
            else:
                self.set_fill_color(255, 255, 255)
            x_start = self.get_x()
            for w, c in zip(widths_text, ex):
                self.cell(w, ROW_H, c, border=1, fill=True)
            img_x = x_start + total_text_w
            self.cell(38, ROW_H, "", border=1, fill=True)
            img_path = get_img(ex[1])
            if img_path and os.path.exists(img_path):
                self.image(img_path, x=img_x + 12, y=y_start + 1, w=IMG_W, h=IMG_H)
            self.ln()
        self.ln(2)

    def cooldown_table_with_images(self, exercises, get_img):
        IMG_W = 14
        IMG_H = 14
        ROW_H = max(IMG_H + 2, 8)
        widths_text = [8, 82, 62]
        total_text_w = sum(widths_text)

        self.set_fill_color(100, 100, 140)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 8)
        for w, h in zip([8, 82, 62, 38], ["#", "Exercise", "Duration", "Image"]):
            self.cell(w, 7, h, border=1, fill=True, align="C")
        self.ln()
        self.set_text_color(0, 0, 0)

        for i, ex in enumerate(exercises):
            if self.get_y() + ROW_H > self.h - 15:
                self.add_page()
            y_start = self.get_y()
            self.set_font("Helvetica", "", 7.5)
            if i % 2 == 0:
                self.set_fill_color(240, 240, 250)
            else:
                self.set_fill_color(255, 255, 255)
            x_start = self.get_x()
            for w, c in zip(widths_text, ex):
                self.cell(w, ROW_H, c, border=1, fill=True)
            img_x = x_start + total_text_w
            self.cell(38, ROW_H, "", border=1, fill=True)
            img_path = get_img(ex[1])
            if img_path and os.path.exists(img_path):
                self.image(img_path, x=img_x + 12, y=y_start + 1, w=IMG_W, h=IMG_H)
            self.ln()
        self.ln(2)

    def cardio_table(self, exercises):
        widths = [70, 40, 80]
        headers = ["Exercise", "Duration", "Notes"]
        self.set_fill_color(180, 80, 50)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 8)
        for w, h in zip(widths, headers):
            self.cell(w, 7, h, border=1, fill=True, align="C")
        self.ln()
        self.set_text_color(0, 0, 0)
        for i, ex in enumerate(exercises):
            self.set_font("Helvetica", "", 7.5)
            self.set_fill_color(255, 245, 240)
            for w, c in zip(widths, ex):
                self.cell(w, 6, c, border=1, fill=True)
            self.ln()
        self.ln(2)

    def simple_table(self, widths, headers, rows, fill_color=(30, 60, 120)):
        self.set_fill_color(*fill_color)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 8)
        for w, h in zip(widths, headers):
            self.cell(w, 7, h, border=1, fill=True, align="C")
        self.ln()
        self.set_text_color(0, 0, 0)
        for i, row in enumerate(rows):
            self.set_font("Helvetica", "", 7.5)
            if i % 2 == 0:
                self.set_fill_color(240, 245, 255)
            else:
                self.set_fill_color(255, 255, 255)
            for w, c in zip(widths, row):
                self.cell(w, 6, c, border=1, fill=True)
            self.ln()
        self.ln(2)


def build_pdf(db):
    pdf = WorkoutPDF()
    pdf.alias_nb_pages()

    def get_img(name):
        return get_exercise_image(db, name) or create_placeholder(name)

    # ===== COVER PAGE =====
    pdf.add_page()
    pdf.ln(30)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(30, 60, 120)
    pdf.cell(0, 15, "6-DAY WORKOUT PLAN", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 16)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 10, "Push / Pull / Legs  |  Chest & Arm Focus", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)
    pdf.set_draw_color(30, 60, 120)
    pdf.set_line_width(0.8)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.set_line_width(0.2)
    pdf.ln(10)

    pdf.simple_table(
        [60, 130],
        ["Detail", "Value"],
        [
            ["Body Fat", "~27-29%"],
            ["Primary Goal", "Build chest size + Increase arm/forearm size"],
            ["Secondary Goal", "Reduce belly fat + Improve aesthetics"],
            ["Concerns", "Tailbone discomfort (cardio), Posterior knee discomfort"],
            ["Focus", "Body recomposition + Hypertrophy"],
            ["Equipment", "Full Gym"],
            ["Schedule", "Mon-Sat (Thu Active Recovery, Sun Full Rest)"],
        ],
        fill_color=(50, 80, 140),
    )
    pdf.ln(5)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, "Injury-aware | Sustainable progression | Every exercise has an alternate", align="C")

    # ===== TRAINING RULES =====
    pdf.add_page()
    pdf.section_title("IMPORTANT TRAINING RULES", 180, 50, 50)
    pdf.ln(2)

    pdf.sub_title("Failure Training Rules")
    pdf.bullet("Compound exercises: Stop at 1-2 reps before failure (Incline DB press, Leg press, RDL, Chest-supported row)")
    pdf.bullet("Isolation exercises: Final set can safely go to failure (Cable fly, Pec deck, Lateral raise, Pushdowns, Curls)")
    pdf.ln(2)

    pdf.sub_title("Drop Set Rules")
    pdf.bullet("Use drop sets ONLY on the final set")
    pdf.bullet("Best for: Cable lateral raise, Pec deck, Rope pushdowns, Cable curls, Hammer curls, Leg extension")
    pdf.bullet("Do NOT drop set: RDL, Leg press, Heavy DB presses, Hip thrusts")
    pdf.ln(2)

    pdf.sub_title("Superset Rules")
    pdf.bullet("Use supersets mainly for isolation exercises and time efficiency")
    pdf.bullet("Avoid supersets on heavy compound lifts")
    pdf.ln(2)

    pdf.sub_title("Injury Awareness")
    for t in [
        "Tailbone: Avoid excessive stairmaster / intense incline treadmill after leg day",
        "Tailbone: Cycling and moderate incline walking are preferred cardio options",
        "Posterior knee: Choose pain-free leg press/hack squat option",
        "Posterior knee: Replace Bulgarian split squat with leg press if discomfort",
        "General: Do NOT ego lift. Train most sets 1-2 reps before failure",
    ]:
        pdf.bullet(t)
    pdf.ln(3)

    pdf.section_title("WEEKLY OVERVIEW")
    pdf.simple_table(
        [30, 60, 40, 30],
        ["Day", "Focus", "Type", "Time"],
        [
            ["Monday", "Push A (Chest Strength)", "Strength", "~75 min"],
            ["Tuesday", "Legs + Shoulders A", "Hypertrophy", "~80 min"],
            ["Wednesday", "Pull A (Back + Biceps)", "Strength", "~75 min"],
            ["Thursday", "Active Recovery", "Mobility", "~30 min"],
            ["Friday", "Push B (Chest Hypertrophy)", "Volume", "~75 min"],
            ["Saturday", "Legs + Pull B", "Hypertrophy", "~80 min"],
            ["Sunday", "FULL REST", "-", "-"],
        ],
    )
    pdf.ln(1)
    pdf.sub_title("Rep Range Guide")
    pdf.simple_table(
        [60, 40, 90],
        ["Exercise Type", "Rep Range", "Rest Time"],
        [
            ["Heavy compound", "6-10 reps", "90-120 sec"],
            ["Hypertrophy", "10-15 reps", "60-90 sec"],
            ["Isolation", "12-15 reps", "45-75 sec"],
        ],
        fill_color=(50, 80, 140),
    )

    pdf.ln(2)
    pdf.section_title("HOW TO READ EACH EXERCISE CARD")
    pdf.ln(1)

    pdf.simple_table(
        [35, 155],
        ["Element", "What It Means"],
        [
            ["Sets x Reps", "e.g. 4 x 6-10 = 4 sets of 6-10 reps"],
            ["Rest", "How long to rest between sets"],
            ["RIR", "Reps In Reserve = how many reps you could still do. RIR 2 = stop 2 reps before failure"],
            ["Alt", "Alternate exercise you can swap in (same muscle, different movement)"],
        ],
        fill_color=(50, 80, 140),
    )

    pdf.ln(2)
    pdf.sub_title("Intensity Technique Tags")

    pdf.set_fill_color(240, 160, 40)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 7)
    pdf.cell(14, 5, "DROP", fill=True, align="C")
    pdf.set_text_color(60, 60, 60)
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(170, 5, "  Drop Set = on last set, reduce weight 30-40% and immediately do more reps (no rest)")
    pdf.ln(6)

    pdf.set_fill_color(220, 50, 50)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 7)
    pdf.cell(20, 5, "FAILURE", fill=True, align="C")
    pdf.set_text_color(60, 60, 60)
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(164, 5, "  Go to Failure = on last set, keep going until you can't do another rep with good form")
    pdf.ln(6)

    pdf.set_fill_color(130, 60, 180)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 7)
    pdf.cell(22, 5, "SUPERSET", fill=True, align="C")
    pdf.set_text_color(60, 60, 60)
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(162, 5, "  Superset = do both exercises back-to-back with no rest between them")
    pdf.ln(8)
    pdf.set_text_color(0, 0, 0)

    # ===================================================================
    #              MONDAY - Push A (Chest Strength Focus)
    # ===================================================================
    pdf.add_page()
    pdf.section_title("MONDAY - Push A (Chest Strength Focus)", 30, 60, 120)

    pdf.sub_title("Warm-Up (8-10 min)", 80, 130, 80)
    pdf.warmup_table_with_images([
        ["1", "Light treadmill walk or cycling", "5 min"],
        ["2", "Shoulder rolls", "10 reps"],
        ["3", "Band pull-aparts", "15 reps"],
        ["4", "Wall slides (scapular activation)", "10 reps"],
        ["5", "External rotations (light band/DB)", "12 reps each"],
    ], get_img)

    pdf.sub_title("Chest + Shoulders (2 exercises + 1 superset)", 30, 60, 120)
    chest_mon = [
        (1, "Incline Dumbbell Press", "Incline Machine Press", "4 x 6-10", "90-120s", "1-2", "", "Priority chest movement. Controlled eccentric."),
        (2, "Flat Dumbbell Press", "Chest Press Machine", "3 x 8-10", "90s", "1-2", "", "Controlled stretch at bottom."),
    ]
    for num, name, alt, sets, rest, rir, technique, note in chest_mon:
        pdf.exercise_with_image(num, name, alt, sets, rest, rir, technique, note, get_img(name), get_img(alt))

    pdf.ln(2)
    pdf.superset_block(
        ("3A", "Cable Fly (Mid/Low-to-High)", "Pec Deck", "3 x 12-15", "60s", "2", "SUPERSET", "Slow eccentric. Squeeze at peak contraction."),
        ("3B", "Cable Lateral Raise", "DB Lateral Raise", "3 x 12-15", "60s", "1-2", "SUPERSET", "Focus on side delts. Light weight, strict form."),
        get_img,
    )

    pdf.ln(3)
    pdf.sub_title("Triceps (2 exercises - Superset)", 30, 60, 120)
    pdf.ln(2)
    pdf.superset_block(
        ("4A", "Rope Pushdown", "V-Bar Pushdown", "3 x 12-15", "60s", "1-2", "SUPERSET", "Elbows pinned. Full extension."),
        ("4B", "Overhead Rope Extension", "Single-Arm Cable Pushdown", "3 x 12-15", "60s", "1-2", "SUPERSET", "Long head stretch. Controlled movement."),
        get_img,
    )

    pdf.ln(3)
    pdf.sub_title("Cardio (15-20 min)", 180, 80, 50)
    pdf.cardio_table([
        ["Incline treadmill walk or cycling", "15-20 min", "HR target: 120-140 BPM"],
    ])

    pdf.sub_title("Stretching", 100, 100, 140)
    pdf.cooldown_table_with_images([
        ["1", "Doorway chest stretch", "30s each side"],
        ["2", "Overhead tricep stretch", "30s each side"],
        ["3", "Cross-body shoulder stretch", "30s each side"],
        ["4", "Child's pose stretch", "45s"],
    ], get_img)

    # ===================================================================
    #        TUESDAY - Legs + Shoulders A
    # ===================================================================
    pdf.add_page()
    pdf.section_title("TUESDAY - Legs + Shoulders A", 30, 60, 120)

    pdf.sub_title("Warm-Up (8-10 min)", 80, 130, 80)
    pdf.warmup_table_with_images([
        ["1", "Cycling (easy pace)", "5 min"],
        ["2", "Leg swings (front-back + side-side)", "10 each leg"],
        ["3", "Bodyweight squats", "15 reps"],
        ["4", "Glute bridges", "15 reps"],
        ["5", "Walking lunges (bodyweight)", "10 each leg"],
        ["6", "Cat-cow mobility", "10 reps"],
    ], get_img)

    pdf.sub_title("Legs (3 exercises)", 30, 60, 120)
    legs_tue = [
        (1, "Leg Press", "Hack Squat", "4 x 8-12", "90-120s", "1-2", "", "Choose pain-free option for knee. Depth over weight."),
        (2, "Seated Leg Curl", "Lying Leg Curl", "3 x 10-12", "60s", "1-2", "", "Controlled tempo. Full ROM."),
        (3, "Leg Extension", "Walking Lunges", "3 x 12-15", "60s", "1", "DROP", "Last set drop set. Controlled reps, squeeze at top."),
    ]
    for num, name, alt, sets, rest, rir, technique, note in legs_tue:
        pdf.exercise_with_image(num, name, alt, sets, rest, rir, technique, note, get_img(name), get_img(alt))

    pdf.ln(3)
    pdf.sub_title("Shoulders (1 exercise)", 30, 60, 120)
    shldr_tue = [
        (4, "Machine Shoulder Press", "Seated DB Press", "3 x 8-10", "90s", "1-2", "", "Shoulder-safe pressing. No barbell overhead."),
    ]
    for num, name, alt, sets, rest, rir, technique, note in shldr_tue:
        pdf.exercise_with_image(num, name, alt, sets, rest, rir, technique, note, get_img(name), get_img(alt))

    pdf.ln(3)
    pdf.sub_title("Calves (2 exercises)", 30, 60, 120)
    calves_tue = [
        (5, "Standing Calf Raise", "Leg Press Calf Raise", "3 x 12-15", "45s", "1-2", "", "Full stretch at bottom, pause at top."),
        (6, "Seated Calf Raise", "DB Standing Calf Raise", "2-3 x 12-15", "45s", "1-2", "", "Targets soleus. 2x/week calf frequency."),
    ]
    for num, name, alt, sets, rest, rir, technique, note in calves_tue:
        pdf.exercise_with_image(num, name, alt, sets, rest, rir, technique, note, get_img(name), get_img(alt))

    pdf.ln(3)
    pdf.sub_title("Core (2 exercises)", 30, 60, 120)
    core_tue = [
        (7, "Dead Bug", "Reverse Crunch", "2 x 10 each side", "45s", "2", "", "Deep core activation. No spinal stress."),
        (8, "Pallof Press", "Banded Pallof Press", "2 x 10 each side", "45s", "2", "", "Anti-rotation. Builds core stability."),
    ]
    for num, name, alt, sets, rest, rir, technique, note in core_tue:
        pdf.exercise_with_image(num, name, alt, sets, rest, rir, technique, note, get_img(name), get_img(alt))

    pdf.ln(3)
    pdf.sub_title("Cardio (5-10 min)", 180, 80, 50)
    pdf.cardio_table([
        ["Easy cycling (or skip)", "5-10 min", "Very light only. NO intense incline treadmill."],
    ])

    pdf.sub_title("Stretching", 100, 100, 140)
    pdf.cooldown_table_with_images([
        ["1", "Seated hamstring stretch", "30s each side"],
        ["2", "Standing quad stretch", "30s each side"],
        ["3", "Kneeling hip flexor stretch", "30s each side"],
        ["4", "Figure-4 glute stretch", "30s each side"],
        ["5", "Wall calf stretch", "30s each side"],
    ], get_img)

    # ===================================================================
    #            WEDNESDAY - Pull A (Back Width + Biceps)
    # ===================================================================
    pdf.add_page()
    pdf.section_title("WEDNESDAY - Pull A (Back Width + Biceps)", 30, 60, 120)

    pdf.sub_title("Warm-Up (8-10 min)", 80, 130, 80)
    pdf.warmup_table_with_images([
        ["1", "Rowing machine or cycling", "5 min"],
        ["2", "Scapular pulldown", "12 reps"],
        ["3", "Band rows", "15 reps"],
        ["4", "Cat-cow", "10 reps"],
        ["5", "Dead hang", "15 sec"],
    ], get_img)

    pdf.sub_title("Back (2 exercises)", 30, 60, 120)
    back_wed = [
        (1, "Lat Pulldown", "Assisted Pull-Up", "4 x 8-12", "90s", "1-2", "", "Squeeze shoulder blades. Full stretch at top."),
        (2, "Chest-Supported Row", "Seated Cable Row", "3 x 8-12", "90s", "1-2", "", "Lower-back friendly. Pull to lower chest."),
    ]
    for num, name, alt, sets, rest, rir, technique, note in back_wed:
        pdf.exercise_with_image(num, name, alt, sets, rest, rir, technique, note, get_img(name), get_img(alt))

    pdf.ln(3)
    pdf.sub_title("Back + Biceps (2 supersets)", 30, 60, 120)
    pdf.ln(2)
    pdf.superset_block(
        ("3A", "Face Pulls", "Reverse Pec Deck", "3 x 12-15", "60s", "2", "SUPERSET", "Pull to forehead. Great for posture + rear delts."),
        ("3B", "Hammer Curl", "Cable Hammer Curl", "3 x 10-12", "60s", "1-2", "SUPERSET", "Forearm + brachialis focus. No swinging."),
        get_img,
    )

    pdf.ln(2)
    pdf.superset_block(
        ("4A", "Incline Dumbbell Curl", "Machine Preacher Curl", "3 x 10-12", "60s", "1-2", "SUPERSET", "Deep stretch. Light weight."),
        ("4B", "Reverse Curl", "DB Hammer Curl", "2-3 x 12-15", "60s", "2", "SUPERSET", "Forearm thickness. Strict form."),
        get_img,
    )

    pdf.ln(3)
    pdf.sub_title("Cardio (15-20 min)", 180, 80, 50)
    pdf.cardio_table([
        ["Cycling or incline treadmill walk", "15-20 min", "Moderate intensity only."],
    ])

    pdf.sub_title("Stretching", 100, 100, 140)
    pdf.cooldown_table_with_images([
        ["1", "Kneeling lat prayer stretch", "30s"],
        ["2", "Wall bicep stretch", "30s each side"],
        ["3", "Wrist flexor/forearm stretch", "20s each"],
        ["4", "Seated hamstring stretch", "30s each side"],
        ["5", "Child's pose stretch", "45s"],
    ], get_img)

    # ===================================================================
    #         THURSDAY - Active Recovery
    # ===================================================================
    pdf.add_page()
    pdf.section_title("THURSDAY - Active Recovery", 100, 140, 80)
    pdf.ln(2)
    pdf.sub_title("Recovery Work")
    for t in [
        "20-30 minutes easy walking OR easy cycling",
        "No heavy lifting",
        "Focus on recovery, mobility, and flexibility",
    ]:
        pdf.bullet(t)
    pdf.ln(3)

    pdf.sub_title("Mobility Routine")
    pdf.simple_table(
        [8, 110, 72],
        ["#", "Exercise", "Duration"],
        [
            ["1", "Seated hamstring stretch", "30 sec each side"],
            ["2", "Kneeling hip flexor stretch", "30 sec each side"],
            ["3", "Figure-4 glute stretch", "30 sec each side"],
            ["4", "Wall calf stretch", "30 sec each side"],
            ["5", "Cat-cow", "10 reps"],
            ["6", "Child's pose stretch", "45 sec"],
            ["7", "Open book thoracic rotations", "10 each side"],
        ],
        fill_color=(100, 140, 80),
    )

    pdf.ln(5)
    pdf.sub_title("Key Reminders")
    for t in [
        "This day is essential for recovery and muscle growth",
        "Keep heart rate low - this is NOT a cardio day",
        "Hydrate well - 3+ liters of water",
        "Prioritize sleep (7-8 hours)",
        "Meal prep for the rest of the week",
    ]:
        pdf.bullet(t)

    # ===================================================================
    #           FRIDAY - Push B (Chest Hypertrophy Focus)
    # ===================================================================
    pdf.add_page()
    pdf.section_title("FRIDAY - Push B (Chest Hypertrophy Focus)", 30, 60, 120)

    pdf.sub_title("Warm-Up (8-10 min)", 80, 130, 80)
    pdf.warmup_table_with_images([
        ["1", "Light treadmill walk or cycling", "5 min"],
        ["2", "Shoulder rolls", "10 reps"],
        ["3", "Band pull-aparts", "15 reps"],
        ["4", "Wall slides (scapular activation)", "10 reps"],
        ["5", "External rotations (light band/DB)", "12 reps each"],
    ], get_img)

    pdf.sub_title("Chest (3 exercises + 1 superset)", 30, 60, 120)
    chest_fri = [
        (1, "Incline Machine Press", "Incline Dumbbell Press", "4 x 8-12", "90s", "1-2", "", "Machine for stability. Focus on squeeze."),
        (2, "Chest Press Machine", "Flat Dumbbell Press", "3 x 10-12", "60s", "2", "", "Controlled reps. Mind-muscle connection."),
        (3, "Flat Dumbbell Press", "DB Floor Press", "2-3 x 8-10", "60s", "1-2", "", "Additional chest overload. Controlled stretch."),
    ]
    for num, name, alt, sets, rest, rir, technique, note in chest_fri:
        pdf.exercise_with_image(num, name, alt, sets, rest, rir, technique, note, get_img(name), get_img(alt))

    pdf.ln(2)
    pdf.superset_block(
        ("4A", "Pec Deck", "Cable Fly (Mid/Low-to-High)", "3 x 12-15", "60s", "1", "SUPERSET", "Controlled squeeze."),
        ("4B", "Cable Lateral Raise", "DB Lateral Raise", "3 x 12-15", "60s", "1-2", "SUPERSET", "Side delt isolation."),
        get_img,
    )

    pdf.ln(3)
    pdf.sub_title("Triceps (2 exercises - Superset)", 30, 60, 120)
    pdf.ln(2)
    pdf.superset_block(
        ("5A", "V-Bar Pushdown", "Rope Pushdown", "3 x 12-15", "60s", "1-2", "SUPERSET", "Focus on contraction. Full lockout."),
        ("5B", "Overhead Cable Extension", "DB Overhead Extension", "3 x 12-15", "60s", "1-2", "SUPERSET", "Long head stretch. Controlled."),
        get_img,
    )

    pdf.ln(3)
    pdf.sub_title("Cardio (15-20 min)", 180, 80, 50)
    pdf.cardio_table([
        ["Moderate cycling (preferred)", "15-20 min", "Cycling preferred over treadmill."],
    ])

    pdf.sub_title("Stretching", 100, 100, 140)
    pdf.cooldown_table_with_images([
        ["1", "Doorway chest stretch", "30s each side"],
        ["2", "Cross-body shoulder stretch", "30s each side"],
        ["3", "Overhead tricep stretch", "30s each side"],
    ], get_img)

    # ===================================================================
    #       SATURDAY - Legs + Pull B
    # ===================================================================
    pdf.add_page()
    pdf.section_title("SATURDAY - Legs + Pull B", 30, 60, 120)

    pdf.sub_title("Warm-Up (8-10 min)", 80, 130, 80)
    pdf.warmup_table_with_images([
        ["1", "Cycling (easy pace)", "5 min"],
        ["2", "Glute bridges", "15 reps"],
        ["3", "Leg swings (front-back)", "10 each leg"],
        ["4", "Bodyweight squats", "15 reps"],
        ["5", "Hip mobility circles", "10 each direction"],
    ], get_img)

    pdf.sub_title("Legs - Posterior Chain (3 exercises)", 30, 60, 120)
    legs_sat = [
        (1, "Romanian Deadlift (RDL)", "Cable Pull-Through", "3 x 8-10", "90-120s", "1-2", "", "Controlled form. Hinge at hips. Do NOT go to failure."),
        (2, "Hip Thrust", "Glute Bridge", "3 x 10-12", "90s", "1-2", "", "Pad the bar. Full glute squeeze at top."),
        (3, "Bulgarian Split Squat", "Reverse Lunge", "2-3 x 10 each", "60s", "2", "", "Replace with leg press if knee discomfort."),
    ]
    for num, name, alt, sets, rest, rir, technique, note in legs_sat:
        pdf.exercise_with_image(num, name, alt, sets, rest, rir, technique, note, get_img(name), get_img(alt))

    pdf.ln(3)
    pdf.sub_title("Back (1 exercise)", 30, 60, 120)
    back_sat = [
        (4, "Seated Cable Row", "Machine Row", "3 x 10-12", "60s", "1-2", "", "Extra upper/mid-back work for posture support."),
    ]
    for num, name, alt, sets, rest, rir, technique, note in back_sat:
        pdf.exercise_with_image(num, name, alt, sets, rest, rir, technique, note, get_img(name), get_img(alt))

    pdf.ln(3)
    pdf.sub_title("Back + Biceps (Superset)", 30, 60, 120)
    pdf.ln(2)
    pdf.superset_block(
        ("5A", "Rear Delt Cable Fly", "Seated Rear Delt Raise", "3 x 12-15", "60s", "2", "SUPERSET", "Rear delt + posture. Light weight."),
        ("5B", "Spider Curl", "Preacher Curl Machine", "3 x 10-12", "60s", "1-2", "SUPERSET", "Strict form, no momentum."),
        get_img,
    )

    pdf.ln(3)
    pdf.sub_title("Biceps (1 exercise)", 30, 60, 120)
    bi_sat = [
        (6, "Incline Dumbbell Curl", "Concentration Curl", "2 x 10-12", "60s", "2", "", "Stretch-focused. Fuller long-head development."),
    ]
    for num, name, alt, sets, rest, rir, technique, note in bi_sat:
        pdf.exercise_with_image(num, name, alt, sets, rest, rir, technique, note, get_img(name), get_img(alt))

    pdf.ln(3)
    pdf.sub_title("Biceps + Calves (Superset)", 30, 60, 120)
    pdf.ln(2)
    pdf.superset_block(
        ("7A", "Cable Hammer Curl", "DB Cross-Body Hammer Curl", "2-3 x 12", "60s", "1-2", "SUPERSET", "Forearm + brachialis focus."),
        ("7B", "Seated Calf Raise", "DB Standing Calf Raise", "2-3 x 12-15", "45s", "1-2", "SUPERSET", "Targets soleus. Paired for time efficiency."),
        get_img,
    )

    pdf.ln(3)
    pdf.sub_title("Core (2 exercises)", 30, 60, 120)
    core_sat = [
        (8, "Hanging Knee Raise", "Captain's Chair Knee Raise", "2-3 x 10", "45s", "2", "", "Controlled - no swinging."),
        (9, "Cable Crunch", "Ab Crunch Machine", "2-3 x 12-15", "45s", "2", "", "Squeeze at bottom. Upper abs focus."),
    ]
    for num, name, alt, sets, rest, rir, technique, note in core_sat:
        pdf.exercise_with_image(num, name, alt, sets, rest, rir, technique, note, get_img(name), get_img(alt))

    pdf.ln(3)
    pdf.sub_title("Cardio (5-10 min)", 180, 80, 50)
    pdf.cardio_table([
        ["Easy walk only (optional)", "5-10 min", "NO intense cardio. Recovery priority."],
    ])

    pdf.sub_title("Stretching", 100, 100, 140)
    pdf.cooldown_table_with_images([
        ["1", "Seated hamstring stretch", "30s each side"],
        ["2", "Figure-4 glute stretch", "30s each side"],
        ["3", "Kneeling hip flexor stretch", "30s each side"],
        ["4", "Child's pose stretch", "45s"],
        ["5", "Wall calf stretch", "30s each side"],
    ], get_img)

    # ===================================================================
    #              SUNDAY + OVERLOAD + NUTRITION
    # ===================================================================
    pdf.add_page()
    pdf.section_title("SUNDAY - Full Rest", 100, 140, 80)
    pdf.ln(2)
    for t in [
        "Focus on recovery, mobility, hydration, and sleep",
        "Optional: Easy walking or light stretching",
        "Meal preparation for the week ahead",
        "Hydrate - 3-4 liters of water",
        "Sleep - aim for 7-8 hours",
        "No gym work",
    ]:
        pdf.bullet(t)
    pdf.ln(5)

    pdf.section_title("PROGRESSIVE OVERLOAD RULES")
    pdf.ln(1)
    pdf.bullet("Very important for chest and arm growth")
    pdf.ln(1)
    pdf.simple_table(
        [30, 160],
        ["Phase", "What to Do"],
        [
            ["Week 1", "e.g. 15kg DB x 8 reps - Learn movements, focus on form"],
            ["Week 2", "e.g. 15kg DB x 10 reps - Add reps with same weight"],
            ["Week 3", "e.g. 17.5kg DB x 8 reps - Increase weight, reset reps"],
            ["Ongoing", "Small progression over time builds muscle. Patience is key."],
            ["Every 6-8 wks", "Deload week - reduce weight, sets, and intensity for 1 week"],
        ],
    )

    pdf.ln(3)
    pdf.section_title("NUTRITION TARGETS")
    pdf.simple_table(
        [35, 45, 110],
        ["Macro", "Daily Target", "Notes"],
        [
            ["Calories", "1,900-2,200 kcal", "Adjust based on progress"],
            ["Protein", "120-140g/day", "Very important for muscle growth (~2g/kg)"],
            ["Water", "3-4 liters", "More if sweating heavily"],
        ],
    )

    pdf.ln(3)
    pdf.section_title("CARDIO RULES", 180, 80, 50)
    pdf.simple_table(
        [90, 100],
        ["Best Options", "Avoid"],
        [
            ["Cycling", "Excessive HIIT"],
            ["Incline walk (moderate)", "Long stairmaster sessions"],
            ["Elliptical", "Intense incline treadmill after leg day"],
        ],
        fill_color=(180, 80, 50),
    )

    pdf.ln(3)
    pdf.section_title("WARNING SIGNS - Reduce Volume If:", 180, 50, 50)
    pdf.simple_table(
        [80, 110],
        ["Warning Sign", "Action"],
        [
            ["Sharp pain", "Stop immediately - switch to alternate"],
            ["Worsening knee pain", "Switch to pain-free variant or skip"],
            ["Severe tailbone pain", "Change cardio modality (try cycling)"],
            ["Strength drops continuously", "Consider deload or extra rest day"],
            ["Fatigue becomes excessive", "Reduce volume/intensity, check sleep"],
            ["Sleep worsens badly", "Scale back training, prioritize recovery"],
        ],
        fill_color=(180, 50, 50),
    )

    pdf.ln(5)
    pdf.section_title("EXPECTED RESULTS TIMELINE")
    pdf.simple_table(
        [40, 150],
        ["Timeline", "Expected Changes"],
        [
            ["8-12 weeks", "Better chest fullness, slight waist reduction, improved arm size, better stamina"],
            ["4-6 months", "Noticeable physique transformation, reduced belly fat, better shoulder/chest separation"],
            ["6-10 months", "Body fat near 15-17%, strong aesthetic improvement, leaner waist, visible muscularity"],
        ],
        fill_color=(50, 100, 80),
    )

    pdf.output(OUTPUT_PDF)
    return OUTPUT_PDF


def collect_all_exercises():
    days = []

    days.append({
        "title": "MONDAY - Push A (Chest Strength Focus)",
        "color": "#1e3c78",
        "warmup": [
            ("Light treadmill walk or cycling", "5 min"),
            ("Shoulder rolls", "10 reps"),
            ("Band pull-aparts", "15 reps"),
            ("Wall slides (scapular activation)", "10 reps"),
            ("External rotations (light band/DB)", "12 reps each"),
        ],
        "sections": [
            ("Chest", [
                {"num": 1, "name": "Incline Dumbbell Press", "alt": "Incline Machine Press", "sets": "4 x 6-10", "rest": "90-120s", "rir": "1-2", "technique": "", "note": "Priority chest movement. Controlled eccentric."},
                {"num": 2, "name": "Flat Dumbbell Press", "alt": "Chest Press Machine", "sets": "3 x 8-10", "rest": "90s", "rir": "1-2", "technique": "", "note": "Controlled stretch at bottom."},
            ]),
            ("Chest + Shoulders (Superset)", [
                {"num": "3A", "name": "Cable Fly (Mid/Low-to-High)", "alt": "Pec Deck", "sets": "3 x 12-15", "rest": "60s", "rir": "2", "technique": "SUPERSET", "note": "Slow eccentric. Squeeze at peak contraction.", "superset": True},
                {"num": "3B", "name": "Cable Lateral Raise", "alt": "DB Lateral Raise", "sets": "3 x 12-15", "rest": "60s", "rir": "1-2", "technique": "SUPERSET", "note": "Focus on side delts. Light weight, strict form.", "superset": True},
            ]),
            ("Triceps (Superset)", [
                {"num": "4A", "name": "Rope Pushdown", "alt": "V-Bar Pushdown", "sets": "3 x 12-15", "rest": "60s", "rir": "1-2", "technique": "SUPERSET", "note": "Elbows pinned. Full extension.", "superset": True},
                {"num": "4B", "name": "Overhead Rope Extension", "alt": "Single-Arm Cable Pushdown", "sets": "3 x 12-15", "rest": "60s", "rir": "1-2", "technique": "SUPERSET", "note": "Long head stretch. Controlled movement.", "superset": True},
            ]),
        ],
        "cardio": ("Incline treadmill walk or cycling", "15-20 min", "HR target: 120-140 BPM"),
        "stretches": [
            ("Doorway chest stretch", "30s each side"),
            ("Overhead tricep stretch", "30s each side"),
            ("Cross-body shoulder stretch", "30s each side"),
            ("Child's pose stretch", "45s"),
        ],
    })

    days.append({
        "title": "TUESDAY - Legs + Shoulders A",
        "color": "#1e3c78",
        "warmup": [
            ("Cycling (easy pace)", "5 min"),
            ("Leg swings (front-back + side-side)", "10 each leg"),
            ("Bodyweight squats", "15 reps"),
            ("Glute bridges", "15 reps"),
            ("Walking lunges (bodyweight)", "10 each leg"),
            ("Cat-cow mobility", "10 reps"),
        ],
        "sections": [
            ("Legs", [
                {"num": 1, "name": "Leg Press", "alt": "Hack Squat", "sets": "4 x 8-12", "rest": "90-120s", "rir": "1-2", "technique": "", "note": "Choose pain-free option for knee."},
                {"num": 2, "name": "Seated Leg Curl", "alt": "Lying Leg Curl", "sets": "3 x 10-12", "rest": "60s", "rir": "1-2", "technique": "", "note": "Controlled tempo. Full ROM."},
                {"num": 3, "name": "Leg Extension", "alt": "Walking Lunges", "sets": "3 x 12-15", "rest": "60s", "rir": "1", "technique": "DROP", "note": "Last set drop set. Squeeze at top."},
            ]),
            ("Shoulders", [
                {"num": 4, "name": "Machine Shoulder Press", "alt": "Seated DB Press", "sets": "3 x 8-10", "rest": "90s", "rir": "1-2", "technique": "", "note": "Shoulder-safe pressing."},
            ]),
            ("Calves", [
                {"num": 5, "name": "Standing Calf Raise", "alt": "Leg Press Calf Raise", "sets": "3 x 12-15", "rest": "45s", "rir": "1-2", "technique": "", "note": "Full stretch at bottom."},
                {"num": 6, "name": "Seated Calf Raise", "alt": "DB Standing Calf Raise", "sets": "2-3 x 12-15", "rest": "45s", "rir": "1-2", "technique": "", "note": "Targets soleus."},
            ]),
            ("Core", [
                {"num": 7, "name": "Dead Bug", "alt": "Reverse Crunch", "sets": "2 x 10 each side", "rest": "45s", "rir": "2", "technique": "", "note": "Deep core activation."},
                {"num": 8, "name": "Pallof Press", "alt": "Banded Pallof Press", "sets": "2 x 10 each side", "rest": "45s", "rir": "2", "technique": "", "note": "Anti-rotation."},
            ]),
        ],
        "cardio": ("Easy cycling (or skip)", "5-10 min", "Very light only. NO intense incline treadmill."),
        "stretches": [
            ("Seated hamstring stretch", "30s each side"),
            ("Standing quad stretch", "30s each side"),
            ("Kneeling hip flexor stretch", "30s each side"),
            ("Figure-4 glute stretch", "30s each side"),
            ("Wall calf stretch", "30s each side"),
        ],
    })

    days.append({
        "title": "WEDNESDAY - Pull A (Back Width + Biceps)",
        "color": "#1e3c78",
        "warmup": [
            ("Rowing machine or cycling", "5 min"),
            ("Scapular pulldown", "12 reps"),
            ("Band rows", "15 reps"),
            ("Cat-cow", "10 reps"),
            ("Dead hang", "15 sec"),
        ],
        "sections": [
            ("Back", [
                {"num": 1, "name": "Lat Pulldown", "alt": "Assisted Pull-Up", "sets": "4 x 8-12", "rest": "90s", "rir": "1-2", "technique": "", "note": "Squeeze shoulder blades."},
                {"num": 2, "name": "Chest-Supported Row", "alt": "Seated Cable Row", "sets": "3 x 8-12", "rest": "90s", "rir": "1-2", "technique": "", "note": "Lower-back friendly."},
            ]),
            ("Back + Biceps (Superset 1)", [
                {"num": "3A", "name": "Face Pulls", "alt": "Reverse Pec Deck", "sets": "3 x 12-15", "rest": "60s", "rir": "2", "technique": "SUPERSET", "note": "Pull to forehead. Posture + rear delts.", "superset": True},
                {"num": "3B", "name": "Hammer Curl", "alt": "Cable Hammer Curl", "sets": "3 x 10-12", "rest": "60s", "rir": "1-2", "technique": "SUPERSET", "note": "Forearm + brachialis focus.", "superset": True},
            ]),
            ("Biceps (Superset 2)", [
                {"num": "4A", "name": "Incline Dumbbell Curl", "alt": "Machine Preacher Curl", "sets": "3 x 10-12", "rest": "60s", "rir": "1-2", "technique": "SUPERSET", "note": "Deep stretch. Light weight.", "superset": True},
                {"num": "4B", "name": "Reverse Curl", "alt": "DB Hammer Curl", "sets": "2-3 x 12-15", "rest": "60s", "rir": "2", "technique": "SUPERSET", "note": "Forearm thickness.", "superset": True},
            ]),
        ],
        "cardio": ("Cycling or incline treadmill walk", "15-20 min", "Moderate intensity only."),
        "stretches": [
            ("Kneeling lat prayer stretch", "30s"),
            ("Wall bicep stretch", "30s each side"),
            ("Wrist flexor/forearm stretch", "20s each"),
            ("Seated hamstring stretch", "30s each side"),
            ("Child's pose stretch", "45s"),
        ],
    })

    days.append({
        "title": "THURSDAY - Active Recovery",
        "color": "#648c50",
        "warmup": [],
        "sections": [],
        "cardio": None,
        "stretches": [],
        "recovery": True,
        "mobility": [
            ("Seated hamstring stretch", "30 sec each side"),
            ("Kneeling hip flexor stretch", "30 sec each side"),
            ("Figure-4 glute stretch", "30 sec each side"),
            ("Wall calf stretch", "30 sec each side"),
            ("Cat-cow", "10 reps"),
            ("Child's pose stretch", "45 sec"),
            ("Open book thoracic rotations", "10 each side"),
        ],
    })

    days.append({
        "title": "FRIDAY - Push B (Chest Hypertrophy Focus)",
        "color": "#1e3c78",
        "warmup": [
            ("Light treadmill walk or cycling", "5 min"),
            ("Shoulder rolls", "10 reps"),
            ("Band pull-aparts", "15 reps"),
            ("Wall slides (scapular activation)", "10 reps"),
            ("External rotations (light band/DB)", "12 reps each"),
        ],
        "sections": [
            ("Chest", [
                {"num": 1, "name": "Incline Machine Press", "alt": "Incline Dumbbell Press", "sets": "4 x 8-12", "rest": "90s", "rir": "1-2", "technique": "", "note": "Machine for stability."},
                {"num": 2, "name": "Chest Press Machine", "alt": "Flat Dumbbell Press", "sets": "3 x 10-12", "rest": "60s", "rir": "2", "technique": "", "note": "Mind-muscle connection."},
                {"num": 3, "name": "Flat Dumbbell Press", "alt": "DB Floor Press", "sets": "2-3 x 8-10", "rest": "60s", "rir": "1-2", "technique": "", "note": "Additional chest overload."},
            ]),
            ("Chest + Shoulders (Superset)", [
                {"num": "4A", "name": "Pec Deck", "alt": "Cable Fly (Mid/Low-to-High)", "sets": "3 x 12-15", "rest": "60s", "rir": "1", "technique": "SUPERSET", "note": "Controlled squeeze.", "superset": True},
                {"num": "4B", "name": "Cable Lateral Raise", "alt": "DB Lateral Raise", "sets": "3 x 12-15", "rest": "60s", "rir": "1-2", "technique": "SUPERSET", "note": "Side delt isolation.", "superset": True},
            ]),
            ("Triceps (Superset)", [
                {"num": "5A", "name": "V-Bar Pushdown", "alt": "Rope Pushdown", "sets": "3 x 12-15", "rest": "60s", "rir": "1-2", "technique": "SUPERSET", "note": "Full lockout.", "superset": True},
                {"num": "5B", "name": "Overhead Cable Extension", "alt": "DB Overhead Extension", "sets": "3 x 12-15", "rest": "60s", "rir": "1-2", "technique": "SUPERSET", "note": "Long head stretch.", "superset": True},
            ]),
        ],
        "cardio": ("Moderate cycling (preferred)", "15-20 min", "Cycling preferred over treadmill."),
        "stretches": [
            ("Doorway chest stretch", "30s each side"),
            ("Cross-body shoulder stretch", "30s each side"),
            ("Overhead tricep stretch", "30s each side"),
        ],
    })

    days.append({
        "title": "SATURDAY - Legs + Pull B",
        "color": "#1e3c78",
        "warmup": [
            ("Cycling (easy pace)", "5 min"),
            ("Glute bridges", "15 reps"),
            ("Leg swings (front-back)", "10 each leg"),
            ("Bodyweight squats", "15 reps"),
            ("Hip mobility circles", "10 each direction"),
        ],
        "sections": [
            ("Legs - Posterior Chain", [
                {"num": 1, "name": "Romanian Deadlift (RDL)", "alt": "Cable Pull-Through", "sets": "3 x 8-10", "rest": "90-120s", "rir": "1-2", "technique": "", "note": "Do NOT go to failure."},
                {"num": 2, "name": "Hip Thrust", "alt": "Glute Bridge", "sets": "3 x 10-12", "rest": "90s", "rir": "1-2", "technique": "", "note": "Full glute squeeze at top."},
                {"num": 3, "name": "Bulgarian Split Squat", "alt": "Reverse Lunge", "sets": "2-3 x 10 each", "rest": "60s", "rir": "2", "technique": "", "note": "Replace with leg press if knee discomfort."},
            ]),
            ("Back", [
                {"num": 4, "name": "Seated Cable Row", "alt": "Machine Row", "sets": "3 x 10-12", "rest": "60s", "rir": "1-2", "technique": "", "note": "Posture support."},
            ]),
            ("Back + Biceps (Superset)", [
                {"num": "5A", "name": "Rear Delt Cable Fly", "alt": "Seated Rear Delt Raise", "sets": "3 x 12-15", "rest": "60s", "rir": "2", "technique": "SUPERSET", "note": "Rear delt + posture. Light weight.", "superset": True},
                {"num": "5B", "name": "Spider Curl", "alt": "Preacher Curl Machine", "sets": "3 x 10-12", "rest": "60s", "rir": "1-2", "technique": "SUPERSET", "note": "Strict form, no momentum.", "superset": True},
            ]),
            ("Biceps", [
                {"num": 6, "name": "Incline Dumbbell Curl", "alt": "Concentration Curl", "sets": "2 x 10-12", "rest": "60s", "rir": "2", "technique": "", "note": "Stretch-focused."},
            ]),
            ("Biceps + Calves (Superset)", [
                {"num": "7A", "name": "Cable Hammer Curl", "alt": "DB Cross-Body Hammer Curl", "sets": "2-3 x 12", "rest": "60s", "rir": "1-2", "technique": "SUPERSET", "note": "Forearm + brachialis focus.", "superset": True},
                {"num": "7B", "name": "Seated Calf Raise", "alt": "DB Standing Calf Raise", "sets": "2-3 x 12-15", "rest": "45s", "rir": "1-2", "technique": "SUPERSET", "note": "Targets soleus. Paired for time efficiency.", "superset": True},
            ]),
            ("Core", [
                {"num": 8, "name": "Hanging Knee Raise", "alt": "Captain's Chair Knee Raise", "sets": "2-3 x 10", "rest": "45s", "rir": "2", "technique": "", "note": "Controlled."},
                {"num": 9, "name": "Cable Crunch", "alt": "Ab Crunch Machine", "sets": "2-3 x 12-15", "rest": "45s", "rir": "2", "technique": "", "note": "Upper abs focus."},
            ]),
        ],
        "cardio": ("Easy walk only (optional)", "5-10 min", "NO intense cardio."),
        "stretches": [
            ("Seated hamstring stretch", "30s each side"),
            ("Figure-4 glute stretch", "30s each side"),
            ("Kneeling hip flexor stretch", "30s each side"),
            ("Child's pose stretch", "45s"),
            ("Wall calf stretch", "30s each side"),
        ],
    })

    return days


def build_html(db, days):
    import base64

    def get_img(name):
        return get_exercise_image(db, name) or create_placeholder(name)

    def img_to_data_uri(path):
        if not path or not os.path.exists(path):
            return ""
        ext = path.rsplit(".", 1)[-1].lower()
        mime = "image/gif" if ext == "gif" else "image/jpeg"
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f"data:{mime};base64,{data}"

    def badge_html(technique):
        badges = ""
        colors = {"DROP": "#f0a028", "FAILURE": "#dc3232", "SUPERSET": "#823cb4"}
        for tag in ["DROP", "FAILURE", "SUPERSET"]:
            if tag in technique:
                badges += f'<span class="badge" style="background:{colors[tag]}">{tag}</span> '
        return badges

    html_parts = []
    html_parts.append("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>6-Day Workout Plan v3</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f1117; color: #e0e0e0; line-height: 1.5; }
.container { max-width: 1000px; margin: 0 auto; padding: 20px; }
h1 { text-align: center; font-size: 2.2em; color: #6ea8fe; margin: 30px 0 5px; }
.subtitle { text-align: center; color: #888; font-size: 1.1em; margin-bottom: 30px; }
.day-card { background: #1a1d27; border-radius: 12px; margin-bottom: 24px; overflow: hidden; border: 1px solid #2a2d37; }
.day-header { padding: 16px 24px; font-size: 1.3em; font-weight: bold; color: #fff; }
.day-body { padding: 0 24px 24px; }
.section-title { font-size: 1.1em; font-weight: 600; color: #6ea8fe; margin: 18px 0 10px; border-bottom: 1px solid #2a2d37; padding-bottom: 6px; }
.exercise-card { display: flex; align-items: center; background: #22252f; border-radius: 8px; margin-bottom: 8px; padding: 12px 16px; gap: 16px; border-left: 3px solid #3a6fd8; }
.exercise-card.superset { border-left-color: #823cb4; background: #25213a; }
.ex-num { font-size: 1.4em; font-weight: bold; color: #6ea8fe; min-width: 32px; text-align: center; }
.ex-info { flex: 1; min-width: 0; }
.ex-name { font-weight: 600; font-size: 1em; color: #fff; }
.ex-meta { font-size: 0.85em; color: #aaa; margin-top: 2px; }
.ex-meta .sets { color: #4caf50; font-weight: 600; }
.ex-meta .rir { color: #e53935; font-weight: 600; }
.ex-alt { font-size: 0.82em; color: #c77d30; margin-top: 2px; }
.ex-note { font-size: 0.8em; color: #7a7a9a; font-style: italic; margin-top: 2px; }
.badge { display: inline-block; padding: 1px 7px; border-radius: 3px; font-size: 0.7em; font-weight: bold; color: #fff; vertical-align: middle; margin-left: 4px; }
.ex-images { display: flex; gap: 8px; flex-shrink: 0; }
.ex-images img { width: 80px; height: 80px; object-fit: cover; border-radius: 6px; border: 2px solid #333; background: #1a1d27; }
.ex-images .img-label { text-align: center; font-size: 0.65em; color: #888; margin-top: 2px; }
.warmup-table, .stretch-table, .mobility-table { width: 100%; border-collapse: collapse; margin: 8px 0; }
.warmup-table th, .stretch-table th, .mobility-table th { background: #2a3a2a; color: #8bc34a; padding: 6px 10px; text-align: left; font-size: 0.85em; }
.warmup-table td, .stretch-table td, .mobility-table td { padding: 5px 10px; border-bottom: 1px solid #2a2d37; font-size: 0.85em; vertical-align: middle; }
.table-img { width: 50px; height: 50px; object-fit: cover; border-radius: 4px; border: 1px solid #333; }
.stretch-table th { background: #2a2a3a; color: #9575cd; }
.mobility-table th { background: #2a3a2a; color: #8bc34a; }
.cardio-box { background: #2a1a14; border: 1px solid #5d3522; border-radius: 8px; padding: 10px 16px; margin: 8px 0; font-size: 0.9em; }
.cardio-box strong { color: #ff8a50; }
.recovery-info { padding: 16px; background: #1a2a1a; border-radius: 8px; margin: 10px 0; }
.recovery-info li { margin: 6px 0; color: #8bc34a; }
.superset-label { display: inline-block; background: #823cb4; color: #fff; padding: 2px 10px; border-radius: 4px; font-size: 0.75em; font-weight: bold; margin-bottom: 6px; }
.info-section { background: #1a1d27; border-radius: 12px; margin-bottom: 24px; padding: 24px; border: 1px solid #2a2d37; }
.info-section h2 { color: #6ea8fe; margin-bottom: 12px; }
.info-table { width: 100%; border-collapse: collapse; margin: 10px 0; }
.info-table th { background: #1e3c78; color: #fff; padding: 8px 12px; text-align: left; font-size: 0.9em; }
.info-table td { padding: 7px 12px; border-bottom: 1px solid #2a2d37; font-size: 0.85em; }
.info-table tr:nth-child(even) td { background: #1f2230; }
.warning-table th { background: #7a2020 !important; }
.timeline-table th { background: #1a4a32 !important; }
</style>
</head>
<body>
<div class="container">
<h1>6-DAY WORKOUT PLAN</h1>
<p class="subtitle">Push / Pull / Legs &nbsp;|&nbsp; Chest & Arm Focus</p>
""")

    for day in days:
        is_recovery = day.get("recovery", False)
        html_parts.append(f'<div class="day-card">')
        html_parts.append(f'<div class="day-header" style="background:{day["color"]}">{day["title"]}</div>')
        html_parts.append(f'<div class="day-body">')

        if is_recovery:
            html_parts.append('<div class="recovery-info"><ul>')
            html_parts.append('<li>20-30 minutes easy walking OR easy cycling</li>')
            html_parts.append('<li>No heavy lifting</li>')
            html_parts.append('<li>Focus on recovery, mobility, and flexibility</li>')
            html_parts.append('</ul></div>')
            html_parts.append('<div class="section-title">Mobility Routine</div>')
            html_parts.append('<table class="mobility-table"><tr><th>#</th><th>Exercise</th><th>Duration</th><th>Demo</th></tr>')
            for i, (ex, dur) in enumerate(day.get("mobility", [])):
                mob_uri = img_to_data_uri(get_img(ex))
                img_cell = f'<img src="{mob_uri}" class="table-img">' if mob_uri else ""
                html_parts.append(f'<tr><td>{i+1}</td><td>{ex}</td><td>{dur}</td><td>{img_cell}</td></tr>')
            html_parts.append('</table>')
        else:
            if day["warmup"]:
                html_parts.append('<div class="section-title" style="color:#8bc34a">Warm-Up</div>')
                html_parts.append('<table class="warmup-table"><tr><th>#</th><th>Exercise</th><th>Duration</th><th>Demo</th></tr>')
                for i, (ex, dur) in enumerate(day["warmup"]):
                    wu_uri = img_to_data_uri(get_img(ex))
                    img_cell = f'<img src="{wu_uri}" class="table-img">' if wu_uri else ""
                    html_parts.append(f'<tr><td>{i+1}</td><td>{ex}</td><td>{dur}</td><td>{img_cell}</td></tr>')
                html_parts.append('</table>')

            for sec_name, exercises in day["sections"]:
                is_superset_section = any(e.get("superset") for e in exercises)
                html_parts.append(f'<div class="section-title">{sec_name}</div>')
                if is_superset_section:
                    html_parts.append('<span class="superset-label">SUPERSET</span>')

                for ex in exercises:
                    is_ss = ex.get("superset", False)
                    card_class = "exercise-card superset" if is_ss else "exercise-card"
                    primary_path = get_img(ex["name"])
                    alt_path = get_img(ex["alt"])
                    primary_uri = img_to_data_uri(primary_path)
                    alt_uri = img_to_data_uri(alt_path)

                    html_parts.append(f'<div class="{card_class}">')
                    html_parts.append(f'<div class="ex-num">{ex["num"]}</div>')
                    html_parts.append(f'<div class="ex-info">')
                    html_parts.append(f'<div class="ex-name">{ex["name"]} {badge_html(ex["technique"])}</div>')
                    html_parts.append(f'<div class="ex-meta"><span class="sets">{ex["sets"]}</span> &nbsp; Rest: {ex["rest"]} &nbsp; <span class="rir">RIR: {ex["rir"]}</span></div>')
                    html_parts.append(f'<div class="ex-alt">Alt: {ex["alt"]}</div>')
                    if ex["note"]:
                        html_parts.append(f'<div class="ex-note">{ex["note"]}</div>')
                    html_parts.append('</div>')
                    html_parts.append('<div class="ex-images">')
                    if primary_uri:
                        html_parts.append(f'<div><img src="{primary_uri}" alt="{ex["name"]}"><div class="img-label">Primary</div></div>')
                    if alt_uri:
                        html_parts.append(f'<div><img src="{alt_uri}" alt="{ex["alt"]}"><div class="img-label">Alternate</div></div>')
                    html_parts.append('</div></div>')

            if day["cardio"]:
                c_ex, c_dur, c_note = day["cardio"]
                html_parts.append(f'<div class="section-title" style="color:#ff8a50">Cardio</div>')
                html_parts.append(f'<div class="cardio-box"><strong>{c_ex}</strong> - {c_dur} &nbsp; <em>{c_note}</em></div>')

            if day["stretches"]:
                html_parts.append('<div class="section-title" style="color:#9575cd">Stretching</div>')
                html_parts.append('<table class="stretch-table"><tr><th>#</th><th>Exercise</th><th>Duration</th><th>Demo</th></tr>')
                for i, (ex, dur) in enumerate(day["stretches"]):
                    st_uri = img_to_data_uri(get_img(ex))
                    img_cell = f'<img src="{st_uri}" class="table-img">' if st_uri else ""
                    html_parts.append(f'<tr><td>{i+1}</td><td>{ex}</td><td>{dur}</td><td>{img_cell}</td></tr>')
                html_parts.append('</table>')

        html_parts.append('</div></div>')

    html_parts.append("""
<div class="info-section">
<h2>Progressive Overload Rules</h2>
<table class="info-table">
<tr><th>Phase</th><th>What to Do</th></tr>
<tr><td>Week 1</td><td>e.g. 15kg DB x 8 reps - Learn movements, focus on form</td></tr>
<tr><td>Week 2</td><td>e.g. 15kg DB x 10 reps - Add reps with same weight</td></tr>
<tr><td>Week 3</td><td>e.g. 17.5kg DB x 8 reps - Increase weight, reset reps</td></tr>
<tr><td>Ongoing</td><td>Small progression over time builds muscle. Patience is key.</td></tr>
<tr><td>Every 6-8 wks</td><td>Deload week - reduce weight, sets, and intensity for 1 week</td></tr>
</table>
</div>

<div class="info-section">
<h2>Nutrition Targets</h2>
<table class="info-table">
<tr><th>Macro</th><th>Daily Target</th><th>Notes</th></tr>
<tr><td>Calories</td><td>1,900-2,200 kcal</td><td>Adjust based on progress</td></tr>
<tr><td>Protein</td><td>120-140g/day</td><td>Very important for muscle growth (~2g/kg)</td></tr>
<tr><td>Water</td><td>3-4 liters</td><td>More if sweating heavily</td></tr>
</table>
</div>

<div class="info-section">
<h2>Warning Signs</h2>
<table class="info-table warning-table">
<tr><th>Warning Sign</th><th>Action</th></tr>
<tr><td>Sharp pain</td><td>Stop immediately - switch to alternate</td></tr>
<tr><td>Worsening knee pain</td><td>Switch to pain-free variant or skip</td></tr>
<tr><td>Severe tailbone pain</td><td>Change cardio modality (try cycling)</td></tr>
<tr><td>Strength drops continuously</td><td>Consider deload or extra rest day</td></tr>
<tr><td>Fatigue becomes excessive</td><td>Reduce volume/intensity, check sleep</td></tr>
<tr><td>Sleep worsens badly</td><td>Scale back training, prioritize recovery</td></tr>
</table>
</div>

<div class="info-section">
<h2>Expected Results Timeline</h2>
<table class="info-table timeline-table">
<tr><th>Timeline</th><th>Expected Changes</th></tr>
<tr><td>8-12 weeks</td><td>Better chest fullness, slight waist reduction, improved arm size, better stamina</td></tr>
<tr><td>4-6 months</td><td>Noticeable physique transformation, reduced belly fat, better shoulder/chest separation</td></tr>
<tr><td>6-10 months</td><td>Body fat near 15-17%, strong aesthetic improvement, leaner waist, visible muscularity</td></tr>
</table>
</div>

</div>
</body>
</html>""")

    html_path = os.path.join(os.path.dirname(OUTPUT_PDF), "v3.html")
    with open(html_path, "w") as f:
        f.write("\n".join(html_parts))
    return html_path


def main():
    os.makedirs(IMG_DIR, exist_ok=True)
    print("Loading exercise database...")
    db = load_exercise_db()
    print(f"Loaded {len(db)} exercises from database")

    print("Downloading exercise images (animated GIFs)...")
    print("Building PDF...")
    pdf_path = build_pdf(db)
    print(f"PDF generated: {pdf_path}")

    print("Building HTML with animated exercise images...")
    days = collect_all_exercises()
    html_path = build_html(db, days)
    print(f"HTML generated: {html_path}")

    gif_count = len([f for f in os.listdir(IMG_DIR) if f.endswith(".gif")])
    jpg_count = len([f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")])
    print(f"Images: {gif_count} animated GIFs, {jpg_count} static JPGs")


if __name__ == "__main__":
    main()
