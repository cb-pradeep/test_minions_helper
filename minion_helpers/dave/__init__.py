from minion_helpers.service import Service

DAVE_CLIENT = None


class Dave(Service):
    """
    Global Class for Handling Dave Maintenance Interactions
    """

    def __init__(self, endpoint_url=None):
        self.endpoint_url = endpoint_url

    def get_url(self):
        return self.endpoint_url


def _get_dave_client(*args, **kwargs):
    """
    Returns a Dave client to do Maintenance and other details.
    :return: Object of Dave
    """
    global DAVE_CLIENT
    if DAVE_CLIENT is None:
        DAVE_CLIENT = Dave(**kwargs)
    return DAVE_CLIENT


def client(*args, **kwargs):
    return _get_dave_client(*args, **kwargs)
