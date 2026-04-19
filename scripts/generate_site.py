#!/usr/bin/env python3
import os
from pathlib import Path

REPO = "yahya9090/dancper"
BRANCH = "main"
WALLPAPERS_DIR = Path("wallpapers")
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}

def raw_url(filename):
    return f"https://media.githubusercontent.com/media/{REPO}/{BRANCH}/wallpapers/{filename}"

def get_wallpapers():
    if not WALLPAPERS_DIR.exists():
        print(f"Warning: {WALLPAPERS_DIR} not found")
        return []
    return sorted(
        f.name for f in WALLPAPERS_DIR.iterdir()
        if f.suffix.lower() in IMAGE_EXTS
    )

def build_html(wallpapers):
    items = ""
    for name in wallpapers:
        url = raw_url(name)
        stem = Path(name).stem.replace("_", " ").replace("-", " ")
        items += f"""
      <div class="wall-card" onclick="openLightbox('{url}')">
        <div class="wall-card__media">
          <img loading="lazy" src="{url}" alt="{stem}">
        </div>
      </div>"""

    count = len(wallpapers)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="color-scheme" content="dark light">
  <title>dancper — wallpapers</title>
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,1,0" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Roboto+Flex:opsz,wght@8..144,300;8..144,400;8..144,500;8..144,700&display=swap" rel="stylesheet">
  <script type="importmap">
  {
    "imports": {
      "@material/web/": "https://esm.run/@material/web/"
    }
  }
  </script>
  <script type="module">
    import '@material/web/all.js';
    import {argbFromHex, themeFromSourceColor, applyTheme} from 'https://esm.run/@material/material-color-utilities';
    const seed = '#7C9E3C';
    const theme = themeFromSourceColor(argbFromHex(seed));
    const dark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    applyTheme(theme, {target: document.documentElement, dark});
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
      applyTheme(theme, {target: document.documentElement, dark: e.matches});
    });
  </script>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Roboto Flex', sans-serif;
      background-color: var(--md-sys-color-background);
      color: var(--md-sys-color-on-background);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }
    .top-app-bar {
      position: sticky; top: 0; z-index: 10;
      background-color: var(--md-sys-color-surface-container);
      display: flex; align-items: center; gap: 12px;
      padding: 0 16px; height: 64px;
      box-shadow: 0 1px 0 var(--md-sys-color-outline-variant);
    }
    .top-app-bar__icon { font-family: 'Material Symbols Rounded'; font-size: 24px; color: var(--md-sys-color-on-surface); }
    .top-app-bar__title { font-size: 22px; font-weight: 400; color: var(--md-sys-color-on-surface); flex: 1; }
    .top-app-bar__count {
      font-size: 12px; font-weight: 500; letter-spacing: 0.5px;
      padding: 4px 12px; border-radius: 100px;
      background: var(--md-sys-color-secondary-container);
      color: var(--md-sys-color-on-secondary-container);
    }
    .grid {
      flex: 1;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(min(280px, 100%), 1fr));
      gap: 12px; padding: 16px;
    }
    .wall-card {
      position: relative; border-radius: 16px; overflow: hidden;
      background: var(--md-sys-color-surface-container-high);
      cursor: pointer; aspect-ratio: 16/9;
      transition: box-shadow 0.2s ease;
    }
    .wall-card:hover { box-shadow: 0 4px 16px color-mix(in srgb, var(--md-sys-color-shadow) 24%, transparent); }
    .wall-card__media { width: 100%; height: 100%; }
    .wall-card__media img { width: 100%; height: 100%; object-fit: cover; display: block; transition: transform 0.35s cubic-bezier(0.2,0,0,1); }
    .wall-card:hover .wall-card__media img { transform: scale(1.05); }
    .wall-card::after {
      content: ''; position: absolute; inset: 0;
      background: var(--md-sys-color-on-surface);
      opacity: 0; transition: opacity 0.2s ease; pointer-events: none;
    }
    .wall-card:hover::after { opacity: 0.08; }
    .wall-card:active::after { opacity: 0.12; }
    .lightbox {
      display: none; position: fixed; inset: 0; z-index: 100;
      background: rgba(0,0,0,0.85);
      align-items: center; justify-content: center; padding: 24px;
      backdrop-filter: blur(8px);
    }
    .lightbox.open { display: flex; animation: lb-in 0.2s ease; }
    @keyframes lb-in { from { opacity: 0; } to { opacity: 1; } }
    .lightbox__img { max-width: 100%; max-height: 100%; border-radius: 28px; box-shadow: 0 24px 80px rgba(0,0,0,0.7); object-fit: contain; }
    .lightbox__close { position: absolute; top: 20px; right: 20px; }
    .lightbox__download { position: absolute; bottom: 28px; right: 28px; }
    footer {
      padding: 20px 24px; display: flex; align-items: center; justify-content: space-between;
      border-top: 1px solid var(--md-sys-color-outline-variant);
      font-size: 12px; color: var(--md-sys-color-on-surface-variant);
    }
    footer a { color: var(--md-sys-color-primary); text-decoration: none; }
  </style>
</head>
<body>
  <div class="top-app-bar">
    <span class="top-app-bar__icon">wallpaper</span>
    <span class="top-app-bar__title">dancper</span>
    <span class="top-app-bar__count">COUNT_PLACEHOLDER walls</span>
  </div>
  <main class="grid">ITEMS_PLACEHOLDER
  </main>
  <div class="lightbox" id="lightbox" onclick="closeLightbox(event)">
    <img class="lightbox__img" id="lightbox-img" src="" alt="">
    <md-filled-tonal-icon-button class="lightbox__close" onclick="closeLightbox()">
      <md-icon>close</md-icon>
    </md-filled-tonal-icon-button>
    <md-filled-button class="lightbox__download" id="lightbox-dl" href="" target="_blank">
      <md-icon slot="icon">download</md-icon>
      Download
    </md-filled-button>
  </div>
  <footer>
    <span>dancper wallpaper collection</span>
    <a href="https://github.com/REPO_PLACEHOLDER">github.com/REPO_PLACEHOLDER</a>
  </footer>
  <script>
    const lb = document.getElementById('lightbox');
    const lbImg = document.getElementById('lightbox-img');
    const lbDl = document.getElementById('lightbox-dl');
    function openLightbox(url) {
      lbImg.src = url; lbDl.href = url;
      lb.classList.add('open');
      document.body.style.overflow = 'hidden';
    }
    function closeLightbox(e) {
      if (e && e.target !== lb) return;
      lb.classList.remove('open');
      document.body.style.overflow = '';
      lbImg.src = '';
    }
    document.addEventListener('keydown', e => { if (e.key === 'Escape') { lb.classList.remove('open'); lbImg.src=''; document.body.style.overflow=''; }});
  </script>
</body>
</html>"""

    html = html.replace("COUNT_PLACEHOLDER", str(count))
    html = html.replace("ITEMS_PLACEHOLDER", items)
    html = html.replace("REPO_PLACEHOLDER", REPO)
    return html

if __name__ == "__main__":
    wallpapers = get_wallpapers()
    print(f"Found {len(wallpapers)} wallpapers")
    html = build_html(wallpapers)
    with open("index.html", "w") as f:
        f.write(html)
    print("Generated index.html")
