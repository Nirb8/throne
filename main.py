# token accessible via: os.environ['TOKEN']
import discord
import os
import game_lib
import ctypes
from dotenv import load_dotenv

load_dotenv()
bot = discord.Bot()

# TODO this should be backed up to a database/text file
games = []

# TODO move these into a new cards.py
EMOTE_DICT = {'A_hearts': '<:A_hearts:1073878545455124571>', '2_hearts': '<:2_hearts:1073878461053161472>', 'Q_hearts': '<:Q_hearts:1073878549532004383>', 'K_hearts': '<:K_hearts:1073878548043014194>', 'J_hearts': '<:J_hearts:1073878546801508353>', '3_hearts': '<:3_hearts:1073878462512775178>', '4_hearts': '<:4_hearts:1073878463775244308>', '5_hearts': '<:5_hearts:1073878464614121523>', '6_hearts': '<:6_hearts:1073878465490731058>', '7_hearts': '<:7_hearts:1073878467332022332>', '8_hearts': '<:8_hearts:1073878541386657802>', '9_hearts': '<:9_hearts:1073878542833700864>', '10_hearts': '<:10_hearts:1073878543739662366>', '10_clubs': '<:10_clubs:1073878161495965737>', '10_diamonds': '<:10_diamonds:1073876973966852167>', '10_spades': '<:10_spades:1073877343371800616>', '2_clubs': '<:2_clubs:1073878065270231050>', '2_diamonds': '<:2_diamonds:1073866501662191626>', '2_spades': '<:2_spades:1073877181387771925>', '3_clubs': '<:3_clubs:1073878067455463454>', '3_diamonds': '<:3_diamonds:1073865772578918410>', '3_spades': '<:3_spades:1073877183069683732>', '4_clubs': '<:4_clubs:1073878068655030293>', '4_diamonds': '<:4_diamonds:1073876967671201853>', '4_spades': '<:4_spades:1073877183820464198>', '5_clubs': '<:5_clubs:1073878069674250320>',
              '5_diamonds': '<:5_diamonds:1073876969147617300>', '5_spades': '<:5_spades:1073877184940355594>', '6_clubs': '<:6_clubs:1073878070420832297>', '6_diamonds': '<:6_diamonds:1073876970288459857>', '6_spades': '<:6_spades:1073877185997328454>', '7_clubs': '<:7_clubs:1073878072085975121>', '7_diamonds': '<:7_diamonds:1073876971060207647>', '7_spades': '<:7_spades:1073877187431759922>', '8_clubs': '<:8_clubs:1073878158052438036>', '8_diamonds': '<:8_diamonds:1073876971433500743>', '8_spades': '<:8_spades:1073877340658073640>', '9_clubs': '<:9_clubs:1073878160086683770>', '9_diamonds': '<:9_diamonds:1073876972675006494>', '9_spades': '<:9_spades:1073877341819899924>', 'A_diamonds': '<:A_diamonds:1073866534147084348>', 'A_spades': '<:A_spades:1073877347637416038>', 'J_clubs': '<:J_clubs:1073878162670366761>', 'J_diamonds': '<:J_diamonds:1073876974797344818>', 'J_spades': '<:J_spades:1073877350015582248>', 'K_clubs': '<:K_clubs:1073878164243234823>', 'K_diamonds': '<:K_diamonds:1073877048239607828>', 'K_spades': '<:K_spades:1073877351399698503>', 'Q_clubs': '<:Q_clubs:1073878165287612447>', 'Q_diamonds': '<:Q_diamonds:1073877049078464592>', 'Q_spades': '<:Q_spades:1073877352565710918>', 'A_clubs': '<:A_clubs:1074251701952983140>'}


def get_emote_from_string(card_string):
    if card_string not in EMOTE_DICT.keys():
        return "💀"
    return EMOTE_DICT[card_string]


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online")


@bot.command(name="hello", description="Say hello to Throne")
async def hello(ctx):
    # print(ctx.channel.__dir__())
    await ctx.respond(f"Hey User {ctx.author} in channel {ctx.channel} (id: {ctx.channel.id})")
    return

@bot.command(name="makegame", description="Make a new game in this channel (limit 1 per channel)")
async def makegame(ctx):
    game = game_lib.find_game(ctx.channel.id, games)
    if game:
        await ctx.respond("A game has already been created in this channel.")
        return
    new_game = game_lib.Game(ctx.channel.id)
    games.append(new_game)
    await ctx.respond(f"Created new game in channel {ctx.channel}")
@bot.command(name="joingame", description="Join the ongoing game in this channel")
async def joingame(ctx):
    player_id = ctx.author.id
    game = game_lib.find_game(ctx.channel.id, games)
    if game is False:
        await ctx.respond("A game doesn't exist in this channel yet, create one with /makegame")
        return
    player = game_lib.find_player(player_id, game)
    if player:
        await ctx.respond(f"Player {ctx.author.mention} has already joined the game in this channel")
        return
    new_player = game_lib.Player(player_id, ctx.author.mention)
    game.players.append(new_player)
    await ctx.respond(f"Player {ctx.author.mention} has joined the game in this channel")
    return
@bot.command(name="listmem", description="Show participating players in the game in this channel")
async def listmem(ctx):
    game = game_lib.find_game(ctx.channel.id, games)
    if game is False:
        await ctx.respond("A game doesn't exist in this channel yet, create one with /makegame")
        return
    players = game.players
    player_list_string = f"List of players in channel {ctx.channel}:\n"
    for p in players:
        player_list_string += f"{p.username}\n"
    await ctx.respond(player_list_string)
    return

# TODO delet this later when mvp is delivered
@bot.command(name="debugaddmem", description="hardcoded to add two users for testing purposes")
async def debugaddmem(ctx):
    game = game_lib.find_game(ctx.channel.id, games)
    if game is False:
        await ctx.respond("A game doesn't exist in this channel yet, create one with /makegame")
        return
    p2 = game_lib.Player("216969551584165888", "<@216969551584165888>")
    p3 = game_lib.Player("479758872412684290", "<@479758872412684290>")
    game.players.append(p2)
    game.players.append(p3)
    await ctx.respond("added extra members")

@bot.command(name="deal", description="deal new hands")
async def deal(ctx, num_decks = 1, num_jokers = 2):
    game = game_lib.find_game(ctx.channel.id, games)
    if game is False:
        await ctx.respond("A game doesn't exist in this channel yet, create one with /makegame")
        return
    game.shuffle(num_decks, num_jokers)
    game.deal()
    await ctx.respond(f"Dealt hands of size {len(game.players[0].hand)} to all players.")
@bot.command()
async def p(ctx):
    player_id = ctx.author.id
    game = game_lib.find_game(ctx.channel.id, games)
    if game is False:
        await ctx.respond("A game doesn't exist in this channel yet, create one with /makegame")
        return
    player = game_lib.find_player(player_id, game)
    if player is False:
        await ctx.send_response(content="You aren't in this game yet", ephemeral = True)
        return
    # await ctx.send_response(content="**Card Select Menu**", view=CardSelectView(), ephemeral=True)
    if game.gaming is False:
        await ctx.send_response(content="Game hasn't started yet, be patient", ephemeral = True)
        return
    # TODO will probably want to extract into separate method 
    card_options = []
    for card in player.hand:
        new_option = discord.SelectOption(label=card.get_human_readable(), emoji=card.get_emote(), value = str(id(card)))
        card_options.append(new_option)
    card_select_menu = discord.ui.Select(options=card_options)
    async def card_selection_callback(interaction):
        user_picked_cards = []
        user_picked_values = ""
        for value in card_select_menu.values:
            # convert reference id to Card object and append it to user_picked_cards
            value_as_int = int(value)
            user_picked_cards.append(ctypes.cast(value_as_int, ctypes.py_object).value)
        user_picked_cards.sort()
        # TODO perform a verification process on user_picked_cards
        # TODO if verification successful remove user_picked_cards from user's cards
        for card in user_picked_cards:
            user_picked_values += card.get_emote()
        await interaction.response.send_message(user_picked_values)
    card_select_menu.callback = card_selection_callback
    card_select_menu.max_values = 13
    if len(player.hand) < 13:
        card_select_menu.max_values = len(player.hand)
    view = discord.ui.View()
    view.add_item(card_select_menu)
    await ctx.send_response(content="**Card Selection Menu**", view=view, ephemeral = True)
    
bot.run(os.getenv('TOKEN'))
