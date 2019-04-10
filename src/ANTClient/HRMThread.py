import threading
from time import sleep
from HRMListener import *
from usb import USBError
import requests
import config
import json


class HRMThread(threading.Thread):

    # #inerval is the period the thread get HR from device
    def __init__(self, monitorScreen, statusMessage, interval=10, userID=None):
        threading.Thread.__init__(self)

        self.listener = HRMListener(netkey=NETKEY, serial=SERIAL)
        self.monitorScreen = monitorScreen
        self.interval = interval
        self.alive = False
        self.exception = None
        self.statusMessage = statusMessage
        self.userID = userID
        self.failure_count = 0

    def run(self):

        try:
            self.listener.start()
            self.alive = True
            self.showMessage("Hardware Connected.")

        except USBError as e:

            self.showMessage("USBError: " + e.message)
            self.alive = False

        except exceptions.DriverError as e:

            self.showMessage("DriverError: " + e.message)
            self.alive = False

        while self.alive:

            if self.userID is not None and self.listener.getHR() != '0':

                self.postHRToServer(self.listener.getHR())

            self.updateScreen()
            sleep(self.interval)

    def postHRToServer(self, heartRate):

        try:
            destUrl = config.url + '/active_user/' + str(self.userID) + '/heart_rate'
            body = {'id': self.userID, 'heart_rate': str(heartRate)}
            r = requests.post(url=destUrl, json=body)
            msg = json.loads(str(r.text))

            print 'HRM Message', msg['message']

            if msg['message'] is 'User not activated':
                self.showMessage('Not activated, please activate through website.')
                self.failure_count += 1

            if msg['message'] != 'recorded' or 'User not activated':
                print 'post hr: ', heartRate
                self.failure_count += 1

            elif msg['message'] == 'timeReached':
                self.showMessage('Session time Finished.')

            else:
                self.showMessage(msg['message'])

        except (requests.HTTPError, requests.ConnectionError, requests.RequestException) as e:
            print "hrmThread error", e.message
            self.failure_count += 1

            pass

        # self.checkErrorTime()
        
    def finish(self):

        try:
            self.listener.stop()

        except exceptions.NodeError as e:
            self.showMessage("NodeError: " + e.message)

        finally:

            self.monitorScreen.config(text="0")
            self.alive = False

    def showMessage(self, msg):
        self.statusMessage.config(text="Status: " + msg)

    def updateScreen(self):
        self.monitorScreen.config(text=self.listener.getHR())

    def isAlive(self):
        return self.alive

    def getException(self):
        return self.exception

    # def checkErrorTime(self):
    #
    #     print "error time", self.failure_count
    #     if self.failure_count > 10:
    #
    #         self.showMessage("connection error, disconnected.")
    #         self.failure_count = 0
    #         self.finish()
