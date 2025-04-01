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
        GPIO.output(self.EN, GPIO.LOW)
        GPIO.output(self.DIR, GPIO.LOW)
        GPIO.setup(self.schalterLinksPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.schalterRechtsPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # Enable the stepper motor

    def getSchalterRechtsStatus(self):
        # Check the status of the right limit switch
        return GPIO.input(self.schalterRechtsPin) == 1

    def getSchalterLinksStatus(self):
        # Check the status of the left limit switch
        return GPIO.input(self.schalterLinksPin) == 1

    def moveRelPos(self, relative_steps):
        """ Bewegt den Stepper-Motor um eine relative Anzahl an Schritten. """
        if relative_steps == 0:
            print("Motor ist bereits an der gewünschten Position.")
            return

        # Richtung setzen
        direction = GPIO.HIGH if relative_steps > 0 else GPIO.LOW
        absolute_steps = abs(relative_steps)
        GPIO.output(self.DIR, direction)

        for _ in range(absolute_steps):
            # Grenzüberprüfung vor der Bewegung
            if (direction == GPIO.HIGH and self.aktuellePos >= self.maxPos) or \
                    (direction == GPIO.LOW and self.aktuellePos <= self.nullPos):
                print("⚠️ Grenze erreicht! Motor stoppt.")
                break  # Stoppe die Bewegung

            GPIO.output(self.STEP, GPIO.HIGH)
            time.sleep(self.uS * self.us_delay)
            GPIO.output(self.STEP, GPIO.LOW)
            time.sleep(self.uS * self.us_delay)

            # Position aktualisieren
            self.aktuellePos += 1 if direction == GPIO.HIGH else -1

    def move_to_position(self, target_steps):
        """ Bewegt den Stepper-Motor zu einer absoluten Position. """
        if target_steps == self.aktuellePos:
            print("Motor ist bereits an der gewünschten Position.")
            return

        relative_steps = target_steps - self.aktuellePos
        self.moveRelPos(relative_steps)
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

    def quick_init(self):
        self.move_to_left_limit()
        # Explicitly reset position tracking
        self.aktuellePos = 0
        self.nullPos = 0
        time.sleep(1)

        # Ensure direction is set correctly before moving right
        GPIO.output(self.DIR, GPIO.LOW)
        self.move_to_position(self.defaultPos)
        self.aktuellePos = self.defaultPos

    def move_to_left_limit(self):
        """
        Move the stepper motor as far to the left as possible until the left limit switch is triggered.
        """
        GPIO.output(self.DIR, GPIO.LOW)  # Set direction to left (LOW)

        while not GPIO.input(self.schalterLinksPin):  # Check if limit switch is pressed
            GPIO.output(self.STEP, GPIO.HIGH)
            time.sleep(self.uS * self.us_delay)
            GPIO.output(self.STEP, GPIO.LOW)
            time.sleep(self.uS * self.us_delay)

        self.aktuellePos = self.maxPos  # Update limit switch

    def move_to_right_limit(self):
        """
        Move the stepper motor as far to the right as possible until the right limit switch is triggered.
        """
        GPIO.output(self.DIR, GPIO.HIGH)  # Set direction to right (HIGH)

        while not GPIO.input(self.schalterRechtsPin):  # Check if right limit switch is pressed
            GPIO.output(self.STEP, GPIO.HIGH)
            time.sleep(self.uS * self.us_delay)
            GPIO.output(self.STEP, GPIO.LOW)
            time.sleep(self.uS * self.us_delay)

        self.aktuellePos = 0  # Reset current position to zero (since it's at the limit)

    def shutdown(self):
        """
        Clean up GPIO resources.
        """
        GPIO.cleanup()

