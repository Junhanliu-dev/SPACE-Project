from ANTPack.message import *
from ANTPack import event


class MyCallback(event.EventCallback):

    def __init__(self):
        self.currentHRRate = 0

    def process(self, msg):
        # print "MSG type: ", tyoe(msg)

        if isinstance(msg, ChannelBroadcastDataMessage):

            # print "ChannelBroadcastDataMessage"
            # beatCount = ord(msg.getPayload()[7])
            heartRate = ord(msg.getPayload()[8])

            if self.currentHRRate != heartRate:
                self.currentHRRate = heartRate

            # print 'Beat Count: ', beatCount
            # print 'Heart Rate: ', self.currentHRRate

    def getHeartRate(self):

        print "callback, heart rate: ", self.currentHRRate
        return self.currentHRRate
