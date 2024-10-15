import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
from dotenv import  load_dotenv



load_dotenv()


DATABASE_URL = os.getenv('DATABASE_URL')
BUCKET_URL = os.getenv('BUCKET_URL')

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': DATABASE_URL,
    'storageBucket': BUCKET_URL
})

ref = db.reference('students')

data = {
    "101":
        {
            'name':'Abdul',
            'branch':'CSE(AI&ML)',
            'year_joining': 2022,
            'total_attendance':7,
            'standing':'G',
            "year":3,
            "lasy_attendance":'2024-10-14 09:00:00'

        },
"102":
        {
            'name':'Tata',
            'branch':'CSE(AI&ML)',
            'year_joining': 2022,
            'total_attendance':7,
            'standing':'G',
            "year":3,
            "lasy_attendance":'2024-10-14 09:00:00'

        },
"103":
        {
            'name':'sundar',
            'branch':'CSE(AI&ML)',
            'year_joining': 2022,
            'total_attendance':7,
            'standing':'G',
            "year":3,
            "lasy_attendance":'2024-10-14 09:00:00'

        },
    "104":
        {
            'name':'pavan',
            'branch':'CSE(AI&ML)',
            'year_joining': 2022,
            'total_attendance':9,
            'standing':'G',
            "year":3,
            "lasy_attendance":'2024-10-14 09:00:00'

        }
}


for key,value in data.items():
    ref.child(key).set(value)