import os
import ctypes
from dotenv import load_dotenv
import discord
import game_lib
import card_lib

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
    game.state.players.append(new_player)
    await ctx.respond(f"Player {ctx.author.mention} has joined the game in this channel")
    return


@bot.command(name="listmem", description="Show participating players in the game in this channel")
async def listmem(ctx):
    game = game_lib.find_game(ctx.channel.id, games)
    if game is False:
        await ctx.respond("A game doesn't exist in this channel yet, create one with /makegame")
        return
    players = game.state.players
    player_list_string = f"List of players in channel {ctx.channel}:\n"
    for p in players:
        player_list_string += f"{p.username}\n"
    await ctx.respond(player_list_string)
    return

# TODO delet this later when mvp is delivered


@bot.command(name="addmem_debug", description="hardcoded to add two users for testing purposes")
async def debugaddmem(ctx):
    game = game_lib.find_game(ctx.channel.id, games)
    if game is False:
        await ctx.respond("A game doesn't exist in this channel yet, create one with /makegame")
        return
    p2 = game_lib.Player("216969551584165888", "<@216969551584165888>")
    p3 = game_lib.Player("479758872412684290", "<@479758872412684290>")
    game.state.players.append(p2)
    game.state.players.append(p3)
    await ctx.respond("added extra members")


@bot.command(name="deal", description="deal new hands")
async def deal(ctx, num_decks="1", num_jokers="2", paltry_deck = "0"):
    num_decks = int(num_decks)
    num_jokers = int(num_jokers)
    paltry_deck = int(paltry_deck)
    
    game = game_lib.find_game(ctx.channel.id, games)
    if game is False:
        await ctx.respond("A game doesn't exist in this channel yet, create one with /makegame")
        return
    game.shuffle(num_decks, num_jokers)
    game.deal()
    if paltry_deck == 1:
        game.deal_paltry()
    await ctx.respond(f"Dealt hands of size {len(game.state.players[0].hand)} to all players.")


@bot.command(name="stats", description="show current game stats")
async def stats(ctx):
    game = game_lib.find_game(ctx.channel.id, games)
    if game is False:
        await ctx.respond("A game doesn't exist in this channel yet, create one with /makegame")
        return
    stat_string = ""
    if game.state.last_played_cards != []:
        stat_string += f"Current Trick: {card_lib.hand_as_emotes(game.state.last_played_cards)} played by {game.state.last_played_player}\n"
    stat_string += f"Current Player: {game.state.current_player.username}\n"
    stat_string += f"Turn Order:\n {game.state.get_turn_order_string()}\n"
    await ctx.send_response(stat_string, allowed_mentions=discord.AllowedMentions.none())


@bot.command(name="trick", description="show currently played cards in big emote format")
async def trick(ctx):
    game = game_lib.find_game(ctx.channel.id, games)
    if game is False:
        await ctx.respond("A game doesn't exist in this channel yet, create one with /makegame")
        return
    if game.state.last_played_cards == []:
        await ctx.send_response(f"There are no cards in play at the moment. It is {game.state.current_player}'s turn.")
        return
    await ctx.send_response(f"{card_lib.hand_as_emotes(game.state.last_played_cards)}")


async def card_select_menu_gameplay_callback_generator(ctx, card_select_menu, player_id = None):
    async def card_selection_callback_gameplay(interaction):
        game = game_lib.find_game(interaction.channel.id, games)
        # player = game_lib.find_player(interaction.user.id, game)
        player = game_lib.find_player(player_id, game)
        spoofing_override = True
        if game.state.current_player != player and spoofing_override is False:
            turn_order_string = game.state.get_turn_order_string()
            await interaction.response.send_message(f"It's not your turn yet, the current player is {game.state.current_player}. The turn order is: \n{turn_order_string}", ephemeral=True)
            return
        if player.is_active is False:
            await interaction.response.send_message(content="You're already out!", ephemeral=True)
            return
        user_picked_cards = []
        card_emote_string = ""
        for value in card_select_menu.values:
            # convert reference id to Card object and append it to user_picked_cards
            value_as_int = int(value)
            if value_as_int > 100:
                user_picked_cards.append(ctypes.cast(
                    value_as_int, ctypes.py_object).value)
                continue
            # if the value is less than 100, it is a special option?
            if value_as_int == 0:
                is_new_trick = game.make_pass()
                if is_new_trick:
                    await interaction.response.send_message(
                        f"Everyone passed 🗿🗿🗿 \n{game.state.current_player} gets to start a new trick")
                    return
                await interaction.response.send_message(
                    f"{player} has passed 🗿 \nIt's now {game.state.current_player}'s turn")
                return
        cards_not_held = []
        for card in user_picked_cards:
            if card not in player.hand:
                cards_not_held.append(card)
        if len(cards_not_held) > 0:
            not_held_emotes = card_lib.hand_as_emotes(cards_not_held)
            await interaction.response.send_message(f"You are missing the cards: {not_held_emotes}.\nTry using the /p command again to refresh your card selection menu.", ephemeral = True)
            return
        # TODO intercept this with a joker value replacement method and purge the option cards
        user_picked_cards.sort()
        # build card emote string from selected cards
        card_emote_string = card_lib.hand_as_emotes(user_picked_cards)
        legal = card_lib.is_play_legal(user_picked_cards)
        if not legal:
            await interaction.response.send_message(f"{card_emote_string} is an illegal move!", ephemeral=True)
            return
        play_message = game.state.check_play_valid(user_picked_cards)
        if play_message != "ok":
            await interaction.response.send_message(f"{play_message}", ephemeral=True)
            return
        move_status_message = game.make_move(player, user_picked_cards)
        if move_status_message != "ok":
            await ctx.send(move_status_message)
        
        # if move_status == game_lib.MoveStatus.One_Player_Out:
        #     await ctx.send(f"{player} has played all their cards and is now out of the game.")
        # if move_status == game_lib.MoveStatus.All_Out:
        #     await ctx.send(f"{player} has played all their cards and is now out of the game.")
        #     await ctx.send_followup(f"Game is over, standings: \n{game.get_player_titles()}")
        await interaction.response.send_message(f"{player.username} played: {card_emote_string}", allowed_mentions=discord.AllowedMentions.none())
        await ctx.send_followup(card_emote_string)
    return card_selection_callback_gameplay
@bot.command()
async def p(ctx, spoof_player=None):
    game = game_lib.find_game(ctx.channel.id, games)
    if game is False:
        await ctx.respond("A game doesn't exist in this channel yet, create one with /makegame")
        return
    player_id = ctx.author.id
    if spoof_player is not None and int(spoof_player)<len(game.state.players):
        player_id = game.state.players[int(spoof_player)].player_id
        await ctx.send(f"spoofing player {game_lib.find_player(player_id, game)}")
    player = game_lib.find_player(player_id, game)
    if player is False:
        await ctx.send_response(content="You aren't in this game yet", ephemeral=True)
        return
    if player.is_active is False:
        await ctx.send_response(content="You're already out!", ephemeral=True)
        return
    if game.gaming is False:
        await ctx.send_response(content="Game hasn't started yet, be patient", ephemeral=True)
        return
    if game.state.current_player != player:
        turn_order_string = game.state.get_turn_order_string()
        await ctx.send_response(content=f"It's not your turn yet, the current player is {game.state.current_player}. The turn order is: \n{turn_order_string}", ephemeral=True)
        return
    card_select_menu = card_lib.build_select_menu_from_hand(True, player.hand)

    card_select_menu.callback = await card_select_menu_gameplay_callback_generator(ctx, card_select_menu, player_id)
    card_select_menu.max_values = 13
    if len(player.hand) < 13:
        card_select_menu.max_values = len(player.hand)
    view = discord.ui.View()
    view.add_item(card_select_menu)
    await ctx.send_response(content=f"**Card Selection Menu** for **{player}**", view=view, ephemeral=True)

@bot.command(name="trade", description="show currently played cards in big emote format")
async def trade(ctx, spoof_player=None):
    game = game_lib.find_game(ctx.channel.id, games)
    if game is False:
        await ctx.respond("A game doesn't exist in this channel yet, create one with /makegame")
        return
    player_id = ctx.author.id
    if spoof_player is not None and int(spoof_player)<len(game.state.players):
        player_id = game.state.players[int(spoof_player)].player_id
        await ctx.send(f"spoofing player {game_lib.find_player(player_id, game)}")
    player = game_lib.find_player(player_id, game)
    
    card_select_menu = card_lib.build_select_menu_from_hand(False, player.hand)
    
    card_select_menu.callback = await card_select_menu_trading_callback_generator(ctx, card_select_menu, player_id)
    card_select_menu.max_values = 2
    card_select_menu.min_values = 1
    if player.title == game_lib.Title("Biggest Loser"):
        card_select_menu.min_values = 2
    if player.title == game_lib.Title("Vice President") or player.title == game_lib.Title("Poor"):
        card_select_menu.max_values = 1
    view = discord.ui.View()
    view.add_item(card_select_menu)
    await ctx.send_response(content=f"**Trading Selection Menu** for **{player}**({player.title.value})", view=view, ephemeral=True)
async def card_select_menu_trading_callback_generator(ctx, card_select_menu, player_id):
    async def card_selection_callback_trading(interaction):
        game = game_lib.find_game(interaction.channel.id, games)
        # player = game_lib.find_player(interaction.user.id, game)
        player = game_lib.find_player(player_id, game)
        if player.title == game_lib.Title("*The Guy*"):
            await interaction.response.send_message(content=f"You're The Guy👨, no trading for you", ephemeral=True)
            return
        if player.is_trading is False:
            await interaction.response.send_message(content=f"You've already traded!", ephemeral=True)
            return
        user_picked_cards = []
        for value in card_select_menu.values:
            # convert reference id to Card object and append it to user_picked_cards
            value_as_int = int(value)
            user_picked_cards.append(ctypes.cast(
                    value_as_int, ctypes.py_object).value)
        user_picked_cards.sort()
        card_emote_string = card_lib.hand_as_emotes(user_picked_cards)
        
        trading_message = card_lib.is_trade_legal(user_picked_cards, player.hand, player.title)
        if trading_message != "ok":
            await interaction.response.send_message(content=f"Your trade of {card_emote_string} is invalid. {trading_message}", ephemeral=True)
            return
        dest_player = game.find_trading_recipient(player)
        
        # the actual giving of cards
        for card in user_picked_cards:
            player.hand.remove(card)
            dest_player.hand.append(card)
        dest_player.hand.sort()
        player.is_trading = False
        
        await interaction.response.send_message(content=f"Your trade of {card_emote_string} was successful.", ephemeral=True)
    return card_selection_callback_trading


bot.run(os.getenv('TOKEN'))
