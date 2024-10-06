from typing import List, MutableMapping, Set

Parameters = MutableMapping[str, Set[str]]


class VcardProperty:  # pylint: disable=too-few-public-methods
    parameters: Parameters

    def __init__(self, name: str, values: List[List[str]]):
        self.name = name
        self.values = values
        self.parameters = {}
