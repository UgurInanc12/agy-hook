# Code Generation & App Scaffolding — Guide

## Tools Available via agy

- `create_file` — create new file
- `edit_file` — edit existing file
- `view_file` — read file contents
- `run_command` — execute shell commands
- `list_directory` / `search_directory` / `find_file` — file discovery
- `start_subagent` — spawn sub-agents

## Single File Generation

```
agy -p 'Write a <LANGUAGE> <DESCRIPTION> and save it to C:/Users/uguri/Desktop/<FILE>.' --dangerously-skip-permissions --print-timeout 2m
```

Examples:
```
Write a Lua function for Roblox that makes a part rotate smoothly around Y axis at 45 degrees per second. Save to C:/Users/uguri/Desktop/rotate.lua
```

```
Write a Python script that fetches the top 10 trending GitHub repos and saves them as JSON. Save to C:/Users/uguri/Desktop/trending.py
```

## Full Single-File HTML App

```
agy -p 'Create a complete single-file HTML app at C:/Users/uguri/Desktop/app.html:
<DETAILED_SPEC>. Include CSS and JS inline. Make it polished and production-ready.'
--dangerously-skip-permissions --print-timeout 5m
```

### What to Include in <DETAILED_SPEC>

- **Purpose:** What the app does, who it is for
- **Features:** Every feature, user flow, interaction
- **Tech:** HTML/CSS/JS inline (or React via CDN, etc.)
- **Design:** Colors, layout, responsive, dark mode, animations
- **Data:** Mock data or API integration
- **Polish:** Loading states, error handling, empty states

### Example: Full Spec

```
Create a complete single-file HTML app at C:/Users/uguri/Desktop/todo.html:
A beautiful todo app with: add/edit/delete tasks, categories (work/personal),
priority levels (high/medium/low) with color coding, due dates, search and filter,
localStorage persistence, dark/light theme toggle, drag to reorder, progress bar.
Design: modern glassmorphism, rounded corners, smooth animations, responsive.
Include CSS and JS inline. Polished and production-ready.
```

## Multi-File Project

```
agy -p 'Create a new project at C:/Users/uguri/Desktop/my-project/:
<SPEC>. Create the full directory structure, write all files,
and verify they exist. Use <STACK> (e.g., React + Vite, Node + Express).'
--dangerously-skip-permissions --add-dir C:/Users/uguri/Desktop --print-timeout 5m
```

## Model Selection for Code

| Task | Model |
|---|---|
| Simple scripts, single files | `Gemini 3.7 Flash (High)` |
| Full apps, complex scaffolding | `Gemini 3.1 Pro (High)` |
| Code review, architecture | `Claude Sonnet 4.6 (Thinking)` |

```
agy -p '<CODE_TASK>' --model 'Gemini 3.1 Pro (High)' --dangerously-skip-permissions --print-timeout 5m
```

## Verification

```
terminal(command="ls -R C:/Users/uguri/Desktop/my-project/ 2>&1")
read_file(path="C:/Users/uguri/Desktop/app.html")
# For HTML: open in browser
browser_navigate(url="file:///C:/Users/uguri/Desktop/app.html")
```

## Tips

- Always specify the **absolute output path** in the prompt
- One prompt = one complete task. Don't split app scaffolding across multiple calls
- Ask for `polished and production-ready` to get better quality
- For Roblox: mention `Luau`, `Roblox Studio`, existing conventions
- Verify every file after generation — Gemini sometimes says "done" without writing
