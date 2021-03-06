#!/usr/bin/python
import sys
import os.path
import numpy as np
import cv2

debug = 1  # turns debug messaging/display on and off

if debug:
    print 'Input file: ',str(sys.argv[1])

# get the filename, minus the extension
filename = os.path.basename(os.path.splitext(sys.argv[1])[0])

# load image as is
input = cv2.imread(str(sys.argv[1]), -1)

if debug:
    # show input image
    cv2.imshow("input", input)

# set up cascades
face_cascade = cv2.CascadeClassifier('./classifiers/haarcascade_frontalface_default.xml')
    #face_cascade = cv2.CascadeClassifier('./classifiers/lbpcascade_frontalface.xml') #likely faster, since int based instead of float
eye_cascade = cv2.CascadeClassifier('./classifiers/haarcascade_eye.xml')
    #eye_cascade = cv2.CascadeClassifier('./classifiers/haarcascade_eye_tree_eyeglasses.xml') #causes my laptop to crash hard

# get grayscale version of input image
gray = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)

# find the face
faces = face_cascade.detectMultiScale(gray, 1.3, 5)
# check to make sure a face was found, return error if not
if(len(faces) < 1):
    # drop image into "no faces found" folder for later analysis
    cv2.imwrite('./anomalies/faces/'+filename+'.png', gray)
    # db shoud flag this entry as a problem
    if debug:
        print 'Error: No face found'
    sys.exit(1)
elif (len(faces) > 1):
    # drop image into "no faces found" folder for later analysis
    cv2.imwrite('./anomalies/faces/'+filename+'.png', gray)
    # db shoud flag this entry as a problem
    if debug:
        print 'Error: Too many faces found'
    #sys.exit(2)
else:
    # drop image into "faces found" folder for later Face training
    if debug:
        print len(faces), 'faces found.'
#box the face
for (x,y,w,h) in faces:
    # save off roi_color into a "found faces" folder for later Eye training
    roi_color = input[y:y+h, x:x+w]
    cv2.imwrite('./extractedfeatures/faces/'+filename+'.png', roi_color)
    # draw the box
    cv2.rectangle(input,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    # find the eyes
    eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 4)
    # need to make sure there are no eyes inside of eyes
    
    # check to make sure 2 eyes were found, return error if not (note: change to 1 eye, since some people may only have 1)
    if(len(eyes) < 1):
        # drop image into "no eyes found" folder for later analysis
        cv2.imwrite('./anomalies/faces/'+filename+'.png', roi_gray)
        # db shoud flag this entry as a problem
        if debug:
            print 'Error: Not enough eyes found'
        sys.exit(3)
    elif(len(eyes) > 2):
        # drop image into "no eyes found" folder for later analysis
        cv2.imwrite('./anomalies/faces/'+filename+'.png', roi_gray)
        # db shoud flag this entry as a problem
        if debug:
            print 'Error: Too many eyes found'
        #sys.exit(4)
    else:
        if debug:
            print len(eyes), 'eyes found.'
    #box the eyes
    i = 1
    for (ex,ey,ew,eh) in eyes:
        # save off found eyes into a "found eyes" folder for later training (good eyes/bad eyes/etc)
        roi_eye = roi_color[ey:ey+eh, ex:ex+ew]
        cv2.imwrite('./extractedfeatures/eyes/'+filename+'-'+str(i)+'.png', roi_eye)
        i = i+1
        #draw the box
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

if debug:
    # display outlined features, wait for key
    cv2.imshow('output',input)
    cv2.waitKey(0)

# close
if debug:
    cv2.destroyAllWindows()
sys.exit(0)
