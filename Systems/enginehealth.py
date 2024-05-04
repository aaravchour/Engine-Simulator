import random

class enginehealth:
    def __init__(self, engine_simulator):
        self.engine_simulator = engine_simulator

    def check_engine_health(self):
        if self.temperature > 40 or self.fuel_level < 20 or self.oil_level < 20 or self.battery_level < 20:
            return False
        else:
            return True