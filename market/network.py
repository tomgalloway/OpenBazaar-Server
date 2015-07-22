__author__ = 'chris'

import json

from market.protocol import MarketProtocol

from constants import DATA_FOLDER

from dht.utils import digest

from collections import OrderedDict

class Server(object):

    def __init__(self, kserver):
        self.kserver = kserver
        self.router = kserver.router
        self.protocol = MarketProtocol(kserver.node, self.router)

    def rpc_get_contract(self, contract_hash):
        try:
            with open (DATA_FOLDER + "/store/listings/contracts/" + contract_hash + ".json", "r") as file:
                contract = file.read()
            return contract
        except:
            return None

    def get_contract(self, guid, contract_hash):
        def get_result(result):
            if digest(result) == contract_hash:
                return json.loads(result, object_pairs_hook=OrderedDict)
            else:
                return None
        node_to_ask = self.kserver.get_node(guid)
        if node_to_ask is None:
            return None
        d = self.protocol.call_get_contract(guid, contract_hash)
        d.addCallback(get_result)