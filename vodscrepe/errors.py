


class InvalidVideoException(Exception):
    def __init__(self, *args):
        message = "Invalid Video: vods.co vod '%s' links to invalid video" % args
        super(InvalidVideoException, self).__init__(message)


class InvalidPageException(Exception):
    def __init__(self, *args):
        message = "Invalid Page: vods.co game '%s' does not have page '%i'" % args
        super(InvalidPageException, self).__init__(message)
