# Export Specifications

## Output Format (Locked)

These settings produce universally compatible vertical video for YouTube Shorts, Instagram Reels, and TikTok.

| Spec | Value | Rationale |
|------|-------|-----------|
| Resolution | 1080 × 1920 | 9:16, max quality for all platforms |
| Frame rate | 30 FPS | Standard for short-form; 60fps adds no value for motion graphics |
| Codec | H.264 High Profile | Universal — plays everywhere, all editors accept it |
| CRF | 18 | Visually lossless for motion graphics content |
| Pixel format | yuv420p | Required for compatibility (players reject yuv444p) |
| movflags | +faststart | Moves moov atom to start for instant web playback |
| Audio | None (-an) | Voiceover recorded separately in post-production |
| Container | MP4 | Universal container format |
| Duration | ≤60 seconds | YouTube Shorts limit; aim for 55-57s |

## FFmpeg Command

```bash
ffmpeg -y \
  -f rawvideo \
  -vcodec rawvideo \
  -pix_fmt rgb24 \
  -s 1080x1920 \
  -r 30 \
  -i - \
  -c:v libx264 \
  -preset medium \
  -crf 18 \
  -pix_fmt yuv420p \
  -movflags +faststart \
  -an \
  output.mp4
```

### Parameter Notes

- **`-f rawvideo -pix_fmt rgb24`**: Pillow outputs raw RGB bytes via `img.tobytes()`. This tells FFmpeg to interpret the stdin pipe as raw frames.
- **`-s 1080x1920`**: Must match exactly — FFmpeg has no way to infer dimensions from raw bytes.
- **`-r 30`**: Input AND output frame rate. Since we pipe raw frames, this sets both.
- **`-preset medium`**: Balance of speed and compression. Use `slow` for marginally smaller files if time allows. Never use `ultrafast` — it bloats files 3-5x.
- **`-crf 18`**: Quality factor. 0 = lossless, 23 = default, 51 = worst. 18 is conservative for our content. Motion graphics compress extremely well; expect 1-5 MB for 57 seconds.
- **`-movflags +faststart`**: Critical for web playback — without this, the entire file must download before playback starts.
- **`-an`**: No audio stream. The MP4 is a visual-only track.

## Python Rendering Pipeline

```python
import subprocess
from PIL import Image, ImageDraw

W, H, FPS, DURATION = 1080, 1920, 30, 57
TOTAL_FRAMES = DURATION * FPS

cmd = [
    'ffmpeg', '-y',
    '-f', 'rawvideo', '-vcodec', 'rawvideo', '-pix_fmt', 'rgb24',
    '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
    '-pix_fmt', 'yuv420p', '-movflags', '+faststart', '-an',
    OUTPUT_PATH
]

proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

for frame_num in range(TOTAL_FRAMES):
    t = frame_num / FPS
    img = render_frame(t)           # Returns PIL Image (RGB, 1080x1920)
    proc.stdin.write(img.tobytes()) # Raw RGB bytes to FFmpeg stdin

proc.stdin.close()
stderr = proc.stderr.read().decode()
proc.wait()

if proc.returncode != 0:
    print(f"FFmpeg error: {stderr}")
```

## Validation

Always verify the output:

```bash
ffprobe -v quiet -print_format json -show_streams output.mp4
```

Expected values:
```json
{
  "codec_name": "h264",
  "profile": "High",
  "width": 1080,
  "height": 1920,
  "r_frame_rate": "30/1",
  "pix_fmt": "yuv420p",
  "nb_frames": "1710",
  "duration": "57.000000"
}
```

Frame count = DURATION × FPS. For 57s @ 30fps = 1710 frames exactly.

## File Size Expectations

Motion graphics (flat colors, clean edges, text) compress dramatically better than live footage:

| Content | Expected Size (57s) |
|---------|-------------------|
| Motion graphics (our content) | 1-5 MB |
| Mixed (graphics + photos) | 5-15 MB |
| Live footage | 20-60 MB |

If the file exceeds 10 MB for pure motion graphics, something is wrong. Check:
- Are frames being written as RGB? (not RGBA — extra channel wastes bytes)
- Is CRF set correctly? (18, not 0)
- Is preset at least `medium`? (`ultrafast` bloats output)

## Why Not WebM?

Browser-based `MediaRecorder` produces WebM (VP8/VP9). We avoid it because:
1. WebM uses constant bitrate by default → 52 MB for content that's 1.6 MB as H.264 CRF
2. `captureStream` + `setTimeout` can produce empty blobs or corrupt timing
3. WebM → MP4 conversion via FFmpeg introduces frame timing drift
4. Instagram and TikTok prefer H.264 MP4; WebM requires transcoding on upload

Always render directly to MP4 via the Python pipeline.

## Platform-Specific Upload Notes

### YouTube Shorts
- Title: first 40 characters must hook (rest truncated on mobile)
- Pin a comment linking to the full-length video
- Add `#Shorts` in description (no longer required but aids discovery)
- Thumbnail: YouTube auto-selects a frame; you cannot upload a custom Shorts thumbnail

### Instagram Reels
- Same MP4 file, no re-encoding needed
- Caption text is separate from the video (add in Instagram's editor)
- "Link in bio" for the full video

### TikTok
- Same MP4 file
- Add trending sounds in TikTok's editor if relevant (layered on top of your voiceover)
