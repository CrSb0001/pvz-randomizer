from __future__ import annotations

import copy
import random
import multiprocessing

from collections import Counter
from time import perf_count_ns
from os import cpu_count

from util_helpers import *

class MockSetting:
    def __init__(self, value):
        self.value = value
    
    def __bool__(self):
        return bool(self.value)
    
    def get(self):
        return self.value

# Mock writing to address
def write_memory(type_, data, *addr) -> None:
    return


SUCCESS             = 0x00
FAILURE_GOOD_PLANTS = 0x01
FAILURE_POOL_ONE    = 0x02
FAILURE_POOL_TWO    = 0x03
FAILURE_POOL_TRHEE  = 0x04
FAILURE_POOL_FOUR   = 0x05
FAILURE_ROOF_ONE    = 0x06
FAILURE_POT_TWO     = 0x07
FAILURE_GARGS       = 0x08
FAILURE_BALLOON_ONE = 0x09
FAILURE_BALLOON_TWO = 0x0A
FAILURE_SHROOMS     = 0x0B
FAILURE_INSTA       = 0x0C
FAILURES_COUNT      = 0x0D

DEFAULT_FLAGS = {
    k + 1:v for k, v in enumerate(
        [1, 1, 1, 1, 1, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 2, 1, 2, 2, 3, 2, 2, 3, 2, 3, 3, 1, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1, 2, 2, 3, 2, 2, 3, 2, 3, 3]
)}
DEFAULT_WAVECOUNT = {k + 1:v for k, v in enumerate([4, 6, 8, 10, 8] + [DEFAULT_FLAGS[x] * 10 for x in range_(5, 49)])}
DEFAULT_WAVES_PER_FLAG = {x + 1:10 for x in range_(49)}

WAVE_POINT_ARRAY = [1, 1, 2, 2, 4, 2, 4, 7, 5, 0, 1,
                    3, 7, 3, 3, 3, 2, 4, 4, 4, 3, 4,
                    5, 10, 10, 0, 1, 4, 3, 3, 3, 7, 10]

ZOMBIES = [[]]
PLANTS  = [[]]

BYTES_PER_PLANT_STRING  = 0x0200
BYTES_PER_ZOMBIE_STRING = 0x0200
BYTES_PER_GAME_STRING   = 0x0100
NUM_OF_PLANT_STRINGS    = 0x32
NUM_OF_ZOMBIE_STRINGS   = 0x21
NUM_OF_GAME_STRINGS     = 0x18

STRONG_ZOMBIES = [0x04, 0x06, 0x07, 0x0C, 0x15, 0x17, 0x1F, 0x20]

BUCKETHEADS_PRESENT = [0x08, 0x09, 0x0C, 0x0D, 0x0E, 0x11, 0x13, 0x16, 0x18, 0x1B, 0x1D, 0x25, 0x26, 0x27, 0x2A, 0x2B, 0x2C, 0x2E, 0x2F, 0x31]
PLAYABLE_NON_POT    = [0x02, 0x03, 0x04, 0x06, 0x07, 0x0B, 0x0D, 0x12, 0x13, 0x15, 0x17, 0x1C, 0x1F, 0x21, 0x22, 0x29, 0x2B, 0x2E, 0x2F]
FOOTBALLERS_PRESENT = [0x10, 0x11, 0x16, 0x1A, 0x1B, 0x1D, 0x20, 0x2C, 0x2E, 0x2F, 0x30, 0x31]
