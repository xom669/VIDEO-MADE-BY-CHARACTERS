#GlyphStream: High-Resolution Video-to-Text & RGB ASCII Studio

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-Vectorized-green?style=for-the-badge&logo=opencv)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

**GlyphStream** is a high-performance Python rendering engine that converts standard video files (`.mp4`, `.mkv`, `.avi`, `.mov`, `.webm`) into high-resolution videos composed entirely of typographic characters. 

Instead of slow per-character drawing loops, GlyphStream uses **NumPy matrix masking** to render 2K/4K multi-language text grids at high frame rates while preserving exact RGB pixel colors and automatically multiplexing the original audio stream.

---

## Key Features

- **Vectorized NumPy Rendering Engine:** Renders tens of thousands of characters per frame using stencil array multiplication rather than individual draw calls.
- **7 Built-in Multi-Language Character Packs:**
  1. **Standard 70-Level ASCII** (Full English typographic brightness ramp)
  2. **Japanese** (Full-width Katakana & stroke-ordered Kanji up to `鬱`)
  3. **Chinese Mandarin** (Simplified Hanzi gradient up to 48-stroke `龘`)
  4. **Greek & Mathematical Symbols** (`π`, `Σ`, `Ω`, `Φ`, `Ψ`, `Ξ`)
  5. **Bengali Script** (`অ`, `ক`, `খ`, `ক্ষ`, `জ্ঞ`)
  6. **Matrix Binary & Hexadecimal** (`0-9`, `A-F`)
  7. **Retro Block Shading** (`░▒▓█`)
  8. **Custom String Input** (Define your own character ramp on the fly)
- **5 Visual & Color Modes:**
  - **True RGB Color:** Matches original video colors per character block.
  - **Cyberpunk RGB + Neon Bloom:** Adds a Gaussian phosphor light-bleed around bright glyphs.
  - **Classic Matrix Green:** Monochrome terminal green (`#14FF41`).
  - **Crisp Monochrome White:** High-contrast grayscale typography.
  - **Retro Amber CRT:** Vintage monitor aesthetic.
- **Automatic Lossless Audio Sync:** Uses a self-contained `imageio-ffmpeg` binary to copy the original audio track into the final `.mp4` with zero manual FFmpeg setup required.
- **Native File Picker + CLI:** Browse for files with a native GUI window or paste file paths directly.

---

## Quick Start

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/glyphstream-ascii-studio.git](https://github.com/YOUR_USERNAME/glyphstream-ascii-studio.git)
cd glyphstream-ascii-studio
