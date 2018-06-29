from flask import Flask,render_template,request
import mysql.connector as mysql
import kairos_face as kf
import json
import cv2
app=Flask(__name__)
login_data=[]
register_data=[]
@app.route('/')
def webpage():
    return render_template('store_sql.html')
@app.route('/result',methods=['POST'])
def result():
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
    conn=mysql.connect(user='root',password='password',database='face',host='localhost')
    if conn.is_connected():
        print("Connected")
        curs=conn.cursor()
        #query='INSERT INTO cgi_info VALUES("%s","%d","%s","%s")'%(name,number,email,password))
        out = curs.execute('insert into registration1 values("%s","%d","%s","%s")'%(user_name,user_mobile,user_email,user_password))
        conn.commit()
        return render_template('capture.html')
@app.route('/capture',methods=['POST'])
def capture():
    def already_registered():
        recognized_faces = kf.recognize_face(file=img_path, gallery_name='a-gallery')
        status = recognized_faces['images'][0]['transaction']['status']
        if status=="success":
            return True
        elif status=="failure":
            return False
        else:
            return "Error"
    def register(img_path='face.jpg'):
        global cursor
        global conn
        fname='firstname'
        lname='lastname'
        dob='dob'
        email='email'
        branch='branch'
        contact='contact'
        cursor.execute("INSERT INTO registration (firstname,lastname,dob,email,branch,contact) VALUES (%s,%s,%s,%s,%s,%s)", (fname,lname,dob,email,branch,contact));
        conn.commit()
        cursor.execute("SELECT * FROM registration where contact="+contact)
        out=cursor.fetchall()
        sid=out[0][0]
        return sid
    def enroll_student(sid,img_path='face.jpg'):
        enrolled_face = kf.enroll_face(file=img_path, subject_id=str(sid), gallery_name='a-gallery')
        status = enrolled_face['images'][0]['transaction']['status']
        if status=="success":
            return "enrolled"
        elif status=="failure":
            return "failure"

    kf.settings.app_id = 'f58c7bf9'
    kf.settings.app_key = '1b68e4a2b7e125ecb49a5729f5d3ed57'
    img_path='face.jpg'

    conn =mysql.connect(user='root',password='password',database='face',host='localhost')
    cursor=conn.cursor()
    var=already_registered()
    if var:
        print("mark attandance")
    else:
        sid=register()
        enroll_student(sid)


if __name__=="__main__":
    app.run(debug=True,port=9997)
