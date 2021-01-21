import re


stages = {
    "Battlefield": re.compile(r"battle", flags=re.I),
    "Dream Land N64": re.compile(r"land", flags=re.I),
    "Final Destination": re.compile(r"final|fd", flags=re.I),
    "Fountain of Dreams": re.compile(r"fount|fod", flags=re.I),
    "Yoshi's Story": re.compile(r"yoshi", flags=re.I),
    "Pokemon Stadium": re.compile(r"pokemon|stadium|ps", flags=re.I),
}
characters = {
    "Bowser": re.compile(r"bowser", flags=re.I),
    "Captain Falcon": re.compile(r"falcon|cf", flags=re.I),
    "Donkey Kong": re.compile(r"donkey|kong|dk", flags=re.I),
    "Dr. Mario": re.compile(r"doc|dr", flags=re.I),
    "Falco": re.compile(r"falco\b", flags=re.I),
    "Fox": re.compile(r"fox", flags=re.I),
    "Ganondorf": re.compile(r"ganon", flags=re.I),
    "Ice Climbers": re.compile(r"ic", flags=re.I),
    "Jigglypuff": re.compile(r"jig|puff", flags=re.I),
    "Kirby": re.compile(r"kirby", flags=re.I),
    "Link": re.compile(r"(?!y)link", flags=re.I),
    "Luigi": re.compile(r"luigi", flags=re.I),
    "Mario": re.compile(r"(?!d)mario", flags=re.I),
    "Marth": re.compile(r"marth", flags=re.I),
    "Mewtwo": re.compile(r"mew", flags=re.I),
    "Mr. Game & Watch": re.compile(r"game|&", flags=re.I),
    "Ness": re.compile(r"ness", flags=re.I),
    "Peach": re.compile(r"peach|daisy", flags=re.I),
    "Pichu": re.compile(r"pichu", flags=re.I),
    "Pikachu": re.compile(r"pika", flags=re.I),
    "Roy": re.compile(r"roy", flags=re.I),
    "Samus": re.compile(r"samus", flags=re.I),
    "Sheik": re.compile(r"sh", flags=re.I),
    "Young Link": re.compile(r"y.*link", flags=re.I),
    "Yoshi": re.compile(r"yoshi", flags=re.I),
    "Zelda": re.compile(r"zelda", flags=re.I),
}
rounds = {
    "Winners Quarters": re.compile(r"winner.*quarter|wq", flags=re.I),
    "Winners Semis": re.compile(r"winner.*semi|ws", flags=re.I),
    "Winners Finals": re.compile(r"winner.*final|wf", flags=re.I),
    "Losers Eighths": re.compile(r"loser.*eight", flags=re.I),
    "Losers Quarters": re.compile(r"loser.*quarter|lq", flags=re.I),
    "Losers Semis": re.compile(r"loser.*semi|ls", flags=re.I),
    "Losers Finals": re.compile(r"loser.*final|lf", flags=re.I),
    "Grand Finals": re.compile(r"grand.*final|gf", flags=re.I),
}
sponsors = {
    "Team Liquid": re.compile(r"liquid|tl", flags=re.I),
    "Alliance": re.compile(r"\[A\]|alliance", flags=re.I),
    "Counter Logic Gaming": re.compile(r"clg|counter.*logic", flags=re.I),
    "Cloud 9": re.compile(r"c9|cloud", flags=re.I),
}


def guess_character(ch):
    for item, prog in characters.items():
        if prog.search(ch):
            return item
    return None


def guess_stage(s):
    for item, prog in stages.items():
        if prog.search(s):
            return item
    return None


def guess_round(r):
    for item, prog in rounds.items():
        if prog.search(r):
            return item
    return None


def guess_sponsor(s):
    for item, prog in sponsors.items():
        if prog.search(s):
            return item
    return None
