from minion_helpers.bob.bob import Bob

BOB_CLIENT = None


def _get_bob_client(*args, **kwargs):
    """
    Returns a Bob client to do authentication and other details.
    :return: Object of Bob
    """
    global BOB_CLIENT
    if BOB_CLIENT is None:
        BOB_CLIENT = Bob(**kwargs)
    return BOB_CLIENT


def client(*args, **kwargs):
    return _get_bob_client(*args, **kwargs)
