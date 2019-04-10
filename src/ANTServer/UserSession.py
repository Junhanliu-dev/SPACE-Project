import datetime
import time


class UserSession:

    def __init__(self, userInfo):
        # User info fields
        self.id = userInfo['id']
        self.exerZoneHR = userInfo['exercise_zone']
        # Coolzone = warmup zone
        self.cooZoneHR = userInfo['cool_zone']
        self.name = userInfo['name']
        self.heart_rate = int(userInfo['heart_rate'])

        self.isActivated = False

        # session fields
        self.current_session = self.createNewSession(userInfo['latest_session'])
        self.sessionData = list()
        self.latest_hr = 0
        self.secondElapsed = 0
        self.numOfHRUpdated = 0

        # in the zone indicator
        self.time_in_coolZone = 0
        self.time_in_exercise_zone = 0
        self.time_in_warmup_zone = 0

    def createNewSession(self, latset_session):
        timestamp = self.getTimestamp()

        if len(latset_session) == 0:
            newSessionCode = 'S1' + "_" + timestamp

        else:
            newSessionCode = self.generateNewSessionCode(latset_session, timestamp)

        return newSessionCode

    def generateNewSessionCode(self, latest_session, timestamp):
        # prefix of S1 = 1
        newNum = str(int(latest_session.split('_')[0].strip('S')) + 1)
        newSessionCode = 'S' + newNum + '_' + timestamp

        return newSessionCode

    def updateHR(self, heartRate):
        self.latest_hr = heartRate

        if self.isActivated is True:
            self.numOfHRUpdated += 1
            status = self.recordIntoSession(self.latest_hr,self.numOfHRUpdated)
            self.secondElapsed += 10

            return status

        return 'User not activated.'

    def recordIntoSession(self, heart_rate, num_of_hr_updated):
        # Time are based on record time 1 per 10 seconds
        totalTime = 3600  # 3600 for real

        if self.secondElapsed >= totalTime:
            return 'timeReached'

        warmUpTime = 30  # WarmUpTime stops at 05:00
        exerciseTime = 330  # ExerciseTime stops at 55:00
        end_up_time = 360 # Session stops at 60:00
        record = list()

        hr = heart_rate
        timestamp = self.getTimestamp()
        second = self.secondElapsed
        indication = 'None'
        record.append(hr)

        if num_of_hr_updated <= warmUpTime:
            indication = self.checkIndication(hr, 'warmup_zone')

        elif warmUpTime < num_of_hr_updated <= exerciseTime:
            indication = self.checkIndication(hr, 'exercise_zone')

        elif exerciseTime < num_of_hr_updated <= end_up_time:
            indication = self.checkIndication(hr, 'cool_zone')

        record.append(indication)
        record.append(timestamp)
        record.append(second)
        self.sessionData.append(record)

        return 'recorded'

    def checkIndication(self, hr, zone):
        hr = int(hr)

        if zone in ['warmup_zone', 'cool_zone']:
            floor = int(self.heart_rate * 0.45)
            ceil = int(self.heart_rate * 0.55)

        else:
            floor = int(self.heart_rate * 0.65)
            ceil = int(self.heart_rate * 0.75)

        if hr < floor:
            return 'below'

        elif hr in range(floor, ceil+1):  # make range inclusive in both sides

            if zone == 'warmup_zone':
                self.time_in_warmup_zone += 10
            elif zone == 'cool_zone':
                self.time_in_coolZone += 10
            else:
                self.time_in_exercise_zone += 10

            return 'in'

        else:
            return 'up'

    def getUserInfo(self):
        cool_zone_floor = int(self.heart_rate * 0.45)
        cool_zone_ceil = int(self.heart_rate * 0.55)
        exer_zone_floor = int(self.heart_rate * 0.65)
        exer_zone_ceil = int(self.heart_rate * 0.75)

        seconds_in_warmup_zone = self.time_in_warmup_zone
        seconds_in_exercise_zone = self.time_in_exercise_zone
        seconds_in_cool_zone = self.time_in_coolZone

        userInfo = {'id': self.id,
                    'name': self.name,
                    'heart_rate': self.heart_rate,
                    'cool_zone': [cool_zone_floor, cool_zone_ceil],
                    'exercise_zone': [exer_zone_floor, exer_zone_ceil],
                    'time_in_warmup_zone': seconds_in_warmup_zone,
                    'time_in_exercise_zone': seconds_in_exercise_zone,
                    'time_in_cool_zone': seconds_in_cool_zone
                    }

        return userInfo

    def activeSession(self):
        self.isActivated = True

    def getTimestamp(self):

        return str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S'))

    def getUserName(self):
        return self.name

    def getUserID(self):
        return self.id

    def getLatestHR(self):
        return self.latest_hr, self.numOfHRUpdated

    def getCurSession(self):
        return self.current_session

    def getSessionData(self):
        return self.sessionData

