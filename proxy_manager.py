from datetime import datetime, timedelta
from collections import OrderedDict


class MyProxyManager:
    """
    Manages a global tracking of proxies, so proxy will not be used more than once in 10 seconds.
    """

    # will hold dictionary of {proxy_name: proxy} ordered by insertion time (first item --> last inserted)
    _proxies = None
    # we can use a proxy once in this seconds time interval
    _time_policy_in_seconds = 0

    def __init__(self, time_policy_in_seconds=10):

        self._proxies = OrderedDict()
        self._time_policy_in_seconds = time_policy_in_seconds

        self._load_proxies_from_file()

    def get_proxy(self):
        """
        gets the next available proxy, if none are available returns None.
        using FIFO,
        :return: normalized proxy or None
        """

        # loop through proxies (from the last recently used) to find an available one
        for proxy_name, proxy in self._proxies.iteritems():

            # if proxy is blocked, unblock it and move it to end
            if proxy.is_blocked():
                proxy.unblock()
                self._move_to_end(proxy_name, proxy_name)

            else:
                # if proxy time policy stops us, return None. Since each proxy used later than the next in dict
                if self._proxy_violates_time_policy(proxy) is True:
                    return None

                # if we are ok with proxy time policy, update its time, and move it to the end
                else:
                    proxy.update_last_used()
                    self._move_to_end(proxy_name, proxy)

                    return proxy.normalize()

        return None

    def _proxy_violates_time_policy(self, proxy):
        return proxy.used_later_than(datetime.now() - timedelta(seconds=self._time_policy_in_seconds))

    def _load_proxies_from_file(self):

        with open('proxies.txt', 'r') as f:
            for line in f:
                proxy = Proxy('http', 'http://{}'.format(line.strip()))
                self._add_proxy('{}'.format(line.strip()), proxy)

    def _add_proxy(self, proxy_name, proxy):
        self._proxies[proxy_name] = proxy

    def _move_to_end(self, proxy_name, proxy):
        if proxy_name in self._proxies:
            self._proxies.pop(proxy_name)
            self._proxies[proxy_name] = proxy


class Proxy:
    _protocol = ''
    _address = ''
    _blocked = None
    _last_used_timestamp = None

    def __init__(self, protocol, address):
        self._protocol = protocol
        self._address = address
        self._blocked = False

        # init last_used with yesterday, to make it available to use
        self._last_used_timestamp = datetime.now() - timedelta(days=1)

    def is_blocked(self):
        return self._blocked

    def unblock(self):
        self._blocked = False

    def block(self):
        self._blocked = True

    def update_last_used(self):
        self._last_used_timestamp.now()

    def used_later_than(self, timestamp):
        return self._last_used_timestamp > timestamp

    def normalize(self):
        return {self._protocol: self._address}


