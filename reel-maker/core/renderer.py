"""
FFmpeg pipe renderer for reel-maker.
Renders all frames and pipes to FFmpeg for H.264 MP4 output.
"""

import subprocess
import sys
import os
from .drawing import W, H
from .scene_base import make_render_frame


def render_to_mp4(scenes, captions, scene_renderers, output_path,
                  fps=30, duration=57, verbose=True):
    """
    Render a complete video to MP4.

    Args:
        scenes: list of scene dicts with 'id', 'start', 'end', 'label', 'color'
        captions: list of (start_time, end_time, text) tuples
        scene_renderers: dict mapping scene_id → draw_scene_N(draw, img, progress)
        output_path: path for output .mp4 file
        fps: frames per second (default 30)
        duration: total duration in seconds (default 57)
        verbose: print progress to stdout
    """
    total_frames = duration * fps
    render_frame = make_render_frame(scenes, captions, scene_renderers, duration)

    if verbose:
        print(f"Rendering {total_frames} frames at {W}x{H} @{fps}fps...")
        print(f"Output: {output_path}")

    cmd = [
        'ffmpeg', '-y',
        '-f', 'rawvideo',
        '-vcodec', 'rawvideo',
        '-pix_fmt', 'rgb24',
        '-s', f'{W}x{H}',
        '-r', str(fps),
        '-i', '-',
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '18',
        '-pix_fmt', 'yuv420p',
        '-movflags', '+faststart',
        '-an',
        output_path
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

    for frame_num in range(total_frames):
        t = frame_num / fps
        img = render_frame(t)
        proc.stdin.write(img.tobytes())

        if verbose and frame_num % fps == 0:
            pct = frame_num / total_frames * 100
            print(f"  {pct:5.1f}% — {int(t)}s / {duration}s", flush=True)

    proc.stdin.close()
    stderr = proc.stderr.read().decode()
    proc.wait()

    if proc.returncode == 0:
        size_mb = os.path.getsize(output_path) / 1024 / 1024
        if verbose:
            print(f"\n✅ Done! {output_path} ({size_mb:.1f} MB)")
        return True
    else:
        if verbose:
            print(f"\n❌ FFmpeg error:\n{stderr}", file=sys.stderr)
        return False


def validate_output(output_path, expected_duration=57, expected_fps=30):
    """
    Validate MP4 output using FFprobe. Returns (valid, info_dict).
    """
    import json

    cmd = [
        'ffprobe', '-v', 'quiet',
        '-print_format', 'json',
        '-show_streams',
        output_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return False, {"error": "FFprobe failed"}

    data = json.loads(result.stdout)
    stream = data['streams'][0]

    info = {
        "codec": stream.get("codec_name"),
        "profile": stream.get("profile"),
        "width": stream.get("width"),
        "height": stream.get("height"),
        "fps": stream.get("r_frame_rate"),
        "pix_fmt": stream.get("pix_fmt"),
        "frames": stream.get("nb_frames"),
        "duration": float(stream.get("duration", 0)),
    }

    expected_frames = str(expected_duration * expected_fps)
    valid = (
        info["codec"] == "h264" and
        info["width"] == 1080 and
        info["height"] == 1920 and
        info["fps"] == f"{expected_fps}/1" and
        info["pix_fmt"] == "yuv420p" and
        info["frames"] == expected_frames
    )

    return valid, info
