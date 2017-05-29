'''
Created on Mar 26, 2017

@author: CarstenHøilund
'''

import time
from datetime import datetime

import ctypes as ct
import URplus.pyllt as llt
#from URBasic.dataLogging import Singleton

class Singleton2(type):
    _instances = {}
    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(Singleton2, self).__call__(*args, **kwargs)
        return self._instances[self]

class MicroEpsilonScanControl(metaclass=Singleton2):
    """
    Class for interfacing with the Micro-Epsilon line laser scanner

    Args:
        resolution (int): Set the resolution of the line scanner
    """

    def __init__(self, resolution=640):
        # Parametrize transmission
        self.resolution = resolution
        self.scanner_type = ct.c_int(0)

        # Init profile buffer and timestamp info
        self.profile_buffer = (ct.c_ubyte * (resolution * 64))()
        self.timestamp = (ct.c_ubyte * 16)()
        available_resolutions = (ct.c_uint * 4)()
        available_interfaces = (ct.c_uint * 6)()
        self.lost_profiles = ct.c_int()
        self.shutter_opened = ct.c_double(0.0)
        self.shutter_closed = ct.c_double(0.0)
        self.profile_count = ct.c_uint(0)

        # Declare measuring data array
        self.x = (ct.c_double * resolution)()
        self.z = (ct.c_double * resolution)()
        self.intensities = (ct.c_ushort * resolution)()

        # Null pointer if data not necessary
        self.null_ptr_short = ct.POINTER(ct.c_ushort)()
        self.null_ptr_int = ct.POINTER(ct.c_uint)()

        # Create instance and set IP address
        self.hLLT = llt.CreateLLTDevice(llt.TInterfaceType.INTF_TYPE_ETHERNET)

        # Get available interfaces
        ret = llt.GetDeviceInterfacesFast(
            self.hLLT, available_interfaces, len(available_interfaces))
        if ret < 1:
            raise ValueError("Error getting interfaces : " + str(ret))

        ret = llt.SetDeviceInterface(self.hLLT, available_interfaces[0], 0)
        if ret < 1:
            raise ValueError("Error setting device interface: " + str(ret))

        # Connect
        ret = llt.Connect(self.hLLT)
        if ret < 1:
            raise ConnectionError("Error connect: " + str(ret))

        # Get available resolutions
        ret = llt.GetResolutions(
            self.hLLT, available_resolutions, len(available_resolutions))
        if ret < 1:
            raise ValueError("Error getting resolutions : " + str(ret))

        if self.resolution not in available_resolutions:
            raise AttributeError("Wrong resolution")

        # Scanner type
        ret = llt.GetLLTType(self.hLLT, ct.byref(self.scanner_type))
        if ret < 1:
            raise ValueError("Error scanner type: " + str(ret))

        # Scanner type
        ret = llt.SetResolution(self.hLLT, self.resolution)
        if ret < 1:
            raise ValueError("Error setting resolution: " + str(ret))

        # Set profile config
        ret = llt.SetProfileConfig(self.hLLT, llt.TProfileConfig.PROFILE)
        if ret < 1:
            raise ValueError("Error setting profile config: " + str(ret))

        # Start transfer
        ret = llt.TransferProfiles(
            self.hLLT, llt.TTransferProfileType.NORMAL_TRANSFER, 1)
        if ret < 1:
            raise ValueError("Error starting transfer profiles: " + str(ret))

        # Warm-up time
        time.sleep(0.1)

    def __del__(self):
        # Stop transmission
        ret = llt.TransferProfiles(
            self.hLLT, llt.TTransferProfileType.NORMAL_TRANSFER, 0)
        if ret < 1:
            raise ValueError("Error stopping transfer profiles: " + str(ret))

        # Disconnect
        ret = llt.Disconnect(self.hLLT)
        if ret < 1:
            raise ConnectionAbortedError("Error while disconnect: " + str(ret))

        print("Disconnected from laser gracefully")

    def setup(self):
        raise NotImplementedError
    
    def setLaserOn(self):
        """
        Turn on laser.
        """
        raise NotImplementedError
    
    def setLaserOff(self):
        """
        Turn off laser.
        
        Useful as a safety precaution or to exclude it from the camera image.
        """
        raise NotImplementedError

    def getLine(self, remove_outliers=False):
        """
        Get a line scan.

        Args:
            remove_outliers (bool, False): If known outliers should be removed before returning the results

        Returns:
            x,z 
        """
        ret = llt.GetActualProfile(self.hLLT, self.profile_buffer, len(self.profile_buffer), llt.TProfileConfig.PROFILE,
                                   ct.byref(self.lost_profiles))
        if ret != len(self.profile_buffer):
            print("Error get profile buffer data: " + str(ret))

        ret = llt.ConvertProfile2Values(self.hLLT, self.profile_buffer, self.resolution, llt.TProfileConfig.PROFILE, self.scanner_type, 0, 1,
                                        self.null_ptr_short, self.intensities, self.null_ptr_short, self.x, self.z, self.null_ptr_int, self.null_ptr_int)
        if ret & llt.CONVERT_X is 0 or ret & llt.CONVERT_Z is 0 or ret & llt.CONVERT_MAXIMUM is 0:
            raise ValueError("Error converting data: " + str(ret))

        for i in range(16):
            self.timestamp[i] = self.profile_buffer[self.resolution * 64 - 16 + i]

        llt.Timestamp2TimeAndCount(self.timestamp, ct.byref(self.shutter_opened), ct.byref(
            self.shutter_closed), ct.byref(self.profile_count))

        if remove_outliers:
            raise NotImplementedError

        # TODO: Convert to standard python types before returning
        return self.x, self.z

    def cleanLine(self):
        """
        Remove noise.
        """
        raise NotImplementedError


