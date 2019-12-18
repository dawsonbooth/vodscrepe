# TODO: Replace lambda match functions with machine learning lol
stages = {
    "Battlefield": lambda str: "battle" in str,
    "Dream Land N64": lambda str: "land" in str,
    "Final Destination": lambda str: "final" in str or str == "fd",
    "Fountain of Dreams": lambda str: "fountain" in str or str == "fod",
    "Yoshi's Story": lambda str: "yoshi" in str,
    "Pokemon Stadium": lambda str: "pokemon" in str or "stadium" in str or str == "ps",
    # TODO: Add non-legal stages
}
characters = {
    "Bowser": lambda str: "bowser" in str,
    "Captain Falcon": lambda str: "falcon" in str or str == "cf",
    "Donkey Kong": lambda str: "donkey" in str or str == "dk",
    "Dr. Mario": lambda str: "dr" in str,
    "Falco": lambda str: "falco" in str and "falcon" not in str,
    "Fox": lambda str: "fox" in str,
    "Ganondorf": lambda str: "ganon" in str,
    "Ice Climbers": lambda str: "ic" in str,
    "Jigglypuff": lambda str: "jig" in str or "puff" in str,
    "Kirby": lambda str: "kirby" in str,
    "Link": lambda str: "link" in str and "y" not in str,
    "Luigi": lambda str: "luigi" in str,
    "Mario": lambda str: "mario" in str and "dr" not in str,
    "Marth": lambda str: "marth" in str,
    "Mewtwo": lambda str: "mew" in str,
    "Mr. Game & Watch": lambda str: "game" in str or "&" in str,
    "Ness": lambda str: "ness" in str,
    "Peach": lambda str: "peach" in str or "daisy" in str,
    "Pichu": lambda str: "pichu" in str,
    "Pikachu": lambda str: "pikachu" in str,
    "Roy": lambda str: "roy" in str,
    "Samus": lambda str: "samus" in str,
    "Sheik": lambda str: "sheik" in str or "shiek" in str,
    "Young Link": lambda str: "link" in str and "y" in str,
    "Yoshi": lambda str: "yoshi" in str,
    "Zelda": lambda str: "zelda" in str
    # TODO: Add SSBU characters
}
rounds = {
    "Winners Quarters": lambda str: "winner" in str and "quarter" in str,
    "Winners Semis": lambda str: "winner" in str and "semi" in str,
    "Winners Finals": lambda str: "winner" in str and "final" in str,
    "Losers Eighths": lambda str: "loser" in str and "eight" in str,
    "Losers Quarters": lambda str: "loser" in str and "quarter" in str,
    "Losers Semis": lambda str: "loser" in str and "semi" in str,
    "Losers Finals": lambda str: "loser" in str and "final" in str,
    "Grand Finals": lambda str: "grand" in str and "final" in str,
}
sponsors = {
    "Team Liquid": lambda str: "liquid" in str or "tl" in str,
    "Alliance": lambda str: "[A]" in str or "alliance" in str,
    "Counter Logic Gaming": lambda str: "clg" in str or ("counter" in str and "logic" in str),
    "Cloud 9": lambda str: "C9" in str or "cloud" in str,

}


def character(str):
    str = str.lower()
    for char, compare in characters.items():
        if compare(str):
            return char
    return None


def stage(str):
    str = str.lower()
    for stage, compare in stages.items():
        if compare(str):
            return stage
    return None


def round(str):
    str = str.lower()
    for round, compare in rounds.items():
        if compare(str):
            return round
    return None