class Error(Exception):
    message: str


class InvalidVideoError(Error):
    def __init__(self, vod_id: str):
        message = f"Invalid Video: vods.co vod '{vod_id}' links to invalid video"
        super().__init__(message)


class InvalidPageError(Error):
    def __init__(self, *args):
        message = "Invalid Page: vods.co game '%s' does not have page '%i'" % args
        super().__init__(message)
