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



bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
async def sync(ctx):
    synced = await ctx.bot.tree.sync()

@bot.hybrid_command()
async def ping(ctx):
    await ctx.interaction.response.send_message(content = 'pong', ephemeral = True)
    # await ctx.send(content = 'pong', ephemeral = True)

# client = MyClient(intents=intents)
# client.run(os.environ['TOKEN'])
bot.run(os.environ['TOKEN'])