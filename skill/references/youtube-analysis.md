# YouTube & Video Understanding — Guide

## Tool

Gemini's native video understanding — watches YouTube URLs directly. No download, no transcoding.

## YouTube Videos

```
agy -p 'Watch this YouTube video https://www.youtube.com/watch?v=VIDEO_ID and <QUESTION>. Be specific about what you see and hear.' --dangerously-skip-permissions --print-timeout 3m
```

### Example Questions

- `summarize what happens in the video` — general summary
- `describe the editing techniques and visual style used` — analysis
- `list every product shown with timestamps` — extraction
- `transcribe the key dialogue` — transcription
- `what is the main argument and what evidence is presented?` — critical analysis
- `extract the tutorial steps in order` — how-to extraction

### Advantage Over watch-and-answer

| Feature | Gemini (this skill) | Hermes watch-and-answer |
|---|---|---|
| Method | Native URL parsing | yt-dlp download → transcode/frames |
| Speed | Fast (~10s) | Slower (download + model routing) |
| YouTube | Native, best quality | Works but indirect |
| Local files | Via --add-dir | Direct file upload |
| Long videos | Native support | Compact transcode |

**Rule:** For any YouTube URL, prefer Gemini. For local video files, either works.

## Local Video Files

```
agy -p 'Analyze the video at C:/Users/uguri/Desktop/clip.mp4 and describe what happens. Include visual details and any spoken content.' --dangerously-skip-permissions --add-dir C:/Users/uguri/Desktop --print-timeout 3m
```

## Audio-Only / Transcription

```
agy -p 'Watch https://www.youtube.com/watch?v=VIDEO_ID and provide a full transcript of all spoken content with approximate timestamps.' --dangerously-skip-permissions --print-timeout 3m
```

## Tips

- Always include the full YouTube URL with `https://`
- Be specific about what you want: summary vs. transcript vs. analysis are different
- For long videos (30+ min), ask focused questions rather than "summarize everything"
- Gemini can answer follow-ups about the same video if you use `agy --continue` (not available in `-p` mode — include all questions in one prompt)
