class Error(Exception):
    pass


class InvalidVideoError(Error):
    def __init__(self, *args):
        message = "Invalid Video: Vods.co vod '%s' links to invalid '%s' video: '%s'" % args
        super(InvalidVideoError, self).__init__(message)
