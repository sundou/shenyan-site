#!/usr/bin/env python3
"""Get note_ids for the featured works by parsing the user_profile response"""
import json, subprocess, re

def get_session():
    result = subprocess.run([
        "curl", "-s", "-i", "http://localhost:18060/mcp",
        "-H", "Content-Type: application/json",
        "-d", '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}}}'
    ], capture_output=True, text=True, timeout=10)
    for line in result.stdout.split('\n'):
        if 'Mcp-Session-Id:' in line:
            return line.split(':', 1)[1].strip()
    return ""

def notify_init(session):
    subprocess.run([
        "curl", "-s", "--max-time", "25", "http://localhost:18060/mcp",
        "-H", "Content-Type: application/json",
        "-H", f"Mcp-Session-Id: {session}",
        "-d", '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}'
    ], capture_output=True, timeout=30)

def call_tool(session, name, args):
    payload = json.dumps({
        "method": "tools/call",
        "params": {"name": name, "arguments": args},
        "jsonrpc": "2.0", "id": 2
    })
    result = subprocess.run([
        "curl", "-s", "--max-time", "30", "http://localhost:18060/mcp",
        "-H", "Content-Type: application/json",
        "-H", f"Mcp-Session-Id: {session}",
        "-d", payload
    ], capture_output=True, text=True, timeout=35)
    return json.loads(result.stdout)

session = get_session()
notify_init(session)

resp = call_tool(session, "user_profile", {
    "user_id": "5b19e59be8ac2b261e2f167a",
    "xsec_token": "ABcvPCcg0-ECS9nouQBTQQ8BbPztw_3LAFHSL6guAqsQg="
})

content = resp.get("result", {}).get("content", [])
text = content[0].get("text", "") if content else ""
profile = json.loads(text)
feeds = profile.get("feeds", [])

print(f"Total feeds: {len(feeds)}")
for i, f in enumerate(feeds[:15]):
    nc = f.get("noteCard", {})
    nid = nc.get("noteId", f.get("id", ""))
    title = nc.get("displayTitle", "").strip()
    feed_id = f.get("id", "")
    print(f"[{i}] {title} | noteId={nid} | feedId={feed_id}")
