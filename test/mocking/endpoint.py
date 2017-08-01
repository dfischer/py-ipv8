import random

from twisted.internet import reactor

from messaging.interfaces.endpoint import Endpoint

internet = {}


class MockEndpoint(Endpoint):

    def __init__(self, lan_address, wan_address):
        super(MockEndpoint, self).__init__()
        internet[lan_address] = self
        internet[wan_address] = self

        self.lan_address = lan_address
        self.wan_address = wan_address

    def assert_open(self):
        pass

    def is_open(self):
        return True

    def get_address(self):
        return self.wan_address

    def send(self, socket_address, packet):
        if socket_address in internet:
            reactor.callInThread(internet[socket_address].notify_listeners, packet)

    def open(self):
        pass

    def close(self, timeout=0.0):
        pass


class AutoMockEndpoint(MockEndpoint):

    def __init__(self):
        super(AutoMockEndpoint, self).__init__(self._generate_unique_address(), self._generate_unique_address())

    def _generate_address(self):
        b0 = random.randint(0, 255)
        b1 = random.randint(0, 255)
        b2 = random.randint(0, 255)
        b3 = random.randint(0, 255)
        port = random.randint(0, 65535)

        return ('%d.%d.%d.%d' % (b0, b1, b2, b3), port)

    def _generate_unique_address(self):
        address = self._generate_address()

        while address in internet:
            address = self._generate_address()

        return address
