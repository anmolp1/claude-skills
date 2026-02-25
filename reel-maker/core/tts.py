"""
Text-to-Speech module for reel-maker.

Priority chain:
  1. Dia (local GPU, ~4.4GB VRAM) — best open-source quality, Apache 2.0
  2. Higgs Audio API (Deep Infra) — best overall quality, needs API key
  3. Flite (always available offline) — timing reference only, robotic voice

Usage:
    from core.tts import generate_narration, mux_audio_video
    
    # Auto-detects best available backend
    audio_path = generate_narration(scenes, output_dir="/home/user/output")
    
    # Mux narration into silent MP4
    mux_audio_video("video.mp4", audio_path, "final.mp4")
"""

import subprocess
import os
import wave
import json
import shutil
import tempfile
import math

# ── Backend Detection ───────────────────────────────────

def detect_backend():
    """
    Detect the best available TTS backend.
    Returns: 'dia', 'dia-hf', 'higgs-api', or 'flite'
    """
    # 1. Check for Dia via HuggingFace Transformers (preferred)
    try:
        import torch
        if torch.cuda.is_available():
            from transformers import AutoProcessor, DiaForConditionalGeneration
            return "dia-hf"
    except ImportError:
        pass

    # 2. Check for Dia via native package
    try:
        import torch
        if torch.cuda.is_available():
            from dia.model import Dia
            return "dia"
    except ImportError:
        pass

    # 3. Check for Higgs Audio API (Deep Infra) — needs network + API key
    api_key = os.environ.get("DEEPINFRA_API_KEY") or os.environ.get("HIGGS_API_KEY")
    if api_key:
        try:
            import requests
            return "higgs-api"
        except ImportError:
            pass

    # 4. Flite fallback (always available on Ubuntu)
    try:
        import ctypes
        ctypes.CDLL('libflite.so.2.2')
        return "flite"
    except OSError:
        pass

    return None


# ── Dia Backend (HuggingFace Transformers) ──────────────

def _generate_dia_hf(text, output_path, voice_seed=42, temperature=1.3, top_p=0.95):
    """
    Generate speech using Dia via HuggingFace Transformers.
    
    Dia uses [S1] and [S2] speaker tags. For single-narrator Shorts,
    we use [S1] throughout. Add [S1] at the end for clean audio tail.
    
    Supported non-verbal tags (use sparingly):
        (laughs), (clears throat), (sighs), (gasps), (coughs),
        (singing), (mumbles), (groans), (sniffs), (inhales), (exhales)
    """
    import torch
    from transformers import AutoProcessor, DiaForConditionalGeneration

    device = "cuda"
    model_id = "nari-labs/Dia-1.6B-0626"

    processor = AutoProcessor.from_pretrained(model_id)
    model = DiaForConditionalGeneration.from_pretrained(model_id).to(device)

    # Format text with Dia's speaker tags
    # Single narrator = all [S1], with [S1] at end for clean tail
    dia_text = f"[S1] {text} [S1]"

    inputs = processor(text=[dia_text], padding=True, return_tensors="pt").to(device)

    # Set seed for consistent voice across scenes
    torch.manual_seed(voice_seed)

    outputs = model.generate(
        **inputs,
        max_new_tokens=3072,
        guidance_scale=3.0,
        temperature=temperature,
        top_p=top_p,
        top_k=45,
    )

    decoded = processor.batch_decode(outputs)
    processor.save_audio(decoded, output_path)

    # Clean up GPU memory
    del model
    torch.cuda.empty_cache()

    return output_path


# ── Dia Backend (Native Package) ────────────────────────

def _generate_dia_native(text, output_path, voice_seed=42):
    """
    Generate speech using Dia's native package.
    pip install git+https://github.com/nari-labs/dia.git
    """
    import torch
    from dia.model import Dia

    model = Dia.from_pretrained("nari-labs/Dia-1.6B-0626", compute_dtype="float16")

    dia_text = f"[S1] {text} [S1]"
    torch.manual_seed(voice_seed)

    output = model.generate(
        dia_text,
        max_tokens=3072,
        cfg_scale=3.0,
        temperature=1.3,
        top_p=0.95,
        use_torch_compile=True,
    )

    import soundfile as sf
    sf.write(output_path, output, 44100)

    del model
    torch.cuda.empty_cache()

    return output_path


# ── Higgs Audio API Backend ─────────────────────────────

def _generate_higgs_api(text, output_path):
    """
    Generate speech via Deep Infra's hosted Higgs Audio V2.5 API.
    Requires DEEPINFRA_API_KEY environment variable.
    
    Pricing: ~$20/1M characters ($0.003 per typical scene).
    """
    import requests

    api_key = os.environ.get("DEEPINFRA_API_KEY") or os.environ.get("HIGGS_API_KEY")
    if not api_key:
        raise ValueError("Set DEEPINFRA_API_KEY or HIGGS_API_KEY environment variable")

    url = "https://api.deepinfra.com/v1/inference/bosonai/HiggsAudioV2.5"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "text": text,
        "output_format": "pcm",
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    # Save raw PCM → convert to WAV via FFmpeg
    pcm_path = output_path + ".pcm"
    with open(pcm_path, 'wb') as f:
        f.write(response.content)

    # Convert PCM to WAV (assume 24kHz mono 16-bit, Higgs Audio default)
    cmd = [
        'ffmpeg', '-y',
        '-f', 's16le', '-ar', '24000', '-ac', '1',
        '-i', pcm_path,
        '-c:a', 'pcm_s16le',
        output_path
    ]
    subprocess.run(cmd, capture_output=True, check=True)
    os.remove(pcm_path)

    return output_path


# ── Flite Fallback Backend ──────────────────────────────

def _generate_flite(text, output_path, voice='rms'):
    """
    Generate speech using Flite via ctypes. Always available offline.
    Voice quality is robotic — use as timing reference only.
    
    Available voices: 'rms' (male, deep), 'slt' (female), 
                      'kal16' (male, neutral), 'awb' (male, Scottish)
    """
    import ctypes

    flite = ctypes.CDLL('libflite.so.2.2')
    ctypes.CDLL('libflite_usenglish.so.2.2')
    ctypes.CDLL('libflite_cmulex.so.2.2')
    flite.flite_init()
    flite.flite_text_to_speech.argtypes = [
        ctypes.c_char_p, ctypes.c_void_p, ctypes.c_char_p
    ]
    flite.flite_text_to_speech.restype = ctypes.c_float

    voice_map = {
        'rms': ('libflite_cmu_us_rms.so.2.2', 'register_cmu_us_rms'),
        'slt': ('libflite_cmu_us_slt.so.2.2', 'register_cmu_us_slt'),
        'kal16': ('libflite_cmu_us_kal16.so.2.2', 'register_cmu_us_kal16'),
        'awb': ('libflite_cmu_us_awb.so.2.2', 'register_cmu_us_awb'),
    }

    lib_name, fn_name = voice_map.get(voice, voice_map['rms'])
    voice_lib = ctypes.CDLL(lib_name)
    register_fn = getattr(voice_lib, fn_name)
    register_fn.restype = ctypes.c_void_p
    voice_ptr = register_fn(None)

    # Strip Dia tags if present
    clean_text = text.replace("[S1]", "").replace("[S2]", "").strip()

    raw_wav = output_path + ".raw.wav"
    flite.flite_text_to_speech(clean_text.encode(), voice_ptr, raw_wav.encode())

    # Post-process: upsample + EQ for less robotic sound
    filters = (
        "aresample=44100,"
        "highpass=f=80:poles=2,"
        "lowpass=f=8000:poles=2,"
        "equalizer=f=300:width_type=o:width=1.5:g=4,"
        "equalizer=f=3000:width_type=o:width=1:g=-3,"
        "equalizer=f=6000:width_type=o:width=1:g=-6,"
        "acompressor=threshold=-20dB:ratio=3:attack=5:release=50,"
        "loudnorm=I=-16:TP=-1.5:LRA=11"
    )

    cmd = ['ffmpeg', '-y', '-i', raw_wav, '-filter:a', filters, '-ac', '1', output_path]
    subprocess.run(cmd, capture_output=True)
    os.remove(raw_wav)

    return output_path


# ── Scene-Level Generation ──────────────────────────────

def _generate_scene(backend, text, output_path, voice_seed=42):
    """Route to the appropriate backend."""
    if backend == "dia-hf":
        return _generate_dia_hf(text, output_path, voice_seed=voice_seed)
    elif backend == "dia":
        return _generate_dia_native(text, output_path, voice_seed=voice_seed)
    elif backend == "higgs-api":
        return _generate_higgs_api(text, output_path)
    elif backend == "flite":
        return _generate_flite(text, output_path)
    else:
        raise ValueError(f"Unknown backend: {backend}")


def _time_stretch(input_wav, output_wav, target_duration):
    """
    Stretch/compress a WAV to fit target_duration using FFmpeg atempo.
    atempo accepts 0.5-2.0, so we chain filters for extreme ratios.
    """
    with wave.open(input_wav, 'rb') as w:
        actual = w.getnframes() / w.getframerate()

    if actual <= 0 or target_duration <= 0:
        shutil.copy2(input_wav, output_wav)
        return

    ratio = actual / target_duration

    # Build atempo chain (each filter: 0.5 - 2.0)
    filters = []
    r = ratio
    while r > 2.0:
        filters.append("atempo=2.0")
        r /= 2.0
    while r < 0.5:
        filters.append("atempo=0.5")
        r *= 2.0
    filters.append(f"atempo={r:.4f}")

    fchain = ",".join(filters) + ",aresample=44100,loudnorm=I=-16:TP=-1.5:LRA=11"

    cmd = ['ffmpeg', '-y', '-i', input_wav, '-filter:a', fchain, '-ac', '1', output_wav]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        shutil.copy2(input_wav, output_wav)


# ── Main Narration Pipeline ─────────────────────────────

def generate_narration(scenes, output_dir, duration=57, voice_seed=42,
                       backend=None, verbose=True):
    """
    Generate a complete narration track aligned to scene timestamps.
    
    Args:
        scenes: list of dicts with 'id', 'start', 'end', 'text' keys
        output_dir: directory for output files
        duration: total video duration in seconds
        voice_seed: seed for consistent voice across scenes (Dia only)
        backend: force a specific backend, or None for auto-detect
        verbose: print progress
    
    Returns:
        Path to the final narration WAV file, aligned to video timing.
    """
    if backend is None:
        backend = detect_backend()
        if backend is None:
            raise RuntimeError(
                "No TTS backend available. Install one of:\n"
                "  - Dia (recommended): pip install git+https://github.com/nari-labs/dia.git\n"
                "  - HuggingFace Transformers: pip install transformers torch\n"
                "  - Set DEEPINFRA_API_KEY for Higgs Audio API\n"
                "  - Install libflite for offline fallback"
            )

    if verbose:
        quality = {"dia-hf": "high", "dia": "high", "higgs-api": "high", "flite": "low (timing ref)"}
        print(f"TTS backend: {backend} (quality: {quality.get(backend, '?')})")

    tmpdir = tempfile.mkdtemp(prefix="reel_tts_")

    try:
        scene_wavs = []

        for scene in scenes:
            scene_dur = scene["end"] - scene["start"]
            # Leave 0.3s padding at start, 0.3s at end
            target_speech_dur = scene_dur - 0.6
            if target_speech_dur < 1.0:
                target_speech_dur = scene_dur - 0.2

            if verbose:
                print(f"\n  Scene {scene['id']} ({scene['start']}s-{scene['end']}s, "
                      f"speech target: {target_speech_dur:.1f}s)")

            # Generate raw TTS
            raw_wav = os.path.join(tmpdir, f"raw_{scene['id']}.wav")
            _generate_scene(backend, scene["text"], raw_wav, voice_seed=voice_seed)

            # Time-stretch to fit scene
            stretched_wav = os.path.join(tmpdir, f"stretched_{scene['id']}.wav")
            _time_stretch(raw_wav, stretched_wav, target_speech_dur)

            if verbose:
                with wave.open(stretched_wav, 'rb') as w:
                    final = w.getnframes() / w.getframerate()
                print(f"    Stretched: {final:.1f}s")

            scene_wavs.append((scene, stretched_wav))

        # Align each scene to its exact timestamp using adelay + amix
        inputs = []
        filter_parts = []

        for i, (scene, wav) in enumerate(scene_wavs):
            inputs.extend(['-i', wav])
            delay_ms = int((scene["start"] + 0.3) * 1000)
            filter_parts.append(
                f"[{i}]adelay={delay_ms}|{delay_ms},"
                f"apad=whole_dur={duration}[s{i}]"
            )

        mix_in = "".join(f"[s{i}]" for i in range(len(scene_wavs)))
        n = len(scene_wavs)
        filter_parts.append(
            f"{mix_in}amix=inputs={n}:duration=first:dropout_transition=0,"
            f"volume={n}[out]"
        )

        narration_path = os.path.join(output_dir, "narration.wav")
        cmd = [
            'ffmpeg', '-y', *inputs,
            '-filter_complex', ";".join(filter_parts),
            '-map', '[out]',
            '-c:a', 'pcm_s16le', '-ar', '44100', '-ac', '1',
            '-t', str(duration),
            narration_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg mix failed: {result.stderr[:500]}")

        if verbose:
            with wave.open(narration_path, 'rb') as w:
                total = w.getnframes() / w.getframerate()
            print(f"\n  ✅ Narration: {narration_path} ({total:.1f}s)")

        return narration_path

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


# ── Audio/Video Muxing ──────────────────────────────────

def mux_audio_video(video_path, audio_path, output_path, verbose=True):
    """
    Mux narration audio into a silent MP4 video.
    Video is copied (not re-encoded). Audio is encoded as AAC 192kbps.
    """
    cmd = [
        'ffmpeg', '-y',
        '-i', video_path,
        '-i', audio_path,
        '-c:v', 'copy',
        '-c:a', 'aac', '-b:a', '192k',
        '-ar', '44100',
        '-shortest',
        '-movflags', '+faststart',
        output_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Mux failed: {result.stderr[:500]}")

    if verbose:
        size_mb = os.path.getsize(output_path) / 1024 / 1024
        print(f"  ✅ Final video: {output_path} ({size_mb:.1f} MB)")

        # Show stream info
        r = subprocess.run(
            ['ffprobe', '-v', 'quiet', '-print_format', 'json',
             '-show_streams', output_path],
            capture_output=True, text=True
        )
        if r.returncode == 0:
            for s in json.loads(r.stdout).get('streams', []):
                codec = s.get('codec_name', '?')
                if s.get('codec_type') == 'video':
                    print(f"    Video: {codec}, {s['width']}x{s['height']}, "
                          f"{s['r_frame_rate']}fps")
                elif s.get('codec_type') == 'audio':
                    print(f"    Audio: {codec}, {s.get('sample_rate')}Hz, "
                          f"dur={float(s.get('duration', 0)):.1f}s")

    return output_path
