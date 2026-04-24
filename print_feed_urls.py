#!/usr/bin/env python3
import json, sys, subprocess, re

PYBIN = "/Users/sunxubo/.workbuddy/binaries/python/versions/3.13.12/bin/python3"

# Read cached feeds
with open("/Users/sunxubo/Desktop/vibe-project/shenyan-site/all_feeds.json", "r") as f:
    data = json.load(f)

feeds = data["feeds"]

# Map: index in feeds list -> name
targets = {
    1: "厨房指南",
    2: "共享茶室",
    10: "叠墅",
}

for idx, name in targets.items():
    if idx < len(feeds):
        f = feeds[idx]
        nc = f.get("note_card", {})
        print(f"[{name}] feed_index={idx}")
        print(f"  feed_id: {f['id']}")
        print(f"  interact_info: {f.get('interact_info', {})}")
        print(f"  user: {f.get('user', {})}")
        # Try to get the note URL from various fields
        for key in ["id", "note_id", "url", "share_link", "share_url"]:
            if key in f:
                print(f"  {key}: {f[key]}")
        for key in ["note_card"]:
            nc = f.get(key, {})
            if isinstance(nc, dict):
                for k, v in nc.items():
                    if 'url' in k.lower() or 'id' in k.lower() or 'link' in k.lower():
                        print(f"  {key}.{k}: {v}")
        print()
