#!/usr/bin/env python3
"""
Data Cleaner and Normalizer for S117-P1MP VS Alliance Competition Rankings.
"""
import re

def clean_alliance_tag_and_name(raw_ally):
    if not raw_ally:
        return "", ""
    s = raw_ally.strip()
    
    # Check for P1MP variations
    if re.search(r'P1MP|PIMP', s, re.IGNORECASE):
        return "P1MP", "JU1CE"
    # Check for 0BS / OBS variations
    if re.search(r'[0O]BS|ZeroBullsht|ZeroBull', s, re.IGNORECASE):
        return "0BS", "ZeroBullsht"
        
    # Generic regex: [TAG] Name
    m = re.match(r'^[\[\(]?([A-Za-z0-9]{2,6})[\]\)]\s*(.*)$', s)
    if m:
        return m.group(1).upper(), m.group(2).strip()
    return "", s

def clean_player_name(raw_name):
    if not raw_name:
        return ""
    name = raw_name.strip()
    # Strip leading/trailing brackets or junk
    name = re.sub(r'^[\[\(][^\]\)]*[\]\)]\s*', '', name)
    return name

def clean_record(rec):
    rank = rec['rank']
    cmd = clean_player_name(rec.get('player', ''))
    raw_ally = rec.get('alliance', '')
    pts = rec.get('points', 0)
    
    tag, ally_name = clean_alliance_tag_and_name(raw_ally)
    if not tag:
        # If commander text had the alliance tag instead
        if 'P1MP' in cmd or 'JU1CE' in cmd:
            tag, ally_name = "P1MP", "JU1CE"
            cmd = ""
        elif '0BS' in cmd or 'OBS' in cmd or 'ZeroBullsht' in cmd:
            tag, ally_name = "0BS", "ZeroBullsht"
            cmd = ""

    full_ally = f"[{tag}] {ally_name}" if tag else ally_name
    
    return {
        'rank': rank,
        'player': cmd,
        'alliance': full_ally,
        'alliance_tag': tag,
        'alliance_name': ally_name,
        'points': pts
    }
