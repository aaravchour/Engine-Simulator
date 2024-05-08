import random

class fuel:
    def __init__(self, engine_simulator):
        self.engine_simulator = engine_simulator
        self.fuel_level = 100

    def update_fuel_level(self):
        if self.engine_simulator.accelerator_pressed:
            self.fuel_level -= 1
        else:
            self.fuel_level += 1

        if self.fuel_level < 0:
            self.fuel_level = 0
        elif self.fuel_level > 100:
            self.fuel_level = 100

