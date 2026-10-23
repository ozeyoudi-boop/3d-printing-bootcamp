# CLAUDE.md

Interactive 3D printing course (zero → hero) for the Bambu Lab X2D, published with GitHub Pages.
Live site: https://ozeyoudi-boop.github.io/3d-printing-bootcamp/

## Layout

- `docs/` — the published site (Pages serves this folder from `main`). Generated, do not hand-edit the HTML.
  - `index.html`, `00-orientation.html` … `07-x2d-and-materials.html`, `capstone.html`, `reference.html`
  - `assets/css/main.css` — design system
  - `assets/js/main.js` — progress (localStorage key `bootcamp3d:done`), quizzes, copy buttons, theme, notes, design-for-print checker (`#dfp`)
- `_course/build.py` — source of truth for all page content; writes every file in `docs/*.html`.
- `_course/curriculum.md` — module list, ordering rationale, accuracy notes.

## Workflow

Edit content in `_course/build.py`, then rebuild:

```bash
python3 -I _course/build.py
```

Preview locally (any static server works):

```bash
python3 -m http.server 4173 --directory docs
```

Deploy: commit and `git push origin main`; Pages rebuilds in about a minute.

## Conventions

- Quiz items are `(question, [options], correct_index, explanation)`; pass mark is 70%.
- Adding a module: add it to `ORDER` in `build.py` and to `PAGES` in `main.js` so progress counts it.
- Only state X2D facts that are confirmed (dual nozzle, 65 °C chamber, 300 °C nozzle, ~256×256×256–260 mm build volume, reduced travel with the second nozzle). Send readers to the Bambu Lab Wiki for everything else; do not guess specs.
- Keep it mobile-first: no horizontal page scroll, tap targets ≥ 44 px, wide tables and code scroll inside their own containers.
