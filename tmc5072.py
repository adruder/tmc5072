from dataclasses import dataclass
from spidev import SpiDev
from configparser import ConfigParser

@dataclass
class TrinamicRegister:
    address: int
    value: int
    access: str

class TMC5072:
    def __init__(self, spi_if, spi_cs, config_file = None):
        self.spi_if = spi_if
        self.spi_cs = spi_cs

        # General configuration registers
        self.gconf = TrinamicRegister(0x00, 0x00000200, 'RW')
        self.gstat = TrinamicRegister(0x01, 0x00000000, 'RC')
        self.ifcnt = TrinamicRegister(0x02, 0x00000000, 'R')
        self.nodeconf = TrinamicRegister(0x03, 0x00000000, 'W')
        self.input_output = TrinamicRegister(0x04, 0x00000000, 'RW')
        self.x_compare = TrinamicRegister(0x05, 0x00000000, 'W')

        # Ramp generator registers - Motion Control
        self.rampmode = [
            TrinamicRegister(0x20, 0x00000003, 'RW'),
            TrinamicRegister(0x40, 0x00000003, 'RW')
        ]
        self.xactual = [
            TrinamicRegister(0x21, 0x00000000, 'RW'),
            TrinamicRegister(0x41, 0x00000000, 'RW')
        ]
        self.vactual = [
            TrinamicRegister(0x22, 0x00000000, 'R'),
            TrinamicRegister(0x42, 0x00000000, 'R')
        ]
        self.vstart = [
            TrinamicRegister(0x23, 0x00000000, 'W'),
            TrinamicRegister(0x43, 0x00000000, 'W')
        ]
        self.a1 = [
            TrinamicRegister(0x24, 1000, 'W'),
            TrinamicRegister(0x44, 1000, 'W')
        ]
        self.v1 = [
            TrinamicRegister(0x25, 50000, 'W'),
            TrinamicRegister(0x45, 50000, 'W')
        ]
        self.amax = [
            TrinamicRegister(0x26, 5000, 'W'),
            TrinamicRegister(0x46, 5000, 'W')
        ]
        self.vmax = [
            TrinamicRegister(0x27, 400000, 'W'),
            TrinamicRegister(0x47, 400000, 'W')
        ]
        self.dmax = [
            TrinamicRegister(0x28, 5000, 'W'),
            TrinamicRegister(0x48, 5000, 'W')
        ]
        self.d1 = [
            TrinamicRegister(0x2A, 1000, 'W'),
            TrinamicRegister(0x4A, 1000, 'W')
        ]
        self.vstop = [
            TrinamicRegister(0x2B, 10, 'W'),
            TrinamicRegister(0x4B, 10, 'W')
        ]
        self.tzerowait = [
            TrinamicRegister(0x2C, 0x00000000, 'W'),
            TrinamicRegister(0x4C, 0x00000000, 'W')
        ]
        self.xtarget = [
            TrinamicRegister(0x2D, 0x00000000, 'RW'),
            TrinamicRegister(0x4D, 0x00000000, 'RW')
        ]

        # Ramp Generator - Drive Feature Controls
        self.ihold_irun = [
            TrinamicRegister(0x30, 0x00001F00, 'W'),
            TrinamicRegister(0x50, 0x00001F00, 'W')
        ]
        self.vcoolthrs = [
            TrinamicRegister(0x31, 0x00000000, 'W'),
            TrinamicRegister(0x51, 0x00000000, 'W')
        ]
        self.vhigh = [
            TrinamicRegister(0x32, 0x00000000, 'W'),
            TrinamicRegister(0x52, 0x00000000, 'W')
        ]
        self.vdcmin = [
            TrinamicRegister(0x33, 0x00000000, 'W'),
            TrinamicRegister(0x53, 0x00000000, 'W')
        ]
        self.sw_mode = [
            TrinamicRegister(0x34, 0x00000000, 'RW'),
            TrinamicRegister(0x54, 0x00000000, 'RW')
        ]
        self.ramp_stat = [
            TrinamicRegister(0x35, 0x00000000, 'RC'),
            TrinamicRegister(0x55, 0x00000000, 'RC')
        ]
        self.xlatch = [
            TrinamicRegister(0x36, 0x00000000, 'R'),
            TrinamicRegister(0x56, 0x00000000, 'R')
        ]

        # Encoder Registers
        self.encmode = [
            TrinamicRegister(0x38, 0x00000000, 'RW'),
            TrinamicRegister(0x58, 0x00000000, 'RW')
        ]
        self.x_enc = [
            TrinamicRegister(0x39, 0x00000000, 'RW'),
            TrinamicRegister(0x59, 0x00000000, 'RW')
        ]
        self.enc_const = [
            TrinamicRegister(0x3A, 0x00000000, 'W'),
            TrinamicRegister(0x5A, 0x00000000, 'W')
        ]
        self.enc_status = [
            TrinamicRegister(0x3B, 0x00000000, 'RC'),
            TrinamicRegister(0x5B, 0x00000000, 'RC')
        ]
        self.enc_latch = [
            TrinamicRegister(0x3C, 0x00000000, 'R'),
            TrinamicRegister(0x5C, 0x00000000, 'R')
        ]

        # Microstep Table (ignoring these for now!)

        # Motor Driver Registers
        self.mscnt = [
            TrinamicRegister(0x6A, 0x00000000, 'R'),
            TrinamicRegister(0x7A, 0x00000000, 'R')
        ]
        self.mscuract = [
            TrinamicRegister(0x6B, 0x00000000, 'R'),
            TrinamicRegister(0x7B, 0x00000000, 'R')
        ]
        self.chopconf = [
            TrinamicRegister(0x6C, 0x00010135, 'RW'),
            TrinamicRegister(0x7C, 0x00010135, 'RW')
        ]
        self.coolconf = [
            TrinamicRegister(0x6D, 0x00000000, 'W'),
            TrinamicRegister(0x7D, 0x00000000, 'W')
        ]
        self.dcctrl = [
            TrinamicRegister(0x6E, 0x00000000, 'W'),
            TrinamicRegister(0x7E, 0x00000000, 'W')
        ]
        self.drv_status = [
            TrinamicRegister(0x6F, 0x00000000, 'R'),
            TrinamicRegister(0x7F, 0x00000000, 'R')
        ]

        # Voltage PWM mode StealthChop
        self.pwmconf = [
            TrinamicRegister(0x10, 0x000504C8, 'W'),
            TrinamicRegister(0x18, 0x000504C8, 'W')
        ]
        self.pwm_status = [
            TrinamicRegister(0x11, 0x00000000, 'R'),
            TrinamicRegister(0x19, 0x00000000, 'R')
        ]
        if config_file is None:
            pass
        else:
            self.load_config(config_file)

    def load_config(self, filepath):
        print('loading config...')
        config = ConfigParser()
        config.read(filepath)
        for c in config.sections():
            print(config[c])
            for k in config[c].keys():
                print(k)
                if hasattr(self, k):
                    print(f'Found attribute {k}')
                    temp_attr = getattr(self, k)
                    if type(temp_attr) is list:
                        temp_cfg = config[c][k].strip('[]').split(',')
                        for i in range(2): temp_attr[i].value = int(temp_cfg[i], 0)
                    else:
                        print(config[c][k])
                        temp_attr.value = int(config[c][k], 0)
                    setattr(self, k, temp_attr)
                    print(getattr(self, k))

    def basic_init(self):
        self.write_register(self.gconf)
        for i in range(2):
            self.write_register(self.sw_mode[i])
            self.write_register(self.chopconf[i])
            self.write_register(self.rampmode[i])
            self.write_register(self.xactual[i])
            self.write_register(self.xtarget[i])
            self.write_register(self.ihold_irun[i])
            self.write_register(self.pwmconf[i])
            self.write_register(self.a1[i])
            self.write_register(self.v1[i])
            self.write_register(self.amax[i])
            self.write_register(self.vmax[i])
            self.write_register(self.dmax[i])
            self.write_register(self.d1[i])
            self.write_register(self.vstop[i])

    def goto_position(self, motor_number, microsteps):
        self.xtarget[motor_number].value = microsteps
        self.rampmode[motor_number].value = 0
        self.write_register(self.rampmode[motor_number])
        self.write_register(self.xtarget[motor_number])

    def jog_position(self, motor_number, microsteps):
        temp = self.read_register(self.xactual[motor_number])
        xactual = temp[1] << 24
        xactual |= temp[2] << 16
        xactual |= temp[3] << 8
        xactual |= temp[4]
        new_xtarget = xactual + microsteps
        self.goto_position(motor_number, new_xtarget)

    def get_switch_status(self, motor_number):
        status = self.read_register(self.ramp_stat[motor_number])[-1]
        status &= 0x03
        if status != 0:
            return True
        else:
            return False

    def get_xlatch(self, motor_number):
        xlatch = self.read_register(self.xlatch[motor_number])
        output = xlatch[1] << 24
        output |= xlatch[2] << 16
        output |= xlatch[3] << 8
        output |= xlatch[4]
        if output > 2 ** 31 - 1:
            output -= 2 ** 32
        return output

    def write_register(self, register):
        tx_bytes = [
            register.address | 0x80,
            register.value >> 24 & 0xFF,
            register.value >> 16 & 0xFF,
            register.value >> 8 & 0xFF,
            register.value & 0xFF,
        ]
        with SpiDev() as spi:
            spi.open(self.spi_if, self.spi_cs)
            spi.max_speed_hz = 1000000
            spi.mode = 0b11
            rx_bytes = spi.xfer3(tx_bytes)
        return rx_bytes

    def read_register(self, register):
        tx_bytes = [
            register.address,
            0x00,
            0x00,
            0x00,
            0x00
        ]
        with SpiDev() as spi:
            spi.open(self.spi_if, self.spi_cs)
            spi.max_speed_hz = 1000000
            spi.mode = 0b11
            rx_bytes = spi.xfer3(tx_bytes)
            rx_bytes = spi.xfer3(tx_bytes)
        return rx_bytes
