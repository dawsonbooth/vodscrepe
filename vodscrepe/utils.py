

def formatted_title(vod) -> str:
    title = ""
    title += "[" + repr(vod["date"]) + "] "
    title += vod["tournament"] + " - "
    title += vod["players"][0]["name"] + " "
    title += "(" + ", ".join(vod["players"][0]["characters"]) + ") "
    title += "vs "
    title += vod["players"][1]["name"] + " "
    title += "(" + ", ".join(vod["players"][1]["characters"]) + ") "
    title += "- " + vod["round"] + " "
    title += "- Bo" + str(vod["best_of"])

    return title


def build_url(video_game, event: str = None, player1: str = None, player2: str = None, character1: str = None, character2: str = None) -> str:
    base_url = "https://vods.co/" + video_game
    if player1:
        base_url += "/player/" + player1
    if player2:
        base_url += "/player2/" + player2
    if event:
        base_url += "/event/" + event
    if character1:
        base_url += "/character/" + character1
    if character2:
        base_url += "/character2/" + character2
    return base_url