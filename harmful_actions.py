# harmful_actions.py

harmful_actions = ["owoslap", "owopunch", "owokill", "mean", "bad", "idiot", "stupid", "fuck you"]

async def handle_harmful_actions(message, bot, master_mention):
    for action in harmful_actions:
        if action in message.content.lower() and master_mention in message.content:
            response = f"{action} <@{message.author.id}>"
            await message.channel.send(response)
            warn_message = f"?warn <@{message.author.id}> STUUUUUUUUUUUUUPID"
            await message.channel.send(warn_message)
            break
