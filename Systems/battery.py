import random

class battery:
    def __init__(self, engine_simulator):
        self.engine_simulator = engine_simulator
        self.battery_level = 100

    def update_battery_level(self):
        if self.engine_simulator.accelerator_pressed:
            self.battery_level -= 2
        else:
            self.battery_level += 1

        if self.battery_level < 0:
            self.battery_level = 0
        elif self.battery_level > 100:
            self.battery_level = 100