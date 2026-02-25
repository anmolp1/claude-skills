"""
Reusable Pillow drawing helpers for reel-maker.
These are shared across all video renderers.
"""

from PIL import ImageFont

# ── Constants ───────────────────────────────────────────
W, H = 1080, 1920
BG = (13, 17, 23)
RED = (255, 59, 48)
GREEN = (0, 255, 136)
BLUE = (0, 122, 255)
YELLOW = (255, 214, 10)
WHITE = (240, 246, 252)
GRAY = (139, 148, 158)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


# ── Color Helpers ───────────────────────────────────────
def rgba(color, alpha):
    """Blend color with BG at given alpha (0-1). Returns RGB tuple."""
    alpha = max(0.0, min(1.0, alpha))
    return tuple(int(c * alpha + b * (1 - alpha)) for c, b in zip(color, BG))


# ── Font Helpers ────────────────────────────────────────
def font_mono(size, bold=True):
    """Monospace font (DejaVu Sans Mono)."""
    name = "DejaVuSansMono-Bold.ttf" if bold else "DejaVuSansMono.ttf"
    return ImageFont.truetype(FONT_DIR + name, size)


def font_sans(size, bold=True):
    """Sans-serif font (DejaVu Sans)."""
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(FONT_DIR + name, size)


# ── Drawing Primitives ──────────────────────────────────
def draw_rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    """Draw a rounded rectangle. xy = (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = xy
    r = min(radius, (x1 - x0) // 2, (y1 - y0) // 2)
    r = max(0, r)
    if fill:
        draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)
    elif outline:
        draw.rounded_rectangle(xy, radius=r, outline=outline, width=width)


def centered_text(draw, text, cx, cy, f, fill=WHITE):
    """Draw text centered at (cx, cy)."""
    bbox = f.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2), text, font=f, fill=fill)


def left_text(draw, text, x, cy, f, fill=WHITE):
    """Draw text left-aligned at x, vertically centered at cy."""
    bbox = f.getbbox(text)
    th = bbox[3] - bbox[1]
    draw.text((x, cy - th // 2), text, font=f, fill=fill)


def right_text(draw, text, x, cy, f, fill=WHITE):
    """Draw text right-aligned at x, vertically centered at cy."""
    bbox = f.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((x - tw, cy - th // 2), text, font=f, fill=fill)


def draw_line(draw, xy, fill, width=2):
    """Draw a line. xy = [(x1,y1), (x2,y2)]."""
    draw.line(xy, fill=fill, width=width)
