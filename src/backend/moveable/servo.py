from moveable.pcadevice import PCADevice

import json
import time


# ServoMotor Inheriting from PCADevice
class ServoMotor(PCADevice):
    def __init__(self, address, channel):
        """
        Servo motor controlled via PCA9685.
        :param address: I2C address of PCA board
        :param channel: Channel number (0-15)
        """
        super().__init__(address, channel)

        with open('../json/settings.json', 'r') as file:
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
        If the file or the required fields are missing, default values are used.
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
        """Move servo to the active position.
        self.pca.set_pwm(self.channel, 0, self.active_pos)
        time.sleep(1)
        """
        self.current_position = 'active'
        print(self.current_position)

    def deactivate(self):
        """Move servo to the inactive position.
        self.pca.set_pwm(self.channel, 0, self.inactive_pos)
        time.sleep(1)
        """
        self.current_position = 'inactive'
        print(self.current_position)

    def move_to_waiting(self):
        """Move the servo to a waiting position.
        self.pca.set_pwm(self.channel, 0, self.waiting_pos)
        time.sleep(1)
        """
        self.current_position = 'waiting'
        print(self.current_position)

    def get_status(self):
        """Return the current position of the servo."""
        return {'current_position': self.current_position}

    def shutdown(self):
        """Shutdown the servo by moving it to inactive and turning off the PWM signal.
        self.deactivate()  # Ensure the servo is in the inactive position
        self.pca.set_pwm(self.channel, 0, 0)  # Turn off the PWM signal
        """
