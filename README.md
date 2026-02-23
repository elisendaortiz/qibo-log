# Elis Ortiz — CQT Dev Progress

Live dashboard tracking my contributions to quantum computing open-source projects at the **Centre for Quantum Technologies (CQT)**, National University of Singapore.

🔗 **[View Dashboard](https://elisortiz.github.io/cqt-progress/)**

## What This Is

A self-built progress tracker that turns a weekly task spreadsheet into a live, interactive dashboard — designed to give stakeholders instant visibility into development progress across multiple repos.

Built during a short-term engagement at CQT, where I contribute to the [Qibo](https://github.com/qiboteam) ecosystem: an open-source framework for quantum computing simulation, calibration, and benchmarking.

## Contributions

My work at CQT spans across several repositories, for now:

- **[CQT-reporting](https://github.com/qiboteam/CQT-reporting)** — Automated benchmarking reports: summary metrics, plot extraction, template improvements
- **[qibocal](https://github.com/qiboteam/qibocal)** — Quantum calibration library: bug fixes in tomography and experiment routines
- **[CQT-experiments](https://github.com/qiboteam/CQT-experiments)** — Experiment pipeline: debugging, restructuring, new experiment support

## Dashboard Features

- Task cards with effort estimates, status, and direct links to GitHub Issues/PRs
- Collapsible weekly sections with completion ratios
- Filter by category (Feature, Bug, Access, Docs) with live done/total counts
- Clickable stat cards to isolate completed, in-progress, or blocked work
- Effort distribution chart
- Auto-calculated project duration

## How It Works

```
Google Sheets → export CSV → Python script → data.json → static site on GitHub Pages
```

The dashboard is a single `index.html` that reads from `data.json` at load time. No frameworks, no build step, no dependencies.

Simple.

**Update workflow:**
```bash
python csv_to_json.py "data/Quantum_Tracker_OompaLumpa - Progress_log.csv" data.json
git add -A && git commit -m "Week update" && git push
```

## Tech

HTML, CSS, vanilla JavaScript. Python for data conversion. Hosted on GitHub Pages.

## Contact

**Elis Ortiz** — [GitHub](https://github.com/elisendaortiz) · [LinkedIn](https://linkedin.com/in/elisendaortiz)