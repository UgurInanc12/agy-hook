<div align="center">

# 🪝 agy-hook

**Hermes Agent + Google Gemini bridge via Antigravity CLI**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Hermes Agent](https://img.shields.io/badge/Hermes-Agent-purple.svg)](https://hermes.nousresearch.com)

*Image generation, video generation, web search, YouTube analysis, code generation — all through your Google Gemini subscription*

</div>

---

> [!CAUTION]
> ## ⚠️ Risk Warning — Read Before Use
>
> This project uses the **Antigravity CLI (`agy`)** to access Google Gemini capabilities
> through your Google account's OAuth session. While this uses the **official CLI**
> (not CDP injection or API hacking), it still carries risks:
>
> - **Terms of Service** — Using automated CLI calls (`agy -p`) in headless mode
>   may violate [Google's Terms of Service](https://policies.google.com/terms)
>   or [Antigravity's Terms](https://antigravity.google/terms). The `--dangerously-skip-permissions`
>   flag bypasses interactive safety prompts for a reason.
> - **Account throttling** — Excessive automated usage may trigger rate limiting,
>   degraded responses, or temporary restrictions on your Google account.
> - **Account suspension** — In extreme cases, your Google account could be suspended,
>   potentially affecting other Google services (Gmail, GCP, Workspace).
> - **Detection** — Headless CLI calls have non-human patterns (no typing delay,
>   no cursor movement, consistent command structure). Google can detect this.
> - **Breakage** — This relies on Antigravity CLI internals. Updates to `agy`,
>   changes to Google's backend, or auth flow changes can break this at any time.
>
> **Protect yourself:**
> 1. 🚫 **Do not use your primary Google account** — Use a dedicated account
> 2. 🐢 **Rate limit yourself** — Don't hammer the API; space out requests
> 3. 🧪 **Personal/educational use only** — Not for production or commercial use
> 4. 💀 **Expect breakage** — The CLI or backend can change at any time
> 5. 📋 **Read Google's ToS** — Understand what you're agreeing to
>
> *Use at your own risk. The authors are not responsible for any account actions
> taken by Google or Anthropic. This is an unofficial, community-driven project.*

---

## What is this?

**agy-hook** is a [Hermes Agent](https://hermes.nousresearch.com) skill that teaches
Hermes how to use [Google Gemini](https://gemini.google.com) as a sub-agent through
the official [Antigravity CLI](https://antigravity.google) (`agy`).

It does **not** modify, reverse-engineer, or intercept the Antigravity CLI. It simply
invokes `agy -p` (the official non-interactive mode) with well-crafted prompts — the
same way a human would type them in a terminal.

### What you get

| Capability | Example |
|---|---|
| **Image generation** | "Generate a 512x512 Roblox coin icon" |
| **Video generation** | "Generate a 5-second space video" |
| **Web search** | "Search the web for latest AI news" (priority 1) |
| **YouTube analysis** | "What happens in this YouTube video?" |
| **Code generation** | "Write a Lua module for Roblox" |
| **App scaffolding** | "Create a complete HTML pomodoro app" |

### Web search priority

When Hermes needs to search the web, it follows this priority:

1. **`agy` (Gemini)** — first choice, best quality, grounded results
2. **`mimo-websearch`** — second choice, if agy fails
3. **Hermes built-in `web_search`** — third/fallback

---

## Prerequisites

- [Hermes Agent](https://hermes.nousresearch.com) installed
- [Antigravity CLI](https://antigravity.google/docs/cli) (`agy`) v1.1.11+ installed
  and authenticated (`agy models` should list models)
- Windows, macOS, or Linux

## Installation

### Automatic (recommended)

The skill is installed to:
```
~/.local/share/hermes/skills/creative/antigravity/
```

Or copy manually:
```bash
# Clone the repo
git clone https://github.com/UgurInanc12/agy-hook.git
cd agy-hook

# Copy skill to Hermes
cp -r skill/* ~/.local/share/hermes/skills/creative/antigravity/
```

### Verify

```bash
# Check agy is installed
agy --version  # Should show 1.1.11+

# Check authentication
agy models  # Should list gemini-3.6-flash-high etc.

# Run the verification script
python scripts/verify_agy.py
```

---

## Usage

Once installed, Hermes automatically loads the skill. Just ask naturally:

```
"Generate a sci-fi metal wall texture for Roblox, 1024x1024 tileable"
→ Hermes loads antigravity skill → agy -p 'Generate...' → verifies output → shows result

"What happens in this YouTube video? https://youtube.com/watch?v=..."
→ Hermes loads antigravity skill → agy -p 'Watch...' → returns summary

"Create a complete todo app as a single HTML file"
→ Hermes loads antigravity skill → agy -p 'Create...' → writes file → verifies
```

### Manual invocation via terminal

```bash
# Image generation
agy -p "Generate a 512x512 golden coin icon. Save to C:/Users/you/Desktop/coin.png" \
    --dangerously-skip-permissions --print-timeout 3m

# Web search
agy -p "Search the web for latest Roblox updates 2026, return 3 bullet points" \
    --dangerously-skip-permissions --print-timeout 2m

# YouTube analysis
agy -p "Watch https://youtube.com/watch?v=VIDEO_ID and summarize" \
    --dangerously-skip-permissions --print-timeout 3m

# Code generation
agy -p "Write a Lua rotation script. Save to C:/Users/you/Desktop/rotate.lua" \
    --dangerously-skip-permissions --print-timeout 2m
```

---

## Project Structure

```
agy-hook/
├── README.md              # This file
├── LICENSE                # MIT License
├── .gitignore
├── plan.md                # Full technical plan
├── skill/                 # Hermes skill (installable)
│   ├── SKILL.md           # Main skill definition
│   ├── references/        # Detailed guides per capability
│   │   ├── image-generation.md
│   │   ├── video-generation.md
│   │   ├── web-search.md
│   │   ├── youtube-analysis.md
│   │   ├── code-generation.md
│   │   ├── models.md
│   │   └── app-scaffold.md
│   ├── templates/         # Copy-paste prompt templates
│   │   ├── image-prompts.md
│   │   ├── app-scaffold.md
│   │   └── video-prompts.md
│   └── scripts/           # Helper scripts
│       ├── verify_agy.py  # Health check
│       └── agy_run.py     # Python wrapper
└── docs/                  # Additional documentation
```

---

## How it works

```
User asks Hermes → "Generate a texture"
  → Hermes loads antigravity skill
  → Skill tells Hermes to call agy -p with --dangerously-skip-permissions
  → agy authenticates via OS keyring (OAuth, your Google account)
  → Gemini generates the image/text/code
  → Output saved to disk or returned as stdout
  → Hermes verifies the output (file exists, correct format, etc.)
```

**Key points:**
- Uses the **official** `agy` CLI — no hacking, no reverse engineering
- Authenticates via **OS keyring** (same as running `agy` interactively)
- `--dangerously-skip-permissions` is required for headless operation
- Each call is a **fresh session** — no conversation memory between calls
- Uses your **Google Gemini Pro subscription** quota (not API key quota)

---

## Models

| Model | Best for |
|---|---|
| `Gemini 3.6 Flash (High)` | Default, balanced, all tasks |
| `Gemini 3.1 Pro (High)` | Complex reasoning, app scaffolding |
| `Claude Sonnet 4.6 (Thinking)` | Code review, architecture |
| `Claude Opus 4.6 (Thinking)` | Deepest reasoning |

Run `agy models` for the full list.

---

## Known Limitations

- **Each call starts a full agent session** — ~3-6s startup overhead per call
- **No streaming** from `-p` mode — full response at once
- **No conversation memory** between separate `-p` calls
- **Video generation** is slow (~30-60s for 5s clip)
- **Image/video gen not available via OpenAI API** — only through `agy -p`
- **Auth expiry** — keyring token refreshes automatically, but may need re-auth periodically

---

## Related Projects

| Project | Approach | Notes |
|---|---|---|
| [lojik-ng/agy-openai-api](https://github.com/lojik-ng/agy-openai-api) | FastAPI + Docker proxy | OpenAI-compatible, most complete |
| [benteckxyz/agy-openai-proxy](https://github.com/benteckxyz/agy-openai-proxy) | FastAPI + SSE streaming | macOS only, streaming support |
| [marcodiniz/ag-local-bridge](https://github.com/marcodiniz/ag-local-bridge) | VS Code extension | Most elegant, ConnectRPC |
| [ythx-101/antigravity-bridge](https://github.com/ythx-101/antigravity-bridge) | CDP injection | macOS only, fragile |
| [12errh/antigravity-proxy](https://github.com/12errh/antigravity-proxy) | TLS MITM gateway | Production-grade, other direction |

---

## Contributing

Contributions welcome! Please read the warning at the top first.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `agy` and Hermes
5. Submit a pull request

---

## License

[MIT](LICENSE) — Use at your own risk.

---

## Disclaimer

This project is **not affiliated with, endorsed by, or sponsored by Google,
Anthropic, or Antigravity**. It is an independent, community-driven project.

The Antigravity CLI (`agy`) is a product of Google/Antigravity. This project
simply provides instructions for using it within the Hermes Agent framework.

**The authors make no guarantees about the safety, reliability, or legality
of using this project. Use at your own risk.**
