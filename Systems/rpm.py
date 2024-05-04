import random

class basesystem:
    def __init__(self, engine_simulator):
        self.engine_simulator = engine_simulator

    def update_rpm(self):
        if self.engine_simulator.accelerator_pressed:
            self.engine_rpm = int(self.throttle / 100.0 * 8500)
        else:
            self.engine_rpm = int(self.throttle * 1000 / (self.fuel_level + 100) * 8500 / (self.temperature + 1))