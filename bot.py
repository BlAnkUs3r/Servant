import discord
import json
import random
from discord.ext import tasks, commands
from googlesearch import search
from bible_verses import bible_verses

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Ensure to enable message content intents
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

    # Convert master ID to mention format
    master_mention = f"<@{MASTER_USER_ID}>"

    # Check if the message contains any harmful action and mentions the master
    for action in harmful_actions:
        if action in message.content.lower() and master_mention in message.content:
            # Prepare the defense message
            response = f"{action} <@{message.author.id}>"
            await message.channel.send(response)
            # Send a warning
            warn_message = f"?warn <@{message.author.id}> STUUUUUUUUUUUUUPID"
            await message.channel.send(warn_message)
            break
    
    if message.author.id == KING_USER_ID:
        # 10% chance to respond with "Yes, my glorious king"
        if random.random() < 0.15:
            await message.channel.send("Yes, my glorious king")
	# Check for "why" or "what is that"
    content_lower = message.content.lower()
    if "why" in content_lower or "what is that" in content_lower:
        await message.channel.send("The less you know, the better.")

    # Process commands
    await bot.process_commands(message)

@bot.command(name='google')
async def google_command(ctx, *, query: str):
    try:
        # Perform the search and get the top 3 results
        search_results = list(search(query, num_results=3))
        if search_results:
            # Send the top 3 results, each on a new line
            await ctx.send('\n'.join(search_results))
        else:
            await ctx.send("No results found.")
    except Exception as e:
        await ctx.send(f"An error occurred while searching: {e}")
   
async def listen_for_terminal_input():
    """Listen for terminal input and send messages via the bot."""
    await bot.wait_until_ready()  # Ensure bot is logged in and ready
    while True:
        message = input("Enter your message: ")
        channel = bot.get_channel(REMINDER_CHANNEL_ID)
        if channel:
            await channel.send(message)
        else:
            print(f"Could not find a channel with ID {REMINDER_CHANNEL_ID}.")

bot.run(TOKEN)