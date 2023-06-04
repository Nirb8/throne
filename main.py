# token accessible via: os.environ['TOKEN']
import discord
import os
from dotenv import load_dotenv

load_dotenv()
bot = discord.Bot()

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
    await ctx.respond("Hey!")


class CardSelectView(discord.ui.View):
    @discord.ui.select(
        placeholder="Choose the cards you want to play!",
        min_values=1,
        max_values=4,
        options=[
            discord.SelectOption(
                label="3 of Clubs",
                value="3_clubs",
                emoji=get_emote_from_string("3_clubs")
            ),
            discord.SelectOption(
                label="3 of Spades",
                value="3_spades",
                emoji=get_emote_from_string("3_spades")
            ),
            discord.SelectOption(
                label="3 of Hearts",
                value="3_hearts",
                emoji=get_emote_from_string("3_hearts")
            ),
            discord.SelectOption(
                label="3 of Diamonds",
                value="3_diamonds",
                emoji=get_emote_from_string("3_diamonds")
            ),
            discord.SelectOption(
                label="4 of Clubs",
                value="4_clubs",
                emoji=get_emote_from_string("4_clubs")
            ),
            discord.SelectOption(
                label="4 of Spades",
                value="4_spades",
                emoji=get_emote_from_string("4_spades")
            ),
            discord.SelectOption(
                label="4 of Hearts",
                value="4_hearts",
                emoji=get_emote_from_string("4_hearts")
            ),
            discord.SelectOption(
                label="4 of Diamonds",
                value="4_diamonds",
                emoji=get_emote_from_string("4_diamonds")
            ),
            discord.SelectOption(
                label="5 of Clubs",
                value="5_clubs",
                emoji=get_emote_from_string("5_clubs")
            ),
            discord.SelectOption(
                label="5 of Spades",
                value="5_spades",
                emoji=get_emote_from_string("5_spades")
            ),
            discord.SelectOption(
                label="5 of Hearts",
                value="5_hearts",
                emoji=get_emote_from_string("5_hearts")
            ),
            discord.SelectOption(
                label="5 of Diamonds",
                value="5_diamonds",
                emoji=get_emote_from_string("5_diamonds")
            ),
            discord.SelectOption(
                label="6 of Clubs",
                value="6_clubs",
                emoji=get_emote_from_string("6_clubs")
            ),
            discord.SelectOption(
                label="6 of Spades",
                value="6_spades",
                emoji=get_emote_from_string("6_spades")
            ),
            discord.SelectOption(
                label="6 of Hearts",
                value="6_hearts",
                emoji=get_emote_from_string("6_hearts")
            ),
            discord.SelectOption(
                label="6 of Diamonds",
                value="6_diamonds",
                emoji=get_emote_from_string("6_diamonds")
            ),
            discord.SelectOption(
                label="7 of Clubs",
                value="7_clubs",
                emoji=get_emote_from_string("7_clubs")
            ),
            discord.SelectOption(
                label="7 of Spades",
                value="7_spades",
                emoji=get_emote_from_string("7_spades")
            ),
            discord.SelectOption(
                label="7 of Hearts",
                value="7_hearts",
                emoji=get_emote_from_string("7_hearts")
            ),
            discord.SelectOption(
                label="7 of Diamonds",
                value="7_diamonds",
                emoji=get_emote_from_string("7_diamonds")
            ),
            discord.SelectOption(
                label="8 of Clubs",
                value="8_clubs",
                emoji=get_emote_from_string("8_clubs")
            ),
            # discord.SelectOption(
            #     label="8 of Spades",
            #     value="8_spades",
            #     emoji=get_emote_from_string("8_spades")
            # ),
            # discord.SelectOption(
            #     label="8 of Hearts",
            #     value="8_hearts",
            #     emoji=get_emote_from_string("8_hearts")
            # ),
            # discord.SelectOption(
            #     label="8 of Diamonds",
            #     value="8_diamonds",
            #     emoji=get_emote_from_string("8_diamonds")
            # ),
            # discord.SelectOption(
            #     label="9 of Clubs",
            #     value="9_clubs",
            #     emoji=get_emote_from_string("9_clubs")
            # ),
            # discord.SelectOption(
            #     label="9 of Spades",
            #     value="9_spades",
            #     emoji=get_emote_from_string("9_spades")
            # ),
            # discord.SelectOption(
            #     label="9 of Hearts",
            #     value="9_hearts",
            #     emoji=get_emote_from_string("9_hearts")
            # ),
            # discord.SelectOption(
            #     label="9 of Diamonds",
            #     value="9_diamonds",
            #     emoji=get_emote_from_string("9_diamonds")
            # ),
            # discord.SelectOption(
            #     label="10 of Clubs",
            #     value="10_clubs",
            #     emoji=get_emote_from_string("10_clubs")
            # ),
            # discord.SelectOption(
            #     label="10 of Spades",
            #     value="10_spades",
            #     emoji=get_emote_from_string("10_spades")
            # ),
            # discord.SelectOption(
            #     label="10 of Hearts",
            #     value="10_hearts",
            #     emoji=get_emote_from_string("10_hearts")
            # ),
            # discord.SelectOption(
            #     label="10 of Diamonds",
            #     value="10_diamonds",
            #     emoji=get_emote_from_string("10_diamonds")
            # ),
            # discord.SelectOption(
            #     label="Jack of Clubs",
            #     value="J_clubs",
            #     emoji=get_emote_from_string("J_clubs")
            # ),
            # discord.SelectOption(
            #     label="Jack of Spades",
            #     value="J_spades",
            #     emoji=get_emote_from_string("J_spades")
            # ),
            # discord.SelectOption(
            #     label="Jack of Hearts",
            #     value="J_hearts",
            #     emoji=get_emote_from_string("J_hearts")
            # ),
            # discord.SelectOption(
            #     label="Jack of Diamonds",
            #     value="J_diamonds",
            #     emoji=get_emote_from_string("J_diamonds")
            # ),
            # discord.SelectOption(
            #     label="Jack of Clubs",
            #     value="J_clubs",
            #     emoji=get_emote_from_string("J_clubs")
            # ),
            # discord.SelectOption(
            #     label="Jack of Spades",
            #     value="J_spades",
            #     emoji=get_emote_from_string("J_spades")
            # ),
            # discord.SelectOption(
            #     label="Jack of Hearts",
            #     value="J_hearts",
            #     emoji=get_emote_from_string("J_hearts")
            # ),
            # discord.SelectOption(
            #     label="Jack of Diamonds",
            #     value="J_diamonds",
            #     emoji=get_emote_from_string("J_diamonds")
            # ),
            # discord.SelectOption(
            #     label="Queen of Clubs",
            #     value="Q_clubs",
            #     emoji=get_emote_from_string("Q_clubs")
            # ),
            # discord.SelectOption(
            #     label="Queen of Spades",
            #     value="Q_spades",
            #     emoji=get_emote_from_string("Q_spades")
            # ),
            # discord.SelectOption(
            #     label="Queen of Hearts",
            #     value="Q_hearts",
            #     emoji=get_emote_from_string("Q_hearts")
            # ),
            # discord.SelectOption(
            #     label="Queen of Diamonds",
            #     value="Q_diamonds",
            #     emoji=get_emote_from_string("Q_diamonds")
            # ),
            # discord.SelectOption(
            #     label="King of Clubs",
            #     value="K_clubs",
            #     emoji=get_emote_from_string("K_clubs")
            # ),
            # discord.SelectOption(
            #     label="King of Spades",
            #     value="K_spades",
            #     emoji=get_emote_from_string("K_spades")
            # ),
            # discord.SelectOption(
            #     label="King of Hearts",
            #     value="K_hearts",
            #     emoji=get_emote_from_string("K_hearts")
            # ),
            # discord.SelectOption(
            #     label="King of Diamonds",
            #     value="K_diamonds",
            #     emoji=get_emote_from_string("K_diamonds")
            # ),
            # discord.SelectOption(
            #     label="Ace of Clubs",
            #     value="A_clubs",
            #     emoji=get_emote_from_string("A_clubs")
            # ),
            # discord.SelectOption(
            #     label="Ace of Spades",
            #     value="A_spades",
            #     emoji=get_emote_from_string("A_spades")
            # ),
            # discord.SelectOption(
            #     label="Ace of Hearts",
            #     value="A_hearts",
            #     emoji=get_emote_from_string("A_hearts")
            # ),
            # discord.SelectOption(
            #     label="Ace of Diamonds",
            #     value="A_diamonds",
            #     emoji=get_emote_from_string("A_diamonds")
            # ),
            discord.SelectOption(
                label="Pass",
                emoji="🗿",
            )
        ]
    )
    # the function called when the user is done selecting options
    async def select_callback(self, select, interaction):
        userPickedValues = ""
        for value in select.values:
            userPickedValues += get_emote_from_string(value)
        await interaction.response.send_message(userPickedValues)


@bot.command()
async def p(ctx):
    await ctx.send_response(content="**Card Select Menu**", view=CardSelectView(), ephemeral=True)

bot.run(os.getenv('TOKEN'))
