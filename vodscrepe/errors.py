class Error(Exception):
    message: str


class InvalidVideoError(Error):
    def __init__(self, vod_id: str):
        message = f"Invalid Video: vods.co vod '{vod_id}' links to invalid video"
        super().__init__(message)


class InvalidPageError(Error):
    def __init__(self, game, page):
        message = f"Invalid Page: vods.co game '{game}' does not have page '{page}'"
        super().__init__(message)
