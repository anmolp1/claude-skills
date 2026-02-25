# TTS Setup Guide

The reel-maker skill auto-detects the best available TTS backend. This guide covers installation and configuration for each option.

## Recommended: Dia (Local GPU)

**Quality:** High — natural prosody, emotional expression, non-verbal sounds
**Requirements:** CUDA GPU with ~4.4GB VRAM (RTX 3060 or better), Python 3.10+
**Cost:** Free (Apache 2.0 license, runs locally)
**Speed:** ~2x realtime on RTX 4090

Dia is a 1.6B parameter model from Nari Labs (19k+ GitHub stars). It generates ultra-realistic speech in one pass with support for non-verbal sounds like laughter and sighs.

### Installation (Option A: HuggingFace Transformers — recommended)

```bash
pip install torch transformers
pip install git+https://github.com/huggingface/transformers.git
```

The model (~3GB) downloads automatically from HuggingFace on first run.

### Installation (Option B: Native Dia package)

```bash
pip install git+https://github.com/nari-labs/dia.git
```

### How It Works

Dia uses speaker tags `[S1]` and `[S2]` for dialogue. For our single-narrator Shorts, the skill wraps all text in `[S1]`:

```
[S1] Your AI agent is getting dumber with every single message. 
And there's no error log telling you why. [S1]
```

The trailing `[S1]` ensures clean audio at the end (per Dia's guidelines).

### Voice Consistency

Dia generates a random voice each run. The skill uses a fixed `voice_seed` (default: 42) to keep the same voice across all 6 scenes. Change the seed to get a different voice:

```python
from core.tts import generate_narration
generate_narration(scenes, output_dir, voice_seed=123)  # Different voice
```

### Generation Guidelines (from Dia docs)

- Keep each scene's text moderate length (5-20 seconds of speech)
- Non-verbal tags are supported but use sparingly: `(laughs)`, `(clears throat)`, `(sighs)`, `(gasps)`, `(coughs)`
- Overusing non-verbal tags or using unlisted ones causes artifacts
- Short inputs (<5s of audio) may sound unnatural
- Very long inputs (>20s) may produce unnaturally fast speech

### Tips for Shorts Narration

- Write script text as natural speech, not written prose
- Use short sentences (5-12 words) — Dia handles these well
- Add a `(sighs)` or `(clears throat)` before dramatic reveals for effect
- The cliffhanger scene can end with a slight pause by adding "..." at the end


## Alternative: Higgs Audio V2.5 (API)

**Quality:** Highest — beats GPT-4o-mini-tts on expressiveness benchmarks
**Requirements:** Network access + API key
**Cost:** ~$20/1M characters (about $0.003 per scene, ~$0.02 per video)

### Setup

1. Get an API key from [Deep Infra](https://deepinfra.com/bosonai/HiggsAudioV2.5)
2. Set the environment variable:

```bash
export DEEPINFRA_API_KEY="your-key-here"
```

3. Install requests: `pip install requests`

The skill auto-detects the API key and uses Higgs Audio when Dia is unavailable.

### Other Hosted Options

| Provider | URL | Notes |
|----------|-----|-------|
| Deep Infra | deepinfra.com | $20/1M chars, REST API |
| Replicate | replicate.com/lucataco/higgs-audio-v2 | ~$0.004/run |
| Eigen AI | app.eigenai.com | Direct inference |
| Boson AI Demo | voice.boson.ai/demo | Free demo (not for automation) |


## Fallback: Flite (Offline)

**Quality:** Low — robotic, suitable only as a timing reference
**Requirements:** libflite (pre-installed on Ubuntu)
**Cost:** Free

Flite is a 2002-era diphone synthesizer. The skill applies post-processing (EQ, compression, noise reduction) to improve quality slightly, but the output is not publish-ready.

**Use case:** When working in environments without GPU or network (e.g., Claude.ai sandbox), Flite generates a timing reference track. You then:
1. Record your own voiceover using the timing reference
2. Or feed the script to an external TTS service

### Available Voices

| Voice | Description |
|-------|-------------|
| `rms` | Male, deep (default) |
| `slt` | Female |
| `kal16` | Male, neutral, 16kHz |
| `awb` | Male, Scottish accent |


## Backend Priority

The skill auto-detects backends in this order:

```
1. dia-hf    → Dia via HuggingFace Transformers (needs GPU + transformers)
2. dia       → Dia via native package (needs GPU + dia package)
3. higgs-api → Higgs Audio V2.5 via Deep Infra API (needs network + API key)
4. flite     → Flite via system libflite (always available on Ubuntu)
```

To force a specific backend:

```python
from core.tts import generate_narration
generate_narration(scenes, output_dir, backend="dia-hf")   # Force Dia
generate_narration(scenes, output_dir, backend="flite")     # Force Flite
```


## Post-Generation Pipeline

Regardless of backend, the narration pipeline:

1. Generates one WAV per scene
2. Time-stretches each to fit its scene duration (minus 0.6s padding)
3. Places each at its exact scene timestamp using FFmpeg `adelay`
4. Mixes all streams with `amix` to produce a single WAV
5. Muxes the WAV into the silent MP4 (video copied, audio as AAC 192kbps)

The output is a complete MP4 with synchronized narration ready for upload.
