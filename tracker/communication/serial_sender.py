import serial
import time


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

    def __init__(self, port, baudrate):
        self.ser = serial.Serial(port, baudrate)
        time.sleep(2)

    def _send(self, data):
        self.ser.write(bytes(data))

    def move(self, dx, dy):
        self._send([
            self.CMD_MOVE,
            dx & 0xFF,
            dy & 0xFF
        ])

    def click(self, button="left"):
        if button == "left":
            self._send([self.CMD_LEFT_CLICK])
        elif button == "right":
            self._send([self.CMD_RIGHT_CLICK])
        elif button == "middle":
            self._send([self.CMD_MIDDLE_CLICK])

    def press(self, button="left"):
        if button == "left":
            self._send([self.CMD_LEFT_PRESS])
        elif button == "right":
            self._send([self.CMD_RIGHT_PRESS])

    def release(self, button="left"):
        if button == "left":
            self._send([self.CMD_LEFT_RELEASE])
        elif button == "right":
            self._send([self.CMD_RIGHT_RELEASE])

    def scroll(self, amount):
        self._send([
            self.CMD_SCROLL,
            amount & 0xFF
        ])

    def close(self):
        self.ser.close()