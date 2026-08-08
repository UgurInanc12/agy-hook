# Video Generation — Guide

## Model

No dedicated SDK tool, but `agy -p` can generate videos through the agent.

## Basic Usage

```
agy -p 'Generate a 5-second video clip: <DESCRIPTION>. Save to C:/Users/uguri/Desktop/output.mp4' --dangerously-skip-permissions --print-timeout 5m
```

## Prompt Anatomy

```
[SUBJECT + ACTION] + [STYLE] + [CAMERA] + [DURATION/TECHNICAL]
```

Example:
```
"Generate a 5-second video: a glowing blue Gemini star logo slowly rotating
and pulsing in deep space, surrounded by drifting stars and nebula clouds.
Cinematic, smooth 60fps, dark background with subtle lens flare.
Save to C:/Users/uguri/Desktop/gemini_space.mp4"
```

## Duration & Resolution

- Default: 5 seconds at 1080p 60FPS → H.264/MP4
- Currently ~2.7MB for 5s
- Keep prompts focused on a single continuous action

## Prompt Tips

- Describe ONE continuous action, not multiple cuts
- Include camera: `slow dolly in`, `static camera`, `orbiting camera`
- Include motion: `gentle floating`, `smooth rotation`, `particles drifting`
- Include style: `cinematic`, `photorealistic`, `anime style`, `low-poly`
- Avoid: complex multi-scene narratives, text overlays, rapid cuts

## Verification

```
ls -lh C:/Users/uguri/Desktop/output.mp4
ffprobe -v quiet -print_format json -show_format -show_streams C:/Users/uguri/Desktop/output.mp4
```

## Limitations

- Slow: ~30-60s generation for 5s clip
- No audio generation (video is silent)
- Single scene only, no editing/cuts
