import sys
import os
import ac
import acsys
import time
from datetime import datetime

telemetryInstance = None


def clickNext(x, y):
    telemetryInstance.nextDriver()


def clickStart(x, y):
    telemetryInstance.startLogging()


class ACTelemetry:
    driversCount = 0
    carId = 0
    driverLabel = None
    currentStateLabel = None
    outputFile = None

    def __init__(self):
        self.driversCount = ac.getCarsCount()

        appWindow = ac.newApp('ACTelemetry')
        ac.setSize(appWindow, 200, 125)

        self.driverLabel = ac.addLabel(appWindow, self.getDriverString())
        ac.setPosition(self.driverLabel, 10, 35)

        self.currentStateLabel = ac.addLabel(appWindow, 'NOT Logging')
        ac.setPosition(self.currentStateLabel, 10, 60)

        nextButton = ac.addButton(appWindow, 'Next')
        ac.setPosition(nextButton, 5, 95)
        ac.setSize(nextButton, 92, 22)
        ac.addOnClickedListener(nextButton, clickNext)

        startButton = ac.addButton(appWindow, 'Start')
        ac.setPosition(startButton, 103, 95)
        ac.setSize(startButton, 92, 22)
        ac.addOnClickedListener(startButton, clickStart)

    def getDriverString(self):
        return str(self.carId) + ' : ' + ac.getDriverName(self.carId)

    def nextDriver(self):
        if self.outputFile != None:
            return

        self.carId = (self.carId + 1) % self.driversCount
        ac.setText(self.driverLabel, self.getDriverString())

    def startLogging(self):
        if self.outputFile != None:
            return

        ac.console('Start')
        ac.setText(self.currentStateLabel, 'Logging')

        # tmpFile.write('Course : {}\n'.format(ac.getTrackName(self.carId)))
        # tmpFile.write('Layout : {}\n'.format(ac.getTrackConfiguration(self.carId)))
        # tmpFile.write('Car Id : {}\n'.format(self.carId))
        # tmpFile.write('Driver : {}\n'.format(ac.getDriverName(self.carId)))
        # tmpFile.write('Driver : {}\n'.format(ac.getCarName(self.carId)))
        # tmpFile.write('\n')

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        trackName = ac.getTrackName(self.carId)
        trackConfiguration = ac.getTrackConfiguration(self.carId)
        carId = self.carId
        driverName = ac.getDriverName(self.carId)
        carName = ac.getCarName(self.carId)

        desktop_dir = os.path.expanduser('~/Desktop')
        tmpFile = open(desktop_dir + '/ACLog_{},{},{},{},{},{}.csv'.format(timestamp, trackName, trackConfiguration, carId, driverName, carName), mode='w')
        tmpFile.write(','.join(['timestamp', 'lapCount', 'lapTime', 'distance', 'speed', 'throttle', 'brake', 'gear', 'RPM', 'steer', 'x', 'y', 'z\n']))

        self.outputFile = tmpFile

    def close(self):
        self.outputFile.close()

    def logging(self):
        if self.outputFile == None:
            return

        timestamp = datetime.now().isoformat()
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

        self.outputFile.write('{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(timestamp, lapCount, lapTime, distance, speed, throttle, brake, gear, rpm, steer, x, y, z))


def acMain(ac_version):
    global telemetryInstance
    telemetryInstance = ACTelemetry()
    return 'ACTelemetry'


def acUpdate(deltaT):
    global telemetryInstance
    telemetryInstance.logging()


def acShutdown():
    global telemetryInstance
    telemetryInstance.close()
