import ctypes as ct
from enum import IntEnum
import os.path

dll_name = "LLT.dll"
dll_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), dll_name)

# Callback
CBFUNC = ct.CFUNCTYPE(None, ct.POINTER(ct.c_ubyte), ct.c_uint, ct.c_uint)

# Convert Data
CONVERT_X = 0x00000800
CONVERT_Z = 0x00001000
CONVERT_WIDTH = 0x00000100
CONVERT_MAXIMUM = 0x00000200
CONVERT_THRESHOLD = 0x00000400
CONVERT_M0 = 0x00002000
CONVERT_M1 = 0x00004000

# RS422 Interface Function
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
RS422_INTERFACE_FUNCTION_SERIALPORT_115200 = 0
RS422_INTERFACE_FUNCTION_SERIALPORT_57600 = 1
RS422_INTERFACE_FUNCTION_SERIALPORT_38400 = 2
RS422_INTERFACE_FUNCTION_SERIALPORT_19200 = 3
RS422_INTERFACE_FUNCTION_SERIALPORT_9600 = 4
RS422_INTERFACE_FUNCTION_TRIGGER_INPUT = 5
RS422_INTERFACE_FUNCTION_TRIGGER_OUTPUT = 6
RS422_INTERFACE_FUNCTION_CMM_TRIGGER = 7

ERROR_OK = 0
ERROR_SERIAL_COMM = 1
ERROR_SERIAL_LLT = 7
ERROR_CONNECTIONLOST = 10
ERROR_STOPSAVING = 100

IS_FUNC_NO = 0
IS_FUNC_YES = 1

# General return data
GENNERAL_FUNCTION_DEVICE_NAME_NOT_SUPPORTED = 4
GENERAL_FUNCTION_PACKET_SIZE_CHANGED = 3
GENERAL_FUNCTION_CONTAINER_MODE_HEIGHT_CHANGED = 2
GENERAL_FUNCTION_OK = 1
GENERAL_FUNCTION_NOT_AVAILABLE = 0

# Error variables
ERROR_GENERAL_WHILE_LOAD_PROFILE = -1000
ERROR_GENERAL_NOT_CONNECTED = -1001
ERROR_GENERAL_DEVICE_BUSY = -1002
ERROR_GENERAL_WHILE_LOAD_PROFILE_OR_GET_PROFILES = -1003
ERROR_GENERAL_WHILE_GET_PROFILES = -1004
ERROR_GENERAL_GET_SET_ADDRESS = -1005
ERROR_GENERAL_POINTER_MISSING = -1006
ERROR_GENERAL_WHILE_SAVE_PROFILES = -1007
ERROR_GENERAL_SECOND_CONNECTION_TO_LLT = -1008
ERROR_GETDEVICENAME_SIZE_TOO_LOW = -1
ERROR_GETDEVICENAME_NO_BUFFER = -2
ERROR_LOADSAVE_WRITING_LAST_BUFFER = -50
ERROR_LOADSAVE_WHILE_SAVE_PROFILE = -51
ERROR_LOADSAVE_NO_PROFILELENGTH_POINTER = -52
ERROR_LOADSAVE_NO_LOAD_PROFILE = -53
ERROR_LOADSAVE_STOP_ALREADY_LOAD = -54
ERROR_LOADSAVE_CANT_OPEN_FILE = -55
ERROR_LOADSAVE_FILE_POSITION_TOO_HIGH = -57
ERROR_LOADSAVE_AVI_NOT_SUPPORTED = -58
ERROR_LOADSAVE_NO_REARRANGEMENT_POINTER = -59
ERROR_LOADSAVE_WRONG_PROFILE_CONFIG = -60
ERROR_LOADSAVE_NOT_TRANSFERING = -61
ERROR_PROFTRANS_SHOTS_NOT_ACTIVE = -100
ERROR_PROFTRANS_SHOTS_COUNT_TOO_HIGH = -101
ERROR_PROFTRANS_WRONG_PROFILE_CONFIG = -102
ERROR_PROFTRANS_FILE_EOF = -103
ERROR_PROFTRANS_NO_NEW_PROFILE = -104
ERROR_PROFTRANS_BUFFER_SIZE_TOO_LOW = -105
ERROR_PROFTRANS_NO_PROFILE_TRANSFER = -106
ERROR_PROFTRANS_PACKET_SIZE_TOO_HIGH = -107
ERROR_PROFTRANS_CREATE_BUFFERS = -108
ERROR_PROFTRANS_WRONG_PACKET_SIZE_FOR_CONTAINER = -109
ERROR_PROFTRANS_REFLECTION_NUMBER_TOO_HIGH = -110
ERROR_PROFTRANS_MULTIPLE_SHOTS_ACTIVE = -111
ERROR_PROFTRANS_BUFFER_HANDOUT = -112
ERROR_PROFTRANS_WRONG_BUFFER_POINTER = -113
ERROR_PROFTRANS_WRONG_TRANSFER_CONFIG = -114
ERROR_SETGETFUNCTIONS_WRONG_BUFFER_COUNT = -150
ERROR_SETGETFUNCTIONS_PACKET_SIZE = -151
ERROR_SETGETFUNCTIONS_WRONG_PROFILE_CONFIG = -152
ERROR_SETGETFUNCTIONS_NOT_SUPPORTED_RESOLUTION = -153
ERROR_SETGETFUNCTIONS_REFLECTION_NUMBER_TOO_HIGH = -154
ERROR_SETGETFUNCTIONS_WRONG_FEATURE_ADRESS = -155
ERROR_SETGETFUNCTIONS_SIZE_TOO_LOW = -156
ERROR_SETGETFUNCTIONS_WRONG_PROFILE_SIZE = -157
ERROR_SETGETFUNCTIONS_MOD_4 = -158
ERROR_SETGETFUNCTIONS_REARRANGEMENT_PROFILE = -159
ERROR_SETGETFUNCTIONS_USER_MODE_TOO_HIGH = -160
ERROR_SETGETFUNCTIONS_USER_MODE_FACTORY_DEFAULT = -161
ERROR_SETGETFUNCTIONS_HEARTBEAT_TOO_HIGH = -162
ERROR_POSTPROCESSING_NO_PROF_BUFFER = -200
ERROR_POSTPROCESSING_MOD_4 = -201
ERROR_POSTPROCESSING_NO_RESULT = -202
ERROR_POSTPROCESSING_LOW_BUFFERSIZE = -203
ERROR_POSTPROCESSING_WRONG_RESULT_SIZE = -204
ERROR_GETDEVINTERFACES_WIN_NOT_SUPPORTED = -250
ERROR_GETDEVINTERFACES_REQUEST_COUNT = -251
ERROR_GETDEVINTERFACES_CONNECTED = -252
ERROR_GETDEVINTERFACES_INTERNAL = -253
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
ERROR_CMMTRIGGER_NO_DIVISOR = -400
ERROR_CMMTRIGGER_TIMEOUT_AFTER_TRANSFERPROFILES = -401
ERROR_CMMTRIGGER_TIMEOUT_AFTER_SETCMMTRIGGER = -402
ERROR_TRANSERRORVALUE_WRONG_ERROR_VALUE = -450
ERROR_TRANSERRORVALUE_BUFFER_SIZE_TOO_LOW = -451
ERROR_READWRITECONFIG_CANT_CREATE_FILE = -500
ERROR_READWRITECONFIG_CANT_OPEN_FILE = -501
ERROR_READWRITECONFIG_QUEUE_TO_SMALL = -502

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
FEATURE_FUNCTION_ANALOGFREQUENCY = 0xf0f00828
INQUIRY_FUNCTION_ANALOGFREQUENCY = 0xf0f00528
FEATURE_FUNCTION_ANALOGOUTPUTMODES = 0xf0f00820
INQUIRY_FUNCTION_ANALOGOUTPUTMODES = 0xf0f00520
FEATURE_FUNCTION_CMMTRIGGER = 0xf0f00888
INQUIRY_FUNCTION_CMMTRIGGER = 0xf0f00588
FEATURE_FUNCTION_REARRANGEMENT_PROFILE = 0xf0f0080c
INQUIRY_FUNCTION_REARRANGEMENT_PROFILE = 0xf0f0050c
FEATURE_FUNCTION_PROFILE_FILTER = 0xf0f00818
INQUIRY_FUNCTION_PROFILE_FILTER = 0xf0f00518
FEATURE_FUNCTION_RS422_INTERFACE_FUNCTION = 0xf0f008c0
INQUIRY_FUNCTION_RS422_INTERFACE_FUNCTION = 0xf0f005c0
FEATURE_FUNCTION_SATURATION = 0xf0f00814
INQUIRY_FUNCTION_SATURATION = 0xf0f00514
FEATURE_FUNCTION_TEMPERATURE = 0xf0f0082c
INQUIRY_FUNCTION_TEMPERATURE = 0xf0f0052c
FEATURE_FUNCTION_CAPTURE_QUALITY = 0xf0f008c4
INQUIRY_FUNCTION_CAPTURE_QUALITY = 0xf0f005c4
FEATURE_FUNCTION_SHARPNESS = 0xf0f00808
INQUIRY_FUNCTION_SHARPNESS = 0xf0f00508
FEATURE_FUNCTION_PACKET_DELAY = 0x00000d08
FEATURE_FUNCTION_CONNECTION_SPEED = 0x00000670


# Structs
class TPartialProfile(ct.Structure):
    _fields_ = [('nStartPoint', ct.c_uint),
                ('nStartPointData', ct.c_uint),
                ('nPointCount', ct.c_uint),
                ('nPointDataWidth', ct.c_uint)]


# Enums
class CtypesEnum(IntEnum):
    """A ctypes-compatible IntEnum superclass."""

    @classmethod
    def from_param(cls, obj):
        return obj


class TScannerType(CtypesEnum):
    scanCONTROL28xx_25 = 0
    scanCONTROL28xx_100 = 1
    scanCONTROL28xx_10 = 2

    scanCONTROL27xx_25 = 1000
    scanCONTROL27xx_100 = 1001
    scanCONTROL27xx_50 = 1002

    scanCONTROL26xx_25 = 2000
    scanCONTROL26xx_100 = 2001
    scanCONTROL26xx_50 = 2002
    scanCONTROL26xx_10 = 2003

    scanCONTROL29xx_25 = 3000
    scanCONTROL29xx_100 = 3001
    scanCONTROL29xx_50 = 3002
    scanCONTROL29xx_10 = 3003


class TFileType(CtypesEnum):
    AVI = 0
    LLT = 1
    CSV = 2
    BMP = 3
    CSV_NEG = 4


class TCallbackType(CtypesEnum):
    STD_CALL = 0
    C_DECL = 1


class TProfileConfig(CtypesEnum):
    NONE = 0
    PROFILE = 1
    CONTAINER = 1
    VIDEO_IMAGE = 1
    PURE_PROFILE = 2
    QUARTER_PROFILE = 3
    CSV_PROFILE = 4
    PARTIAL_PROFILE = 5


class TTransferProfileType(CtypesEnum):
    NORMAL_TRANSFER = 0
    SHOT_TRANSFER = 1
    NORMAL_CONTAINER_MODE = 2
    SHOT_CONTAINER_MODE = 3
    NONE_TRANSFER = 4


class TInterfaceType(CtypesEnum):
    INTF_TYPE_UNKNOWN = 0
    INTF_TYPE_SERIAL = 1
    INTF_TYPE_FIREWIRE = 2
    INTF_TYPE_ETHERNET = 3


class TTransferVideoType(CtypesEnum):
    VIDEO_MODE_0 = 0
    VIDEO_MODE_1 = 1
    NONE_VIDEOMODE = 2

# DLL Loader
llt = ct.CDLL(dll_path)

# ID functions
GetDeviceName = llt['c_GetDeviceName']
GetDeviceName.restype = ct.c_int
GetDeviceName.argtypes = [ct.c_uint, ct.c_char_p, ct.c_uint,  ct.c_char_p, ct.c_uint]

GetLLTType = llt['c_GetLLTType']
GetLLTType.restype = ct.c_int
GetLLTType.argtypes = [ct.c_uint, ct.POINTER(ct.c_int)]

GetLLTVersions = llt['c_GetLLTVersions']
GetLLTVersions.restype = ct.c_int
GetLLTVersions.argtypes = [ct.c_uint, ct.POINTER(ct.c_uint), ct.POINTER(ct.c_uint), ct.POINTER(ct.c_uint)]

# Init Functions
CreateLLTDevice = llt['c_CreateLLTDevice']
CreateLLTDevice.restype = ct.c_uint
CreateLLTDevice.argtypes = [TInterfaceType]

GetDeviceInterfaces = llt['c_GetDeviceInterfaces']
GetDeviceInterfaces.restype = ct.c_int
GetDeviceInterfaces.argtypes = [ct.c_uint, ct.POINTER(ct.c_uint), ct.c_uint]

GetDeviceInterfacesFast = llt['c_GetDeviceInterfacesFast']
GetDeviceInterfacesFast.restype = ct.c_int
GetDeviceInterfacesFast.argtypes = [ct.c_uint, ct.POINTER(ct.c_uint), ct.c_uint]

SetDeviceInterface = llt['c_SetDeviceInterface']
SetDeviceInterface.restype = ct.c_int
SetDeviceInterface.argtypes = [ct.c_uint, ct.c_uint, ct.c_int]

GetInterfaceType = llt['c_GetInterfaceType']
GetInterfaceType.restype = ct.c_int
GetInterfaceType.argtypes = [ct.c_uint]

GetInterfaceType = llt['c_GetDiscoveryBroadcastTarget']
GetInterfaceType.restype = ct.c_int
GetInterfaceType.argtypes = [ct.c_uint]

GetInterfaceType = llt['c_SetDiscoveryBroadcastTarget']
GetInterfaceType.restype = ct.c_int
GetInterfaceType.argtypes = [ct.c_uint, ct.c_uint, ct.c_int]

# Delete Device
DelDevice = llt['c_DelDevice']
DelDevice.restype = ct.c_uint
DelDevice.argtypes = [ct.c_uint]

# Connect
Connect = llt['c_Connect']
Connect.restype = ct.c_int
Connect.argtypes = [ct.c_uint]

Disconnect = llt['c_Disconnect']
Disconnect.restype = ct.c_int
Disconnect.argtypes = [ct.c_uint]

# Write Config
ExportLLTConfig = llt['c_ExportLLTConfig']
ExportLLTConfig.restype = ct.c_int
ExportLLTConfig.argtypes = [ct.c_uint, ct.c_char_p]

# Transfer and Profile Functions
TransferProfiles = llt['c_TransferProfiles']
TransferProfiles.restype = ct.c_int
TransferProfiles.argtypes = [ct.c_uint, TTransferProfileType, ct.c_int]

TransferVideoStream = llt['c_TransferVideoStream']
TransferVideoStream.restype = ct.c_int
TransferVideoStream.argtypes = [ct.c_uint, TTransferVideoType, ct.c_int, ct.POINTER(ct.c_uint), ct.POINTER(ct.c_uint)]

GetActualProfile = llt['c_GetActualProfile']
GetActualProfile.restype = ct.c_int
GetActualProfile.argtypes = [ct.c_uint, ct.POINTER(ct.c_ubyte), ct.c_uint, TProfileConfig, ct.POINTER(ct.c_int)]

GetProfile = llt['c_GetProfile']
GetProfile.restype = ct.c_int
GetProfile.argtypes = [ct.c_uint]

MultiShot = llt['c_MultiShot']
MultiShot.restype = ct.c_int
MultiShot.argtypes = [ct.c_uint, ct.c_uint]

SetHoldBuffersForPolling = llt['c_SetHoldBuffersForPolling']
SetHoldBuffersForPolling.restype = ct.c_int
SetHoldBuffersForPolling.argtypes = [ct.c_uint, ct.c_uint]

GetHoldBuffersForPolling = llt['c_GetHoldBuffersForPolling']
GetHoldBuffersForPolling.restype = ct.c_int
GetHoldBuffersForPolling.argtypes = [ct.c_uint, ct.POINTER(ct.c_uint)]

# Convert Profiles
ConvertProfile2Values = llt['c_ConvertProfile2Values']
ConvertProfile2Values.restype = ct.c_int
ConvertProfile2Values.argtypes = [ct.c_uint, ct.POINTER(ct.c_ubyte), ct.c_uint, TProfileConfig, TScannerType, ct.c_uint,
                                  ct.c_uint, ct.POINTER(ct.c_ushort), ct.POINTER(ct.c_ushort), ct.POINTER(ct.c_ushort),
                                  ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.POINTER(ct.c_uint),
                                  ct.POINTER(ct.c_uint)]

ConvertPartProfile2Values = llt['c_ConvertPartProfile2Values']
ConvertPartProfile2Values.restype = ct.c_int
ConvertPartProfile2Values.argtypes = [ct.c_uint, ct.POINTER(ct.c_ubyte), ct.POINTER(TPartialProfile), TScannerType,
                                      ct.c_int, ct.c_uint, ct.POINTER(ct.c_ushort), ct.POINTER(ct.c_ushort),
                                      ct.POINTER(ct.c_ushort), ct.POINTER(ct.c_double), ct.POINTER(ct.c_double),
                                      ct.POINTER(ct.c_uint), ct.POINTER(ct.c_uint)]

# Timestamp
Timestamp2TimeAndCount = llt['c_Timestamp2TimeAndCount']
Timestamp2TimeAndCount.restype = None
Timestamp2TimeAndCount.argtypes = [ct.POINTER(ct.c_ubyte), ct.POINTER(ct.c_double), ct.POINTER(ct.c_double),
                                   ct.POINTER(ct.c_uint)]

Timestamp2CmmTriggerAndInCounter = llt['c_Timestamp2CmmTriggerAndInCounter']
Timestamp2CmmTriggerAndInCounter.restype = None
Timestamp2CmmTriggerAndInCounter.argtypes = [ct.POINTER(ct.c_ubyte), ct.POINTER(ct.c_uint), ct.POINTER(ct.c_int),
                                             ct.POINTER(ct.c_int), ct.POINTER(ct.c_uint)]

# Set Functions
SetFeature = llt['c_SetFeature']
SetFeature.restype = ct.c_int
SetFeature.argtypes = [ct.c_uint, ct.c_uint, ct.c_uint]

SetBufferCount = llt['c_SetBufferCount']
SetBufferCount.restype = ct.c_int
SetBufferCount.argtypes = [ct.c_uint, ct.c_uint]

SetMainReflection = llt['c_SetMainReflection']
SetMainReflection.restype = ct.c_int
SetMainReflection.argtypes = [ct.c_uint, ct.c_uint]

SetMaxFileSize = llt['c_SetMaxFileSize']
SetMaxFileSize.restype = ct.c_int
SetMaxFileSize.argtypes = [ct.c_uint, ct.c_uint]

SetPacketSize = llt['c_SetPacketSize']
SetPacketSize.restype = ct.c_int
SetPacketSize.argtypes = [ct.c_uint, ct.c_uint]

SetProfileConfig = llt['c_SetProfileConfig']
SetProfileConfig.restype = ct.c_int
SetProfileConfig.argtypes = [ct.c_uint, TProfileConfig]

SetResolution = llt['c_SetResolution']
SetResolution.restype = ct.c_int
SetResolution.argtypes = [ct.c_uint, ct.c_uint]

SetProfileContainerSize = llt['c_SetProfileContainerSize']
SetProfileContainerSize.restype = ct.c_int
SetProfileContainerSize.argtypes = [ct.c_uint, ct.c_uint, ct.c_uint]

SetEthernetHeartbeatTimeout = llt['c_SetEthernetHeartbeatTimeout']
SetEthernetHeartbeatTimeout.restype = ct.c_int
SetEthernetHeartbeatTimeout.argtypes = [ct.c_uint, ct.c_uint]

# Get Functions
GetFeature = llt['c_GetFeature']
GetFeature.restype = ct.c_int
GetFeature.argtypes = [ct.c_uint, ct.c_uint, ct.POINTER(ct.c_uint)]

GetMinMaxPacketSize = llt['c_GetMinMaxPacketSize']
GetMinMaxPacketSize.restype = ct.c_int
GetMinMaxPacketSize.argtypes = [ct.c_uint, ct.POINTER(ct.c_uint), ct.POINTER(ct.c_uint)]

GetResolutions = llt['c_GetResolutions']
GetResolutions.restype = ct.c_int
GetResolutions.argtypes = [ct.c_uint, ct.POINTER(ct.c_uint), ct.c_uint]

GetBufferCount = llt['c_GetBufferCount']
GetBufferCount.restype = ct.c_int
GetBufferCount.argtypes = [ct.c_uint, ct.POINTER(ct.c_uint)]

GetMainReflection = llt['c_GetMainReflection']
GetMainReflection.restype = ct.c_int
GetMainReflection.argtypes = [ct.c_uint, ct.POINTER(ct.c_uint)]

GetMaxFileSize = llt['c_GetMaxFileSize']
GetMaxFileSize.restype = ct.c_int
GetMaxFileSize.argtypes = [ct.c_uint, ct.POINTER(ct.c_uint)]

GetPacketSize = llt['c_GetPacketSize']
GetPacketSize.restype = ct.c_int
GetPacketSize.argtypes = [ct.c_uint, ct.POINTER(ct.c_uint)]

GetProfileConfig = llt['c_GetProfileConfig']
GetProfileConfig.restype = ct.c_int
GetProfileConfig.argtypes = [ct.c_uint, ct.POINTER(ct.c_uint)]

GetProfileConfig = llt['c_GetResolution']
GetProfileConfig.restype = ct.c_int
GetProfileConfig.argtypes = [ct.c_uint, ct.POINTER(ct.c_uint)]

GetProfileConfig = llt['c_GetProfileContainerSize']
GetProfileConfig.restype = ct.c_int
GetProfileConfig.argtypes = [ct.c_uint, ct.POINTER(ct.c_uint), ct.POINTER(ct.c_uint)]

GetMaxProfileContainerSize = llt['c_GetMaxProfileContainerSize']
GetMaxProfileContainerSize.restype = ct.c_int
GetMaxProfileContainerSize.argtypes = [ct.c_uint, ct.POINTER(ct.c_uint), ct.POINTER(ct.c_uint)]

GetEthernetHeartbeatTimeout = llt['c_GetEthernetHeartbeatTimeout']
GetEthernetHeartbeatTimeout.restype = ct.c_int
GetEthernetHeartbeatTimeout.argtypes = [ct.c_uint, ct.POINTER(ct.c_uint)]

# Maintenance parameter
GetActualUserMode = llt['c_GetActualUserMode']
GetActualUserMode.restype = ct.c_int
GetActualUserMode.argtypes = [ct.c_uint, ct.POINTER(ct.c_uint), ct.POINTER(ct.c_uint)]

ReadWriteUserModes = llt['c_ReadWriteUserModes']
ReadWriteUserModes.restype = ct.c_int
ReadWriteUserModes.argtypes = [ct.c_uint, ct.c_int, ct.c_uint]

SaveGlobalParameter = llt['c_SaveGlobalParameter']
SaveGlobalParameter.restype = ct.c_int
SaveGlobalParameter.argtypes = [ct.c_uint]

TriggerProfile = llt['c_TriggerProfile']
TriggerProfile.restype = ct.c_int
TriggerProfile.argtypes = [ct.c_uint]

# Partial profiles function
GetPartialProfileUnitSize = llt['c_GetPartialProfileUnitSize']
GetPartialProfileUnitSize.restype = ct.c_int
GetPartialProfileUnitSize.argtypes = [ct.c_uint, ct.POINTER(ct.c_uint), ct.POINTER(ct.c_uint)]

GetPartialProfile = llt['c_GetPartialProfile']
GetPartialProfile.restype = ct.c_int
GetPartialProfile.argtypes = [ct.c_uint, ct.POINTER(TPartialProfile)]

SetPartialProfile = llt['c_SetPartialProfile']
SetPartialProfile.restype = ct.c_int
SetPartialProfile.argtypes = [ct.c_uint, ct.POINTER(TPartialProfile)]

# Is Functions
IsInterfaceType = llt['c_IsInterfaceType']
IsInterfaceType.restype = ct.c_int
IsInterfaceType.argtypes = [ct.c_uint, ct.c_int]

IsTransferingProfiles = llt['c_IsTransferingProfiles']
IsTransferingProfiles.restype = ct.c_int
IsTransferingProfiles.argtypes = [ct.c_uint]

# PostProcessing
ReadPostProcessingParameter = llt['c_ReadPostProcessingParameter']
ReadPostProcessingParameter.restype = ct.c_int
ReadPostProcessingParameter.argtypes = [ct.c_uint, ct.POINTER(ct.c_uint), ct.c_uint]

WritePostProcessingParameter = llt['c_WritePostProcessingParameter']
WritePostProcessingParameter.restype = ct.c_int
WritePostProcessingParameter.argtypes = [ct.c_uint, ct.POINTER(ct.c_uint), ct.c_uint]

ConvertProfile2ModuleResult = llt['c_ConvertProfile2ModuleResult']
ConvertProfile2ModuleResult.restype = ct.c_int
ConvertProfile2ModuleResult.argtypes = [ct.c_uint, ct.POINTER(ct.c_ubyte), ct.c_uint, ct.POINTER(ct.c_ubyte), ct.c_uint,
                                        ct.POINTER(TPartialProfile)]

# Load/Save Functions
SaveProfiles = llt['c_SaveProfiles']
SaveProfiles.restype = ct.c_int
SaveProfiles.argtypes = [ct.c_uint, ct.c_char_p, TFileType]

LoadProfiles = llt['c_LoadProfiles']
LoadProfiles.restype = ct.c_int
LoadProfiles.argtypes = [ct.c_uint, ct.c_char_p, ct.POINTER(TPartialProfile), ct.POINTER(ct.c_uint),
                         ct.POINTER(ct.c_uint), ct.POINTER(ct.c_uint)]

LoadProfilesGetPos = llt['c_LoadProfilesGetPos']
LoadProfilesGetPos.restype = ct.c_int
LoadProfilesGetPos.argtypes = [ct.c_uint, ct.POINTER(ct.c_uint), ct.POINTER(ct.c_uint)]

LoadProfilesSetPos = llt['c_LoadProfilesSetPos']
LoadProfilesSetPos.restype = ct.c_int
LoadProfilesSetPos.argtypes = [ct.c_uint, ct.c_uint]

# Register Functions
RegisterCallback = llt['c_RegisterCallback']
RegisterCallback.restype = ct.c_int
RegisterCallback.argtypes = [ct.c_uint, TCallbackType, CBFUNC, ct.c_uint]

RegisterErrorMsg = llt['c_RegisterErrorMsg']
RegisterErrorMsg.restype = ct.c_int
RegisterErrorMsg.argtypes = [ct.c_uint, ct.c_uint, ct.POINTER(ct.c_int), ct.POINTER(ct.c_uint)]

# Special CMM Trigger Functions
StopTransmissionAndCmmTrigger = llt['c_StopTransmissionAndCmmTrigger']
StopTransmissionAndCmmTrigger.restype = ct.c_int
StopTransmissionAndCmmTrigger.argtypes = [ct.c_uint, ct.c_uint, TTransferProfileType, ct.c_uint, ct.c_char_p, TFileType,
                                          ct.c_uint]

StopTransmissionAndCmmTrigger = llt['c_StopTransmissionAndCmmTrigger']
StopTransmissionAndCmmTrigger.restype = ct.c_int
StopTransmissionAndCmmTrigger.argtypes = [ct.c_uint, ct.c_int, ct.c_uint]