# App Scaffolding — Template Guide

Use this template when asking Gemini to scaffold a complete application.

## Base Prompt Template

```
Create a complete single-file HTML app at C:/Users/uguri/Desktop/<NAME>.html:

PURPOSE: <one sentence>
FEATURES:
- <feature 1>
- <feature 2>
- <feature 3>

DESIGN:
- Style: <modern minimal / glassmorphism / brutalist / neumorphism>
- Colors: <palette>
- Layout: <single column / sidebar / grid / dashboard>
- Responsive: yes, mobile-first
- Dark mode: yes/no

TECH:
- Single HTML file, CSS and JS inline
- <vanilla JS / React via CDN / Vue via CDN>
- <localStorage / no persistence / mock data>

POLISH:
- Loading, empty, and error states
- Smooth animations and transitions
- Keyboard shortcuts where useful
- Production-ready, no placeholders

Save to C:/Users/uguri/Desktop/<NAME>.html and verify the file exists.
```

## Example: Todo App

```
Create a complete single-file HTML app at C:/Users/uguri/Desktop/todo.html:
A beautiful todo app with add/edit/delete, categories (work/personal),
priority (high/medium/low) with colors, due dates, search/filter,
localStorage, dark/light toggle, drag to reorder, progress bar.
Design: glassmorphism, rounded corners, smooth animations, responsive.
Single HTML file, CSS and JS inline. Polished and production-ready.
```

## Example: Dashboard

```
Create a complete single-file HTML app at C:/Users/uguri/Desktop/dashboard.html:
An analytics dashboard with 4 stat cards, line chart (Chart.js via CDN),
recent activity feed, date range picker, export to CSV.
Design: dark theme, sidebar navigation, card grid, Tailwind-like utility styles.
Single HTML file. Polished and production-ready.
```

## Example: Game

```
Create a complete single-file HTML game at C:/Users/uguri/Desktop/game.html:
A Snake game with WASD/arrows, score, high score (localStorage),
pause, game over screen, difficulty levels, touch controls for mobile.
Design: retro pixel style, neon colors on dark background, canvas-based.
Single HTML file. Polished and playable.
```
