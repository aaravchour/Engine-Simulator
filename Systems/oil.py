import random

class oil:
    def __init__(self, engine_simulator):
        self.engine_simulator = engine_simulator
        self.oil_level = 100


    def update_oil_level(self):
        if self.engine_simulator.accelerator_pressed:
            self.oil_level -= 1
        else:
            self.oil_level += 1

        if self.oil_level < 0:
            self.oil_level = 0
        elif self.oil_level > 100:
            self.oil_level = 100