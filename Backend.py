import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import pyautogui
import time


def main():

    path = '#path to save the registered images'
    images = []
    classNames = []
    myList = os.listdir(path)
    for cl in myList:
        if cl != '.DS_Store':
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])
            

    def findEncodings(images):
        encodeList = []
        classNames2 = []
        myList2 = os.listdir(path)

        print("All valid/invalid registered images: ", myList2)
        print("\n")

        i = 0
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            unknown_face_encodings = face_recognition.face_encodings(img)

            if len(unknown_face_encodings) > 0:

                encodeList.append(unknown_face_encodings[0])

                print("Image",i,"saved!")

                i += 1

                current_Name = os.path.splitext(myList2[i])[0]

                for cl2 in myList2:
                    if cl2 != '.DS_Store':
                        if current_Name not in classNames2:
                            classNames2.append(current_Name)
                            print("Successfully added! ", current_Name)
                            print("Current names that can be detect", classNames2)
                            print("\n")

            else:
                i += 1
                current_Name2 = os.path.splitext(myList2[i])[0]
                print("Invalid image",i-1,": ", current_Name2)
                print("\n")

        print("Total registered images: ", len(myList2))
        print("Total valid images: ", len(encodeList))
        print("\n")

        return encodeList, classNames2


    def markAttendance(name):
        os.chdir('/Users/liewchaiheng/PycharmProjects/Facial Recognition')


        with open('Attendance.csv','r+') as f:
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])

            if name not in nameList:
                now = datetime.now()

                f.writelines(f'\n{name}, {now}')


    def screenshot(name, img):

        os.chdir('/Users/liewchaiheng/PycharmProjects/Facial Recognition/screenshot')


        screnshotList = os.listdir('/Users/liewchaiheng/PycharmProjects/Facial Recognition/screenshot')

        screenshotIMG = []

        for current_screenshot in screnshotList:

            name2 = os.path.splitext(current_screenshot)[0].split("_")[0]

            screenshotIMG.append(name2)

        now = datetime.now()
        nameAndDate = str(name)+'_' + str(now) + ".jpg"

        if name not in screenshotIMG:

            cv2.imwrite(nameAndDate, img)



    encodeListKnown, classNames2 = findEncodings(images)

    print('Encoding Complete')


    cap = cv2.VideoCapture(0)

    while True:

        success, img = cap.read()
        # img = captureScreen()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)

        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)



        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)


            if faceDis[matchIndex] < 0.50:
                name = classNames2[matchIndex].upper()
                screenshot(name, img)
                markAttendance(name)

            else:
                name = 'Unknown'
                screenshot(name, img)

            top, right, bot, left = faceLoc
            top, right, bot, left = top * 4, right * 4, bot * 4, left * 4
            cv2.rectangle(img, (left, top), (right, bot), (0, 255, 0), 2)
            cv2.rectangle(img, (left, bot - 35), (right, bot), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (left + 6, bot - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('Webcam', img)

        if cv2.waitKey(1) & 0xff == 27:
            break

