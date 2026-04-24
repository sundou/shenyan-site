#!/usr/bin/env python3
import json, urllib.request, urllib.parse, re

def run():
    # Init session
    init = json.dumps({
        "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "openclaw", "version": "1.0"}},
        "jsonrpc": "2.0", "id": 0
    }).encode()

    req = urllib.request.Request("http://localhost:18060/mcp", data=init, headers={"Content-Type": "application/json"})
    resp = json.loads(urllib.request.urlopen(req, timeout=10).read().decode())

    # Extract session ID from Set-Cookie
    session_id = ""
    if hasattr(resp, 'headers'):
        session_id = resp.headers.get('Set-Cookie', '')
    elif isinstance(resp, dict):
        for k, v in resp.items():
            if 'session' in str(k).lower() or 'session' in str(v).lower():
                session_id = str(v)

    # Try user_profile
    payload = json.dumps({
        "method": "tools/call",
        "params": {
            "name": "user_profile",
            "arguments": {
                "user_id": "5b19e59be8ac2b261e2f167a",
                "xsec_token": "ABcvPCcg0-ECS9nouQBTQQ8BbPztw_3LAFHSL6guAqsQg="
            }
        },
        "jsonrpc": "2.0", "id": 1
    }).encode()

    # Find session ID from init response headers
    # Re-do with Cookie header from MCP session
    headers = {"Content-Type": "application/json"}

    # Try the same curl approach
    import subprocess
    result = subprocess.run([
        "bash", "-c",
        '''
        SESSION=$(curl -s -i http://localhost:18060/mcp \\
          -H "Content-Type: application/json" \\
          -d \'{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}}}\' 2>/dev/null | grep -i "Mcp-Session-Id:" | cut -d" " -f2 | tr -d "\\r\\n")

        curl -s --max-time 25 http://localhost:18060/mcp \\
          -H "Content-Type: application/json" \\
          -H "Mcp-Session-Id: $SESSION" \\
          -d \'{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}\' > /dev/null

        curl -s --max-time 30 http://localhost:18060/mcp \\
          -H "Content-Type: application/json" \\
          -H "Mcp-Session-Id: $SESSION" \\
          -d \'{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"user_profile","arguments":{"user_id":"5b19e59be8ac2b261e2f167a","xsec_token":"ABcvPCcg0-ECS9nouQBTQQ8BbPztw_3LAFHSL6guAqsQg="}}}\'
        '''
    ], capture_output=True, text=True, timeout=40)

    data = json.loads(result.stdout)
    content = data.get("result", {}).get("content", [])
    text = content[0].get("text", "") if content else ""

    # Parse the text as JSON
    profile = json.loads(text)
    notes = profile.get("notes", [])

    print(f"Total notes: {len(notes)}")
    print()
    for i, n in enumerate(notes):
        nc = n.get("note_card", {})
        nid = nc.get("note_id", n.get("id", ""))
        title = nc.get("display_title", n.get("title", ""))
        print(f"[{i}] {title} | {nid}")

if __name__ == "__main__":
    run()
