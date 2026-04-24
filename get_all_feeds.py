#!/usr/bin/env python3
"""获取沈燕全部笔记封面图，一并保存"""
import subprocess, json, os

def mcp_raw(tool, args):
    result = subprocess.run(
        ["/Users/sunxubo/.workbuddy/binaries/python/versions/3.13.12/bin/python3",
         "/Users/sunxubo/Desktop/vibe-project/shenyan-site/mcp_call.py",
         tool, json.dumps(args)],
        capture_output=True, text=True, timeout=60
    )
    try:
        return json.loads(result.stdout)
    except:
        return {}

# Get all feeds
result = mcp_raw("user_profile", {
    "user_id": "5b19e59be8ac2b261e2f167a",
    "xsec_token": "ABcvPCcg0-ECS9nouQBTQQ8BbPztw_3LAFHSL6guAqsQg="
})

feeds = result.get("feeds", [])
print(f"共 {len(feeds)} 篇笔记\n")

# 打印前32篇的标题和封面图
for i, feed in enumerate(feeds):
    card = feed.get("noteCard", {})
    title = card.get("displayTitle", "").strip()
    interact = card.get("interactInfo", {})
    cover = card.get("cover", {})
    url = cover.get("urlDefault") or cover.get("urlPre", "")
    liked = interact.get("likedCount", "0")
    collected = interact.get("collectedCount", "")
    print(f"{i+1:2d}. [{liked}赞/{collected}藏] {title}")
    print(f"    封面: {url[:80]}...")
    print(f"    id: {feed['id']} | token: {feed['xsecToken'][:30]}...")
    print()
