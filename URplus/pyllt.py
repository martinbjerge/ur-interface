import ctypes as ct
from enum import IntEnum
import os.path

lib_name = "libmescan.so.1.0"
lib_path = "/usr/local/lib" + os.path.sep + lib_name

# Callback
buffer_cb_func = ct.CFUNCTYPE(None, ct.c_void_p, ct.c_uint, ct.c_void_p)
buffer_cl_func = ct.CFUNCTYPE(None, ct.c_void_p, ct.c_void_p)

# Convert Data
CONVERT_X = 0x00000800
CONVERT_Z = 0x00001000
CONVERT_WIDTH = 0x00000100
CONVERT_MAXIMUM = 0x00000200
CONVERT_THRESHOLD = 0x00000400
CONVERT_M0 = 0x00002000
CONVERT_M1 = 0x00004000

# Processing flags
PROC_HIGH_RESOLUTION = 1
PROC_CALIBRATION = (1 << 1)
PROC_MULTIREFL_ALL = (0 << 2)
PROC_MULITREFL_FIRST = (1 << 2)
PROC_MULITREFL_LAST = (2 << 2)
PROC_MULITREFL_LARGESTAREA = (3 << 2)
PROC_MULITREFL_MAXINTENS = (4 << 2)
PROC_MULITREFL_SINGLE = (5 << 2)
PROC_POSTPROCESSING_ON = (1 << 5)
PROC_FLIP_DISTANCE = (1 << 6)
PROC_FLIP_POSITION = (1 << 7)
PROC_AUTOSHUTTER_DELAY = (1 << 8)
PROC_SHUTTERALIGN_CENTRE = (0 << 9)
PROC_SHUTTERALIGN_RIGHT = (1 << 9)
PROC_SHUTTERALIGN_LEFT = (2 << 9)
PROC_SHUTTERALIGN_OFF = (3 << 9)
PROC_AUTOSHUTTER_ADVANCED = (1 << 11)

# Threshold flags
THRESHOLD_DYNAMIC = (1 << 24)
THRESHOLD_VIDEO_FILTER = (1 << 11)
THRESHOLD_BACKGROUND_FILTER = (1 << 10)

# Shutter flags
SHUTTER_AUTOMATIC = (1 << 24)

# Laser power flags
LASER_OFF = 0
LASER_REDUCED_POWER = 1
LASER_FULL_POWER = 2
LASER_PULSEMODE = (1 << 11)

# Temperature register
TEMP_PREPARE_VALUE = 0x86000000

# Trigger flags
TRIG_MODE_EDGE = (0 << 16)
TRIG_MODE_PULSE = (1 << 16)
TRIG_MODE_GATE = (2 << 16)
TRIG_MODE_ENCODER = (3 << 16)
TRIG_INPUT_RS422 = (0 << 21)
TRIG_INPUT_DIGIN = (1 << 21)
TRIG_POLARITY_LOW = (0 << 24)
TRIG_POLARITY_HIGH = (1 << 24)
TRIG_EXT_ACTIVE = (1 << 25)
TRIG_INTERNAL = (0 << 25)

# Measuring field flags
MEASFIELD_ACTIVATE_FREE = (1 << 11)

# Maintenance flags
MAINTENANCE_LOOPBACK = (1 << 1)
MAINTENANCE_ENCODER_ACTIVE = (1 << 3)
MAINTENANCE_SUPPRESS_REGISTER_RESET = (1 << 5)
MAINTENANCE_UM_LOAD_VIA_DIGIN = (0 << 6)
MAINTENANCE_UM_SUPPRESS_UNTIL_REBOOT = (1 << 6)
MAINTENANCE_UM_SUPPRESS_UNTIL_GVCP_CLOSE = (2 << 6)
MAINTENANCE_UM_SUPPRESS_UNTIL_REBOOT_GVCP_CLOSE = (3 << 6)

# Multiport flags
MULTI_LEVEL_5V = (0 << 11)
MULTI_LEVEL_24V = (1 << 11)
MULTI_RS422_TERM_ON = (0 << 10)
MULTI_RS422_TERM_OFF = (1 << 10)
MULTI_ENCODER_BIDIRECT = (0 << 9)
MULTI_ENCODER_UNIDIRECT = (1 << 9)
MULTI_DIGIN_ENC_INDEX = (0 << 4)
MULTI_DIGIN_ENC_TRIG = (1 << 4)
MULTI_DIGIN_TRIG_ONLY = (2 << 4)
MULTI_DIGIN_TRIG_UM = (3 << 4)
MULTI_DIGIN_UM = (4 << 4)
MULTI_DIGIN_TS = (5 << 4)
MULTI_DIGIN_FRAMETRIG_BI = (6 << 4)
MULTI_DIGIN_FRAMETRIG_UNI = (7 << 4)
MULTI_RS422_115200 = 0
MULTI_RS422_57600 = 1
MULTI_RS422_38400 = 2
MULTI_RS422_19200 = 3
MULTI_RS422_9600 = 4
MULTI_RS422_TRIG_IN = 5
MULTI_RS422_TRIG_OUT = 6
MULTI_RS422_CMM = 7

RS422_INTERFACE_FUNCTION_AUTO_27xx = 0
RS422_INTERFACE_FUNCTION_SERIALPORT_115200_27xx = 1
RS422_INTERFACE_FUNCTION_TRIGGER_27xx = 2
RS422_INTERFACE_FUNCTION_CMM_TRIGGER_27xx = 3
RS422_INTERFACE_FUNCTION_ENCODER_27xx = 4
RS422_INTERFACE_FUNCTION_DIGITAL_OUTPUT_27xx = 6
RS422_INTERFACE_FUNCTION_TRIGGER_LASER_PULSE_27xx = 7
RS422_INTERFACE_FUNCTION_SERIALPORT_57600_27xx = 8
RS422_INTERFACE_FUNCTION_SERIALPORT_38400_27xx = 9
RS422_INTERFACE_FUNCTION_SERIALPORT_19200_27xx = 10
RS422_INTERFACE_FUNCTION_SERIALPORT_9600_27xx = 11

# Profile filter flags
FILTER_RESAMPLE_EXTRAPOLATE_POINTS = (1 << 11)
FILTER_RESAMPLE_ALL_INFO = (1 << 10)
FILTER_RESAMPLE_DISABLED = (0 << 4)
FILTER_RESAMPLE_TINY = (1 << 4)
FILTER_RESAMPLE_VERYSMALL = (2 << 4)
FILTER_RESAMPLE_SMALL = (3 << 4)
FILTER_RESAMPLE_MEDIUM = (4 << 4)
FILTER_RESAMPLE_LARGE = (5 << 4)
FILTER_RESAMPLE_VERYLARGE = (6 << 4)
FILTER_RESAMPLE_HUGE = (7 << 4)
FILTER_MEDIAN_DISABLED = (0 << 2)
FILTER_MEDIAN_3 = (1 << 2)
FILTER_MEDIAN_5 = (2 << 2)
FILTER_MEDIAN_7 = (3 << 2)
FILTER_AVG_DISABLED = 0
FILTER_AVG_3 = 1
FILTER_AVG_5 = 2
FILTER_AVG_7 = 3

# Container flags
CONTAINER_STRIPE_4 = (1 << 23)
CONTAINER_STRIPE_3 = (1 << 22)
CONTAINER_STRIPE_2 = (1 << 21)
CONTAINER_STRIPE_1 = (1 << 20)
CONTAINER_JOIN = (1 << 19)
CONTAINER_DATA_SIGNED = (1 << 18)
CONTAINER_DATA_LSBF = (1 << 17)
CONTAINER_DATA_TS = (1 << 11)
CONTAINER_DATA_EMPTYFIELD4TS = (1 << 10)
CONTAINER_DATA_LOOPBACK = (1 << 9)
CONTAINER_DATA_MOM0U = (1 << 8)
CONTAINER_DATA_MOM0L = (1 << 7)
CONTAINER_DATA_MOM1U = (1 << 6)
CONTAINER_DATA_MOM1L = (1 << 5)
CONTAINER_DATA_WIDTH = (1 << 4)
CONTAINER_DATA_INTENS = (1 << 3)
CONTAINER_DATA_THRES = (1 << 2)
CONTAINER_DATA_X = (1 << 1)
CONTAINER_DATA_Z = (1 << 0)

# General return values
GENERAL_FUNCTION_DEVICE_NAME_NOT_SUPPORTED = 4
GENERAL_FUNCTION_OK = 1
GENERAL_FUNCTION_NOT_AVAILABLE = 0

ERROR_GETDEVICENAME_SIZE_TOO_LOW = -1
ERROR_GETDEVICENAME_NO_BUFFER = -2

ERROR_PROFTRANS_WRONG_DATA_SIZE = -100
ERROR_PROFTRANS_WRONG_DATA_FORMAT = -101
ERROR_PROFTRANS_WRONG_RESOLUTION = -102
ERROR_PROFTRANS_REFLECTION_NO_DATA = -103
ERROR_PROFTRANS_NO_NEW_PROFILE = -104
ERROR_PROFTRANS_BUFFER_SIZE_TOO_LOW = -105
ERROR_PROFTRANS_NO_PROFILE_TRANSFER = -106
ERROR_PROFTRANS_REFLECTION_NUMBER_TOO_HIGH = -110
ERROR_PROFTRANS_WRONG_BUFFER_POINTER = -113
ERROR_PROFTRANS_WRONG_TRANSFER_CONFIG = -114
ERROR_PROFTRANS_LOOPBACK_NOT_SUPPORTED = -115

ERROR_SETGETFUNCTIONS_WRONG_BUFFER_COUNT = -150
ERROR_SETGETFUNCTIONS_PACKET_SIZE = -151
ERROR_SETGETFUNCTIONS_WRONG_PROFILE_CONFIG = -152
ERROR_SETGETFUNCTIONS_NOT_SUPPORTED_RESOLUTION = -153
ERROR_SETGETFUNCTIONS_REFLECTION_NUMBER_TOO_HIGH = -154
ERROR_SETGETFUNCTIONS_WRONG_FEATURE_ADRESS = -155
ERROR_SETGETFUNCTIONS_SIZE_TOO_LOW = -156
ERROR_SETGETFUNCTIONS_WRONG_PROFILE_SIZE = -157
ERROR_SETGETFUNCTIONS_MOD_4 = -158
ERROR_SETGETFUNCTIONS_USER_MODE_TOO_HIGH = -160
ERROR_SETGETFUNCTIONS_USER_MODE_FACTORY_DEFAULT = -161
ERROR_SETGETFUNCTIONS_HEARTBEAT_TOO_HIGH = -162

# Error values
ERROR_GETDEVINTERFACE_REQUEST_COUNT = -251
ERROR_GETDEVINTERFACE_INTERNAL = -253

ERROR_CONNECT_LLT_COUNT = -300
ERROR_CONNECT_SELECTED_LLT = -301
ERROR_CONNECT_ALREADY_CONNECTED = -302
ERROR_CONNECT_LLT_NUMBER_ALREADY_USED = -303
ERROR_CONNECT_SERIAL_CONNECTION = -304
ERROR_CONNECT_INVALID_IP = -305

ERROR_PARTPROFILE_NO_PART_PROF = -350
ERROR_PARTPROFILE_TOO_MUCH_BYTES = -351
ERROR_PARTPROFILE_TOO_MUCH_POINTS = -352
ERROR_PARTPROFILE_NO_POINT_COUNT = -353
ERROR_PARTPROFILE_NOT_MOD_UNITSIZE_POINT = -354
ERROR_PARTPROFILE_NOT_MOD_UNITSIZE_DATA = -355

ERROR_TRANSERRORVALUE_WRONG_ERROR_VALUE = -450
ERROR_TRANSERRORVALUE_BUFFER_SIZE_TOO_LOW = -451

ERROR_TRANSMISSION_CANCEL_NO_CAM = -888
ERROR_DEVPROP_NOT_AVAILABLE = -999

ERROR_GENERAL_NOT_CONNECTED = -1001
ERROR_GENERAL_DEVICE_BUSY = -1002
ERROR_TRANSMISSION_CANCEL_NO_TRANSMISSION_ACTIVE = -1003
ERROR_TRANSMISSION_CANCEL_TRANSMISSION_ACTIVE = -1004
ERROR_GENERAL_GET_SET_ADDRESS = -1005
ERROR_GENERAL_POINTER_MISSING = -1006
ERROR_GENERAL_WHILE_SAVE_PROFILES = -1007
ERROR_GENERAL_VALUE_NOT_ALLOWED = -1008

ERROR_DEVPROP_NOT_FOUND = -1300
ERROR_DEVPROP_DECODE = -1301
ERROR_DEVPROP_DEPRECATED = -1302
ERROR_DEVPROP_READ_FAILURE = -1303
ERROR_DEVPROP_WRONG_FILE_FORMAT = -1304
ERROR_DEVPROP_WRONG_CAMERA = -1305

# Feature Register
FEATURE_FUNCTION_SERIAL = 0xf0000410
FEATURE_FUNCTION_LASERPOWER = 0xf0f00824
INQUIRY_FUNCTION_LASERPOWER = 0xf0f00524
FEATURE_FUNCTION_MEASURINGFIELD = 0xf0f00880
INQUIRY_FUNCTION_MEASURINGFIELD = 0xf0f00580
FEATURE_FUNCTION_TRIGGER = 0xf0f00830
INQUIRY_FUNCTION_TRIGGER = 0xf0f00530
FEATURE_FUNCTION_SHUTTERTIME = 0xf0f0081c
INQUIRY_FUNCTION_SHUTTERTIME = 0xf0f0051c
FEATURE_FUNCTION_IDLETIME = 0xf0f00800
INQUIRY_FUNCTION_IDLETIME = 0xf0f00500
FEATURE_FUNCTION_PROCESSING_PROFILEDATA = 0xf0f00804
INQUIRY_FUNCTION_PROCESSING_PROFILEDATA = 0xf0f00504
FEATURE_FUNCTION_THRESHOLD = 0xf0f00810
INQUIRY_FUNCTION_THRESHOLD = 0xf0f00510
FEATURE_FUNCTION_MAINTENANCEFUNCTIONS = 0xf0f0088c
INQUIRY_FUNCTION_MAINTENANCEFUNCTIONS = 0xf0f0058c
FEATURE_FUNCTION_REARRANGEMENT_PROFILE = 0xf0f0080c
INQUIRY_FUNCTION_REARRANGEMENT_PROFILE = 0xf0f0050c
FEATURE_FUNCTION_PROFILE_FILTER = 0xf0f00818
INQUIRY_FUNCTION_PROFILE_FILTER = 0xf0f00518
FEATURE_FUNCTION_RS422_INTERFACE_FUNCTION = 0xf0f008c0
INQUIRY_FUNCTION_RS422_INTERFACE_FUNCTION = 0xf0f005c0
FEATURE_FUNCTION_TEMPERATURE = 0xf0f0082c
INQUIRY_FUNCTION_TEMPERATURE = 0xf0f0052c
FEATURE_FUNCTION_SHARPNESS = 0xf0f00808
INQUIRY_FUNCTION_SHARPNESS = 0xf0f00508
FEATURE_FUNCTION_PACKET_DELAY = 0x00000d08

# MISC
WAIT_OBJECT_0 = 0

# Structs
class TPartialProfile(ct.Structure):
    _fields_ = [('nStartPoint', ct.c_uint),
                ('nStartPointData', ct.c_uint),
                ('nPointCount', ct.c_uint),
                ('nPointDataWidth', ct.c_uint)]


class MEDeviceData(ct.Structure):
    _fields_ = [('device_series', ct.c_int),
                ('scaling', ct.c_double),
                ('offset', ct.c_double),
                ('max_packet_size', ct.c_int),
                ('max_frequency', ct.c_int),
                ('post_proc', ct.c_int),
                ('min_x_display', ct.c_double),
                ('max_x_display', ct.c_double),
                ('min_y_display', ct.c_double),
                ('max_y_display', ct.c_double),
                ('rotate_image', ct.c_int),
                ('min_width', ct.c_double)]


class EHANDLE(ct.Structure):
    pass


class LLT(ct.Structure):
    pass


class ArvDevice(ct.Structure):
    pass


# Enums
class CtypesEnum(IntEnum):
    """A ctypes-compatible IntEnum superclass."""

    @classmethod
    def from_param(cls, obj):
        return obj


class TScannerType(CtypesEnum):
    scanCONTROL27xx_25 = 1000
    scanCONTROL27xx_100 = 1001
    scanCONTROL27xx_50 = 1002
    scanCONTROL27xx_xxx = 1999

    scanCONTROL26xx_25 = 2000
    scanCONTROL26xx_100 = 2001
    scanCONTROL26xx_50 = 2002
    scanCONTROL26xx_10 = 2003
    scanCONTROL26xx_xxx = 2999

    scanCONTROL29xx_25 = 3000
    scanCONTROL29xx_100 = 3001
    scanCONTROL29xx_50 = 3002
    scanCONTROL29xx_10 = 3003
    scanCONTROL29xx_xxx = 3999


class TProfileConfig(CtypesEnum):
    NONE = 0
    PROFILE = 1
    VIDEO_IMAGE = 2
    PARTIAL_PROFILE = 5
    CONTAINER = 6


class TStreamPriorityState(CtypesEnum):
    PRIO_NOT_SET = 0
    PRIO_SET_SUCCESS = 1
    PRIO_SET_NICE_FAILED = 2
    PRIO_SET_RT_FAILED = 3
    PRIO_SET_FAILED = 4


class TTransferProfileType(CtypesEnum):
    NORMAL_TRANSFER = 0
    NORMAL_CONTAINER_MODE = 2
    NONE_TRANSFER = 4


# DLL Loader
llt = ct.CDLL(lib_path)

#
# Basic
#

# Search for interfaces
# Hint: make interface array with:
# available_interfaces = [ct.create_string_buffer(8) for i in range(6)]
# available_interfaces_p = (ct.c_char_p * 6)(*map(ct.addressof, available_interfaces))
GetDeviceInterfaces = llt['get_device_interfaces']
GetDeviceInterfaces.restype = ct.c_int
GetDeviceInterfaces.argtypes = [ct.POINTER(ct.c_char_p), ct.c_uint]

# Init Device
InitDevice = llt['init_device']
InitDevice.restype = ct.c_int
InitDevice.argtypes = [ct.c_char_p, ct.POINTER(MEDeviceData), ct.c_char_p]

# Getter
GetLLTTypeByName = llt['get_llt_type_by_name']
GetLLTTypeByName.restype = ct.c_int
GetLLTTypeByName.argtypes = [ct.c_char_p, ct.POINTER(ct.c_int)]

GetScalingAndOffsetByType = llt['get_scaling_and_offset_by_type']
GetScalingAndOffsetByType.restype = ct.c_int
GetScalingAndOffsetByType.argtypes = [ct.c_int, ct.POINTER(ct.c_double), ct.POINTER(ct.c_double)]

# Convert Profiles
ConvertProfile2Values = llt['convert_profile_2_values']
ConvertProfile2Values.restype = ct.c_int
ConvertProfile2Values.argtypes = [ct.POINTER(ct.c_ubyte), ct.c_uint, ct.c_uint, TScannerType, ct.c_uint,
                                  ct.POINTER(ct.c_ushort), ct.POINTER(ct.c_ushort), ct.POINTER(ct.c_ushort),
                                  ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.POINTER(ct.c_uint),
                                  ct.POINTER(ct.c_uint)]

ConvertPartProfile2Values = llt['convert_part_profile_2_values']
ConvertPartProfile2Values.restype = ct.c_int
ConvertPartProfile2Values.argtypes = [ct.POINTER(ct.c_ubyte), ct.c_uint, ct.POINTER(TPartialProfile), TScannerType,
                                      ct.c_uint, ct.POINTER(ct.c_ushort), ct.POINTER(ct.c_ushort),
                                      ct.POINTER(ct.c_ushort), ct.POINTER(ct.c_double), ct.POINTER(ct.c_double),
                                      ct.POINTER(ct.c_uint), ct.POINTER(ct.c_uint)]

ConvertRearrangedContainer2Values = llt['convert_rearranged_container_2_values']
ConvertRearrangedContainer2Values.restype = ct.c_int
ConvertRearrangedContainer2Values.argtypes = [ct.POINTER(ct.c_ubyte), ct.c_uint, ct.c_uint, ct.c_uint, TScannerType,
                                      ct.c_uint, ct.POINTER(ct.c_ushort), ct.POINTER(ct.c_ushort),
                                      ct.POINTER(ct.c_ushort), ct.POINTER(ct.c_double), ct.POINTER(ct.c_double)]

# Timestamp
Timestamp2TimeAndCount = llt['timestamp_2_time_and_count']
Timestamp2TimeAndCount.restype = None
Timestamp2TimeAndCount.argtypes = [ct.POINTER(ct.c_ubyte), ct.POINTER(ct.c_double), ct.POINTER(ct.c_double),
                                   ct.POINTER(ct.c_uint), ct.POINTER(ct.c_ushort)]

# Event funcs
CreateEvent = llt['create_event']
CreateEvent.restype = ct.POINTER(EHANDLE)
CreateEvent.argtypes = []

SetEvent = llt['set_event']
SetEvent.argtypes = [ct.POINTER(EHANDLE)]

ResetEvent = llt['reset_event']
ResetEvent.argtypes = [ct.POINTER(EHANDLE)]

FreeEvent = llt['free_event']
FreeEvent.argtypes = [ct.POINTER(EHANDLE)]

WaitForSingleObject = llt['wait_for_single_object']
WaitForSingleObject.restype = ct.c_int
WaitForSingleObject.argtypes = [ct.POINTER(EHANDLE), ct.c_uint]

#
# Advanced
#

# Device

CreateLLTDevice = llt['create_llt_device']
CreateLLTDevice.restype = ct.POINTER(LLT)
CreateLLTDevice.argtypes = []

DelDevice = llt['del_device']
DelDevice.restype = ct.c_int
DelDevice.argtypes = [ct.POINTER(LLT)]

# Connect

Connect = llt['connect_llt']
Connect.restype = ct.c_int
Connect.argtypes = [ct.POINTER(LLT)]

Disconnect = llt['disconnect_llt']
Disconnect.restype = ct.c_int
Disconnect.argtypes = [ct.POINTER(LLT)]

SetDeviceInterface = llt['set_device_interface']
SetDeviceInterface.restype = ct.c_int
SetDeviceInterface.argtypes = [ct.POINTER(LLT), ct.c_char_p]

# MUST BE CALLED BEFORE CONNECT
SetPathToDeviceProperties = llt['set_path_device_properties']
SetPathToDeviceProperties.restype = ct.c_int
SetPathToDeviceProperties.argtypes = [ct.POINTER(LLT), ct.c_char_p]

# ID functions

GetLLTType = llt['get_llt_type']
GetLLTType.restype = ct.c_int
GetLLTType.argtypes = [ct.POINTER(LLT), ct.POINTER(ct.c_int)]

GetDeviceName = llt['get_device_name']
GetDeviceName.restype = ct.c_int
GetDeviceName.argtypes = [ct.POINTER(LLT), ct.POINTER(ct.c_char_p), ct.POINTER(ct.c_char_p)]

GetLLTVersions = llt['get_llt_version']
GetLLTVersions.restype = ct.c_int
GetLLTVersions.argtypes = [ct.POINTER(LLT), ct.POINTER(ct.c_char_p)]

# path to device_properties.dat must be set
# USAGE:
# me_dev_data = ct.POINTER(llt.MEDeviceData)()
# llt.GetMEDeviceData(hLLT, ct.byref(me_dev_data))
# print(me_dev_data.contents.scaling)
GetMEDeviceData = llt['get_medevice_data']
GetMEDeviceData.restype = ct.c_int
GetMEDeviceData.argtypes = [ct.POINTER(LLT), ct.POINTER(ct.POINTER(MEDeviceData))]

GetArvDevice = llt['get_arv_device']
GetArvDevice.restype = ct.c_int
GetArvDevice.argtypes = [ct.POINTER(LLT), ct.POINTER(ct.POINTER(ArvDevice))]

GetStreamStatistics = llt['get_stream_statistics']
GetStreamStatistics.restype = ct.c_int
GetStreamStatistics.argtypes = [ct.POINTER(LLT), ct.POINTER(ct.c_ulong), ct.POINTER(ct.c_ulong), ct.POINTER(ct.c_ulong)]

# Getter for parameter

GetProfileConfig = llt['get_profile_config']
GetProfileConfig.restype = ct.c_int
GetProfileConfig.argtypes = [ct.POINTER(LLT), ct.POINTER(ct.c_int)]

GetFeature = llt['get_feature']
GetFeature.restype = ct.c_int
GetFeature.argtypes = [ct.POINTER(LLT), ct.c_uint, ct.POINTER(ct.c_uint)]

GetPartialProfile = llt['get_partial_profile']
GetPartialProfile.restype = ct.c_int
GetPartialProfile.argtypes = [ct.POINTER(LLT), ct.POINTER(TPartialProfile)]

GetProfileContainerSize = llt['get_profile_container_size']
GetProfileContainerSize.restype = ct.c_int
GetProfileContainerSize.argtypes = [ct.POINTER(LLT), ct.POINTER(ct.c_uint), ct.POINTER(ct.c_uint)]

GetMaxProfileContainerSize = llt['get_max_profile_container_size']
GetMaxProfileContainerSize.restype = ct.c_int
GetMaxProfileContainerSize.argtypes = [ct.POINTER(LLT), ct.POINTER(ct.c_uint), ct.POINTER(ct.c_uint)]

GetBufferCount = llt['get_buffer_count']
GetBufferCount.restype = ct.c_int
GetBufferCount.argtypes = [ct.POINTER(LLT), ct.POINTER(ct.c_uint)]

GetResolutions = llt['get_resolutions']
GetResolutions.restype = ct.c_int
GetResolutions.argtypes = [ct.POINTER(LLT), ct.POINTER(ct.c_uint), ct.c_uint]

GetResolution = llt['get_resolution']
GetResolution.restype = ct.c_int
GetResolution.argtypes = [ct.POINTER(LLT), ct.POINTER(ct.c_uint)]

GetPartialProfileUnitSize = llt['get_partial_profile_unit_size']
GetPartialProfileUnitSize.restype = ct.c_int
GetPartialProfileUnitSize.argtypes = [ct.POINTER(LLT), ct.POINTER(ct.c_uint), ct.POINTER(ct.c_uint)]

GetMinMaxPacketSize = llt['get_min_max_packet_size']
GetMinMaxPacketSize.restype = ct.c_int
GetMinMaxPacketSize.argtypes = [ct.POINTER(LLT), ct.POINTER(ct.c_uint), ct.POINTER(ct.c_uint)]

GetPacketSize = llt['get_packet_size']
GetPacketSize.restype = ct.c_int
GetPacketSize.argtypes = [ct.POINTER(LLT), ct.POINTER(ct.c_uint)]

GetStreamNiceValue = llt['get_stream_nice_value']
GetStreamNiceValue.restype = ct.c_int
GetStreamNiceValue.argtypes = [ct.POINTER(LLT), ct.POINTER(ct.c_uint)]

GetStreamPriority = llt['get_stream_priority']
GetStreamPriority.restype = ct.c_int
GetStreamPriority.argtypes = [ct.POINTER(LLT), ct.POINTER(ct.c_uint)]

GetLLTScalingAndOffset = llt['get_llt_scaling_and_offset']
GetLLTScalingAndOffset.restype = ct.c_int
GetLLTScalingAndOffset.argtypes = [ct.POINTER(LLT), ct.POINTER(ct.c_double), ct.POINTER(ct.c_double)]

GetHoldBuffersForPolling = llt['get_hold_buffers_for_polling']
GetHoldBuffersForPolling.restype = ct.c_int
GetHoldBuffersForPolling.argtypes = [ct.POINTER(LLT), ct.POINTER(ct.c_uint)]

GetStreamPriorityState = llt['get_stream_priority_state']
GetStreamPriorityState.restype = ct.c_int
GetStreamPriorityState.argtypes = [ct.POINTER(LLT), ct.POINTER(ct.c_int)]

# Set Functions

SetProfileConfig = llt['set_profile_config']
SetProfileConfig.restype = ct.c_int
SetProfileConfig.argtypes = [ct.POINTER(LLT), ct.c_int]

SetFeature = llt['set_feature']
SetFeature.restype = ct.c_int
SetFeature.argtypes = [ct.POINTER(LLT), ct.c_uint, ct.c_uint]

SetResolution = llt['set_resolution']
SetResolution.restype = ct.c_int
SetResolution.argtypes = [ct.POINTER(LLT), ct.c_uint]

SetProfileContainerSize = llt['set_profile_container_size']
SetProfileContainerSize.restype = ct.c_int
SetProfileContainerSize.argtypes = [ct.POINTER(LLT), ct.c_uint, ct.c_uint]

SetPartialProfile = llt['set_partial_profile']
SetPartialProfile.restype = ct.c_int
SetPartialProfile.argtypes = [ct.POINTER(LLT), ct.POINTER(TPartialProfile)]

SetBufferCount = llt['set_buffer_count']
SetBufferCount.restype = ct.c_int
SetBufferCount.argtypes = [ct.POINTER(LLT), ct.c_uint]

SetPacketSize = llt['set_packet_size']
SetPacketSize.restype = ct.c_int
SetPacketSize.argtypes = [ct.POINTER(LLT), ct.c_uint]

SetStreamNiceValue = llt['set_stream_nice_value']
SetStreamNiceValue.restype = ct.c_int
SetStreamNiceValue.argtypes = [ct.POINTER(LLT), ct.c_uint]

SetStreamPriority = llt['set_stream_priority']
SetStreamPriority.restype = ct.c_int
SetStreamPriority.argtypes = [ct.POINTER(LLT), ct.c_uint]

SetHoldBuffersForPolling = llt['set_hold_buffers_for_polling']
SetHoldBuffersForPolling.restype = ct.c_int
SetHoldBuffersForPolling.argtypes = [ct.POINTER(LLT), ct.c_uint]

# Maintenance

GetActualUserMode = llt['get_actual_usermode']
GetActualUserMode.restype = ct.c_int
GetActualUserMode.argtypes = [ct.POINTER(LLT), ct.POINTER(ct.c_uint), ct.POINTER(ct.c_uint)]

ReadWriteUserModes = llt['read_write_usermodes']
ReadWriteUserModes.restype = ct.c_int
ReadWriteUserModes.argtypes = [ct.POINTER(LLT), ct.c_bool, ct.c_uint]

SetCustomCalibration = llt['set_custom_calibration']
SetCustomCalibration.restype = ct.c_int
SetCustomCalibration.argtypes = [ct.POINTER(LLT), ct.c_double, ct.c_double, ct.c_double, ct.c_double, ct.c_double]

ResetCustomCalibration = llt['reset_custom_calibration']
ResetCustomCalibration.restype = ct.c_int
ResetCustomCalibration.argtypes = [ct.POINTER(LLT)]

# Register Functions

RegisterBufferCallback = llt['register_buffer_callback']
RegisterBufferCallback.restype = ct.c_int
RegisterBufferCallback.argtypes = [ct.POINTER(LLT), buffer_cb_func, ct.c_void_p]

RegisterControlLostCallback = llt['register_control_lost_callback']
RegisterControlLostCallback.restype = ct.c_int
RegisterControlLostCallback.argtypes = [ct.POINTER(LLT), buffer_cl_func, ct.c_void_p]

# Transfer

TransferProfiles = llt['transfer_profiles']
TransferProfiles.restype = ct.c_int
TransferProfiles.argtypes = [ct.POINTER(LLT), ct.c_int, ct.c_bool]

GetActualProfile = llt['get_actual_profile']
GetActualProfile.restype = ct.c_int
GetActualProfile.argtypes = [ct.POINTER(LLT), ct.POINTER(ct.c_ubyte), ct.c_uint, TProfileConfig, ct.POINTER(ct.c_uint)]

# Advanced

TriggerProfile = llt['trigger_profile']
TriggerProfile.restype = ct.c_int
TriggerProfile.argtypes = [ct.POINTER(LLT)]

SetPeakFilter = llt['set_peak_filter']
SetPeakFilter.restype = ct.c_int
SetPeakFilter.argtypes = [ct.POINTER(LLT), ct.c_ushort, ct.c_ushort, ct.c_ushort, ct.c_ushort]

SetFreeMeasuringField = llt['set_free_measuring_field']
SetFreeMeasuringField.restype = ct.c_int
SetFreeMeasuringField.argtypes = [ct.POINTER(LLT), ct.c_ushort, ct.c_ushort, ct.c_ushort, ct.c_ushort]

SetDynamicMeasuringFieldTracking = llt['set_dynamic_measuring_field_tracking']
SetDynamicMeasuringFieldTracking.restype = ct.c_int
SetDynamicMeasuringFieldTracking.argtypes = [ct.POINTER(LLT), ct.c_ushort, ct.c_ushort, ct.c_ushort, ct.c_ushort]

# MISC

TranslateErrorValues = llt['translate_error_values']
TranslateErrorValues.restype = ct.c_int
TranslateErrorValues.argtypes = [ct.POINTER(LLT), ct.POINTER(ct.c_char_p), ct.c_uint]