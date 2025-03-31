# led_controller.py
from dictionaries.led_mapping import led_mapping, steps_to_position  # Import from the separate file


class LEDController:
    def __init__(self):
        # Use the imported mappings
        self.led_mapping = led_mapping
        self.steps_to_position = steps_to_position

    def get_position_by_steps(self, steps):
        """
        Get the position name by step value.
        """
        return self.steps_to_position.get(steps, None)

    def activate_leds(self, position):
        """
        Activate the LEDs for a given position.
        """
        if position in self.led_mapping:
            # Retrieve the LEDs to activate
            top_row_leds = self.led_mapping[position]["top-row"]
            bottom_row_leds = self.led_mapping[position]["bottom-row"]

            # Print or trigger hardware logic (replace with GPIO commands, etc.)
            print(f"Activating top-row LEDs: {top_row_leds}")
            print(f"Activating bottom-row LEDs: {bottom_row_leds}")
        else:
            print(f"No LEDs mapped for position: {position}")

    def activate_leds_by_steps(self, steps):
        """
        Activate LEDs based on the current step value by determining the position.
        """
        position = self.get_position_by_steps(steps)
        if position:
            self.activate_leds(position)
        else:
            print(f"No LEDs mapped for steps: {steps}")


if __name__ == "__main__":
    # Initialize the LED controller
    led_controller = LEDController()

    # Example: Activate LEDs by position
    led_controller.activate_leds("Pos1")

    # Example: Activate LEDs by steps
    led_controller.activate_leds_by_steps(25)

    # Example for invalid steps
    led_controller.activate_leds_by_steps(9999)
