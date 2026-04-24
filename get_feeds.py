#!/usr/bin/env python3
"""获取沈燕主页全部笔记的封面图 URL"""
import subprocess
import json

def call_mcp(tool, args):
    result = subprocess.run(
        ["/Users/sunxubo/.workbuddy/binaries/python/versions/3.13.12/bin/python3",
         "/Users/sunxubo/Desktop/vibe-project/shenyan-site/mcp_call.py",
         tool, json.dumps(args)],
        capture_output=True, text=True, timeout=60
    )
    try:
        return json.loads(result.stdout)
    except:
        print("Error:", result.stdout[:500])
        return {}

# Get user profile to list all posts
result = call_mcp("user_profile", {
    "user_id": "5b19e59be8ac2b261e2f167a",
    "xsec_token": "ABcvPCcg0-ECS9nouQBTQQ8BbPztw_3LAFHSL6guAqsQg="
})

feeds = result.get("userBasicInfo", {})

if "feeds" in result:
    feeds = result["feeds"]
    print(f"共获取 {len(feeds)} 篇笔记\n")

    # 找出匹配的案例帖子
    keywords = {
        "茶室": ["茶室", "共享"],
        "叠墅": ["叠墅", "中梁"],
        "90㎡": ["90㎡", "万科", "朗拾"],
        "老别墅": ["老别墅", "别墅改造"],
        "厨房": ["厨房"],
        "工艺": ["工艺细节", "极简风"],
    }

    for kw_name, kw_list in keywords.items():
        print(f"\n=== {kw_name} 相关帖子 ===")
        for feed in feeds:
            title = feed.get("noteCard", {}).get("displayTitle", "")
            if any(k in title for k in kw_list):
                cover = feed["noteCard"]["cover"]
                url = cover.get("urlDefault") or cover.get("urlPre", "")
                liked = feed["noteCard"]["interactInfo"].get("likedCount", "0")
                collected = feed["noteCard"]["interactInfo"].get("collectedCount", "")
                print(f"  标题: {title.strip()}")
                print(f"  赞: {liked}  收藏: {collected}")
                print(f"  封面图: {url}")
                print(f"  feed_id: {feed['id']}")
                print(f"  xsecToken: {feed['xsecToken']}")
                print()
else:
    print("No feeds found. Keys:", list(result.keys()))
