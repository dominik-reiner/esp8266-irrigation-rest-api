import time


class AHT20:
    def __init__(self, i2c_bus, addr=0x38):
        self.i2c = i2c_bus
        self.addr = addr
        self.t_c = None
        self.hum = None
        try:
            if self.addr not in self.i2c.scan():
                raise OSError("AHT20 not found.")
            self.i2c.writeto(self.addr, b"\xba")  # Soft reset
            time.sleep_ms(20)
            self.i2c.writeto(self.addr, b"\xbe\x08\x00")  # Init command
            time.sleep_ms(20)
        except Exception as e:
            print(f"Error init AHT20: {e}")
            self.i2c = None

    def read_values(self):
        if self.i2c is None:
            return None, None
        try:
            self.i2c.writeto(self.addr, b"\xac\x33\x00")  # Measure command
            time.sleep_ms(80)
            data = self.i2c.readfrom(self.addr, 6)
            if not (data[0] & 0x80):
                h_raw = ((data[1] << 16) | (data[2] << 8) | data[3]) >> 4
                t_raw = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
                self.hum = (h_raw / 0x100000) * 100.0
                self.t_c = (t_raw / 0x100000) * 200.0 - 50.0
                return self.t_c, self.hum
            else:
                print("AHT20 busy.")
                return None, None
        except Exception as e:
            print(f"Error read AHT20: {e}")
            return None, None
