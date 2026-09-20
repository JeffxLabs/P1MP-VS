# S117 [P1MP] JU1CE — Alliance Duel Performance Intelligence

Tactical performance analysis, daily stage breakdowns, and member combat intelligence for **[P1MP] JU1CE** (Server 117) during the Alliance Duel (Alliance Competition / VS) against **[0BS] ZeroBullsht** in *Z Route: Redemption*.

🌐 **Live Interactive Dashboard**: [https://jeffxlabs.github.io/s117-p1mp/](https://jeffxlabs.github.io/s117-p1mp/)

---

## 🏆 Duel Summary: P1MP Victory (5 - 1)

| Metric | [P1MP] JU1CE (Home / S117) | [0BS] ZeroBullsht (Opponent) | Advantage |
| :--- | :--- | :--- | :--- |
| **Weekly Total Score** | **3,972,000,390** | 3,392,662,344 | **+579,338,046** (+17.1%) |
| **Stages Won** | **5 Stages** | 1 Stage | **P1MP Champions** |
| **War Share** | **53.94%** | 46.06% | **+7.88%** |
| **Active Roster** | **96 Operatives** | 94 Operatives | **+2** |

---

## 📅 Daily Stage Breakdown (Monday – Saturday)

| Day | Stage Theme | [P1MP] JU1CE | [0BS] ZeroBullsht | Stage Winner | Margin |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Monday** | Stage 1: Radar & Exploration | **726,993,167** | 491,589,978 | 🏆 **P1MP** | +235,403,189 |
| **Tuesday** | Stage 2: Base Expansion & Construction | **515,673,737** | 481,958,232 | 🏆 **P1MP** | +33,715,505 |
| **Wednesday** | Stage 3: Scientific Research | **564,910,851** | 544,811,851 | 🏆 **P1MP** | +20,099,000 |
| **Thursday** | Stage 4: Hero Recruitment & Growth | 1,102,056,044 | **1,128,796,856** | 🔴 0BS | +26,740,812 |
| **Friday** | Stage 5: Total Troop Training | **587,062,055** | 567,396,280 | 🏆 **P1MP** | +19,665,775 |
| **Saturday** | Stage 6: Enemy Assault & Elimination | **470,889,288** | 326,733,492 | 🏆 **P1MP** | +144,155,796 |

---

## 🌟 Top 10 MVP Alliance Operatives

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

## 📁 Repository Structure & Datasets

```
s117-p1mp/
├── index.html                   # Interactive visual web application & member tracker
├── README.md                    # Intelligence briefing & pipeline documentation
├── data/
│   ├── mon.json                 # Monday Stage 1 complete duel rankings (182 players)
│   ├── tue.json                 # Tuesday Stage 2 complete duel rankings (179 players)
│   ├── wed.json                 # Wednesday Stage 3 complete duel rankings (191 players)
│   ├── thu.json                 # Thursday Stage 4 complete duel rankings (192 players)
│   ├── fri.json                 # Friday Stage 5 complete duel rankings (191 players)
│   ├── sat.json                 # Saturday Stage 6 complete duel rankings (187 players)
│   ├── week.json                # Weekly Total complete duel rankings (190 players)
│   ├── p1mp_members.json        # Consolidated 96-member roster with daily metrics & tiers
│   ├── duel_summary.json        # High-level duel match summary & stage point margins
│   └── embedded_data.js         # Offline-first standalone data bundle
└── pipeline/
    ├── capture_all.py           # Automated BlueStacks capture & Vision OCR ingest engine
    ├── build_analytics.py       # Member performance aggregator and validator
    ├── cleaner.py               # Data normalizer and integrity checker
    ├── vision_ocr.swift         # Native Apple Vision OCR worker source
    └── vision_ocr               # High-performance compiled native binary
```

---

## 🚀 Re-Running the Pipeline for Future VS Events

To ingest a new VS Alliance Competition week automatically from BlueStacks:

1. Ensure the target BlueStacks device is connected:
   ```bash
   adb connect 127.0.0.1:5555
   ```
2. Navigate to the in-game **Alliance Competition -> Rankings** screen.
3. Execute the automated pipeline:
   ```bash
   python3 pipeline/capture_all.py
   python3 pipeline/build_analytics.py
   ```
4. Commit and push:
   ```bash
   git add data/ index.html
   git commit -m "feat(duel): ingest weekly VS competition data"
   git push origin main
   ```
