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
current_player = ""
current_trick = []

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
async def sync(ctx):
    print("syncing slash commands...")
    synced = await ctx.bot.tree.sync()

#this makes a button, still trying to sus it out
# class MyView(discord.ui.View):
#     @discord.ui.button(label='Example')
#     async def example_button(self, interaction: discord.Interaction, button: discord.ui.Button):
#         print(self.children)
#         await interaction.response.send_message('Hello!', ephemeral=True)
#
# @bot.hybrid_command()
# async def david(ctx):
#     view = MyView()
#     view.message = await ctx.send('Press me!', view=view)
#     msg = await ctx.send(content="hello!",ephemeral=True)
#     msg15 = await ctx.send(content="Hello 1.5!")
#     msg2 = await ctx.send(content="hello 2!!!!",ephemeral=True)
@bot.hybrid_command()
async def p(ctx, arg):
    
    player = ctx.message.author.name
    if game_in_progress is False:
        await respond_ghost(ctx=ctx, response="game hasn't started yet dummy")
        return
    if player not in player_list:
        await respond_ghost(ctx=ctx, response="you ain't in the game yet dummy")
        return
    if player != current_player:
        await respond_ghost(ctx=ctx, response="wait your turn dummy")
        return


@bot.hybrid_command()
async def start(ctx, jokers = 2):
    global game_in_progress
    global current_player
    if not game_in_progress:
        deck = shuffle.get_shuffled_deck_numeric(jokers)
        deck_string = ""
        current_player = player_list[0]
        print(f"current player: {current_player}")
        for card in deck.values():
            print(card)
            deck_string += cards.get_emote(card)
        await get_hands(deck)
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
        await respond_global(ctx = ctx, response = f'Player: {new_player} has joined the game!')
        return
    await respond_ghost(ctx=ctx,response="Can't join a game in progress")

@bot.hybrid_command()
async def addplayer(ctx, new_player):
    if not game_in_progress:
        if new_player in player_list:
            await respond_ghost(ctx = ctx, response = f"{new_player} is already in the game!")
            return
        player_list.append(new_player)
        await respond_global(ctx = ctx, response = f'Added {new_player} to the game')
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
async def sh(ctx):
    player = ctx.message.author.name
    print(f'show hand command run by user: {player}')
    if not game_in_progress:
        await respond_ghost(ctx=ctx,response="Game hasn't started yet")
        return
    if player not in player_list:
        await respond_ghost(ctx = ctx, response = "Not in game")
        return
    deck_string = ""
    prev_card = []
    for card in player_hands[player]:
        prev_card = card
        break
    for card in player_hands[player]:
        if card["rank"] != prev_card["rank"]:
            deck_string+="   "
        prev_card = card
        deck_string += cards.get_emote(card)
    await respond_ghost(ctx = ctx, response = deck_string)
    
async def respond_ghost(ctx, response):
    await ctx.interaction.response.send_message(content=response, ephemeral=True)

async def respond_global(ctx, response):
    await ctx.interaction.response.send_message(content=response)

async def get_hands(deck):
    num_players = len(player_list)
    hands_value, leftover = shuffle.deal(num_players, deck)
    i = 0
    for player in player_list:
        sorted_hand = await sort_hand(hands_value[i], False)
        player_hands[player] = sorted_hand
        i += 1

async def sort_hand(hand, in_revolution):
    res= sorted(hand,key=lambda card: (card['rank'], card['suit']), reverse = in_revolution)
    return res

bot.run(os.environ['TOKEN'])