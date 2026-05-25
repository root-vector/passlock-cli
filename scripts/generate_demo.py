#!/usr/bin/env python3
"""
Generate demo.gif for passlock-cli README
Creates a terminal-style animated GIF showing basic usage
"""

import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def create_demo_gif():
    """Generate terminal-style animated GIF demonstrating passlock-cli usage."""

    # Configuration
    WIDTH = 900
    HEIGHT = 500
    BG_COLOR = (0, 0, 0)  # Black background
    TEXT_COLOR = (0, 255, 0)  # Green text
    CHAR_DELAY = 80  # ms per character
    LINE_DELAY = 500  # ms pause after each line

    # Terminal session frames
    lines = [
        "$ passlock init",
        "Creating vault at ~/.passlock/",
        "Master password set.",
        "",
        "$ passlock add --site example.com --username alice",
        "Password saved.",
        "",
        "$ passlock get example.com",
        "✓ Password copied to clipboard (clears in 15s)",
        "",
        "$ passlock list",
        "example.com | alice | updated today",
    ]

    frames = []
    durations = []

    # Try to use a monospace font, fallback to default
    try:
        # Try common monospace fonts
        font_paths = [
            "C:\\Windows\\Fonts\\consola.ttf",  # Windows
            "/System/Library/Fonts/Monaco.dfont",  # macOS
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",  # Linux
        ]
        font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                font = ImageFont.truetype(font_path, 16)
                break
        if font is None:
            font = ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()

    # Build frames by simulating typing
    current_text = []

    for line in lines:
        if line == "":
            # Empty line - just add it
            current_text.append("")
            frame = create_frame(current_text, WIDTH, HEIGHT, BG_COLOR, TEXT_COLOR, font)
            frames.append(frame)
            durations.append(LINE_DELAY)
        else:
            # Simulate typing each character
            for i in range(len(line) + 1):
                partial_line = line[:i]
                display_text = current_text + [partial_line]

                frame = create_frame(display_text, WIDTH, HEIGHT, BG_COLOR, TEXT_COLOR, font)
                frames.append(frame)
                durations.append(CHAR_DELAY)

            # Line complete - add to current text
            current_text.append(line)

            # Pause after line completion
            frame = create_frame(current_text, WIDTH, HEIGHT, BG_COLOR, TEXT_COLOR, font)
            frames.append(frame)
            durations.append(LINE_DELAY)

    # Hold final frame longer
    frames.append(frames[-1])
    durations.append(2000)

    # Save as GIF
    output_path = Path(__file__).parent.parent / "docs" / "demo.gif"
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=False,
    )

    print(f"Demo GIF created: {output_path}")
    print(f"Total frames: {len(frames)}")
    print(f"Dimensions: {WIDTH}x{HEIGHT}")


def create_frame(text_lines, width, height, bg_color, text_color, font):
    """Create a single frame with the given text lines."""
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Starting position
    x = 20
    y = 20
    line_height = 25

    # Draw each line
    for line in text_lines:
        draw.text((x, y), line, fill=text_color, font=font)
        y += line_height

    return img


if __name__ == "__main__":
    create_demo_gif()
