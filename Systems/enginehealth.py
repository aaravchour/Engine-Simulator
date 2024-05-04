import random

import sys
sys.path.insert(0, 'Systems')

from temperatures import temperatures
from fuel import fuel
from oil import oil
from battery import battery

class enginehealth:
    def __init__(self, engine_simulator):
        self.engine_simulator = engine_simulator

        self.temperatures = temperatures(self)
        self.fuel = fuel(self)
        self.oil = oil(self)
        self.battery = battery(self)
        

    