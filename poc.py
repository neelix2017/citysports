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

async def notify_(address,  debug=True):
    global queue
    result = ""
    start = time.time()
    async with BleakClient(address, timeout  = 10) as client:
        await client.start_notify("ffeeddcc-bbaa-9988-7766-554433221102", notification_handler) 
        #start treadmill
        #await client.write_gatt_char("ffeeddcc-bbaa-9988-7766-554433221101",  bytearray(b'\xa1\x03\x01\x01\xa2'), response=False)
        #stop treadmill
        #await client.write_gatt_char("ffeeddcc-bbaa-9988-7766-554433221101",  bytearray(b'\xa1\x03\x01\x05\xa6'), response=False)
        if len(queue) > 0:
            logger.info(queue)
            await client.write_gatt_char("ffeeddcc-bbaa-9988-7766-554433221101",  bytearray(queue[0]), response=False)
            queue = queue[1:]
        await asyncio.Future()
        #await client.stop_notify("ffeeddcc-bbaa-9988-7766-554433221102")
    return result

def read_request(characteristic: BlessGATTCharacteristic, **kwargs) -> bytearray:
    logger.debug(f"Reading {characteristic.value}")
    return characteristic.value


def write_request(characteristic: BlessGATTCharacteristic, value: Any, **kwargs):
    characteristic.value = value
    logger.debug(f"Char {characteristic.uuid} value set to {characteristic.value}")
    if characteristic.value == b"\x0f":
        logger.debug("Nice")
        trigger.set()

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
        send = ( b'\x84\x24\xaa\xaa\x00\x00\x00\x00\x00\x00\x00\x00\x0B\x00\x00\x00\x00' )
        logger.info("[%s] Updating app : speed %s",datetime.datetime.now().strftime("%Y-%m-%YT%H:%M:%S.%fZ"),speed)
        _speed = struct.pack('<h',int(speed*100))
        send=send.replace(b"\xaa\xaa", _speed)
        server.get_characteristic(bc.cTreadmillDataUUID).value =  bytearray (send)  
        server.update_value(     bc.sFitnessMachineUUID, bc.cTreadmillDataUUID    )
        #queue.append([bc.cFitnessMachineControlPointUUID, response])    
        await asyncio.sleep(1)
    await server.stop()

async def repeater(): # Here
    loop = asyncio.get_running_loop()
    loop.create_task(notify_("84:C2:E4:54:E0:40")) # Here
    await loop.create_task(run(loop)) # "await" is needed

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(repeater()) 