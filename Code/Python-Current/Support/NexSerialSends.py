import serial, platform, time
from Support.SupportUtils import printDebug

end_cmd=b'\xff\xff\xff'

if(platform.system() == "Windows"):
    ser = serial.Serial('COM7', baudrate = 19200,  writeTimeout = 10)  # open serial port
    #pass
elif (platform.system() == "Linux"):
    ser = serial.Serial('\dev\tty0')  # open serial port

NT = "t"
NN  = "n"
NP  = "p"
NC = "c"

#---Nextion Assets------
AssetLDWL_B       = 110
AssetLDWL_B_HL    = 111
AssetLDWL_B_FC    = 112
AssetLDWL_B_HL_FC = 113
AssetLDWL_Y       = 114
AssetLDWL_Y_HL    = 115
AssetLDWL_Y_FC    = 116
AssetLDWL_Y_HL_FC = 117
AssetLDWR_B       = 118
AssetLDWR_B_HL    = 119
AssetLDWR_B_FC    = 120
AssetLDWR_B_HL_FC = 121 
AssetLDWR_Y       = 122
AssetLDWR_Y_HL    = 123
AssetLDWR_Y_FC    = 124
AssetLDWR_Y_HL_FC = 125
AssetLDWL_B_Brake = 126
AssetLDWL_Y_Brake = 127
AssetLDWR_B_Brake = 128
AssetLDWR_Y_Brake = 129

AssetAEB1      = 130
AssetAEB2      = 131
AssetAEB3      = 132
AssetAEBBrake  = 83

AssetRCTA1     = 133
AssetRCTA2     = 134
AssetRCTAL     = 87
AssetRCTAR     = 91
ASSETRCTABrake = 135

AssetPOPO1     = 141
AssetPOPO2     = 142
AssetPOPOBrake = 143

#---NextionPics--------
NEX_Alert_Center    = 30
NEX_Center_L        = 3
NEX_Center_R        = 4

NEX_Brake_AEB       = 14
NEX_Brake_LDW       = 31
NEX_Brake_POPO_RCTA = 32 

NEX_BSD_RCTA_L      = 15
NEX_BSD_RCTA_R      = 16

#---Vars---------------
anishows = 5





def send(cmd):
    ser.write(cmd)
    ser.write(end_cmd)
    ser.close

def ResetNextion():
    printDebug("[From nextion.py] Restarting Nextion!!!!")
    send(command)

def SendRef(type, id):
    #72 65 66 20 70 31 ff ff ff
    typebyte = str.encode(str(type))
    idbyte = str.encode(str(id))
    ser.write(b'\x72\x65\x66\x20')
    ser.write(typebyte)
    ser.write(idbyte)
    ser.write(end_cmd)

def SendPage(pagecmd):
    printDebug("[From nextion.py] Showing page {}".format(pagecmd))
    pagebyte = str.encode(str(pagecmd))
    ser.write(b'\x70\x61\x67\x65\x20')
    ser.write(pagebyte)
    ser.write(end_cmd)
    
def SendVal(type, id, val):
    idbyte = str.encode(str(id))
    if isinstance(val, str) or isinstance(val, int):
        textbyte = str.encode(str(val))
    elif isinstance(val, float):
        textbyte = str.encode(str(float(val)))
    else:
        print("Please provide str, int, or float")

    if type == "t":
        #74(type) 31(ID) 2E 74 78 74 3D 22(begin marker) 33(CMD) 22(end marker) [ff ff ff](End Bytes)
        ser.write(b'\x74')
        ser.write(idbyte)
        ser.write(b'\x2E\x74\x78\x74\x3D\x22')
        ser.write(textbyte)
        ser.write(b'\x22')
        ser.write(end_cmd)
    elif type == "n":
        #6E 31(id) 2E 76 61 6C 3D 32(val) ff ff ff (end bytes)
        ser.write(b'\x6E')
        ser.write(idbyte)
        ser.write(b'\x2E\x76\x61\x6C\x3D')
        ser.write(textbyte)
        ser.write(end_cmd)

def SendVis(type, id, isVis):
    #76 69 73 20 70(type) 32(id) 2C 30(val) ff ff ff (teminator)ser.write(b'\x74')
    typebyte = str.encode(str(type))
    idbyte = str.encode(str(id))
    visbyte = str.encode(str(isVis))
    ser.write(b'\x76\x69\x73\x20')
    ser.write(typebyte)
    ser.write(idbyte)
    ser.write(b'\x2C')
    ser.write(visbyte)
    ser.write(end_cmd)

def SendPic(id, asset):
    #p26.pic=81
    #70 (32 36)ID 2E 70 69 63 3D (38 31)Val (ff ff ff) terminator
    idbyte = str.encode(str(id))
    assbyte = str.encode(str(asset))
    ser.write(b'\x70')
    ser.write(idbyte)
    ser.write(b'\x2E\x70\x69\x63\x3D')
    ser.write(assbyte)
    ser.write(end_cmd)

def SendBright(value):
    #64 69 6D 73 3D 30(level) ff ff ff(teminator)
    valbyte = str.encode(str(id))
    ser.write(b'\x64\x69\x6D\x3D\x31\x30\x30\xff\xff\xff')
    #ser.write(valbyte)
    #ser.write(end_cmd)


#####################################################################################################################
def AEBShow(brake, severity):
    pass

def LDWLShow(brake):
    pass

def LDWRShow(brake):
    pass

def SwayShow():
    pass

def RCTAShow(direction):
    pass



