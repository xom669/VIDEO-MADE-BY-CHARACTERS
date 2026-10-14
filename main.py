import os
import platform
import subprocess
import sys
import time

print("MADE BY DIPANJAN BAIDYA\nig: @xom699\njust a follow")

# =====================================================================
# 1. AUTOMATIC DEPENDENCY INSTALLER
# =====================================================================
def ensure_dependencies():
    """Checks for required libraries and installs them automatically if missing."""
    required = {
        "cv2": "opencv-python",
        "numpy": "numpy",
        "PIL": "Pillow",
        "imageio_ffmpeg": "imageio-ffmpeg",
    }
    for module_name, pip_name in required.items():
        try:
            __import__(module_name)
        except ImportError:
            print(f"[*] Missing '{pip_name}'. Installing automatically...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pip_name]
            )
            print(f"[+] Successfully installed '{pip_name}'!\n")


ensure_dependencies()

import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# =====================================================================
# 2. LANGUAGE & CHARACTER PACKS (Ordered Darkest to Brightest)
# =====================================================================
CHAR_PACKS = {
    "1": {
        "name": "Standard ASCII (70-level Detailed English + Punctuation)",
        "chars": " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$",
        "fonts": ["consola.ttf", "cour.ttf", "lucon.ttf", "DejaVuSansMono.ttf"],
    },
    "2": {
        "name": "Japanese (Katakana & Dense Kanji)",
        "chars": " ・丶一ノ十人ニエロコ日ヨ目田国回品晶森闇鬱",
        "fonts": ["msgothic.ttc", "YuGothM.ttc", "meiryo.ttc", "NotoSansCJK-Regular.ttc"],
    },
    "3": {
        "name": "Chinese Mandarin (Simplified Hanzi Stroke Gradient)",
        "chars": " 丶一二十人卜入八几刀力口山千日月中水火木金土田目电国晶森繁龘",
        "fonts": ["simsun.ttc", "msyh.ttc", "simhei.ttf", "msgothic.ttc"],
    },
    "4": {
        "name": "Greek & Mathematical Symbols",
        "chars": " .·:;-+=÷×±√πτφθλΔΣΠΩαβγδεζηκμνξρσψωΦΨΘΞ",
        "fonts": ["consola.ttf", "cour.ttf", "arial.ttf", "DejaVuSansMono.ttf"],
    },
    "5": {
        "name": "Bengali Script (বাংলা অক্ষর)",
        "chars": " .ঁংঃইউএওকখগঘচছজঝটঠডঢণতথদধনপফবভমযরলশষসহক্ষজ্ঞ",
        "fonts": ["Nirmala.ttf", "Vrinda.ttf", "arial.ttf"],
    },
    "6": {
        "name": "Matrix Binary & Hexadecimal (0-1 / A-F)",
        "chars": "  .:0123456789ABCDEF#",
        "fonts": ["consola.ttf", "cour.ttf", "DejaVuSansMono.ttf"],
    },
    "7": {
        "name": "Retro Block Shading (High-Contrast Blocks)",
        "chars": " ░▒▓█",
        "fonts": ["consola.ttf", "lucon.ttf", "DejaVuSansMono.ttf"],
    },
}

# =====================================================================
# 3. RESOLUTION TIERS
# =====================================================================
RESOLUTIONS = {
    "1": {"name": "Retro Low-Res (Fastest, Chunky Text)", "width": 120, "font_size": 14},
    "2": {"name": "Standard HD (Balanced)", "width": 200, "font_size": 11},
    "3": {"name": "Ultra-Sharp 2K (High Detail)", "width": 280, "font_size": 9},
    "4": {"name": "Extreme 4K Micro-Text (Maximum Sharpness)", "width": 380, "font_size": 7},
}

# =====================================================================
# 4. COLOR & VISUAL THEMES
# =====================================================================
COLOR_MODES = {
    "1": "True RGB Color (Matches Original Video Colors)",
    "2": "Cyberpunk RGB + Neon Bloom Glow (Glowing Highlights)",
    "3": "Classic Matrix Phosphor Green",
    "4": "Crisp Monochrome White on Dark Gray",
    "5": "Retro Amber CRT Monitor",
}


def load_best_font(font_filenames, font_size):
    """Searches system font directories across Windows, macOS, and Linux."""
    search_dirs = [
        r"C:\Windows\Fonts",
        "/usr/share/fonts",
        "/System/Library/Fonts",
        os.path.expanduser("~/.local/share/fonts"),
    ]
    for directory in search_dirs:
        if not os.path.exists(directory):
            continue
        for fname in font_filenames:
            full_path = os.path.join(directory, fname)
            if os.path.exists(full_path):
                try:
                    return ImageFont.truetype(full_path, font_size)
                except IOError:
                    continue
    print("[!] Warning: Specific language font not found; using default font.")
    return ImageFont.load_default()


def select_video_file():
    """Lets the user paste a path or open a native OS file browser."""
    print("\n" + "=" * 60)
    print(" STEP 1: SELECT INPUT VIDEO")
    print("=" * 60)
    print("Enter the full path to your video file, OR press [ENTER] to open")
    print("a file browser window and pick it with your mouse.")

    user_input = input("\nVideo Path (or press Enter to browse): ").strip().strip('"').strip("'")

    if not user_input:
        try:
            import tkinter as tk
            from tkinter import filedialog

            root = tk.Tk()
            root.withdraw()
            root.attributes("-topmost", True)
            file_path = filedialog.askopenfilename(
                title="Select Video File",
                filetypes=[
                    ("Video Files", "*.mp4 *.avi *.mkv *.mov *.webm"),
                    ("All Files", "*.*"),
                ],
            )
            root.destroy()
            return file_path
        except Exception as e:
            print(f"[!] Could not open file picker ({e}). Please paste path:")
            return input("Video Path: ").strip().strip('"').strip("'")
    return user_input


def get_user_configuration():
    """Interactive CLI menu for resolution, character set, and visual style."""
    video_path = select_video_file()
    while not video_path or not os.path.exists(video_path):
        print(f"\n[X] File not found: '{video_path}'")
        video_path = input("Please enter a valid video file path: ").strip().strip('"').strip("'")

    print("\n" + "=" * 60)
    print(" STEP 2: CHOOSE RESOLUTION TIER")
    print("=" * 60)
    for key, val in RESOLUTIONS.items():
        print(f"  [{key}] {val['name']} (Grid Width: {val['width']} chars, Font: {val['font_size']}pt)")
    print("  [5] Custom Resolution (Enter your own character width & font size)")

    res_choice = input("\nSelect Resolution [1-5] (Default=3): ").strip() or "3"
    if res_choice == "5":
        custom_w = int(input("Enter horizontal character count (e.g., 100 to 500): ").strip() or "260")
        custom_f = int(input("Enter font size in points (e.g., 6 to 16): ").strip() or "9")
        width, font_size = custom_w, custom_f
    else:
        preset = RESOLUTIONS.get(res_choice, RESOLUTIONS["3"])
        width, font_size = preset["width"], preset["font_size"]

    print("\n" + "=" * 60)
    print(" STEP 3: CHOOSE LANGUAGE / CHARACTER PACK")
    print("=" * 60)
    for key, val in CHAR_PACKS.items():
        print(f"  [{key}] {val['name']}")
    print("  [8] Custom Characters (Type your own string from dark to bright)")

    char_choice = input("\nSelect Character Pack [1-8] (Default=2): ").strip() or "2"
    if char_choice == "8":
        custom_chars = input("Enter custom characters (start with space for dark, end with dense char): ")
        if len(custom_chars) < 2:
            custom_chars = " .:-=+*#%@"
        chars = np.array(list(custom_chars))
        font_list = ["consola.ttf", "msgothic.ttc", "arial.ttf"]
        pack_tag = "custom"
    else:
        pack = CHAR_PACKS.get(char_choice, CHAR_PACKS["2"])
        chars = np.array(list(pack["chars"]))
        font_list = pack["fonts"]
        pack_tag = f"pack{char_choice}"

    print("\n" + "=" * 60)
    print(" STEP 4: CHOOSE COLOR & VISUAL EFFECT")
    print("=" * 60)
    for key, desc in COLOR_MODES.items():
        print(f"  [{key}] {desc}")

    color_choice = input("\nSelect Color Mode [1-5] (Default=1): ").strip() or "1"
    if color_choice not in COLOR_MODES:
        color_choice = "1"

    return video_path, width, font_size, chars, font_list, color_choice, pack_tag


def merge_audio_with_video(original_video, silent_ascii_video, final_output_video):
    """Uses the bundled imageio-ffmpeg executable to copy the original audio track."""
    print("\n[*] Merging original audio track into the rendered video...")
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    cmd = [
        ffmpeg_exe,
        "-y",
        "-i", silent_ascii_video,
        "-i", original_video,
        "-map", "0:v:0",
        "-map", "1:a:0?",
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        final_output_video,
    ]

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0 and os.path.exists(final_output_video):
            os.remove(silent_ascii_video)
            print("[+] Audio track merged successfully!")
            return final_output_video
        else:
            print("[!] Audio merge returned a warning. Keeping silent video.")
            if os.path.exists(silent_ascii_video):
                os.replace(silent_ascii_video, final_output_video)
            return final_output_video
    except Exception as e:
        print(f"[!] Could not merge audio ({e}). Keeping silent video.")
        if os.path.exists(silent_ascii_video):
            os.replace(silent_ascii_video, final_output_video)
        return final_output_video


def render_video():
    input_path, width, font_size, char_array, font_list, color_mode, pack_tag = get_user_configuration()

    folder, filename = os.path.split(input_path)
    base_name, _ = os.path.splitext(filename)
    temp_silent_path = os.path.join(folder, f"{base_name}_TEMP_SILENT_{pack_tag}.mp4")
    final_output_path = os.path.join(folder, f"{base_name}_TEXT_{pack_tag}_w{width}.mp4")

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"\n[X] Error: Could not open video at {input_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    ret, first_frame = cap.read()
    if not ret:
        print("\n[X] Error: Could not read video frames.")
        return

    font = load_best_font(font_list, font_size)

    sample_char = char_array[-1]
    bbox = font.getbbox(sample_char)
    char_w = max(1, bbox[2] - bbox[0])
    char_h = max(1, int((bbox[3] - bbox[1]) * 1.08))
    aspect_correction = char_w / char_h

    h, w, _ = first_frame.shape
    cols = width
    rows = max(1, int(width * (h / w) * aspect_correction))

    out_w = cols * char_w
    out_h = rows * char_h

    pad_w = out_w % 2
    pad_h = out_h % 2
    final_w = out_w + pad_w
    final_h = out_h + pad_h

    print("\n" + "=" * 60)
    print(" STARTING RENDER ENGINE (WITH AUDIO SYNC)")
    print("=" * 60)
    print(f"  Input File        : {filename}")
    print(f"  Character Grid    : {cols} columns x {rows} rows")
    print(f"  Output Resolution : {final_w}x{final_h} px @ {fps:.2f} FPS")
    print(f"  Color Mode        : {COLOR_MODES[color_mode]}")
    print(f"  Final Output      : {final_output_path}\n")

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out_video = cv2.VideoWriter(temp_silent_path, fourcc, fps, (final_w, final_h))

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    frame_count = 0
    start_clock = time.time()

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1

            small_bgr = cv2.resize(frame, (cols, rows), interpolation=cv2.INTER_AREA)
            small_gray = cv2.cvtColor(small_bgr, cv2.COLOR_BGR2GRAY)

            indices = (small_gray.astype(np.int32) * (len(char_array) - 1)) // 255
            text_grid = char_array[indices]
            lines = ["".join(row) for row in text_grid]

            mask_img = Image.new("L", (out_w, out_h), color=0)
            draw = ImageDraw.Draw(mask_img)
            for idx, line in enumerate(lines):
                draw.text((0, idx * char_h), line, font=font, fill=255)

            mask_arr = np.array(mask_img, dtype=np.float32) / 255.0

            if color_mode in ("1", "2"):
                color_blocks = cv2.resize(small_bgr, (out_w, out_h), interpolation=cv2.INTER_NEAREST)
                color_blocks = np.clip(color_blocks.astype(np.float32) * 1.35, 0, 255)
                colored_text = (color_blocks * mask_arr[:, :, np.newaxis]).astype(np.uint8)

                if color_mode == "2":
                    glow = cv2.GaussianBlur(colored_text, (0, 0), sigmaX=6, sigmaY=6)
                    colored_text = cv2.addWeighted(colored_text, 1.0, glow, 0.65, 0)

            elif color_mode == "3":
                green_layer = np.zeros((out_h, out_w, 3), dtype=np.float32)
                green_layer[:, :, 0] = 65
                green_layer[:, :, 1] = 255
                green_layer[:, :, 2] = 20
                colored_text = (green_layer * mask_arr[:, :, np.newaxis]).astype(np.uint8)

            elif color_mode == "4":
                white_layer = np.full((out_h, out_w, 3), 245, dtype=np.float32)
                colored_text = (white_layer * mask_arr[:, :, np.newaxis]).astype(np.uint8)

            elif color_mode == "5":
                amber_layer = np.zeros((out_h, out_w, 3), dtype=np.float32)
                amber_layer[:, :, 0] = 15
                amber_layer[:, :, 1] = 176
                amber_layer[:, :, 2] = 255
                colored_text = (amber_layer * mask_arr[:, :, np.newaxis]).astype(np.uint8)

            bg = np.full_like(colored_text, (10, 8, 8))
            final_frame = np.where(mask_arr[:, :, np.newaxis] > 0.03, colored_text, bg)

            if pad_w or pad_h:
                final_frame = cv2.copyMakeBorder(
                    final_frame, 0, pad_h, 0, pad_w, cv2.BORDER_CONSTANT, value=(10, 8, 8)
                )

            out_video.write(final_frame)

            elapsed = time.time() - start_clock
            current_fps = frame_count / elapsed if elapsed > 0 else 0
            remaining = (total_frames - frame_count) / current_fps if current_fps > 0 else 0
            pct = (frame_count / total_frames) * 100 if total_frames else 0

            sys.stdout.write(
                f"\r[>] Frame {frame_count}/{total_frames} ({pct:.1f}%) | "
                f"Speed: {current_fps:.1f} fps | ETA: {remaining:.0f}s   "
            )
            sys.stdout.flush()

    except KeyboardInterrupt:
        print("\n\n[!] Rendering paused/stopped early by user. Saving partial video with synced audio...")
    finally:
        cap.release()
        out_video.release()

    if os.path.exists(temp_silent_path) and frame_count > 0:
        saved_file = merge_audio_with_video(input_path, temp_silent_path, final_output_path)
        print(f"\n[+] SUCCESS! Video with audio saved to:\n    {saved_file}")


if __name__ == "__main__":
    render_video()
