import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import shuffle
import cards
load_dotenv()

# class MyClient(discord.Client):
#     async def on_ready(self):
#         print(f'Logged on as {self.user}!')

intents = discord.Intents.default()
intents.message_content = True

player_list = []
player_hands = {}
game_in_progress = False

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
async def sync(ctx):
    print("syncing slash commands...")
    synced = await ctx.bot.tree.sync()

@bot.hybrid_command()
async def ping(ctx):
    await ctx.interaction.response.send_message(content = 'pong', ephemeral = True)

@bot.hybrid_command()
async def start(ctx):
    global game_in_progress
    if not game_in_progress:
        game_in_progress = True
        await respond_global(ctx=ctx,response="THE GAME HAS STARTED") #TODO: Print out the standings
        return
    await respond_ghost(ctx=ctx,response="Game in progress dummy, don't jump the gun")

@bot.hybrid_command()
async def screwthis(ctx):
    global game_in_progress
    global player_list
    player = ctx.message.author.name
    if game_in_progress:
        game_in_progress = False
        player_list = []
        await respond_global(ctx = ctx, response=f"Player {player} flipped the table. Laugh at them!")
        return
    await respond_ghost(ctx = ctx, response="Game hasn't started dummy don't try and quit already")


@bot.hybrid_command()
async def join(ctx):
    new_player = ctx.message.author.name
    print(f'join command run by user: {new_player}')
    if not game_in_progress:
        if new_player in player_list:
            await respond_ghost(ctx = ctx, response = "You are already in the game!")
            return
        player_list.append(new_player)
        await respond_ghost(ctx = ctx, response = f'You have joined the ongoing game as {new_player}')
        return
    await respond_ghost(ctx=ctx,response="Can't join a game in progress")

@bot.hybrid_command()
async def addplayer(ctx, new_player):
    if not game_in_progress:
        if new_player in player_list:
            await respond_ghost(ctx = ctx, response = f"{new_player} is already in the game!")
            return
        player_list.append(new_player)
        await respond_ghost(ctx = ctx, response = f'Added {new_player} to the game')
        return
    await respond_ghost(ctx=ctx,response="Can't join a game in progress")

@bot.hybrid_command()
async def leave(ctx):
    if not game_in_progress:
        if (player := ctx.message.author.name) in player_list:
            print(f'Leave command run by user: {player}')
            player_list.remove(player)
            await respond_ghost(ctx = ctx, response = 'You have left the ongoing game')
            return
        await respond_ghost(ctx = ctx, response = "You aren't in the current game! use /join to join")
        return
    await respond_ghost(ctx=ctx,response="Can't leave mid match, find the secret command to end the game!")

@bot.hybrid_command()
async def rmplayer(ctx, player_name):
    print(f"To Remove {player_name}")
    if not game_in_progress:
        if player_name in player_list:
            player_list.remove(player_name)
            await respond_global(ctx=ctx,response=f"Player: {player_name} has been removed from the game")
            return
        await respond_ghost(ctx=ctx,response=f"Player: {player_name} is currently not in the game")
        return
    await respond_ghost(ctx=ctx, response="Cannot remove a player mid game")


@bot.hybrid_command()
async def listp(ctx):
    print(player_list)
    await respond_global(ctx = ctx, response = player_list)


@bot.hybrid_command()
async def deckme(ctx):
    deck = shuffle.get_shuffled_deck_numeric(2)
    deck_string = ""
    for card in deck.values():
        print(card)
        deck_string += cards.get_emote(card)
    await get_hands(ctx, deck)

async def get_hands(ctx, deck):
    num_players = len(player_list)
    hands_value = shuffle.deal(num_players, deck)
    i = 0
    for player in player_list:
        sorted_hand = await sort_hand(hands_value[0][i], False)
        player_hands[player] = sorted_hand
        i += 1
    await respond_global(ctx = ctx, response=hands_value)

async def sort_hand(hand, in_revolution):
    res= sorted(hand,key=lambda card: card['suit'],     reverse = in_revolution)
    res = sorted(hand,key=lambda card: card['rank'],     reverse = in_revolution)
    return res

@bot.hybrid_command()
async def sh(ctx):
    new_player = ctx.message.author.name
    print(f'show hand command run by user: {new_player}')
    if not game_in_progress:
        await respond_ghost(ctx=ctx,response="Game hasn't started yet")
        return
    if new_player not in player_list:
        await respond_ghost(ctx = ctx, response = "Not in game")
        return
    deck_string = ""
    prev_card = []
    for card in player_hands[new_player]:
        prev_card = card
        break
    for card in player_hands[new_player]:
        if card["rank"] != prev_card["rank"]:
            deck_string+="   "
        prev_card = card
        deck_string += cards.get_emote(card)
    await respond_ghost(ctx = ctx, response = deck_string)
    
async def respond_ghost(ctx, response):
    await ctx.interaction.response.send_message(content=response, ephemeral=True)

async def respond_global(ctx, response):
    await ctx.interaction.response.send_message(content=response)

bot.run(os.environ['TOKEN'])