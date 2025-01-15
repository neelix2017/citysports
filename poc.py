"""
Example for a BLE 4.0 Server using a GATT dictionary of services and
characteristics
"""
import sys
import logging
import asyncio
import threading
from random import randrange
import struct
from typing import Any, Dict, Union
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak import BleakClient
from bless import (  # type: ignore
    BlessServer,
    BlessGATTCharacteristic,
    GATTCharacteristicProperties,
    GATTAttributePermissions,
)
import bleConstants         as bc
import datetime,time
start=time.time()
_distance = 0
speed = 0
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name=__name__)
queue = []

CitySports_codes = {
  "stop":        'a1030105',
  "start":       'a1030101',
  "pause":       'a1030101',
  "changeSpeed": 'a1010201',
  "changeIncli": 'a1020202',
}
def check_xor(s):
    i = 0
    i2 = 0
    while i < len(s):
        i3 = i + 2
        i2 ^= int(s[i:i3], 16)
        i = i3
    return int_to_hex_str(i2)
    
def int_to_hex_str(i):
    hex_string = hex(i)[2:]  # Convert to hex and remove '0x' prefix
    str_hex = hex_string
    if len(hex_string) % 2 != 0:
        str_hex = "0" + hex_string
    return str_hex.upper()
    
def getIntValue(bArr, i, i2):
        i3 = 0
        if (bArr is not None):
            i3 = 0;
            if (i < len(bArr)):
                i3 = 0
                if (i >= 0) :
                    if (i2 > 0) :
                        i4 = i2 - 1
                        i5 = i
                        i6 = 0
                        while (True) :
                            i7 = i6
                            i3 = i7
                            if (i4 < 0) :
                                break
                            i8 = i7
                            if (i5 < len(bArr)) :
                                i8 = i7 + ((bArr[i5] & 255) << (i4 * 8))
                            
                            i4-=1
                            i5+=1
                            i6 = i8
                    else :
                        i3 = 0

        return i3/2560

def createCommand(speed):
    if (speed=='start'): return CitySports_codes['start']+check_xor( CitySports_codes['start'])
    if (speed=='stop') : return CitySports_codes['stop']+check_xor( CitySports_codes['stop'])
    try:
        if (speed==float(speed)):
            speedup= CitySports_codes['changeSpeed']+("%0.2X" % int(speed*10)).lower()
            speedup= speedup + check_xor(speedup)
            return speedup
    except:
        return None

async def notify_(address,  debug=True):
    global queue
    result = ""
    start = time.time()
    queue.append([5, createCommand("start")])
    queue.append([8, createCommand(4)])
    queue.append([20, createCommand("stop")])
    _time = 0
    async with BleakClient(address, timeout  = 10) as client:
        await client.start_notify("ffeeddcc-bbaa-9988-7766-554433221102", notification_handler) 
        while (True):
            if len(queue) > 0:
                if (_time >= queue[0][0]):
                    logger.info(bytes.fromhex(queue[0][1]))
                    await client.write_gatt_char("ffeeddcc-bbaa-9988-7766-554433221101",  bytearray(bytes.fromhex(queue[0][1])), response=False)
                    queue = queue[1:]
            logger.info('.')
            _time += 1
            await asyncio.sleep(1)
        #await asyncio.Future()
        #await client.stop_notify("ffeeddcc-bbaa-9988-7766-554433221102")
    return result

def read_request(characteristic: BlessGATTCharacteristic, **kwargs) -> bytearray:
    logger.debug(f"Reading {characteristic.value}")
    return characteristic.value


def write_request(characteristic: BlessGATTCharacteristic, value: Any, **kwargs):
    characteristic.value = value
    logger.debug(f"Char {characteristic.uuid} value set to {characteristic.value}")

def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    """Simple notification handler which prints the data received."""
    #logging.getLogger(__name__).info("%s: %r", characteristic.description, data)
    if (data[1] == 1):
        global start
        global _distance
        global speed
        speed = getIntValue(data,7,2)
        _start = time.time() - start
        distance = speed * 0.2777777777778 * _start
        _distance = distance + _distance
        logger.info("%s,    speed: %s, distance: %s (total %s)",datetime.datetime.now().strftime("%Y-%m-%YT%H:%M:%S.%fZ"), speed, distance, _distance)
        start = time.time()

async def run(loop):
    # Instantiate the server
    gatt: Dict = {
    bc.sFitnessMachineUUID: {
        bc.cFitnessMachineFeatureUUID: {
            "Properties":   (GATTCharacteristicProperties.read),
            "Permissions":  (GATTAttributePermissions.readable | GATTAttributePermissions.writeable),
            "Value":        bc.fmf_Info,                        # b'\x02\x40\x00\x00\x08\x20\x00\x00',
            "value":        bc.fmf_Info,
            "Description":  bc.cFitnessMachineFeatureName
        },
        bc.cTreadmillDataUUID: {
            "Properties":   (GATTCharacteristicProperties.notify),
            "Permissions":  (GATTAttributePermissions.readable | GATTAttributePermissions.writeable),
            "Value":        bc.ibd_Info,                        # Instantaneous Cadence, Power, HeartRate
            "value":        bc.ibd_Info,
            "Description":  bc.cIndoorBikeDataName
        },
        bc.cFitnessMachineStatusUUID: {
            "Properties":   (GATTCharacteristicProperties.notify),
            "Permissions":  (GATTAttributePermissions.readable | GATTAttributePermissions.writeable),
            "value":        b'\x00\x00',                        # Status as "sent" to Cycling Training Program
            "Value":        b'\x00\x00',
            "Description":  bc.cFitnessMachineStatusName
        },
        bc.cFitnessMachineControlPointUUID: {
            "Properties":   (GATTCharacteristicProperties.write | GATTCharacteristicProperties.indicate),
            "Permissions":  (GATTAttributePermissions.readable | GATTAttributePermissions.writeable),
            "Value":        b'\x00\x00',                        # Commands as received from Cycling Training Program
            "value":        b'\x00\x00',
            "Description":  bc.cFitnessMachineControlPointName
        },
        bc.cSupportedPowerRangeUUID: {
            "Properties":   (GATTCharacteristicProperties.read),
            "Permissions":  (GATTAttributePermissions.readable | GATTAttributePermissions.writeable),
            "Value":        bc.spr_Info,                        # Static additional properties of the FTMS
                                                                # b'\x00\x00\xe8\x03\x01\x00'
                                                                # min=0, max=1000, incr=1 
                                                                # ==> 0x0000 0x03e8 0x0001 ==> 0x0000 0xe803 0x0100
            "value":        bc.spr_Info,
            "Description":  bc.cSupportedPowerRangeName
        }
    },
    bc.sHeartRateUUID: {
        bc.cHeartRateMeasurementUUID: {
            "Properties":   (GATTCharacteristicProperties.notify),
            "Permissions":  (GATTAttributePermissions.readable | GATTAttributePermissions.writeable),
            "Value":        bc.hrm_Info,
            "value":        bc.hrm_Info,
            "Description":  bc.cHeartRateMeasurementName
        }
    }
}

    my_service_name = "Citysports-APP"
    server = BlessServer(name=my_service_name, loop=loop)
    server.read_request_func = read_request
    server.write_request_func = write_request
    await server.add_gatt(gatt)
    await server.start()
    logger.debug(server.get_characteristic(bc.cFitnessMachineFeatureUUID))
    logger.debug("Advertising")
    await asyncio.sleep(2)
    #84-24-FA-00-00-00-00-00-00-00-00-00-00-00-00-00-00
    while (True):
        global speed
        #send = ( b'\x84\x24\xaa\xaa\x00\x00\x00\x00\x00\x00\x00\x00\x0B\x00\x00\x00\x00' )
        send  =  struct.pack ("<" + "H" * 8 + "?", 9348,int(speed*100),0,0,0,0,0,0,0)
        logger.info("[%s] Updating app : speed %s",datetime.datetime.now().strftime("%Y-%m-%YT%H:%M:%S.%fZ"),speed)
        #_speed = struct.pack('<h',int(speed*100))
        #send=send.replace(b"\xaa\xaa", _speed)
        server.get_characteristic(bc.cTreadmillDataUUID).value =  bytearray (send)  
        server.update_value(     bc.sFitnessMachineUUID, bc.cTreadmillDataUUID    )  
        await asyncio.sleep(1)
    await server.stop()

async def repeater(): # Here
    loop = asyncio.get_running_loop()
    loop.create_task(notify_("84:C2:E4:54:E0:40")) # Here
    await loop.create_task(run(loop)) # "await" is needed

def createTCX(session_data):
    import TCXexport
    tcx = TCXexport.clsTcxExport()
    tcx.Start()   
    now = datetime.datetime.utcnow()
    j = len (session_data)
    for line in session_data:
        tcx.Trackpoint(Time = now - datetime.timedelta(0,j), HeartRate=line[3], Cadence=line[2], Watts=line[1], SpeedKmh= line[4])
        j -= 1
    tcx.Stop()
    
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    loop.run_until_complete(repeater()) 
except KeyboardInterrupt: 
    print('End')
    #createTCX(session_data)