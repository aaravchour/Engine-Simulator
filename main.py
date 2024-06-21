import sys
import random
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QProgressBar,
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image, ImageDraw, ImageFont
from math import cos, sin, radians


class EngineSimulator(QWidget):
    def __init__(self):
        super().__init__()
        self.max_rpm = 9000
        self.throttle_value = 0
        self.engine_rpm = 0
        self.accelerator_pressed = False
        self.fuel_level = 100.0
        self.battery_level = 100.0
        self.timer_throttle = QTimer()
        self.timer_throttle.timeout.connect(self.update_rpm)
        self.timer_battery = QTimer()
        self.timer_battery.timeout.connect(self.update_battery)
        self.initUI()

    def draw_rpm_meter(self, rpm):
        width, height = 400, 400
        img = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        centre_x, centre_y = width // 2, height // 2
        radius = 150

        draw.ellipse(
            (
                centre_x - radius,
                centre_y - radius,
                centre_x + radius,
                centre_y + radius,
            ),
            outline=(0, 0, 0),
            width=5,
        )

        num_markings = 9
        font = ImageFont.load_default()

        for i in range(num_markings + 1):
            angle = 180 - (i * 180 / num_markings)
            x_start = centre_x + radius * 0.8 * cos(radians(angle))
            y_start = centre_y - radius * 0.8 * sin(radians(angle))
            x_end = centre_x + radius * cos(radians(angle))
            y_end = centre_y - radius * sin(radians(angle))
            draw.line((x_start, y_start, x_end, y_end), fill=(0, 0, 0), width=2)

            rpm_value = int(self.max_rpm / num_markings * i)
            text_x = centre_x + (radius - 40) * cos(radians(angle)) - 10
            text_y = centre_y - (radius - 40) * sin(radians(angle)) - 10
            draw.text((text_x, text_y), str(rpm_value), fill=(0, 0, 0), font=font)

        angle = 180 - (rpm * 180 / self.max_rpm)
        x_end = centre_x + (radius - 20) * cos(radians(angle))
        y_end = centre_y - (radius - 20) * sin(radians(angle))
        draw.line((centre_x, centre_y, x_end, y_end), fill=(255, 0, 0), width=3)

        return img

    def update_rpm(self):
        if self.accelerator_pressed:
            self.throttle_value += 1
            if self.throttle_value > 100:
                self.throttle_value = 100
            self.engine_rpm = int(self.throttle_value / 100.0 * self.max_rpm)
        else:
            self.throttle_value -= 1
            if self.throttle_value < 0:
                self.throttle_value = 0
            self.engine_rpm -= random.randint(1, 100)
            if self.engine_rpm < 0:
                self.engine_rpm = 0

        self.rpm_label.setText("RPM: " + str(self.engine_rpm))
        self.rpm_meter.setValue(self.engine_rpm)

        rpm_image = self.draw_rpm_meter(self.engine_rpm)
        rpm_qimage = QImage(
            rpm_image.tobytes(), rpm_image.width, rpm_image.height, QImage.Format_RGB888
        )
        self.rpm_image_label.setPixmap(QPixmap.fromImage(rpm_qimage))

        self.redline()
        self.update_fuel(self.engine_rpm)

    def accelerator(self):
        self.accelerator_pressed = True
        self.timer_throttle.start(50)

    def accelerator_released(self):
        self.accelerator_pressed = False

    def stop(self):
        self.accelerator_button.show()
        self.stop_button.hide()
        self.accelerator_button.setEnabled(True)
        self.accelerator_pressed = False
        self.timer_throttle.stop()
        self.timer_battery.stop()

    def redline(self):
        if self.engine_rpm >= self.max_rpm:
            self.health_label.setText("Engine Health: REDLINE")
            self.health_label.setStyleSheet("color: red")
            self.rpm_label.setStyleSheet("color: red")
        else:
            self.health_label.setText("Engine Health: OK")
            self.health_label.setStyleSheet("color: white")
            self.rpm_label.setStyleSheet("color: white")

    def update_fuel(self, value):
        if self.accelerator_pressed:
            self.fuel_level -= 0.001
            if self.fuel_level < 0:
                self.fuel_level = 0
        self.fuel_label.setText("Fuel Level: " + str(round(self.fuel_level, 2)))
        if self.fuel_level == 0:
            self.engine_rpm = 0

    def update_battery(self):
        if self.accelerator_pressed:
            self.battery_level += 0.01
            if self.battery_level > 100:
                self.battery_level = 100
        else:
            self.battery_level -= 0.01
            if self.battery_level < 0:
                self.battery_level = 0
        self.battery_label.setText(
            "Battery Level: " + str(round(self.battery_level, 2))
        )
        self.update_battery_status()

    def update_battery_status(self):
        if self.accelerator_pressed:
            self.battery_status_label.setText("Battery Status: CHARGING")
        else:
            self.battery_status_label.setText("Battery Status: DISCHARGING")

    def update_temperature(self):
        if self.engine_rpm > 0 and self.engine_rpm < 2125:
            self.temperature_level = 23

    def initUI(self):
        self.setWindowTitle("Engine Simulator")

        self.vbox = QVBoxLayout(self)

        self.rpm_label = QLabel("RPM: 0", self)
        self.vbox.addWidget(self.rpm_label)

        self.temperature_label = QLabel("Temperature: 0", self)
        self.vbox.addWidget(self.temperature_label)

        self.fuel_label = QLabel("Fuel Level: 0", self)
        self.vbox.addWidget(self.fuel_label)

        self.battery_label = QLabel("Battery Level: 0", self)
        self.vbox.addWidget(self.battery_label)

        self.battery_status_label = QLabel("Battery Status: STANDBY", self)
        self.vbox.addWidget(self.battery_status_label)

        self.health_label = QLabel("Engine Health: OK", self)
        self.vbox.addWidget(self.health_label)

        self.accelerator_button = QPushButton("Accelerator", self)
        self.vbox.addWidget(self.accelerator_button)

        self.rpm_meter = QProgressBar(self)
        self.rpm_meter.setMinimum(0)
        self.rpm_meter.setMaximum(self.max_rpm)
        self.vbox.addWidget(self.rpm_meter)

        self.rpm_image_label = QLabel(self)
        self.vbox.addWidget(self.rpm_image_label)

        self.setLayout(self.vbox)

        self.accelerator_button.pressed.connect(self.accelerator)
        self.accelerator_button.released.connect(self.accelerator_released)

        self.setMinimumWidth(400)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = EngineSimulator()
    sys.exit(app.exec_())
