import firebase_admin
import schedule
import time
import datetime
from retrying import retry
from firebase_admin import credentials
from firebase_admin import firestore

from co2 import *
from humidity import *
from temperature import *
from pressure import *

class params1:
    def __init__(self, temp, hum, press, co2):
        self.temp = temp
        self.hum = hum
        self.press = press
        self.co2 = co2

    def set(self, db):
        ref = db.collection('params1').document('data')
        ref.set({'temp': self.temp, 'hum': self.hum, 'press': self.press, \
            'co2': self.co2, 'time': firestore.SERVER_TIMESTAMP})


@retry(wait_fixed=30000)
def set_params1():
    # doc_ref = db.collection('params1').document()

    temp = temp_start()
    hum = hum_start()
    press = (press_start() + press_start())/2
    co2 = get_co2()

    print(datetime.datetime.now())
    print('%f, %f, %f, %d' % (temp, hum, press, co2))
    print('')

    try:
        if co2 != -1:
            data = params1(temp=temp, hum=hum, press=press, co2=co2)
            data.set(db)
        else:
            raise Exception()
    except:
        print('Error->retry!')
        raise Exception()


# Use a service account
cred = credentials.Certificate(
    '/home/pi/room_monitor/nabe1005-room-monitor-firebase-adminsdk-t2ykf-8532a3d274.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

schedule.every().hours.at(':00').do(set_params1)
schedule.every().hours.at(':10').do(set_params1)
schedule.every().hours.at(':20').do(set_params1)
schedule.every().hours.at(':30').do(set_params1)
schedule.every().hours.at(':40').do(set_params1)
schedule.every().hours.at(':50').do(set_params1)

while True:
    schedule.run_pending()
    time.sleep(1)

