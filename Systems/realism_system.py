import random

class RealismSystem:
    def __init__(self, engine_simulator):
        self.engine_simulator = engine_simulator
        self.temperature = 25
        self.fuel_level = 100
        self.oil_level = 100
        self.battery_level = 100

    def update_temperature(self):
        if self.engine_simulator.accelerator_pressed:
            self.temperature += 1
        else:
            self.temperature -= 1

        if self.temperature < 0:
            self.temperature = 0
        elif self.temperature > 50:
            self.temperature = 50

    def update_fuel_level(self):
        if self.engine_simulator.accelerator_pressed:
            self.fuel_level -= 1
        else:
            self.fuel_level += 1

        if self.fuel_level < 0:
            self.fuel_level = 0
        elif self.fuel_level > 100:
            self.fuel_level = 100

    def update_oil_level(self):
        if self.engine_simulator.accelerator_pressed:
            self.oil_level -= 1
        else:
            self.oil_level += 1

        if self.oil_level < 0:
            self.oil_level = 0
        elif self.oil_level > 100:
            self.oil_level = 100

    def update_battery_level(self):
        if self.engine_simulator.accelerator_pressed:
            self.battery_level -= 2
        else:
            self.battery_level += 1

        if self.battery_level < 0:
            self.battery_level = 0
        elif self.battery_level > 100:
            self.battery_level = 100

    def update_all(self):
        self.update_temperature()
        self.update_fuel_level()
        self.update_oil_level()
        self.update_battery_level()

    def check_engine_health(self):
        if self.temperature > 40 or self.fuel_level < 20 or self.oil_level < 20 or self.battery_level < 20:
            return False
        else:
            return True
        
    engine_health = ""

    if check_engine_health == "True":
        engine_health = "Healthy"
    else:
        engine_health = "Damaged"
        
    def update_rpm(self):
        if self.engine_simulator.accelerator_pressed:
            self.engine_rpm = int(self.throttle / 100.0 * 8500)
        else:
            self.engine_rpm = int(self.throttle * 1000 / (self.fuel_level + 100) * 8500 / (self.temperature + 1))