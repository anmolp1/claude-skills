---
name: reel-maker
user-invocable: true
description: "Create production-ready YouTube Shorts and Instagram Reels as MP4 video files with animated motion graphics, timed captions, and scene transitions. Use this skill whenever the user asks to make a reel, Short, vertical video, TikTok, 9:16 video, animated explainer, or short-form video content. Also trigger when the user says 'render a video', 'export as MP4', 'create a Short for [topic]', 'make an animated reel', or references producing video content from a script or outline. This skill handles the full pipeline: scriptwriting, animated preview, and final MP4 export via Pillow + FFmpeg."
---

# Reel Maker

Create production-ready YouTube Shorts / Instagram Reels with animated motion graphics, timed captions, and H.264 MP4 export.

## What This Skill Produces

Given a topic, outline, or script → this skill outputs:
1. A **6-scene narration script** with timestamped caption chunks
2. An **animated React preview** (optional, for timing/pacing review)
3. A **1080×1920 @30fps H.264 MP4** with animated visuals
4. A **narrated MP4** with TTS audio muxed in (Dia, Higgs Audio, or Flite)

## Dependencies

**Core (always required):**
- Python 3 with Pillow (`pip install pillow --break-system-packages` if needed)
- FFmpeg (system-installed, verify with `which ffmpeg`)
- DejaVu fonts (standard on Ubuntu; on macOS/Windows the renderer falls back to system fonts automatically)

**TTS — install one (in order of quality):**
- **Dia** (recommended): `pip install git+https://github.com/nari-labs/dia.git` + CUDA GPU (~4.4GB)
- **Higgs Audio API**: `pip install requests` + set `DEEPINFRA_API_KEY` env var
- **Flite** (fallback): `libflite` system package (pre-installed on Ubuntu)

**Preview (optional):**
- React artifact with Tone.js (available in Claude artifacts)

## Workflow

### Phase 1: Script

Read `references/script_rules.md` before writing the script.

**Input:** A topic, video outline, or brief description.
**Output:** A markdown file containing:

```
- Scene breakdown (6 scenes with timestamps, labels, colors)
- Full narration (~155-170 words for 55-60 seconds)
- Caption chunks array: [startTime, endTime, "3-5 words"] per chunk
- Cross-link target (which video the cliffhanger teases)
```

The 6-scene structure is always:

| # | Scene | Time | Purpose |
|---|-------|------|---------|
| 1 | Cold Open | 0:00-0:05 | Provocative hook, no preamble |
| 2 | Promise Lock | 0:05-0:12 | Name the concept + credibility spike |
| 3 | The Problem | 0:12-0:25 | Build the mechanic step by step |
| 4 | The Evidence | 0:25-0:38 | Dramatic escalation (the "cliff" moment) |
| 5 | The Fix | 0:38-0:48 | Actionable solution, time-boxed |
| 6 | Cliffhanger | 0:48-0:57 | Tease next video, open loop |

### Phase 2: Animated Preview (Optional)

If the user wants to preview before rendering, create a React JSX artifact:

- Each scene is a component receiving `progress` (0→1)
- Captions displayed as 3-5 word chunks in a pill overlay at the bottom
- Segmented progress bar at top, color-coded per scene
- Tone.js audio: ambient drone (PolySynth FM, C2+G2, -26dB through LowPass 350Hz + Reverb), scene transition hits (MembraneSynth), caption ticks (MetalSynth, -32dB)
- Controls: play/pause, restart, mute, scene jump buttons

**Important:** `speechSynthesis` is blocked in artifact iframes. Use only Tone.js for audio. Voiceover is recorded separately.

### Phase 3: Render to MP4

This is the production pipeline. Read `references/export_specs.md` for the locked FFmpeg command and codec specs.

**Step 1:** Import shared helpers:
```python
# Copy core/drawing.py and core/scene_base.py to working directory
# These provide: draw_rounded_rect, centered_text, left_text, right_text,
#                rgba, draw_progress_bar, draw_caption, render_frame shell
```

**Step 2:** Write scene renderers. Each scene is a function:
```python
def draw_scene_N(draw, img, progress):
    # progress is 0.0 → 1.0 across the scene's duration
    # Use draw (ImageDraw) and img (PIL Image) to render
    # All animation derived from progress via easing math
```

For animation patterns (glitch effects, filling containers, charts, diagrams, crack effects), read `references/scene_cookbook.md`.

For a complete working example, read `examples/video5_context_erosion.py`.

**Step 3:** Render and pipe to FFmpeg:
```python
from core.renderer import render_to_mp4
render_to_mp4(scenes, captions, scene_renderers, output_path)
```

**Step 4:** Validate output:
```bash
ffprobe -v quiet -print_format json -show_streams output.mp4
```
Verify: codec=h264, 1080×1920, 30fps, yuv420p, correct frame count.

## Design System (Locked)

| Element | Value |
|---------|-------|
| Background | `(13, 17, 23)` / #0D1117 |
| Alert Red | `(255, 59, 48)` / #FF3B30 |
| Data Green | `(0, 255, 136)` / #00FF88 |
| Electric Blue | `(0, 122, 255)` / #007AFF |
| Warning Yellow | `(255, 214, 10)` / #FFD60A |
| Text White | `(240, 246, 252)` / #F0F6FC |
| Muted Gray | `(139, 148, 158)` / #8B949E |
| Font (render) | DejaVuSansMono-Bold / DejaVuSans-Bold |
| Resolution | 1080 × 1920 (9:16) |
| Frame rate | 30 FPS |
| Duration | 55-60 seconds max |

## Common Animation Patterns

Quick reference (full details in `references/scene_cookbook.md`):

```python
fade_in     = min(1, progress * 3)                        # Fast fade
delayed     = max(0, (progress - 0.5) * 2)                # Appears at 50%
slide_up    = (1 - opacity) * 20                           # Y offset
pulse       = 0.5 + math.sin(progress * 20) * 0.5         # Oscillation
cliff_drop  = max(0, min(1, (progress - 0.35) * 2.5))     # Delayed sharp drop
```

### Phase 4: Narration (TTS)

Read `references/tts_setup.md` for installation of TTS backends.

The skill auto-detects the best available TTS engine:

| Priority | Backend | Quality | Requirement |
|----------|---------|---------|-------------|
| 1 | **Dia** (local) | High — natural, expressive | CUDA GPU ~4.4GB VRAM |
| 2 | **Higgs Audio** (API) | Highest — beats GPT-4o-mini-tts | API key + network |
| 3 | **Flite** (offline) | Low — timing reference only | Always available |

**Generate narration and mux into MP4:**
```python
from core.tts import generate_narration, mux_audio_video

# Each scene dict needs 'id', 'start', 'end', 'text' keys
narration_wav = generate_narration(scenes, output_dir="/output",
                                    voice_seed=42)  # seed = consistent voice
mux_audio_video("silent_video.mp4", narration_wav, "final_with_audio.mp4")
```

The pipeline generates speech per scene, time-stretches each to fit its scene duration, aligns them to exact timestamps via FFmpeg `adelay`, and muxes the result into the MP4 as AAC audio.

**Dia speaker tags:** For single-narrator Shorts, all text is wrapped in `[S1]`. Non-verbal tags like `(laughs)`, `(sighs)`, `(clears throat)` are supported but should be used sparingly.

**Voice consistency:** Dia generates a random voice per run. Use a fixed `voice_seed` to keep the same voice across all 6 scenes. Change the seed for a different voice.

## Known Limitations

| Limitation | Workaround |
|-----------|-----------|
| Dia needs CUDA GPU (~4.4GB VRAM) | Use Higgs Audio API, or Flite for timing reference |
| Flite voice is robotic | Use as timing guide, record own voiceover or use Dia/Higgs |
| speechSynthesis blocked in artifact iframe | Use Tone.js for preview audio; real TTS in render phase |
| Emoji rendering in Pillow | Use text symbols (↻, ⚡, ?) instead of emoji |
| No anti-aliasing on Pillow shapes | 1080p resolution compensates; use clean geometry |
| Browser video export unreliable | Always use Python+FFmpeg server-side render |
| WebM→MP4 conversion drops frames | Render directly to MP4, never convert |

## Post-Production (If Using Flite or No TTS)

If the narration was generated with Dia or Higgs Audio, the MP4 is ready for upload. If using Flite or no TTS:

1. Import MP4 into editor (Premiere / DaVinci / CapCut)
2. Record voiceover at ~160 WPM matching caption timing
3. Layer voiceover + optional music bed (-20dB under voice)
4. Export H.264 1080×1920 30fps matching source
5. Upload: YouTube Shorts (pin comment with full video link), Instagram Reels (same file)
