"""
Bot Discord coded by Jere_ID
Code Configured for Python 3.10.6
Credit for : Hikari, Lightbulb and others
"""
import re
import time
import datetime
import logging
from utils import get_secret
import hikari
import lightbulb
from brainfuckery import Brainfuckery

cfg = get_secret()

COOLDOWN_RATE = 8.0  # in seconds
last_executed = time.time()
last_executed_shit = time.time();


def assert_cooldown():
    global last_executed
    if last_executed + COOLDOWN_RATE < time.time():
        last_executed = time.time()
        return True
    return False

def shit_assert_cooldown():
    global last_executed_shit
    if last_executed_shit + COOLDOWN_RATE < time.time():
        last_executed_shit = time.time()
        return True
    return False

# Silit to sulit and sulit to silit
# ============
rep = {"sulit": "silit", "silit": "sulit"}
# pattern = re.compile(r"(?i)\bsulit|silit\b", flags=re.IGNORECASE)
pattern = re.compile(r"(?i)sulit|silit", flags=re.IGNORECASE)

# ============

bot = lightbulb.BotApp(prefix=cfg.PREFIX, token=cfg.BOT_TOKEN, intents=hikari.Intents.ALL_UNPRIVILEGED, logs="DEBUG")


@bot.listen(hikari.ShardReadyEvent)
async def ready_listener(_):
    print("The bot is ready!")


@bot.command
@lightbulb.command("ping", "checks that the bot is alive")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    msg = await ctx.respond("🎾Checking Latency...")
    msg_ctx = await msg.message()
    await msg.edit(
        f"📶Raw Latency: "
        f"`{(datetime.datetime.now() - msg_ctx.timestamp.replace(tzinfo=None)).total_seconds() / 1000:.2f}` ms\n"
        f"🫀HeartBeat Latency: "
        f"`{bot.heartbeat_latency * 1000:.2f}` ms"
    )

@bot.command()
@lightbulb.option("count", "The amount of messages to purge.", type=int, max_value=100, min_value=1)
@lightbulb.command("purge", "Purge a certain amount of messages from a channel.", pass_options=True)
#@lightbulb.implements(lightbulb.PrefixCommand)
@lightbulb.implements(lightbulb.SlashCommand)
async def purge(ctx: lightbulb.SlashContext, count: int) -> None:
    """Purge a certain amount of messages from a channel."""
    if not ctx.guild_id:
        await ctx.respond("This command can only be used in a server.")
        return

    messages = (
        await ctx.app.rest.fetch_messages(ctx.channel_id)
        .take_until(lambda m: datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=14) > m.created_at)
        .limit(count)
    )
    if messages:
        await ctx.app.rest.delete_messages(ctx.channel_id, messages)
        await ctx.respond(f"Purged {len(messages)} messages.")
    else:
        await ctx.respond("Could not find any messages younger than 14 days!")
    

@bot.listen()
async def on_message(event: hikari.MessageCreateEvent) -> None:
    """Listen for messages being created."""
    if not event.is_human:
        return
    # if re.search(r"(?i)\bmerita\b", event.content.lower()):
    #    return
    
    # print("Sender: " + event.author.username);
    
    if event.content:
        if event.author.username == "Jere_ID" or event.author.id == 445556306535776266:
            if not shit_assert_cooldown():  # add cooldown 8s
                return
            await event.message.add_reaction(emoji="💩")
        if 'elek' in event.content.lower():
            await event.message.add_reaction(emoji="👍")
        if event.content.lower().startswith("bf"):
            msg = event.content.lower().split()
            if len(msg) <= 1:
                await event.message.respond(content=f"Usage bf compile/interpret <code>")
                return
            if msg[1] == "compile":
                res = Brainfuckery().convert(' '.join(msg[2:]))
                await event.message.respond(content=f"```brainfuck\n{res}```")
            elif msg[1] == "interpret":
                res = Brainfuckery().interpret(' '.join(msg[2:]))
                await event.message.respond(content=f"```{res}```")
            else:
                await event.message.respond(content=f"Usage bf compile/interpret <code>")

        elif "sulit" in event.content.lower() or "silit" in event.content.lower():
            if not assert_cooldown():  # add cooldown 8s
                await event.message.respond(content=f"You're being rate limited please wait a few seconds", reply=True)
                return
            # msg = re.sub(r"(?i)\bsulit\b", "silit", event.content, flags=re.IGNORECASE)
            msg = pattern.sub(lambda m: rep[re.escape(m.group(0)).lower()], event.content)
            await event.message.respond(content=f"{msg.capitalize()}", reply=True)


bot.run()
