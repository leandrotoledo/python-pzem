import minimalmodbus
import logging
import time
from datetime import datetime


class PZEM(minimalmodbus.Instrument):
    def __init__(self, serial_port, slave_addr=1):
        minimalmodbus.Instrument.__init__(self, serial_port, slave_addr)
        self.serial.baudrate = 9600
        self.serial.parity = minimalmodbus.serial.PARITY_NONE
        self.serial.timeout = 0.1
        self.mode = minimalmodbus.MODE_RTU
        self.close_port_after_each_call = True

        self.registers = {
            "voltage": {
                "address": (0, 1, 4),  # 0.1V
            },
            "current": {"address": (1, 2, 4), "multiplier": 0.1},  # 0.001A
            "power": {"address": (3, 2, 4), "multiplier": 10},  # 0.1W
            "energy": {"address": (5, 2, 4), "multiplier": 10},  # 1Wh
            "frequency": {
                "address": (7, 1, 4),  # 0.1Hz
            },
            "power_factor": {"address": (8, 1, 4), "multiplier": 0.1},  # 0.01
            "alarm_status": {
                "address": (9, 0, 4),  # 0xFFF for alarm
            },
            "alarm_threshold": {
                "address": (1, 0, 3),  # 1W
            },
            "set_alarm_threshold": {"address": (1, None, 0, 6)},
            "set_slave_address": {"address": (2, None, 0, 6)},
            "reset_energy": {"address": (66, "")},
        }

    @property
    def voltage(self) -> float:
        return self.read_register(*self.registers["voltage"]["address"])

    @property
    def current(self) -> float:
        value = self.read_register(*self.registers["current"]["address"])
        if value:
            return round(value * self.registers["current"]["multiplier"], 3)
        return value

    @property
    def power(self) -> float:
        value = self.read_register(*self.registers["power"]["address"])
        if value:
            return round(value * self.registers["power"]["multiplier"], 1)
        return value

    @property
    def energy(self) -> int:
        value = self.read_register(*self.registers["energy"]["address"])
        if value:
            return round(value * self.registers["energy"]["multiplier"], 1)
        return value

    @property
    def frequency(self) -> float:
        return self.read_register(*self.registers["frequency"]["address"])

    @property
    def power_factor(self) -> float:
        value = self.read_register(*self.registers["power_factor"]["address"])
        if value:
            return round(value * self.registers["power_factor"]["multiplier"], 1)
        return value

    @property
    def has_alarm(self) -> bool:
        value = self.read_register(*self.registers["alarm_status"]["address"])
        if value:
            return True
        return False

    @property
    def alarm_threshold(self) -> int:
        return self.read_register(*self.registers["alarm_threshold"]["address"])

    def set_alarm_threshold(self, watts: int) -> bool:
        try:
            args = list(self.registers["set_alarm_threshold"]["address"])
            args[1] = watts

            self.write_register(*args)
            return True
        except Exception:
            logging.exception("Failed to set alarm threshold.")

        return False

    def set_slave_address(self, slave_address: int) -> bool:
        try:
            args = list(self.registers["set_slave_address"]["address"])
            args[1] = slave_address

            self.write_register(*args)
            return True
        except Exception as e:
            logging.exception("Failed to set slave address.")

        return False

    def reset_energy(self) -> bool:
        try:
            self._performCommand(*self.registers["reset_energy"]["address"])
            return True
        except Exception as e:
            logging.exception("Failed to reset energy counters.")

        return False

    def report(self, delay=5) -> None:
        print("Timestamp \t\t| V \t| A \t| W \t| Wh \t| Hz \t| PF \t| Alarm Status \t| Alarm Threshold")
        while True:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\t| "
                  + f"{self.voltage}\t| "
                  + f"{self.current}\t| "
                  + f"{self.power}\t| "
                  + f"{self.energy}\t| "
                  + f"{self.frequency}\t| "
                  + f"{self.power_factor}\t| "
                  + f"{self.has_alarm}\t\t| "
                  + f"{self.alarm_threshold}")
            time.sleep(delay)

    def read(self) -> dict:
        return {
            "voltage": self.voltage,
            "current": self.current,
            "power": self.power,
            "energy": self.energy,
            "frequency": self.frequency,
            "power_factor": self.power_factor,
            "alarm_status": self.has_alarm,
            "alarm_threshold": self.alarm_threshold
        }


#pz = PZEM("/dev/ttyUSB0")
#pz.report()