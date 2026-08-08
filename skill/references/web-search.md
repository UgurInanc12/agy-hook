# Web Search — Grounded Search Guide

## Tool

`search_web` builtin (read-only) + native YouTube/video understanding.

## Basic Search

```
agy -p 'Search the web for <QUERY> and summarize the key findings with sources. Cite your sources.' --dangerously-skip-permissions --print-timeout 2m
```

## Structured Output

For bullet points:
```
agy -p 'Search the web for the latest Roblox Studio updates in 2026. Return exactly 3 bullet points, each with a title and one-sentence summary.' --dangerously-skip-permissions --print-timeout 2m
```

For JSON:
```
agy -p 'Search the web for top 5 AI image generation tools in 2026. Return a JSON array with objects {name, url, price}.' --output-format json --json-schema '{\"type\":\"array\",\"items\":{\"type\":\"object\",\"properties\":{\"name\":{\"type\":\"string\"},\"url\":{\"type\":\"string\"},\"price\":{\"type\":\"string\"}}}}' --dangerously-skip-permissions --print-timeout 2m
```

## Prompt Tips

- Be specific: `Roblox Studio MCP server setup 2026` > `Roblox updates`
- Ask for citations: `Cite your sources` ensures grounded results
- Specify format: `as 3 bullet points`, `as a markdown table`, `as JSON`
- Time-bounding: `in the last 3 months`, `published in 2026`

## Web Search Priority (User Preference)

| Priority | Tool | When to use |
|---|---|---|
| **1st** | agy (Gemini) | Always try first. Best quality, grounded, native. |
| **2nd** | mimo-websearch | If agy fails, times out, or is unavailable. |
| **3rd** | Hermes `web_search` / `web_extract` | Final fallback. Fastest, simplest. |

**For YouTube video questions:** Always use agy — native YouTube understanding, no download needed.

**Simple rule:** `agy` first, `mimo` second, built-in third. Never skip `agy` for web search.

## Reading URL Content

```
agy -p 'Read the content at https://example.com/article and summarize the 5 key points.' --dangerously-skip-permissions --print-timeout 2m
```

Uses `read_url_content` builtin tool internally.
