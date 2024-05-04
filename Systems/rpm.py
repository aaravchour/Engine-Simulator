import random

class rpm:
    def __init__(self, engine_simulator):
        self.engine_simulator = engine_simulator

    def update_rpm(self):
        if self.throttle > 0:
            self.engine_rpm = int(self.throttle / 100.0 * 8500)
        elif self.throttle == 0:
            self.engine_rpm -= random.randint(1, 4000)

        if self.engine_rpm < 0:
            self.engine_rpm = 0
        elif self.engine_rpm > 8500:
            self.engine_rpm = 8500

        self.rpm_label.setText("RPM: " + str(self.engine_rpm))
        self.rpm_meter.setValue(self.engine_rpm)

        if self.accelerator_pressed:
            self.realism_system.update_all()

        