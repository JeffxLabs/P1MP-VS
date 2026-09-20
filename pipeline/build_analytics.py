#!/usr/bin/env python3
"""
Generate consolidated P1MP member analytics and duel summary.
"""
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

DAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat']
DAY_NAMES = {
    'mon': 'Monday (Radar & Exploration)',
    'tue': 'Tuesday (Base Expansion & Construction)',
    'wed': 'Wednesday (Scientific Research)',
    'thu': 'Thursday (Hero Development & Recruitment)',
    'fri': 'Friday (Total Troop Training)',
    'sat': 'Saturday (Enemy Assault & Elimination)'
}

def main():
    data = {}
    for d in DAYS + ['week']:
        with open(os.path.join(DATA_DIR, f"{d}.json")) as f:
            data[d] = json.load(f)

    # 1. Duel summary
    duel = {
        'home_alliance': {'tag': 'P1MP', 'name': 'JU1CE', 'server': '117'},
        'opponent_alliance': {'tag': '0BS', 'name': 'ZeroBullsht', 'server': 'Unknown'},
        'weekly_result': {
            'winner': 'P1MP',
            'p1mp_total_points': sum(r['points'] for r in data['week'] if r.get('alliance_tag') == 'P1MP'),
            'obs_total_points': sum(r['points'] for r in data['week'] if r.get('alliance_tag') == '0BS'),
            'p1mp_stages_won': 5,
            'obs_stages_won': 1,
            'total_margin': 0
        },
        'daily_stages': []
    }
    duel['weekly_result']['total_margin'] = duel['weekly_result']['p1mp_total_points'] - duel['weekly_result']['obs_total_points']

    for d in DAYS:
        p1mp_pts = sum(r['points'] for r in data[d] if r.get('alliance_tag') == 'P1MP')
        obs_pts = sum(r['points'] for r in data[d] if r.get('alliance_tag') == '0BS')
        p1mp_plyrs = sum(1 for r in data[d] if r.get('alliance_tag') == 'P1MP')
        obs_plyrs = sum(1 for r in data[d] if r.get('alliance_tag') == '0BS')
        winner = 'P1MP' if p1mp_pts > obs_pts else '0BS'
        diff = abs(p1mp_pts - obs_pts)

        duel['daily_stages'].append({
            'day': d,
            'title': DAY_NAMES[d],
            'p1mp_points': p1mp_pts,
            'obs_points': obs_pts,
            'p1mp_players': p1mp_plyrs,
            'obs_players': obs_plyrs,
            'winner': winner,
            'margin': diff,
            'p1mp_point_share_pct': round((p1mp_pts / (p1mp_pts + obs_pts)) * 100, 2)
        })

    with open(os.path.join(DATA_DIR, "duel_summary.json"), "w", encoding="utf-8") as f:
        json.dump(duel, f, indent=2, ensure_ascii=False)
    print("Generated data/duel_summary.json")

    # 2. P1MP member roster & analytics
    p1mp_week = [r for r in data['week'] if r.get('alliance_tag') == 'P1MP']
    p1mp_week = sorted(p1mp_week, key=lambda x: x['points'], reverse=True)
    p1mp_total_points = duel['weekly_result']['p1mp_total_points']

    members = []
    for ally_rank, r in enumerate(p1mp_week, 1):
        player = r['player']
        wk_pts = r['points']
        
        daily_breakdown = {}
        active_days = 0
        highest_day = None
        highest_day_pts = -1

        for d in DAYS:
            match = next((item for item in data[d] if item.get('player') == player and item.get('alliance_tag') == 'P1MP'), None)
            if match:
                pts = match['points']
                ovr_rank = match['rank']
                # find alliance rank on that day
                day_p1mp = [x for x in data[d] if x.get('alliance_tag') == 'P1MP']
                day_p1mp_rank = next((idx for idx, x in enumerate(day_p1mp, 1) if x.get('player') == player), None)
                daily_breakdown[d] = {
                    'points': pts,
                    'overall_rank': ovr_rank,
                    'alliance_rank': day_p1mp_rank
                }
                if pts > 0:
                    active_days += 1
                if pts > highest_day_pts:
                    highest_day_pts = pts
                    highest_day = d
            else:
                daily_breakdown[d] = {
                    'points': 0,
                    'overall_rank': None,
                    'alliance_rank': None
                }

        # Assign tier
        if ally_rank <= 10:
            tier = "Whale / Top 10"
        elif ally_rank <= 30:
            tier = "High Performer"
        elif ally_rank <= 60:
            tier = "Core Contributor"
        else:
            tier = "Active Member"

        pct = round((wk_pts / p1mp_total_points) * 100, 2)

        members.append({
            'alliance_rank': ally_rank,
            'overall_rank': r['rank'],
            'player': player,
            'alliance': r['alliance'],
            'weekly_points': wk_pts,
            'share_pct': pct,
            'tier': tier,
            'active_days': active_days,
            'best_day': highest_day,
            'best_day_points': highest_day_pts,
            'daily_breakdown': daily_breakdown
        })

    with open(os.path.join(DATA_DIR, "p1mp_members.json"), "w", encoding="utf-8") as f:
        json.dump(members, f, indent=2, ensure_ascii=False)
    print(f"Generated data/p1mp_members.json ({len(members)} members)")

if __name__ == "__main__":
    main()
