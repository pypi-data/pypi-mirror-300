from pytoniq import begin_cell, Cell, Address, LiteClientLike
from stonfisdk.constants import PTON_V1_ADDRESS

class pTON_V1:
    def __init__(self, address = PTON_V1_ADDRESS):
        self.address = Address(address)

