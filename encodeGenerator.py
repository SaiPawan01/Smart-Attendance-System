import cv2 as cv
import face_recognition
import pickle
import os
from dotenv import load_dotenv

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
BUCKET_URL = os.getenv('BUCKET_URL')

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': DATABASE_URL,
    'storageBucket': BUCKET_URL
})

#Importing images
imgPath = 'Images'
imgPathList = os.listdir(imgPath)
imgList = []
studentIds = []
for path in imgPathList:
    imgList.append(cv.imread(os.path.join(imgPath,path)))
    studentIds.append(os.path.splitext(path)[0])

    #uploading image to database storage
    filename = f"{imgPath}/{path}"
    bucket = storage.bucket()
    blob = bucket.blob(filename)
    with open(filename, 'rb') as file_obj:
        blob.upload_from_file(file_obj)



#finding encodings of imgs
def findEndcodings(imgList):
    encodeList = []
    for img in imgList:
        img = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList


print('encoding started')
encodingsList = findEndcodings(imgList)
encodeListWithIds = [encodingsList,studentIds]
print('encoding completed')

#creating pickle files
file = open('encodingsFile.p','wb')
pickle.dump(encodeListWithIds, file)
file.close()
print('encodes file saved')
