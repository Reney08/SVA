import RPi.GPIO as GPIO
import time
from fileHandler import FileHandler
from logger import setup_logger


class StepperMotor:
    def __init__(self):
        # Initialize the StepperMotor with logger, GPIO configuration, and file handlers
        self.logger = setup_logger()
        self.settingsFileHandler = FileHandler('./json/settings.json')
        self.settings = self.settingsFileHandler.readJson()

        # Load GPIO configurations
        self.STEP = self.settings.get('STEP')
        self.DIR = self.settings.get('DIR')
        self.EN = self.settings.get('EN')
        self.schalterLinksPin = self.settings.get('schalterLinksPin')
        self.schalterRechtsPin = self.settings.get('schalterRechtsPin')
        self.us_delay = self.settings.get('us_delay', 950)  # Default microsecond delay
        self.uS = self.settings.get('uS', 0.000001)  # Microsecond in seconds

        # Load positions from positions.json
        self.positionsFileHandler = FileHandler('./json/positions.json')
        self.positions = self.positionsFileHandler.readJson()

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
        self.logger.info("Stepper motor GPIO configured.")

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
        self.logger.info(f"Stepper motor moved to position: {self.aktuellePos}")

    def move_to_named_position(self, position_name):
        """
        Move the stepper motor to a named position from positions.json.
        Args:
            position_name (str): The name of the position (e.g., "Pos1", "Pumps").
        """
        if position_name in self.positions:
            target_steps = self.positions[position_name]["steps"]
            self.move_to_position(target_steps)
            self.logger.info(f"Stepper motor moved to named position '{position_name}' at steps: {target_steps}")
        else:
            self.logger.warning(f"Position '{position_name}' not found in positions.json.")

    def load_positions(self):
        """
        Reload positions from the JSON file.
        """
        self.positions = self.positionsFileHandler.readJson()
        self.nullPos = self.positions['nullPos']['steps']
        self.maxPos = self.positions['maxPos']['steps']
        self.defaultPos = self.positions['standardPos']['steps']
        self.logger.info("Positions reloaded from positions.json.")

    def save_positions(self):
        """
        Save the current positions to the JSON file.
        """
        self.positionsFileHandler.writeJson(self.positions)
        self.logger.info("Positions saved to positions.json.")

    def edit_position(self, position_name, new_steps):
        """
        Edit the step count for an existing position and update its value.
        Args:
            position_name (str): The name of the position to update.
            new_steps (int): The new step position value.
        """
        if position_name in self.positions:
            self.positions[position_name]["steps"] = new_steps
            self.save_positions()
            self.logger.info(f"Updated position '{position_name}' to new steps: {new_steps}.")
        else:
            self.logger.warning(f"Position '{position_name}' does not exist. Cannot update.")

    def delete_position(self, position_name):
        """
        Delete a position from the positions list.
        Args:
            position_name (str): The name of the position to delete.
        """
        if position_name in self.positions and position_name not in ['nullPos', 'maxPos', 'standardPos']:
            del self.positions[position_name]
            self.save_positions()
            self.logger.info(f"Position '{position_name}' deleted.")
        else:
            self.logger.warning(f"Cannot delete position '{position_name}'. Reserved or does not exist.")

    def shutdown(self):
        """
        Clean up GPIO resources.
        """
        GPIO.cleanup()
        self.logger.info("Stepper motor GPIO cleaned up.")
