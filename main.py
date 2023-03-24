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
player_last_played = {}
game_in_progress = False
current_player = ""


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
async def undo(ctx):
    player = ctx.message.author.name
    if player_last_played[player]:
        undo_string = ""
        for card in player_last_played[player]:
            player_hands[player].append(card)
            undo_string += cards.get_emote(card)
        player_hands[player] = await sort_hand(player_hands[player], False)
        await respond_global(ctx=ctx, response=f"Undo: {undo_string}")
        player_last_played[player] = None
    else:
        await respond_ghost(ctx=ctx, response="Can't undo!")
@bot.hybrid_command()
async def give(ctx, rank, suit, recv_player):
    player = ctx.message.author.name
    if recv_player not in player_list:
        await respond_ghost(ctx=ctx, response="That player doesn't exist")
        return
    cards_to_give = []
    club_played = False
    diamond_played = False
    heart_played = False
    spade_played = False
    for c in suit:
        print(c)
        if c == "c" and club_played is False:
            cards_to_give.append({"suit": 0, "rank": int(rank)})
            club_played = True
        if c == "d" and diamond_played is False:
            cards_to_give.append({"suit": 1, "rank": int(rank)})
            diamond_played = True
        if c == "h" and heart_played is False:
            cards_to_give.append({"suit": 2, "rank": int(rank)})
            heart_played = True
        if c == "s" and spade_played is False:
            cards_to_give.append({"suit": 3, "rank": int(rank)})
            spade_played = True
        if c == "j":
            cards_to_give.append({"suit": -1, "rank": int(rank)})
    print(cards_to_give)
    legal = cards.verify_play(player_hands[player], cards_to_give)
    if legal is False:
        await respond_ghost(ctx=ctx, response="you can't play that 💀")
        return
    await respond_global(ctx=ctx, response=f"{player} gave {len(cards_to_give)} card(s) to {recv_player}.")
    for card in cards_to_give:
        cards.remove_card(card, player_hands[player])
        player_hands[recv_player].append(card)
        sorted_hand = await sort_hand(player_hands[recv_player], False)
        player_hands[recv_player] = sorted_hand
    return

@bot.hybrid_command()
async def p(ctx, rank, card_string):
    player = ctx.message.author.name
    print(f"player {player} called p with rank: {rank} and card string: {card_string}")
    if game_in_progress is False:
        await respond_ghost(ctx=ctx, response="game hasn't started yet dummy")
        return
    if player not in player_list:
        await respond_ghost(ctx=ctx, response="you ain't in the game yet dummy")
        return
    # taking out the turn rule for now
    # if player != current_player:
    #     await respond_ghost(ctx=ctx, response="wait your turn dummy")
    #     return
    rank = cards.rank_to_num(rank)
    if rank == -69:
        await respond_ghost(ctx=ctx, response="invalid rank 💀")
        return
# TODO actual validation and state updating, actually might not do this part because rules complex..
    cards_to_play = []
    club_played = False
    diamond_played = False
    heart_played = False
    spade_played = False
    for c in card_string:
        print(c)
        if c == "c" and club_played is False:
            cards_to_play.append({"suit": 0, "rank": int(rank)})
            club_played = True
        if c == "d" and diamond_played is False:
            cards_to_play.append({"suit": 1, "rank": int(rank)})
            diamond_played = True
        if c == "h" and heart_played is False:
            cards_to_play.append({"suit": 2, "rank": int(rank)})
            heart_played = True
        if c == "s" and spade_played is False:
            cards_to_play.append({"suit": 3, "rank": int(rank)})
            spade_played = True
        if c == "j":
            cards_to_play.append({"suit": -1, "rank": int(rank)})
    print(cards_to_play)
    legal = cards.verify_play(player_hands[player], cards_to_play)
    if legal is False:
        await respond_ghost(ctx=ctx, response="you can't play that 💀")
        return
    card_string = ""
    for card in cards_to_play:
        card_string += cards.get_emote(card)
    if card_string:
        await respond_global(ctx=ctx, response=f"{card_string}")
        print("deducting cards from player hand")
        # add to last played (for undo)
        player_last_played[player] = cards_to_play
        for card in cards_to_play:
            cards.remove_card(card, player_hands[player])
        return
    await respond_ghost(ctx=ctx, response="actually put some cards")
        

@bot.hybrid_command()
async def start(ctx, jokers = 2, burn_cards = 0):
    global game_in_progress
    global current_player
    if not game_in_progress:
        deck = shuffle.get_shuffled_deck_numeric(jokers)
        for i in range(0, burn_cards):
            deck.popitem()
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
async def end(ctx):
    global game_in_progress
    if not game_in_progress:
        await respond_ghost(ctx=ctx,response="Game not in progress dummy, don't jump the gun")
        return
    game_in_progress = False
    await respond_global(ctx=ctx,response="Ending current game and keeping current players")

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