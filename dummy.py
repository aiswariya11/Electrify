import random
import time
import math
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file and initialize Firebase Admin SDK
cred = credentials.Certificate(r"C:\Users\Abhijith C\Apps\electrify-5ae88-firebase-adminsdk-spnrb-56328eb6ad.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://electrify-5ae88-default-rtdb.firebaseio.com/Devices'
})

# Get a reference to the root of your Firebase Realtime Database
root_ref = db.reference('/')

bulb1_totalenergy = 0;
bulb2_totalenergy = 0;
total_energy = 0;

# Loop indefinitely to continuously upload random values to the database
while True:
    # Generate random VRMS and IRMS values for two bulbs
    bulb1_vrms = round(random.uniform(220, 240), 2)
    bulb1_irms = round(random.uniform(0.01, 0.02), 4)
    bulb2_vrms = round(random.uniform(220, 240), 2)
    bulb2_irms = round(random.uniform(0.01, 0.02), 4)

    # Calculate the power and energy consumption values for each bulb
    bulb1_power = round(bulb1_vrms * bulb1_irms, 4)
    bulb1_energy = round(bulb1_power * 1 / 3600, 4)
    bulb2_power = round(bulb2_vrms * bulb2_irms, 4)
    bulb2_energy = round(bulb2_power * 1 / 3600, 4)

    bulb1_totalenergy += bulb1_energy
    bulb2_totalenergy +=bulb2_energy

    total_energy += bulb1_energy + bulb2_energy 

    bulb1_unit = math.floor(bulb1_totalenergy);
    bulb2_unit = math.floor(bulb2_totalenergy);

    bulb1_totalenergy = round(bulb1_totalenergy, 4)
    bulb2_totalenergy = round(bulb2_totalenergy, 4)
    total_energy = round(total_energy, 4)

    # Create a dictionary of the data to be uploaded to the database
    data = {
        'devices' : {
            'bulb1': {
                'voltage': bulb1_vrms,
                'current': bulb1_irms,
                'power': bulb1_power,
                'energy': bulb1_totalenergy,
                'unit' : bulb1_unit
            },
            'bulb2': {
                'voltage': bulb2_vrms,
                'current': bulb2_irms,
                'power': bulb2_power,
                'energy': bulb2_totalenergy,
                'unit' : bulb2_unit
            },
            'totalEnergy' : total_energy
        }
    }

    # Upload the data to the database
    root_ref.update(data)

    # Wait for 5 seconds before generating and uploading the next set of values
    time.sleep(1)
