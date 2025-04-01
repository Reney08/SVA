def process_mixing_sequence(sequence):
    """
    Processes a mixing sequence step-by-step, extracting key variables for pumps and servos.

    :param sequence: List of steps in the mixing sequence.
    """
    for step_index, step in enumerate(sequence, start=1):
        # Extract and store variables for the current step.
        step_number = step_index  # Step number (position in sequence)
        step_type = step["type"]  # Type of the step: "pump" or "servo"
        action = step["action"]  # Action being performed (e.g., "dispense")

        # Access data nested in the 'details' key
        step_details = step.get("details", {})
        liquid = step_details.get("liquid", None)  # Name of the liquid, if available
        amount_ml = step_details.get("amount", None)  # Amount to dispense, if available

        # Extract variables based on the step type (pump/servo)
        if step_type == "pump":
            pwm_channel = step_details.get("pwm_channel", None)  # PWM channel for pump
            weight_target = step_details.get("weight_target", None)  # Target weight (in ml or grams)
            wait_time = None  # No wait time for pump (it's controlled by weight)

            # Print or store extracted variables as needed
            print(f"Step: {step_number}, Type: Pump, Liquid: {liquid}, PWM Channel: {pwm_channel}, "
                  f"Weight Target: {weight_target}")

        elif step_type == "servo":
            pwm_channel = None  # No pwm_channel for servos
            weight_target = None  # No weight target for servos
            wait_time = step.get("time_delay", None)  # Time delay for servo actions

            # Print or store extracted variables as needed
            print(f"Step: {step_number}, Type: Servo, Liquid: {liquid}, Wait Time: {wait_time}")

        else:
            # Handle unknown step types gracefully
            raise ValueError(f"Unexpected step type: {step_type}")


def get_step_number(step):
    """
    Retrieves the step number from the provided step dictionary.
    Args:
        step (dict): A dictionary containing details of a step, including the "step_number" key.

    Returns:
        int: The step number indicating the sequence/order of the step.
    """
    return step["step_number"]


def get_step_action(step):
    """
    Retrieves the action to be performed in the given step.
    Args:
        step (dict): A dictionary containing details of a step, including the "action" key.
    Returns:
        str: The action indicating the operation to perform (e.g., "mix", "fill").
    """
    return step["action"]


def get_liquid(step):
    """
    Retrieves the liquid type associated with the given step.
    Args:
        step (dict): A dictionary containing details of a step, with the "liquid" key located in "details".
    Returns:
        str: The name or identifier of the liquid.
    """
    return step["details"]["liquid"]


def get_amount(step):
    """
    Retrieves the amount of liquid or material required for the step.
    Args:
        step (dict): A dictionary containing details of a step, with the "amount" key located in "details".
    Returns:
        int or float: The required amount of liquid or material for the step.
    """
    return step["details"]["amount"]


def get_weight_target(step):
    """
    Retrieves the weight target for the given step.
    Args:
        step (dict): A dictionary containing details of a step, with the "weight_target" key located in "details".
    Returns:
        float: The target weight for the step.
    """
    return step["details"]["weight_target"]


def get_pwm_channel(step):
    """
    Retrieves the PWM channel required for the step.
    Args:
        step (dict): A dictionary containing details of a step, with the "pwm_channel" key located in "details".
    Returns:
        int: The PWM channel number to be used for the step.
    """
    return step["details"]["pwm_channel"]


def get_time_delay(step):
    """
    Retrieves the time delay specified for the step.
    Args:
        step (dict): A dictionary containing details of a step, with a "time_delay" key.
    Returns:
        float: The time delay (in seconds or another unit) for the step.
    """
    return step["time_delay"]

