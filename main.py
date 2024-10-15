import pickle
import cv2 as cv
import numpy as np
import face_recognition
from datetime import datetime
import os
from dotenv import load_dotenv

#database configration
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
BUCKET_URL = os.getenv('BUCKET_URL')


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': DATABASE_URL,
    'storageBucket': BUCKET_URL
})


#loading the encoding file
print('loading encodings')
file = open('encodingsFile.p','rb')
encodeListWithIds = pickle.load(file)
file.close()
encodingsList, studentIds = encodeListWithIds
print('loading encodings completed')


studentInfo = None

#live video capturing and comparing
cap = cv.VideoCapture(0)
while True:
    ret, frame = cap.read()

    frame = cv.cvtColor(frame,cv.COLOR_BGR2RGB)

    faceCurrLoc = face_recognition.face_locations(frame)
    print(faceCurrLoc)

    # if no face detected then go to next frame
    if len(faceCurrLoc) == 0:
        cv.putText(frame,'No Face Detected!',(50,50),cv.FONT_HERSHEY_SIMPLEX,1,(255,0,0))
        print('No face Detected!')
        continue

    encodeCurrFrame = face_recognition.face_encodings(frame,faceCurrLoc)

    for encodedFace, faceLoc in zip(encodeCurrFrame,faceCurrLoc):
        match = face_recognition.compare_faces(encodingsList,encodedFace)
        faceDistance = face_recognition.face_distance(encodingsList,encodedFace)
        # print("Match : ",match)
        # print("faceDistance : ",faceDistance)

        matchIndex = np.argmin(faceDistance)
        print('matchIndex : ', matchIndex)


        # checking if face known or unknown and retrieving student data
        if matchIndex:
            print('detected known face')
            studentId = studentIds[matchIndex]
            if studentInfo:
                pass
            else:
                studentInfo = db.reference(f'students/{studentId}').get()
                print(studentInfo)

                #update student attendance
                dateTimeObj = datetime.strptime(studentInfo['lasy_attendance'],"%Y-%m-%d %H:%M:%S")
                timeElapsed = (datetime.now()-dateTimeObj).total_seconds()
                print(timeElapsed)

                ref = db.reference(f'students/{studentId}')
                studentInfo['total_attendance'] += 1
                ref.child('total_attendance').set(studentInfo['total_attendance'])
                ref.child('lasy_attendance').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        else:
            print('detected unknown face')


        # drawing rectangle around the face detected
        cv.rectangle(frame,(faceCurrLoc[0][0],faceCurrLoc[0][1]),(faceCurrLoc[0][2],faceCurrLoc[0][3]),(0,255,0),1)


    #displaying the frame
    cv.imshow("img",frame)

    if cv.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()