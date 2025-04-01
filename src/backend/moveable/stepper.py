import RPi.GPIO as GPIO
import json
import time

class Stepper:
    instance = None
    STEP = None
    DIR = None
    EN = None
    schalterLinksPin = None
    schalterRechtsPin = None
    US_DELAY = None
    US = None
    aktuelle_position = 0

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(Stepper, cls).__new__(cls, *args, **kwargs)
        return cls.instance

    def __init__(self):
        if not hasattr(self, "initialized"):
            self.initialized = True
            print("stepper initialized")

        self.load_from_dict(json.load(open("../json/settings.json")))
        self.gpio_init()

    @classmethod
    def load_from_dict(cls, data):
        cls.STEP = data.get("STEP")
        cls.DIR = data.get("DIR")
        cls.EN = data.get("EN")
        cls.schalterLinksPin = data.get("schalterLinksPin")
        cls.schalterRechtsPin = data.get("schalterRechtsPin")
        cls.US_DELAY = data.get("US_DELAY")
        cls.US = data.get("US")

    #TODO Define GPIO Pins
    def gpio_init(self):
        # Configure GPIO settings
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.STEP, GPIO.OUT)
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.EN, GPIO.OUT)
        GPIO.setup(self.schalterLinksPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.schalterRechtsPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.output(self.EN, GPIO.LOW)

    def move_step(self, direction):
        """Move the motor one step in the specified direction (GPIO.HIGH or GPIO.LOW)."""
        GPIO.output(self.DIR, direction)
        GPIO.output(self.STEP, GPIO.HIGH)
        time.sleep(self.US * self.US_DELAY)  # Pulse HIGH
        GPIO.output(self.STEP, GPIO.LOW)
        time.sleep(self.US * self.US_DELAY)  # Pulse LOW
        # Update current position
        if direction == GPIO.HIGH:
            self.aktuelle_position += 1
        else:
            self.aktuelle_position -= 1

    def move_rel_pos(self, relative_steps):
        """Move motor by a relative number of steps (+ve for right, -ve for left)."""
        direction = GPIO.HIGH if relative_steps > 0 else GPIO.LOW
        for _ in range(abs(relative_steps)):
            # Check limit switches
            if direction == GPIO.HIGH and self.get_schalter_rechts_status():
                print("Right limit reached. Stopping.")
                break
            if direction == GPIO.LOW and self.get_schalter_links_status():
                print("Left limit reached. Stopping.")
                break
            self.move_step(direction)

    def move_to_position(self, target_position):
        """Move motor to an absolute position."""
        relative_steps = target_position - self.aktuelle_position
        self.move_rel_pos(relative_steps)

    def get_current_position(self):
        """Return the current stepper position."""
        return self.aktuelle_position

    # Limit switches
    def get_schalter_links_status(self):
        """Check status of the left limit switch."""
        return GPIO.input(self.schalterLinksPin) == GPIO.LOW

    def get_schalter_rechts_status(self):
        """Check status of the right limit switch."""
        return GPIO.input(self.schalterRechtsPin) == GPIO.LOW

    def get_status(self):
        """Return current stepper status."""
        return {
            "current_position": self.aktuelle_position,
            "limit_reached_left": self.get_schalter_links_status(),
            "limit_reached_right": self.get_schalter_rechts_status()
        }

    def shutdown(self):
        """Clean up GPIO and shutdown stepper."""
        GPIO.cleanup()
        print("Stepper shutdown")

