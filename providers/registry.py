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
