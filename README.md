# Discord Hosting Bot

A Discord bot focused on hosting and infrastructure support questions (servers, VPS, cloud, networking, deployment, and related topics).  
The bot uses local Ollama responses and includes a stress/lives system for off-topic handling.

## Features

- Discord bot built with `discord.py`
- Local LLM responses via Ollama (`llama3` by default)
- Topic guardrails for infrastructure-focused conversations
- Per-user stress/life tracking with recovery logic
- DM-only private chat flow per user
- Persistent per-user chat history/state in `data/user_sessions.json`

## Project Structure

```text
HostSense/
  main.py
  config.py
  ollama_client.py
  prompt_builder.py
  stress_manager.py
  requirements.txt
```

## Requirements

- Python 3.10+
- A Discord bot token
- Ollama running locally

## Setup

1. Open the project:
   ```powershell
   cd HostSense
   ```
2. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Configure settings in `config.py`:
   - Set `DISCORD_TOKEN`
   - Confirm `OLLAMA_URL` (default: `http://localhost:11434/api/generate`)
   - Set `OLLAMA_MODEL` (default: `llama3`)

## Run

From `HostSense/`:

```powershell
python main.py
```

## Private Chat Behavior

- In server channels, the bot is fully silent.
- Real conversation happens only in DM, so each user has separate data and history.
- Per-user state survives restarts using `data/user_sessions.json`.
- Commands in DM:
  - `!reset` or `/reset`: reset stress/lives only
  - `!clear` or `/clear`: clear chat history and reset stress/lives

## Update On Your Server

From your server checkout directory:

```powershell
cd HostSense
git pull
```

If dependencies changed (safe to run anytime):

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Restart the bot process (use the method you normally run it with, for example):

```powershell
python main.py
```

If you run with PM2/systemd/Docker, restart that service/container instead.

## Notes

- The bot sends a one-time transparency notice per user.
- Off-topic messages consume lives; valid infrastructure questions help recovery/reset.
- If you accidentally exposed your Discord token, rotate it immediately in the Discord Developer Portal.
