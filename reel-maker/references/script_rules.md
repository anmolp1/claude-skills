# Script Rules — Short-Form Vertical Video

## The 6-Scene Structure

Every Short follows this compressed Investigation formula. Total duration: 55-60 seconds.

### Scene 1: Cold Open (0:00-0:05)
- **Technique:** Hook
- **Rule:** Start mid-thought. No "hey guys", no intro, no context. First sentence must create a gap the viewer needs closed.
- **Pattern:** "[Surprising claim] — and [why you should care]."
- **Color:** Use Alert Red for danger/urgency topics, Electric Blue for technical topics.

### Scene 2: Promise Lock (0:05-0:12)
- **Technique:** Credibility Spike
- **Rule:** Name the concept explicitly. Follow with a credibility proof: "I see this in every system I audit" / "This broke 3 production systems last month."
- **Pattern:** "This is [named concept] — [credibility proof]."

### Scene 3: The Problem (0:12-0:25)
- **Technique:** Evidence + Open Loop
- **Rule:** Build the mechanic step by step. Each sentence adds one layer. End with the consequence, not the solution.
- **Pattern:** "Here's what happens. [Step 1]. [Step 2]. [Step 3]. Eventually, [consequence]."

### Scene 4: The Evidence (0:25-0:38)
- **Technique:** Stakes Escalation
- **Rule:** This is the dramatic peak. Use a chart, cliff, or before/after. The visual must be the most striking in the video.
- **Pattern:** "And the [metric] isn't gradual. It's a cliff. [Specific data]. Then [catastrophic outcome]."

### Scene 5: The Fix (0:38-0:48)
- **Technique:** Resolution
- **Rule:** Actionable, specific, time-boxed. Must include implementation time estimate. Viewer should feel "I can do this Monday."
- **Pattern:** "The fix: [specific action]. [How it works]. [Time to implement]."

### Scene 6: Cliffhanger (0:48-0:57)
- **Technique:** Open Loop
- **Rule:** Never say "like and subscribe." Reframe the current topic, then tease the next video as an unresolved threat.
- **Pattern:** "[Current topic] is the [X] you can [verb]. The next one you can't — [tease]."

## Narration Rules

- **Word count:** 155-170 words total
- **Pacing:** 160-170 WPM (slower than conversational, signals expertise)
- **Sentence length:** 5-12 words. Short punchy fragments.
- **Forbidden words:** "so", "basically", "essentially", "let me explain", "in this video"
- **Voice:** Authoritative but not arrogant. Practitioner, not professor.
- **Pauses:** 0.5s pause before the most important line in each scene.

## Caption Chunks

Break the narration into 3-5 word segments with precise timestamps.

### Rules
- Each chunk is a perceptual unit — it should feel like a complete thought fragment
- Key terms get their own chunk: "It's a cliff." stands alone
- Timing: 1.0-1.5 seconds per chunk
- Total chunks: 40-50 for a 57-second video
- No chunk should exceed 5 words

### Format
```python
CAPTIONS = [
    (start_time, end_time, "3-5 word text"),
    (0.0, 1.0, "Your AI agent"),
    (1.0, 2.0, "is getting dumber"),
    ...
]
```

### Alignment
Caption timing should match natural speech rhythm:
- Emphatic words get slightly longer duration (1.2-1.5s)
- Transitional phrases are faster (0.8-1.0s)
- Dramatic pauses: insert a 0.3-0.5s gap between chunks

## Scene Color Assignments

Each scene has a primary color that drives its visual palette:

| Content Type | Color |
|-------------|-------|
| Failures, danger, cost, urgency | Alert Red (#FF3B30) |
| Solutions, success, fixes | Data Green (#00FF88) |
| Technical concepts, neutral info | Electric Blue (#007AFF) |
| Warnings, thresholds, transitions | Warning Yellow (#FFD60A) |

Assign colors based on the emotional register of each scene, not rigidly by scene number. The Cold Open and Cliffhanger are almost always Red. The Fix is almost always Green.

## Cross-Linking

Every Short must tease one specific other video in the Cliffhanger. This creates a binge funnel:

```
Short → Full-length version (deep dive)
Cliffhanger → Next Short in sequence
```

Name the cross-link target explicitly in the script metadata.
