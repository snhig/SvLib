from abc import ABC, abstractmethod
from .SvError import SvError
from numpy import ndarray
import cv2
class SvAbstractCamera(ABC):
    """
    Abstract base class for a microscope camera.
    
    This class defines the basic functionalities for both continuous acquisition
    and single frame capture.
    """
    
    
    @abstractmethod
    def initialize(self) -> SvError | None:
        """
        Initializes the camera, setting up necessary configurations.
        
        Implementations might include setting up the connection to the camera,
        configuring initial settings, and preparing the camera for acquisition.
        """
        return SvError("Not implemented", None)
    
    
    @abstractmethod
    def get_image(self) -> SvError | ndarray:
        """
        Gets an image frame from the camera.
        
        This method should return an image frame from the camera. Implementations
        may choose to capture a single frame or return the latest frame from a
        continuous acquisition mode.
        
        Returns:
            An numpy ndarray image frame from the camera.
        """
        return SvError("Not implemented", None)
    
    
    @abstractmethod
    def start_continuous_acquisition(self) -> SvError | None:
        """
        Starts continuous image acquisition.
        
        This method should initiate a continuous acquisition mode, where the camera
        continuously captures images. Implementations may need to consider buffer
        management, frame rate control, and synchronization mechanisms.
        """
        return SvError("Not implemented", None)
    
    
    @abstractmethod
    def stop_continuous_acquisition(self) -> SvError | None:
        """
        Stops continuous image acquisition.
        
        This method is responsible for stopping the continuous acquisition mode
        initiated by start_continuous_acquisition. It may also involve cleaning up
        resources and ensuring that the camera is left in a stable state.
        """
        return SvError("Not implemented", None)
    
    
    @abstractmethod
    def write_image(self, image, filepath) -> SvError | None:
        """
        Saves an image to a specified file path.
        
        Args:
            image: The image frame to save.
            filepath: The file path where the image should be saved.
        """
        try:
            cv2.imwrite(filepath, image)
        except Exception as e:
            return SvError("Failed to save image.", e)
        
        return None
    
    
    @abstractmethod
    def shutdown(self) -> SvError | None:
        """
        Shuts down the camera and cleans up resources.
        
        This method is called to properly close the connection to the camera and
        ensure that all resources are cleaned up properly.
        """
        return SvError("Not implemented", None)
    
    
    @abstractmethod
    def set_gain(self, gain) -> SvError | None:
        """
        Sets the camera gain.
        
        Args:
            gain: The gain value to set.
        """
        return SvError("Not implemented", None)
    
    
    @abstractmethod
    def get_gain(self) -> SvError | float | int:
        """
        Gets the current camera gain.
        
        Returns:
            The current gain value.
        """
        return SvError("Not implemented", None)
    
    
    @abstractmethod
    def set_exposure_time(self, exposure_time) -> SvError | None:
        """
        Sets the camera exposure time.
        
        Args:
            exposure_time: The exposure time in milliseconds.
        """
        return SvError("Not implemented", None)
    
    
    @abstractmethod
    def get_exposure_time(self) -> SvError | float | int:
        """
        Gets the current camera exposure time.
        
        Returns:
            The current exposure time in milliseconds.
        """
        return SvError("Not implemented", None)