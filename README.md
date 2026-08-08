# agy-hook

Use Google Gemini from Hermes Agent through the official Antigravity CLI.

agy-hook is a Hermes skill, not an API reimplementation. It teaches Hermes when
and how to call `agy` for tasks that benefit from Gemini, including image
creation, short video generation, grounded web research, YouTube analysis, code
writing, and application scaffolding.

## Important warning

> [!CAUTION]
> **Using this project may get your Google account restricted or banned.**
>
> This skill runs automated, non-interactive Antigravity CLI requests. Google
> may consider repeated headless automation, unusual request frequency, or
> unattended use inconsistent with its service rules. Possible consequences
> include throttling, reduced access, temporary restrictions, loss of your
> Antigravity or Gemini access, or suspension of the Google account connected to
> the CLI. A suspension could affect other services under the same account.
>
> **The risk is yours. Use a separate Google account if you decide to test this.**
> Do not use an important personal, work, school, Workspace, or production
> account. Keep request frequency low, do not run a public multi-user service,
> and stop using the project if Google shows a warning or restriction.
>
> This repository is unofficial and is not affiliated with, sponsored by, or
> endorsed by Google, Gemini, Antigravity, or Hermes Agent. The author cannot
> recover an account, quota, subscription, or data lost after using this project.

## Why this exists

Google Gemini features available through an Antigravity account are not the
same as a Google AI Studio API key. A user may have a Google Gemini or Google
AI Pro subscription, while the public Gemini API uses a separate API key and
billing system.

This project does not claim to convert that subscription into a public API.
Instead, it uses the official `agy` CLI that the user has already authenticated
through Google OAuth. Hermes starts an `agy` request only when a suitable task
requires Gemini.

In practical terms, a user with an authenticated Antigravity account can ask
Hermes to use capabilities available to that account, including Gemini features
provided by the Antigravity service. Availability, model access, limits, and
subscription treatment are controlled by Google and can change without notice.

## Capabilities

| Capability | Typical request |
| --- | --- |
| Image generation | Create a game icon, texture, wallpaper, or concept image |
| Video generation | Create a short single-scene video clip |
| Web research | Search current information and return cited findings |
| YouTube understanding | Watch a YouTube URL and answer questions about it |
| Code generation | Write scripts, modules, and project files |
| App scaffolding | Build a complete single-file web app or project skeleton |

For web research, this skill follows the configured priority:

1. `agy` with Gemini
2. `mimo-websearch` if `agy` fails or times out
3. Hermes built-in `web_search` or `web_extract` as the final fallback

For YouTube questions, `agy` is preferred because Gemini can process the URL
without first downloading and transcoding the video locally.

## Requirements

- Hermes Agent
- Antigravity CLI `agy` version 1.1.11 or newer
- A Google account authenticated in Antigravity
- Windows, macOS, or Linux

Check the installation before using the skill:

```bash
agy --version
agy models
python skill/scripts/verify_agy.py
```

`agy models` should return the models available to the signed-in account.
Authentication is managed by Antigravity. This project does not collect or
store Google credentials.

## Installation

Clone the repository and copy the skill directory into the Hermes skills root.
The exact Hermes home can differ by platform and installation method.

```bash
git clone https://github.com/UgurInanc12/agy-hook.git
cd agy-hook

# Replace this destination with your Hermes skills directory when necessary.
cp -r skill "$HERMES_HOME/skills/creative/antigravity"
```

On the author's Windows installation, the destination is:

```text
C:\Users\<user>\AppData\Local\hermes\skills\creative\antigravity
```

The skill contains no Hermes plugin process and does not require a gateway
restart. Hermes discovers it from the skills directory when the skill is
loaded.

## Usage examples

Ask Hermes naturally:

```text
Generate a 1024x1024 seamless sci-fi metal texture for Roblox.

Search the web for the latest ComfyUI video workflows and cite the sources.

Watch this YouTube video and explain the main ideas: https://youtube.com/watch?v=...

Create a complete single-file HTML pomodoro application with a dark theme.
```

The underlying command follows this pattern:

```bash
agy -p "<complete task description>" \
  --dangerously-skip-permissions \
  --print-timeout 3m
```

The skill requires an explicit output path for generated files and verifies the
result afterward. Images and videos are checked on disk, code is read back, and
web results are returned as text with citations when Gemini provides them.

## Prompt guidance

### Images

Describe the subject, visual style, composition, lighting, dimensions, and
technical constraints. For a tileable game texture, explicitly request a
square resolution, orthographic view, seamless edges, and no baked shadows.

```text
Generate a 1024x1024 seamless tileable PBR texture of brushed sci-fi steel,
with rivets, vents, and restrained cyan lights. Use a top-down orthographic
view with no perspective distortion or baked shadows. Save it to
C:/Users/<user>/Desktop/sci-fi-wall.png.
```

### Videos

Keep the scene focused. Describe one continuous action, the camera movement,
lighting, visual style, duration, and destination path.

```text
Generate a 5-second cinematic video of a luminous blue star emblem rotating
slowly in a dark space scene with drifting particles. Use smooth motion and a
slow camera push-in. Save it to C:/Users/<user>/Desktop/star-scene.mp4.
```

### Applications

Give Gemini the complete specification in one request:

- purpose and target user
- features and user flows
- technology and file layout
- visual design and responsive behavior
- persistence and data handling
- loading, empty, and error states
- exact absolute output path

For larger projects, tell Gemini to create the directory structure, write every
file, run the relevant checks, and report the files it actually created.

## Repository layout

```text
agy-hook/
├── README.md
├── LICENSE
├── .gitignore
├── plan.md
└── skill/
    ├── SKILL.md
    ├── references/
    │   ├── app-scaffold.md
    │   ├── code-generation.md
    │   ├── image-generation.md
    │   ├── models.md
    │   ├── video-generation.md
    │   ├── web-search.md
    │   └── youtube-analysis.md
    ├── scripts/
    │   ├── agy_run.py
    │   └── verify_agy.py
    └── templates/
        ├── app-scaffold.md
        ├── image-prompts.md
        └── video-prompts.md
```

## Security and operational notes

- Never commit Google credentials, tokens, cookies, or Antigravity data.
- Keep the skill local if you do not want to expose your workflow publicly.
- Do not expose an `agy` wrapper to the internet without authentication and
  strict rate limiting.
- Do not run arbitrary prompts from untrusted users with
  `--dangerously-skip-permissions`.
- Keep generated files in a dedicated output directory and inspect them before
  opening or executing them.
- The CLI can write files and run commands when permissions are bypassed. Treat
  every generated command and file as untrusted until reviewed.

## Related projects

These projects use different approaches and are listed only for technical
comparison. They are not dependencies of agy-hook:

- [Hermes Agent](https://github.com/NousResearch/hermes-agent)
- [Antigravity Bridge](https://github.com/ythx-101/antigravity-bridge)
- [Antigravity OpenAI API](https://github.com/lojik-ng/agy-openai-api)
- [agy OpenAI Proxy](https://github.com/benteckxyz/agy-openai-proxy)

## License and disclaimer

This project is released under the MIT License. The license does not grant
permission to violate any third-party terms or policies.

Use the project at your own risk. Google controls Antigravity authentication,
model availability, quotas, account enforcement, and subscription access. The
author provides no guarantee that the CLI will continue to work or that an
account will remain in good standing.

This project is independent of Google, Gemini, Antigravity, and Hermes Agent.

<p align="center">Unofficial tooling. Review the warning before installing.</p>
