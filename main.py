import requests
import time
import checkJoin

config = {
    "user": "", #JOIN username
    "pass": "", #JOIN password
    "delay": 1, #delay in minutes, integer
    "defaultMessage": "Application Under Review" #The message you currently see. Configurable as I've been told it's different for 101/105D/105F/etc people
}

def makeNoise():
    for i in range(5):
        print('\a')
        time.sleep(3)

while True:
    with requests.Session() as client:
        dashboard = checkJoin.check_Join(client, config)
        if "Application Under Review" not in dashboard:
            print("DECISION RELEASED!!!!!!!!!!")
            makeNoise()
            break;
        else:
            print(time.ctime(time.time()) + ": Still under review")
        time.sleep(config["delay"] * 60)
        client.cookies.clear()
