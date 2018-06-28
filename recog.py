#!/usr/bin/python3
import kairos_face as kf
import json
import mysql.connector as mysql
import cv2
import requests
import pyrebase
# credentials for kairos
# setting up API keys
kf.settings.app_id = ''
kf.settings.app_key = ''
img_path='face.jpg'
try :
	# create a connection with database
    conn =mysql.connect(user='root',password='password',database='face',host='localhost')
    cursor = conn.cursor()
    if already_registered():
        return "mark_attendance"
    else:
        sid = register()
        return enroll_student(sid)


except:
	print("Error")


def already_registered() :
	#recognizing registered faces
	recognized_faces = kf.recognize_face(file=img_path, gallery_name='students')

	status = recognized_faces['images'][0]['transaction']['status']

	if status == 'success' :
		return True

	elif status == 'failure' :
		return False

	else :
		print('Error in recognising')

def register(img_path='face.jpg') :

	global cursor
	global conn

	# storing data to list
	fname = 'firstname'
	lname = 'lastname'
	dob = 'dob'
	email = 'email'
	branch = 'branch'
	contact = 'contact'

	#data = [_fname,_lname,_dob,_email,_branch,_contact]

	# enter into the database
	cursor.execute("INSERT INTO registration (firstname,lastname,dob,email,branch,contact) VALUES (%s,%s,%s,%s,%s,%s)", (fname,lname,dob,email,branch,contact));
	conn.commit()

	cursor.execute("SELECT * FROM registration where contact="+contact)
	out = cursor.fetchall()

	sid = out[0][0]
	return sid

def enroll_student(sid,img_path='face.jpg') :
	#enrolling face
	enrolled_face = kf.enroll_face(file=img_path, subject_id=str(sid), gallery_name='students')
	#returning status
	status = enrolled_face['images'][0]['transaction']['status']

	if status == 'success':
		return "enrolled"
    # elif status=='failure':
    #     return "not enrolled"
