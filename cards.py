
def get_emote(card):
    if card["suit"] == -1:
        return "<:R_red:1073878240101412874>"
    if card["suit"] == -2:
        return "<:R_black:1073878238457233418>"
    return "💀"
# TODO: set up some smart way to get the rest of the emotes
# the hearts (from my private server)
# idea could be to take the two first chars of each string, delet second char if underscore
# then aces are 12 and 3s are 0, and you can sort suit by contains("suit name")
# suits alphabetical, clubs diamonds hearts spades
# <:A_hearts:1073878545455124571> <:2_hearts:1073878461053161472> <:Q_hearts:1073878549532004383><:K_hearts:1073878548043014194><:J_hearts:1073878546801508353> <:3_hearts:1073878462512775178> <:4_hearts:1073878463775244308> <:5_hearts:1073878464614121523> <:6_hearts:1073878465490731058> <:7_hearts:1073878467332022332> <:8_hearts:1073878541386657802> <:9_hearts:1073878542833700864> <:10_hearts:1073878543739662366>