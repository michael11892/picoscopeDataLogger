import ctypes
import copy
from ctypes import *
from picosdk.ps2000a import ps2000a as ps
from picosdk.functions import assert_pico_ok
from picosdk.ps2000a import PS2000A_TRIGGER_CONDITIONS
from picosdk.ps2000a import PS2000A_TRIGGER_CHANNEL_PROPERTIES
try:
    from picosdk.ps2000a import PS2000A_PWQ_CONDITIONS
except:
    class P3000A_PWQ_CONDITIONS(Structure): #In case the class isn't available in the SDK (i.e. ps 3000a)
        _pack_ = 1
        _fields_ = [("channelA", c_int32),
                    ("channelB", c_int32),
                    ("channelC", c_int32),
                    ("channelD", c_int32),
                    ("external", c_int32),
                    ("aux", c_int32)]

def trig_pwq_config(chandle, status, trig_pwq_conditions, trig_direction, trig_lower, trig_upper, trig_type):
    #Set channel conditions
    pwq_list = []
    for condition in trig_pwq_conditions:
        condition = list(map(ctypes.c_int32, condition)) #Convert arguments to ctypes.c_int32
        pwq_list.append(PS2000A_PWQ_CONDITIONS(condition[0], condition[1], condition[2], condition[3], condition[4], condition[5]))
    pwq_list_c = (PS2000A_PWQ_CONDITIONS * len(pwq_list))(*pwq_list)

    #Set pulse width qualifier conditions
    status["setPulseWidthQualifier"] = ps2.ps2000aSetPulseWidthQualifier(chandle, ctypes.byref(pwq_list_c), len(pwq_list), trig_direction, trig_lower, trig_upper, trig_type)
    assert_pico_ok(status["setPulseWidthQualifier"])

def trig_logic_config(chandle, status, trig_conditions, trig_directions, trig_properties, trig_auto):
    #Set channel conditions
    cond_list = []
    for condition in trig_conditions:
        condition_ = copy.deepcopy(condition)
        try:
            condition = list(map(ctypes.c_int32, condition_)) #Convert arguments to ctypes.c_int32
            cond_list.append(PS2000A_TRIGGER_CONDITIONS(condition[0], condition[1], condition[2], condition[3], condition[4], condition[5], condition[6], condition[7]))
        except:
            condition = list(map(ctypes.c_uint32, condition_)) #Convert arguments to ctypes.c_uint32
            cond_list.append(PS2000A_TRIGGER_CONDITIONS(condition[0], condition[1], condition[2], condition[3], condition[4], condition[5], condition[6], condition[7]))
    cond_list_c = (PS2000A_TRIGGER_CONDITIONS * len(cond_list))(*cond_list)
    status["setTriggerChannelConditions"] = ps.ps2000aSetTriggerChannelConditions(chandle, ctypes.byref(cond_list_c), ctypes.c_int16(len(cond_list)))
    assert_pico_ok(status["setTriggerChannelConditions"])

    #Set channel directions
    #Examples don't have the change of type so try running the code without the below line
    trig_directions =  list(map(ctypes.c_int32, trig_directions)) #Convert arguments to ctypes.c_int32
    status["setTriggerChannelDirections"] = ps.ps2000aSetTriggerChannelDirections(chandle, trig_directions[0], trig_directions[1], trig_directions[2], trig_directions[3], trig_directions[4], trig_directions[5])
    assert_pico_ok(status["setTriggerChannelDirections"])

    #Set channel properties
    prop_list = []
    for property in trig_properties:
        try:
            prop_list.append(PS2000A_TRIGGER_CHANNEL_PROPERTIES(ctypes.c_int16(property[0]), ctypes.c_uint16(property[1]), ctypes.c_int16(property[2]), ctypes.c_uint16(property[3]), ctypes.c_int32(property[4]), ctypes.c_int32(property[5])))
        except:
            prop_list.append(PS2000A_TRIGGER_CHANNEL_PROPERTIES(ctypes.c_int16(property[0]), ctypes.c_uint16(property[1]), ctypes.c_int16(property[2]), ctypes.c_uint16(property[3]), ctypes.c_uint32(property[4]), ctypes.c_uint32(property[5])))
    prop_list_c = (PS2000A_TRIGGER_CHANNEL_PROPERTIES * len(prop_list))(*prop_list)
    status["setTriggerChannelProperties"] = ps.ps2000aSetTriggerChannelProperties(chandle, ctypes.byref(prop_list_c),  ctypes.c_int16(len(prop_list)), ctypes.c_int16(1), ctypes.c_int32(trig_auto))
    assert_pico_ok(status["setTriggerChannelProperties"])

def trig_simple_config(chandle, status, enable, channel, trig_adc_counts, trig_direction, trig_delay, trig_auto):
    status["trigger"] = ps.ps2000aSetSimpleTrigger(chandle, enable, channel, trig_adc_counts, trig_direction, trig_delay, trig_auto)
    assert_pico_ok(status["trigger"])
