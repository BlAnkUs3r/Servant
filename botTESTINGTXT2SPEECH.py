import discord
import json
import random
from discord.ext import tasks, commands
from tts import text_to_speech  # Import the TTS function
from bible_verses import bible_verses

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Ensure to enable message content intents
intents.voice_states = True  # To handle voice state updates
bot = commands.Bot(command_prefix='!', intents=intents)

# Load configuration
with open('config.json') as config_file:
    config = json.load(config_file)
    TOKEN = config["DISCORD_TOKEN"]
    MASTER_USER_ID = int(config["MASTER_USER_ID"])  # Ensure ID is an integer
    REMINDER_CHANNEL_ID = int(config["REMINDER_CHANNEL_ID"])  # Add reminder channel ID
    KING_USER_ID = int(config["KING_USER_ID"])  # Ensure ID is an integer

# Define harmful actions
harmful_actions = ["owoslap", "owopunch", "owokill", "mean", "bad", "idiot", "stupid", "fuck you"]

# Define the role name that can use the TTS command
ROLE_NAME = "mic"

# Task for periodic Bible verses
@tasks.loop(hours=random.uniform(0.5, 1))
async def send_bible_verse():
    channel = bot.get_channel(REMINDER_CHANNEL_ID)
    if channel:
        verse = random.choice(bible_verses)
        await channel.send(verse)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    send_bible_verse.start()  # Start the Bible verse task

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Check for harmful actions
    master_mention = f"<@{MASTER_USER_ID}>"
    for action in harmful_actions:
        if action in message.content.lower() and master_mention in message.content:
            response = f"{action} <@{message.author.id}>"
            await message.channel.send(response)
            warn_message = f"?warn <@{message.author.id}> STUUUUUUUUUUUUUPID"
            await message.channel.send(warn_message)
            break

    if message.author.id == KING_USER_ID:
        if random.random() < 0.15:
            await message.channel.send("Yes, my glorious king")

    if "why" in message.content.lower() or "what is that" in message.content.lower():
        await message.channel.send("The less you know, the better.")

    # Check if the user is in a voice channel and the bot is not in the same channel
    if message.author.voice:
        voice_channel = message.author.voice.channel
        if not bot.voice_clients or bot.voice_clients[0].channel != voice_channel:
            await voice_channel.connect()

        # Speak out the message in the voice channel
        if bot.voice_clients:
            vc = bot.voice_clients[0]
            text_to_speech(message.content, "tts.mp3")
            vc.play(discord.FFmpegPCMAudio("tts.mp3"), after=lambda e: print(f"Finished playing: {e}"))

    # Process commands if there are any
    await bot.process_commands(message)

@bot.command(name='leave')
async def leave_command(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from the voice channel.")
    else:
        await ctx.send("I am not connected to a voice channel.")

bot.run(TOKEN)
