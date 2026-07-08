from communication.serial_sender import SerialSender

sender = SerialSender("COM9", 115200)

while True:
    cmd = input("w/a/s/d move, l left, r right, m middle, p press, o release, +/- scroll, q quit > ")

    if cmd == "w":
        sender.move(0, -10)
    elif cmd == "s":
        sender.move(0, 10)
    elif cmd == "a":
        sender.move(-10, 0)
    elif cmd == "d":
        sender.move(10, 0)
    elif cmd == "l":
        sender.click("left")
    elif cmd == "r":
        sender.click("right")
    elif cmd == "m":
        sender.click("middle")
    elif cmd == "p":
        sender.press("left")
    elif cmd == "o":
        sender.release("left")
    elif cmd == "+":
        sender.scroll(3)
    elif cmd == "-":
        sender.scroll(-3)
    elif cmd == "q":
        break

sender.close()