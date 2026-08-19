---
name: antigravity
description: "Use Google Gemini via Antigravity CLI (agy) as a sub-agent for image generation, video generation, web search (priority 1, prefer over mimo-websearch and built-in web_search), YouTube video understanding, code generation, and full app scaffolding. Activate when the user needs Gemini capabilities or wants to delegate work to a Gemini-powered sub-agent."
version: 1.1.0
author: Ugur Inanc
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [gemini, antigravity, agy, image-generation, video-generation, web-search, youtube, code-generation, sub-agent, google]
    related_skills: [comfyui, comfyui-video, roblox-mcp, watch-and-answer, mimo-websearch]
    category: creative
---

# Antigravity — Gemini Sub-Agent via `agy` CLI

Delegate any task to **Google Gemini** through the Antigravity CLI (`agy`) — image generation, video generation, grounded web search, native YouTube understanding, code generation, and full application scaffolding. All on Google's free quota.

## Prerequisites

- `agy` binary installed and on PATH. Verify: `terminal(command="agy --version")` — expect `1.1.11` or newer.
- Authenticated as a Google account. Verify: `terminal(command="agy models")` — should list `gemini-3.7-flash-high` etc. If it asks to sign in, the user must run `agy` interactively once (`pty=true`) and complete browser auth.
- Paths: `agy` stores data under `~/.gemini/antigravity-cli/` and `~/.gemini/config/`.

## Core Execution Pattern

Every Gemini task goes through the same `terminal` call. **Always use these flags:**

```bash
agy -p "<PROMPT>" --dangerously-skip-permissions --print-timeout <TIMEOUT>
```

| Flag | Why |
|---|---|
| `-p` / `--print` | Non-interactive one-shot. Returns plain text stdout. |
| `--dangerously-skip-permissions` | **Required.** Without it, headless mode auto-denies `write_file`/`command` tools and produces no output. |
| `--print-timeout` | Upper bound. Default `5m`. Raise for video/long tasks. |
| `--model` | Select model: `gemini-3.7-flash-high`, `gemini-3.1-pro-high`, `claude-sonnet-4-6`, etc. Run `agy models` for the full list. |
| `--add-dir` | Expose a local directory to the agent (repeatable). Used for reference images. |
| `--output-format` | `text` (default), `json`, or `stream-json`. Use `json` when you need structured output with `--json-schema`. |

**Output handling:**
- Text answers (search, YouTube, code explanation) come back as stdout.
- Generated files (images, videos, code files) are saved to disk — **always verify** with `read_file` or `terminal(ls ...)`.
- Binary on this machine: `C:\Users\uguri\bin\agy.exe` — also available as `agy` via PATH.

## Capability 1: Image Generation

Gemini generates images via its `generate_image` tool (model: `gemini-3.1-flash-lite-image`).

### Basic Image

```
terminal(command="agy -p 'Generate an image: <DETAILED_PROMPT>. Save it to C:/Users/uguri/Desktop/output.png' --dangerously-skip-permissions --print-timeout 3m")
```

### Prompt Engineering

Be extremely specific. Include:
- **Subject** — what is in the image
- **Style** — photorealistic, PBR texture, anime, oil painting, isometric, etc.
- **Composition** — framing, camera angle, lighting
- **Technical specs** — resolution, aspect ratio, seamless/tileable if needed

Example for Roblox texture:
```
Generate a 1024x1024 seamless tileable PBR texture of a sci-fi metal wall panel.
Brushed steel with rivets, ventilation grilles, cyan LED strip accents.
Top-down orthographic view, no perspective distortion, perfectly tileable edges.
Save to C:/Users/uguri/Desktop/sci_fi_wall.png
```

Example for app asset:
```
Generate a 512x512 app icon for a weather app. Minimalist flat design,
blue gradient background, white cloud with sun peeking behind it.
Centered, no text, transparent-friendly. Save to C:/Users/uguri/Desktop/weather_icon.png
```

### Reference Images

There is no dedicated `--reference-image` flag. To use a reference:

1. Place the reference image in a directory, e.g. `C:/Users/uguri/Desktop/refs/`
2. Pass `--add-dir C:/Users/uguri/Desktop/refs` so the agent can read it
3. Mention the file path in the prompt:

```
terminal(command="agy -p 'Look at the reference image at C:/Users/uguri/Desktop/refs/inspiration.png. Generate a new image in the same art style but with a futuristic city skyline. Save to C:/Users/uguri/Desktop/output.png' --dangerously-skip-permissions --add-dir C:/Users/uguri/Desktop/refs --print-timeout 3m")
```

### Verification

After generation:
```
terminal(command="ls -lh C:/Users/uguri/Desktop/output.png && file C:/Users/uguri/Desktop/output.png")
vision_analyze(image_url="C:/Users/uguri/Desktop/output.png", question="Describe this image. Does it match the prompt requirements?")
```

> **Pitfall:** Output is often JPEG data with `.png` extension. Check with `file` command. Not a real problem — the image is valid regardless of extension.

> **See also:** `references/image-generation.md` for advanced prompt patterns and `templates/image-prompts.md` for copy-paste templates.

## Capability 2: Video Generation

Gemini can generate short video clips.

```
terminal(command="agy -p 'Generate a 5-second video clip: <DESCRIPTION>. Save to C:/Users/uguri/Desktop/output.mp4' --dangerously-skip-permissions --print-timeout 5m")
```

Video generation is slower (~30-60s for 5s at 1080p 60FPS) and produces H.264/MP4. Keep prompts focused on a single scene/action.

Verify: `terminal(command="ls -lh C:/Users/uguri/Desktop/output.mp4 && ffprobe -v quiet -print_format json -show_format -show_streams C:/Users/uguri/Desktop/output.mp4 2>&1 | head -30")`

> **See also:** `references/video-generation.md`

## Capability 3: Grounded Web Search

Gemini has a native `search_web` tool for real-time grounded search.

```
terminal(command="agy -p 'Search the web for <QUERY> and summarize the key findings with sources. Cite your sources.' --dangerously-skip-permissions --print-timeout 2m")
```

For structured output:
```
terminal(command="agy -p 'Search the web for the latest Roblox Studio updates in 2026. Return exactly 3 bullet points, each with a title and one-sentence summary.' --dangerously-skip-permissions --print-timeout 2m")
```

Results come back as markdown text with citations. Parse `stdout` directly.

> **Web search priority (user preference):**
> 1. **agy (Gemini)** — first choice, always try this first
> 2. **mimo-websearch** — second choice, if agy fails or times out
> 3. **Hermes built-in `web_search` / `web_extract`** — third/fallback choice
>
> For YouTube video questions, always use agy (native YouTube understanding).

> **See also:** `references/web-search.md`

## Capability 4: YouTube / Video Understanding

Gemini natively understands YouTube URLs — it fetches and analyzes the video content directly. No download or transcoding needed.

```
terminal(command="agy -p 'Watch this YouTube video https://www.youtube.com/watch?v=VIDEO_ID and <QUESTION>. Be specific about what you see and hear.' --dangerously-skip-permissions --print-timeout 3m")
```

Examples:
- Summarize: `... and summarize what happens in the video.`
- Analyze: `... and describe the editing techniques and visual style used.`
- Extract: `... and list every product shown with timestamps.`
- Transcribe: `... and transcribe the key dialogue.`

For local video files, use `--add-dir`:
```
terminal(command="agy -p 'Analyze the video at C:/Users/uguri/Desktop/clip.mp4 and describe what happens.' --dangerously-skip-permissions --add-dir C:/Users/uguri/Desktop --print-timeout 3m")
```

> **Advantage over Hermes watch-and-answer:** Gemini watches YouTube natively (no yt-dlp download, no transcoding, no frame sampling). Use this for any YouTube question — it is faster and more accurate for YouTube content.

> **See also:** `references/youtube-analysis.md`

## Capability 5: Code Generation & App Scaffolding

Gemini can write code, create files, edit files, run commands, and scaffold entire applications.

### Single File

```
terminal(command="agy -p 'Write a Lua function for Roblox that makes a part rotate smoothly around Y axis at 45 degrees per second. Save it to C:/Users/uguri/Desktop/rotate.lua' --dangerously-skip-permissions --print-timeout 2m")
terminal(command="cat C:/Users/uguri/Desktop/rotate.lua")
```

### Full App Scaffolding

```
terminal(command="agy -p 'Create a complete single-file HTML app at C:/Users/uguri/Desktop/app.html: <DETAILED_APP_SPEC>. Include CSS and JS inline. Make it polished and production-ready.' --dangerously-skip-permissions --print-timeout 5m")
```

**For full apps, always include in the prompt:**
- What the app does (features, user flow)
- Tech stack (HTML/CSS/JS, React, etc.)
- Design requirements (colors, layout, responsive)
- Where to save the output file (absolute Windows path)

### Project in a Directory

```
terminal(command="agy -p 'Create a new project at C:/Users/uguri/Desktop/my-project/: <SPEC>. Initialize the directory structure, write all files, and verify they exist.' --dangerously-skip-permissions --add-dir C:/Users/uguri/Desktop --print-timeout 5m")
terminal(command="ls -R C:/Users/uguri/Desktop/my-project/ 2>&1 | head -40")
```

### Verification

After any code generation:
```
terminal(command="ls -la C:/path/to/output 2>&1")
read_file(path="C:/path/to/output")
# For HTML apps: open_preview or browser_navigate to verify visually
```

> **Pitfall:** On Windows, always use forward slashes or escaped backslashes in paths within prompts: `C:/Users/uguri/Desktop/file.lua` or `C:\\Users\\uguri\\Desktop\\file.lua`.

> **See also:** `references/code-generation.md` and `templates/app-scaffold.md`

## Capability 6: General Sub-Agent & Reasoning

For anything else — complex multi-step tasks, research, analysis:

```
terminal(command="agy -p '<TASK_DESCRIPTION>. Think step by step, use tools as needed, and produce a complete result.' --dangerously-skip-permissions --print-timeout 5m")
```

Gemini can also spawn its own sub-agents (`start_subagent` tool) for parallel work. For maximum reasoning:

```
terminal(command="agy -p '<COMPLEX_TASK>' --model 'Gemini 3.1 Pro (High)' --dangerously-skip-permissions --print-timeout 10m")
```

For Claude models via the same CLI:
```
terminal(command="agy -p '<TASK>' --model 'Claude Sonnet 4.6 (Thinking)' --dangerously-skip-permissions --print-timeout 5m")
```

## Model Selection

| Task | Recommended Model | Why |
|---|---|---|
| Image generation | `Gemini 3.7 Flash (High)` | Fast, good quality (default) |
| Video generation | `Gemini 3.7 Flash (High)` | Default, handles video |
| Web search | `Gemini 3.7 Flash (High)` | Fast grounded search |
| YouTube analysis | `Gemini 3.7 Flash (High)` | Native video understanding |
| Simple code | `Gemini 3.7 Flash (High)` | Fast code gen |
| Complex reasoning / app scaffold | `Gemini 3.1 Pro (High)` | Best reasoning |
| Code review / architecture | `Claude Sonnet 4.6 (Thinking)` | Excellent at code |
| Quick one-liners | `Gemini 3.7 Flash (Low)` | Fastest, cheapest |

Run `agy models` to see the current list. Model display names need exact match including `(High)` suffix.

## Timeout Guide

| Task | Recommended `--print-timeout` |
|---|---|
| Web search | `2m` |
| YouTube analysis | `3m` |
| Image generation | `3m` |
| Code (single file) | `2m` |
| Code (full app) | `5m` |
| Video generation | `5m` |
| Complex research | `5m - 10m` |

Always pair with `terminal(timeout=...)` — set the terminal timeout slightly higher than `--print-timeout` (e.g., `--print-timeout 5m` with `timeout=360`).

## Path Conventions (Windows)

- In prompts to Gemini: use `C:/Users/uguri/Desktop/file.png` (forward slashes)
- In terminal commands: use `/c/Users/uguri/Desktop/file.png` (MSYS) or `C:/Users/uguri/Desktop/file.png`
- For `--add-dir`: use the Windows-native path `C:/Users/uguri/Desktop/refs`
- Output files: prefer `C:/Users/uguri/Desktop/` or a project subdirectory for easy verification

## Verification Checklist

After every `agy` call:

1. Check stdout for success/error: the response text tells you what happened
2. For file outputs: `terminal(command="ls -lh <OUTPUT_PATH> && file <OUTPUT_PATH>")`
3. For images: `vision_analyze(image_url="<OUTPUT_PATH>", question="...")`
4. For code: `read_file(path="<OUTPUT_PATH>")`
5. For HTML apps: `browser_navigate(url="file:///C:/path/to/app.html")` or `open_preview`

## Common Pitfalls

1. **Missing `--dangerously-skip-permissions`** — headless `agy -p` auto-denies all tools without this flag. You get `jetski: no output produced` and no files. Always include it.
2. **Wrong model name** — display names are exact: `Gemini 3.7 Flash (High)` not `gemini-3.7-flash-high`. Use `agy models` to verify.
3. **Timeout too short** — image/video generation needs 3-5 minutes. If you get a timeout, raise `--print-timeout`.
4. **Path with spaces** — wrap Windows paths in the prompt with quotes or use forward slashes.
5. **Image extension mismatch** — output may be JPEG data with `.png` extension. Check with `file` command; the image is still valid.
6. **Auth expiry** — if `agy models` fails with auth error, the user must re-authenticate: run `agy` interactively with `pty=true` and complete browser sign-in.
7. **Each `agy -p` is a fresh session** — no conversation memory between calls. For multi-turn work, use `agy --continue` or describe the full task in one prompt.

## Scripts

| Script | Purpose |
|---|---|
| `scripts/verify_agy.py` | Check `agy` is installed and authenticated |
| `scripts/agy_run.py` | Python wrapper for `agy -p` with structured output |
| `scripts/generate_image.py` | Dedicated image generation helper |
| `scripts/generate_video.py` | Dedicated video generation helper |

## References

| File | Content |
|---|---|
| `references/image-generation.md` | Advanced image prompt engineering, PBR textures, icon design, reference image workflow |
| `references/video-generation.md` | Video prompts, duration, resolution, style control |
| `references/web-search.md` | Grounded search patterns, citation handling, structured output |
| `references/youtube-analysis.md` | YouTube URL handling, local video analysis, transcript extraction |
| `references/code-generation.md` | Single-file, multi-file, and full-app scaffolding patterns |
| `references/models.md` | Complete model catalog, selection guide, effort levels |
| `references/app-scaffold.md` | Template for scaffolding complete applications |

## Templates

| File | Content |
|---|---|
| `templates/image-prompts.md` | Copy-paste image prompt templates (texture, icon, wallpaper, character) |
| `templates/app-scaffold.md` | Copy-paste app scaffolding prompts (landing page, dashboard, game) |
| `templates/video-prompts.md` | Copy-paste video generation prompts |
