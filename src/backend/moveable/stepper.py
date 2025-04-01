import RPi.GPIO as GPIO
import time
import json


class Stepper:
    def __init__(self):
        # Initialize the StepperMotor with logger, GPIO configuration, and file handlers
        with open('../json/settings.json', 'r') as file:
            self.settings = json.load(file)

        # Load GPIO configurations
        self.STEP = self.settings.get('STEP')
        self.DIR = self.settings.get('DIR')
        self.EN = self.settings.get('EN')
        self.schalterLinksPin = self.settings.get('schalterLinksPin')
        self.schalterRechtsPin = self.settings.get('schalterRechtsPin')
        self.us_delay = self.settings.get('us_delay', 950)  # Default microsecond delay
        self.uS = self.settings.get('uS', 0.000001)  # Microsecond in seconds

        # Load positions from positions.json
        with open('../json/positions.json', 'r') as file:
            self.positions = json.load(file)

        # Initialize position tracking
        self.aktuellePos = 0  # Current position in steps
        self.nullPos = self.positions['nullPos']['steps']  # Steps for null position
        self.maxPos = self.positions['maxPos']['steps']  # Steps for max position
        self.defaultPos = self.positions['standardPos']['steps']  # Standard position steps

        # GPIO setup
        self.GPIOConfig()

    def GPIOConfig(self):
        """Configure GPIO settings for the stepper motor."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.STEP, GPIO.OUT)
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.EN, GPIO.OUT)
        GPIO.output(self.EN, GPIO.LOW)  # Enable the stepper motor

    def moveRelPos(self, relative_steps):
        """
        Move the stepper motor by a relative number of steps.
        Args:
            relative_steps (int): Number of steps to move (positive for forward, negative for backward).
        """
        direction = GPIO.HIGH if relative_steps > 0 else GPIO.LOW
        absolute_steps = abs(relative_steps)
        GPIO.output(self.DIR, direction)

        for _ in range(absolute_steps):
            GPIO.output(self.STEP, GPIO.HIGH)
            time.sleep(self.uS * self.us_delay)
            GPIO.output(self.STEP, GPIO.LOW)
            time.sleep(self.uS * self.us_delay)

        self.aktuellePos += relative_steps  # Update the current position

    def move_to_position(self, target_steps):
        """
        Move the stepper motor to an absolute position.
        Args:
            target_steps (int): The target position in steps.
        """
        relative_steps = target_steps - self.aktuellePos
        self.moveRelPos(relative_steps)
        self.aktuellePos = target_steps

    def move_to_named_position(self, position_name):
        """
        Move the stepper motor to a named position from positions.json.
        Args:
            position_name (str): The name of the position (e.g., "Pos1", "Pumps").
        """
        if position_name in self.positions:
            target_steps = self.positions[position_name]["steps"]
            self.move_to_position(target_steps)

    def load_positions(self):
        """
        Reload positions from the JSON file.
        """
        self.nullPos = self.positions['nullPos']['steps']
        self.maxPos = self.positions['maxPos']['steps']
        self.defaultPos = self.positions['standardPos']['steps']


    def shutdown(self):
        """
        Clean up GPIO resources.
        """
        GPIO.cleanup()

