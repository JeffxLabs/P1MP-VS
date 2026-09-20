#!/usr/bin/env python3
"""
Multi-Week Aggregator & Integrity Validator for S117-P1MP.
Validates zero skipped ranks, compiles multi-week member trends, and generates standalone bundles.
"""
import os
import json
import glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
WEEKS_DIR = os.path.join(DATA_DIR, "weeks")

DAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat']

def validate_week_ranks(week_path, week_id):
    """Ensure no numbers are skipped in rankings for any day or weekly total."""
    errors = []
    for d in DAYS + ['week']:
        p = os.path.join(week_path, f"{d}.json")
        if not os.path.exists(p):
            errors.append(f"Missing file: {d}.json in {week_id}")
            continue
        with open(p) as f:
            records = json.load(f)
        ranks = [r['rank'] for r in records]
        max_rank = max(ranks) if ranks else 0
        missing = [r for r in range(1, max_rank + 1) if r not in ranks]
        if missing:
            errors.append(f"[{week_id}/{d.upper()}] SKIPPED RANKS DETECTED: {missing[:10]} (total {len(missing)} missing)")
    return errors

def build_multi_week():
    print("=== Scanning Weeks in data/weeks/ ===")
    week_dirs = sorted([d for d in os.listdir(WEEKS_DIR) if os.path.isdir(os.path.join(WEEKS_DIR, d))])
    print(f"Found {len(week_dirs)} week(s): {week_dirs}")

    weeks_index = []
    weeks_bundle = {}
    member_history = {} # player -> { total_pts, weeks_played, history: { week_id: {...} } }

    all_validation_errors = []

    for wid in week_dirs:
        wpath = os.path.join(WEEKS_DIR, wid)
        errs = validate_week_ranks(wpath, wid)
        if errs:
            all_validation_errors.extend(errs)
        else:
            print(f"  ✓ [{wid}] Rank Integrity Verified: 0 skipped ranks across all 7 leaderboards.")

        duel = json.load(open(os.path.join(wpath, "duel_summary.json")))
        members = json.load(open(os.path.join(wpath, "p1mp_members.json")))
        daily = {d: json.load(open(os.path.join(wpath, f"{d}.json"))) for d in DAYS + ['week']}

        w_summary = {
            "id": wid,
            "date": wid,
            "title": f"Week {wid} (vs [{duel['opponent_alliance']['tag']}] {duel['opponent_alliance']['name']})",
            "opponent_tag": duel['opponent_alliance']['tag'],
            "opponent_name": duel['opponent_alliance']['name'],
            "winner": duel['weekly_result']['winner'],
            "p1mp_points": duel['weekly_result']['p1mp_total_points'],
            "obs_points": duel['weekly_result']['obs_total_points'],
            "margin": duel['weekly_result']['total_margin'],
            "stages_won": duel['weekly_result'].get('p1mp_stages_won', 5),
            "stages_lost": duel['weekly_result'].get('obs_stages_won', 1),
            "members_count": len(members),
            "top_performer": members[0]['player'] if members else ""
        }
        weeks_index.append(w_summary)

        weeks_bundle[wid] = {
            "summary": w_summary,
            "duel": duel,
            "members": members,
            "daily": daily
        }

        # Accumulate member history
        for m in members:
            pname = m['player']
            if pname not in member_history:
                member_history[pname] = {
                    "player": pname,
                    "alliance": m['alliance'],
                    "total_points": 0,
                    "weeks_count": 0,
                    "best_week": None,
                    "best_week_pts": -1,
                    "best_week_rank": 999,
                    "history": {}
                }
            rec = member_history[pname]
            rec["total_points"] += m['weekly_points']
            rec["weeks_count"] += 1
            if m['weekly_points'] > rec["best_week_pts"]:
                rec["best_week_pts"] = m['weekly_points']
                rec["best_week"] = wid
            if m['alliance_rank'] < rec["best_week_rank"]:
                rec["best_week_rank"] = m['alliance_rank']

            rec["history"][wid] = {
                "weekly_points": m['weekly_points'],
                "alliance_rank": m['alliance_rank'],
                "overall_rank": m['overall_rank'],
                "tier": m['tier'],
                "active_days": m['active_days'],
                "best_day": m['best_day'],
                "daily_breakdown": m['daily_breakdown']
            }

    if all_validation_errors:
        print("\n⚠️ VALIDATION WARNINGS:")
        for e in all_validation_errors:
            print("  ", e)
    else:
        print("\n✅ PERFECT RANK INTEGRITY: All ranks are strictly contiguous with zero numbers skipped.")

    # Calculate member multi-week averages and rankings
    multi_members = []
    for pname, rec in member_history.items():
        avg_pts = round(rec["total_points"] / max(rec["weeks_count"], 1))
        rec["avg_weekly_points"] = avg_pts
        multi_members.append(rec)

    # Sort multi-week members by total points
    multi_members.sort(key=lambda x: x["total_points"], reverse=True)
    for idx, m in enumerate(multi_members, 1):
        m["career_rank"] = idx

    # Alliance multi-week analytics
    total_alliance_pts = sum(w["p1mp_points"] for w in weeks_index)
    total_opponent_pts = sum(w["obs_points"] for w in weeks_index)
    wins = sum(1 for w in weeks_index if w["winner"] == "P1MP")
    losses = len(weeks_index) - wins

    # Stage dominance across all weeks
    stage_wins = {d: 0 for d in DAYS}
    stage_totals_p1mp = {d: 0 for d in DAYS}
    stage_totals_opp = {d: 0 for d in DAYS}
    for wid, wdata in weeks_bundle.items():
        for st in wdata["duel"]["daily_stages"]:
            d = st["day"]
            if st["winner"] == "P1MP":
                stage_wins[d] += 1
            stage_totals_p1mp[d] += st["p1mp_points"]
            stage_totals_opp[d] += st["obs_points"]

    multi_week_analytics = {
        "total_weeks": len(weeks_index),
        "record": f"{wins}-{losses}",
        "total_p1mp_points": total_alliance_pts,
        "total_opponent_points": total_opponent_pts,
        "average_weekly_points": round(total_alliance_pts / max(len(weeks_index), 1)),
        "stage_dominance": {
            d: {
                "wins": stage_wins[d],
                "win_pct": round((stage_wins[d] / max(len(weeks_index), 1)) * 100, 1),
                "total_p1mp_pts": stage_totals_p1mp[d],
                "total_opp_pts": stage_totals_opp[d]
            } for d in DAYS
        },
        "members": multi_members
    }

    # Save to data files
    with open(os.path.join(DATA_DIR, "weeks_index.json"), "w", encoding="utf-8") as f:
        json.dump(weeks_index, f, indent=2, ensure_ascii=False)
    with open(os.path.join(DATA_DIR, "multi_week_analytics.json"), "w", encoding="utf-8") as f:
        json.dump(multi_week_analytics, f, indent=2, ensure_ascii=False)

    # Master JavaScript embedded bundle
    full_bundle = {
        "weeksIndex": weeks_index,
        "latestWeekId": weeks_index[-1]["id"] if weeks_index else "",
        "multiWeek": multi_week_analytics,
        "weeks": weeks_bundle
    }

    with open(os.path.join(DATA_DIR, "embedded_data.js"), "w", encoding="utf-8") as f:
        f.write("window.P1MP_DATA = " + json.dumps(full_bundle, ensure_ascii=False) + ";\n")

    print("Generated data/weeks_index.json")
    print("Generated data/multi_week_analytics.json")
    print(f"Generated data/embedded_data.js ({round(os.path.getsize(os.path.join(DATA_DIR, 'embedded_data.js'))/1024, 1)} KB)")

if __name__ == "__main__":
    build_multi_week()
