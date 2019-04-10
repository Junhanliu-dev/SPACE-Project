# USB1 ANT stick interface. Running `dmesg | tail -n 25` after plugging the
# stick on a USB port should tell you the exact interface.
SERIAL = '/dev/ttyUSB0'


# Some demos depend on this setting being True, so unless you know what you
# are doing, leave it as is.
DEBUG = True

NETKEY = b'\xB9\xA5\x21\xFB\xBD\x72\xC3\x45'

# Set to None to disable logging
LOG = None
# LOG = log.LogWriter()

# ========== DO NOT CHANGE ANYTHING BELOW THIS LINE ==========
# print "Using log file:", LOG.filename

# Message configurations

helloMsg = "Welcome to ANT+ config window."
defFont = "times new roman"

# CouchDB Connection configurations
couch_address = "http://admin:liujunhanchang@18.219.29.53:5984/"
url = 'http://18.219.29.53:5000'
header = {'Content-type': 'application/json'}

# For testing purpose

jsonObj = {"PID": "001",
           "PName": "James Bond",
           "HR_Max": 80,
           "Cool_Zone": [40,66],
           "Exercise_zone": [56,70],
           "Session":
               {"S1_time1": [["HR", "indication", "timestamp", "second"],
                             ["HR", "indication", "timestamp", "second"],
                             ["HR", "indication", "timestamp", "second"]],
                "S2_time2": [["HR", "indication", "timestamp", "second"],
                             ["HR", "indication", "timestamp", "second"],
                             ["HR", "indication", "timestamp", "second"]]
                }
           }

sess = [["HR", "indication", "timestamp", "second"],
        ["HR", "indication", "timestamp", "second"],
        ["HR", "indication", "timestamp", "second"]]

