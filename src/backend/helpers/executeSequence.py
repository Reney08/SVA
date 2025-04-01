from ..moveable import leds
'''
from .moveable import pump
from .moveable import scale
from .moveable import servo
from .moveable import stepper

'''
# import sequenceHelper
import json
import time

class ExecuteSequence:

    def __init__(self, sequence):
        self.exec_sequence = sequence
        self.positions = self.load_position()
        self.led_controller = leds.LEDController()

    def execute_sequence(self, exec_sequence):
        for step in exec_sequence:
            if step['type'] == 'pump':
                pump_position = self.get_pump_position(self.positions)
                self.led_controller.activate_leds_by_step(pump_position, (255, 0, 0))
                print("moving Stepper to pump position")
                print(f"Pump Position: {pump_position}")
            elif step['type'] == 'servo':
                liquid_position = self.get_position_for_liquid(self.positions, step['details']['liquid'])
                self.led_controller.activate_leds_by_step(liquid_position, (255, 0, 0))
                print("moving Stepper to servo position")
                print(f"Liquid '{step['details']['liquid']}' is stored at position {liquid_position}")
            time.sleep(10)

    def load_position(self):
        """
        Loads the positions JSON file into a dictionary.
        Args:
            filepath (str): Path to the positions.json file.

        Returns:
            dict: Dictionary containing the positions data.
        """
        with open("../json/positions.json", 'r') as file:
            return json.load(file)

    def get_position_for_liquid(self, positions, liquid):
        """
        Retrieves the position (steps) assigned to the specified liquid.

        Args:
            positions (dict): Dictionary of positions data from positions.json.
            liquid (str): The name of the liquid to find in positions.json.

        Returns:
            int: The number of steps assigned to the liquid in positions.json.
                 Returns None if no matching liquid is found.
        """
        for key, value in positions.items():
            if value.get("liquid") == liquid:
                return value.get("steps", None)
        return None  # Return None if no match is found

    def get_pump_position(self, positions):
        """
        Retrieves the pump position (steps) from positions.json.

        Args:
            positions (dict): Dictionary of positions data.

        Returns:
            dict: The entry for the pump (key: "Pumps").
        """
        return positions.get("Pumps", None)


