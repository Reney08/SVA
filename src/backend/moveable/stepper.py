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

        self.load_from_dict(json.load(open("./json/settings.json")))
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

    # Limit switches
    def get_schalter_links_status(self):
        """Check status of the left limit switch."""
        print(f"Schalter Links: {GPIO.input(self.schalterLinksPin)}")
        return GPIO.input(self.schalterLinksPin) == GPIO.HIGH

    def get_schalter_rechts_status(self):
        """Check status of the right limit switch."""
        print(f"Schalter Rechts: {GPIO.input(self.schalterRechtsPin)}")
        return GPIO.input(self.schalterRechtsPin) == GPIO.LOW

    def shutdown(self):
        """Clean up GPIO and shutdown stepper."""
        GPIO.cleanup()
        print("Stepper shutdown")

