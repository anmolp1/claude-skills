# Scene Animation Cookbook

Reusable animation patterns for rendering scenes with Pillow. Each pattern is a building block — combine them to create full scenes.

## Core Principle

Every animation is derived from a single `progress` value (0.0 → 1.0) that represents how far into the scene we are. All motion, opacity, scale, and position changes are pure functions of progress. No state, no timers.

## Easing Functions

```python
import math

def ease_in(p):       return p * p
def ease_out(p):      return 1 - (1 - p) * (1 - p)
def ease_in_out(p):   return 3*p*p - 2*p*p*p

# Staggered reveal: element N appears at progress = N * delay
def stagger(progress, index, delay=0.15):
    return max(0, min(1, (progress - index * delay) / (1 - index * delay)))

# Delayed start: nothing happens until threshold, then 0→1
def delayed(progress, start=0.3, speed=2.0):
    return max(0, min(1, (progress - start) * speed))
```

## Pattern: Glitch Effect
For broken/corrupted visuals (errors, failures, warnings).

```python
def glitch_offset(progress, intensity=12):
    """Returns (x, y) pixel offset for chromatic aberration effect."""
    gx = int(math.sin(progress * 40) * intensity)
    gy = int(math.cos(progress * 35) * intensity * 0.7)
    return gx, gy

def glitch_intensity(progress):
    """Oscillating 0-1 value for flickering elements."""
    return 0.5 + math.sin(progress * 20) * 0.5

# Usage: Draw the same element twice — once offset in red (ghost), once in main position
# Scan lines: horizontal lines every 6px with very low opacity red
```

## Pattern: Filling Container
For showing accumulation (tokens, data, memory usage).

```python
def container_fill(progress, min_pct=15, max_pct=70):
    """Returns fill percentage for a container."""
    return min_pct + progress * (max_pct - min_pct)

def stacking_blocks(progress, max_blocks=9):
    """Returns how many blocks should be visible."""
    return min(max_blocks, int(progress * (max_blocks + 2)) + 1)

def fading_label(progress, fade_speed=1.8):
    """First item fades as others pile on top."""
    return max(0, 1 - progress * fade_speed)
```

Draw a rounded rectangle as the container, a gradient fill from bottom, and small labeled blocks stacking inside.

## Pattern: Quality Meter
Vertical bar that drains from green → yellow → red.

```python
def meter_value(progress, start=85, end=-20):
    """Returns 0-100 value, optionally with cliff behavior."""
    if progress < 0.7:
        return start - progress * 30
    else:
        return start - 0.7 * 30 - (progress - 0.7) * 150

def meter_color(value):
    """Returns RGB tuple based on value."""
    if value > 60: return (0, 255, 136)    # Green
    if value > 30: return (255, 214, 10)   # Yellow
    return (255, 59, 48)                     # Red
```

Draw as a narrow rounded rect with a fill from bottom, colored by the current value.

## Pattern: Animated Line Chart
For showing performance curves and cliff drops.

```python
def draw_line_chart(draw, points, progress, box, color, width=6):
    """
    points: list of (x_frac, y_frac) where 0,0 is top-left of box
    progress: 0-1 controls how much of the line is drawn
    box: (x, y, w, h) chart area
    """
    x, y, w, h = box
    visible = []
    for i, (fx, fy) in enumerate(points):
        seg = i / len(points)
        if seg > progress and i > 0:
            # Interpolate to exact progress point
            prev = points[i-1]
            t = (progress - (i-1)/len(points)) / (1/len(points))
            fx = prev[0] + (fx - prev[0]) * t
            fy = prev[1] + (fy - prev[1]) * t
            visible.append((x + int(fx*w), y + int(fy*h)))
            break
        visible.append((x + int(fx*w), y + int(fy*h)))
    if len(visible) >= 2:
        draw.line(visible, fill=color, width=width)
```

Typical usage: draw a green stable line (0-60% x-axis), then a red dropping line (60-100%).

## Pattern: Architecture Diagram
For showing systems, flows, decision gates.

```python
def flow_nodes(draw, cx, nodes, progress):
    """
    nodes: list of (y, label, sublabel, color, stagger_index)
    Draws rounded rect nodes with connectors, staggered reveal.
    """
    nW, nH = 560, 130
    for i, (ny, label, sub, color, si) in enumerate(nodes):
        op = stagger(progress, si, delay=0.25)
        if op <= 0: continue
        # Draw node with opacity
        # Draw connector line to next node
```

Branch pattern: at the bottom, two side-by-side cards (Continue/Reset, Accept/Reject, Pass/Fail).

## Pattern: Crack Effect
For cliffhangers, broken systems, dramatic endings.

```python
def draw_cracks(draw, cx, cy, progress, color, width_range=(1, 3)):
    """Draw diagonal crack lines emanating from center."""
    op = min(1, progress * 2) * 0.35
    lines = [
        (cx, 0, cx-80, cy*0.6),
        (cx-80, cy*0.6, cx+40, cy*1.3),
        (cx, 0, cx+100, cy*0.5),
        (cx+100, cy*0.5, cx-40, cy*1.5),
    ]
    for x1, y1, x2, y2 in lines:
        draw.line([(int(x1),int(y1)), (int(x2),int(y2))],
                  fill=rgba(color, op), width=random.choice(range(*width_range)))
```

## Pattern: Badge / Pill
For callouts, time estimates, CTAs.

```python
def draw_badge(draw, cx, cy, text, color, progress, font):
    """Pill-shaped badge that scales in."""
    op = max(0, (progress - 0.8) * 5)
    if op <= 0: return
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    pw, ph = tw + 50, 60
    draw_rounded_rect(draw, (cx-pw//2, cy-ph//2, cx+pw//2, cy+ph//2),
                      ph//2, fill=rgba(color, 0.08*op), outline=rgba(color, 0.25*op))
    centered_text(draw, text, cx, cy, font, fill=rgba(color, op))
```

## Pattern: Text Reveal
For titles, labels, key terms.

```python
def text_with_reveal(draw, text, cx, cy, font, color, progress, delay=0.3):
    """Text that fades in and slides up."""
    op = max(0, min(1, (progress - delay) * 2.5))
    if op <= 0: return
    ty = int(cy + (1 - op) * 30)  # Slide up 30px
    centered_text(draw, text, cx, ty, font, fill=rgba(color, op))
```

## Combining Patterns into Scenes

A typical scene combines 2-3 patterns:

**"The Problem" scene:**
- Filling Container (background) + Fading Label (system prompt fading) + Quality Meter (side)

**"The Cliff" scene:**
- Line Chart (main) + Text Reveal ("THE CLIFF" annotation) + Badge cards (failure modes)

**"The Fix" scene:**
- Architecture Diagram (nodes + connectors) + Badge ("20 min to implement")

**"Cliffhanger" scene:**
- Crack Effect (background) + Text Reveal (staggered: "Coming Next" → title → subtitle → CTA)

## Color Blending

Since Pillow doesn't support alpha compositing on RGB images natively, use this helper everywhere:

```python
BG = (13, 17, 23)  # Background color

def rgba(color, alpha):
    """Blend color with background at given alpha. Returns RGB tuple."""
    return tuple(int(c * alpha + b * (1 - alpha)) for c, b in zip(color, BG))
```

This gives the appearance of transparency without needing RGBA mode.
