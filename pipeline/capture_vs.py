#!/usr/bin/env python3
"""
VS Alliance Competition Automated Capture & Ingestion Engine.
Captures MON, TUE, WED, THU, FRI, SAT, and This Week rankings.
"""
import os
import sys
import time
import json
import re
import shutil
import subprocess
import threading
from cleaner import clean_record

PIPELINE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PIPELINE_DIR)
SCRATCH_DIR = os.path.join(PIPELINE_DIR, "scratch")
OCR_BIN = os.path.join(PIPELINE_DIR, "vision_ocr")

def parse_items_to_rows(items, max_known_rank=0):
    valid_items = []
    for it in items:
        x, y, w, h = it['x'], it['y'], it['width'], it['height']
        text = it['text'].strip()
        # Filter out header, footer, and pinned row (pinned row is below y=0.22)
        if y < 0.22 or y > 0.83:
            continue
        # Filter out announcement banners
        if any(keyword in text for keyword in ['Total Power', 'Warzone', 'reaches', 'Alliance Members', 'Eliminate']):
            continue
        if w > 0.45 and x < 0.30:
            continue
        valid_items.append(it)

    rank_boxes = []
    points_boxes = []
    middle_boxes = []

    for it in valid_items:
        x, y, w, h = it['x'], it['y'], it['width'], it['height']
        text = it['text'].strip()
        clean_digits = re.sub(r'[^\d]', '', text)

        if x < 0.20 and clean_digits:
            val = int(clean_digits)
            # Accept valid ranks up to max_known + 20
            if 1 <= val <= max(max_known_rank + 20, 205):
                rank_boxes.append({'rank': val, 'y': y, 'h': h, 'x': x, 'raw': text})
        elif x > 0.70 and clean_digits:
            points_boxes.append({'points': int(clean_digits), 'y': y, 'h': h, 'raw': text})
        elif 0.30 <= x <= 0.74:
            middle_boxes.append({'text': text, 'y': y, 'h': h, 'x': x})

    # Sort and dedup rank boxes
    rank_boxes = sorted(rank_boxes, key=lambda r: r['rank'])
    dedup_ranks = {}
    for r in rank_boxes:
        if r['rank'] not in dedup_ranks:
            dedup_ranks[r['rank']] = r
    rank_boxes = list(dedup_ranks.values())

    rows = []
    for r in rank_boxes:
        ry = r['y']
        best_pt = None
        min_p_dist = 0.05
        for p in points_boxes:
            dist = abs(p['y'] - ry)
            if dist < min_p_dist:
                min_p_dist = dist
                best_pt = p['points']

        # Middle texts within row y tolerance
        mids = [m for m in middle_boxes if abs(m['y'] - ry) <= 0.045]
        mids = sorted(mids, key=lambda m: m['y'], reverse=True)

        player = ''
        alliance = ''
        if len(mids) == 1:
            txt = mids[0]['text']
            if 'P1MP' in txt or '0BS' in txt or 'Zero' in txt or txt.startswith('['):
                alliance = txt
            else:
                player = txt
        elif len(mids) >= 2:
            player = mids[0]['text']
            alliance = ' '.join(m['text'] for m in mids[1:])

        # Confidence score based on vertical alignment and field completeness
        score = 100 - abs(ry - 0.5) * 40
        if best_pt is not None:
            score += 30
        if player:
            score += 20
        if alliance:
            score += 15

        rows.append({
            'rank': r['rank'],
            'player': player,
            'alliance': alliance,
            'points': best_pt,
            'y': ry,
            'score': score
        })
    return rows

def screencap(adb, device, dest_path):
    with open(dest_path, "wb") as f:
        subprocess.run([adb, "-s", device, "exec-out", "screencap", "-p"], stdout=f)

def swipe_async(adb, device):
    subprocess.run([adb, "-s", device, "shell", "input", "swipe", "540", "1350", "540", "750", "450"])

def rewind_to_top(adb, device):
    print("Rewinding list to top (Rank 1)...")
    for _ in range(12):
        subprocess.run([adb, "-s", device, "shell", "input", "swipe", "540", "500", "540", "1750", "120"])
        time.sleep(0.08)
    time.sleep(0.8)

def capture_active_list(adb, device, label="List", max_frames=70):
    os.makedirs(SCRATCH_DIR, exist_ok=True)
    print(f"\n--- Capturing {label} ---")
    t0 = time.time()
    data_dict = {}
    last_frame_ranks = ()
    stuck_count = 0

    for frame in range(max_frames):
        img_path = os.path.join(SCRATCH_DIR, f"frame_{frame % 2}.png")
        screencap(adb, device, img_path)

        # Launch swipe concurrently with OCR
        swipe_th = threading.Thread(target=swipe_async, args=(adb, device))
        swipe_th.start()

        # Run OCR
        out = subprocess.check_output([OCR_BIN, img_path])
        items = json.loads(out)

        cur_max = max(data_dict.keys()) if data_dict else 10
        rows = parse_items_to_rows(items, cur_max)
        frame_ranks = tuple(sorted(r['rank'] for r in rows))

        for row in rows:
            rk = row['rank']
            if rk not in data_dict:
                data_dict[rk] = row
            else:
                curr = data_dict[rk]
                if row['score'] > curr.get('score', 0):
                    if row['points'] is None and curr['points'] is not None:
                        row['points'] = curr['points']
                    if not row['player'] and curr['player']:
                        row['player'] = curr['player']
                    if not row['alliance'] and curr['alliance']:
                        row['alliance'] = curr['alliance']
                    data_dict[rk] = row
                else:
                    if curr['points'] is None and row['points'] is not None:
                        curr['points'] = row['points']
                    if not curr['player'] and row['player']:
                        curr['player'] = row['player']
                    if not curr['alliance'] and row['alliance']:
                        curr['alliance'] = row['alliance']

        swipe_th.join()
        time.sleep(0.1)

        cur_max = max(data_dict.keys()) if data_dict else 0
        sys.stdout.write(f"\r[{label} Frame {frame:2d}] Max Rank: {cur_max:3d} | Total unique: {len(data_dict):3d} | Rate: {(time.time()-t0)/(frame+1):.2f}s/f")
        sys.stdout.flush()

        # Detect bottom termination
        if frame_ranks == last_frame_ranks and len(frame_ranks) > 0 and cur_max > 120:
            stuck_count += 1
            if stuck_count >= 4:
                print(f"\nReached bottom of {label} at Rank {cur_max}!")
                break
        else:
            stuck_count = 0
            last_frame_ranks = frame_ranks

    sorted_ranks = sorted(data_dict.keys())
    cleaned_records = [clean_record(data_dict[r]) for r in sorted_ranks]
    print(f"\nFinished {label}: {len(cleaned_records)} records in {time.time()-t0:.1f}s.")
    return cleaned_records

if __name__ == '__main__':
    device = "127.0.0.1:5555"
    adb = shutil.which("adb") or "/opt/homebrew/bin/adb"
    # Test SAT capture
    rewind_to_top(adb, device)
    records = capture_active_list(adb, device, "SAT")
    with open(os.path.join(BASE_DIR, "data", "sat.json"), "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    print("Saved data/sat.json")
