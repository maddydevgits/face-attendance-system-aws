import streamlit as st
from datetime import datetime
import cv2
import os
import boto3

accessKey='' # ask admin to share access key
secretAccessKey='' # ask admin to share secret access
region='us-east-1'

def write_data_to_excel(k):
    f=open('attendance.csv','a')
    dummy=str(datetime.now())
    dummy=dummy.split(' ')
    f.writelines([k+',',dummy[0]+',',dummy[1].split('.')[0]+'\r\n'])
    f.close()

st.title('Smart Attendance System')
run=st.checkbox('Run Camera')

FRAME_WINDOW=st.image([])
camera=cv2.VideoCapture(0)
student_paths=os.listdir('students/')
client=boto3.client('rekognition',aws_access_key_id=accessKey,aws_secret_access_key=secretAccessKey,region_name=region)

while run:
    _,frame=camera.read()
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    FRAME_WINDOW.image(frame)
    
    cv2.imwrite('test.jpg',frame)
    for i in student_paths:
        imageSource=open('test.jpg','rb')
        imageTarget=open('students/'+i,'rb')
        response=client.compare_faces(SimilarityThreshold=70,SourceImage={'Bytes':imageSource.read()},TargetImage={'Bytes':imageTarget.read()})
        #st.write(response)
        if response['FaceMatches']:
            result=i.split('.')[0]
            st.success('Face Identified as ' + result)
            write_data_to_excel(result)
            st.write('Your attendance Recorded, please do uncheck the box')
            st.write('Thank You')
            run=False
            break
    run=False
    break