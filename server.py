
import os
from flask import Flask, flash, render_template, send_from_directory, request, redirect, url_for, session
from werkzeug.utils import secure_filename


import hashlib
salt = "thisissalt"

import mysql.connector
from mysql.connector import errorcode


cnx = mysql.connector.connect(user='root', password='Cundis00!',
                                host ='127.0.0.1',
                                database='users_passwords')

def execute_query(sql):
    cursor = cnx.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result

def execute_permission_query(sql):
    cursor = cnx.cursor()
    cursor.execute(sql)
    cursor.close()
    return result



app = Flask(__name__)

app.secret_key = 'admin'
ALLOWED_EXTENSIONS = set(['jpg', 'mp3','mp4', 'mov' ,'txt', 'doc'])

app.debug = True
source_folder = r"C:\Users\Ben\benproject"

@app.route('/list/<path:directory>')
def list_folder(directory):
    if session['logged_in'] == False:
         return redirect('/login')
    folder_contents = os.listdir(os.path.join(source_folder, directory))
    print folder_contents
    filelist = []
    folderslist = []
    for i in folder_contents:
        if os.path.isfile(os.path.join(source_folder, directory, i)) == True:
            filelist.append(i)
        elif os.path.isdir(os.path.join(source_folder, directory, i)) == True:
            folderslist.append(i)

    return render_template("index.html", files=filelist, folders=folderslist)
@app.route('/list')
def list_folderroot():
    if session['logged_in'] == False:
         return redirect('/login')
    folder_contents = os.listdir(source_folder)
    filelist = []
    folderslist = []
    for i in folder_contents:
        if os.path.isfile(os.path.join(source_folder, i)) == True:
            filelist.append(i)
        elif os.path.isdir(os.path.join(source_folder, i)) == True:
            folderslist.append(i)

    return render_template("index.html", files=filelist, folders=folderslist)

@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(source_folder,filename)

def allowed_file(filename):
    f = filename.split('.')
    extension = f[-1]
    if extension in ALLOWED_EXTENSIONS:
        return True
    return False


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        print request.files
        file = request.files['uploadfile']
        print file
        file.save(os.path.join(source_folder, file.filename))
        allowed_file(file.filename)
    return redirect("/list")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_credentials(username,password):
            session['logged_in'] = True
            flash('YAY')
            return render_template('whatever.html')
        else:
            error ='BOO'
    return render_template('login.html', error = error)

def check_credentials(username,password):
    sql = "select username, password from user_credentials where username = '{}'".format(username)
    print sql
    result = execute_query(sql)
    hp = hashpassword(password)
    if username == result[0] and hp == result[1]:
        return True
    return False


def hashpassword(p):
    h = hashlib.sha256(p + salt)
    return h.hexdigest()




def select_query(file_path,allowed_users):


    result = execute_permission_query(sql)





def insert_query():


    result = execute_permission_query(sql)







@app.route('/logout', methods=['GET'])
def logout():
    session['logged_in'] = False
    return redirect ('/login')





#Upload files
#Download files
#List files

if __name__ == "__main__":
    app.run()

