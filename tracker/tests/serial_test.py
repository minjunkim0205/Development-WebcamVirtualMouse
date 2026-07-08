import serial
import time

PORT = "COM5"
BAUD = 115200

ser = serial.Serial(PORT, BAUD)
time.sleep(2)

print("Connected")

while True:
    cmd = input("w/a/s/d, q 종료 : ")

    if cmd == "w":
        ser.write(bytes([0, (-10) & 0xFF]))

    elif cmd == "s":
        ser.write(bytes([0, 10]))

    elif cmd == "a":
        ser.write(bytes([(-10) & 0xFF, 0]))

    elif cmd == "d":
        ser.write(bytes([10, 0]))

    elif cmd == "q":
        break

ser.close()