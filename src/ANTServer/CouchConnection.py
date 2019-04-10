import couchdb
import config
import os
import thread
import csv


class CouchConnection:

    def __init__(self, address=config.couch_address, dbName=config.dbName):

        self.rootPath = config.rootPath
        try:
            self.server = couchdb.Server(address)

            if dbName in self.server:
                self.db = self.server[dbName]
            else:
                self.db = self.server.create(dbName)

        except couchdb.HTTPError as e:

            print "Connection error: %s , please try again." % e

        self.makeDir(self.rootPath)

    def makeDir(self, path):

        if os.path.isdir(path) is False:
            os.mkdir(path)

    def getUserInfo(self, uid):
        info = {}
        # payload = tuple()

        try:
            user = self.db[uid]
            info['id'] = user['PID']
            info['exercise_zone'] = user['Exercise_Zone']
            info['name'] = user['PName']
            # CoolZone = Warm up zone
            info['cool_zone'] = user['Cool_Zone']
            info['heart_rate'] = user['HR_Max']
            info['latest_session'] = self.getLatestSession(user['Session'].keys())

            payload = {'code': 200, 'message': info}

        except couchdb.ResourceNotFound:
            payload = {'code': 404, 'message': 'ResourceNotFound'}

        except couchdb.HTTPError:
            payload = {'code': 503, 'message': "HTTPError"}

        return payload

    def getLatestSession(self, userSessions):

        if userSessions == []:
            return []

        else:

            return sorted(userSessions,
                          key=lambda prefix: int(prefix.split('_')[0].strip('S')),
                          reverse=True)[0]

    def createUser(self, userInfo):

        try:
            docID = userInfo["PID"]
            userPath = self.rootPath + "/" + str(docID)
            self.makeDir(userPath)
            self.db[docID] = userInfo

        except couchdb.http.ResourceConflict:
            msg = "The User %s already exists, please check" % docID

            return {'code': 409, 'message': msg}

        except Exception:
            return {'code': 400, 'message ': 'Bad request.'}

        return {'code': 200, 'message': 'created: %s' % docID}

    def verifyUser(self, userID):
        status = ()

        if userID is None:
            status = (False, "User ID not verified.")
            return status

        try:

            userName = self.db[userID]["PName"]
            status = (True, userName)

        except (couchdb.http.ResourceNotFound, couchdb.HTTPError, KeyError) as e:
            status = (False, e)

        finally:
            return status

    def saveSession(self, user_info, sessionCode, session_data):

        try:
            user_id = user_info['id']
            doc = self.db[user_id]
            # print doc["Session"]
            doc["Session"][sessionCode] = session_data

            thread.start_new_thread(self.parseToCSV, (user_info, sessionCode, session_data, ))
            self.db.save(doc)

            print "Session saved."
            return True

        except Exception as e:

            print "Excp in CouchConnection_saveSession", e
            return False

    def getSessions(self, userID):

        try:
            doc = self.db[userID]

            return {'code': 200, 'message': sorted(doc["Session"].keys(),
                                                   key=lambda x: int(x.split('_')[0].strip('S')),
                                                   reverse=True)}

        except Exception as e:
            msg = "Retrieve error %s, please try again." % e

            return {'code': 500, 'message': msg}

    def getUsers(self):
        userList = list()

        try:
            for item in self.db.view('_design/views/_view/identity'):

                userList.append([item.id, item.value])

            return {'code': 200, 'message': userList}

        except couchdb.HTTPError as e:
            # e.message
            return {'code': 500, 'message': e.message}

    def parseToCSV(self, userInfo, sessionCode, sessionData):
        userID = userInfo['id']

        print 'type of User ID :', type(userID)

        timeLine = sessionCode.split('_')[1]
        fileStructure = list()

        fileStructure.append(['ID:', str(userID)])
        fileStructure.append(['PName:', userInfo['name']])
        fileStructure.append(['HR_Max:', userInfo['heart_rate']])
        fileStructure.append(['Cool_Zone:', userInfo['cool_zone']])
        fileStructure.append(['Exercise_zone:', userInfo['exercise_zone']])
        fileStructure.append(['Time_in_warm_up_zone_(second):', userInfo['time_in_warmup_zone']])
        fileStructure.append(['Time_in_exercise_zone_(second):', userInfo['time_in_exercise_zone']])
        fileStructure.append(['Time_in_cool_zone_(second):', userInfo['time_in_cool_zone']])
        fileStructure.append(['TimeLine:', timeLine])
        # Add column names
        fileStructure.append(['Heart_Rate', 'Indication', 'Timestamp', 'Starting second'])

        fileName = sessionCode + ".csv"
        dataToBeStored = (fileStructure, sessionData)

        self.saveCSVToLocalDir(dataToBeStored, fileName, userID)

    def saveCSVToLocalDir(self, dataToBeStored, fileName, userID):

        # userPath = config.rootPath.strip(chars=['./']) + "/" + str(userID)
        # dirPath = os.getcwd()
        # folderName = os.path.basename(dirPath)
        path = os.path.abspath('space_proj/' + userID)
        os.chdir(path)

        fileHandler = open(fileName, "w")
        writer = csv.writer(fileHandler)

        print "file writing..."

        for i in dataToBeStored:
            writer.writerows(i)

        fileHandler.close()
        os.chdir('../../')

        print "file saved in File system...."

    def getUserDetail(self, userID):
        userInfo = {}

        try:
            userDetail = self.db.get(userID)

            userInfo['id'] = userDetail['PID']
            userInfo['name'] = userDetail['PName']
            userInfo['max_hr'] = userDetail['HR_Max']
            userInfo['exercise_zone'] = userDetail['Exercise_Zone']
            userInfo['cool_zone'] = userDetail['Cool_Zone']
            userInfo['sessionList'] = sorted(userDetail['Session'].keys(),
                                             key=lambda x: int(x.split('_')[0].strip('S')),
                                             reverse=True)
            del userDetail

            return True, userInfo

        except Exception:
            return False, {}

    def checkUser(self, user_id):

        if user_id in self.db:
            return True
        else:
            return False

# couch = CouchConnection()
# couch.createUser(config.jsonObj)
# couch.saveSession("001", "S3_time1", config.sess)
# couch.retrieveSessions("001")
# couch.parseToCSV("001", "S3_time1")
# couch.verifyUser("003")
# couch.getUserInfo("001")
# couch.getUsers()