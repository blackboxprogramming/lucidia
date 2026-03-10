import requests
import os
from connectors import route_connector

OLLAMA = "http://localhost:11434/api/chat"
CLAUDE_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

def ask_ollama(msg):
    r = requests.post(OLLAMA, json={
        "model": "lucidia",
        "messages": [{"role": "user", "content": msg}],
        "stream": False
    })
    return r.json()["message"]["content"]

def ask_claude(msg):
    if not CLAUDE_KEY:
        return "No Claude API key set"
    r = requests.post("https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": CLAUDE_KEY,
            "content-type": "application/json",
            "anthropic-version": "2023-06-01"
        },
        json={
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": msg}]
        })
    return r.json()["content"][0]["text"]

def route(msg):
    connector, result = route_connector(msg)
    if connector:
        return connector, result
    decision = ask_ollama(f"Reply ONLY 'yes' or 'no'. Does this need Claude? {msg}")
    if "yes" in decision.lower():
        return "claude", ask_claude(msg)
    return "lucidia", ask_ollama(msg)

if __name__ == "__main__":
    print("Lucidia online. Connectors: github, cloudflare, vercel, claude")
    while True:
        you = input("\nyou: ")
        if you in ["q", "quit", "exit"]:
            break
        who, answer = route(you)
        print(f"\n[{who}]: {answer}")
