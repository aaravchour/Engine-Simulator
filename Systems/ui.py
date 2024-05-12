import playsound
import random
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QSlider, QProgressBar
from PyQt5.QtCore import QTimer, Qt

from basesystem import basesystem
from temperatures import temperatures
from fuel import fuel
from oil import oil
from battery import battery
from enginehealth import enginehealth


class ui(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def update_throttle(self):
        self.parent.update_throttle()

    def update_rpm(self):
        if self.parent.throttle > 0:
            self.parent.engine_rpm = int(self.parent.throttle / 100.0 * 8500)
        elif self.parent.throttle == 0:
            self.parent.engine_rpm -= random.randint(1, 4000)

        if self.parent.engine_rpm < 0:
            self.parent.engine_rpm = 0
        elif self.parent.engine_rpm > 8500:
            self.parent.engine_rpm = 8500

        self.rpm_label.setText("RPM: " + str(self.parent.engine_rpm))
        self.rpm_meter.setValue(self.parent.engine_rpm)

        if self.parent.accelerator_pressed:
            self.parent.temperatures.update_temperature()
            self.parent.fuel.update_fuel_level()
            self.parent.oil.update_oil_level()
            self.parent.battery.update_battery_level()

    def accelerator(self):
        self.parent.accelerator_pressed = True
        self.parent.accelerator_button.setEnabled(False)
        self.parent.accelerator_button.hide()
        self.stop_button = QPushButton("Stop Engine", self)
        self.stop_button.clicked.connect(self.stop)
        self.vbox.addWidget(self.stop_button)
        self.stop_button.show()

        playsound.playsound('engine_sound.wav')

        self.timer_throttle = QTimer()
        self.timer_throttle.timeout.connect(self.update_rpm)
        self.timer_throttle.start(400)

    def stop(self):
        self.parent.accelerator_button.show()
        self.stop_button.hide()
        self.parent.accelerator_button.setEnabled(True)
        self.parent.accelerator_pressed = False

    def redline(self):
        if self.parent.engine_rpm >= 8500:
            self.health_label.setText("Engine Health: REDLINE")
            self.health_label.setStyleSheet("color: red")
            self.rpm_label.setStyleSheet("color:red")
        else:
            self.health_label.setText("Engine Health: OK")
            self.health_label.setStyleSheet("color: white")
            self.rpm_label.setStyleSheet("color:white")

    def initUI(self):
        self.setWindowTitle('Engine Simulator')

        self.vbox = QVBoxLayout(self)

        self.rpm_label = QLabel("RPM: 0", self)
        self.vbox.addWidget(self.rpm_label)

        self.temperature_label = QLabel("Temperature: 0", self)
        self.vbox.addWidget(self.temperature_label)

        self.fuel_label = QLabel("Fuel Level: 0", self)
        self.vbox.addWidget(self.fuel_label)

        self.oil_label = QLabel("Oil Level: 0", self)
        self.vbox.addWidget(self.oil_label)

        self.battery_label = QLabel("Battery Level: 0", self)
        self.vbox.addWidget(self.battery_label)

        self.health_label = QLabel("Engine Health: OK", self)
        self.vbox.addWidget(self.health_label)

        self.parent.accelerator_button = QPushButton("Start Engine", self)
        self.vbox.addWidget(self.parent.accelerator_button)

        self.throttle_slider = QSlider(Qt.Vertical)
        self.throttle_slider.setMinimum(0)
        self.throttle_slider.setMaximum(100)
        self.vbox.addWidget(self.throttle_slider)

        self.rpm_meter = QProgressBar(self)
        self.rpm_meter.setMinimum(0)
        self.rpm_meter.setMaximum(8500)
        self.vbox.addWidget(self.rpm_meter)

        self.setLayout(self.vbox)

        self.parent.accelerator_button.clicked.connect(self.accelerator)
        self.throttle_slider.valueChanged.connect(self.update_throttle)

        self.setMinimumWidth(400)

        self.show()


class EngineSimulator(QWidget):
    def __init__(self):
        super().__init__()

        self.ui = ui(parent=self)
        self.initUI()

        self.temperature = 25
        self.fuel_level = 100
        self.oil_level = 100
        self.battery_level = 100

        self.basesystem = basesystem(self)
        self.temperatures = temperatures(self)
        self.fuel = fuel(self)
        self.oil = oil(self)
        self.battery = battery(self)
        self.enginehealth = enginehealth(self)

        self.engine_rpm = 0
        self.accelerator_pressed = False
        self.throttle = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_rpm)
        self.timer.start(400)

    def update_throttle(self):
        self.throttle = self.ui.throttle_slider.value()

    def update_rpm(self):
        if self.throttle > 0:
            self.engine_rpm = int(self.throttle / 100.0 * 8500)
        elif self.throttle == 0:
            self.engine_rpm -= random.randint(1, 4000)

        if self.engine_rpm < 0:
            self.engine_rpm = 0
        elif self.engine_rpm > 8500:
            self.engine_rpm = 8500

        self.ui.rpm_label.setText("RPM: " + str(self.engine_rpm))
        self.ui.rpm_meter.setValue(self.engine_rpm)
        self.ui.redline()

        if self.accelerator_pressed:
            self.temperatures.update_temperature()
            self.fuel.update_fuel_level()
            self.oil.update_oil_level()
            self.battery.update_battery_level()

    def initUI(self):
        self.show()


