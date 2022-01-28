from PyTado.interface import Tado
from datetime import datetime
import time
import threading

log = "tado-autoassist.log"
loginlist = [('user1@example.com', 'PASSWORD1'),
             ('user2@example.com', 'PASSWORD2')]
userlist = []


def login(user, secret):
    userdata = []
    userdata.append(Tado(user, secret))                     # user
    userdata.append(userdata[0].getZones())                 # zones
    userdata.append(userdata[0].getHomeState()["presence"])  # homestate
    return userdata


def autoassist(userdata):
    t = userdata[0]
    zones = userdata[1]

    # Open Window Detection
    for zone in zones:
        try:
            iswindowopenzone = t.getOpenWindowDetected(
                zone["id"])["openWindowDetected"]
        except Exception as e:
            writeToLog("An Error Occurred: " + str(e))
            iswindowopenzone = False
        if iswindowopenzone:
            writeToLog("Open Window in '"
                       + zone["name"] + "' detected: Switching to open-window-mode.")
            try:
                t.setOpenWindow(zone["id"])
            except Exception as e:
                writeToLog("An Error Occurred: " + str(e))
    # Home and Away
    try:
        mobileDevices = t.getMobileDevices()
    except Exception as e:
        writeToLog("An Error Occurred: " + str(e))
        mobileDevices = []
    someonehome = False
    try:
        userdata[2] = t.getHomeState()["presence"]
    except Exception as e:
        writeToLog("An Error Occurred: " + str(e))
    for device in mobileDevices:
        if device["settings"]["geoTrackingEnabled"]:
            print("HomeState: "
                  + userdata[2] + ", Location at Home: " + str(device["location"]["atHome"]))
            if device["location"]["atHome"]:  # someone is home
                someonehome = True
                if (userdata[2] == "AWAY"):  # nobody home
                    writeToLog("Presence detected: Switching to home-mode.")
                    try:
                        t.setHome()
                    except Exception as e:
                        writeToLog("An Error Occurred: " + str(e))
                    else:
                        userdata[2] = "HOME"
    if not(someonehome) and userdata[2] == "HOME":
        writeToLog("Nobody home: Switching to away-mode.")
        try:
            t.setAway()
        except Exception as e:
            writeToLog("An Error Occurred: " + str(e))
        else:
            userdata[2] = "AWAY"
    return userdata


def syncHomeState():
    for user in userlist:
        try:
            user[2] = user[0].getHomeState()
        except Exception as e:
            writeToLog("An Error Occurred: " + str(e))


def writeToLog(msg):
    filelength = 10
    f = open(log, "a")
    with open(log, "r") as f:
        lines = f.readlines()
    with open(log, "w") as outfile:
        outfile.write("[" + str(datetime.now()) + "] " + msg + "\n")
        print("[" + str(datetime.now()) + "] " + msg)
        for index, line in enumerate(lines):
            if index < (filelength-1):
                outfile.write(line)


def action():
    for user in userlist:
        user = autoassist(user)


class setInterval:
    def __init__(self, interval, action):
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()):
            nextTime += self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()


for i in range(len(loginlist)):
    try:
        userlist.append(login(loginlist[i][0], loginlist[i][1]))
    except Exception as e:
        writeToLog(str(e))
        writeToLog("Critical error: Could not log into account. Stopping...")
        exit()


# start action every 10s
inter = setInterval(10, action)
# synchronize the HomeState every min
inter2 = setInterval(60, syncHomeState)
writeToLog('Py-Auto-Assist started!')
