import time
import neopixel
import board

from moveable.leds import LEDController

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

    def display_rainbow(self, speed=0.05, direction="left_to_right"):
        """
        Display a rainbow animation on the LED strip.
        """
        try:
            while True:
                for j in range(255):
                    for i in range(self.num_leds_per_row):
                        pixel_index = ((i if direction == "left_to_right" else (
                                    self.num_leds_per_row - 1 - i)) * 256 // self.num_leds_per_row) + j
                        color = self._color_wheel(pixel_index & 255)
                        self.pixels[self.num_leds_per_row - 1 - i] = color
                        self.pixels[i + self.num_leds_per_row] = color
                    self.pixels.show()
                    time.sleep(speed)
        except KeyboardInterrupt:
            print("\nRainbow animation stopped.")
            self.clear()


    def run_color_loop(self):
        """
        LÃ¤sst den Benutzer eine Farbe auswÃ¤hlen und wendet sie dynamisch auf die LEDs an.
        Die Schleife lÃ¤uft, bis der Benutzer `Ctrl + C` drÃ¼ckt.
        """
        print("DrÃ¼cke Strg+C, um das Programm zu beenden.")
        print("Gib die neue Farbe als RGB-Werte (z. B. '255 0 0' fÃ¼r Rot) ein.")

        try:
            while True:
                user_input = input("Neue Farbe (RGB-Werte): ")
                try:
                    r, g, b = map(int, user_input.split())
                    if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                        self.set_color(r, g, b)
                        self.pixels.show()
                        print(f"Neue Farbe auf R:{r}, G:{g}, B:{b} gesetzt.")
                    else:
                        print("RGB-Werte mÃ¼ssen zwischen 0 und 255 liegen.")
                except ValueError:
                    print("UngÃ¼ltige Eingabe. Bitte gib drei Zahlen ein, getrennt durch Leerzeichen.")
        except KeyboardInterrupt:
            print("\nProgramm beendet. LEDs werden ausgeschaltet.")
            self.clear()

    def _color_wheel(self, pos):
        """
        Generate a color from a rainbow wheel.
        """
        if pos < 85:
            return int(pos * 3), int(255 - (pos * 3)), 0
        elif pos < 170:
            pos -= 85
            return int(255 - (pos * 3)), 0, int(pos * 3)
        else:
            pos -= 170
            return 0, int(pos * 3), int(255 - (pos * 3))


if __name__ == "__main__":
    # Configure GPIO Pin and LED parameters
    TEST_PIN = board.D18  # GPIO 18
    TEST_NUM_LEDS = 150
    TEST_BRIGHTNESS = 0.5

    # Initialize Objects for Both Controllers
    test_leds = TestAddressableRGBLEDs(TEST_PIN, TEST_NUM_LEDS, TEST_BRIGHTNESS)
    leds_controller = LEDController()  # Assuming it uses its own default settings

    print("Test program started.")
    print("Choose an option:")
    print("1. TestAddressableRGBLEDs - Display Rainbow")
    print("2. TestAddressableRGBLEDs - Clear LEDs")
    print("3. LEDController (from leds.py) - Activate LEDs by steps")
    print("4. LEDController (from leds.py) - Clear LEDs")
    print("0. Exit")

    while True:
        try:
            choice = int(input("Please choose an option: "))
            if choice == 1:
                test_leds.display_rainbow(direction="left_to_right")
            elif choice == 2:
                test_leds.clear()
            elif choice == 3:
                # Ask for steps and activate LEDs using LEDController
                try:
                    steps = int(input("Enter step value: "))
                    leds_controller.activate_leds_by_steps(steps)
                except ValueError:
                    print("Invalid step value. Please enter a number.")
            elif choice == 4:
                # Clear LEDs using the LEDController
                try:
                    test_leds.clear()
                except AttributeError:
                    print("The `clear` method is not defined in the `LEDController`. Please implement it.")
            elif choice == 5:
                test_leds.run_color_loop()
            elif choice == 6:
                # Activate LEDs based on step-to-position mapping (new feature)
                try:
                    steps = int(input("Enter step value to determine position: "))
                    position = leds_controller.get_position_by_steps(steps)

                    if position:
                        print(f"Position mapped to steps {steps}: {position}")
                        # Activate LEDs for the determined position
                        leds_controller.activate_leds(position)
                    else:
                        print(f"No position found for steps {steps}.")

                except ValueError:
                    print("Invalid input. Please enter a valid number for steps.")

            elif choice == 0:
                print("Exiting program.")
                test_leds.clear()
                break
            else:
                print("Invalid input. Please try again!")
        except ValueError:
            print("Please enter a valid number.")
