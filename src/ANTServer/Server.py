from CouchConnection import CouchConnection
from UserSession import UserSession


class Server:

    def __init__(self):
        self.database = CouchConnection()
        self.activeUser = dict()

    def loginUser(self, user_id):

        return self.database.checkUser(user_id)

    def getActiveUser(self):
        return self.activeUser.keys()

    def registerSession(self, userID):
        recvMsg = self.database.getUserInfo(userID)
        print 'recv', recvMsg

        if recvMsg['code'] == 200:
            userInfo = recvMsg['message']
            userID = userInfo['id']

            if userID in self.activeUser:
                return {'code': 409, 'message': 'user has already activated.'}

            self.activeUser[userID] = UserSession(userInfo)
            sessionCode = self.activeUser[userID].getCurSession()

            sendMsg = {'code': 200,
                       'message': {'user': userInfo['name'],
                                   'sessionCode': sessionCode
                                   }
                       }

        else:
            sendMsg = recvMsg

        return sendMsg

    def updateHR(self, userID, heartRate):

        if userID not in self.activeUser:
            return False

        try:

            status = self.activeUser[userID].updateHR(heartRate)

            if status == 'timeReached':
                sessionCode = self.activeUser[userID].getCurSession()
                sessionData = self.activeUser[userID].getSessionData()

                userInfo = self.activeUser[userID].getUserInfo()
                self.database.saveSession(userInfo, sessionCode, sessionData)
                return {'message': status}

            return {'message': status}

        except Exception:
            return False

    def getUserLatestHR(self, userID):

        try:
            hr, hr_count = self.activeUser[userID].getLatestHR()

            return hr, hr_count
        except KeyError:
            return False

    def getAllUsers(self):

        response = self.database.getUsers()
        if response['code'] == 200:
            list = response['message']

            return {'code': 200, 'message': list}
        else:
            return {'code': 500, 'message': response['message']}

    def createUser(self, userInfo):
        response = self.database.createUser(userInfo)

        if response['code'] == 200:
            return {'code': 200, 'message': response['message']}
        else:
            return response

    def active_user(self, userID):

        if userID in self.activeUser:
            self.activeUser[userID].activeSession()

            return True, 'user ' + userID + ' activated.'

        else:
            return False, 'user not found.'

    def deactiveUser(self, userID):

        if userID in self.activeUser:
            del self.activeUser[userID]

            return True, 'removed'

        return False, 'not found'

    def getUserDetail(self, userID):

        status = self.database.getUserDetail(userID)
        isSuccessful = status[0]

        if isSuccessful is True:
            userDetail = status[1]
            return True, userDetail

        return False, {}





