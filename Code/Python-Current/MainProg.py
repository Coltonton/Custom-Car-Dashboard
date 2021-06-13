import serial, time, platform, threading
import pyfirmata
from datetime import datetime
from Support.NexSerialSends import ResetNextion, SendPage, SendVal, SendVis, SendBright, SendPic, SendRef
#from Support.NexSerialSends import PoPoShow
from Support.SupportUtils import printDebug
import multitimer


#if(platform.system() == "Windows"):
#    #ardMega = pyfirmata.Arduino('COM8')
#elif (platform.system() == "Linux"):
    #ardMega = pyfirmata.Arduino('\dev\tty0')
printDebug("Running on {}".format(platform.system()))



hour = ""
minn = ""
temp = ""

#---Nex Types -----
NT = "t" #NexText
NN = "n" #NexNumber
NP = "p" #NexPic
NC = "c" #NexCrop

CW = "w" #Color White
CB = "b" #Color Blue
CG = "g" #Color Green
CY = "y" #Color Yellow
CR = "r" #Color Red

#---Save Values----
FuelVal  = 0
VarHella = 0
TrainVal = 0
DistVal  = 0
DayVal   = 0
NteVal   = 0
ODOVal   = 0
MPGVal   = 0
TripVal = ""
TripaVal = ""
TripbVal = ""
HeadlightVal = 0

#---Vars---------
sysStartup         = 1
isRemoteStarted    = 0
VarCurrentGear     = "P"
VarGear            = "P" 
shownBLAlerts      = 0
BSDOff             = 0
SRFOff             = 0
IceWarning         = 0
shownBRAlerts      = 0
sysAlert           = 0
parkBrake          = 0
speed              = 0
speedPrev          = 0
anishows           = 10
VarHeadlight       = 0
VarCruiseFollowing = 0
VarPOPO            = 0
VarCruiseState     = 5
VarCruiseDist      = 0
VarCruiseSetSpeed  = "--"
VarIsRainbow       = 0
VarLaneColor       = "white"
VarBrake           = 0
VarFrontUS         = 0
VarRearUS          = 0
VarSpeed           = 0
VarTopPage         = 1
pageOveride        = 0
HideHella          = 0
HidePoPo           = 0
VarFollowing       = 0

VarBSD             = ""
VarRCTA            = 0

VarBSDOff          = 1
VarSRFOff          = 1
VarIceWarning      = 1
VarSysAlert        = 1
VarParkBrake       = 1

driveGearsList = ["N", "D", "1", "2", "3", "4", "5", "6"]

temp = 0

#---Timer Threads---
tTime  = None
tTemp  = None
tSpeed = None


#---Nex Pages ------
pageBoot  = 0
pagePark  = 1
pageDrive = 2
pageMenu  = 3

#---NEX Numbers----
NNumLe = 0
NNumCe = 1
NNumRi = 2

#---NEX Texts------
NTextTemp     = 0
NTextHour     = 1
NTextMin      = 2
NTextSetSpeed = 3
NTextInfo     = 4
NTextGear     = 5
NTextMPG      = 6
NTextTrip     = 7
NTextFuel     = 8
NTextODO      = 9
NTextAboVer   = 10
NTextAboOPVer = 11

#---Nex Pics-------
NPicUpperPannel    = 0
NPicHella          = 1
NPicPOPO           = 2
NPicLeftLane       = 3
NPicRightLane      = 4
NPicCruiseState    = 5
NPicFollowingCar   = 7
NPicHeadlightLeft  = 8
NPicHeadlightRight = 9
NPicCruiseMain     = 10
NPicCruise2        = 11
NPicCruise3        = 12
NPicCruise4        = 13
NPicBrakeMainAEB   = 14
NPicBSDRCTAL       = 15
NPicBSDRCTAR       = 16
NPicLowerPannel    = 17
NPicBL1            = 18
NPicBL2            = 19
NPicBL3            = 20
NPicBR2            = 23
NPicBR1            = 24
NPicFuel           = 25
NPicTrip           = 26

NPicCenterPannel   = 30
NPicBrakeLDW       = 31
NPicBrakePOPORCTA  = 32
NPicRevDistanceBar = 33
NPicAboutPane      = 34

#===========Nex Assets================
AssetHellaAuto           = 32      
AssetHellaOn             = 33

AssetCruiseMain          = 79

AssetBSDOff              = 93
AssetSRFOff              = 94
AssetIce                 = 95

AssetPageMPH             = 26
AssetPageRPM             = 27
AssetPageGyro            = 28
AssetPageUltra           = 29
AssetPageSpeedDistance   = 31
AssetPageISet            = 30

AssetLeftLaneWhite       = 35
AssetLeftLaneBlue        = 36
AssetLeftLaneBlueRain    = 37
AssetLeftLaneGreen       = 38
AssetLeftLaneGreenRain   = 39
AssetLeftLaneYellow      = 40
AssetLeftLaneYellowRain  = 41
AssetLeftLaneRed         = 42
AssetRightLaneWhite      = 43
AssetRightLaneBlue       = 44
AssetRightLaneBlueRain   = 45
AssetRightLaneGreen      = 46
AssetRightLaneGreenRain  = 47
AssetRightLaneYellow     = 48
AssetRightLaneYellowRain = 49
AssetRightLaneRed        = 50

AssetACCruiseA           = 51
AssetACCruiseO           = 52
AssetCruiseA             = 53
AssetCruiseO             = 54

AssetFollowing           = 59
AssetFollowingHL         = 60
AssetFollowingRain       = 61
AssetFollowingHLRain     = 62

AssetHLLeftWhite         = 63
AssetHLLeftBlue          = 64
AssetHLLeftBlueRain      = 65
AssetHLLeftGreen         = 66
AssetHLLeftGreenRain     = 67
AssetHLLeftYellow        = 68
AssetHLLeftYellowRain    = 69
AssetHLLeftRed           = 70
AssetHLRightWhite        = 71
AssetHLRightBlue         = 72
AssetHLRightBlueRain     = 65
AssetHLRightGreen        = 66
AssetHLRightGreenRain    = 67
AssetHLRightYellow       = 68
AssetHLRightYellowRain   = 69
AssetHLRightRed          = 70

AssetMainBrake           = 81
AssetMainBrakeRainbow    = 82
AssetAEBBrake            = 83

AssetBSDLNorm            = 84
AssetBSDLBlue            = 85
AssetBSDLYell            = 86
AssetBSDRNorm            = 88
AssetBSDRBlue            = 89
AssetBSDRYell            = 90

AssetSysAlert            = 100
AssetParkBrake           = 101
AssetFuelNorm            = 102
AssetFuelLow             = 103
AssetTripA               = 104
AssetTripB               = 105

AssetESOff               = 106
AssetESOff_HL            = 107
AssetESCrit              = 108
AssetESCrit_HL           = 109

AssetLDWL_B              = 110
AssetLDWL_B_HL           = 111
AssetLDWL_B_FC           = 112
AssetLDWL_B_HL_FC        = 113
AssetLDWL_Y              = 114
AssetLDWL_Y_HL           = 115
AssetLDWL_Y_FC           = 116
AssetLDWL_Y_HL_FC        = 117
AssetLDWR_B              = 118
AssetLDWR_B_HL           = 119
AssetLDWR_B_FC           = 120
AssetLDWR_B_HL_FC        = 121 
AssetLDWR_Y              = 122
AssetLDWR_Y_HL           = 123
AssetLDWR_Y_FC           = 124
AssetLDWR_Y_HL_FC        = 125
AssetLDWL_B_Brake        = 126
AssetLDWL_Y_Brake        = 127
AssetLDWR_B_Brake        = 128
AssetLDWR_Y_Brake        = 129

AssetAEB1                = 130
AssetAEB2                = 131
AssetAEB3                = 132


AssetRCTA1               = 133
AssetRCTA2               = 134
AssetRCTAL               = 87
AssetRCTAR               = 91
ASSETRCTABrake           = 135

AssetPOPO1               = 141
AssetPOPO2               = 142
AssetPOPOBrake           = 143

AssetUpperRS             = 155


#########################################################################################################################
####################* FUNCTION START *###################################################################################
#########################################################################################################################
def GetSavedValues():
    global FuelVal
    global VarHella
    #global TrainVal
    global DayVal
    global NteVal
    global ODOVal
    global MPGVal
    global TripVal
    global TripaVal
    global TripbVal
    f=open("mydata/fuelval.txt", "r")  
    FuelVal = int(f.read())
    f=open("mydata/VarHella.txt", "r")  
    VarHella = int(f.read())
    #f=open("mydata/TrainVal.txt", "r")  
    #TrainVal = f.read()
    f=open("mydata/DayVal.txt", "r")  
    DayVal = f.read()
    f=open("mydata/NteVal.txt", "r")  
    NteVal = f.read()
    f=open("mydata/ODOVal.txt", "r")  
    ODOVal = f.read()
    f=open("mydata/MPGVal.txt", "r")  
    MPGVal = f.read()
    f=open("mydata/TripVal.txt", "r")  
    TripVal = f.read()
    f=open("mydata/TripaVal.txt", "r")  
    TripaVal = f.read()
    f=open("mydata/TripbVal.txt", "r")  
    TripbVal = f.read()
    printDebug("Saved Fuel Value: {}".format(FuelVal))
    printDebug("Saved Hella Value: {}".format(VarHella))
    printDebug("Saved Day Value: {}".format(DayVal))
    printDebug("Saved Nte Value: {}".format(NteVal))
    printDebug("Saved ODO Value: {}".format(ODOVal))
    printDebug("Saved Trip Value: {}".format(TripVal))
    printDebug("Saved Tripa Value: {}".format(TripaVal))
    printDebug("Saved Tripb Value: {}".format(TripbVal))
    printDebug("Saved MPG Value: {}".format(MPGVal))

def Update(page):
    global VarCurrentGear
    global sysStartup
    global TripVal
    localCounter = 0
    nextSequence = False
    if(page == "B"):
        SetTrip(TripVal)
        SetODO()
        TimeThread()
    elif(page == "P"):
        TimeThread(1)
        TempThread(1)
        SetHella(VarHella)
        SetMPG()
        SetTrip(TripVal)
        SetFuel(FuelVal)
        SetODO()
        SetBLAlerts(1, BSDOff, SRFOff, IceWarning)
        SetBRAlerts(1, sysAlert, parkBrake)
        while(VarCurrentGear == "P"):
            #BLAlertThread
            #ButtonThread
            #FuelThread
            #LightThread
            #PoPoThread
            time.sleep(1)
    elif(page == "D"):
        #Init
        TimeThread(1)
        TempThread(1)
        #SetHella(2)
        SetMPG()
        SetTrip(TripVal)
        SetFuel(FuelVal)
        SetODO()
        SetBLAlerts(1, BSDOff, SRFOff, IceWarning)
        SetBRAlerts(1, sysAlert, parkBrake)

        #tCruise.start()
        #tLight.start()
        
        #Loop
        while((VarCurrentGear == "R" or "N" or "D") or (VarCurrentGear.isdigit() == True)):
            
            lastKnownGear = "Z"

            #if(VarCurrentGear == "R"):
            #    if(lastKnownGear != VarCurrentGear):
            #        SetGear(VarCurrentGear)
            #        lastKnownGear = VarCurrentGear
            #    SendPic(NPicCenterPannel, AssetRCTA1)
            #    SendVis(NP, NPicCenterPannel, 1)
            #SendVis(NP, NPicCenterPannel, 0)

            if(VarCurrentGear == "N" or "D"): #or (VarCurrentGear.isdigit() == True)):
                VarCurrentGear = GearThread()
                if(lastKnownGear != VarCurrentGear):
                    SetGear(VarCurrentGear)
                    lastKnownGear = VarCurrentGear
                CruiseThread()
                LightThread()
                time.sleep(0.25)
                print('why am i here?')

            if(VarCurrentGear == "P"):
                print("im here")
                break
                        

def RefCenter():
    SendRef(NP, NPicCruiseState)
    SendRef(NT, NTextSetSpeed)
    SendRef(NT, NTextInfo)
    SendRef(NP, NPicLeftLane)
    SendRef(NP, NPicRightLane)
    SendRef(NP, NPicHeadlightLeft)
    SendRef(NP, NPicHeadlightRight)
    SendRef(NP, NPicCruiseMain)
    SendRef(NP, NPicCruise2)
    SendRef(NP, NPicCruise3)
    SendRef(NP, NPicCruise4)
    SendRef(NP, NPicBrakeMainAEB)

def SetHella(value=0):          #Hella Set Function  0-Off 1-Auto 2-On
    global VarHella
    if value == 0:   # If Set to Off
        SendVis(NP, NPicHella, 0)
    elif value == 1: # If Set to Auto
        SendVis(NP, NPicHella, 1)
        SendPic(NPicHella, AssetHellaAuto)
    elif value == 2: #If Set to On
        SendVis(NP, NPicHella, 1)
        SendPic(NPicHella, AssetHellaOn)
    
    VarHella = value
    printDebug("Updated Hella to state {}".format(value))

def SetPoPo(state=0):
    if(state == 1):
        SendVis(NP, NPicPOPO, 1)
    elif(state == 0):
        SendVis(NP, NPicPOPO, 0)

def SetBLAlerts(pageChange, temp1, SRF, ICE): #BL ALerts Set Function
    global shownBLAlerts
    global VarBSDOff
    global VarSRFOff
    global VarIceWarning

    BSDOff      = temp1
    SRFOff      = SRF
    IceWarning  = ICE
    if(pageChange == 1): #In The Event of a page change, Clear shownBLAlerts
        shownBLAlerts = 0
    
    #The Following mess looks through the 3 possible bottom left alerts in order of BSD OFF, SRF OFF, Ice Warning
    #And places them in available order in those spots. This is to make sure any appearing icons show from Left to right
    #BSDOff can only ever be poss 1, SRF Off can only be Poss 1 or 2, Ice can be any 3. We must first detrime what
    #Icons are active (done above), then work though the 3 possiablilities using thr shownBLAlerts counter as a sudo
    #Place holder. 
    #
    #EX. If only the Ice warning is active, when the code reaches (IceWarning == 1) The shownBLAlerts counter will
    #Be 0 and place the alert in posistion 1
    if(BSDOff == 1):    #If the BSDOff warning is an active warning
        SendPic(NPicBL1, AssetBSDOff)      #(place in pos1)
        printDebug("From BL Alerts: BSD Off")
        shownBLAlerts = shownBLAlerts + 1 #Increment counter
    if(SRFOff == 1):    #If the SRFOff warning is an active warning
        if(shownBLAlerts == 1):           #If One Shown Alert (place in pos2)
            SendPic(NPicBL2, AssetSRFOff)
        elif(shownBLAlerts == 0):         #If No other shown Alerts (place in pos1)
            SendPic(NPicBL1, AssetSRFOff)
        printDebug("From BL Alerts: SRF Off")
        shownBLAlerts = shownBLAlerts + 1 #Increment counter
    if(IceWarning == 1):    #If the Ice warning is an active warning
        if(shownBLAlerts == 2):           #If Two Shown Alerts (place in pos3)
            SendPic(NPicBL3, AssetIce)
        elif(shownBLAlerts == 1):         #If One Shown Alert (place in pos2)
            SendPic(NPicBL2, AssetIce)
        elif(shownBLAlerts == 0):         #If No other shown Alerts (place in pos1)
            SendPic(NPicBL1, AssetIce)
        printDebug("From BL Alerts: Ice Warning")
        shownBLAlerts = shownBLAlerts + 1 #Increment counter

    #Show the correct ammount of box's
    if(shownBLAlerts == 1):      # Show 1 BL Box
        SendVis(NP, NPicBL1, 1)
        SendVis(NP, NPicBL2, 0)
        SendVis(NP, NPicBL3, 0)
    elif(shownBLAlerts == 2):    # Show 2 BL Boxs
        SendVis(NP, NPicBL1, 1)
        SendVis(NP, NPicBL2, 1)
        SendVis(NP, NPicBL3, 0)
    elif(shownBLAlerts == 3):    # Show All 3 BL Boxs
        SendVis(NP, NPicBL1, 1)
        SendVis(NP, NPicBL2, 1)
        SendVis(NP, NPicBL3, 1)

def SetBRAlerts(pageChange, sys, park):       #BR Alerts Set Function
    global shownBRAlerts
    global sysAlert
    global parkBrake

    if(pageChange == 1): #In The Event of a page change, Clear shownBLAlerts
        shownBRAlerts = 0
    sysAlert = sys
    parkBrake = park

    #The Following mess looks through the 2 possible bottom right alerts in order of Parking Brake, Sys alert 
    #And places them in available order in those spots. This is to make sure any appearing icons show from Right to Left
    #ParkBrake can only ever be poss 1, and SysAlert can only be Poss 1 or 2. We must first detrime what
    #Icons are active (done above), then work though the 2 possiablilities using thr shownBRAlerts counter as a sudo
    #Place holder. 
    #
    #EX. If only the SysAlert is active, when the code reaches (SysAlert == 1) The shownBRAlerts counter will
    #Be 0 and place the alert in posistion 1
    if(parkBrake == 1):    #If the BSDOff warning is an active warning
        SendPic(NPicBR1, AssetParkBrake)      #(place in pos1)
        shownBRAlerts = shownBRAlerts + 1 #Increment counter
    if(sysAlert == 1):    #If the SRFOff warning is an active warning
        if(shownBRAlerts == 1):           #If One Shown Alert (place in pos2)
            SendPic(NPicBR2, AssetSysAlert)
        elif(shownBRAlerts == 0):         #If No other shown Alerts (place in pos1)
            SendPic(NPicBR1, AssetSysAlert)
        shownBRAlerts = shownBRAlerts + 1 #Increment counter

    #Show the correct ammount of box's
    if(shownBRAlerts == 1):      # Show 1 BL Box
        SendVis(NP, NPicBR1, 1)
        SendVis(NP, NPicBR2, 0)
    elif(shownBRAlerts == 2):    # Show 2 BL Boxs
        SendVis(NP, NPicBR1, 1)
        SendVis(NP, NPicBR2, 1)

def SetMPG(value=0):            #MPG Set Function 
    global MPGVal
    if(value == 0):
        SendVal(NT, NTextMPG, MPGVal)
    else:
        SendVal(NT, NTextMPG, value)
        MPGVal = value
    printDebug("Updated MPG to {} MPG".format(MPGVal))

def SetTrip(mode, value=0):     #Trip Set Function 
    global TripVal
    global TripaVal
    global TripbVal

    if(value == 0 and mode == "A"):
        value = TripaVal
    elif(value == 0 and mode == "A"):    
        value = TripbVal

    if(mode == "A"):   #TripA
        TripaVal = value
        SendVal(NT, NTextTrip, TripaVal)
        SendPic(NPicTrip, AssetTripA)
        printDebug("Updated Trip to {}: {}".format(TripVal, TripaVal))
    elif(mode == "B"): #TripB
        TripbVal = value
        SendVal(NT, NTextTrip, TripbVal)
        SendPic(NPicTrip, AssetTripB)
        printDebug("Updated Trip to {}: {}".format(TripVal, TripbVal))

def SetFuel(value=1000):        #Fuel Set Function
    global FuelVal
    if(value != 1000):
        FuelVal = value

    if(FuelVal <= 25): #Used when init is called to get the saved value from the stored variable
            SendVal(NT, NTextFuel, FuelVal)
            SendPic(NPicFuel, AssetFuelLow)
    elif(FuelVal >= 26):           #Used to pass in a value to set & save
            SendVal(NT, NTextFuel, FuelVal)
            SendPic(NPicFuel, AssetFuelNorm)
    printDebug("Updated Fuel to {}%".format(FuelVal))

def SetODO(value=0):            #ODO Set Function
    global ODOVal
    if (value != 0):
        ODOVal = value
    SendVal(NT, NTextODO, ODOVal)
    printDebug("Updated ODO {}".format(ODOVal))

def SetGear(gear):              #Gear Set Function
    global VarGear
    VarGear = gear
    SendVal(NT, NTextGear, VarGear)
    printDebug("Updated Gear {}".format (VarGear))

def PoPoShow():             #TODO Brakes
    global VarPOPO
    anicount = 0
    SendVis(NP, NPicCenterPannel, 1)
    while(anicount <= anishows/2):
        SendPic(NPicCenterPannel, AssetPOPO1)
        time.sleep(0.33)
        SendPic(NPicCenterPannel, AssetPOPO2)
        time.sleep(0.33)
        anicount = anicount +1
        printDebug("From POPO Show: Count {}/{}".format(anicount, anishows/2))
    time.sleep(0.75)
    VarPOPO = 1
    SendVis(NP, NPicRightLane, 1)
    SendVis(NP, NPicLeftLane, 1)
    printDebug("From POPO Show: DONE")

def LDWShow(mode):          #TODO Brakes # 1-Left 2-Right 3-Sway
    global VarHeadlight
    global VarFollowing
    anicount = 1
    
    while(anicount <= anishows):
        selectedFrame = 0
        frameEvenOdd = 0
        #Get the correct frame to display
        if (anicount % 2) == 0: #Even Frame
            frameEvenOdd = "E" 
            if(mode == 1):
                if(VarHeadlight == 1 and VarFollowing == 0):
                    selectedFrame = AssetLDWL_Y_HL
                elif(VarHeadlight == 0 and VarFollowing == 1):
                    selectedFrame = AssetLDWL_Y_FC
                elif(VarHeadlight == 1 and VarFollowing == 1):
                    selectedFrame = AssetLDWL_Y_HL_FC
                elif(VarHeadlight == 0 and VarFollowing == 0):
                    selectedFrame = AssetLDWL_Y
            elif(mode == 2):
                if(VarHeadlight == 1 and VarFollowing == 0):
                    selectedFrame = AssetLDWR_Y_HL
                elif(VarHeadlight == 0 and VarFollowing == 1):
                    selectedFrame = AssetLDWR_Y_FC
                elif(VarHeadlight == 1 and VarFollowing == 1):
                    selectedFrame = AssetLDWR_Y_HL_FC
                elif(VarHeadlight == 0 and VarFollowing == 0):
                    selectedFrame = AssetLDWR_Y
            elif(mode == 3):
                if(VarHeadlight == 1 and VarFollowing == 0):
                    selectedFrame = AssetLDWR_Y_HL
                elif(VarHeadlight == 0 and VarFollowing == 1):
                    selectedFrame = AssetLDWR_Y_FC
                elif(VarHeadlight == 1 and VarFollowing == 1):
                    selectedFrame = AssetLDWR_Y_HL_FC
                elif(VarHeadlight == 0 and VarFollowing == 0):
                    selectedFrame = AssetLDWR_Y
        else:                   #Odd Frame 
            frameEvenOdd =  "O"  
            if(mode == 1):
                if(VarHeadlight == 1 and VarFollowing == 0):
                    selectedFrame = AssetLDWL_B_HL
                elif(VarHeadlight == 0 and VarFollowing == 1):
                    selectedFrame = AssetLDWL_B_FC
                elif(VarHeadlight == 1 and VarFollowing == 1):
                    selectedFrame = AssetLDWL_B_HL_FC
                elif(VarHeadlight == 0 and VarFollowing == 0):
                    selectedFrame = AssetLDWL_B
            elif(mode == 2):
                if(VarHeadlight == 1 and VarFollowing == 0):
                    selectedFrame = AssetLDWR_B_HL
                elif(VarHeadlight == 0 and VarFollowing == 1):
                    selectedFrame = AssetLDWR_B_FC
                elif(VarHeadlight == 1 and VarFollowing == 1):
                    selectedFrame = AssetLDWR_B_HL_FC
                elif(VarHeadlight == 0 and VarFollowing == 0):
                    selectedFrame = AssetLDWR_B

            elif(mode == 3):
                if(VarHeadlight == 1 and VarFollowing == 0):
                    selectedFrame = AssetLDWL_Y_HL
                elif(VarHeadlight == 0 and VarFollowing == 1):
                    selectedFrame = AssetLDWL_Y_FC
                elif(VarHeadlight == 1 and VarFollowing == 1):
                    selectedFrame = AssetLDWL_Y_HL_FC
                elif(VarHeadlight == 0 and VarFollowing == 0):
                    selectedFrame = AssetLDWL_Y

        SendPic(30, selectedFrame)
        SendVis(NP, 30, 1)
        time.sleep(0.33)
        printDebug("FROM LDW ANIMATION {}: {} -Count {}/{} -Frame {}".format(mode, frameEvenOdd, anicount, anishows, selectedFrame))
        anicount = anicount +1
    time.sleep(0.75)
    SendVis(NP, NPicLeftLane, 1)
    SendVis(NP, NPicRightLane, 1)
    printDebug("FROM LDW ANIMATION {}: DONE".format(mode))

def RCTAShow(mode):
    global VarBrake
    anicount = 1
    SendPic(NPicCenterPannel, AssetRCTA2)
    while(anicount <= anishows+2):
        selectedFrame = 0
        frameEvenOdd = 0
        #Get the correct frame to display
        if (anicount % 2) == 0: #Even Frame
            frameEvenOdd = "E" 
            if(mode == "L"):
                SendPic(NPicBSDRCTAL, AssetRCTAL)
                SendVis(NP, NPicBSDRCTAL, 1)
            elif(mode == "R"):
                SendPic(NPicBSDRCTAR, AssetRCTAR)
                SendVis(NP, NPicBSDRCTAR, 1)
        else:                   #Odd Frame 
            frameEvenOdd =  "O"  
            if(mode == "L"):
                SendRef(NP, NPicCenterPannel)
                SendRef(NP, NPicBrakePOPORCTA)
            elif(mode == "R"):
                SendRef(NP, NPicCenterPannel)
                SendRef(NP, NPicBrakePOPORCTA)

        VarBrake = 0
        LightThread("R")
        time.sleep(0.22)
        printDebug("FROM RCTA ANIMATION {}: {} -Count {}/{}".format(mode, frameEvenOdd, anicount, anishows+2))
        anicount = anicount +1
    SendVis(NP, NPicBSDRCTAL, 0)
    SendVis(NP, NPicBSDRCTAR, 0)
    time.sleep(1)
    SendPic(NPicCenterPannel, AssetRCTA1)
    SendRef(NP, NPicBrakePOPORCTA)
    
def AEBShow():              #TODO BRAKES
    anicount = 1

    while(anicount <= anishows):
        selectedFrame = 0
        frameEvenOdd = 0
        #Get the correct frame to display
        if (anicount % 2) == 0: #Even Frame
            frameEvenOdd = "E"
            selectedFrame = AssetAEB1 
        else:                   #Odd Frame
            frameEvenOdd = "O"
            selectedFrame = AssetAEB3

        SendPic(30, selectedFrame)
        SendVis(NP, 30, 1)
        time.sleep(0.33)
        printDebug("FROM AEB ANIMATION: {} -Count {}/{} -Frame {}".format(frameEvenOdd, anicount, anishows, selectedFrame))
        anicount = anicount +1
    time.sleep(0.75)
    SendVis(NP, NPicLeftLane, 1)
    SendVis(NP, NPicRightLane, 1)
    printDebug("FROM AEB ANIMATION: DONE")

def EyeSightShow(command):               # 0-Clear 1-Off 2-Critical
    global VarHeadlight
    if(command == 0):   #Clear
        SendPic(NPicLeftLane, AssetLeftLaneWhite)
        SendPic(NPicRightLane, AssetRightLaneWhite)
    elif(command == 1): #Cant See/Off
        SendPic(NPicLeftLane, AssetESOff)
    elif(command == 2): #Critical Fail
        SendPic(NPicLeftLane, AssetESCrit)
    printDebug("EyeSight Status: {}".format(command))

def SetCruise(state, headlight, setspeed, distance=0, following=0, brake=0): # 0-Off 1-StdOn 2-StdActive 3-AdaOn 4-AdaActive #CLEANME
    global VarIsRainbow
    
    if(state == 0): #Clear
        SetLaneLight("LR", "white")
        if(headlight == 1):
            SetHeadlight("LR", "white")
        SendVis(NP, NPicCruiseState, 0)
        SendVis(NT, NTextSetSpeed, 0)
        SendVis(NP, NPicFollowingCar, 0)
        SetCruiseDist()  
        if(brake == 1):
            SetBrake("main")  
    elif(state == 1): #Standard On
        SetLaneLight("LR", "white")
        if(headlight == 1):
            SetHeadlight("LR", "white")
        SendPic(NPicCruiseState, AssetCruiseO)
        SendVis(NP, NPicCruiseState, 1)
        SetCruiseSpeed(setspeed)
        SendVis(NP, NPicFollowingCar, 0)
        SetCruiseDist()
        if(brake == 1):
            SetBrake("main") 
    elif(state == 2): #Standard Active
        SetLaneLight("LR", "white")
        if(headlight == 1):
            SetHeadlight("LR", "white")
        SendPic(NPicCruiseState, AssetCruiseA)
        SendVis(NP, NPicCruiseState, 1)
        SetCruiseSpeed(setspeed)
        SendVis(NP, NPicFollowingCar, 0)
        SetCruiseDist()  
        if(brake == 1):
            SetBrake("main") 
    elif(state == 3): #Adaptive On
        SetLaneLight("LR", "white")
        if(headlight == 1):
            SetHeadlight("LR", "white")
        SendPic(NPicCruiseState, AssetACCruiseO)   
        SendVis(NP, NPicCruiseState, 1)                    #SOMEWHERE SETTING BRAKES TO OFF WHEN COME FROM 4 to any
        SetCruiseSpeed(setspeed)
        SendVis(NP, NPicFollowingCar, 0)
        SetCruiseDist(distance)
        if(brake == 1):
            SetBrake("main")  
            time.sleep(3)
    elif(state == 4): #Adaptive Active
        SetLaneLight("LR", "blue")
        if(headlight == 1):
            SetHeadlight("LR", "blue")
        SendPic(NPicCruiseState, AssetACCruiseA)
        SendVis(NP, NPicCruiseState, 1)
        SetCruiseSpeed(setspeed)
        SetCruiseDist(distance) 
        if(brake == 1):
            SetBrake("main") 
        if(following == 1):
            SetFollowing(headlight)

    SendRef(NP, NPicBSDRCTAL)
    SendRef(NP, NPicBSDRCTAR)
    SendRef(NT, NTextInfo)
    printDebug("Updated cruise to state: {}".format(state))

def SetLaneLight(side, color): #TODO
    global VarIsRainbow
    if(side == "LR"):   #All Lines
        if(color == "white"):
            SendPic(NPicLeftLane , AssetLeftLaneWhite)
            SendPic(NPicRightLane, AssetRightLaneWhite)
        elif(color == "blue" and VarIsRainbow == 0):
            SendPic(NPicLeftLane , AssetLeftLaneBlue)
            SendPic(NPicRightLane, AssetRightLaneBlue)
        elif(color == "blue" and VarIsRainbow == 1):
            SendPic(NPicLeftLane , AssetLeftLaneBlueRain)
            SendPic(NPicRightLane, AssetRightLaneBlueRain)
    elif(side == "L"): #Left Line
        if(color == "green" and VarIsRainbow == 0):
            pass
        elif(color == "green" and VarIsRainbow == 1):
            pass
        elif(color == "yellow" and VarIsRainbow == 0):
            pass
        elif(color == "yellow" and VarIsRainbow == 1):
            pass
        elif(color == "red"):
            pass
    elif(side == "R"): #Right Line
        if(color == "green" and VarIsRainbow == 0):
            pass
        elif(color == "green" and VarIsRainbow == 1):
            pass
        elif(color == "yellow" and VarIsRainbow == 0):
            pass
        elif(color == "yellow" and VarIsRainbow == 1):
            pass
        elif(color == "red"):
            pass
    printDebug("{} Lane(s) set to {}: Rainbow {}".format(side, color, VarIsRainbow))
    
def SetCruiseDist(value=0):             #Pass in distance to set or noting to clear
    global VarCruiseState
    if(value == 1 and VarCruiseState >= 3):    #Distance 1
        SendVis(NP, NPicCruiseMain, 1)
        SendVis(NP, NPicCruise2, 0)
        SendVis(NP, NPicCruise3, 0)
        SendVis(NP, NPicCruise4, 0)
    elif(value == 2 and VarCruiseState >= 3):  #Distance 2
        SendVis(NP, NPicCruiseMain, 1)
        SendVis(NP, NPicCruise2, 1)
        SendVis(NP, NPicCruise3, 0)
        SendVis(NP, NPicCruise4, 0)
    elif(value == 3 and VarCruiseState >= 3):  #Distance 3
        SendVis(NP, NPicCruiseMain, 1)
        SendVis(NP, NPicCruise2, 1)
        SendVis(NP, NPicCruise3, 1)
        SendVis(NP, NPicCruise4, 0)
    elif(value == 4 and VarCruiseState >= 3):  #Distance 4
        SendVis(NP, NPicCruiseMain, 1)
        SendVis(NP, NPicCruise2, 1)
        SendVis(NP, NPicCruise3, 1)
        SendVis(NP, NPicCruise4, 1)
    else:              #Hide
        SendVis(NP, NPicCruiseMain, 0)
        SendVis(NP, NPicCruise2, 0)
        SendVis(NP, NPicCruise3, 0)
        SendVis(NP, NPicCruise4, 0)

def SetCruiseSpeed(setspeed=225):       #Pass in Set Speed or nothing to clear
    if(setspeed!=255):
        SendVal(NT, NTextSetSpeed, setspeed)
        SendVis(NT, NTextSetSpeed, 1)
        printDebug("Set cruise set speed to {}".format(setspeed))
    else:
        SendVal(NT, NTextSetSpeed, "--")
        SendVis(NT, NTextSetSpeed, 0)
        printDebug("Removed cruise set speed")

def SetHeadlight(side, color="white"): #TODO
    global VarIsRainbow
    if(side == "LR"):   #All Lines
        if(color == "white"):
            SendPic(NPicHeadlightLeft , AssetHLLeftWhite)
            SendPic(NPicHeadlightRight, AssetHLRightWhite)
        elif(color == "blue" and VarIsRainbow == 0):
            SendPic(NPicHeadlightLeft , AssetHLLeftBlue)
            SendPic(NPicHeadlightRight, AssetHLRightBlue)
        elif(color == "blue" and VarIsRainbow == 1):
            SendPic(NPicHeadlightLeft , AssetHLLeftBlueRain)
            SendPic(NPicHeadlightRight, AssetHLRightBlueRain)
    elif(side == "L"): #Left Line
        if(color == "green" and VarIsRainbow == 0):
            pass
        elif(color == "green" and VarIsRainbow == 1):
            pass
        elif(color == "yellow" and VarIsRainbow == 0):
            pass
        elif(color == "yellow" and VarIsRainbow == 1):
            pass
        elif(color == "red"):
            pass
    elif(side == "R"): #Right Line
        if(color == "green" and VarIsRainbow == 0):
            pass
        elif(color == "green" and VarIsRainbow == 1):
            pass
        elif(color == "yellow" and VarIsRainbow == 0):
            pass
        elif(color == "yellow" and VarIsRainbow == 1):
            pass
        elif(color == "red"):
            pass
    
    if(side != "C"):   #ShowAssets
        SendVis(NP, NPicHeadlightLeft , 1)
        SendVis(NP, NPicHeadlightRight, 1)
        printDebug("{} HeadLight(s) set to {}: Rainbow {}".format(side, color, VarIsRainbow))
    elif(side == "C"): #Clear
        SendVis(NP, NPicHeadlightLeft , 0)
        SendVis(NP, NPicHeadlightRight, 0)
        printDebug("Headlights Switched Off")

    SendRef(NP, NPicCruiseMain)
    SendRef(NP, NPicCruise2)
    SendRef(NP, NPicCruise3)

def SetFollowing(headlight, clear=0):          #Pass in headlight, or nothing to clear following car
    global VarIsRainbow
    #If there was a passed in value (only passed a binary 1 or 0)
    if(clear == 0):
        #If no headlight or rainbow road
        if(headlight == 0 and VarIsRainbow == 0):
            SendPic(NPicFollowingCar, AssetFollowing)
        #If Headlight and no rainbow road
        elif(headlight == 1 and VarIsRainbow == 0):
            SendPic(NPicFollowingCar, AssetFollowingHL)
        #If no headlight but rainbow road
        elif(headlight == 0 and VarIsRainbow == 1):
            SendPic(NPicFollowingCar, AssetFollowingRain)
        #If Headlight and rainbow road
        elif(headlight == 1 and VarIsRainbow == 1):
            SendPic(NPicFollowingCar, AssetFollowingHLRain)

        SendVis(NP, NPicFollowingCar, 1)
        printDebug("Set Following car")
    #If no value was passed in, clear following car
    else:
        SendVis(NP, NPicFollowingCar, 0)
        SendPic(NPicFollowingCar, AssetFollowing)
        printDebug("Removed Following car")

def SetBrake(mode="z", frame=0):
    global VarIsRainbow
    global VarCruiseState
    statetext = ""
    if(mode == "main" and VarCruiseState <= 4):
        SendPic(NPicBrakeMainAEB, AssetMainBrake)
        SendVis(NP, NPicBrakeMainAEB, 1)
        statetext = ("main - ON")
    elif(mode == "main" and VarCruiseState == 4 and VarIsRainbow == 1):
        SendPic(NPicBrakeMainAEB, AssetMainBrakeRainbow)
        SendVis(NP, NPicBrakeMainAEB, 1)
        statetext = ("main with rainbow")
    elif(mode == "aeb"):
        SendPic(NPicBrakeMainAEB, AssetAEBBrake)
        SendVis(NP, NPicBrakeMainAEB, 1)
        statetext = ("AEB")
    elif(mode == "ldwl"):
        if(frame % 2): #Even Frame (Yellow)
            SendPic(NPicBrakeMainAEB, AssetLDWL_Y_Brake)
            SendVis(NP, NPicBrakeLDW, 1)
            statetext = ("LDWL Yellow")
        else:          #Odd Frame (Blue)
            SendPic(NPicBrakeMainAEB, AssetLDWL_B_Brake)
            SendVis(NP, NPicBrakeLDW, 1)
            statetext = ("LDWL Blue")
    elif(mode == "ldwr"):
        if(frame % 2): #Even Frame (Yellow)
            SendPic(NPicBrakeMainAEB, AssetLDWR_Y_Brake)
            SendVis(NP, NPicBrakeLDW, 1)
            statetext = ("LDWR Yellow")
        else:          #Odd Frame (Blue)
            SendPic(NPicBrakeMainAEB, AssetLDWR_B_Brake)
            SendVis(NP, NPicBrakeLDW, 1)
            statetext = ("LDWR Blue")
    elif(mode == "popo"):
        SendPic(NPicBrakeMainAEB, AssetPOPOBrake)
        SendVis(NP, NPicBrakePOPORCTA, 1)
        statetext = ("POPO")
    elif(mode == "rcta"):
        SendPic(NPicBrakeMainAEB, ASSETRCTABrake)
        SendVis(NP, NPicBrakePOPORCTA, 1)
        statetext = ("RCTA")
    else:  
        SendVis(NP, NPicBrakeMainAEB, 0)
        SendVis(NP, NPicBrakeLDW, 0)
        SendVis(NP, NPicBrakePOPORCTA, 0)
        statetext = ("off")
    printDebug("Set brake status to {}".format(statetext))

def SetBSD(side, state="N"):              #TODO ADD LR LDW/SWAY ANI
    if(side == "L"):      #BSD Left
        if(state == "N"):     #Normal
            SendPic(NPicBSDRCTAL, AssetBSDLNorm)
            SendVis(NP, NPicBSDRCTAL, 1)
            SendVis(NP, NPicBSDRCTAR, 0)
        elif(state == "E"):   #Even frame (from LDW)
            SendPic(NPicBSDRCTAL, AssetBSDLYell)
            SendVis(NP, NPicBSDRCTAL, 1)
            SendVis(NP, NPicBSDRCTAR, 0)
        elif(state == "O"):   #Odd frame (from LDW)
            SendPic(NPicBSDRCTAL, AssetBSDLBlue)
            SendVis(NP, NPicBSDRCTAL, 1)
            SendVis(NP, NPicBSDRCTAR, 0)
        elif(state == "C"):   #Cancel
            SendVis(NP, NPicBSDRCTAL, 0)
            SendVis(NP, NPicBSDRCTAR, 0)
    elif(side == "R"):    #BSD Left
        if(state == "N"):     #Normal
            SendPic(NPicBSDRCTAR, AssetBSDRNorm)
            SendVis(NP, NPicBSDRCTAL, 0)
            SendVis(NP, NPicBSDRCTAR, 1)
        elif(state == "E"):   #Even frame (from LDW)
            SendPic(NPicBSDRCTAR, AssetBSDRYell)
            SendVis(NP, NPicBSDRCTAL, 0)
            SendVis(NP, NPicBSDRCTAR, 1)
        elif(state == "O"):   #Odd frame (from LDW)
            SendPic(NPicBSDRCTAR, AssetBSDRBlue)
            SendVis(NP, NPicBSDRCTAL, 0)
            SendVis(NP, NPicBSDRCTAR, 1)
        elif(state == "C"):   #Cancel
            SendVis(NP, NPicBSDRCTAL, 0)
            SendVis(NP, NPicBSDRCTAR, 0)
    elif(side == "LR"):
        if(state == "N"):     #Normal
            SendPic(NPicBSDRCTAL, AssetBSDLNorm)
            SendPic(NPicBSDRCTAR, AssetBSDRNorm)
            SendVis(NP, NPicBSDRCTAL, 1)
            SendVis(NP, NPicBSDRCTAR, 1)
        elif(state == "E"):   #Even frame (from LDW) #TODO 
            SendPic(NPicBSDRCTAL, AssetBSDLYell)
            SendVis(NP, NPicBSDRCTAL, 1)
        elif(state == "O"):   #Odd frame (from LDW)  #TODO
            SendPic(NPicBSDRCTAL, AssetBSDLBlue)
            SendVis(NP, NPicBSDRCTAL, 1)
        elif(state == "C"):   #Cancel
            SendVis(NP, NPicBSDRCTAL, 0)
            SendVis(NP, NPicBSDRCTAR, 0)
    
    
    printDebug("Set BSD: {} - {}".format(side, state))

#########################################################################################################################
######################* Threads *########################################################################################
#########################################################################################################################
def RemoteStartThread():
    global isRemoteStarted
    time.sleep(1)
    isRemoteStarted = 0 # DEV EDIT ME
    return isRemoteStarted
    
def TimeThread(force=0):
    global hour
    global minn
    now = datetime.now()
    temptime = now.strftime("%M")
    if(temptime != minn or force == 1):
        hour = now.strftime("%I")
        minn = now.strftime("%M")
        SendVal(NT, NTextHour, hour)
        SendVal(NT, NTextMin, minn)
        printDebug("Update Time. F={}".format(force))

def TempThread(force=0):
    #global tTemp
    global temp
    cur_temp = 46
    if(cur_temp != temp or force == 1):
        temp = cur_temp
        SendVal(NT, NTextTemp, temp)
        printDebug("Update Temp. F={}".format(force))

    #tTemp = threading.Timer(3, TempThread)
    #tTemp.start()

def GearThread():
    global VarGear

    #CAN magic to read cruise state
    f=open("LiveTests/VarCurrentGear.txt", "r")  
    VarGear = str(f.read())

    return VarGear

def SpeedThread():
    global VarSpeed
    global VarTopPage
    #CAN/Ard magic to read Brake & Hella state
    f=open("LiveTests/VarSpeed.txt", "r")  
    ReadSpeed = int(f.read())

    if((VarTopPage == 1 or 3) and VarGear != "P"):
        if(ReadSpeed != VarSpeed):
            SendVal(NN, NNumCe, ReadSpeed)
    if(VarTopPage == 5):
        if(ReadSpeed != VarSpeed):
            SendVal(NN, NNumLe, ReadSpeed)
    VarSpeed = ReadSpeed
    

#########################################################################################################################
##################* Non Threading Threads *##############################################################################
#########################################################################################################################
def UpperThread():           #TODO DEV EDITS & ADD CAN
    global VarTopPage
    global VarHella
    global VarPOPO
    global HideHella
    global HidePoPo
    global pageOveride
    lastKnownPage = 1
    updateHella   = 2
    updatePoPo    = 2 

    #Get steering wheel controls
    f=open("LiveTests/VarControls.txt", "r")   
    SelectedPage = int(f.read())
    if(pageOveride != 0):
        #printDebug("Page Override: {}".format(pageOveride))     TODO DEV UNREMERK ME!!
        SelectedPage = pageOveride
        #pageOveride = 0                                         TODO DEV UNREMERK ME!!
    f=open("mydata/VarHella.txt", "r")  
    ReadVarHella = int(f.read())
    f=open("LiveTests/VarPopo.txt", "r")  
    ReadVarPoPo = int(f.read())

    #Set Hella if changed
    if(ReadVarHella != VarHella and HideHella == 0):
        SetHella(ReadVarHella)
    #Set PoPo if changed
    if(ReadVarPoPo != VarPOPO and HidePoPo == 0):
        SetPoPo(ReadVarPoPo)

    #Pages checks & sets
    if(SelectedPage != VarTopPage):
        if(SelectedPage == 1):    #Speed
            SendPic(NPicUpperPannel, AssetPageMPH)
            SendVis(NN, NNumLe, 0)
            SendVis(NN, NNumCe, 1)
            SendVis(NN, NNumRi, 0)
            updateHella = 1
            HideHella   = 0
            updatePoPo  = 1
            HidePoPo    = 0
            SendRef(NT, NTextTemp)
            SendRef(NT, NTextHour)
            SendRef(NT, NTextMin)
            SpeedThread()
        elif(SelectedPage == 2):  #RPM
            SendPic(NPicUpperPannel, AssetPageRPM)
            SendVis(NN, NNumLe, 0)
            SendVis(NN, NNumCe, 1)
            SendVis(NN, NNumRi, 0)
            updateHella = 1
            HideHella   = 0
            updatePoPo  = 1
            HidePoPo    = 0
            SendVis(NT, NTextTemp, 1)
            SendVis(NT, NTextHour, 1)
            SendVis(NT, NTextMin, 1)
            #RPMThread()
        elif(SelectedPage == 3):  #Gyro
            SendPic(NPicUpperPannel, AssetPageGyro)
            SendVis(NN, NNumLe, 1)
            SendVis(NN, NNumCe, 1)
            SendVis(NN, NNumRi, 1)
            updateHella = 0
            HideHella   = 1
            updatePoPo  = 0
            HidePoPo    = 1
            SendVis(NT, NTextTemp, 0)
            SendVis(NT, NTextHour, 0)
            SendVis(NT, NTextMin, 0)
        elif(SelectedPage == 4):  #UltraSonic
            SendPic(NPicUpperPannel, AssetPageUltra)
            SendVis(NN, NNumLe, 1)
            SendVis(NN, NNumCe, 0)
            SendVis(NN, NNumRi, 1)
            updateHella = 0
            HideHella   = 1
            updatePoPo  = 0
            HidePoPo    = 1
            SendVis(NT, NTextTemp, 1)
            SendVis(NT, NTextHour, 1)
            SendVis(NT, NTextMin, 1)
        elif(SelectedPage == 5):  #Front Distance (unused)
            SendPic(NPicUpperPannel, AssetPageSpeedDistance)
            SendVis(NN, NNumLe, 1)
            SendVis(NN, NNumCe, 1)
            SendVis(NN, NNumRi, 0)
            updateHella = 0
            HideHella   = 1
            updatePoPo  = 1
            HidePoPo    = 0
            SendRef(NT, NTextTemp)
            SendRef(NT, NTextHour)
            SendRef(NT, NTextMin)
        elif(SelectedPage == 6):  #I/Set
            SendPic(NPicUpperPannel, AssetPageISet)
            SendVis(NN, NNumLe, 0)
            SendVis(NN, NNumCe, 0)
            SendVis(NN, NNumRi, 0)
            updateHella = 0
            HideHella   = 1
            updatePoPo  = 0
            HidePoPo    = 1
            SendRef(NT, NTextTemp)
            SendRef(NT, NTextHour)
            SendRef(NT, NTextMin)
    
        if(updateHella == 1 and HideHella != 1):
            SetHella(ReadVarHella)
        elif(updateHella == 0 or HideHella == 1):
            SetHella()
        if(updatePoPo == 1 and HidePoPo != 1):
            SetPoPo(ReadVarPoPo)
        elif(updatePoPo == 0 or HidePoPo == 1):
            SetPoPo()
        printDebug("Changed Selected page to: {}".format(SelectedPage))

    VarTopPage = SelectedPage
    VarHella = ReadVarHella
    VarPOPO  = ReadVarPoPo   

def MillageThread():         #TODO
    pass
    #Can Magic to get OBO
    #ODOVal = CanMagic
    #Can Magic to get Trip
    #if(TripVal == 1):
        #TripaVal = CanMagic
    #else:
        #TripbVal = CanMagic
    #Can Magic to get Fuel
    #FuelVal = CanMagic()

    #write values to save files
    #f = open("../odo.txt", "r")
    #for x in f:
        #print(x)

def CruiseThread():          #Handles everything cruise status! (State, Set Speed, Following Car, Set Distance)
    #0-Off 1-StandardOn 2-StandardActive 3-AdaptiveOn 4-AdaptiveActive
    global VarCruiseState
    global VarCruiseDist
    global VarCruiseSetSpeed
    global VarHeadlight
    global VarCruiseFollowing
    global VarIsRainbow
    global VarBrake

    #CAN magic to read cruise state
    f=open("LiveTests/VarCruiseState.txt", "r")  
    ReadVarCruiseState = int(f.read())
    f=open("LiveTests\VarCruiseDist", "r")  
    ReadVarCruiseDist = int(f.read())
    f=open("LiveTests/VarCruiseSetSpeed.txt", "r")  
    ReadVarCruiseSetSpeed = int(f.read())
    f=open("LiveTests/VarCruiseFollowing.txt", "r")  
    ReadVarCruiseFollowing = int(f.read())
    f=open("LiveTests/VarIsRainbow.txt", "r")  
    ReadVarIsRainbow = int(f.read())

    #If read cruise state changed from previous stored  
    if(VarCruiseState != ReadVarCruiseState):
        SetCruise(ReadVarCruiseState, VarHeadlight, ReadVarCruiseSetSpeed, ReadVarCruiseDist, 
        ReadVarCruiseFollowing, VarBrake)
    elif(VarCruiseFollowing != ReadVarCruiseFollowing and VarCruiseState == 4):
        if(ReadVarCruiseFollowing == 1):
            SetFollowing(VarHeadlight)
        else:
            SetFollowing(VarHeadlight, 1)
    elif(VarCruiseDist != ReadVarCruiseDist):
        SetCruiseDist(ReadVarCruiseDist)
    elif(VarCruiseSetSpeed != ReadVarCruiseSetSpeed):
        SetCruiseSpeed(ReadVarCruiseSetSpeed)
    #Assign to global vars
    VarCruiseState     = ReadVarCruiseState 
    VarCruiseDist      = ReadVarCruiseDist
    VarCruiseSetSpeed  = ReadVarCruiseSetSpeed
    VarCruiseFollowing = ReadVarCruiseFollowing
    VarIsRainbow       = ReadVarIsRainbow

def CarStatsThread():
    pass

def LightThread(option="Z"): # TODO For HL & Brakes REMEMBER to include all headlight options, (like ES OFF)
    global VarHeadlight
    global VarBrake
    global VarHella
    global VarCruiseState
    global VarTopPage

    #CAN/Ard magic to read Brake & Hella state
    f=open("LiveTests/VarHeadlight.txt", "r")  
    ReadVarHeadlight = int(f.read())
    f=open("LiveTests/VarBrake.txt", "r")  
    ReadVarBrake = int(f.read())

    if(ReadVarHeadlight != VarHeadlight and option == "Z"):
        printDebug("HL")
        if(VarCruiseState == 4):
            SetHeadlight("LR", "blue")
        elif(VarCruiseState <= 3):
            SetHeadlight("LR")
        else:
            SetHeadlight()
        SendRef(NP, NPicFollowingCar)
    if(ReadVarBrake != VarBrake):
        if(option == "Z"):
            if(ReadVarBrake == 1 and VarIsRainbow == 0):
                SetBrake("main", 0)
            elif(ReadVarBrake == 1 and VarIsRainbow == 1):
                SetBrake("main")
            else:
                SetBrake()
        elif(option == "R"):
            if(ReadVarBrake == 1):
                SetBrake("rcta")
            else:
                SetBrake()
    

    VarHeadlight = ReadVarHeadlight
    VarBrake = ReadVarBrake

def AlertThread():
    pass

def BottomAlertThread():
    global VarBSDOff
    global VarSRFOff
    global VarIceWarning
    global VarSysAlert
    global VarParkBrake

    #CAN/Ard magic to read Brake & Hella state
    f=open("LiveTests/VarBSDOff.txt", "r")  
    ReadVarBSDOff = int(f.read())
    f=open("LiveTests/VarSRFOff.txt", "r")  
    ReadVarSRFOff = int(f.read())
    f=open("LiveTests/VarIceWarning.txt", "r")  
    ReadVarIceWarning = int(f.read())
    f=open("LiveTests/VarSysAlert.txt", "r")  
    ReadVarSysAlert = int(f.read())
    f=open("LiveTests/VarParkBrake.txt", "r")  
    ReadVarParkBrake = int(f.read())

def ArduinoThread():
    pass

def ADASThread():      #TODO
    pass

def UltraSonicThread(): #TODO
    global VarFrontUS
    global VarRearUS

    f=open("LiveTests/VarFrontUltrasonic.txt", "r")  
    ReadBSD = int(f.read())
    f=open("LiveTests/VarRearUltrasonic.txt", "r")  
    ReadBSD = int(f.read())

def RadarThread(isLDW="Z"):
    global VarGear
    global VarBSD
    global VarRCTA
    global driveGearsList

    #CAN/Ard magic to read Brake & Hella state
    f=open("LiveTests/VarBSD.txt", "r")  
    ReadBSD = str(f.read())
    f=open("LiveTests/VarRCTA.txt", "r")  
    ReadRCTA = int(f.read())

    #If being called from LDW
    if(isLDW == "E" or "O"):
        state = isLDW
    else:
        state = "N"
    
    #Do sumthin if BSD detected while in drive
    if(ReadBSD != VarBSD and VarGear in driveGearsList):
        VarBSD = ReadBSD
        if(ReadBSD != "0"):
            SetBSD(ReadBSD, "N") 
        elif(ReadBSD == "0"):
            SetBSD("LR", "C")

    #Do sumthin if RCTA detected while in reverse
    if(ReadRCTA != 0 and VarGear == "R"):
       RCTAShow(ReadRCTA)
    time.sleep(0.25)                       #TODO DELME USED CUZ FILES!!!!!!!

def OpenPilotThread():
    pass

def DoorThread():
    pass

def CloseThreads():
    global tTime
    global tTemp
    #tTime.cancel()
    #tTemp.cancel()
    #tSpeed.cancel
    printDebug("Closed All Threads... Will Resume...")


#########################################################################################################################
######################* Loops *##########################################################################################
#########################################################################################################################
def DemoLoop():
    whatDemo = "B"
    printDebug("RUNNING DEMO PROGRAM!!!!!")
    GetSavedValues()
    
   #Boot Sequence
    SendBright(100)
    SendPage(pageBoot)
    SetTrip(TripVal)
    SetODO()
    TimeThread(1)
    time.sleep(5)
    
   #Park Sequence
    SendPage(pagePark)
    time.sleep(3.5)
    TimeThread(1)
    TempThread(1)
    SetHella(1)
    SetPoPo(1)
    SetMPG()
    SetTrip(TripVal)
    SetFuel(FuelVal)
    SetODO()
    SetBLAlerts(1, 1, 1, 1)
    SetBRAlerts(1, 1, 1)
    time.sleep(5)
    
   #Drive Setup
    SendPage(pageDrive)
    TimeThread(1)
    TempThread(1)
    SetHella(1)
    SetGear("D")
    SetMPG()
    SetTrip(TripVal)
    SetFuel(FuelVal)
    SetODO()
    time.sleep(3)

   #Reverse
    SetGear("R")
    SendPic(NPicCenterPannel, AssetRCTA1)
    SendVis(NP, NPicCenterPannel, 1)
    SendVis(NP, NPicLeftLane, 0)
    SendVis(NP, NPicRightLane, 0)
    SendVis(NN, NNumCe, 0)
    SendVis(NP, NPicHella, 0)
    SendPic(NPicUpperPannel, AssetPageUltra)
    SendVal(NN, NNumLe, 12)
    SendVal(NN, NNumRi, 0)
    SendVis(NN, NNumLe, 1)
    SendVis(NN, NNumRi, 1)
    TimeThread(1)
    TempThread(1)
    time.sleep(5)
    RCTAShow("L")
    time.sleep(2)
    RCTAShow("R")
    time.sleep(2)
    #ADD ULTRASONIC DIST
    #time.sleep(2)
    SendPic(NPicUpperPannel, AssetPageMPH)
    SendRef(NP, NPicUpperPannel)
    SendVis(NN, NNumLe, 0)
    SendVis(NN, NNumCe, 1)
    SendVis(NN, NNumRi, 0)
    SendVis(NP, NPicHella, 1)
    SendPic(NPicLeftLane, AssetLeftLaneWhite)
    SendPic(NPicRightLane, AssetRightLaneWhite)
    #SendVis(NP, NPicCenterPannel, 0)
    SetGear("D")
    time.sleep(2)
    
   #Drive
    

   #Alerts Demo
    SendPage(pageDrive)
    time.sleep(1)
    VarHeadlight = 1
    VarFollowing = 1 
    LDWShow(1)
    time.sleep(1)
    VarHeadlight = 1
    VarFollowing = 0 
    LDWShow(2)
    time.sleep(1)
    VarHeadlight = 0
    VarFollowing = 0
    LDWShow(3)
    time.sleep(1)
    AEBShow()
    time.sleep(1)
    PoPoShow()
    time.sleep(1)
    EyeSightShow(1)
    time.sleep(3)
    EyeSightShow(2)
    time.sleep(3)
    EyeSightShow(0)
    time.sleep(3)

def WaitForStrt():   #TODO add arduino sinngling
    power = 0
    printDebug("Waiting to start.....")
    while(power == 0):
        #CArduino magic to read cruise state
        f=open("LiveTests/Pwr.txt", "r")  
        power = int(f.read())
        #pwr = ardMega.digital[10].read()
        #check doors, 
    printDebug("Starting program.....")
    Startup()

def Startup():  #TODO Remote start magic
    SendBright(100)
    SendPage(pageBoot)
    Update("B")
    if (RemoteStartThread() == 1):    ##TODO
        printDebug("Remote Started... Waiting here...")
        rsHold = True
        while(rsHold == True):
            #Do Door Checks for driver open then close
            time.sleep(3)
            rsHold = False
        SendPic(NPicUpperPannel, AssetUpperRS)
        SendVis(NP, NPicUpperPannel, 1)
        #Wait for brake press
        printDebug("Waiting for brake takeover...")
        time.sleep(3)
        printDebug("Takeover Complete!")
        SendVis(NP, NPicUpperPannel, 0)
    time.sleep(3)

def MainLoop():
    global VarGear
    global driveGearList
    global VarTopPage
    global pageOveride
    initRun = 1
    inBootLoop  = 0 
    inParkLoop  = 1
    inRevLoop   = 0
    inDriveLoop = 0
    
    while True:
        if(VarGear == "B"):
            pass

        elif(VarGear == "P"):
            tempCounter = 0
            tTime.start()
            #tGear.start()
            SendPage(pagePark)
            
            while(initRun == 1):     #Func working with Nex programing to wait for park ani if inital boot
                printDebug("Waiting for animation to complete:")
                while(tempCounter < 40):
                    if(GearThread() in driveGearsList):
                        #SendVal(NT, NTextGear, VarGear)
                        #SendVis(NT, NTextGear, 1)
                        inParkLoop = 0
                        inDriveLoop = 1
                        tempCounter = 100
                    tempCounter = tempCounter +1
                    time.sleep(0.1)
                initRun = 0
                
            if(tempCounter != 100):  #If above function catches "D" gear early, we can skip all this
                TimeThread(1)
                TempThread(1)
                SetHella(VarHella)
                SetMPG()
                SetTrip(TripVal)
                SetFuel(FuelVal)
                SetODO()
                SetBLAlerts(1, VarBSDOff, VarSRFOff, VarIceWarning)
                SetBRAlerts(1, VarSysAlert, VarParkBrake)
                printDebug("Park init done, starting loop:")
                while(inParkLoop == 1 and VarGear == "P"):
                    if( GearThread() == 'D'):
                        inParkLoop = 0
                        inDriveLoop = 1
                    #BLAlertThread
                    #ButtonThread
                    #FuelThread
                    #LightThread
                    #PoPoThread
                    VarGear = GearThread()
                    time.sleep(.33)
                    #CloseThreads()

        elif(VarGear == "R"):
            #Init
            lastKnownGear = "R"
            inRevLoop = 1
            SetGear(VarGear)
            SendPage(pageDrive)
            SendVal(NT, NTextGear, VarGear)
            TimeThread(1)
            TempThread(1)
            #SetHella(VarHella)
            SetMPG()
            SetTrip(TripVal)
            SetFuel(FuelVal)
            SetODO()
            SetBLAlerts(1, BSDOff, SRFOff, IceWarning)
            SetBRAlerts(1, sysAlert, parkBrake)

            SendPic(NPicCenterPannel, AssetRCTA1)
            SendVis(NP, NPicCenterPannel, 1)
            SendVis(NP, NPicLeftLane, 0)
            SendVis(NP, NPicRightLane, 0)
            reverseInit = 0
            pageOveride = 4
            printDebug("Reverse init Done, starting loop:")

            while(inRevLoop == 1):
                VarGear = GearThread()
                if(lastKnownGear != VarGear):
                    if(VarGear == "P"):
                        inParkLoop = 1
                    elif(VarGear == "N" or "D" or VarGear.isdigit() == True):
                        inDriveLoop = 1
                    SendVis(NP, NPicCenterPannel, 0)
                    SendVis(NP, NPicCenterPannel, 0)
                    SendVis(NP, NPicLeftLane, 1)
                    SendVis(NP, NPicRightLane, 1)
                    SetGear(VarGear)
                    inRevLoop = 0
                    lastKnownGear = VarGear
                SpeedThread()
                RadarThread()
                ADASThread()
                UpperThread()
                LightThread("R")
        
        elif(VarGear in driveGearsList):
            #Init
            lastKnownGear = "R"
            reverseInit = 1
            SetGear(VarGear)
            SendPage(pageDrive)
            SendVal(NT, NTextGear, VarGear)
            TimeThread(1)
            TempThread(1)
            #SetHella(VarHella)
            SetMPG()
            SetTrip(TripVal)
            SetFuel(FuelVal)
            SetODO()
            SetBLAlerts(1, BSDOff, SRFOff, IceWarning)
            SetBRAlerts(1, sysAlert, parkBrake)
            pageOveride = 1
            printDebug("Drive init Done, starting loop:")

            #tCruise.start()
            #tLight.start()
            #Loop
            while(inDriveLoop == 1):
                VarGear = GearThread()
                if not VarGear in driveGearsList and VarGear != "R":
                    inDriveLoop = 0
                    inParkLoop = 1
                elif(VarGear == "R"):
                    inDriveLoop = 0
                    inRevLoop = 1
                if(lastKnownGear != VarGear):
                    SetGear(VarGear)
                    reverseInit = 1
                    lastKnownGear = VarGear
                SpeedThread()
                RadarThread()
                ADASThread()
                CruiseThread()
                LightThread()
                UpperThread()
                time.sleep(0.25)




def Reverse():
    pass

#def Drive():
 #   SendPage(pageDrive)
 #   SendVal(NT, NTextGear, "D")
 #   Update("D")

def ComTest2(): #TODO
    #ardMega = pyfirmata.Arduino('COM8')

    #it = pyfirmata.util.Iterator(ardMega)
    #it.start()

    #ardMega.digital[10].mode = pyfirmata.INPUT

    while True:
        #ardMega.digital[13].write(1)
        #sw = ardMega.digital[10].read()
        #print(sw)
        time.sleep(1)
        #ardMega.digital[13].write(0)
        time.sleep(1)

#########################################################################################################################
####################* CODE START *#######################################################################################
#########################################################################################################################
tTime = multitimer.MultiTimer(interval=5, function=TimeThread, runonstart=False)
#tGear = multitimer.MultiTimer(interval=1, function=GearThread, runonstart=False)
tCruise = multitimer.MultiTimer(interval=1, function=CruiseThread, runonstart=False)
#tTemp = multitimer.MultiTimer(interval=10, function=TempThread, runonstart=False)
#tTspeed = multitimer.MultiTimer(interval=10, function=SpeedThread, runonstart=False)
tLight = multitimer.MultiTimer(interval=0.25, function=LightThread, runonstart=False)
#tAlert = multitimer.MultiTimer(interval=5, function=AlertThread, runonstart=False)

while True:
   DemoLoop()
   exit()

GetSavedValues()
WaitForStrt()
MainLoop()
#Park()
#Drive()






            #localCounter += 1

            # OLD STUFF
            #if(localCounter % 100 == 0): #Do Every 10 Seconds
            #    TimeThread()
            #    TempThread()
            #   MillageThread()   
            
            #SpeedThread()
            #nextSequence = GearThread()
            #ADASThread()
             #CruiseThread()
             #LightThread()
            #OpenPilotThread()
            #IndicatorThread()
            #AlertThread()
            #DoorThread()

            #time.sleep(0.100)
            #if(localCounter >= 100):
            #    localCounter = 0

        #localCounter = 0
        #nextSequence = False   