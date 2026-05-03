import os
import json
import requests
from io import BytesIO
from PIL import Image
from fpdf import FPDF

EXERCISES_JSON_URL = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/dist/exercises.json"
IMAGE_BASE_URL = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/exercises/"
IMG_DIR = "/Users/amitraj/Desktop/Test/exercise_images"
OUTPUT_PDF = "/Users/amitraj/Desktop/Test/Workout_Plan_6Day_Split.pdf"

EXERCISE_MAP = {
    # Chest
    "DB flat bench press": "dumbbell bench press",
    "Machine chest press": "machine bench press",
    "Incline DB press (30 deg)": "incline dumbbell press",
    "Incline machine press": "leverage incline chest press",
    "Cable crossover (high-to-low)": "cable crossover",
    "Cable crossover (low-to-high)": "cable crossover",
    "Decline DB fly": "decline dumbbell flyes",
    "DB floor press": "dumbbell floor press",
    "Push-ups (knees if needed)": "push-ups - close triceps position",
    "Pec deck machine": "butterfly",

    # Back
    "Lat pulldown (neutral/close grip)": "close-grip front lat pulldown",
    "Assisted pull-up machine": "band assisted pull-up",
    "Seated cable row (neutral grip)": "seated cable rows",
    "Machine row": "seated cable rows",
    "DB single-arm row": "one-arm dumbbell row",
    "Chest-supported DB row": "dumbbell incline row",
    "Face pulls (rope attachment)": "face pull",
    "Reverse pec deck": "cable rear delt fly",

    # Triceps
    "Cable rope pushdowns": "triceps pushdown - rope attachment",
    "V-bar pushdowns": "triceps pushdown - v-bar attachment",
    "Overhead cable extension (rope)": "cable rope overhead triceps extension",
    "Overhead cable extension": "cable rope overhead triceps extension",
    "Overhead DB extension (2-hand)": "cable rope overhead triceps extension",
    "Single-arm cable pushdown": "cable one arm tricep extension",
    "Machine dip (assisted)": "dip machine",
    "Bench dip (partial ROM)": "bench dips",
    "DB kickbacks": "tricep dumbbell kickback",
    "DB kickback": "tricep dumbbell kickback",
    "Close-grip push-ups (knees)": "close-grip push-up off of a dumbbell",
    "Close-grip push-up": "push-ups - close triceps position",

    # Biceps
    "DB hammer curls": "hammer curls",
    "Cable rope hammer curls": "cable hammer curls - rope attachment",
    "Incline DB curls": "incline dumbbell curl",
    "Machine preacher curl": "machine preacher curls",
    "Cable EZ-bar curl": "standing biceps cable curl",
    "Concentration curls": "concentration curls",
    "Cable single-arm curl": "standing one-arm cable curl",
    "Cable curl (EZ-bar)": "standing biceps cable curl",
    "DB standing curl": "standing one-arm dumbbell curl over incline bench",
    "Spider curls (incline bench)": "spider curl",
    "Preacher curl machine": "preacher curl",
    "Cable hammer curl (rope)": "cable hammer curls - rope attachment",
    "DB cross-body hammer curl": "cross body hammer curl",

    # Shoulders
    "Machine shoulder press": "cable shoulder press",
    "Seated DB press (light)": "alternating kettlebell press",
    "Cable lateral raise": "seated cable shoulder press",
    "DB lateral raise (light)": "side lateral raise",
    "Cable face pulls": "face pull",
    "Rear delt cable fly": "cable rear delt fly",
    "Seated rear delt raise": "seated bent-over rear delt raise",
    "DB front raise (neutral grip)": "front dumbbell raise",

    # Abs
    "Dead bug": "dead bug",
    "Reverse crunch": "reverse crunch",
    "Cable Pallof press": "pallof press",
    "Banded Pallof press": "pallof press with rotation",
    "Cable crunch (kneeling)": "cable crunch",
    "Ab crunch machine": "ab crunch machine",
    "Forearm plank": "plank",
    "Incline plank (hands on bench)": "plank",
    "Hanging knee raise": "hanging leg raise",
    "Captain's chair knee raise": "flat bench lying leg raise",

    # Legs - Quads
    "Goblet squat (DB)": "goblet squat",
    "Leg press machine": "leg press",
    "Leg extension machine": "leg extensions",
    "Walking lunges (BW or light DB)": "bodyweight walking lunge",
    "Hack squat machine": "hack squat",
    "Smith machine squat": "smith machine squat",

    # Legs - Hamstrings
    "Romanian deadlift (DBs)": "romanian deadlift",
    "Cable pull-through": "band good morning (pull through)",
    "Lying leg curl machine": "lying leg curls",
    "Seated leg curl machine": "seated leg curl",

    # Legs - Glutes
    "Hip thrust (barbell/Smith)": "barbell hip thrust",
    "Glute bridge (DB on hips)": "barbell glute bridge",
    "Reverse lunge": "dumbbell rear lunge",

    # Calves
    "Standing calf raise (machine)": "standing calf raises",
    "DB standing calf raise": "standing dumbbell calf raise",
    "Seated calf raise (machine)": "seated calf raise",
    "Leg press calf raise": "calf press on the leg press machine",
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


def download_image(image_path, target_path):
    if os.path.exists(target_path):
        return True
    url = IMAGE_BASE_URL + image_path
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            img = Image.open(BytesIO(r.content))
            img = img.convert("RGB")
            img.thumbnail((200, 200), Image.LANCZOS)
            img.save(target_path, "JPEG", quality=80)
            return True
    except Exception as e:
        print(f"  Failed to download {url}: {e}")
    return False


def get_exercise_image(db, exercise_name):
    mapped = EXERCISE_MAP.get(exercise_name)
    if not mapped:
        mapped = exercise_name

    ex = find_exercise(db, mapped)
    if not ex or not ex.get("images"):
        return None

    img_rel = ex["images"][0]
    safe_name = exercise_name.replace("/", "_").replace(" ", "_").replace("(", "").replace(")", "")
    target = os.path.join(IMG_DIR, safe_name + ".jpg")

    if download_image(img_rel, target):
        return target
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
            self.cell(0, 6, "6-Day Workout Plan  |  2 Muscles Per Day  |  2x Per Week", align="C")
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

    def warmup_table(self, exercises):
        widths = [8, 90, 92]
        headers = ["#", "Exercise", "Duration / Reps"]
        self.set_fill_color(80, 130, 80)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 8)
        for w, h in zip(widths, headers):
            self.cell(w, 7, h, border=1, fill=True, align="C")
        self.ln()
        self.set_text_color(0, 0, 0)
        for i, ex in enumerate(exercises):
            self.set_font("Helvetica", "", 7.5)
            if i % 2 == 0:
                self.set_fill_color(240, 248, 240)
            else:
                self.set_fill_color(255, 255, 255)
            for w, c in zip(widths, ex):
                self.cell(w, 6, c, border=1, fill=True)
            self.ln()
        self.ln(2)

    def cooldown_table(self, exercises):
        widths = [8, 100, 82]
        headers = ["#", "Exercise", "Duration"]
        self.set_fill_color(100, 100, 140)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 8)
        for w, h in zip(widths, headers):
            self.cell(w, 7, h, border=1, fill=True, align="C")
        self.ln()
        self.set_text_color(0, 0, 0)
        for i, ex in enumerate(exercises):
            self.set_font("Helvetica", "", 7.5)
            if i % 2 == 0:
                self.set_fill_color(240, 240, 250)
            else:
                self.set_fill_color(255, 255, 255)
            for w, c in zip(widths, ex):
                self.cell(w, 6, c, border=1, fill=True)
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
    pdf.cell(0, 10, "2x/Week Per Muscle  |  2 Muscles Per Day", align="C", new_x="LMARGIN", new_y="NEXT")
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
            ["Age / Sex", "32 / Male"],
            ["Weight / Height", "66 kg / 165 cm"],
            ["BMI / Body Fat", "23.4 / 33.1%"],
            ["Goal", "Fat loss + Muscle gain + Fitness + Flexibility"],
            ["Injuries", "Right elbow (healed), Left clavicle (healed)"],
            ["Equipment", "Full Gym"],
            ["Schedule", "Monday - Saturday (Sunday Rest)"],
        ],
        fill_color=(50, 80, 140),
    )
    pdf.ln(5)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, "Beginner-friendly | Injury-aware | Every exercise has an alternate", align="C")

    # ===== INJURY SAFETY RULES =====
    pdf.add_page()
    pdf.section_title("INJURY SAFETY RULES", 180, 50, 50)
    pdf.ln(2)
    pdf.sub_title("Right Elbow (Healed Fracture)")
    for t in [
        "Use neutral/hammer grip on all curls and presses",
        "No skull crushers, no heavy barbell curls",
        "Wear an elbow sleeve on upper body days",
        "Stop any exercise that causes sharp elbow pain - switch to the alternate",
    ]:
        pdf.bullet(t)
    pdf.ln(2)
    pdf.sub_title("Left Clavicle (Healed Fracture)")
    for t in [
        "Dumbbells only for chest pressing (never barbell)",
        "Machine shoulder press only - no barbell overhead press",
        "No wide-grip pulldowns or dips for weeks 1-4",
        "If collarbone discomfort on bench - switch to floor press",
    ]:
        pdf.bullet(t)
    pdf.ln(3)

    pdf.section_title("WEEKLY OVERVIEW")
    pdf.simple_table(
        [30, 50, 50, 30],
        ["Day", "Muscle 1", "Muscle 2", "Time"],
        [
            ["Monday", "Chest", "Triceps", "~60 min"],
            ["Tuesday", "Legs (Quad)", "Shoulders + Abs", "~65 min"],
            ["Wednesday", "Back", "Biceps", "~60 min"],
            ["Thursday", "Chest", "Triceps", "~60 min"],
            ["Friday", "Legs (Ham/Glute)", "Shoulders + Abs", "~65 min"],
            ["Saturday", "Back", "Biceps", "~60 min"],
            ["Sunday", "REST", "-", "-"],
        ],
    )
    pdf.ln(1)
    pdf.sub_title("Training Approach")
    for t in [
        "Mon/Wed = Strength days (heavier, 10-12 reps, 90s rest)",
        "Thu/Sat = Volume days (lighter, 12-15 reps, 60s rest)",
        "Tue = Quad-focused legs | Fri = Ham/Glute-focused legs",
        "Abs trained 2x/week on leg days",
        "Calves: 4 sets x 15 reps, 45s rest",
    ]:
        pdf.bullet(t)

    pdf.ln(4)
    pdf.section_title("HOW TO READ EACH EXERCISE CARD")
    pdf.ln(1)

    pdf.simple_table(
        [35, 155],
        ["Element", "What It Means"],
        [
            ["Sets x Reps", "e.g. 3 x 12 = 3 sets of 12 reps"],
            ["Rest", "How long to rest between sets"],
            ["RIR", "Reps In Reserve = how many reps you could still do. RIR 2 = stop 2 reps before failure"],
            ["Alt", "Alternate exercise you can swap in (same muscle, different movement)"],
        ],
        fill_color=(50, 80, 140),
    )

    pdf.ln(2)
    pdf.sub_title("Intensity Technique Tags")
    pdf.set_font("Helvetica", "", 8)

    badge_y = pdf.get_y()
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

    pdf.sub_title("Simple Intensity Rule")
    pdf.simple_table(
        [45, 55, 90],
        ["Exercise Type", "Techniques", "Examples"],
        [
            ["Compound lifts", "NONE - just progressive overload", "Bench, Squat, Row, RDL"],
            ["Isolation lifts", "DROP / FAILURE / SUPERSET OK", "Curls, Flys, Pushdowns, Raises"],
            ["Strength days", "Heavy + clean, RIR 1-2", "Monday, Wednesday"],
            ["Volume days", "Pump + intensity, last sets", "Thursday, Saturday"],
        ],
        fill_color=(50, 80, 140),
    )

    # ===================================================================
    #              MONDAY - Chest + Triceps (Strength)
    # ===================================================================
    pdf.add_page()
    pdf.section_title("MONDAY - Chest + Triceps (Strength)", 30, 60, 120)

    pdf.sub_title("Warm-Up (8-10 min)", 80, 130, 80)
    pdf.warmup_table([
        ["1", "Brisk treadmill walk (slight incline)", "5 min"],
        ["2", "Arm circles (forward + backward)", "15 each direction"],
        ["3", "Band pull-aparts", "15 reps"],
        ["4", "Wall slides (scapular activation)", "10 reps"],
        ["5", "Push-up to downward dog", "8 reps"],
    ])

    pdf.sub_title("Chest (4 exercises)", 30, 60, 120)
    chest_mon = [
        (1, "DB flat bench press", "Machine chest press", "3 x 10-12", "90s", "1-2", "", "Neutral grip option. Floor press if collarbone discomfort."),
        (2, "Incline DB press (30 deg)", "Incline machine press", "3 x 10-12", "90s", "1-2", "", "Light weight - don't press above shoulder height."),
        (3, "Cable crossover (high-to-low)", "Decline DB fly", "3 x 12-15", "60s", "2", "", "Targets LOWER chest. Squeeze at bottom."),
        (4, "DB floor press", "Push-ups (knees if needed)", "3 x 12", "60s", "2", "", "Shorter ROM = safest for collarbone."),
    ]
    for num, name, alt, sets, rest, rir, technique, note in chest_mon:
        pdf.exercise_with_image(num, name, alt, sets, rest, rir, technique, note, get_img(name), get_img(alt))

    pdf.ln(3)
    pdf.sub_title("Triceps (3 exercises)", 30, 60, 120)
    tri_mon = [
        (1, "Cable rope pushdowns", "V-bar pushdowns", "3 x 12-15", "60s", "2", "", "Elbows pinned to sides. Low elbow stress."),
        (2, "Overhead cable extension (rope)", "Single-arm cable pushdown", "3 x 12", "60s", "1-2", "", "Controlled movement. Stop if elbow aches."),
        (3, "Machine dip (assisted)", "Bench dip (partial ROM)", "3 x 12", "60s", "2", "", "Machine provides stability. No full dips for 4 weeks."),
    ]
    for num, name, alt, sets, rest, rir, technique, note in tri_mon:
        pdf.exercise_with_image(num, name, alt, sets, rest, rir, technique, note, get_img(name), get_img(alt))

    pdf.ln(3)
    pdf.sub_title("Cardio Finisher (10 min)", 180, 80, 50)
    pdf.cardio_table([
        ["Incline treadmill walk (10-12% incline, 5.5 km/h)", "10 min", "HR target: 130-145 BPM"],
    ])

    pdf.sub_title("Cool-Down (5-7 min)", 100, 100, 140)
    pdf.cooldown_table([
        ["1", "Doorway chest stretch", "30s each side"],
        ["2", "Cross-body shoulder stretch", "30s each side"],
        ["3", "Wrist flexor/extensor stretch", "20s each position"],
        ["4", "Cat-cow spinal mobilization", "10 reps"],
        ["5", "Deep breathing (diaphragmatic)", "1 min"],
    ])

    # ===================================================================
    #        TUESDAY - Legs (Quad Focus) + Shoulders + Abs
    # ===================================================================
    pdf.add_page()
    pdf.section_title("TUESDAY - Legs (Quad Focus) + Shoulders + Abs", 30, 60, 120)

    pdf.sub_title("Warm-Up (8-10 min)", 80, 130, 80)
    pdf.warmup_table([
        ["1", "Stationary bike (easy pace)", "5 min"],
        ["2", "Bodyweight squats", "15 reps"],
        ["3", "Leg swings (front-back + side-side)", "10 each leg, each direction"],
        ["4", "Glute bridges", "15 reps"],
        ["5", "Ankle circles", "10 each direction, each foot"],
    ])

    pdf.sub_title("Legs - Quads + Glutes + Hamstrings (4 exercises)", 30, 60, 120)
    legs_tue = [
        (1, "Goblet squat (DB)", "Leg press machine", "3 x 10-12", "90s", "1-2", "", "Hold DB at chest. Depth over weight."),
        (2, "Leg extension machine", "Walking lunges (BW or light DB)", "3 x 15", "60s", "1", "DROP", "Last set drop set. Squeeze at top for 1 second."),
        (3, "Lying leg curl machine", "Seated leg curl machine", "3 x 12", "60s", "2", "", "Controlled tempo: 2s up, 3s down."),
        (4, "Standing calf raise (machine)", "DB standing calf raise", "4 x 15", "45s", "1-2", "", "Full stretch at bottom, pause at top."),
    ]
    for num, name, alt, sets, rest, rir, technique, note in legs_tue:
        pdf.exercise_with_image(num, name, alt, sets, rest, rir, technique, note, get_img(name), get_img(alt))

    pdf.ln(3)
    pdf.sub_title("Shoulders (2 exercises)", 30, 60, 120)
    shldr_tue = [
        (1, "Machine shoulder press", "Seated DB press (light)", "3 x 10-12", "90s", "1-2", "", "Machine = stable for collarbone. No barbell overhead."),
        (2, "Cable lateral raise", "DB lateral raise (light)", "3 x 15", "60s", "1", "DROP", "Last set drop set. Light weight, control the negative."),
    ]
    for num, name, alt, sets, rest, rir, technique, note in shldr_tue:
        pdf.exercise_with_image(num, name, alt, sets, rest, rir, technique, note, get_img(name), get_img(alt))

    pdf.ln(3)
    pdf.sub_title("Abs (2 exercises)", 30, 60, 120)
    abs_tue = [
        (1, "Dead bug", "Reverse crunch", "3 x 10 each side", "45s", "2", "", "Great for deep core activation. No spinal stress."),
        (2, "Cable Pallof press", "Banded Pallof press", "3 x 10 each side", "45s", "2", "", "Anti-rotation. Builds core stability."),
    ]
    for num, name, alt, sets, rest, rir, technique, note in abs_tue:
        pdf.exercise_with_image(num, name, alt, sets, rest, rir, technique, note, get_img(name), get_img(alt))

    pdf.ln(3)
    pdf.sub_title("Cardio Finisher (10 min)", 180, 80, 50)
    pdf.cardio_table([
        ["Incline treadmill walk (12% incline, 5.5 km/h)", "10 min", "Great quad/glute finisher + fat burn."],
    ])

    pdf.sub_title("Cool-Down (5-7 min)", 100, 100, 140)
    pdf.cooldown_table([
        ["1", "Standing quad stretch", "30s each side"],
        ["2", "Calf stretch against wall", "30s each side"],
        ["3", "Seated hamstring stretch", "30s each side"],
        ["4", "Deep squat hold (no weight)", "30s"],
        ["5", "Ankle circles", "10 each direction"],
    ])

    # ===================================================================
    #            WEDNESDAY - Back + Biceps (Strength)
    # ===================================================================
    pdf.add_page()
    pdf.section_title("WEDNESDAY - Back + Biceps (Strength)", 30, 60, 120)

    pdf.sub_title("Warm-Up (8-10 min)", 80, 130, 80)
    pdf.warmup_table([
        ["1", "Rowing machine (easy pace)", "5 min"],
        ["2", "Band dislocates (shoulder mobility)", "10 reps"],
        ["3", "Scapular push-ups", "10 reps"],
        ["4", "Light DB external rotation", "10 each arm"],
        ["5", "Cat-cow", "10 reps"],
    ])

    pdf.sub_title("Back (4 exercises)", 30, 60, 120)
    back_wed = [
        (1, "Lat pulldown (neutral/close grip)", "Assisted pull-up machine", "3 x 10-12", "90s", "1-2", "", "No wide grip - protect collarbone. Squeeze shoulder blades."),
        (2, "Seated cable row (neutral grip)", "Machine row", "3 x 10-12", "90s", "1-2", "", "Neutral grip = low elbow stress. Pull to lower chest."),
        (3, "DB single-arm row", "Chest-supported DB row", "3 x 10 each", "60s", "2", "", "Support on bench. Start light on right arm."),
        (4, "Face pulls (rope attachment)", "Reverse pec deck", "3 x 15", "60s", "2", "", "Pull to forehead. Great for posture + rear delts."),
    ]
    for num, name, alt, sets, rest, rir, technique, note in back_wed:
        pdf.exercise_with_image(num, name, alt, sets, rest, rir, technique, note, get_img(name), get_img(alt))

    pdf.ln(3)
    pdf.sub_title("Biceps (3 exercises)", 30, 60, 120)
    bi_wed = [
        (1, "DB hammer curls", "Cable rope hammer curls", "3 x 12", "60s", "1-2", "", "Neutral grip = safest for right elbow. No swinging."),
        (2, "Incline DB curls", "Machine preacher curl", "3 x 12", "60s", "2", "", "Light weight, full stretch. Skip if elbow pain."),
        (3, "Cable EZ-bar curl", "Concentration curls", "3 x 12-15", "60s", "0", "FAILURE", "Last set to slight failure. Constant cable tension is joint-friendly."),
    ]
    for num, name, alt, sets, rest, rir, technique, note in bi_wed:
        pdf.exercise_with_image(num, name, alt, sets, rest, rir, technique, note, get_img(name), get_img(alt))

    pdf.ln(3)
    pdf.sub_title("Cardio Finisher (12 min)", 180, 80, 50)
    pdf.cardio_table([
        ["Elliptical (moderate pace)", "12 min", "RPE 5-6/10. Low impact. Light grip."],
    ])

    pdf.sub_title("Cool-Down (5-7 min)", 100, 100, 140)
    pdf.cooldown_table([
        ["1", "Lat stretch (hang from bar lightly)", "30s"],
        ["2", "Cross-body shoulder stretch", "30s each side"],
        ["3", "Tricep overhead stretch", "30s each side"],
        ["4", "Child's pose", "45s"],
        ["5", "Neck stretches (side tilt + rotation)", "20s each direction"],
    ])

    # ===================================================================
    #           THURSDAY - Chest + Triceps (Volume)
    # ===================================================================
    pdf.add_page()
    pdf.section_title("THURSDAY - Chest + Triceps (Volume)", 30, 60, 120)

    pdf.sub_title("Warm-Up (8-10 min)", 80, 130, 80)
    pdf.warmup_table([
        ["1", "Brisk treadmill walk (slight incline)", "5 min"],
        ["2", "Arm circles (forward + backward)", "15 each direction"],
        ["3", "Band pull-aparts", "15 reps"],
        ["4", "Wall slides (scapular activation)", "10 reps"],
        ["5", "Push-up to downward dog", "8 reps"],
    ])

    pdf.sub_title("Chest (4 exercises)", 30, 60, 120)
    chest_thu = [
        (1, "Machine chest press", "DB flat bench press", "3 x 12-15", "60s", "2-3", "", "Machine = controlled movement for volume day."),
        (2, "Incline machine press", "Incline DB press (30 deg)", "3 x 12-15", "60s", "2-3", "", "Focus on squeeze, not weight."),
    ]
    for num, name, alt, sets, rest, rir, technique, note in chest_thu:
        pdf.exercise_with_image(num, name, alt, sets, rest, rir, technique, note, get_img(name), get_img(alt))

    pdf.ln(2)
    pdf.superset_block(
        (3, "Pec deck machine", "Cable crossover (low-to-high)", "3 x 15", "60s", "0", "DROP FAILURE", "Last set drop + failure. Full stretch and squeeze."),
        (4, "Push-ups (knees if needed)", "DB floor press", "3 x AMRAP", "60s", "0", "FAILURE", "Burnout set. Go to failure safely."),
        get_img,
    )

    pdf.ln(3)
    pdf.sub_title("Triceps (3 exercises)", 30, 60, 120)

    pdf.ln(2)
    pdf.superset_block(
        (1, "V-bar pushdowns", "Cable rope pushdowns", "3 x 15", "60s", "1", "DROP", "Last set drop set. Higher reps, focus on squeeze."),
        (2, "DB kickbacks", "Close-grip push-up", "3 x 12 each", "60s", "2-3", "", "Light weight, full extension."),
        get_img,
    )

    tri_thu_rest = [
        (3, "Overhead DB extension (2-hand)", "Overhead cable extension", "3 x 12", "60s", "2-3", "", "Light weight. Skip if elbow pain."),
    ]
    for num, name, alt, sets, rest, rir, technique, note in tri_thu_rest:
        pdf.exercise_with_image(num, name, alt, sets, rest, rir, technique, note, get_img(name), get_img(alt))

    pdf.ln(3)
    pdf.sub_title("Cardio Finisher (10 min)", 180, 80, 50)
    pdf.cardio_table([
        ["Incline treadmill walk (10-12% incline, 5.5 km/h)", "10 min", "HR target: 130-145 BPM"],
    ])

    pdf.sub_title("Cool-Down (5-7 min)", 100, 100, 140)
    pdf.cooldown_table([
        ["1", "Doorway chest stretch", "30s each side"],
        ["2", "Cross-body shoulder stretch", "30s each side"],
        ["3", "Wrist flexor/extensor stretch", "20s each position"],
        ["4", "Cat-cow spinal mobilization", "10 reps"],
        ["5", "Deep breathing (diaphragmatic)", "1 min"],
    ])

    # ===================================================================
    #       FRIDAY - Legs (Ham/Glute Focus) + Shoulders + Abs
    # ===================================================================
    pdf.add_page()
    pdf.section_title("FRIDAY - Legs (Ham/Glute Focus) + Shoulders + Abs", 30, 60, 120)

    pdf.sub_title("Warm-Up (8-10 min)", 80, 130, 80)
    pdf.warmup_table([
        ["1", "Treadmill walk (moderate incline)", "5 min"],
        ["2", "Banded lateral walks", "15 each direction"],
        ["3", "Single-leg glute bridge", "10 each side"],
        ["4", "Inchworms", "8 reps"],
        ["5", "Bodyweight good mornings", "10 reps"],
    ])

    pdf.sub_title("Legs - Hamstrings + Glutes (4 exercises)", 30, 60, 120)
    legs_fri = [
        (1, "Romanian deadlift (DBs)", "Cable pull-through", "3 x 10-12", "90s", "1-2", "", "DBs = easier grip for right elbow. Hinge at hips."),
        (2, "Hip thrust (barbell/Smith)", "Glute bridge (DB on hips)", "3 x 12", "90s", "1-2", "", "Pad the bar. Full glute squeeze at top."),
        (3, "Walking lunges (BW or light DB)", "Reverse lunge", "3 x 10 each", "60s", "2", "", "Bodyweight if grip bothers elbow."),
        (4, "Seated calf raise (machine)", "Leg press calf raise", "4 x 15", "45s", "1-2", "", "Targets soleus. Slow and controlled."),
    ]
    for num, name, alt, sets, rest, rir, technique, note in legs_fri:
        pdf.exercise_with_image(num, name, alt, sets, rest, rir, technique, note, get_img(name), get_img(alt))

    pdf.ln(3)
    pdf.sub_title("Shoulders (2 exercises)", 30, 60, 120)
    shldr_fri = [
        (1, "Seated DB press (light)", "Machine shoulder press", "3 x 12", "60s", "2-3", "", "Lighter than Tuesday, higher reps."),
        (2, "Rear delt cable fly", "Seated rear delt raise", "3 x 15", "60s", "1", "DROP", "Last set drop set. Rear delts often neglected."),
    ]
    for num, name, alt, sets, rest, rir, technique, note in shldr_fri:
        pdf.exercise_with_image(num, name, alt, sets, rest, rir, technique, note, get_img(name), get_img(alt))

    pdf.ln(3)
    pdf.sub_title("Abs (2 exercises)", 30, 60, 120)
    abs_fri = [
        (1, "Hanging knee raise", "Captain's chair knee raise", "3 x 10", "45s", "2", "", "Controlled - no swinging."),
        (2, "Cable crunch (kneeling)", "Ab crunch machine", "3 x 12-15", "45s", "2", "", "Targets UPPER ABS. Squeeze at bottom."),
    ]
    for num, name, alt, sets, rest, rir, technique, note in abs_fri:
        pdf.exercise_with_image(num, name, alt, sets, rest, rir, technique, note, get_img(name), get_img(alt))

    pdf.ln(3)
    pdf.sub_title("Cardio Finisher (10 min)", 180, 80, 50)
    pdf.cardio_table([
        ["Stairclimber (moderate pace)", "10 min", "RPE 5-6. Great glute/hamstring finisher."],
    ])

    pdf.sub_title("Cool-Down (5-7 min)", 100, 100, 140)
    pdf.cooldown_table([
        ["1", "Standing hamstring stretch (foot on bench)", "30s each side"],
        ["2", "Pigeon pose (hip flexor/glute)", "30s each side"],
        ["3", "Seated butterfly stretch", "30s"],
        ["4", "Hip flexor lunge stretch", "30s each side"],
        ["5", "Downward dog", "30s"],
    ])

    # ===================================================================
    #            SATURDAY - Back + Biceps (Volume)
    # ===================================================================
    pdf.add_page()
    pdf.section_title("SATURDAY - Back + Biceps (Volume)", 30, 60, 120)

    pdf.sub_title("Warm-Up (8 min)", 80, 130, 80)
    pdf.warmup_table([
        ["1", "Jump rope (or pretend)", "3 min"],
        ["2", "Band dislocates (shoulder mobility)", "10 reps"],
        ["3", "Scapular push-ups", "10 reps"],
        ["4", "Light DB external rotation", "10 each arm"],
        ["5", "Cat-cow", "10 reps"],
    ])

    pdf.sub_title("Back (4 exercises)", 30, 60, 120)
    back_sat = [
        (1, "Chest-supported DB row", "DB single-arm row", "3 x 12-15", "60s", "2-3", "", "Chest support eliminates momentum."),
        (2, "Machine row", "Seated cable row (neutral grip)", "3 x 12-15", "60s", "1", "DROP", "Last set drop set. Focus on contraction."),
        (3, "Lat pulldown (neutral/close grip)", "Assisted pull-up machine", "3 x 12-15", "60s", "0", "FAILURE", "Last set to failure. Slow negative."),
        (4, "Face pulls (rope attachment)", "Reverse pec deck", "3 x 15", "60s", "2-3", "", "Rear delt + posture work."),
    ]
    for num, name, alt, sets, rest, rir, technique, note in back_sat:
        pdf.exercise_with_image(num, name, alt, sets, rest, rir, technique, note, get_img(name), get_img(alt))

    pdf.ln(3)
    pdf.sub_title("Biceps (3 exercises)", 30, 60, 120)
    pdf.ln(2)
    pdf.superset_block(
        (1, "Cable curl (EZ-bar)", "DB standing curl", "3 x 12", "60s", "1", "SUPERSET", "Constant tension. Don't hyperextend elbow."),
        (2, "Cable hammer curl (rope)", "DB cross-body hammer curl", "3 x 12", "60s", "0", "SUPERSET FAILURE", "Last set to failure. Neutral grip = elbow-safe."),
        get_img,
    )

    bi_sat_rest = [
        (3, "Spider curls (incline bench)", "Preacher curl machine", "3 x 12", "60s", "2-3", "", "Strict form, no momentum."),
    ]
    for num, name, alt, sets, rest, rir, technique, note in bi_sat_rest:
        pdf.exercise_with_image(num, name, alt, sets, rest, rir, technique, note, get_img(name), get_img(alt))

    pdf.ln(3)
    pdf.sub_title("Cardio Finisher (10 min)", 180, 80, 50)
    pdf.cardio_table([
        ["Incline treadmill walk (10% incline, 6 km/h)", "10 min", "Light finish to end the week."],
    ])

    pdf.sub_title("Cool-Down (7 min)", 100, 100, 140)
    pdf.cooldown_table([
        ["1", "Lat stretch (hang from bar lightly)", "30s"],
        ["2", "Cross-body shoulder stretch", "30s each side"],
        ["3", "Wrist flexor/extensor stretch", "20s each position"],
        ["4", "Seated forward fold", "30s"],
        ["5", "Foam roll - upper back", "2 min"],
        ["6", "Deep breathing (box breathing)", "1 min"],
    ])

    # ===================================================================
    #              SUNDAY + OVERLOAD + NUTRITION
    # ===================================================================
    pdf.add_page()
    pdf.section_title("SUNDAY - Rest & Active Recovery", 100, 140, 80)
    pdf.ln(2)
    for t in [
        "Walk 20-30 min at easy pace (outdoors preferred)",
        "Foam roll any sore areas - 5-10 min",
        "Stretch - repeat any cool-down stretches that felt good during the week",
        "Hydrate - 3+ liters of water",
        "Sleep - aim for 7-8 hours",
        "No gym work",
    ]:
        pdf.bullet(t)
    pdf.ln(5)

    pdf.section_title("PROGRESSIVE OVERLOAD (Weeks 1-8)")
    pdf.simple_table(
        [30, 160],
        ["Weeks", "What to Do"],
        [
            ["1-2", "Learn all movements. Light weights (RPE 5-6). Focus 100% on form."],
            ["3-4", "Increase weight by ~2 kg per DB exercise, ~5 kg per machine."],
            ["5-6", "Add 1 set to compound lifts (to 4 sets). Increase planks to 40-45s."],
            ["7-8", "Increase weight again. Reduce rest by 10-15s. Add 2 min to cardio."],
            ["Every 4 wks", "Deload week - drop weights 40%, keep all movements."],
        ],
    )

    pdf.ln(3)
    pdf.section_title("NUTRITION GUIDELINES")
    pdf.simple_table(
        [35, 45, 110],
        ["Macro", "Daily Target", "Notes"],
        [
            ["Calories", "1,700-1,850 kcal", "Slight deficit (~300-400 below maintenance)"],
            ["Protein", "120-130g", "Critical for muscle growth + fat loss (~2g/kg)"],
            ["Carbs", "150-180g", "Fuel workouts. Prioritize around training."],
            ["Fats", "45-55g", "Don't go below 40g - hormone health"],
            ["Water", "3-3.5 liters", "More on training days"],
        ],
    )

    pdf.ln(3)
    pdf.section_title("WHEN TO STOP & SWITCH TO ALTERNATE", 180, 50, 50)
    pdf.simple_table(
        [80, 110],
        ["Warning Sign", "Action"],
        [
            ["Sharp pain at right elbow", "Stop immediately - use the alternate exercise"],
            ["Collarbone ache during press", "Switch to floor press or machine variant"],
            ["Joint clicking with pain", "Stop that exercise for the day"],
            ["Numbness/tingling in arm/hand", "Stop workout, consult doctor if persists"],
            ["Muscle soreness (DOMS)", "Normal - continue with lighter weight"],
        ],
        fill_color=(180, 50, 50),
    )

    pdf.output(OUTPUT_PDF)
    return OUTPUT_PDF


def main():
    os.makedirs(IMG_DIR, exist_ok=True)
    print("Loading exercise database...")
    db = load_exercise_db()
    print(f"Loaded {len(db)} exercises from database")

    print("Downloading exercise images...")
    all_exercises = set()
    for key in EXERCISE_MAP:
        all_exercises.add(key)
    for val in EXERCISE_MAP.values():
        pass  # these get downloaded on demand

    print("Building PDF with images...")
    path = build_pdf(db)
    print(f"\nPDF generated successfully: {path}")

    img_count = len([f for f in os.listdir(IMG_DIR) if f.endswith(".jpg")])
    print(f"Downloaded {img_count} exercise images")


if __name__ == "__main__":
    main()
