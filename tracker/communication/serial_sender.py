import serial
import time
import config


class SerialSender:
    CMD_MOVE = 0x01

    CMD_LEFT_CLICK = 0x02
    CMD_RIGHT_CLICK = 0x03
    CMD_MIDDLE_CLICK = 0x04

    CMD_LEFT_PRESS = 0x05
    CMD_LEFT_RELEASE = 0x06

    CMD_RIGHT_PRESS = 0x07
    CMD_RIGHT_RELEASE = 0x08

    CMD_SCROLL = 0x09

    def __init__(self):
        self.ser = serial.Serial(config.SERIAL_PORT, config.BAUDRATE)
        time.sleep(config.SERIAL_WAIT_SECONDS)

    def _send(self, data):
        self.ser.write(bytes(data))
        self.ser.flush()

    def move(self, dx, dy):
        dx = int(max(-127, min(127, dx)))
        dy = int(max(-127, min(127, dy)))

        self._send([
            self.CMD_MOVE,
            dx & 0xFF,
            dy & 0xFF
        ])

    def left_press(self):
        self._send([self.CMD_LEFT_PRESS])

    def left_release(self):
        self._send([self.CMD_LEFT_RELEASE])

    def right_press(self):
        self._send([self.CMD_RIGHT_PRESS])

    def right_release(self):
        self._send([self.CMD_RIGHT_RELEASE])

    def close(self):
        self.ser.close()