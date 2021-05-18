from datetime import datetime

debugMSGs = 1

def printDebug(msg):
    if debugMSGs == 1:
        now = datetime.now()
        debugtime = now.strftime("%m/%d %I:%M.%S")
        print("[Debug Msg ({})]: {}".format(debugtime, msg))