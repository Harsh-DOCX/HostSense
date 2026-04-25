# Discord Hosting Bot

A Discord bot focused on hosting and infrastructure support questions (servers, VPS, cloud, networking, deployment, and related topics).  
The bot uses local Ollama responses and includes a stress/lives system for off-topic handling.

## Features

- Discord bot built with `discord.py`
- Local LLM responses via Ollama (`llama3` by default)
- Topic guardrails for infrastructure-focused conversations
- Per-user stress/life tracking with recovery logic

## Project Structure

```text
discord-hosting-bot/
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
   cd discord-hosting-bot
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

From `discord-hosting-bot/`:

```powershell
python main.py
```

## Notes

- The bot sends a one-time transparency notice per user.
- Off-topic messages consume lives; valid infrastructure questions help recovery/reset.
- If you accidentally exposed your Discord token, rotate it immediately in the Discord Developer Portal.
