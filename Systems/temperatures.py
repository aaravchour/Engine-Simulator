import random

class temperatures:
    def __init__(self, engine_simulator):
        self.engine_simulator = engine_simulator
        self.temperature = 25

    def update_temperature(self):
        if self.engine_simulator.accelerator_pressed:
            self.temperature += 1
        else:
            self.temperature -= 1

        if self.temperature < 0:
            self.temperature = 0
        elif self.temperature > 50:
            self.temperature = 50