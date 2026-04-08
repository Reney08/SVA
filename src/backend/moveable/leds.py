import json
from dictionaries.led_mapping import led_mapping

try:
    import board
    import neopixel

    # Prüfen, ob NeoPixel wirklich existiert
    if not hasattr(neopixel, "NeoPixel"):
        raise ImportError("Invalid neopixel module")

except (ImportError, RuntimeError):
    board = None

    class MockNeoPixel:
        def __init__(self, pin, num_leds, auto_write=False, brightness=1.0, pixel_order=None):
            self.leds = [(0, 0, 0)] * num_leds

        def __setitem__(self, index, value):
            if isinstance(index, int) and 0 <= index < len(self.leds):
                self.leds[index] = value

        def show(self):
            pass

        def fill(self, color):
            self.leds = [color] * len(self.leds)

    class neopixel:
        GRB = None
        NeoPixel = MockNeoPixel

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class LEDController:
    """
    Controller for NeoPixel LED strips used to indicate positions and actions.

    This class manages LED activation based on positions and steps,
    using mappings from led_mapping.py and positions.json.
    """

    def __init__(self, pin=18, num_leds=150, brightness=0.5, position_file=None):
        """
        Initialize the LED controller.

        Args:
            pin (int): GPIO pin controlling the LED strip (default: 18).
            num_leds (int): Total number of LEDs in the strip.
            brightness (float): Brightness value for the LEDs (0.0 to 1.0).
            position_file (str): Path to the JSON file containing position definitions.
        """
        self.pixels = neopixel.NeoPixel(
            pin,
            num_leds,
            auto_write=False,
            brightness=brightness,
            pixel_order=neopixel.GRB  # Modify if necessary for different strips
        )
        self.led_mapping = led_mapping  # LED-to-position mapping from `led_mapping.py`
        # print("LED Mapping Loaded:", self.led_mapping)  # Debug statement to print the mapping

        if position_file is None:
            position_file = str(BASE_DIR / 'json' / 'positions.json')

        self.positions = self.load_positions(position_file)  # Load step mappings from JSON

    def load_positions(self, position_file):
        """
        Load positions from a JSON file.

        Args:
            position_file (str): Path to the JSON file.

        Returns:
            dict: Dictionary with position data, or empty dict on error.
        """
        try:
            with open(position_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Position file '{position_file}' not found. Using empty mapping.")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON from '{position_file}'. Using empty mapping.")
            return {}

    def get_position_by_steps(self, steps):
        """
        Get the position name corresponding to the given step value.

        Args:
            steps (int): The step value to map.

        Returns:
            str or None: Position name (e.g., "Pos1") or None if not found.
        """
        for position, details in self.positions.items():
            if details.get("steps") == steps:
                return position
        return None  # No matching position found


    def activate_leds_for_position(self, position, color):
        """
        Activate LEDs for a specific position.

        Args:
            position (str): Position to activate (e.g., "Pos1").
            color (tuple): RGB color tuple (R, G, B).
        """
        if position in self.led_mapping:
            # Get the list of top-row and bottom-row LEDs for the position
            top_row = self.led_mapping[position]["top-row"]
            bottom_row = self.led_mapping[position]["bottom-row"]

            # Activate LEDs for this position
            for led in top_row + bottom_row:
                self.pixels[led] = color
            self.pixels.show()
            print(f"Activated LEDs for {position} with color {color}.")
        else:
            print(f"No LEDs defined for position: {position}.")

    def activate_leds_by_step(self, steps, color):
        """
        Activate LEDs based on step value.

        Args:
            steps (int): Step value to determine position.
            color (tuple): RGB color tuple (R, G, B).
        """
        position = self.get_position_by_steps(steps)
        if position:
            self.activate_leds_for_position(position, color)
        else:
            print(f"No position found for steps: {steps}.")

    def deactivate_all_leds(self):
        """
        Turn off all LEDs (set them to black).
        """
        self.pixels.fill((0, 0, 0))
        self.pixels.show()
        print("All LEDs turned off.")

    def activate_leds_by_position(self, position, color):
        """
        Activate LEDs for a specific position using mappings.

        Args:
            position (str): Position to activate (e.g., "Pos1").
            color (tuple): RGB color tuple (R, G, B).
        """
        if position in self.positions:
            # Check if position exists in led_mapping
            if position in self.led_mapping:
                top_row = self.led_mapping[position]["top-row"]
                bottom_row = self.led_mapping[position]["bottom-row"]

                # Set LEDs for both rows to a default color (e.g., blue)
                default_color = (0, 0, 255)  # Default to blue unless changed
                # color = default_color
                for led in top_row + bottom_row:
                    self.pixels[led] = color

                self.pixels.show()
                print(f"Activated LEDs for {position} (Liquid: {self.positions[position]['liquid']}).")
            else:
                print(f"No LED mapping defined for position: {position}.")
        else:
            print(f"Invalid position: {position}. Please choose a valid position.")


    def print_led_mapping(self):
        """
        Print the LED-to-position mapping.

        Returns:
            None
        """
        print("LED Mapping:", self.led_mapping)



