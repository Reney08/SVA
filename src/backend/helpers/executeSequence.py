from moveable.leds import LEDController

# from .moveable import pump
# from .moveable import scale
from moveable.pcadevice import PCADevice
from moveable.servo import ServoMotor
from moveable.stepper import Stepper


# import sequenceHelper
import json
import time
from unittest import case


# from src.backend.moveable import pump


class ExecuteSequence:

    def __init__(self, sequence):
        self.exec_sequence = sequence
        self.positions = self.load_position()
        self.pumps = self.load_pumps()
        print(self.positions)
        self.stepper = Stepper()
        self.servo = ServoMotor(address=0x41, channel=0)
        self.led_controller = LEDController()

    def execute_sequence(self, exec_sequence):
        # self.stepper.moveToStandartPos()
        self.servo.move_to_waiting()
        for step in exec_sequence:
            if step['type'] == 'pump':
                # Get the step count for the pump's position
                pump_position = self.get_pump_position(self.positions)
                if pump_position is not None:
                    
                    self.led_controller.activate_leds_by_step(self.get_pump_position(self.positions), (0, 255, 0))
                    self.stepper.move_to_position(pump_position)
                    
                    print(f"moving Stepper to pump position {pump_position}")
                    self.stepper.move(pump_position)
                    # Get the PWM channel for the liquid from pumps.json
                    liquid = step['details']['liquid']
                    pwm_channel = self.get_pump_pwm_channel(self.pumps, liquid)
                    if pwm_channel is not None:
                        # self.decide_pump(pwm_channel)
                        print(f"The liquid '{liquid}' is dispensed from pump with PWM channel: {pwm_channel}")
                        time.sleep(10)
                    else:
                        print(f"No pump found storing the liquid: {liquid}")
                else:
                    print("No valid pump position found!")

            elif step['type'] == 'servo':
                liquid_position = self.get_position_for_liquid(self.positions, step['details']['liquid'])
                if liquid_position is not None:
                    
                    self.led_controller.activate_leds_by_step(liquid_position, (0, 255, 0))
                    self.stepper.move_to_position(liquid_position)
                    
                    print(f"moving Stepper to liquid position {liquid_position} for servo")
                    self.stepper.move(liquid_position)
                    self.servo.activate()
                    print("activate LEDs blue")
                    time.sleep(5)
                    self.servo.deactivate()
                    print("deactivate LEDs blue")
                    # print(f"Liquid '{step['details']['liquid']}' is stored at position {liquid_position}")
                else:
                    print("No valid liquid position found!")

                print(f"Liquid '{step['details']['liquid']}' is stored at position {liquid_position}")

            # self.led_controller.deactivate_all_leds()
        self.stepper.moveToStandartPos()

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

    def load_pumps(self):
        """
        Loads the pumps JSON file into a dictionary.

        Returns:
            dict: Dictionary containing the pumps data.
        """
        with open("../json/pumps.json", 'r') as file:
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
        return positions.get("Pumps", {}).get("steps", None)
    
    def decide_pump(self, channel):
        match channel:
            case 0:
                self.led_controller.activate_leds_by_step(self.get_pump_position(self.positions),
                                                           (255, 0, 0))
                print("activate LEDs red")
            case 1:
                self.led_controller.activate_leds_by_step(self.get_pump_position(self.positions),
                                                           (0, 255, 0))
                print("activate LEDs green")
            case 2:
                self.led_controller.activate_leds_by_step(self.get_pump_position(self.positions),
                                                           (0, 0, 255))
                print("activate LEDs blue")
            case 3:
                self.led_controller.activate_leds_by_step(self.get_pump_position(self.positions),
                                                           (255, 255, 0))
                print("activate LEDs yellow")
            case 4:
                self.led_controller.activate_leds_by_step(self.get_pump_position(self.positions),
                                                           (255, 0, 255))
                print("activate LEDs magenta")
            case 5:
                self.led_controller.activate_leds_by_step(self.get_pump_position(self.positions),
                                                           (0, 255, 255))
                print("activate LEDs cyan")
            case 6:
                self.led_controller.activate_leds_by_step(self.get_pump_position(self.positions),
                                                           (255, 255, 255))
                print("activate LEDs white")
    

    def get_pump_pwm_channel(self, pumps, liquid):
        """
        Retrieves the PWM channel for the pump storing the given liquid.

        Args:
            pumps (dict): Dictionary of pumps data from pumps.json.
            liquid (str): The liquid to find the corresponding pump for.

        Returns:
            int: The PWM channel associated with the given liquid.
                 Returns None if no match is found.
        """
        for pump, data in pumps.items():
            if data.get("liquid") == liquid:
                return data.get("pwm_channel", None)
        return None  # Return None if no match is found



