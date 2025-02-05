#-------------------------------------------------------------------------------
# Author        https://github.com/WouterJD
#               wouter.dubbeldam@xs4all.nl
#-------------------------------------------------------------------------------
# Version info
#-------------------------------------------------------------------------------
__version__ = "2022-03-21"
# 2022-03-21    Made available to kevincar/bless as example; small modifications
# 2022-03-08    Constants for bleBleak.py and bleBless.py
# 2022-02-22    First version
#-------------------------------------------------------------------------------
import struct

#-------------------------------------------------------------------------------
# To distribute to bless/examples, proceed as follows:
# - Copy bleBless.py, bleBlessClass and bleConstants   bleBleak.py to hbldh\bless\examples
#        FTMSserver   FTMSserverClass   FTMSconstants  FTMSclient
# - Change below "If True:" into "If False:" (and similar in bleBleak/bleBless)
#       like this, precompiler "knows" that code is unused.
# - Check bleBleak/bleBless for BlessExample
#-------------------------------------------------------------------------------
if True:
    BlessExample = True
    #---------------------------------------------------------------------------
    # Import and Constants for bless example context
    #---------------------------------------------------------------------------
    little_endian       ='<'    #  little-endian          standard    none
    unsigned_char       ='B'    #  unsigned char          integer             1               (3)
    short               ='h'    #  short                  integer             2               (3)
    unsigned_short      ='H'    #  unsigned short         integer             2               (3)
    unsigned_long       ='L'    #  unsigned long          integer             4               (3)

    def HexSpace(info):
        return (info)

#-------------------------------------------------------------------------------
# Bluetooth standard-defined UUIDs receive special treatment as they are
# commonly used throughout the various protocols of the Specification. They are
# grouped around the Bluetooth Base UUID (xxxxxxxx-0000-1000-8000-00805F9B34FB)
# and share 96 common bits. (See core specification, 3.B.2.5.1)
# --> "16-bit UUID Numbers Document.pdf"
#-------------------------------------------------------------------------------
# Constants to create the BLE service/characteristics structure
#-------------------------------------------------------------------------------
BluetoothBaseUUID               = 'xxxxxxxx-0000-1000-8000-00805f9b34fb'
BluetoothBaseUUIDsuffix         =         '-0000-1000-8000-00805f9b34fb'
CharacteristicUserDescriptionUUID='00002901-0000-1000-8000-00805f9b34fb'

sGenericAccessUUID              = '00001800-0000-1000-8000-00805f9b34fb'
sGenericAccessUUID_private      = '19590705-0000-1000-8000-00805f9b34fb'
cDeviceNameUUID                 = '00002a00-0000-1000-8000-00805f9b34fb'
cDeviceNameName                 = 'Device Name'
cAppearanceUUID                 = '00002a01-0000-1000-8000-00805f9b34fb'
cAppearanceName                 = 'Appearance'
# Service
sFitnessMachineUUID             = "00001826-0000-1000-8000-00805f9b34fb"
sFitnessMachineName             = "Fitness Machine"
# Service characteristics
cFitnessMachineFeatureUUID      = "00002acc-0000-1000-8000-00805f9b34fb"
cFitnessMachineFeatureName      = "Fitness Machine Feature"
fmf_CadenceSupported                        = 1 <<  1
fmf_HeartRateMeasurementSupported           = 0       # 1 << 10; CTP's do not expect heartrate to be supplied by Fitness Machine
fmf_PowerMeasurementSupported               = 1 << 14
fmf_PowerTargetSettingSupported             = 1 <<  3
fmf_IndoorBikeSimulationParametersSupported = 1 << 13
                                # FM Service, section 4.3 p 19:                         features (32 bits), Target settings features (32 bits)
fmf_Info                        = struct.pack(little_endian + unsigned_long * 2,  fmf_CadenceSupported                        |
                                                                                  fmf_HeartRateMeasurementSupported           |
                                                                                  fmf_PowerMeasurementSupported,
                                                                                  fmf_PowerTargetSettingSupported             |
                                                                                  fmf_IndoorBikeSimulationParametersSupported )

cTreadmillDataUUID                 = "00002acd-0000-1000-8000-00805f9b34fb"
cTreadmillDataName                 = "Treadmill Data"
ibd_InstantaneousSpeedIsNotPresent  = 0         # Bit 0     # Present unless flagged that it's not
ibd_InstantaneousCadencePresent     = 1 << 2    # Bit 2
ibd_InstantaneousPowerPresent       = 1 << 6    # Bit 6
ibd_HeartRatePresent                = 1 << 9    # Bit 9
ibd_Flags                           = 0
                                    # FM Service, section 4.9 p 44: Flags, Cadence, Power, HeartRate
ibd_Info                            = struct.pack(little_endian + unsigned_short * 4, 
                                                ibd_InstantaneousPowerPresent | ibd_HeartRatePresent,
                                                123, 456, 89
                                                )
                                                
cIndoorBikeDataUUID                 = "00002ad2-0000-1000-8000-00805f9b34fb"
cIndoorBikeDataName                 = "Indoor Bike Data"
ibd_InstantaneousSpeedIsNotPresent  = 0         # Bit 0     # Present unless flagged that it's not
ibd_InstantaneousCadencePresent     = 1 << 2    # Bit 2
ibd_InstantaneousPowerPresent       = 1 << 6    # Bit 6
ibd_HeartRatePresent                = 1 << 9    # Bit 9
ibd_Flags                           = 0
                                    # FM Service, section 4.9 p 44: Flags, Cadence, Power, HeartRate
ibd_Info                            = struct.pack(little_endian + unsigned_short * 4, 
                                                ibd_InstantaneousPowerPresent | ibd_HeartRatePresent,
                                                123, 456, 89
                                                )

cFitnessMachineStatusUUID       = "00002ada-0000-1000-8000-00805f9b34fb"
cFitnessMachineStatusName       = "Fitness Machine Status"
                                # FM Service, section 4.17 p 56:                OpCode (UnsignedINT8), Parameter
fms_Reset                                 = 0x01
fms_FitnessMachineStoppedOrPausedByUser   = 0x02
fms_FitnessMachineStartedOrResumedByUser  = 0x04
fms_TargetPowerChanged                    = 0x08
fms_IndoorBikeSimulationParametersChanged = 0x12


cFitnessMachineControlPointUUID = "00002ad9-0000-1000-8000-00805f9b34fb"
cFitnessMachineControlPointName = "Fitness Machine Control Point"
                                # FM Service, section 4.16 p 50:                OpCode (UnsignedINT8), Parameter
fmcp_RequestControl             = 0x00
fmcp_Reset                      = 0x01
fmcp_SetTargetPower             = 0x05
fmcp_StartOrResume              = 0x07
fmcp_StopOrPause                = 0x08
fmcp_SetIndoorBikeSimulation    = 0x11
fmcp_ResponseCode               = 0x80

fmcp_Success                    = 0x01
fmcp_OpCodeNotSupported         = 0x02
fmcp_InvalidParameter           = 0x03
fmcp_OperationFailed            = 0x04
fmcp_ControlNotPermitted        = 0x05

cSupportedPowerRangeUUID        = "00002ad8-0000-1000-8000-00805f9b34fb"
cSupportedPowerRangeName        = "Supported Power Range"
                                # FM Service, section 4.14 p 49:                  Min, Max,  Increment
spr_Info                        = struct.pack(little_endian + unsigned_short * 3, 0,   1000, 1)

# Service
sHeartRateUUID                  = "0000180d-0000-1000-8000-00805f9b34fb"
sHeartRateName                  = "Heart Rate"
# Service characteristics
cHeartRateMeasurementUUID       = "00002a37-0000-1000-8000-00805f9b34fb"
cHeartRateMeasurementName       = "Heart Rate Measurement"
                                # HRS_SPEC_V10, section 3.1 p 9:                 Flags, Heartrate
hrm_Info                        = struct.pack(little_endian + unsigned_char * 2, 0,     123)

# Service
sSteeringUUID                   = "347b0001-7635-408b-8918-8ff3949ce592"
sSteeringName                   = "Steering"
# Service characteristics
cSteeringUnknown1UUID           = "347b0012-7635-408b-8918-8ff3949ce592"
cSteeringUnknown1Name           = "Unknown 1"
cSteeringUnknown2UUID           = "347b0013-7635-408b-8918-8ff3949ce592"
cSteeringUnknown2Name           = "Unknown 2"
cSteeringUnknown3UUID           = "347b0014-7635-408b-8918-8ff3949ce592"
cSteeringUnknown3Name           = "Unknown 3"
cSteeringUnknown4UUID           = "347b0019-7635-408b-8918-8ff3949ce592"
cSteeringUnknown4Name           = "Unknown 4"
cSteeringAngleUUID              = "347b0030-7635-408b-8918-8ff3949ce592"
cSteeringAngleName              = "Angle"
cSteeringTxUUID                 = "347b0032-7635-408b-8918-8ff3949ce592"
cSteeringTxName                 = "Transmission"
cSteeringRxUUID                 = "347b0031-7635-408b-8918-8ff3949ce592"
cSteeringRxName                 = "Reception"

angle_Info                      = "Unknown"

# ==============================================================================
# Main program
# ==============================================================================
if __name__ == "__main__":
    print("bleConstants.py cannot be executed on it's own.")