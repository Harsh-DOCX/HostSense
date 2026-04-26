import discord

from config import DISCORD_TOKEN, LIFE_LIMIT, RECOVERY_REQUIRED, USER_DATA_FILE
from ollama_client import query_ollama
from prompt_builder import build_prompt
from stress_manager import StressManager

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
stress_manager = StressManager(USER_DATA_FILE)


def invalid_response(stress: int, lives: int) -> str:
    messages = {
        1: "That is off-topic. Ask about servers, hosting, VPS, cloud, or infrastructure.",
        2: "Still off-topic. Keep it to infrastructure questions only.",
        3: "Last warning. Stay on hosting/infrastructure topics.",
    }
    base = messages.get(min(stress, 3), messages[3])
    return f"{base} Lives left: {lives}."

def exhausted_response(stress: int) -> str:
    lines = [
        "I am officially irritated now. Off-topic mode is not helping.",
        "Yeah, patience is thin now. Bring me infrastructure problems only.",
        "Still off-topic? Stress is climbing. Ask a real infra question.",
        "No-nonsense mode active. Ask servers/hosting/VPS questions only.",
    ]
    return lines[min(max(stress - 3, 0), len(lines) - 1)]


@client.event
async def on_ready() -> None:
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message: discord.Message) -> None:
    if message.author.bot:
        return

    user_id = str(message.author.id)
    in_dm = isinstance(message.channel, discord.DMChannel)
    bot_mentioned = client.user is not None and client.user in message.mentions

    if not in_dm and not bot_mentioned:
        # In guild channels, only respond when explicitly mentioned.
        return

    content = message.content
    if bot_mentioned and not in_dm and client.user is not None:
        for mention in (
            f"<@{client.user.id}>",
            f"<@!{client.user.id}>",
        ):
            content = content.replace(mention, "")
        content = content.strip()

    if not content:
        if not in_dm:
            await message.channel.send(
                f"Hi {message.author.mention}, mention me with a hosting/infrastructure question."
            )
        return

    user = stress_manager.get_user(user_id)

    normalized = content.strip().lower()
    if normalized in {"!reset", "/reset"}:
        stress_manager.reset_user(user_id, clear_history=False)
        await message.channel.send("Reset complete. Lives and stress are restored for your account.")
        return

    if normalized in {"!clear", "/clear"}:
        stress_manager.reset_user(user_id, clear_history=True)
        await message.channel.send("Your private chat history, lives, and stress have been cleared.")
        return

    if not user["notice_sent"]:
        stress_manager.set_flag(user_id, "notice_sent", True)
        await message.channel.send(
            "Transparency notice: This bot enforces topic limits and stress logic. "
            f"You get {LIFE_LIMIT} off-topic lives. "
            f"After lives are exhausted, ask {RECOVERY_REQUIRED} valid infrastructure questions to reset."
        )

    status = stress_manager.handle(user_id, content)
    user = stress_manager.get_user(user_id)

    if status == "neutral":
        await message.channel.send(
            "No life deducted for that. When you are ready, ask a servers/hosting/VPS question."
        )
        return

    if status == "invalid":
        await message.channel.send(invalid_response(user["stress"], user["lives"]))
        return

    if status == "life_exhausted":
        await message.channel.send(
            "I am irritated now. Lives are fully consumed. "
            f"Ask {RECOVERY_REQUIRED} valid infrastructure questions to reset."
        )
        return

    if status == "exhausted_invalid":
        remaining = max(RECOVERY_REQUIRED - user["recovery"], 0)
        await message.channel.send(
            f"{exhausted_response(user['stress'])} Recovery target: {remaining} valid question(s)."
        )
        return

    history = stress_manager.get_chat_history(user_id)
    prompt = build_prompt(content, user["stress"], history)
    reply = query_ollama(prompt)

    if not reply:
        reply = "I could not generate a response right now. Please try again."

    stress_manager.add_chat_message(user_id, "user", content)
    stress_manager.add_chat_message(user_id, "assistant", reply)

    await message.channel.send(reply)

    if status == "valid_recovery":
        remaining = max(RECOVERY_REQUIRED - user["recovery"], 0)
        await message.channel.send(
            f"Recovery in progress: {remaining} valid infrastructure question(s) remaining."
        )

    if status == "valid_reset":
        await message.channel.send("Reset complete. Lives restored and stress cleared.")


if __name__ == "__main__":
    if DISCORD_TOKEN == "YOUR_DISCORD_BOT_TOKEN":
        raise ValueError("Set DISCORD_TOKEN in config.py before running the bot.")

    client.run(DISCORD_TOKEN)
