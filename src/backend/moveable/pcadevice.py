from abc import ABC, abstractmethod
# from Adafruit_PCA9685 import PCA9685
# Abstract Parent Class for PCA Devices
class PCADevice(ABC):
    """
    Abstract base class for devices controlled via PCA9685 PWM controller.

    This class provides a common interface for PCA-based devices,
    requiring subclasses to implement activate and deactivate methods.
    """

    def __init__(self, address, channel):
        """
        Initialize the PCA device with I2C address and channel.

        Args:
            address: I2C address of the PCA board (e.g., 0x40, 0x41).
            channel: Channel number on the PCA (0-15).
        """
        # self.pca = PCA9685(address=address, busnum=0)  # Initialize PCA9685 at given address
        # self.pca.set_pwm_freq(60)  # Set frequency
        self.channel = channel

    @abstractmethod
    def activate(self):
        """
        Activate the device.

        This method must be implemented by subclasses to perform device-specific activation.
        """
        pass

    @abstractmethod
    def deactivate(self):
        """
        Deactivate the device.

        This method must be implemented by subclasses to perform device-specific deactivation.
        """
        pass
