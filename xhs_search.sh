#!/bin/bash
set -e
SESSION=$(curl --noproxy '*' -s -i -X POST http://localhost:18060/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}}}' \
  | grep -i "Mcp-Session-Id:" | cut -d' ' -f2 | tr -d '\r\n')

curl --noproxy '*' -s -X POST http://localhost:18060/mcp \
  -H "Content-Type: application/json" -H "Mcp-Session-Id: $SESSION" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' > /dev/null

curl --noproxy '*' -s --max-time 60 -X POST http://localhost:18060/mcp \
  -H "Content-Type: application/json" -H "Mcp-Session-Id: $SESSION" \
  -d "{\"jsonrpc\":\"2.0\",\"id\":2,\"method\":\"tools/call\",\"params\":{\"name\":\"$1\",\"arguments\":$2}}"
