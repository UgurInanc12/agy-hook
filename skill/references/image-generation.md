# Image Generation — Advanced Guide

## Model

`generate_image` builtin tool → `gemini-3.1-flash-lite-image` under the hood.

## Resolution & Aspect Ratios

Gemini picks resolution from the prompt. Be explicit:

| Use Case | Prompt Fragment |
|---|---|
| Wallpaper 16:9 | `1920x1080, 16:9 widescreen, landscape` |
| Square icon | `512x512, square, centered icon` |
| Portrait | `1080x1920, 9:16 portrait, vertical` |
| Texture tile | `1024x1024, square, seamless tileable, no perspective` |
| Banner | `1600x400, wide banner, horizontal` |

## Prompt Anatomy

A great image prompt has 5 parts:

```
[SUBJECT] + [STYLE] + [COMPOSITION] + [LIGHTING/COLOR] + [TECHNICAL SPECS]
```

Example:
```
"A medieval blacksmith shop interior (subject), photorealistic PBR game asset
(style), top-down orthographic view centered on the anvil (composition),
warm firelight with cool blue moonlight from window (lighting),
1024x1024 seamless tileable, no perspective distortion (technical)"
```

## Roblox / Game Textures

For PBR tileable textures — critical for Roblox:

```
Generate a 1024x1024 seamless tileable PBR texture of <MATERIAL>.
<MATERIAL_DETAILS>. Top-down orthographic, no perspective, perfectly tileable
edges — left edge matches right edge, top matches bottom. No shadows baked in.
Save to C:/Users/uguri/Desktop/texture_<name>.png
```

Materials to try:
- `weathered concrete with cracks and moss`
- `sci-fi metal wall panel with rivets and cyan LED strips`
- `dark oak wood planks with visible grain`
- `lava rock with glowing cracks`
- `marble floor with gold veins`

## Icons & UI Assets

```
Generate a 512x512 app icon: <DESCRIPTION>.
Minimalist flat design, centered, no text, transparent background.
Save to C:/Users/uguri/Desktop/icon_<name>.png
```

```
Generate a UI button texture 256x64, <STYLE> style, text "<LABEL>" centered,
rounded corners, subtle gradient. Save to C:/Users/uguri/Desktop/btn_<name>.png
```

## Reference Image Workflow

No `--reference-image` flag exists. Use file-based workaround:

1. Place reference in a folder:
   ```
   C:/Users/uguri/Desktop/refs/style_ref.png
   ```
2. Expose it:
   ```
   agy -p 'Look at the image at C:/Users/uguri/Desktop/refs/style_ref.png.
   Generate a new image in the exact same art style but depicting <NEW_SUBJECT>.
   Save to C:/Users/uguri/Desktop/output.png'
   --add-dir C:/Users/uguri/Desktop/refs
   --dangerously-skip-permissions --print-timeout 3m
   ```
3. For best results, describe what you want preserved: "same color palette, same brush style, same lighting"

## Iterative Refinement

If the first result is not perfect, refine:

```
Generate an image: same as before but <CHANGE>.
Previous attempt was at C:/Users/uguri/Desktop/output.png — improve <SPECIFIC_ASPECT>.
Save to C:/Users/uguri/Desktop/output_v2.png
```

Add `--add-dir` pointing to the previous output so Gemini can see it.

## Quality Tips

- Add `highly detailed, 4K, sharp focus, professional` for extra quality
- Add `no text, no watermark, no signature` to avoid unwanted text
- For characters: `full body, centered, white background, character sheet style`
- For environments: `wide angle, cinematic, volumetric lighting`
