from flask import Flask, jsonify, request, abort, send_from_directory
from Server import Server

import sys

app = Flask(__name__)
server = Server()


# Root directory for checking the server is running.
@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to ANT+ Server.'})


@app.route('/users', methods=['POST', 'GET'])
def processUserInfo():

    if request.method == 'POST':

        try:
            message = request.get_json()

        except Exception:
            return abort(400)

        response = server.createUser(message)

        if response['code'] == 200:
            return jsonify({'message': response['message']})

        elif response['code'] == 409:
            return abort(409, response['message'])

        else:
            return abort(400)

    if request.method == 'GET':
        response = server.getAllUsers()

        if response['code'] == 200:
            return jsonify({'message': response['message']})
        else:
            return abort(500, response['message'])


@app.route('/users/<string:user_id>/detail', methods=['GET'])
def requestUserDetail(user_id):

    status = server.getUserDetail(user_id)
    isSuccessful = status[0]

    if isSuccessful is True:
        return jsonify({'id': user_id, 'detail': status[1]})

    else:
        return abort(404)


@app.route('/active_user', methods=['GET'])
def getActiveUser():

    activeUser = server.getActiveUser()

    return jsonify({'message': {'users': activeUser}})


@app.route('/users/<string:user_id>/login', methods=['POST'])
def login(user_id):

    status = server.loginUser(user_id)

    if status is True:
        return jsonify({'message': "User ID: " + user_id + ' logged'})

    else:
        return abort(404, 'user not found')


@app.route('/active_session/<string:user_id>', methods=['POST'])
def activeUser(user_id):

    if user_id not in server.getActiveUser():
        return jsonify({'message': 'session not activated, please active through local application.'})

    response = server.active_user(user_id)

    if response[0] is True:

        return jsonify({'code': 200, 'message': response[1]})

    return jsonify({'code': 404, 'message': response[1]})


@app.route('/active_user/<string:user>/deactive', methods=['POST'])
def deactiveUser(user):
    status = server.deactiveUser(userID=user)

    if status[0] is True:
        return jsonify({'message': 'deactivated', 'id': user})

    else:
        return abort(404, 'resource not found.')


@app.route('/register_session', methods=['POST'])
def register_session():

        requestData = request.get_json()
        userID = requestData['id']
        status = server.registerSession(userID)

        if status['code'] == 200:
            message = status['message']

            body = {'code': 200,
                    'message': {'status': 'registered',
                                'id': userID,
                                'name': message['user'],
                                'sessionCode': message['sessionCode']
                                }
                    }

            return jsonify(body)

        else:
            return abort(status['code'], status['message'])


@app.route('/active_user/<string:user_id>/heart_rate', methods=['POST', 'GET'])
def processHeartRate(user_id):

    if request.method == 'GET':
        status = server.getUserLatestHR(user_id)

        if status is False:
            return jsonify({'code': 500, 'message': 'heart rate get error.'})
        else:
            return jsonify({'code': 200, 'message': {'user': user_id,
                                                     'heart_rate': status[0],
                                                     'heart_count': status[1]}})

    elif request.method == 'POST':
        body = request.get_json()
        heartRate = body['heart_rate']
        status = server.updateHR(userID=user_id, heartRate=heartRate)

        if status is False:
            return jsonify({'message': 'update error.'})

        if status['message'] == 'recorded':
            print "hr, ", server.getUserLatestHR(user_id)
            return jsonify({'message': 'recorded'})

        elif status['message'] == 'timeReached':
            return jsonify({'message': 'timeReached saving session.'})

        else:
            return jsonify({'message': status['message']})

    else:
        return abort(400)


@app.route('/<string:userid>/sessions/<string:fileName>', methods=['GET'])
def downloadSession(userid, fileName):
    userDir = 'space_proj/' + userid

    try:
        userSessionFile = fileName + '.csv'

        return send_from_directory(directory=userDir,
                                   filename=userSessionFile,
                                   mimetype='text/csv',
                                   as_attachment=True)

    except Exception:
        return abort(404, 'Resource not found.')


@app.errorhandler(404)
def custom404(error):
    print "error", error
    return jsonify({'code': 404, 'message': str(error)})


@app.errorhandler(500)
def custom500(error):
    return jsonify({'code': 500, 'message': str(error)})


@app.errorhandler(409)
def custom409(error):
    print "error", error
    return jsonify({'code': 409, 'message': str(error)})


if __name__ == '__main__':
    port = sys.argv[1]
    print "Using port %s" % port
    app.run(port=port)
