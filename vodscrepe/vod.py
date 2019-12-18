import re
        
class Player():
    __slots__ = ['sponsor', 'name', 'characters']

    def __init__(self, sponsor="", name="", characters=[]):
        self.sponsor = sponsor
        self.name = name
        self.characters = characters

class Vod():
    def __init__(self, vod_id=""):
        self.vod_id = vod_id
        self.video_id = ""
        self.platform = ""

        self.date = ""
        self.tournament = ""

        self.player1 = Player()
        self.player2 = Player()

        self.round = ""
        self.format = ""

        self.games = []

    def parse_title(self, vod_title: str):
        title_pattern = "\(([0-9]*-[0-9]*-[0-9]*)\) (.*) vs (.*) \[(.*)\] - (.*) - (.*)"

        m = re.search(title_pattern, vod_title)

        self.date = m.group(1).strip()
        self.tournament = m.group(5).strip()

        self.player1.name = m.group(2).strip()
        self.player2.name = m.group(3).strip()

        self.round = m.group(6).strip()
        self.format = m.group(4).strip()

    def values(self):
        return [self.vod_id, self.video_id, self.platform, self.date,
                self.tournament, self.player1.name, self.player1.characters,
                self.player2.name, self.player2.characters,
                self.round, self.format]

    def formatted_title(self):
        title = ""

        if self.date:
            title += "[" + repr(self.date) + "] "
        if self.tournament:
            title += self.tournament + " - "

        if self.player1.sponsor:
            title += self.player1.sponsor + " | "
        if self.player1.name:
            title += self.player1.name + " "
        else:
            title += "Unknown "
        if self.player1.characters:
            title += "(" + ", ".join(self.player1.characters) + ") "

        title += "vs "

        if self.player2.sponsor:
            title += self.player2.sponsor + " | "
        if self.player2.name:
            title += self.player2.name + " "
        else:
            title += "Unknown "
        if self.player2.characters:
            title += "(" + ", ".join(self.player2.characters) + ") "

        if self.round:
            title += "- " + self.round + " "
        if self.format:
            title += "- " + self.format

        return title.strip()

    def __repr__(self):
        return repr(self.formatted_title())
