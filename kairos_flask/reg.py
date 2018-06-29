from flask import Flask,render_template,request
import mysql.connector as mysql
import kairos_face as kf
import json
import cv2
app=Flask(__name__)
login_data=[]
register_data=[]
img_path='face.jpg'

@app.route('/')
def webpage():
    return render_template('store_sql.html')
@app.route('/result',methods=['POST'])
def result():
    global user_mobile
    result=request.form
    for data in result.items():
        register_data.append(data)
    name=register_data[0]
    user_name=name[1]
    mobile=register_data[1]
    user_mobile=int(mobile[1])
    email=register_data[2]
    user_email=email[1]
    password=register_data[3]
    user_password=password[1]
    # kf.settings.app_id = 'f58c7bf9'
    # kf.settings.app_key = '1b68e4a2b7e125ecb49a5729f5d3ed57'
    kf.settings.app_id = 'ed6e261d'
    kf.settings.app_key = 'bfe71f59834f765f8b215a06e9861434'
    img_path='face.jpg'
    print("hello")
    enrolled_face = kf.enroll_face(file=img_path, subject_id=str(user_mobile), gallery_name='a-gallery')
    print("hello w")
    face_id=enrolled_face['face_id']
    print(face_id)
    status = enrolled_face['images'][0]['transaction']['status']
    print(status)
    if status=="success":
        conn=mysql.connect(user='root',password='password',database='face',host='localhost')
        curs=conn.cursor()
        #curs.execute("INSERT INTO registration1 (face_id) VALUES (%s)", (face_id));
        #curs.execute('insert into registration1(face_id) values("%s")'%(face_id)' where contact='%(user_mobile))
        curs.execute('insert into registration1(name,contact,email,password,face_id) values("%s","%d","%s","%s","%s")'%(user_name,user_mobile,user_email,user_password,face_id))
        conn.commit()

    elif status=="failure":
        return False

    return render_template('login.html')

@app.route('/dashboard',methods=['POST'])
def dashboard():
    print("hello")
    recognized_faces = kf.recognize_face(file='index.jpeg', gallery_name='a-gallery')
    status = recognized_faces['images'][0]['transaction']['status']
    if status=="success":
        return render_template('dashboard.html')
    elif status=="failure":
        return False
    else:
        return "Error"
    return render_template('capture.html')

if __name__=="__main__":
    app.run(debug=True,port=9997)
