#!/usr/bin/env python3
"""Get user's notes with full detail for building Red Book links"""
import json, urllib.request, urllib.error

MCP_URL = "http://localhost:18060/mcp"

def mcp_call(method, params=None):
    payload = {
        "method": method,
        "params": params or {},
        "jsonrpc": "2.0",
        "id": 1
    }
    # Init session
    init_payload = {
        "method": "initialize",
        "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "openclaw", "version": "1.0"}},
        "jsonrpc": "2.0", "id": 0
    }
    req = urllib.request.Request(MCP_URL, data=json.dumps(init_payload).encode(), headers={"Content-Type": "application/json"})
    resp = json.loads(urllib.request.urlopen(req, timeout=10).read().decode())
    session_id = resp.get("headers", {}).get("Mcp-Session-Id", "") if isinstance(resp, dict) else ""

    # Try to extract session from Set-Cookie header approach
    req2 = urllib.request.Request(MCP_URL, data=json.dumps(payload).encode(), headers={
        "Content-Type": "application/json",
        "Cookie": f"mcp-session-id={session_id}" if session_id else ""
    })
    try:
        resp2 = urllib.request.urlopen(req2, timeout=20).read().decode()
        return json.loads(resp2)
    except Exception as e:
        return {"error": str(e)}

# Try the list_notes approach
result = mcp_call("search_feeds", {"keyword": "沈燕", "page_size": 30})
print(json.dumps(result, ensure_ascii=False, indent=2)[:5000])
