import time
import neopixel
import board

class TestAddressableRGBLEDs:
    def __init__(self, pin, num_leds=30, brightness=0.5):
        # Initialization (unchanged)
        self.num_leds = num_leds
        self.num_leds_per_row = num_leds // 2
        self.brightness = brightness

        # NeoPixel-Objekt initialization
        self.pixels = neopixel.NeoPixel(
            pin,
            num_leds,
            auto_write=False,
            brightness=brightness,
            pixel_order=neopixel.GRB
        )

    def get_position_by_steps(self, steps):
        """
        Get a position's LED range based on the step value.
        """
        # Basic example: Map steps to LED segments
        if steps < 100:  # Example condition
            return "Pos1"  # Can add functionality for "step-to-LED" mapping
        elif steps < 200:
            return "Pos2"
        elif steps < 300:
            return "Pos3"
        else:
            return "No Position"

    def light_up_based_on_steps(self, steps, color=(255, 0, 0)):
        """
        Light up specific LEDs based on 'steps'.
        """
        position = self.get_position_by_steps(steps)

        # Map position (e.g., "Pos1") to specific LEDs to light
        if position == "Pos1":
            start, end = 0, 10  # Example range of LEDs for Pos1
        elif position == "Pos2":
            start, end = 10, 20  # Range for Pos2
        elif position == "Pos3":
            start, end = 20, 30  # Range for Pos3
        else:
            print(f"No LEDs to light for steps: {steps}")
            return

        # Light up LEDs in the range with the given color
        print(f"Lighting up LEDs {start}-{end - 1} for {position} based on steps: {steps}")
        for i in range(start, end):
            self.pixels[i] = color
        self.pixels.show()

    def clear(self):
        """
        Turn off all LEDs.
        """
        self.pixels.fill((0, 0, 0))
        self.pixels.show()
        print("LEDs cleared.")


if __name__ == "__main__":
    TEST_PIN = board.D18  # GPIO 18
    TEST_NUM_LEDS = 150  # Example: 150 LEDs on the strip
    TEST_BRIGHTNESS = 0.5  # Default brightness (0.0 - 1.0)

    leds = TestAddressableRGBLEDs(TEST_PIN, TEST_NUM_LEDS, TEST_BRIGHTNESS)

    print("Testing LEDs based on step values.")
    while True:
        try:
            # Step value input from user
            step_input = int(input("Enter step value (or -1 to quit): "))
            if step_input == -1:
                break

            # Light up LEDs based on step value
            leds.light_up_based_on_steps(step_input, color=(0, 255, 0))  # Green color
        except ValueError:
            print("Invalid input. Please enter a valid step number.")

    leds.clear()
