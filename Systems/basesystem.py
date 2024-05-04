import random

import sys
sys.path.insert(0, 'Systems')


from temperatures import temperatures
from fuel import fuel
from oil import oil
from battery import battery
from enginehealth import enginehealth


class basesystem:
    def __init__(self, engine_simulator):
        self.engine_simulator = engine_simulator


    def update_all(self):
        self.update_temperature()
        self.update_fuel_level()
        self.update_oil_level()
        self.update_battery_level()


        
        
