# [P1MP] JU1CE — Alliance Competition (VS) tracker

Weekly Alliance Competition ("VS" / Alliance Duel) results for **[P1MP] JU1CE**, Server 117, in *Z Route: Redemption*:
every daily leaderboard (MON–SAT) and the weekly total, per-member performance, quota tracking, opponent scouting and
multi-week trends.

**Dashboard:** https://jeffxlabs.github.io/P1MP-VS/ — dark/light themes, 10 languages, deep links for every view
(`?week=2026-10-03&view=members&player=…&lang=fr&theme=light`), works offline from `file://`, laid out for phones and desktop.

- **Overview:** score and day-by-day results, quota check (who is below the 11.4M quota, who missed twice in a row,
  who is new), key takeaways, top performers, biggest movers vs the previous captured week, stage points, rank tiers.
- **Week by week** (`view=record`): every member × every tracked week, colour-coded met / near / below / not in alliance
  / week not captured, with quota record, current streak, average and trend. Filters for "below this week", "missed
  any week", "never missed" and "on a streak". OCR look-alikes (0/O, 1/l/I) are folded so a player matches across weeks.
- **Player profile** (click any name): weekly points and alliance rank vs the previous week, active days, tips
  (quota margin or shortfall, days with no points, strongest stage and the stage with most room to grow vs the alliance
  median, week-over-week change, quota streak), daily points against the alliance median, and weekly history against
  the quota line.
- **Members**, **Leaderboards**, **Opponent**, **Trends**, **Stages**, **Data:** this week's roster with daily heat
  cells (relative to each day's alliance median), full server boards, opponent scouting, alliance-level trends
  (quota compliance by week, stage win rate), stage rules, capture integrity and downloads.

Sister project: [S117 Capitol War rankings](https://jeffxlabs.github.io/ZR-S117-Capitol/).

---

## Weeks tracked

| Week (Sat) | Opponent | Score | Weekly points (leaderboard) | Data snapshot (server time, UTC−2) |
| :-- | :-- | :-: | :-- | :-- |
| 2026-10-03 | [DOOM] Armageddon · S119 | **9 : 0** (clinched) | 4,855,902,583 vs 3,932,140,155 | Sat 2026-10-03 22:02–22:23 (Saturday stage still running) |
| 2026-09-19 | [0BS] ZeroBullsht · S113 | **9 : 0** (clinched) | official 4,033,210,605 vs 3,516,839,111 | ≈ Sat 2026-09-19 23:24 (legacy capture, Saturday still running) |

Each board's own snapshot time (MON 22:02, TUE 22:09, WED 22:14, THU 22:15, FRI 22:18, SAT 22:20, This Week 22:23 for
2026-10-03) is in `data/weeks/<week>/week_summary.json` (`snapshots`) and shown on the dashboard.

The 2026-09-26 week was not captured (the game only shows the current week).

### 2026-10-03 vs [DOOM] Armageddon (S119)

| Stage | Wins | [P1MP] | [DOOM] | Players | Top [P1MP] | Top [DOOM] |
| :-- | :-: | --: | --: | :-: | :-- | :-- |
| Mon · Radar Exploration | 1 | **843,652,863** | 632,286,784 | 90 / 93 | ViE 64.0M | Anr23 30.1M |
| Tue · Base Construction | 2 | **578,994,917** | 530,727,851 | 89 / 90 | Whiteline876 30.1M | snaiperpool 13.2M |
| Wed · Tech Research | 2 | **652,113,534** | 565,291,503 | 89 / 88 | Whiteline876 30.4M | iSeeU 20.7M |
| Thu · Hero Training | 2 | **1,675,713,376** | 1,326,704,853 | 90 / 92 | Whiteline876 75.0M | Anr23 50.4M |
| Fri · Full Military Preparation | 2 | **651,720,934** | 527,295,423 | 89 / 90 | RollingStoners 23.4M | Anr23 15.8M |
| Sat · Enemy Assault (live at 22:20) | 4 | 450,967,191 | 418,698,867 | 93 / 91 | TheRequiem 34.4M | EvVa 19.3M |

Quota (11.4M weekly): 84 of 95 members met it, 1 near (11M–11.4M), 10 below.

---

## Competition rules

Monday–Saturday, one stage per day. Daily wins: Mon 1, Tue–Fri 2 each, Sat 4 — 13 in total, 7 clinches the match.
Stage objectives are listed on the dashboard's **Stages** view (`data/competition_stages.json`).

---

## Data quality

Every published board is checked before it is pushed:

- **Every rank read several times.** Each rank is read on 2–4 screenshots (3.4 on average) and voted on: points must
  agree exactly, names are compared on their letters/digits with look-alike characters folded (l/I/1, O/0,
  Cyrillic/Latin twins), so a decorative symbol or one stray misread cannot win.
- **No skipped or duplicated ranks.** Ranks come from the row geometry and the rank digits on screen; every frame must
  overlap the previous one, and any gap is scrolled back to and re-read. Missing, single-read, disagreeing,
  out-of-order or repeated-player ranks are revisited (repair pass) before a board is accepted.
- **Weekly checksum.** Each player's weekly total must equal the sum of their six days. For 2026-10-03: 183 exact,
  6 joined their alliance mid-week (points earned before joining only appear in the weekly total), 5 left before the
  weekly capture (on day boards only). No unexplained differences.
- **Live boards.** Saturday and This Week change while being read: if a scan shows movement, the board is scanned again
  and merged per player, then re-ranked.
- **Evidence.** Compressed screenshots (720 px WebP) of the frames behind every board are in
  `data/weeks/<week>/screenshots/<tab>/`, chosen so each rank appears on at least two of them, with `index.json`
  (capture time and ranks on each frame). Per-rank read counts and agreement are in `capture_qa.json`.

---

## Capturing a week

Requirements: macOS with Xcode command-line tools (Swift, Vision), `adb`, `cwebp` (optional, `brew install webp`),
BlueStacks at 1080×1920 portrait with the game running.

```sh
adb connect 127.0.0.1:5555
python3 pipeline/capture_all.py --opp-server 119  # all seven tabs, week = this Saturday (server time)
python3 pipeline/capture_all.py --tabs sat,week  # just refresh today's and the weekly board
```

What it does:

1. **Navigates by OCR** from wherever the game is: backs out, taps the **VS** icon on the right-hand side of the city
   screen, then **RANKINGS** at the bottom of the Alliance Competition page.
2. For **MON, TUE, WED, THUR, FRI, SAT, This Week** in that order: taps the tab and confirms it is the highlighted one
   (pixel check), confirms the list starts at rank 1, then scrolls to the very bottom (the list lazy-loads more rows
   near its end; the bottom is only accepted after a second check). The pinned own-rank row under the list is ignored.
3. **Continuous capture:** the list is scrolled continuously while screenshots are taken back to back and read by
   Apple Vision OCR as they arrive (a screenshot is a single rendered frame, so it is sharp even mid-scroll). About
   45–55 s per tab; a full week of seven tabs is roughly 7–10 minutes including repairs.
4. Writes `data/weeks/<week>/{mon,tue,wed,thu,fri,sat,week}.json`, `capture.json`, `capture_qa.json`, the screenshot
   archive, then runs `pipeline/build_week.py` (analytics, `week_data.js`, `data/manifest.js`, cache-busting stamps).
   Exits non-zero if any rank is unresolved (`--allow-incomplete` to override).

Then publish:

```sh
git add data index.html README.md && git commit -m "data: VS week 2026-10-10" && git push
```

Useful flags: `--no-navigate` (Rankings already open), `--week YYYY-MM-DD`, `--no-screenshots`, `--no-build`.

Rebuild a board from saved frames after a parser change (no emulator): `python3 pipeline/reprocess.py <week> <tab> <frames dir>`
(full-size frames are kept in `~/Library/Caches/s117-vs-captures/`).

### Other accounts

Account settings live in `pipeline/profiles/*.json` (home tag, device, look-alike tag spellings). `--profile p2mp`
targets the [P2MP] account on its own BlueStacks instance and pauses/resumes the Apparatchik guard around the capture
(`pipeline/apparatchik_control.py`, pairing as in the Capitol project); that week data belongs in a separate P2MP repo.

---

## Repository layout

```
index.html                    dashboard (single file, no build step)
data/manifest.js|json         weeks list (+ data_version for cache busting)
data/i18n.js, data/stages.js  generated by pipeline/build_i18n.py
data/competition_stages.json  stage rules and activities
data/weeks/<week>/            boards (*.json), week_summary.json, week_data.js, capture*.json, meta.json, screenshots/
pipeline/capture_all.py       capture: navigation, tabs, continuous scan, voting, repair, live-board merge
pipeline/vs_frame_parser.py   screenshot OCR boxes -> ranked rows (row geometry, pinned-row exclusion)
pipeline/build_week.py        analytics, checksum, manifest
pipeline/reprocess.py         rebuild a board from saved frames
pipeline/screenshots.py       compressed screenshot archive
pipeline/vision_ocr.swift     Apple Vision OCR worker; pixel_probe.swift: tab highlight check
pipeline/build_i18n.py        translations (10 languages); stamp_assets.py: cache busting
pipeline/tests/               node checks for translations, data files and the page scripts
```
