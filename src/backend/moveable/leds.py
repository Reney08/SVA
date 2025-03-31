import json
import neopixel
import board
from ..dictionarys.led_mapping import led_mapping


class LEDController:
    def __init__(self, pin=board.D18, num_leds=150, brightness=0.5, position_file="../json/positions.json"):
        """
        Initialize the LED controller using NeoPixel and load position/step mappings.

        :param pin: GPIO pin controlling the LED strip (default: GPIO18).
        :param num_leds: Total number of LEDs in the strip.
        :param brightness: Brightness value for the LEDs (0.0 to 1.0).
        :param position_file: JSON file containing position definitions.
        """
        self.pixels = neopixel.NeoPixel(
            pin,
            num_leds,
            auto_write=False,
            brightness=brightness,
            pixel_order=neopixel.GRB  # Modify if necessary for different strips
        )
        self.led_mapping = led_mapping  # LED-to-position mapping from `led_mapping.py`
        self.positions = self.load_positions(position_file)  # Load step mappings from JSON

    def load_positions(self, position_file):
        """
        Load positions (steps, liquid names, etc.) from a JSON file.
        :param position_file: The path to the JSON file.
        :return: A dictionary with position data.
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
        Get the position name that corresponds to the given step value.
        :param steps: The step value to map.
        :return: A position name (e.g., "Pos1").
        """
        for position, details in self.positions.items():
            if details.get("steps") == steps:
                return position
        return None  # No matching position found

    def activate_leds_for_position(self, position, color):
        """
        Activate LEDs corresponding to a specific position (e.g., "Pos1").
        :param position: The position to activate (e.g., "Pos1", "Pos2").
        :param color: A tuple representing the RGB color (R, G, B).
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
        Activate LEDs based on step value by first determining the position.
        :param steps: The step value.
        :param color: A tuple representing the RGB color (R, G, B).
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

    def activate_leds_by_position(self, position):
        """
        Activate LEDs corresponding to a specific position (e.g., "Pos1").
        Uses `positions.json` for validation and `led_mapping` for LED indices.

        :param position: The position to activate (e.g., "Pos1", "Pos2").
        """
        if position in self.positions:
            # Check if position exists in led_mapping
            if position in self.led_mapping:
                top_row = self.led_mapping[position]["top-row"]
                bottom_row = self.led_mapping[position]["bottom-row"]

                # Set LEDs for both rows to a default color (e.g., blue)
                default_color = (0, 0, 255)  # Default to blue unless changed
                for led in top_row + bottom_row:
                    self.pixels[led] = default_color

                self.pixels.show()
                print(f"Activated LEDs for {position} (Liquid: {self.positions[position]['liquid']}).")
            else:
                print(f"No LED mapping defined for position: {position}.")
        else:
            print(f"Invalid position: {position}. Please choose a valid position.")
