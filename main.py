import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# class MyClient(discord.Client):
#     async def on_ready(self):
#         print(f'Logged on as {self.user}!')

intents = discord.Intents.default()
intents.message_content = True

player_list = []

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
async def sync(ctx):
    synced = await ctx.bot.tree.sync()

@bot.hybrid_command()
async def ping(ctx):
    await ctx.interaction.response.send_message(content = 'pong', ephemeral = True)

@bot.hybrid_command()
async def join(ctx):
    print('join command run by user: ')
    print(ctx.message.author.name)
    new_player = ctx.message.author.name
    if new_player in player_list:
        await ctx.interaction.response.send_message(content = "You are already in the game!")
        return
    player_list.append(new_player)
    await ctx.interaction.response.send_message(content = 'You have joined the ongoing game as ' + new_player, ephemeral = True)

@bot.hybrid_command()
async def leave(ctx):
    player = ctx.message.author.name
    if player in player_list:
        print(f'Leave command run by user: {player}')
        player_list.remove(player)
        await respond(ctx, 'You have left the ongoing game')
        return
    await respond(ctx, "You aren't in the current game!")

@bot.hybrid_command()
async def listp(ctx):
    print(player_list)
    await ctx.interaction.response.send_message(content = player_list)

async def respond(ctx, response):
    await ctx.interaction.response.send_message(content=response, ephemeral=True)

bot.run(os.environ['TOKEN'])