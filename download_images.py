#!/usr/bin/env python3
"""下载沈燕帖子封面图到 public/images/"""
import subprocess, json, os, urllib.request

MCP_CALL = "/Users/sunxubo/Desktop/vibe-project/shenyan-site/mcp_call.py"
OUT_DIR = "/Users/sunxubo/Desktop/vibe-project/shenyan-site/public/images"
os.makedirs(OUT_DIR, exist_ok=True)

def call_mcp(tool, args):
    result = subprocess.run(
        ["/Users/sunxubo/.workbuddy/binaries/python/versions/3.13.12/bin/python3", MCP_CALL, tool, json.dumps(args)],
        capture_output=True, text=True, timeout=60
    )
    try:
        return json.loads(result.stdout)
    except:
        return {}

result = call_mcp("user_profile", {
    "user_id": "5b19e59be8ac2b261e2f167a",
    "xsec_token": "ABcvPCcg0-ECS9nouQBTQQ8BbPztw_3LAFHSL6guAqsQg="
})
feeds = result.get("feeds", [])

# Map: slug → (feed_id, filename)
slug_map = {
    "chashi":        (feeds[0]["id"],  "chashi.jpg"),
    "diushu":        (feeds[9]["id"],  "diushu.jpg"),
    "wanke":         (feeds[6]["id"],  "wanke.jpg"),
    "old-villa":     (feeds[14]["id"], "old-villa.jpg"),
    "kitchen":       (feeds[1]["id"],  "kitchen.jpg"),
    "craft":         (feeds[7]["id"],  "craft.jpg"),
}

feed_by_id = {f["id"]: f for f in feeds}
downloaded = []

for slug, (feed_id, filename) in slug_map.items():
    if feed_id not in feed_by_id:
        print(f"❌ {slug}: feed not found")
        continue
    feed = feed_by_id[feed_id]
    cover = feed.get("noteCard", {}).get("cover", {})
    url = cover.get("urlDefault") or cover.get("urlPre") or ""
    if not url:
        print(f"❌ {slug}: no cover URL")
        continue

    out_path = os.path.join(OUT_DIR, filename)
    print(f"⬇️  {slug}: downloading...")
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        })
        with urllib.request.urlopen(req, timeout=20) as r:
            data = r.read()
        with open(out_path, "wb") as f:
            f.write(data)
        downloaded.append(out_path)
        print(f"  ✅ {len(data)} bytes → {filename}")
    except Exception as e:
        print(f"  ❌ {e}")

print(f"\n✅ 下载完成：{len(downloaded)}/{len(slug_map)} 张")
for p in downloaded:
    print(f"   {os.path.basename(p)}")
