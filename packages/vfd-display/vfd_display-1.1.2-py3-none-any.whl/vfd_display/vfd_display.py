import serial
import logging
from time import sleep

class VfdDisplay:
    def __init__(self, port="/dev/ttyUSB0", baudrate=9600, bytesize=serial.EIGHTBITS, 
                 parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1, enabled=True):
        self.enabled = enabled
        self.ser = None
        if self.enabled:
            try:
                self.ser = serial.Serial(port=port, baudrate=baudrate, bytesize=bytesize, 
                                         parity=parity, stopbits=stopbits, timeout=timeout)
                if self.ser.is_open:
                    logging.info("Serial connection opened successfully.")
                else:
                    logging.error("Error opening serial connection.")
            except serial.SerialException as e:
                logging.error(f"Serial connection error: {e}")
            sleep(2)

    def write_line(self, message, line=1, column=1):
        if self.enabled and self.ser:
            self.move_cursor(line, column)
            if line == 1:
                message = self.name_port(config["Position"]) + ": " + message
            self.ser.write(message.encode())

    def clear_screen(self):
        if self.enabled and self.ser:
            self.ser.write(b'\x0C')
            sleep(0.1)

    def move_cursor(self, line, column):
        if self.enabled and self.ser:
            cursor_move_cmd = [0x1F, 0x24, column, line]
            self.ser.write(bytes(cursor_move_cmd))

    def clear_line(self, line):
        if self.enabled and self.ser:
            self.move_cursor(line, 1)
            self.ser.write(b' ' * 20)

    def close(self):
        if self.enabled and self.ser:
            self.ser.close()

    def name_port(self, port):
        self.port = port.split("-")
        return self.port[1].strip()
