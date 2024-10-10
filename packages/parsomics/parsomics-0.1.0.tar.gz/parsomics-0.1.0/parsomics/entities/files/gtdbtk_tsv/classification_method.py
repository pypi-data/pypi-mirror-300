from enum import Enum


class GTDBTkClassificationMethod(str, Enum):
    ANI = "ANI"
    TOPOLOGY = "TOPOLOGY"
    TOPOLOGY_ANI = "TOPOLOGY_ANI"
    TOPOLOGY_RED = "TOPOLOGY_RED"
    ANISCREEN = "ANISCREEN"
