import discord
from datetime import datetime
from discord.ext import commands, tasks 
from discord import app_commands

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.voice_states = True
intents.messages = True
 
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

waiting_room_channel_id = {VC_CHANNEL_ID}  
status_update_channel_id = {TEXT_CHANNEL_ID}

member_entry_times = {}
status_message = None

@tasks.loop(seconds=30)
async def loop_update_status_message():
    await update_status_message()

async def update_status_message():
    global status_message

    channel = discord.utils.get(client.get_all_channels(), id=status_update_channel_id)
    
    if status_message is None:
        status_message = await channel.send("Updating...")
        return

    try:
        sorted_members = sorted(member_entry_times.items(), key=lambda x: x[1], reverse=True)
        
        specific_moderation = []
        general_moderation = []
        
        for member_id, entry_time in sorted_members:
            member = channel.guild.get_member(member_id)
            wait_time = int((datetime.now() - entry_time).total_seconds() // 60)
            line = f"<@{member_id}> has been waiting for {wait_time} minutes"
            if "@" in member.display_name:
                specific_moderation.append(line)
            else:
                general_moderation.append(line)

        specific_section = "\n".join(specific_moderation) if specific_moderation else "No one is waiting in line."
        general_section = "\n".join(general_moderation) if general_moderation else "No one is waiting in line."

        status_text = f"**## Waiting for specific Moderation**\n{specific_section}\n\n**## Waiting for any Moderation**\n{general_section}"
        
        await status_message.edit(content=status_text)
    except discord.NotFound:
        status_message = await channel.send("Updating...")
        await update_status_message()
    except discord.Forbidden:
        print("Bot lacks permission to edit message.")
    except Exception as e:
        print(f"An error occurred: {e}")


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    await tree.sync(guild=discord.Object(id=DISCORD_SERVER_ID))

    channel = discord.utils.get(client.get_all_channels(), id=status_update_channel_id)

    await channel.purge(limit=100)

    global status_message
    status_message = None

    await update_status_message()

    loop_update_status_message.start()

@client.event
async def on_voice_state_update(member, before, after):
    global member_entry_times
    
    if after.channel and after.channel.id == waiting_room_channel_id:
        member_entry_times[member.id] = datetime.now()
        
    if before.channel and before.channel.id == waiting_room_channel_id and (not after.channel or after.channel.id != waiting_room_channel_id):
        member_entry_times.pop(member.id, None)

    await update_status_message()

@tree.command(name="next", description="Move the next user in line to your VC.", guild=discord.Object(id=1150751392030543914))
async def next(ctx):
    valid_member_entries = [(member_id, entry_time) for member_id, entry_time in member_entry_times.items() if "@" not in (ctx.guild.get_member(member_id).nick if ctx.guild.get_member(member_id).nick else ctx.guild.get_member(member_id).name)]
    
    if not valid_member_entries:
        await ctx.response.send_message("No one is waiting.", delete_after=5)
        return

    member_id, _ = sorted(valid_member_entries, key=lambda x: x[1])[0]
    member = ctx.guild.get_member(member_id)
    
    author_voice_channel = ctx.user.voice.channel if ctx.user.voice else None
    if author_voice_channel is None:
        await ctx.response.send_message("You must be in a voice channel to use this command.", delete_after=5)
        return

    await member.move_to(author_voice_channel)
    
    member_entry_times.pop(member_id, None)
    await update_status_message()
    await ctx.response.send_message(f"Moved <@{member_id}> to your voice channel.", delete_after=5)


client.run('BOT_SECRET_TOKEN')
