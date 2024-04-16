from abc import ABC, abstractmethod
from .SvError import SvError
class SvMotor(ABC):
    """
    Abstract base class for a servo motor.
    
    This class defines the essential functionalities for controlling a servo motor,
    including initialization, position control, and shutdown procedures.
    """
    
    
    @abstractmethod
    def initialize(self) -> SvError | None:
        """
        Initializes the servo motor, setting up necessary configurations.
        
        Implementations might include establishing a connection to the motor's
        controller, configuring initial parameters, and performing self-tests
        to ensure readiness for operation.
        """
        return SvError("Not implemented", None)
    
    
    @abstractmethod
    def set_position(self, position) -> SvError | None:
        """
        Sets the servo motor's position.
        
        Args:
            position: The target position for the servo motor. The specific unit
                      and range depend on the servo motor's specifications (e.g.,
                      degrees, radians, or steps).
        """
        return SvError("Not implemented", None)
    
    
    
    @abstractmethod
    def get_position(self) -> SvError | float | int:
        """
        Gets the current position of the servo motor.
        
        Returns:
            The current position of the servo motor. The unit and range of the
            return value depend on the servo motor's specifications.
        """
        return SvError("Not implemented", None)
    
    
    @abstractmethod
    def set_velocity(self, velocity) -> SvError | None:
        """
        Sets the servo motor's velocity.
        
        Args:
            velocity: The target velocity for the servo motor. The specific unit
                      and range depend on the servo motor's specifications.
        """
        return SvError("Not implemented", None)
    
    
    @abstractmethod
    def get_velocity(self) -> SvError | float | int:
        """
        Gets the current velocity of the servo motor.
        
        Returns:
            The current velocity of the servo motor. The unit and range of the
            return value depend on the servo motor's specifications.
        """
        return SvError("Not implemented", None)
    
    
    @abstractmethod
    def shutdown(self) -> SvError | None:
        """
        Safely shuts down the servo motor.
        
        This method ensures that the servo motor is powered down safely,
        optionally bringing it to a neutral position and ensuring that all
        resources are released properly.
        """
        return SvError("Not implemented", None)
    
    @abstractmethod
    def home(self) -> SvError | None:
        """
        Moves the servo motor to a known reference position.
        
        This method moves the servo motor to a predefined reference position,
        which is typically a "home" position or a zero position. The specifics
        of the reference position depend on the servo motor's configuration.
        """
        return SvError("Not implemented", None)
    
    
    

