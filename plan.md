# agy-hook — Hermes ↔ Gemini Bridge

> Turn Google Gemini (via Antigravity CLI) into a native Hermes sub-agent for
> image generation, web search, YouTube analysis, code generation, and more —
> all using Google's free quota.

---

## Problem Statement

Hermes Agent currently lacks native access to Google Gemini capabilities:
image/video generation, grounded web search, YouTube video understanding, and
the full Gemini model suite. These capabilities are available through
Antigravity CLI (`agy`) which authenticates via a free Google account.

**Goal:** Expose Gemini as a callable tool/provider inside Hermes so that any
agent session — whether the user is chatting directly or Hermes is running
autonomously — can invoke Gemini's strengths on demand.

---

## Architecture: Three Integration Layers

The project ships three independent layers, each increasing in power and
complexity. Users can adopt just Layer 1, or go all the way to Layer 3.

```
Layer 3 (Provider)  ───  Hermes native model provider (local OpenAI-compatible proxy)
Layer 2 (Plugin)    ───  Hermes plugin: concrete tools (gemini_generate_image, gemini_search, ...)
Layer 1 (Skill)     ───  Hermes skill: SKILL.md teaches Hermes how and when to call agy
```

### Layer 1: Skill (SKILL.md)

**What:** A skill definition that tells Hermes when and how to use `agy -p`
for Gemini tasks. No code — pure instructions.

**Why:** Zero setup, works immediately, teaches the agent to reach for `agy`
when it needs image gen, web search, or YouTube analysis.

**Location:** `C:\Users\uguri\AppData\Local\hermes\skills\creative\antigravity-cli\SKILL.md`

### Layer 2: Plugin (Hermes native tools)

**What:** A Hermes plugin that registers concrete Python tools —
`gemini_generate_image`, `gemini_web_search`, `gemini_youtube_summary`,
`gemini_generate_code`, `gemini_generate_video` — using `ctx.register_tool`.

**Why:** Direct tool calls with structured parameters, JSON output, error
handling. No prompt engineering needed — Hermes calls the tools by name.

**Location:** `C:\Users\uguri\AppData\Local\hermes\plugins\antigravity-cli\`

### Layer 3: Provider (Local OpenAI-compatible proxy)

**What:** Add Google Gemini as a direct Hermes provider using the built-in
Gemini provider or Google's own OpenAI-compatible `/openai` subpath. **No
local proxy server needed.**

**Why:** Hermes natively supports Gemini — it has a built-in `gemini` provider
that talks directly to `https://generativelanguage.googleapis.com/v1beta` with
native transport (thinking_config support). Additionally, Gemini models are
**already available** through the existing `commandcode` provider
(`google/gemini-3.6-flash`, `google/gemini-3.5-flash`, etc.).

**How:** Just uncomment `GOOGLE_API_KEY` in `C:\Users\uguri\AppData\Local\hermes\.env`
and optionally add this to `config.yaml`:
```yaml
providers:
  gemini-direct:
    name: "Gemini Direct"
    base_url: "https://generativelanguage.googleapis.com/v1beta/openai"
    model: gemini-2.5-flash
    discover_models: true
    key_env: GOOGLE_API_KEY
```

**Location:** No code needed, just config.

---

## Test Results (2026-08-08)

All tests performed via `agy v1.1.11` on Windows, authenticated as
`ugurinanc1@gmail.com`.

| Capability | Status | Notes |
|---|---|---|
| **Web Search** | WORKS | `agy -p "search..."` returns grounded, cited results. ~10s. |
| **YouTube Understanding** | WORKS | Native video URL parsing. Correctly identified Rick Astley video, summarized visuals/outfits. ~11s. |
| **Image Generation** | WORKS | Generated 1376x768 wallpaper (627KB) and 1024x1024 texture (1.5MB). Requires `--dangerously-skip-permissions` in headless mode. ~20s. |
| **Video Generation** | WORKS | Generated 1080p 60FPS 5-second video (2.7MB). Initial 48-byte file was permission-denied. Requires `--dangerously-skip-permissions`. ~30-60s. |
| **Code Generation** | WORKS | Generates and writes files to disk. Needs `write_file` permission or `--dangerously-skip-permissions`. |
| **File Operations** | WORKS | Can read/write/create files. Same permission requirement. |

### Available Models (via `agy models`)

```
gemini-3.6-flash-high     (default)
gemini-3.6-flash-medium
gemini-3.6-flash-low
gemini-3.5-flash-high/medium/low
gemini-3.1-pro-high/low
claude-sonnet-4-6         (Thinking)
claude-opus-4-6-thinking
gpt-oss-120b-medium
```

### Critical Discovery: Permission System

`agy` in headless (`-p`) mode auto-denies any tool that needs permission.
The fix: either configure `~/.gemini/antigravity-cli/settings.json` with
explicit allow rules, or always use `--dangerously-skip-permissions` for
non-interactive calls from Hermes.

---

## Layer 1: Skill Implementation

### Files

```
C:\Users\uguri\AppData\Local\hermes\skills\creative\antigravity-cli\
└── SKILL.md
```

### SKILL.md Content

The skill teaches Hermes:

1. **When to reach for `agy`:** image gen, web search, YouTube analysis, code gen
2. **How to call it:** `agy -p "prompt" --dangerously-skip-permissions --print-timeout 5m`
3. **How to handle output:** stdout text for search/code, file paths for images
4. **Model selection:** `--model "Gemini 3.6 Flash (High)"` for images,
   `--model "Gemini 3.1 Pro (High)"` for complex reasoning
5. **Reference images:** place files in a temp dir, use `--add-dir` to expose
   them to the agent

### Trigger Examples

- "Generate a texture for a sci-fi wall" → image generation
- "Search the web for latest Roblox updates" → web search
- "What happens in this YouTube video?" → YouTube analysis
- "Write a Lua script for Roblox rotation" → code generation

---

## Layer 2: Plugin Implementation

### File Structure

```
C:\Users\uguri\AppData\Local\hermes\plugins\antigravity-cli\
├── plugin.yaml
└── __init__.py
```

### plugin.yaml

```yaml
name: antigravity-cli
version: "1.0.0"
description: "Gemini capabilities via Antigravity CLI: image gen, web search, YouTube, code gen, video gen."
author: "Ugur Inanc"
kind: standalone
```

### Registered Tools

| Tool | Description | Key Parameters |
|---|---|---|
| `gemini_generate_image` | Generate an image with Gemini | `prompt`, `output_path`, `model?`, `width?`, `height?` |
| `gemini_web_search` | Web search via Gemini | `query`, `model?` |
| `gemini_youtube_summary` | Summarize a YouTube video | `url`, `question?`, `model?` |
| `gemini_generate_code` | Generate code and save to file | `prompt`, `output_path`, `model?` |
| `gemini_generate_video` | Generate a video clip | `prompt`, `output_path`, `duration?` |
| `gemini_generate_video` | Generate a video clip | `prompt`, `output_path`, `duration?`, `model?` |
| `gemini_ask` | General-purpose Gemini query | `prompt`, `model?`, `workdir?` |

### Implementation Pattern (per tool)

```python
def _run_agy(prompt: str, model: str | None, workdir: str | None,
             timeout: int, output_format: str = "text") -> dict:
    """Core agy runner shared by all tools."""
    cmd = [AGY_BIN, "-p", prompt, "--dangerously-skip-permissions",
           "--print-timeout", f"{timeout}s"]
    if model:
        cmd += ["--model", model]
    if output_format != "text":
        cmd += ["--output-format", output_format]
    result = subprocess.run(cmd, capture_output=True, text=True,
                            timeout=timeout + 30, cwd=workdir)
    return {"stdout": result.stdout, "stderr": result.stderr,
            "exit_code": result.returncode}
```

Each tool:
1. Builds a specific prompt from structured parameters
2. Calls `_run_agy` with appropriate timeout and model
3. Parses output (text, file path, JSON)
4. Returns structured result

### Tool Definitions (examples)

```python
def _gemini_generate_image(prompt, output_path, model=None):
    p = f"Generate an image: {prompt}. Save it to {output_path}."
    r = _run_agy(p, model=model, timeout=120)
    if os.path.exists(output_path):
        return {"success": True, "file": output_path,
                "size": os.path.getsize(output_path)}
    return {"success": False, "error": r["stdout"]}

def _gemini_web_search(query, model=None):
    p = f"Search the web and return your answer with sources: {query}"
    r = _run_agy(p, model=model, timeout=60)
    return {"answer": r["stdout"], "success": r["exit_code"] == 0}
```

### Registration

```python
def register(ctx):
    ctx.register_tool(
        name="gemini_generate_image",
        description="Generate an image using Google Gemini...",
        parameters={...},
        handler=_gemini_generate_image_handler,
    )
    # ... register other tools
```

---

## Layer 3: Provider Implementation (Config Only)

### Concept

Hermes already supports Gemini natively via two paths:
1. **Built-in Gemini provider** (native transport with thinking_config)
2. **Google's OpenAI-compatible `/openai` subpath** (standard OpenAI transport)

No local proxy server is needed.

### Config Addition

```yaml
providers:
  gemini-direct:
    name: "Gemini Direct"
    base_url: "https://generativelanguage.googleapis.com/v1beta/openai"
    model: gemini-2.5-flash
    discover_models: true
    key_env: GOOGLE_API_KEY
```

### Key Considerations

- **API Key:** Requires a Google AI Studio API key (free tier available at
  https://aistudio.google.com/apikey). This is separate from Antigravity auth.
- **Quota:** Free tier has generous limits (15 RPM for Flash, 2 RPM for Pro).
- **Features:** Text generation, multimodal (image understanding), structured
  output, function calling — all available through the SDK.
- **Image/video generation:** These are Gemini-specific features that don't
  map to OpenAI API. Layer 2 plugin handles these via `agy`.

---

## Implementation Phases

### Phase 1: Skill (1-2 hours)

- [x] Test all capabilities (done)
- [ ] Write SKILL.md with complete instructions
- [ ] Install to Hermes skills directory
- [ ] Verify Hermes picks it up
- [ ] Test: ask Hermes to generate an image using the skill

### Phase 2: Plugin (2-3 hours)

- [ ] Create plugin.yaml + __init__.py
- [ ] Implement `gemini_generate_image` tool
- [ ] Implement `gemini_web_search` tool
- [ ] Implement `gemini_youtube_summary` tool
- [ ] Implement `gemini_generate_code` tool
- [ ] Implement `gemini_ask` tool (general-purpose)
- [ ] Register all tools
- [ ] Copy to Hermes plugins directory
- [ ] Restart Hermes and verify tools appear
- [ ] Test each tool individually

### Phase 3: Provider (3-4 hours)

- [ ] Get Google AI Studio API key (https://aistudio.google.com/apikey)
- [ ] Uncomment GOOGLE_API_KEY in C:\Users\uguri\AppData\Local\hermes\.env
- [ ] Add gemini-direct provider to config.yaml (OpenAI-compat subpath)
- [ ] Test: hermes model → select gemini-direct, then chat
- [ ] Verify streaming, thinking, and tool use work through the provider

### Phase 4: Polish & Publish (1-2 hours)

- [ ] Write README.md with setup instructions
- [ ] Add GitHub Actions CI
- [ ] Create .gitignore
- [ ] Push to GitHub
- [ ] Create skill for Hermes skill hub

---

## Project Structure

```
D:\AI\agy-hook\
├── plan.md                          # This file
├── README.md                        # Public documentation
├── LICENSE                          # MIT
├── .gitignore
│
├── skill\                           # Layer 1: Hermes skill
│   └── SKILL.md
│
├── plugin\                          # Layer 2: Hermes plugin
│   ├── plugin.yaml
│   └── __init__.py
│
├── tests\                           # Test suite
│   ├── test_skill.md
│   ├── test_plugin.py
│   └── test_proxy.py
│
└── docs\                            # Additional documentation
    ├── capabilities.md              # Full Gemini capability matrix
    ├── troubleshooting.md           # Common issues and fixes
    └── examples\                    # Usage examples
        ├── roblox_texture.md
        ├── web_research.md
        └── youtube_analysis.md
```

---

## Key Technical Notes

### Permission Configuration

For headless `agy` usage, either:

**Option A:** Use `--dangerously-skip-permissions` (recommended for plugin)
```bash
agy -p "prompt" --dangerously-skip-permissions
```

**Option B:** Configure `~/.gemini/antigravity-cli/settings.json`
```json
{
  "permissions": {
    "allow": [
      "write_file(*)",
      "command(*)",
      "read_file(*)"
    ]
  }
}
```

### Model Selection Strategy

| Task | Recommended Model | Why |
|---|---|---|
| Image generation | `gemini-3.6-flash-high` | Fast, good quality |
| Complex reasoning | `gemini-3.1-pro-high` | Best reasoning |
| Web search | `gemini-3.6-flash-high` | Fast, grounded search |
| YouTube analysis | `gemini-3.6-flash-high` | Native video understanding |
| Code generation | `claude-sonnet-4-6` | Excellent at code (available via agy) |

### Timeout Recommendations

| Task | --print-timeout |
|---|---|
| Web search | 2m |
| Image generation | 3m |
| Video generation | 5m |
| Code generation | 2m |
| YouTube analysis | 3m |

### Reference Image Upload

To use reference images with Gemini image generation:

1. Place images in a temp directory
2. Use `--add-dir C:/path/to/images` with `agy -p`
3. Reference the file in the prompt: "Generate an image similar to
   reference_image.png but with the following changes..."
4. The Gemini agent can read the file via `view_file` tool and use it as context

Note: No dedicated `--reference-image` flag exists. Workaround is file path
in prompt + agent's file reading capability.

---

## Gemini Built-in Tools (via SDK)

The `google-antigravity` Python SDK exposes these built-in tools:

| Tool | Type | Description |
|---|---|---|
| `generate_image` | write | Generate or edit images (gemini-3.1-flash-lite-image) |
| `search_web` | read-only | Grounded web search |
| `read_url_content` | read-only | Fetch and read URL content |
| `create_file` | write | Create new file |
| `edit_file` | write | Edit existing file |
| `run_command` | write | Execute shell commands |
| `start_subagent` | special | Spawn sub-agents with own tools |
| `list_directory` | read-only | List directory contents |
| `search_directory` | read-only | Grep/search within directories |
| `find_file` | read-only | Find files by name |
| `ask_question` | interactive | Ask user clarifying question |

**Default model:** gemini-3.6-flash
**Default image model:** gemini-3.1-flash-lite-image

This is what `agy -p` uses under the hood. When we build the plugin, we're
essentially exposing these same capabilities as Hermes tools.

---

## Known Limitations

1. **Video generation** works but is slow (30-60s for 5s clip at 1080p 60FPS)
2. **Protobuf version conflict** for Python SDK (needs protobuf>=7.35.0)
3. **Each agy call starts a full agent session** — high token overhead per call
4. **No streaming** from agy CLI print mode — full response at once
5. **Rate limits** depend on Google account quota (free tier)
6. **Auth expiry** — keyring token refreshes, but may need re-auth periodically

---

## Future Enhancements

- [ ] MCP server wrapper (expose Gemini tools via MCP protocol)
- [ ] Streaming proxy for real-time responses
- [ ] Image-to-image editing with reference
- [ ] Batch processing (multiple images in one session)
- [ ] Conversation context (multi-turn via `agy -c`)
- [ ] Model fallback chains
- [ ] Integration with Roblox MCP for texture pipeline
- [ ] Integration with ComfyUI for AI art workflows
