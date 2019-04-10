from ANTPack import node
from ANTPack import driver
from ANTPack.constants import *
from config import *
from CallbackService import MyCallback
from ANTPack import exceptions


class HRMListener:

    def __init__(self, serial, netkey):
        self.serial = serial
        self.netkey = netkey
        self.antnode = None
        self.channel = None
        self.callback = MyCallback()

    def start(self):

        self._start_antnode()
        self._channel_setup()
        self.channel.registerCallback(callback=self.callback)

    def stop(self):

        if self.channel:
            self.channel.close()
            self.channel.unassign()
        if self.antnode:
            self.antnode.stop()

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.stop()

    def _start_antnode(self):

        print "starting node"
        stick = driver.USB2Driver(self.serial)
        self.antnode = node.Node(stick)

        print "antnode Start"
        
        try:

            self.antnode.start()

        except exceptions.DriverError as e:
            print "Driver error %s" % e
            raise exceptions.DriverError(e.message)

        print "netkey Set"
        key = node.NetworkKey('N:ANT+', NETKEY)
        self.antnode.setNetworkKey(0, key)

        print "netkey set finished"
        print "Node Started"

    def _channel_setup(self):

        print "channel setting up..."
        self.channel = self.antnode.getFreeChannel()
        # print 'Set channel Name as C:HRM'
        self.channel.name = 'C:HRM'

        # print 'Channel assign N:ANT+ CHANNEL_TYPE_TWOWAY_RECEIVE'
        self.channel.assign('N:ANT+', CHANNEL_TYPE_TWOWAY_RECEIVE)

        # print "set ID"
        self.channel.setID(120, 0, 0)

        # print "Set Search Timeout"
        self.channel.setSearchTimeout(TIMEOUT_NEVER)

        # print 'set Period 8070'
        self.channel.setPeriod(8070)

        # print 'set frequency 57'
        self.channel.setFrequency(57)

        # print 'channel open'
        self.channel.open()
        print "channel setup finished"

    def getMSGID(self):
        self.antnode.getMSGID()

    def getHR(self):
        return str(self.callback.getHeartRate())
