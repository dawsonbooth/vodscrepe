import re
import svp.smash.melee.singles as svp


class Vod(svp.Vod):
    def __init__(self, vod_id=""):
        self.vod_id = vod_id
        self.video_id = ""
        self.platform = ""

        super().__init__()

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
