#!/usr/bin/env python3
"""
Video #5: Context Window Erosion — MP4 Renderer
1080x1920 @30fps, H.264, 57 seconds
Renders directly to FFmpeg via stdin pipe (no temp files)
"""

import subprocess
import sys
import math
import struct
from PIL import Image, ImageDraw, ImageFont

# ── Config ──────────────────────────────────────────────────
W, H = 1080, 1920
FPS = 30
DURATION = 57
TOTAL_FRAMES = DURATION * FPS
OUTPUT = "/home/claude/Video5_ContextErosion_1080x1920_30fps.mp4"

# ── Colors ──────────────────────────────────────────────────
BG      = (13, 17, 23)
RED     = (255, 59, 48)
GREEN   = (0, 255, 136)
BLUE    = (0, 122, 255)
YELLOW  = (255, 214, 10)
WHITE   = (240, 246, 252)
GRAY    = (139, 148, 158)
DARK    = (45, 51, 59)

def rgba(color, alpha):
    """Blend color with BG at given alpha."""
    return tuple(int(c * alpha + b * (1 - alpha)) for c, b in zip(color, BG))

# ── Fonts ───────────────────────────────────────────────────
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
def font(size, bold=False):
    name = "DejaVuSansMono-Bold.ttf" if bold else "DejaVuSansMono.ttf"
    return ImageFont.truetype(FONT_DIR + name, size)

def font_sans(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(FONT_DIR + name, size)

# ── Scenes ──────────────────────────────────────────────────
SCENES = [
    {"id":1, "start":0,  "end":5,  "label":"COLD OPEN",    "color":RED},
    {"id":2, "start":5,  "end":12, "label":"PROMISE LOCK",  "color":BLUE},
    {"id":3, "start":12, "end":25, "label":"THE PROBLEM",   "color":YELLOW},
    {"id":4, "start":25, "end":38, "label":"THE CLIFF",     "color":RED},
    {"id":5, "start":38, "end":48, "label":"THE FIX",       "color":GREEN},
    {"id":6, "start":48, "end":57, "label":"CLIFFHANGER",   "color":RED},
]

CAPTIONS = [
    (0.0,1.0,"Your AI agent"),(1.0,2.0,"is getting dumber"),(2.0,3.2,"with every message —"),
    (3.2,4.1,"and there's no"),(4.1,5.0,"error log telling you."),
    (5.0,6.2,"This is context"),(6.2,7.4,"window erosion —"),(7.4,8.8,"the #1 way agents"),
    (8.8,10.0,"silently degrade."),(10.0,11.0,"I see it in"),(11.0,12.0,"every system I audit."),
    (12.0,13.2,"Every conversation turn"),(13.2,14.5,"adds tokens to memory."),
    (14.5,15.8,"Instructions, tool results,"),(15.8,17.0,"user messages —"),
    (17.0,18.2,"they all pile up."),(18.2,19.8,"Your original instructions"),
    (19.8,21.0,"get buried."),(21.0,22.5,"The agent can"),
    (22.5,23.5,"still see them."),(23.5,25.0,"But stops paying attention."),
    (25.0,26.5,"The degradation"),(26.5,27.8,"isn't gradual."),(27.8,29.0,"It's a cliff."),
    (29.0,30.5,"Performance holds steady"),(30.5,32.0,"at 60-70% utilization —"),
    (32.0,33.5,"then drops off a cliff."),(33.5,35.0,"The agent starts"),
    (35.0,36.2,"hallucinating, looping,"),(36.2,38.0,"or phantom instructions."),
    (38.0,39.2,"The fix:"),(39.2,40.8,"measure context health"),
    (40.8,42.0,"on every turn."),(42.0,43.5,"Compute the ratio of"),
    (43.5,44.8,"signal to context."),(44.8,46.0,"Below threshold?"),
    (46.0,47.2,"Trigger a reset."),(47.2,48.0,"20 min to implement."),
    (48.0,49.5,"Context erosion is"),(49.5,51.0,"the failure mode"),
    (51.0,52.5,"you can see coming."),(52.5,54.0,"The next one —"),
    (54.0,55.5,"you can't."),(55.5,57.0,"The reasoning has collapsed."),
]

# ── Drawing Helpers ─────────────────────────────────────────
def draw_rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    x0, y0, x1, y1 = xy
    r = min(radius, (x1-x0)//2, (y1-y0)//2)
    if fill:
        draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)
    elif outline:
        draw.rounded_rectangle(xy, radius=r, outline=outline, width=width)

def centered_text(draw, text, cx, cy, f, fill=WHITE):
    bbox = f.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw//2, cy - th//2), text, font=f, fill=fill)

def left_text(draw, text, x, cy, f, fill=WHITE):
    bbox = f.getbbox(text)
    th = bbox[3] - bbox[1]
    draw.text((x, cy - th//2), text, font=f, fill=fill)

def right_text(draw, text, x, cy, f, fill=WHITE):
    bbox = f.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((x - tw, cy - th//2), text, font=f, fill=fill)

# ── Scene Renderers ─────────────────────────────────────────
def draw_scene1(draw, img, p):
    """Glitching Brain"""
    cx, cy = W//2, int(H*0.38)
    gx = int(math.sin(p*40)*12)
    gy = int(math.cos(p*35)*8)
    gi = 0.5 + math.sin(p*20)*0.5
    scale = 0.8 + p*0.3
    r = int(170*scale)

    # Scan lines
    for y in range(0, H, 6):
        draw.rectangle([0, y, W, y+2], fill=rgba(RED, 0.015))

    # Ghost circle (red offset)
    ghost_cx = cx + gx + int(gi*8)
    draw.ellipse([ghost_cx-r, cy+gy-r, ghost_cx+r, cy+gy+r], outline=rgba(RED, 0.3), width=3)

    # Main circle
    bcx, bcy = cx+gx, cy+gy
    draw.ellipse([bcx-r, bcy-r, bcx+r, bcy+r], outline=RED, width=5)

    # Brain ellipse
    br = int(r*0.55)
    bh = int(r*0.6)
    draw.ellipse([bcx-br, bcy-bh-10, bcx+br, bcy+bh-10], fill=rgba(RED, 0.08), outline=(255,107,107), width=3)

    # Neural nodes
    ns = int(40*scale)
    nodes = [
        (bcx-ns, bcy-int(50*scale)),
        (bcx+ns, bcy-int(50*scale)),
        (bcx, bcy),
        (bcx-int(20*scale), bcy+int(50*scale)),
        (bcx+int(20*scale), bcy+int(50*scale)),
    ]
    # Connections
    line_col = rgba((255,107,107), 0.5+gi*0.5)
    for i in [0,1]:
        draw.line([nodes[i], nodes[2]], fill=line_col, width=3)
    for i in [3,4]:
        draw.line([nodes[2], nodes[i]], fill=line_col, width=3)
    # Dots
    for i, (nx, ny) in enumerate(nodes):
        nr = int(10*scale) if i != 2 else int(14*scale)
        dot_col = RED if i != 2 else (255,107,107)
        draw.ellipse([nx-nr, ny-nr, nx+nr, ny+nr], fill=dot_col)

    # Warning icon
    centered_text(draw, "⚠", bcx, bcy+r+30, font(48), fill=rgba(RED, gi))

    # CONTEXT EROSION text
    if p > 0.4:
        op = min(1.0, (p-0.4)/0.2)
        ty = int(cy + r + 120 + (1-op)*40)
        col = rgba(RED, op)
        centered_text(draw, "CONTEXT EROSION", cx, ty, font(64, bold=True), fill=col)


def draw_scene2(draw, img, p):
    """Token Container Filling"""
    cx = W//2
    cW, cH = 460, 900
    cX, cY = cx - cW//2, int(H*0.15) + 80
    fillH = int((15 + p*55)/100 * cH)
    labelOp = max(0, 1 - p*1.8)

    centered_text(draw, "CONTEXT WINDOW", cx, cY-50, font(32), fill=GRAY)

    # Container outline
    draw_rounded_rect(draw, (cX, cY, cX+cW, cY+cH), 20, outline=BLUE, width=4)

    # Fill gradient (simplified as solid blend)
    if fillH > 0:
        fy = cY + cH - fillH
        draw_rounded_rect(draw, (cX+2, fy, cX+cW-2, cY+cH-2), 18, fill=rgba(BLUE, 0.5))

    # Token blocks
    nBlocks = min(9, int(p*8) + 1)
    labels = ['SYSTEM PROMPT','tool_result_1','tool_result_2','user_msg_3','user_msg_4','user_msg_5','user_msg_6','user_msg_7','user_msg_8']
    colors = [GREEN, BLUE, BLUE, YELLOW, YELLOW, YELLOW, BLUE, YELLOW, RED]
    blockH, gap = 60, 78

    for i in range(nBlocks):
        bY = cY + cH - 30 - (i+1)*gap
        if bY < cY + 10:
            continue
        op = labelOp if i == 0 else min(1.0, (p*8 - i) + 0.5)
        if op <= 0:
            continue
        c = colors[i]
        bc = rgba(c, 0.3 * op)
        oc = rgba(c, 0.6 * op)
        draw_rounded_rect(draw, (cX+20, bY, cX+cW-20, bY+blockH), 10, fill=bc, outline=oc, width=2)
        tc = rgba(GREEN if i==0 else GRAY, op)
        centered_text(draw, labels[i], cx, bY+blockH//2, font(20), fill=tc)

    # Utilization %
    pct = int(15 + p*55)
    pc = YELLOW if pct > 55 else BLUE
    right_text(draw, f"{pct}%", cX+cW-30, cY+35, font(36, bold=True), fill=pc)

    centered_text(draw, "Source: Production agent diagnostics", cx, cY+cH+45, font(24), fill=rgba(BLUE, 0.6))


def draw_scene3(draw, img, p):
    """Instructions Getting Buried"""
    cx = W//2
    numBlocks = min(12, int(p*14)+2)
    instOp = max(0.08, 1-p*2.5)
    instScale = max(0.4, 1-p*0.8)
    meterVal = (85-p*30) if p < 0.7 else (85-0.7*30-(p-0.7)*150)
    meterVal = max(0, meterVal)
    mc = GREEN if meterVal > 60 else YELLOW if meterVal > 30 else RED

    # Quality meter
    mX, mY, mW, mH = 100, int(H*0.18), 50, 700
    centered_text(draw, "QUALITY", mX+mW//2, mY-25, font(22), fill=GRAY)
    draw_rounded_rect(draw, (mX, mY, mX+mW, mY+mH), 14, fill=rgba(WHITE, 0.03), outline=rgba(WHITE, 0.1), width=2)
    fillPx = max(10, int(meterVal/100*mH))
    draw_rounded_rect(draw, (mX+3, mY+mH-fillPx, mX+mW-3, mY+mH-3), 12, fill=mc)
    centered_text(draw, f"{int(meterVal)}%", mX+mW//2, mY+mH+30, font(28, bold=True), fill=mc)

    # Token stack
    sX, sY, sW, sH = 250, int(H*0.15), 620, 1000
    draw_rounded_rect(draw, (sX, sY, sX+sW, sY+sH), 20, outline=rgba(WHITE, 0.1), width=3)

    # System instructions
    iH = int(75*instScale)
    ic = rgba(GREEN, instOp)
    iY = sY+sH-20-iH
    draw_rounded_rect(draw, (sX+16, iY, sX+sW-16, iY+iH), 10, fill=rgba(GREEN, 0.12*instOp), outline=ic, width=2)
    label = "SYSTEM INSTRUCTIONS" if instScale > 0.6 else "SYS..."
    centered_text(draw, label, sX+sW//2, iY+iH//2, font(int(20*instScale)), fill=ic)

    # Stacking blocks
    bColors = [BLUE,BLUE,YELLOW,YELLOW,(255,107,107),(255,107,107),BLUE,YELLOW,(255,107,107),RED,RED,RED]
    bLabels = ['tool_call','api_resp','user_q','agent_a','error_ctx','retry','tool_2','user_q2','history','noise','noise','overflow']
    for i in range(numBlocks):
        bY = sY+sH-110-i*58
        op = min(1.0, (p*14-i)*2)
        if op <= 0 or bY < sY+10:
            continue
        c = bColors[i % len(bColors)]
        draw_rounded_rect(draw, (sX+16, bY, sX+sW-16, bY+46), 8, fill=rgba(c, 0.12*op), outline=rgba(c, 0.35*op), width=2)
        left_text(draw, bLabels[i % len(bLabels)], sX+35, bY+23, font(18), fill=rgba(c, op))


def draw_scene4(draw, img, p):
    """The Cliff Chart"""
    cx = W//2
    cW, cH = 880, 580
    cX = (W-cW)//2
    cY = int(H*0.22)
    drawP = min(1, p*1.8)
    dropP = max(0, min(1, (p-0.35)*2.5))
    zoneOp = max(0, (p-0.5)*2)
    failOp = max(0, (p-0.7)*3)

    centered_text(draw, "AGENT OUTPUT QUALITY vs CONTEXT UTILIZATION", cx, cY-50, font(26), fill=GRAY)

    # Grid lines
    for i in range(5):
        y = cY + i*cH//4
        draw.line([(cX, y), (cX+cW, y)], fill=rgba(WHITE, 0.04), width=1)

    # Red danger zone
    if zoneOp > 0:
        zx = cX + int(cW*0.6)
        draw.rectangle([zx, cY, cX+cW, cY+cH], fill=rgba(RED, 0.08*zoneOp))

    # Stable line (green)
    stable = [(0,0.3),(0.15,0.28),(0.3,0.27),(0.5,0.26),(0.58,0.26)]
    if drawP > 0:
        pts = []
        for i, (fx, fy) in enumerate(stable):
            seg = i / len(stable)
            if seg > drawP and i > 0:
                # Interpolate
                prev = stable[i-1]
                t = (drawP - (i-1)/len(stable)) / (1/len(stable))
                fx = prev[0] + (fx-prev[0])*t
                fy = prev[1] + (fy-prev[1])*t
                pts.append((cX+int(fx*cW), cY+int(fy*cH)))
                break
            pts.append((cX+int(fx*cW), cY+int(fy*cH)))
        if len(pts) >= 2:
            draw.line(pts, fill=GREEN, width=6)

    # Drop line (red)
    drop = [(0.58,0.26),(0.66,0.5),(0.76,0.78),(0.85,0.88),(0.92,0.93)]
    if dropP > 0:
        pts = []
        for i, (fx, fy) in enumerate(drop):
            seg = i / len(drop)
            if seg > dropP and i > 0:
                prev = drop[i-1]
                t = (dropP - (i-1)/len(drop)) / (1/len(drop))
                fx = prev[0] + (fx-prev[0])*t
                fy = prev[1] + (fy-prev[1])*t
                pts.append((cX+int(fx*cW), cY+int(fy*cH)))
                break
            pts.append((cX+int(fx*cW), cY+int(fy*cH)))
        if len(pts) >= 2:
            draw.line(pts, fill=RED, width=7)

    # Cliff annotation
    if dropP > 0.3:
        op = min(1, (dropP-0.3)*3)
        cliffX = cX+int(cW*0.58)
        draw.line([(cliffX, cY-10),(cliffX, cY+cH+10)], fill=rgba(RED, 0.5*op), width=2)
        left_text(draw, "THE CLIFF", cliffX+16, cY-25, font(28, bold=True), fill=rgba(RED, op))

    # Axes
    axY = cY+cH+40
    centered_text(draw, "0%", cX, axY, font(22), fill=GRAY)
    centered_text(draw, "33%", cX+int(cW*0.33), axY, font(22), fill=GRAY)
    centered_text(draw, "65%", cX+int(cW*0.58), axY, font(22, bold=True), fill=YELLOW)
    centered_text(draw, "100%", cX+cW, axY, font(22), fill=GRAY)
    right_text(draw, "High", cX-15, cY+20, font(20), fill=GRAY)
    right_text(draw, "Low", cX-15, cY+cH-20, font(20), fill=GRAY)

    # Failure cards
    if failOp > 0:
        cards = [("Loop", RED), ("Hallucinate", RED), ("Phantom", RED)]
        cardW, cardH, gap = 200, 100, 40
        totalW = len(cards)*cardW + (len(cards)-1)*gap
        startX = (W-totalW)//2
        cardY = cY+cH+100
        for i, (label, c) in enumerate(cards):
            x = startX + i*(cardW+gap)
            draw_rounded_rect(draw, (x, cardY, x+cardW, cardY+cardH), 14,
                fill=rgba(RED, 0.05*failOp), outline=rgba(RED, 0.2*failOp), width=2)
            icons = ["↻","?!","⚡"]
            centered_text(draw, icons[i], x+cardW//2, cardY+35, font(32, bold=True), fill=rgba(RED, failOp))
            centered_text(draw, label, x+cardW//2, cardY+75, font(22), fill=rgba((255,107,107), failOp))


def draw_scene5(draw, img, p):
    """The Fix - Architecture Diagram"""
    cx = W//2
    s1 = min(1, p*3)
    s2 = max(0, min(1, (p-0.25)*3))
    s3 = max(0, min(1, (p-0.5)*3))
    chk = max(0, (p-0.8)*5)

    # Title
    centered_text(draw, "CONTEXT HEALTH MONITOR", cx, int(H*0.12), font(32, bold=True), fill=rgba(GREEN, s1))

    # Nodes
    nodes = [
        (H*0.22, "Every Agent Turn", "compute health score", BLUE, s1),
        (H*0.36, "Signal / Context", "instruction ratio", YELLOW, s1),
        (H*0.50, "Above Threshold?", "decision gate", YELLOW, s2),
    ]
    nW, nH = 560, 130
    for i, (ny, label, sub, color, op) in enumerate(nodes):
        if op <= 0:
            continue
        ny = int(ny + (1-op)*30)
        x0, y0 = cx-nW//2, ny
        draw_rounded_rect(draw, (x0, y0, x0+nW, y0+nH), 18,
            fill=rgba(color, 0.06*op), outline=rgba(color, 0.35*op), width=3)
        centered_text(draw, label, cx, y0+45, font(32, bold=True), fill=rgba(color, op))
        centered_text(draw, sub, cx, y0+90, font(22), fill=rgba(GRAY, op))
        # Connector
        if i < 2:
            cop = s1 if i==0 else s2
            if cop > 0:
                next_ny = int(nodes[i+1][0] + (1-nodes[i+1][4])*30)
                draw.line([(cx, y0+nH+5), (cx, next_ny-5)], fill=rgba(WHITE, 0.12*cop), width=4)

    # Branch
    if s3 > 0:
        bY = int(H*0.62)
        bW, bH, gap = 280, 110, 40
        # Continue
        x0 = cx-bW-gap//2
        draw_rounded_rect(draw, (x0, bY, x0+bW, bY+bH), 18,
            fill=rgba(GREEN, 0.06*s3), outline=rgba(GREEN, 0.3*s3), width=3)
        centered_text(draw, "Continue", x0+bW//2, bY+40, font(28, bold=True), fill=rgba(GREEN, s3))
        centered_text(draw, "above threshold", x0+bW//2, bY+80, font(20), fill=rgba(GRAY, s3))
        # Reset
        x1 = cx+gap//2
        draw_rounded_rect(draw, (x1, bY, x1+bW, bY+bH), 18,
            fill=rgba(RED, 0.06*s3), outline=rgba(RED, 0.3*s3), width=3)
        centered_text(draw, "Reset", x1+bW//2, bY+40, font(28, bold=True), fill=rgba(RED, s3))
        centered_text(draw, "below threshold", x1+bW//2, bY+80, font(20), fill=rgba(GRAY, s3))

    # 20 min badge
    if chk > 0:
        bY = int(H*0.76)
        draw_rounded_rect(draw, (cx-250, bY-30, cx+250, bY+30), 30,
            fill=rgba(GREEN, 0.06*chk), outline=rgba(GREEN, 0.25*chk), width=2)
        centered_text(draw, "20 min to implement", cx, bY, font(32, bold=True), fill=rgba(GREEN, chk))


def draw_scene6(draw, img, p):
    """Cliffhanger"""
    cx, cy = W//2, int(H*0.4)
    crk = min(1, p*2)
    txtOp = max(0, (p-0.3)*2)
    nextOp = max(0, (p-0.55)*2.5)
    handleOp = max(0, (p-0.75)*4)

    # Crack lines
    if crk > 0:
        lc = rgba(RED, 0.3*crk)
        draw.line([(cx, 0), (cx-80, int(H*0.3))], fill=lc, width=3)
        draw.line([(cx-80, int(H*0.3)), (cx+40, int(H*0.65))], fill=lc, width=2)
        draw.line([(cx, 0), (cx+100, int(H*0.25))], fill=lc, width=2)
        draw.line([(cx+100, int(H*0.25)), (cx-40, int(H*0.75))], fill=lc, width=2)

    if txtOp > 0:
        centered_text(draw, "COMING NEXT", cx, cy-100, font(38, bold=True), fill=rgba(RED, txtOp))

    if nextOp > 0:
        ty = int(cy + 20 + (1-nextOp)*40)
        nc = rgba(WHITE, nextOp)
        centered_text(draw, "Confident", cx, ty, font_sans(72, bold=True), fill=nc)
        centered_text(draw, "Hallucination", cx, ty+90, font_sans(72, bold=True), fill=nc)
        centered_text(draw, "When perfect outputs hide broken reasoning", cx, ty+170, font(28), fill=rgba(GRAY, nextOp))

    if handleOp > 0:
        bY = int(H*0.72)
        draw_rounded_rect(draw, (cx-230, bY, cx+230, bY+70), 35,
            fill=rgba(RED, 0.1*handleOp), outline=rgba(RED, 0.3*handleOp), width=3)
        centered_text(draw, "FOLLOW FOR PART 2", cx, bY+35, font(32, bold=True), fill=rgba(RED, handleOp))
        centered_text(draw, "@mldeep", cx, bY+100, font(28), fill=rgba(GRAY, handleOp))


# ── Progress Bar + Captions ─────────────────────────────────
def draw_progress_bar(draw, t):
    barY, barH, pad = 55, 10, 40
    totalW = W - pad*2
    x = pad
    for s in SCENES:
        segW = int(((s["end"]-s["start"])/DURATION)*totalW)
        segP = 0 if t < s["start"] else (1 if t > s["end"] else (t-s["start"])/(s["end"]-s["start"]))
        draw_rounded_rect(draw, (x, barY, x+segW-4, barY+barH), 5, fill=rgba(WHITE, 0.08))
        if segP > 0:
            fw = max(4, int((segW-4)*segP))
            draw_rounded_rect(draw, (x, barY, x+fw, barY+barH), 5, fill=s["color"])
        x += segW

    # Labels
    scene = next((s for s in SCENES if s["start"] <= t < s["end"]), SCENES[-1])
    left_text(draw, scene["label"], pad, barY+30, font(24), fill=GRAY)
    right_text(draw, f"{int(t)}s / {DURATION}s", W-pad, barY+30, font(24), fill=GRAY)


def draw_caption(draw, t):
    cap = next((c for c in CAPTIONS if c[0] <= t < c[1]), None)
    if not cap:
        return
    text = cap[2]
    cy = H - 170
    f = font(48, bold=True)
    bbox = f.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pw, ph = tw + 50, th + 28
    rx, ry = W//2-pw//2, cy-ph//2
    draw_rounded_rect(draw, (rx, ry, rx+pw, ry+ph), 14, fill=rgba((0,0,0), 0.75))
    centered_text(draw, text, W//2, cy, f, fill=WHITE)


# ── Main Render ─────────────────────────────────────────────
def render_frame(t):
    img = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(img)

    scene = next((s for s in SCENES if s["start"] <= t < s["end"]), SCENES[-1])
    p = max(0, min(1, (t - scene["start"]) / (scene["end"] - scene["start"])))

    renderers = {1: draw_scene1, 2: draw_scene2, 3: draw_scene3,
                 4: draw_scene4, 5: draw_scene5, 6: draw_scene6}
    renderers[scene["id"]](draw, img, p)

    draw_progress_bar(draw, t)
    draw_caption(draw, t)

    return img


def main():
    print(f"Rendering {TOTAL_FRAMES} frames at {W}x{H} @{FPS}fps...")
    print(f"Output: {OUTPUT}")

    # FFmpeg command: read raw RGB from stdin, encode H.264 MP4
    cmd = [
        'ffmpeg', '-y',
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-pix_fmt', 'rgb24',
        '-s', f'{W}x{H}',
        '-r', str(FPS),
        '-i', '-',
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '18',         # High quality
        '-pix_fmt', 'yuv420p', # Compatibility
        '-movflags', '+faststart', # Web-friendly
        '-an',                 # No audio (voiceover added separately)
        OUTPUT
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    for frame in range(TOTAL_FRAMES):
        t = frame / FPS
        img = render_frame(t)
        proc.stdin.write(img.tobytes())

        if frame % FPS == 0:
            pct = frame / TOTAL_FRAMES * 100
            print(f"  {pct:5.1f}% — {int(t)}s / {DURATION}s", flush=True)

    proc.stdin.close()
    stderr = proc.stderr.read().decode()
    proc.wait()

    if proc.returncode == 0:
        import os
        size_mb = os.path.getsize(OUTPUT) / 1024 / 1024
        print(f"\n✅ Done! {OUTPUT} ({size_mb:.1f} MB)")
    else:
        print(f"\n❌ FFmpeg error:\n{stderr}")
        sys.exit(1)


if __name__ == '__main__':
    main()
