# S117 [P1MP] JU1CE — Alliance Duel Performance Intelligence

Tactical multi-week performance analysis, daily stage breakdowns, and member combat intelligence for **[P1MP] JU1CE** (Server 117) during the weekly Alliance Duel (Alliance Competition / VS) in *Z Route: Redemption*.

🌐 **Live Interactive Multi-Week Dashboard**: [https://jeffxlabs.github.io/s117-p1mp/](https://jeffxlabs.github.io/s117-p1mp/)

---

## ⚡ Features & Capabilities

- 📅 **Multi-Week Event Selector**: Seamlessly switch between any past or present VS match week, or view the **Multi-Week / Career Trends** dashboard.
- 👥 **Operatives Performance Tracker**: Searchable, tier-filtered (*Whale / Top 10*, *High Performer*, *Core*, *Active*), and sortable roster of all 96 alliance members with inline daily trajectory sparklines.
- 🗂️ **Interactive Combat Dossier Modal**: Click any member to pop up their full combat dossier, complete with daily points trajectory, alliance rank, overall rank, and multi-week career history.
- ⚔️ **Daily Stage Breakdown (Monday – Saturday)**: Head-to-head comparison cards for all 6 VS stages (Radar, Base Expansion, Science, Hero Growth, Troop Training, Enemy Assault).
- 🏆 **Full Duel Leaderboards**: Complete daily standings (Mon-Sat + Weekly Total) covering all ~190 duel combatants with live alliance filtering (`[P1MP]` vs opponent).
- ✅ **Strict Rank Integrity Verification**: Built-in verification ensuring strictly contiguous rankings ($1 \dots N$) with zero skipped numbers across every leaderboard.

---

## 🏆 Current Week Summary (2026-09-19: vs [0BS] ZeroBullsht)

| Metric | [P1MP] JU1CE (Home / S117) | [0BS] ZeroBullsht (Opponent) | Advantage |
| :--- | :--- | :--- | :--- |
| **Weekly Total Score** | **3,972,000,390** | 3,392,662,344 | **+579,338,046** (+17.1%) |
| **Stages Won** | **5 Stages** | 1 Stage | **P1MP Champions** |
| **War Share** | **53.94%** | 46.06% | **+7.88%** |
| **Active Roster** | **96 Operatives** | 94 Operatives | **+2** |

### Daily Stage Results

| Day | Stage Theme | [P1MP] JU1CE | [0BS] ZeroBullsht | Stage Winner | Margin |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Monday** | Stage 1: Radar & Exploration | **726,993,167** | 491,589,978 | 🏆 **P1MP** | +235,403,189 |
| **Tuesday** | Stage 2: Base Expansion & Construction | **515,673,737** | 481,958,232 | 🏆 **P1MP** | +33,715,505 |
| **Wednesday** | Stage 3: Scientific Research | **564,910,851** | 544,811,851 | 🏆 **P1MP** | +20,099,000 |
| **Thursday** | Stage 4: Hero Recruitment & Growth | 1,102,056,044 | **1,128,796,856** | 🔴 0BS | +26,740,812 |
| **Friday** | Stage 5: Total Troop Training | **587,062,055** | 567,396,280 | 🏆 **P1MP** | +19,665,775 |
| **Saturday** | Stage 6: Enemy Assault & Elimination | **470,889,288** | 326,733,492 | 🏆 **P1MP** | +144,155,796 |

---

## 🌟 Top 10 MVP Operatives (Current Week)

| Alliance Rank | Overall Duel Rank | Commander | Weekly Points | Alliance Share | Best Stage | Active Days |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: |
| **#1** | #1 | **ViE** | **228,182,613** | 5.74% | Monday (62.1M) | 6/6 |
| **#2** | #2 | **RollingStoners** | **167,053,463** | 4.21% | Thursday (66.0M) | 6/6 |
| **#3** | #3 | **TheRequiem** | **158,455,480** | 3.99% | Monday (48.6M) | 6/6 |
| **#4** | #6 | **Eldagrim** | **124,385,768** | 3.13% | Thursday (33.0M) | 6/6 |
| **#5** | #7 | **Jeff** | **123,757,662** | 3.12% | Thursday (54.7M) | 6/6 |
| **#6** | #9 | **JimmyJam** | **109,315,014** | 2.75% | Thursday (37.2M) | 6/6 |
| **#7** | #10 | **AveGee** | **94,642,886** | 2.38% | Thursday (30.0M) | 6/6 |
| **#8** | #12 | **Whitelne876** | **91,623,383** | 2.31% | Tuesday (21.2M) | 6/6 |
| **#9** | #13 | **Grandpaowl** | **83,576,966** | 2.10% | Thursday (42.1M) | 6/6 |
| **#10** | #15 | **NickiV** | **82,906,539** | 2.09% | Thursday (39.5M) | 6/6 |

---

## 📁 Repository Structure

```
s117-p1mp/
├── index.html                   # Interactive multi-week dashboard & visual tracking application
├── README.md                    # Intelligence briefing & pipeline documentation
├── data/
│   ├── weeks_index.json         # Master registry of all ingested VS weeks
│   ├── multi_week_analytics.json# Career standings, multi-week trajectories & win rates
│   ├── embedded_data.js         # Offline-first bundle containing all weeks & analytics
│   └── weeks/
│       └── 2026-09-19/          # Week archive (Mon-Sat + Weekly Total, summaries, roster)
│           ├── duel_summary.json
│           ├── p1mp_members.json
│           ├── mon.json
│           ├── tue.json
│           ├── wed.json
│           ├── thu.json
│           ├── fri.json
│           ├── sat.json
│           └── week.json
└── pipeline/
    ├── capture_all.py           # Automated BlueStacks capture & Vision OCR ingest engine
    ├── build_analytics.py       # Single-week roster aggregator & mathematical validator
    ├── build_multiweek.py       # Multi-week aggregator & rank contiguity auditor
    ├── cleaner.py               # Data normalizer and integrity checker
    ├── vision_ocr.swift         # Native Apple Vision OCR worker source
    └── vision_ocr               # High-performance compiled native binary
```

---

## 🚀 Ingesting Future Weekly Events

To document a new VS Alliance Competition week from BlueStacks:

1. Ensure the target BlueStacks device is connected:
   ```bash
   adb connect 127.0.0.1:5555
   ```
2. Navigate in-game to **Alliance Competition -> Rankings**.
3. Run the automated pipeline with the new week date:
   ```bash
   python3 pipeline/capture_all.py --week 2026-09-26 --device 127.0.0.1:5555
   ```
   *The pipeline automatically:*
   - Captures all 6 daily stages + weekly total in under 4 minutes.
   - Runs rank integrity verification ensuring **zero skipped ranks** from Rank 1 to bottom.
   - Saves into `data/weeks/<week_id>/`.
   - Aggregates multi-week trends and updates `data/embedded_data.js`.
4. Deploy updates to GitHub Pages:
   ```bash
   git add data/ index.html
   git commit -m "feat(duel): document week 2026-09-26 VS performance"
   git push origin main
   ```
