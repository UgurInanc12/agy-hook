# Models — Complete Reference

## Available Models (agy models)

| Model ID | Display Name | Best For |
|---|---|---|
| `gemini-3.7-flash-high` | Gemini 3.7 Flash (High) | Default, balanced, all tasks |
| `gemini-3.7-flash-medium` | Gemini 3.7 Flash (Medium) | Faster, slightly less reasoning |
| `gemini-3.7-flash-low` | Gemini 3.7 Flash (Low) | Fastest, cheapest |
| `gemini-3.5-flash-high` | Gemini 3.5 Flash (High) | Previous gen, stable |
| `gemini-3.5-flash-medium` | Gemini 3.5 Flash (Medium) | Faster |
| `gemini-3.5-flash-low` | Gemini 3.5 Flash (Low) | Fastest |
| `gemini-3.1-pro-high` | Gemini 3.1 Pro (High) | Best reasoning, complex tasks |
| `gemini-3.1-pro-low` | Gemini 3.1 Pro (Low) | Pro with less effort |
| `claude-sonnet-4-6` | Claude Sonnet 4.6 (Thinking) | Code, analysis |
| `claude-opus-4-6-thinking` | Claude Opus 4.6 (Thinking) | Deepest reasoning |
| `gpt-oss-120b-medium` | GPT-OSS 120B (Medium) | Open alternative |

## Usage

```
agy -p "prompt" --model "Gemini 3.7 Flash (High)" --dangerously-skip-permissions
agy -p "prompt" --model "Claude Sonnet 4.6 (Thinking)" --dangerously-skip-permissions
```

> **Important:** Use the exact display name including `(High)`/`(Low)`/`(Thinking)` suffix. Run `agy models` to verify.

## Effort Levels

Gemini Flash models have 3 effort levels (low/medium/high). Higher effort = more reasoning tokens, better results, slower and more expensive.

```
agy -p "prompt" --effort high --dangerously-skip-permissions
```

For most tasks, `high` is recommended. Use `low` only for trivial tasks.

## Default Model

- Default: `Gemini 3.7 Flash (High)` (gemini-3.7-flash-high)
- Image model: `gemini-3.1-flash-lite-image` (used internally by generate_image)
