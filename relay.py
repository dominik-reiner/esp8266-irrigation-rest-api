import time
from machine import Pin


class Relay:
    """
    A MicroPython class to control a relay module.

    This class provides methods to initialize a relay connected to a
    specific GPIO pin and control its state (on/off).

    Attributes:
        pin_number (int): The GPIO pin number to which the relay is connected.
        relay_pin (machine.Pin): The Pin object representing the relay's GPIO.
        # Note: Relays often operate in a 'normally open' (NO) or
        # 'normally closed' (NC) configuration.
        # For most common relay modules, a LOW signal (0V) activates the relay,
        # and a HIGH signal (3.3V/5V) deactivates it.
        # This class assumes an active-low relay, meaning setting the pin to 0
        # turns the relay ON, and setting it to 1 turns it OFF.
        # If your relay is active-high, simply swap the 0 and 1 in the on() and off() methods.
    """

    def __init__(self, pin_number):
        """
        Initializes the Relay object.

        Args:
            pin_number (int): The GPIO pin number where the relay is connected.
                For ESP32, this would be a number like 2, 4, 16, etc.
        """
        self.pin_number = pin_number
        self.relay_pin = Pin(self.pin_number, Pin.OUT, value=1)

    def on(self):
        """
        Turns the relay ON.
        Then turns it off after 5 seconds.
        For active-low relays, this means setting the pin to LOW (0).
        """
        self.relay_pin.value(0)  # Set pin to (LOW)
        time.sleep(5)
        self.relay_pin.value(1)  # Set pin to (HIGH) to turn off the relay

    def get_state(self):
        """
        Returns the current electrical state of the relay pin (0 or 1).
        Note: For active-low relays, 0 means ON, 1 means OFF.

        Returns:
            int: The current value of the GPIO pin (0 or 1).
        """
        state = self.relay_pin.value()
        return state
