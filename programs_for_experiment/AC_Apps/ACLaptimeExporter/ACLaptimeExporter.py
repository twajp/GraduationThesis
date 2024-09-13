import os
import ac
import acsys
from datetime import datetime

telemetryInstance = None
textInput = None


def clickLStart(x, y):
    telemetryInstance.setLaptime('left start,,')


def clickRStart(x, y):
    telemetryInstance.setLaptime('right start,,')


def clickEnd(x, y):
    telemetryInstance.setLaptime('end\n')


def clickEndCurve(x, y):
    telemetryInstance.setLaptime('end SlightCurve\n')


def clickEndNoCar(x, y):
    telemetryInstance.setLaptime('end Curve\n')


def onValidateListener(string):
    global textInput
    text = ac.getText(textInput)
    telemetryInstance.setLaptime('end {}\n'.format(text))


class ACLaptimeExporter:
    driversCount = 0
    carId = 0
    driverLabel = None
    outputFile = None

    def __init__(self):
        global textInput
        self.driversCount = ac.getCarsCount()

        appWindow = ac.newApp('ACLaptimeExporter')
        ac.setSize(appWindow, 200, 235)

        self.driverLabel = ac.addLabel(appWindow, self.getLaptime())
        ac.setPosition(self.driverLabel, 10, 35)

        startLButton = ac.addButton(appWindow, 'L Start')
        ac.setPosition(startLButton, 5, 75)
        ac.setSize(startLButton, 90, 25)
        ac.addOnClickedListener(startLButton, clickLStart)

        startRButton = ac.addButton(appWindow, 'R Start')
        ac.setPosition(startRButton, 105, 75)
        ac.setSize(startRButton, 90, 25)
        ac.addOnClickedListener(startRButton, clickRStart)

        endButton = ac.addButton(appWindow, 'End')
        ac.setPosition(endButton, 5, 110)
        ac.setSize(endButton, 190, 25)
        ac.addOnClickedListener(endButton, clickEnd)

        endCurveButton = ac.addButton(appWindow, 'End (sCurve)')
        ac.setPosition(endCurveButton, 5, 165)
        ac.setSize(endCurveButton, 90, 25)
        ac.addOnClickedListener(endCurveButton, clickEndCurve)

        endNoCar = ac.addButton(appWindow, 'End (Curve)')
        ac.setPosition(endNoCar, 105, 165)
        ac.setSize(endNoCar, 90, 25)
        ac.addOnClickedListener(endNoCar, clickEndNoCar)

        textInput = ac.addTextInput(appWindow, "TEXT_INPUT")
        ac.setPosition(textInput, 5, 200)
        ac.setSize(textInput, 190, 30)
        ac.addOnValidateListener(textInput, onValidateListener)

        self.startLogging()

    def getLaptime(self):
        laptime_ms = ac.getCarState(self.carId, acsys.CS.LapTime)
        laptime_str = datetime.fromtimestamp(laptime_ms / 1000)
        return '{}:{}:{}.{}'.format(str(laptime_str.hour-9).zfill(2), str(laptime_str.minute).zfill(2), str(laptime_str.second).zfill(2), str(laptime_str.microsecond).zfill(6))

    def setLaptime(self, description):
        ac.setText(self.driverLabel, self.getLaptime())
        self.logging(description)

    def startLogging(self):
        if self.outputFile != None:
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        desktop_dir = os.path.expanduser('~/Desktop')
        tmpFile = open(desktop_dir + '/ACLaptime_Late_{}.csv'.format(timestamp), mode='w')
        tmpFile.write(','.join(['lapCount', 'lapTime ms', 'lapTime str', 'distance', 'speed', 'throttle', 'brake', 'gear', 'RPM', 'steer', 'x', 'y', 'z', 'description\n']))

        self.outputFile = tmpFile

    def close(self):
        self.outputFile.close()

    def logging(self, description):
        if self.outputFile == None:
            return

        lapCount = ac.getCarState(self.carId, acsys.CS.LapCount) + 1
        lapTime = ac.getCarState(self.carId, acsys.CS.LapTime)
        speed = ac.getCarState(self.carId, acsys.CS.SpeedKMH)
        throttle = ac.getCarState(self.carId, acsys.CS.Gas)
        brake = ac.getCarState(self.carId, acsys.CS.Brake)
        gear = ac.getCarState(self.carId, acsys.CS.Gear)
        rpm = ac.getCarState(self.carId, acsys.CS.RPM)
        distance = ac.getCarState(self.carId, acsys.CS.NormalizedSplinePosition)
        steer = ac.getCarState(self.carId, acsys.CS.Steer)
        (x, y, z) = ac.getCarState(self.carId, acsys.CS.WorldPosition)

        self.outputFile.write('{},{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(lapCount, lapTime, self.getLaptime(), distance, speed, throttle, brake, gear, rpm, steer, x, y, z, description))


def acMain(ac_version):
    global telemetryInstance
    telemetryInstance = ACLaptimeExporter()
    return 'ACLaptimeExporter'


def acUpdate(deltaT):
    global telemetryInstance
    # telemetryInstance.logging()


def acShutdown():
    global telemetryInstance
    telemetryInstance.close()
