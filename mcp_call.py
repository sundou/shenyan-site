#!/usr/bin/env python3
"""小红书 MCP 调用封装"""
import subprocess
import json

SESSION = None

def init_session():
    global SESSION
    MCP_URL = "http://localhost:18060/mcp"
    result = subprocess.run(
        ["curl", "--noproxy", "*", "-s", "-i", "-X", "POST", MCP_URL,
         "-H", "Content-Type: application/json",
         "-d", '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}}}'],
        capture_output=True, text=True, timeout=15
    )
    headers_text = result.stdout
    for line in headers_text.split("\n"):
        if line.lower().startswith("mcp-session-id:"):
            SESSION = line.split(":", 1)[1].strip()
            break
    if not SESSION:
        print("Error: no session ID")
        return False
    subprocess.run(
        ["curl", "--noproxy", "*", "-s", "-X", "POST", MCP_URL,
         "-H", "Content-Type: application/json",
         "-H", f"Mcp-Session-Id: {SESSION}",
         "-d", '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}'],
        capture_output=True, timeout=15
    )
    return True

def call(tool_name, arguments):
    if not SESSION and not init_session():
        return {}
    MCP_URL = "http://localhost:18060/mcp"
    payload = {
        "jsonrpc": "2.0", "id": 2, "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments}
    }
    result = subprocess.run(
        ["curl", "--noproxy", "*", "-s", "--max-time", "120", "-X", "POST", MCP_URL,
         "-H", "Content-Type: application/json",
         "-H", f"Mcp-Session-Id: {SESSION}",
         "-d", json.dumps(payload)],
        capture_output=True, text=True, timeout=130
    )
    try:
        return json.loads(result.stdout)
    except:
        print("Raw:", result.stdout[:1000])
        return {}

if __name__ == "__main__":
    import sys
    tool = sys.argv[1] if len(sys.argv) > 1 else "check_login_status"
    args = {}
    if len(sys.argv) > 2:
        args = json.loads(sys.argv[2])
    result = call(tool, args)
    if "result" in result and "content" in result["result"]:
        for item in result["result"]["content"]:
            print(item.get("text", ""))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
