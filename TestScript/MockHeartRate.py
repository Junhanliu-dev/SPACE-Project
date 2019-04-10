import requests
from random import randint
from time import sleep


def get_user_detail(user_id):

    user_detail_address = 'http://18.219.29.53:5000/users/' + user_id + '/detail'

    r = requests.get(user_detail_address)

    return r.json()['detail']


def step1_login(user_id):
    login_address = 'http://18.219.29.53:5000/users/' + user_id + '/login'

    r = requests.post(login_address)

    print "Login response: ", r.text


# From device
def step2_register_session(user_id):
    register_address = 'http://18.219.29.53:5000/register_session'
    json_body = {'id': user_id}

    r = requests.post(register_address, json=json_body)

    print "Register Session Response :", r.text


def step3_active_session(user_id):
    active_session_address = 'http://18.219.29.53:5000/active_session/' + user_id

    r = requests.post(active_session_address)

    print "Active session response: " + r.text


def step4_update_user_heat_rate(user_id):
    update_heart_rate_address = 'http://18.219.29.53:5000/active_user/' + user_id + '/heart_rate'

    user_detail = get_user_detail(user_id)

    user_heart_rate = user_detail['max_hr']

    floor = user_detail['cool_zone'][0]
    ceil = user_detail['exercise_zone'][1]

    print 'Mock start' + '.' * 30

    for i in range(361):

        mock_hr = randint(floor, ceil)

        print 'max_hr = ' + str(user_heart_rate) + ' mocked_hr = ' + str(mock_hr)

        body = {'id': user_id, 'heart_rate': mock_hr}

        r = requests.post(update_heart_rate_address,json=body)

        print 'post iter: ' + str(i) + ' ' + '*' * 10 + ' ' + r.json()['message']

        sleep(0.2)

    print 'Mock finished' + '.' * 30


def deactive_user(user_id):
    deactive_address = 'http://18.219.29.53:5000/active_user/' + user_id + '/deactive'

    r = requests.post(deactive_address)

    print r.json()


def start_mocking_procedure(user_id):
    step1_login(user_id)

    step2_register_session(user_id)

    step3_active_session(user_id)

    step4_update_user_heat_rate(user_id)

    deactive_user(user_id)


start_mocking_procedure('001')