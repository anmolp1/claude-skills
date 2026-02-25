"""
Shared scene infrastructure for reel-maker.
Provides progress bar, caption overlay, and the main render_frame shell.
"""

from .drawing import *


def draw_progress_bar(draw, t, scenes, duration):
    """
    Draw segmented progress bar at top of frame.
    scenes: list of dicts with 'start', 'end', 'label', 'color' keys.
    """
    barY, barH, pad = 55, 10, 40
    totalW = W - pad * 2
    x = pad

    for s in scenes:
        seg_dur = s["end"] - s["start"]
        segW = int((seg_dur / duration) * totalW)
        segP = 0 if t < s["start"] else (1 if t > s["end"] else (t - s["start"]) / seg_dur)

        # Background segment
        draw_rounded_rect(draw, (x, barY, x + segW - 4, barY + barH), 5,
                          fill=rgba(WHITE, 0.08))
        # Fill
        if segP > 0:
            fw = max(4, int((segW - 4) * segP))
            draw_rounded_rect(draw, (x, barY, x + fw, barY + barH), 5,
                              fill=s["color"])
        x += segW

    # Scene label + time
    scene = next((s for s in scenes if s["start"] <= t < s["end"]), scenes[-1])
    left_text(draw, scene["label"], pad, barY + 30, font_mono(24), fill=GRAY)
    right_text(draw, f"{int(t)}s / {duration}s", W - pad, barY + 30, font_mono(24), fill=GRAY)


def draw_caption(draw, t, captions):
    """
    Draw 3-5 word caption overlay at bottom of frame.
    captions: list of (start_time, end_time, text) tuples.
    """
    cap = next((c for c in captions if c[0] <= t < c[1]), None)
    if not cap:
        return

    text = cap[2]
    cy = H - 170
    f = font_mono(48, bold=True)
    bbox = f.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pw, ph = tw + 50, th + 28

    rx, ry = W // 2 - pw // 2, cy - ph // 2
    draw_rounded_rect(draw, (rx, ry, rx + pw, ry + ph), 14,
                      fill=rgba((0, 0, 0), 0.75))
    centered_text(draw, text, W // 2, cy, f, fill=WHITE)


def make_render_frame(scenes, captions, scene_renderers, duration):
    """
    Returns a render_frame(t) function that draws any frame at time t.

    scenes: list of scene dicts
    captions: list of (start, end, text) tuples
    scene_renderers: dict mapping scene_id → draw_scene_N(draw, img, progress)
    duration: total video duration in seconds
    """
    from PIL import Image, ImageDraw

    def render_frame(t):
        img = Image.new('RGB', (W, H), BG)
        draw = ImageDraw.Draw(img)

        scene = next((s for s in scenes if s["start"] <= t < s["end"]), scenes[-1])
        progress = max(0, min(1, (t - scene["start"]) / (scene["end"] - scene["start"])))

        # Render scene content
        renderer = scene_renderers.get(scene["id"])
        if renderer:
            renderer(draw, img, progress)

        # Overlay shared elements
        draw_progress_bar(draw, t, scenes, duration)
        draw_caption(draw, t, captions)

        return img

    return render_frame
