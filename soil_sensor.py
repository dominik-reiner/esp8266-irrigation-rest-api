from machine import ADC


class SoilMoisture:
    def __init__(self):
        # The ESP8266 has a single ADC pin, A0, which is referenced as ADC(0).
        self.adc = ADC(0)
        self.ready = True

        # Calibration values for ESP8266's 10-bit ADC (0-1024).
        # Max value is dry soil, Min value is wet soil.
        # You may need to adjust these based on your specific sensor and calibration.
        self.dry_value = 305
        self.wet_value = 235

    def read_raw(self):
        if not self.ready:
            return None
        return self.adc.read()

    def read_percent(self):
        if not self.ready:
            return None

        raw_value = self.read_raw()
        if raw_value is None:
            return None

        # Linear mapping from raw ADC value to a percentage.
        # The raw value is inverted: higher value = drier, lower value = wetter.
        clamped_value = max(self.wet_value, min(self.dry_value, raw_value))

        moisture_range = self.dry_value - self.wet_value
        moisture_level = clamped_value - self.wet_value

        moisture_percent = 100 - (moisture_level / moisture_range) * 100
        return max(0, min(100, moisture_percent))
