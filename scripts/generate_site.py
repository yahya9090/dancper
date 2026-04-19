#!/usr/bin/env python3
import json
from pathlib import Path

REPO = "yahya9090/dancper"
BRANCH = "main"
WALLPAPERS_DIR = Path("wallpapers")
TAGS_FILE = Path("tags.json")
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}

def raw_url(filename):
    return f"https://media.githubusercontent.com/media/{REPO}/{BRANCH}/wallpapers/{filename}"

def get_wallpapers():
    if not WALLPAPERS_DIR.exists():
        print(f"Warning: {WALLPAPERS_DIR} not found")
        return []
    return sorted(f.name for f in WALLPAPERS_DIR.iterdir() if f.suffix.lower() in IMAGE_EXTS)

def load_tags():
    if TAGS_FILE.exists():
        return json.loads(TAGS_FILE.read_text())
    return {}

def build_html(wallpapers, tags):
    # Collect filter tags
    all_genre = set()
    all_mood = set()
    all_colors = set()
    for name in wallpapers:
        t = tags.get(name, {})
        for v in t.get("genre", []): all_genre.add(v.lower())
        for v in t.get("mood", []): all_mood.add(v.lower())
        for v in t.get("colors", []): all_colors.add(v.lower())

    # Build wallpaper data as JSON for JS
    wall_data = []
    for name in wallpapers:
        t = tags.get(name, {})
        is_gif = name.lower().endswith(".gif") or t.get("animated", False)
        wall_data.append({
            "name": name,
            "url": raw_url(name),
            "gif": is_gif,
            "genre": [v.lower() for v in t.get("genre", [])],
            "mood": [v.lower() for v in t.get("mood", [])],
            "colors": [v.lower() for v in t.get("colors", [])],
        })

    wall_json = json.dumps(wall_data)

    def chips(tags_set, group):
        out = f'<md-filter-chip label="All" class="chip chip--{group} chip--active" data-group="{group}" data-tag="all" onclick="setFilter(\'{group}\',\'all\',this)"></md-filter-chip>'
        for tag in sorted(tags_set):
            out += f'<md-filter-chip label="{tag}" class="chip chip--{group}" data-group="{group}" data-tag="{tag}" onclick="setFilter(\'{group}\',\'{tag}\',this)"></md-filter-chip>'
        return out

    genre_chips = chips(all_genre, "genre")
    mood_chips = chips(all_mood, "mood")
    color_chips = chips(all_colors, "colors")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="color-scheme" content="dark light">
  <title>dancper — wallpapers</title>
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,1,0" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Roboto+Flex:opsz,wght@8..144,300;8..144,400;8..144,500;8..144,700&display=swap" rel="stylesheet">
  <script type="importmap">
  {{
    "imports": {{
      "@material/web/": "https://esm.run/@material/web/"
    }}
  }}
  </script>
  <script type="module">
    import '@material/web/all.js';
    import {{argbFromHex, themeFromSourceColor, applyTheme}} from 'https://esm.run/@material/material-color-utilities';
    const theme = themeFromSourceColor(argbFromHex('#7C9E3C'));
    const applyDark = d => applyTheme(theme, {{target: document.documentElement, dark: d}});
    applyDark(matchMedia('(prefers-color-scheme: dark)').matches);
    matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => applyDark(e.matches));
  </script>
  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Roboto Flex', sans-serif;
      background: var(--md-sys-color-background);
      color: var(--md-sys-color-on-background);
      min-height: 100vh; display: flex; flex-direction: column;
    }}

    /* ── Top App Bar ── */
    .top-bar {{
      position: sticky; top: 0; z-index: 20;
      background: var(--md-sys-color-surface-container);
      display: flex; align-items: center; gap: 8px;
      padding: 0 12px; height: 64px;
      box-shadow: 0 1px 0 var(--md-sys-color-outline-variant);
    }}
    .top-bar__title {{ font-size: 20px; font-weight: 400; color: var(--md-sys-color-on-surface); flex: 1; margin-left: 4px; }}
    .top-bar__count {{
      font-size: 11px; font-weight: 500; letter-spacing: 0.5px;
      padding: 3px 10px; border-radius: 100px;
      background: var(--md-sys-color-secondary-container);
      color: var(--md-sys-color-on-secondary-container);
    }}
    .mi {{ font-family: 'Material Symbols Rounded'; font-size: 24px; color: var(--md-sys-color-on-surface-variant); user-select: none; }}

    /* ── Filter bar ── */
    .filter-bar {{
      background: var(--md-sys-color-surface);
      border-bottom: 1px solid var(--md-sys-color-outline-variant);
    }}
    .filter-section {{
      display: flex; align-items: center; gap: 8px;
      padding: 8px 12px; overflow-x: auto; scrollbar-width: none;
    }}
    .filter-section::-webkit-scrollbar {{ display: none; }}
    .filter-label {{
      font-size: 11px; font-weight: 500; letter-spacing: 0.8px; text-transform: uppercase;
      color: var(--md-sys-color-on-surface-variant); white-space: nowrap; min-width: 44px;
    }}
    md-filter-chip {{ flex-shrink: 0; cursor: pointer; --md-filter-chip-container-shape: 8px; }}

    /* ── Sort + page size bar ── */
    .controls-bar {{
      display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
      padding: 8px 12px;
      background: var(--md-sys-color-surface-container-low);
      border-bottom: 1px solid var(--md-sys-color-outline-variant);
    }}
    .controls-bar label {{ font-size: 12px; color: var(--md-sys-color-on-surface-variant); }}
    .controls-bar select {{
      font-family: inherit; font-size: 13px;
      background: var(--md-sys-color-surface-container-high);
      color: var(--md-sys-color-on-surface);
      border: 1px solid var(--md-sys-color-outline-variant);
      border-radius: 8px; padding: 4px 8px; cursor: pointer;
    }}
    .spacer {{ flex: 1; }}
    #sel-count {{
      font-size: 12px; color: var(--md-sys-color-primary);
      display: none;
    }}
    #sel-count.visible {{ display: block; }}

    /* ── Grid ── */
    .grid {{
      flex: 1; display: grid;
      grid-template-columns: repeat(auto-fill, minmax(min(260px, 100%), 1fr));
      gap: 10px; padding: 12px;
    }}

    /* ── Wall Card ── */
    .wall-card {{
      position: relative; border-radius: 14px; overflow: hidden;
      background: var(--md-sys-color-surface-container-high);
      cursor: pointer; aspect-ratio: 16/9;
      outline: 3px solid transparent;
      transition: outline-color 0.15s, box-shadow 0.2s;
    }}
    .wall-card:focus-visible {{ outline: 3px solid var(--md-sys-color-primary); outline-offset: 2px; }}
    .wall-card.selected {{ outline: 3px solid var(--md-sys-color-primary); }}
    .wall-card__media {{ width: 100%; height: 100%; }}
    .wall-card__media img {{
      width: 100%; height: 100%; object-fit: cover; display: block;
      opacity: 0; transition: opacity 0.35s ease, transform 0.3s cubic-bezier(0.2,0,0,1);
    }}
    .wall-card__media img.loaded {{ opacity: 1; }}
    .wall-card:hover .wall-card__media img {{ transform: scale(1.04); }}

    /* State layer */
    .wall-card::before {{
      content: ''; position: absolute; inset: 0;
      background: var(--md-sys-color-on-surface);
      opacity: 0; transition: opacity 0.15s; pointer-events: none; z-index: 1;
    }}
    .wall-card:hover::before {{ opacity: 0.06; }}
    .wall-card:active::before {{ opacity: 0.1; }}

    /* Hover download overlay */
    .wall-card__hover {{
      position: absolute; inset: 0; z-index: 2;
      display: flex; align-items: flex-end; justify-content: flex-end;
      padding: 8px; opacity: 0; transition: opacity 0.2s;
      pointer-events: none;
    }}
    .wall-card:hover .wall-card__hover {{ opacity: 1; pointer-events: auto; }}
    .dl-btn {{
      display: flex; align-items: center; justify-content: center;
      width: 36px; height: 36px; border-radius: 50%; border: none; cursor: pointer;
      background: var(--md-sys-color-surface-container);
      color: var(--md-sys-color-on-surface);
      box-shadow: 0 2px 8px rgba(0,0,0,0.3);
      transition: background 0.15s, transform 0.15s;
    }}
    .dl-btn:hover {{ background: var(--md-sys-color-primary-container); transform: scale(1.1); }}
    .dl-btn .mi {{ font-size: 20px; color: var(--md-sys-color-on-surface); }}

    /* Selection checkbox indicator */
    .wall-card__check {{
      position: absolute; top: 8px; left: 8px; z-index: 3;
      width: 22px; height: 22px; border-radius: 50%;
      background: var(--md-sys-color-surface-container);
      border: 2px solid var(--md-sys-color-outline);
      display: flex; align-items: center; justify-content: center;
      opacity: 0; transition: opacity 0.15s, background 0.15s;
      pointer-events: none;
    }}
    .wall-card__check .mi {{ font-size: 14px; color: var(--md-sys-color-on-primary); display: none; }}
    .selection-mode .wall-card__check {{ opacity: 1; }}
    .wall-card.selected .wall-card__check {{
      background: var(--md-sys-color-primary);
      border-color: var(--md-sys-color-primary);
    }}
    .wall-card.selected .wall-card__check .mi {{ display: flex; }}

    /* GIF badge */
    .gif-badge {{
      position: absolute; top: 8px; right: 8px; z-index: 3;
      background: var(--md-sys-color-tertiary-container);
      color: var(--md-sys-color-on-tertiary-container);
      font-size: 10px; font-weight: 700; letter-spacing: 1px;
      padding: 2px 6px; border-radius: 6px; pointer-events: none;
    }}

    /* Empty state */
    .empty {{
      grid-column: 1/-1; display: flex; flex-direction: column;
      align-items: center; gap: 12px; padding: 80px 24px;
      color: var(--md-sys-color-on-surface-variant);
    }}
    .empty .mi {{ font-size: 48px; opacity: 0.4; }}

    /* ── Pagination ── */
    .pagination {{
      display: flex; align-items: center; justify-content: center;
      gap: 4px; padding: 16px 12px;
      border-top: 1px solid var(--md-sys-color-outline-variant);
      flex-wrap: wrap;
    }}
    .page-info {{ font-size: 12px; color: var(--md-sys-color-on-surface-variant); margin: 0 8px; }}

    /* ── Lightbox ── */
    .lightbox {{
      display: none; position: fixed; inset: 0; z-index: 100;
      background: rgba(0,0,0,0.92); align-items: center; justify-content: center;
      padding: 24px; backdrop-filter: blur(16px);
    }}
    .lightbox.open {{ display: flex; animation: lb-in 0.18s ease; }}
    @keyframes lb-in {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    .lightbox__img {{
      max-width: min(100%, 1600px); max-height: calc(100vh - 96px);
      border-radius: 16px; object-fit: contain;
      box-shadow: 0 32px 80px rgba(0,0,0,0.8);
      animation: img-in 0.22s cubic-bezier(0.2,0,0,1);
    }}
    @keyframes img-in {{ from {{ transform: scale(0.94); opacity:0; }} to {{ transform: scale(1); opacity:1; }} }}
    .lb-close {{ position: absolute; top: 16px; right: 16px; }}
    .lb-dl {{ position: absolute; bottom: 24px; right: 24px; }}
    .lb-nav {{
      position: absolute; top: 50%; transform: translateY(-50%);
      display: flex; align-items: center; justify-content: center;
      width: 48px; height: 48px; border-radius: 50%; border: none; cursor: pointer;
      background: var(--md-sys-color-surface-container);
      color: var(--md-sys-color-on-surface);
      box-shadow: 0 2px 12px rgba(0,0,0,0.4); transition: background 0.15s;
    }}
    .lb-nav:hover {{ background: var(--md-sys-color-surface-container-high); }}
    .lb-prev {{ left: 16px; }}
    .lb-next {{ right: 80px; }}

    /* ── Footer ── */
    footer {{
      padding: 16px 20px; display: flex; align-items: center; justify-content: space-between;
      border-top: 1px solid var(--md-sys-color-outline-variant);
      font-size: 11px; color: var(--md-sys-color-on-surface-variant);
    }}
    footer a {{ color: var(--md-sys-color-primary); text-decoration: none; }}
  </style>
</head>
<body>

  <!-- Top App Bar -->
  <div class="top-bar">
    <span class="mi">wallpaper</span>
    <span class="top-bar__title">dancper</span>
    <span class="top-bar__count" id="top-count">0 walls</span>
    <md-icon-button id="sel-toggle" title="Toggle selection mode">
      <span class="mi">check_box</span>
    </md-icon-button>
    <md-icon-button id="batch-dl-btn" title="Download selected (Ctrl+D)" style="display:none">
      <span class="mi">download</span>
    </md-icon-button>
  </div>

  <!-- Filter Bar -->
  <div class="filter-bar">
    <div class="filter-section">
      <span class="filter-label">Genre</span>
      {genre_chips}
    </div>
    <div class="filter-section">
      <span class="filter-label">Mood</span>
      {mood_chips}
    </div>
    <div class="filter-section">
      <span class="filter-label">Color</span>
      {color_chips}
    </div>
  </div>

  <!-- Controls Bar -->
  <div class="controls-bar">
    <label>Sort:
      <select id="sort-sel" onchange="applyFilters()">
        <option value="name">Name</option>
        <option value="color">Color</option>
        <option value="genre">Genre</option>
      </select>
    </label>
    <label>Per page:
      <select id="page-size-sel" onchange="setPageSize(this.value)">
        <option value="10">10</option>
        <option value="20">20</option>
        <option value="30" selected>30</option>
        <option value="40">40</option>
        <option value="50">50</option>
        <option value="100">100</option>
        <option value="200">200</option>
        <option value="99999">All</option>
      </select>
    </label>
    <span class="spacer"></span>
    <span id="sel-count"></span>
  </div>

  <!-- Grid -->
  <main class="grid" id="grid"></main>

  <!-- Pagination -->
  <div class="pagination" id="pagination"></div>

  <!-- Lightbox -->
  <div class="lightbox" id="lightbox">
    <button class="lb-nav lb-prev" onclick="lbNav(-1)"><span class="mi">chevron_left</span></button>
    <img class="lightbox__img" id="lb-img" src="" alt="">
    <button class="lb-nav lb-next" onclick="lbNav(1)"><span class="mi">chevron_right</span></button>
    <md-filled-tonal-icon-button class="lb-close" id="lb-close">
      <md-icon>close</md-icon>
    </md-filled-tonal-icon-button>
    <md-filled-button class="lb-dl" id="lb-dl-btn">
      <md-icon slot="icon">download</md-icon>
      Download
    </md-filled-button>
  </div>

  <footer>
    <span>dancper wallpaper collection</span>
    <a href="https://github.com/{REPO}">github.com/{REPO}</a>
  </footer>

  <script>
    const ALL_WALLS = {wall_json};

    // ── State ──
    let filtered = [...ALL_WALLS];
    let page = 0;
    let pageSize = 30;
    let selectionMode = false;
    let selected = new Set();
    let lbIndex = -1;   // index in filtered array
    let lastClickIndex = -1;
    let activeFilters = {{ genre: 'all', mood: 'all', colors: 'all' }};
    let activeSort = 'name';

    // ── Filter + Sort ──
    function setFilter(group, tag, el) {{
      activeFilters[group] = tag;
      document.querySelectorAll(`.chip--${{group}}`).forEach(c => c.removeAttribute('selected'));
      el.setAttribute('selected', '');
      page = 0;
      applyFilters();
    }}

    function applyFilters() {{
      activeSort = document.getElementById('sort-sel').value;
      filtered = ALL_WALLS.filter(w => {{
        for (const [group, tag] of Object.entries(activeFilters)) {{
          if (tag === 'all') continue;
          const arr = w[group] || [];
          if (!arr.includes(tag)) return false;
        }}
        return true;
      }});
      if (activeSort === 'color') filtered.sort((a,b) => (a.colors[0]||'').localeCompare(b.colors[0]||''));
      else if (activeSort === 'genre') filtered.sort((a,b) => (a.genre[0]||'').localeCompare(b.genre[0]||''));
      else filtered.sort((a,b) => a.name.localeCompare(b.name));

      selected.clear();
      updateSelCount();
      renderPage();
    }}

    function setPageSize(v) {{
      pageSize = parseInt(v);
      page = 0;
      renderPage();
    }}

    // ── Render ──
    function renderPage() {{
      const grid = document.getElementById('grid');
      const start = page * pageSize;
      const end = Math.min(start + pageSize, filtered.length);
      const slice = filtered.slice(start, end);

      document.getElementById('top-count').textContent = filtered.length + ' walls';

      if (slice.length === 0) {{
        grid.innerHTML = '<div class="empty"><span class="mi">search_off</span><span>No wallpapers match</span></div>';
        document.getElementById('pagination').innerHTML = '';
        return;
      }}

      grid.innerHTML = slice.map((w, i) => {{
        const gi = start + i;
        const isSel = selected.has(w.name);
        return `<div class="wall-card${{isSel ? ' selected' : ''}}"
          tabindex="0"
          data-name="${{w.name}}"
          data-url="${{w.url}}"
          data-gi="${{gi}}"
          onclick="cardClick(event, ${{gi}})"
          onkeydown="cardKey(event, ${{gi}})">
          <div class="wall-card__check"><span class="mi">check</span></div>
          <div class="wall-card__media">
            <img loading="lazy" src="${{w.url}}" alt="${{w.name}}" decoding="async"
              onload="this.classList.add('loaded')">
            ${{w.gif ? '<span class="gif-badge">GIF</span>' : ''}}
          </div>
          <div class="wall-card__hover">
            <button class="dl-btn" onclick="dlCard(event,'${{w.url}}','${{w.name}}')" title="Download">
              <span class="mi">download</span>
            </button>
          </div>
        </div>`;
      }}).join('');

      if (selectionMode) grid.classList.add('selection-mode');
      renderPagination();
    }}

    function renderPagination() {{
      const total = filtered.length;
      const totalPages = Math.ceil(total / pageSize);
      if (totalPages <= 1) {{ document.getElementById('pagination').innerHTML = ''; return; }}

      const start = page * pageSize + 1;
      const end = Math.min((page+1)*pageSize, total);
      let html = `<md-icon-button ${{page===0?'disabled':''}} onclick="goPage(${{page-1}})"><md-icon>chevron_left</md-icon></md-icon-button>`;

      // Show limited page buttons
      const maxBtns = 7;
      let pages = [];
      if (totalPages <= maxBtns) {{
        pages = Array.from({{length: totalPages}}, (_,i) => i);
      }} else {{
        pages = [0];
        let lo = Math.max(1, page-2), hi = Math.min(totalPages-2, page+2);
        if (lo > 1) pages.push('...');
        for (let i=lo; i<=hi; i++) pages.push(i);
        if (hi < totalPages-2) pages.push('...');
        pages.push(totalPages-1);
      }}

      pages.forEach(p => {{
        if (p === '...') {{ html += `<span style="padding:0 4px;color:var(--md-sys-color-on-surface-variant)">…</span>`; return; }}
        html += `<md-filled-tonal-button ${{p===page?'':''}} onclick="goPage(${{p}})"
          style="${{p===page ? 'background:var(--md-sys-color-primary-container)' : ''}}">
          ${{p+1}}
        </md-filled-tonal-button>`;
      }});

      html += `<md-icon-button ${{page>=totalPages-1?'disabled':''}} onclick="goPage(${{page+1}})"><md-icon>chevron_right</md-icon></md-icon-button>`;
      html += `<span class="page-info">${{start}}–${{end}} of ${{total}}</span>`;
      document.getElementById('pagination').innerHTML = html;
    }}

    function goPage(p) {{
      page = p;
      renderPage();
      window.scrollTo({{top: 0, behavior: 'smooth'}});
    }}

    // ── Card interaction ──
    function cardClick(e, gi) {{
      if (e.target.closest('.dl-btn')) return;
      const w = filtered[gi];
      if (!w) return;

      if (selectionMode || e.ctrlKey || e.metaKey) {{
        e.preventDefault();
        toggleSelect(w.name);
        lastClickIndex = gi;
        return;
      }}
      if (e.shiftKey && lastClickIndex >= 0) {{
        e.preventDefault();
        const lo = Math.min(gi, lastClickIndex), hi = Math.max(gi, lastClickIndex);
        for (let i=lo; i<=hi; i++) {{
          if (filtered[i]) selected.add(filtered[i].name);
        }}
        updateSelCount();
        renderPage();
        return;
      }}
      lastClickIndex = gi;
      openLightbox(gi);
    }}

    function cardKey(e, gi) {{
      if (e.key === 'Enter' || e.key === ' ') {{ e.preventDefault(); cardClick(e, gi); }}
      if (e.key === 'ArrowRight') {{ e.preventDefault(); focusCard(gi+1); }}
      if (e.key === 'ArrowLeft') {{ e.preventDefault(); focusCard(gi-1); }}
      if (e.key === 'ArrowDown') {{
        e.preventDefault();
        const cols = getColCount();
        focusCard(gi + cols);
      }}
      if (e.key === 'ArrowUp') {{
        e.preventDefault();
        const cols = getColCount();
        focusCard(gi - cols);
      }}
    }}

    function getColCount() {{
      const grid = document.getElementById('grid');
      const firstCard = grid.querySelector('.wall-card');
      if (!firstCard) return 1;
      return Math.round(grid.offsetWidth / firstCard.offsetWidth);
    }}

    function focusCard(gi) {{
      if (gi < 0 || gi >= filtered.length) return;
      const targetPage = Math.floor(gi / pageSize);
      if (targetPage !== page) {{ page = targetPage; renderPage(); }}
      const localIdx = gi - page * pageSize;
      const cards = document.querySelectorAll('.wall-card');
      if (cards[localIdx]) cards[localIdx].focus();
    }}

    // ── Selection ──
    function toggleSelect(name) {{
      if (selected.has(name)) selected.delete(name);
      else selected.add(name);
      updateSelCount();
      renderPage();
    }}

    function updateSelCount() {{
      const el = document.getElementById('sel-count');
      const dlBtn = document.getElementById('batch-dl-btn');
      if (selected.size > 0) {{
        el.textContent = selected.size + ' selected';
        el.classList.add('visible');
        dlBtn.style.display = '';
      }} else {{
        el.classList.remove('visible');
        dlBtn.style.display = 'none';
      }}
    }}

    document.getElementById('sel-toggle').addEventListener('click', () => {{
      selectionMode = !selectionMode;
      selected.clear();
      updateSelCount();
      const grid = document.getElementById('grid');
      grid.classList.toggle('selection-mode', selectionMode);
      renderPage();
    }});

    // ── Download ──
    async function dlCard(e, url, name) {{
      e.stopPropagation();
      const a = document.createElement('a');
      try {{
        const blob = await fetch(url).then(r => r.blob());
        a.href = URL.createObjectURL(blob);
      }} catch {{ a.href = url; }}
      a.download = name;
      a.click();
    }}

    document.getElementById('batch-dl-btn').addEventListener('click', batchDownload);

    async function batchDownload() {{
      for (const name of selected) {{
        const w = ALL_WALLS.find(x => x.name === name);
        if (!w) continue;
        const a = document.createElement('a');
        try {{
          const blob = await fetch(w.url).then(r => r.blob());
          a.href = URL.createObjectURL(blob);
        }} catch {{ a.href = w.url; }}
        a.download = name;
        a.click();
        await new Promise(r => setTimeout(r, 300));
      }}
    }}

    // ── Lightbox ──
    const lb = document.getElementById('lightbox');
    const lbImg = document.getElementById('lb-img');

    function openLightbox(gi) {{
      lbIndex = gi;
      const w = filtered[gi];
      if (!w) return;
      lbImg.src = w.url;
      document.getElementById('lb-dl-btn').onclick = () => dlCard(new Event('click'), w.url, w.name);
      lb.classList.add('open');
      document.body.style.overflow = 'hidden';
    }}

    function closeLightbox() {{
      lb.classList.remove('open');
      document.body.style.overflow = '';
      setTimeout(() => lbImg.src = '', 200);
      lbIndex = -1;
    }}

    function lbNav(dir) {{
      const next = lbIndex + dir;
      if (next >= 0 && next < filtered.length) openLightbox(next);
    }}

    lb.addEventListener('click', e => {{ if (e.target === lb) closeLightbox(); }});
    document.getElementById('lb-close').addEventListener('click', closeLightbox);

    // ── Keyboard shortcuts ──
    document.addEventListener('keydown', e => {{
      if (lb.classList.contains('open')) {{
        if (e.key === 'Escape') closeLightbox();
        if (e.key === 'ArrowRight') lbNav(1);
        if (e.key === 'ArrowLeft') lbNav(-1);
        return;
      }}
      if ((e.ctrlKey || e.metaKey) && e.key === 'a') {{
        e.preventDefault();
        const start = page * pageSize, end = Math.min(start + pageSize, filtered.length);
        for (let i=start; i<end; i++) selected.add(filtered[i].name);
        updateSelCount(); renderPage();
      }}
      if ((e.ctrlKey || e.metaKey) && e.key === 'd') {{
        e.preventDefault();
        if (selected.size > 0) batchDownload();
      }}
    }});

    // ── Init ──
    applyFilters();
  </script>
</body>
</html>"""

if __name__ == "__main__":
    wallpapers = get_wallpapers()
    tags = load_tags()
    print(f"Found {len(wallpapers)} wallpapers, {len(tags)} tagged")
    html = build_html(wallpapers, tags)
    with open("index.html", "w") as f:
        f.write(html)
    print("Generated index.html")
