import cv2
import numpy as np
import face_recognition
import os
import csv
from datetime import datetime

path = 'resources';
images = []
classNames = []
myList = os.listdir(path)
# print(myList)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

# print(images)

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        csvreader = csv.reader(f)
        fieldnames = ['Name', 'Time']
        csvwriter = csv.DictWriter(f, fieldnames=fieldnames)
        rows = []
        nameList = []
        csvwriter.writeheader()
        header = next(csvreader)
        # myDataList = f.readLines()
        for row in csvreader:
            rows.append(row)

        print(name)
        # for line in rows:
        #     print(line)
        #     for rrr in line:
        #         entry = line.split(',')
        #         print(entry)
        #         nameList.append(entry[0])
        if name not in nameList:
            if(len(name)>2):
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                data = [name,dtString]
                csvwriter.writerow({'Name':name,'Time':dtString})
                # f.writelines(f'{name},{dtString}')


        print(header)

encodeListKnown = findEncodings(images)
print(len(encodeListKnown))

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        # print(faceDis)
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name=classNames[matchIndex].upper()
            # print(name)
            y1,x2,y2,x1 = faceLoc
            # y1, x2, y2, x1 = y1, x2*4, y2*4, x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(name)

    cv2.imshow('Web Cam',img)
    cv2.waitKey(1)


# faceLoc = face_recognition.face_locations(imgElon)[0]
# encodeElon = face_recognition.face_encodings(imgElon)[0]
# cv2.rectangle(imgElon,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)
#
# faceLocTest = face_recognition.face_locations(imgTest)[0]
# encodeTest = face_recognition.face_encodings(imgTest)[0]
# cv2.rectangle(imgTest,(faceLocTest[3],faceLocTest[0]),(faceLocTest[1],faceLocTest[2]),(255,0,255),2)
#
# results = face_recognition.compare_faces([encodeElon],encodeTest);
# faceDis = face_recognition.face_distance([encodeElon],encodeTest)

# imgElon = face_recognition.load_image_file('resources/elon.jpg');
# imgElon = cv2.cvtColor(imgElon,cv2.COLOR_BGR2RGB);
#
# imgTest = face_recognition.load_image_file('resources/elontest.jpg');
# imgTest = cv2.cvtColor(imgTest,cv2.COLOR_BGR2RGB);


