import playsound
import random
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QSlider, QProgressBar
from PyQt5.QtCore import QTimer, Qt

class ui(QWidget):
    def __init__(self):
        super().__init__()
        self.sound_handle = None
        self.initUI()
        self.throttle_value = 0 
        self.engine_rpm = 0
        self.accelerator_pressed = False
#
#
#
#
#
#
#
# RPM Handler
    def update_throttle(self, value):
        self.throttle_value = value  

    def update_rpm(self):
        if self.throttle_value > 0:
            self.engine_rpm = int(self.throttle_value / 100.0 * 8500)
        elif self.throttle_value == 0:
            self.engine_rpm -= random.randint(1, 4000)

        if self.engine_rpm < 0:
            self.engine_rpm = 0
        elif self.engine_rpm > 8500:
            self.engine_rpm = 8500

        self.rpm_label.setText("RPM: " + str(self.engine_rpm))
        self.rpm_meter.setValue(self.engine_rpm)

        self.redline()

#
#
#
#
#
#
#
# Start button + Stop button
    def accelerator(self):
        self.accelerator_pressed = True
        self.accelerator_button.setEnabled(False)
        self.accelerator_button.hide()
        self.stop_button = QPushButton("Stop Engine", self)
        self.stop_button.clicked.connect(self.stop)
        self.vbox.addWidget(self.stop_button)
        self.stop_button.show()

        playsound.playsound('sounds/engine_sound.wav')

        self.timer_throttle = QTimer()
        self.timer_throttle.timeout.connect(self.update_rpm)
        self.timer_throttle.start(400)

    def stop(self):
        self.accelerator_button.show()
        self.stop_button.hide()
        self.accelerator_button.setEnabled(True)
        self.accelerator_pressed = False
#
#
#
#
#
#
#
# Redline handler
    def redline(self):
        if self.engine_rpm >= 8500:
            self.health_label.setText("Engine Health: REDLINE")
            self.health_label.setStyleSheet("color: red")
            self.rpm_label.setStyleSheet("color:red")
        else:
            self.health_label.setText("Engine Health: OK")
            self.health_label.setStyleSheet("color: white")
            self.rpm_label.setStyleSheet("color:white")

#
#
#
#
#
#
#
# UI Handler
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

        self.accelerator_button.clicked.connect(self.accelerator)
        self.throttle_slider.valueChanged.connect(self.update_throttle)

        self.setMinimumWidth(400)

        self.show()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex = ui()
    sys.exit(app.exec_())
