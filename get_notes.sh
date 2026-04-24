#!/bin/bash
cd /Users/sunxubo/Desktop/vibe-project/shenyan-site

SESSION=$(curl -s -i http://localhost:18060/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}}}' 2>/dev/null | grep -i "Mcp-Session-Id:" | cut -d" " -f2 | tr -d '\r\n')

curl -s --max-time 25 http://localhost:18060/mcp \
  -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: $SESSION" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' > /dev/null

curl -s --max-time 30 http://localhost:18060/mcp \
  -H "Content-Type: application/json" \
  -H "Mcp-Session-Id: $SESSION" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"user_profile","arguments":{"user_id":"5b19e59be8ac2b261e2f167a","xsec_token":"ABcvPCcg0-ECS9nouQBTQQ8BbPztw_3LAFHSL6guAqsQg="}}}' | python3 -c "
import json, sys
data = json.load(sys.stdin)
content = data.get('result', {}).get('content', [])
text = content[0].get('text', '') if content else ''
profile = json.loads(text)
notes = profile.get('notes', [])
print(f'Total: {len(notes)} notes')
for i, n in enumerate(notes):
    nc = n.get('note_card', {})
    nid = nc.get('note_id', n.get('id', ''))
    title = nc.get('display_title', n.get('title', ''))
    print(f'[{i}] {title} | {nid}')
"
