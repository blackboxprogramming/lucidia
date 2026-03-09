from pathlib import Path

# --- providers/registry.py ---
registry = r"""
import os
from typing import Dict, Any

# Feature flags via env; flip to "on" later by setting a token/value
ENABLED = {
    "slack":  bool(os.getenv("SLACK_BOT_TOKEN")),
    "asana":  bool(os.getenv("ASANA_ACCESS_TOKEN")),
    "linear": bool(os.getenv("LINEAR_API_KEY")),
    "notion": bool(os.getenv("NOTION_TOKEN")),
    "github": bool(os.getenv("GITHUB_TOKEN")),
    "jira":   all(os.getenv(k) for k in ["JIRA_URL","JIRA_EMAIL","JIRA_API_TOKEN"]),
}

def get_enabled():
    return {k: v for k, v in ENABLED.items() if v}

def call_tool(tool: str, args: Dict[str, Any]) -> Dict[str, Any]:
    # PURE PLACEHOLDERS for now; return ok if token is present
    if tool == "slack.say":
        if not ENABLED["slack"]: return {"error":"slack not configured"}
        return {"ok": True, "placeholder": "slack.say", "args": args}

    if tool == "asana.me":
        if not ENABLED["asana"]: return {"error":"asana not configured"}
        return {"ok": True, "placeholder": "asana.me"}

    if tool == "linear.me":
        if not ENABLED["linear"]: return {"error":"linear not configured"}
        return {"ok": True, "placeholder": "linear.me"}

    if tool == "notion.me":
        if not ENABLED["notion"]: return {"error":"notion not configured"}
        return {"ok": True, "placeholder": "notion.me"}

    if tool == "github.me":
        if not ENABLED["github"]: return {"error":"github not configured"}
        return {"ok": True, "placeholder": "github.me"}

    if tool == "jira.me":
        if not ENABLED["jira"]: return {"error":"jira not configured"}
        return {"ok": True, "placeholder": "jira.me"}

    return {"error": f"unknown tool: {tool}"}
""".lstrip()

# --- main.py ---
main = r"""
import os, sqlite3
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from providers import get_enabled, call_tool

# ---- tiny sqlite memory ----
DB_PATH = "/home/pi/lucidia/lucidia.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
conn.execute("CREATE TABLE IF NOT EXISTS memory (k TEXT PRIMARY KEY, v TEXT)")

app = FastAPI(title="Lucidia")

@app.get("/")
def root():
    return {"lucidia": "online"}

@app.get("/healthz")
def healthz():
    return {"ok": True}

# ---- memory endpoints ----
class MemoryPut(BaseModel):
    key: str
    value: str

@app.post("/memory/put")
def memory_put(payload: MemoryPut):
    conn.execute("REPLACE INTO memory(k,v) VALUES (?,?)", (payload.key, payload.value))
    conn.commit()
    return {"ok": True}

@app.get("/memory/get")
def memory_get(key: str):
    row = conn.execute("SELECT v FROM memory WHERE k=?", (key,)).fetchone()
    return {"key": key, "value": (row[0] if row else None)}

# ---- minimal service endpoints (placeholders; real calls later) ----
@app.post("/slack/say")
def slack_say(channel: str = "#general", text: str = "Lucidia says hi"):
    r = call_tool("slack.say", {"channel": channel, "text": text})
    if "error" in r: raise HTTPException(500, r["error"])
    return r

@app.get("/asana/me")
def asana_me():
    r = call_tool("asana.me", {})
    if "error" in r: raise HTTPException(500, r["error"])
    return r

@app.get("/linear/me")
def linear_me():
    r = call_tool("linear.me", {})
    if "error" in r: raise HTTPException(500, r["error"])
    return r

# ---- agent skeleton ----
class AgentMsg(BaseModel):
    message: Optional[str] = None
    tool: Optional[str] = None
    args: Optional[Dict[str, Any]] = None

@app.get("/agent/capabilities")
def agent_caps():
    return {"enabled": list(get_enabled().keys())}

@app.post("/agent/chat")
def agent_chat(payload: AgentMsg):
    # If a tool is provided, call it; message is optional.
    if payload.tool:
        r = call_tool(payload.tool, payload.args or {})
        if "error" in r: raise HTTPException(500, r["error"])
        return {"message": "tool_result", "result": r}
    return {
        "message": (payload.message or "").strip(),
        "you_can_call": list(get_enabled().keys()),
        "hint": "POST {'tool':'slack.say','args':{'channel':'#general','text':'hi'}}"
    }
""".lstrip()

# write files atomically
Path("providers").mkdir(exist_ok=True)
Path("providers/registry.py").write_text(registry)
Path("main.py").write_text(main)
print("wrote providers/registry.py and main.py")
