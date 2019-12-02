from minion_helpers.service import Service

CARL_CLIENT = None


class Carl(Service):
    """
    Global Class for Handling Carl Logger Interactions
    """

    def __init__(self, endpoint_url=None):
        self.endpoint_url = endpoint_url

    def get_url(self):
        return self.endpoint_url


def _get_carl_client(*args, **kwargs):
    """
    Returns a Carl client to do Logging and other details.
    :return: Object of Bob
    """
    global CARL_CLIENT
    if CARL_CLIENT is None:
        CARL_CLIENT = Carl(**kwargs)
    return CARL_CLIENT


def client(*args, **kwargs):
    return _get_carl_client(*args, **kwargs)
