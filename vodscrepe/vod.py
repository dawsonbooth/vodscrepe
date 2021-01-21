from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Vod:
    __slots__ = "vod_id", "video_ids", "date", "tournament", "players", "casters", "round", "best_of"

    vod_id: str
    video_ids: List[str]
    date: str
    tournament: str
    players: List[Vod.Player]
    casters: List[Vod.Caster]
    round: str
    best_of: int

    def __str__(self) -> str:
        date = f"[{self.date}]"
        players = " vs ".join(str(p) for p in self.players)
        best_of = f"Bo{self.best_of}"

        return f"{date} {self.tournament} - {players} - {self.round} - {best_of}"

    @dataclass
    class Player:
        __slots__ = "alias", "characters"

        alias: str
        characters: List[str]

        def __str__(self) -> str:
            return f"{self.alias} ({','.join(self.characters)})"

    @dataclass
    class Caster:
        __slots__ = ("alias",)

        alias: str

        def __str__(self) -> str:
            return self.alias
