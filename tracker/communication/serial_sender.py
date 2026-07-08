import serial
import time

class SerialSender:

    def __init__(self, port, baudrate):

        self.ser = serial.Serial(port, baudrate)

        time.sleep(2)

    def move(self, dx, dy):

        self.ser.write(bytes([
            dx & 0xFF,
            dy & 0xFF
        ]))

    def close(self):
        self.ser.close()