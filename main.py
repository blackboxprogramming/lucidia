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


from pydantic import BaseModel
import json, urllib.request

class CompleteReq(BaseModel):
    prompt: str
    max_tokens: int = 128

@app.post("/agent/complete")
def agent_complete(body: CompleteReq):
    req = {
        "prompt": body.prompt,
        "n_predict": body.max_tokens,
        "temperature": 0.7,
    }
    data = json.dumps(req).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(
            "http://127.0.0.1:8080/completion",
            data=data,
            headers={"Content-Type":"application/json"},
            method="POST",
        ), timeout=60) as r:
            out = json.loads(r.read().decode())
            return {"text": out.get("content", ""), "raw": out}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
