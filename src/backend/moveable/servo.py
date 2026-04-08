from pathlib import Path
from moveable.pcadevice import PCADevice

import json
import time

BASE_DIR = Path(__file__).resolve().parent.parent.parent


# ServoMotor Inheriting from PCADevice
class ServoMotor(PCADevice):
    """
    A servo motor controller that inherits from PCADevice.

    This class manages servo motor positions for dispensing liquids,
    with predefined active, inactive, and waiting positions.
    """

    def __init__(self, address, channel):
        """
        Initialize the ServoMotor with I2C address and channel.

        Args:
            address: I2C address of the PCA board.
            channel: Channel number (0-15) on the PCA board.
        """
        super().__init__(address, channel)

        with open(BASE_DIR / 'json' / 'settings.json', 'r') as file:
            self.settings = json.load(file)

        # Load movement limits from settings file
        self.pulse_min = 0
        self.pulse_max = 0

        self.pulse_min, self.pulse_max = self.load_pulse_limits()

        # Compute positions
        self.mid_pos = (self.pulse_max + self.pulse_min) // 2
        self.range = self.pulse_max - self.pulse_min
        self.inactive_pos = self.mid_pos + (self.range // 9) + 20
        self.active_pos = self.mid_pos - (self.range // 9) + 55
        self.waiting_pos = self.mid_pos + (self.range // 9) - 90

        self.current_position = 'inactive'


    def load_pulse_limits(self, settings_path='../json/settings.json'):
        """
        Load pulse_min and pulse_max values from the settings JSON file.

        Args:
            settings_path (str): Path to the settings JSON file. Defaults to '../json/settings.json'.

        Returns:
            tuple: A tuple of (pulse_min, pulse_max) values.
        """
        try:
            with open(settings_path, 'r') as file:
                settings = json.load(file)
                self.pulse_min = settings.get('pulse_min', 150)  # Default to 150 if not defined
                self.pulse_max = settings.get('pulse_max', 600)  # Default to 600 if not defined
        except FileNotFoundError:
            print(f"Error: Settings file not found at {settings_path}. Using default values.")
        except json.JSONDecodeError:
            print("Error: Failed to decode settings file. Ensure it is valid JSON.")
        except Exception as e:
            print(f"Unexpected error while loading settings: {e}")

        # Return default values in case of an error
        return 150, 600

    def activate(self):
        """
        Move the servo to the active position for dispensing.
        """
        
        """Move servo to the active position.
        self.pca.set_pwm(self.channel, 0, self.active_pos)
        time.sleep(1)
        """
        self.current_position = 'active'
        print(self.current_position)

    def deactivate(self):
        """
        Move the servo to the inactive position.
        """
        
        """Move servo to the inactive position.
        self.pca.set_pwm(self.channel, 0, self.inactive_pos)
        time.sleep(1)
        """
        self.current_position = 'inactive'
        print(self.current_position)

    def move_to_waiting(self):
        """
        Move the servo to the waiting position.
        """
        
        """Move the servo to a waiting position.
        self.pca.set_pwm(self.channel, 0, self.waiting_pos)
        time.sleep(1)
        """
        self.current_position = 'waiting'
        print(self.current_position)

    def get_status(self):
        """
        Get the current position of the servo.

        Returns:
            dict: A dictionary with the key 'current_position' indicating the servo's state.
        """
        return {'current_position': self.current_position}

    def shutdown(self):
        """
        Shut down the servo by moving to inactive position and turning off the PWM signal.
        """
        
        """Shutdown the servo by moving it to inactive and turning off the PWM signal.
        self.deactivate()  # Ensure the servo is in the inactive position
        self.pca.set_pwm(self.channel, 0, 0)  # Turn off the PWM signal
        """
