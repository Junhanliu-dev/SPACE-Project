
# CouchDB Connection configurations
couch_address = "http://admin:admin@127.0.0.1:5984/"
dbName = 'space_prog'
rootPath = "./space_proj"

#url
url = 'http://127.0.0.1:5000'


jsonObj = {"PID": "001",
           "PName": "James Bond",
           "HR_Max": 80,
           "Cool_Zone": [40, 50],
           "Exercise_zone": [50, 70],
           'time_in_warmup_zone': 300,
           'time_in_exercise_zone': 300,
           'time_in_cool_zone': 200,
           "Session":
               {"S1_time1": [["HR", "indication", "timestamp", "second"],
                             ["HR", "indication", "timestamp", "second"],
                             ["HR", "indication", "timestamp", "second"]],
                "S2_time2": [["HR", "indication", "timestamp", "second"],
                             ["HR", "indication", "timestamp", "second"],
                             ["HR", "indication", "timestamp", "second"]]
                }
           }


sessData = [[56, "in", "2018-10-04 11:16:33", "10"],
            [66, "up", "2018-10-04 11:16:33", "20"],
            [70, "down", "2018-10-04 11:16:33", "30"]]


sessionCode = 'S1_2018-10-04 11:16:33'

