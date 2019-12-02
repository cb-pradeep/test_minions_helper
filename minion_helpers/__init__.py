# Copyright Chargebee 2019.
# Created by cb-infra team

import logging
import minion_helpers.bob as Bob
import minion_helpers.carl as Carl
import minion_helpers.dave as Dave

services = {
    'bob': Bob.client,
    'carl': Carl.client,
    'dave': Dave.client,
}


class UnknownServiceException(Exception):
    pass


def summon(*args, **kwargs):
    """
    Base function to call all the Minion Helper Clients
    :return: Return the client required for micro service actions
    """
    try:
        return services[args[0]](*args, **kwargs)
    except KeyError:
        raise UnknownServiceException("Unknown Service Summon. %s" % args[0])


# Set up logging to ``/dev/null`` like a library is supposed to.
# http://docs.python.org/3.3/howto/logging.html#configuring-logging-for-a-library
class NullHandler(logging.Handler):
    def emit(self, record):
        pass


logging.getLogger('minion_helpers').addHandler(NullHandler())
