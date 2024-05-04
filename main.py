import time
import random
import playsound
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QSlider, QProgressBar
from PyQt5.QtCore import QTimer, Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

import sys
sys.path.insert(0, 'Systems')

from Systems.basesystem import basesystem
from Systems.temperatures import temperatures
from Systems.fuel import fuel
from Systems.oil import oil
from Systems.battery import battery
from Systems.enginehealth import enginehealth



class EngineSimulator(QWidget):
    def __init__(self):
        super().__init__()

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


    def initUI(self):
        self.setWindowTitle('Engine Simulator')

        self.vbox = QVBoxLayout()

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

        self.accelerator_button = QPushButton("Start Engine", self)
        self.vbox.addWidget(self.accelerator_button)

        self.throttle_slider = QSlider(Qt.Vertical)
        self.throttle_slider.setMinimum(0)
        self.throttle_slider.setMaximum(100)
        self.vbox.addWidget(self.throttle_slider)

        self.rpm_meter = QProgressBar(self)
        self.rpm_meter.setMinimum(0)
        self.rpm_meter.setMaximum(8500)
        self.vbox.addWidget(self.rpm_meter)

        self.setLayout(self.vbox)

        self.engine_rpm = 0
        self.accelerator_pressed = False
        self.throttle = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_rpm)
        self.timer.start(100)

        self.throttle_slider.valueChanged.connect(self.update_throttle)

        self.accelerator_button.clicked.connect(self.accelerator)

        self.show()

    def accelerator(self):
        self.accelerator_pressed = True
        self.accelerator_button.setEnabled(False)
        self.accelerator_button.hide()
        self.stop_button = QPushButton("Stop Engine", self)
        self.stop_button.clicked.connect(self.stop)
        self.vbox.addWidget(self.stop_button)
        self.stop_button.show()
        
        playsound.playsound('engine_sound.wav')

        self.timer_throttle = QTimer()
        self.timer_throttle.timeout.connect(self.update_rpm)
        self.timer_throttle.start(1000)

    def stop(self):
        self.accelerator_button.show()
        self.stop_button.hide()
        self.accelerator_button.setEnabled(True)
        self.accelerator_pressed = False

    def update_throttle(self):
        self.throttle = self.throttle_slider.value()
        self.timer_throttle = QTimer()
        self.timer_throttle.timeout.connect(self.update_rpm)
        self.timer_throttle.start(1000)  
        

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
            self.temperatures.update_temperature()
            self.fuel.update_fuel_level()
            self.oil.update_oil_level()
            self.battery.update_battery_level()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EngineSimulator()
    sys.exit(app.exec_())