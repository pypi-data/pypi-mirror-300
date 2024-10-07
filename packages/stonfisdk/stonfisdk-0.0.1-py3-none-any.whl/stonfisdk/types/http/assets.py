from dataclasses import dataclass
from typing import Optional

from dataclasses_json import CatchAll, Undefined, dataclass_json


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class Asset:
    blacklisted: bool
    community: bool
    decimals: int
    default_symbol: bool
    deprecated: bool
    display_name: str
    image_url: str
    kind: str
    symbol: str
    contract_address: str
    dex_price_usd: Optional[str] = None
    third_party_price_usd: Optional[str] = None
    third_party_usd_price: Optional[str] = None
    dex_usd_price: Optional[str] = None
    balance: Optional[str] = None
    wallet_address: Optional[str] = None
    unknown_things: CatchAll = None

    @classmethod
    def from_dict(cls, param):
        pass

    @classmethod
    def schema(cls):
        pass


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass
class AssetsResponse:
    asset_list: list[Asset]
    unknown_things: CatchAll = None

    @classmethod
    def from_dict(cls, param):
        pass
