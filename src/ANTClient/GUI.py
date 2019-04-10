import Tkinter as tk
from config import *
from HRMThread import HRMThread

import requests
import tkMessageBox
import config
import json


class UI:

    def __init__(self):

        # Root Setting
        self.root = tk.Tk()
        self.root.title("ANT+ Connector")
        self.root.geometry("550x300+500+300")
        # self.root.resizable(0, 0)
        self.root.lift()
        self.root.attributes('-topmost', 1)
        self.root.attributes('-topmost', 0)

        # Set Welcome Label, No functional Use
        tk.Label(self.root, text=helloMsg, fg="blue", font=(defFont, 20)).pack(side=tk.TOP)

        # Login Frame on Left Side of the UI
        self.loginFrame = tk.Frame(self.root,
                                   highlightcolor="grey",
                                   highlightbackground="grey",
                                   highlightthickness=1,
                                   width=300, height=400)

        self.loginFrame.pack_propagate(0)
        self.loginFrame.pack(side=tk.LEFT)
        self.loginInfo = None

        # Monitor Frame, Message Label and Monitor screen Setting on the right hand side
        self.monitorFrame = tk.Frame(self.root,
                                     highlightcolor="grey",
                                     highlightbackground="grey",
                                     highlightthickness=1,
                                     width=300, height=400)
        self.monitorFrame.pack(side=tk.RIGHT)

        self.HRMessageLabel = tk.Label(master=self.monitorFrame, text="Your Heart Rate is: ", font=(defFont, 23))
        self.HRMessageLabel.place(x=10, y=10)

        self.HRMonitorScreen = tk.Label(master=self.monitorFrame, text="0", font=(defFont, 110))
        self.HRMonitorScreen.place(x=40, y=60)

        # userID entry Setting
        self.userTextBox = tk.Entry(self.loginFrame)
        self.userTextBox.place(x=100, y=62)

        # Functional Settings
        self.isConnected = False
        self.userID = None
        self.connectButton = None
        self.disConnectButton = None
        self.statusMessage = None
        self.hrmThread = None
        self.initLayout()

    # Add buttons and Functions
    def initLayout(self):

        # UserID Label and Entry TextBox
        tk.Label(self.loginFrame, text="userID:", font=(defFont, 24)).place(x=20, y=60)
        self.loginInfo = tk.Label(self.root, font=(defFont, 18))
        # Add button layout and Func
        self.connectButton = tk.Button(master=self.loginFrame,
                                       text='Connect',
                                       font=(defFont, 20),
                                       command=lambda: self.connectButtonFunc(self.userTextBox.get()),
                                       relief=tk.RAISED,
                                       compound=tk.LEFT, width=8)
        self.connectButton.config(text='Connect')
        self.root.bind("<Return>", lambda event: self.connectButtonFunc(self.userTextBox.get()))

        self.disConnectButton = tk.Button(master=self.loginFrame,
                                          text="Disconnect",
                                          font=(defFont, 20),
                                          command=self.disConnectButtonFunc,
                                          relief=tk.RAISED,
                                          compound=tk.LEFT)

        self.statusMessage = tk.Message(master=self.loginFrame, text="Status: ", font=(defFont, 17), width=250)

        self.statusMessage.place(x=20, y=155)
        self.connectButton.place(x=20, y=120)
        self.disConnectButton.place(x=150, y=120)
        self.loginInfo.place(x=20, y=35)

    def connectButtonFunc(self, userID):
        self.setStatusMessgae("connecting...")
        # if database found user name, then it is string, otherwise it is error code
        try:
            body = {'message': 'register_session', 'id': userID}
            r = requests.post(url=config.url+'/register_session', json=body)
            msg = r.text
            self.establishHardware(str(msg))

        except requests.HTTPError as e:
            # print "Connection error: ", e
            self.setStatusMessgae(e.message)
            msg = json.dumps({'code': 400, 'message': 'Connection error, try again or connect as single mode'})

            self.establishHardware(msg)

        except requests.ConnectionError:
            # print "Server lost: ", e.message
            self.setStatusMessgae("Server lost, please try again or connect as local mode.")
            msg = json.dumps({'code': 400, 'message': 'Server lost, please try again or connect as local mode.'})

            self.establishHardware(msg)

    def establishHardware(self, msg):
        msg = json.loads(msg)

        if msg['code'] == 200:
            body = msg['message']
            self.userID = body['id']
            self.isConnected = True

            self.loginInfo.config(text="Connected as " + body['name'])
            self.userTextBox.config(state=tk.DISABLED)
            self.createHRMConnection(userID=body['id'])

        else:
            # self.setStatusMessgae("User not found. Please check and try again.")
            result = tkMessageBox.askokcancel(msg['message'], "Would you like run as guest?")

            if result is True:
                self.loginInfo.config(text="Connected as offline mode.")
                self.setStatusMessgae(text="Offline Mode")
                # Create HRM device object
                self.createHRMConnection()

    def disConnectButtonFunc(self):

        try:
            self.hrmThread.finish()

            if self.isConnected is True:
                body = {}
                request_url = config.url + '/active_user/' + self.userID + '/deactive'

                requests.post(url=request_url, json=body)
                self.userID = None
                self.isConnected = False

        except AttributeError as e:
            print "AttributeError: " + e.message

        finally:

            self.hrmThread = None
            self.HRMonitorScreen.config(text=0)
            self.userTextBox.config(state=tk.NORMAL)
            self.userTextBox.delete(0, 'end')
            self.setStatusMessgae("Status: Hardware disconnected.")
            self.loginInfo.config(text="Connected as:")

    def createHRMConnection(self, userID=None):

        if self.hrmThread is not None and self.hrmThread.isAlive() is not False:
            self.hrmThread.join()

            print "You have already opened the hardware."

        else:
            self.hrmThread = HRMThread(monitorScreen=self.HRMonitorScreen,
                                       statusMessage=self.statusMessage,
                                       userID=userID)

            self.setStatusMessgae('Hardware starting...')
            self.hrmThread.start()

    def setStatusMessgae(self, text):

        self.statusMessage.config(text=text)

    def start(self):

        self.root.mainloop()


UI().start()
