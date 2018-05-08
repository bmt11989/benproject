
import os
from flask import Flask, render_template, send_from_directory, request, redirect, session

import hashlib
salt = "Glhk2!"

import pymysql


cnx = pymysql.connect(user='root', password='Cundis00!',
                                host ='127.0.0.1',
                                database='users_passwords')

def execute_query(sql):
    cursor = cnx.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    return result


app = Flask(__name__)

app.secret_key = 'admin'
ALLOWED_EXTENSIONS = set(['jpg', 'wav', 'mp3', 'mp4', 'mov' , 'txt', 'doc', 'docx', 'pdf', 'ppt', 'pptx'])

app.debug = True
source_folder = r"C:\Users\Ben\benproject"

@app.route('/list')
def list_folderroot():
    if session['logged_in'] !=  True:
         return redirect('/login')
    folder_contents = os.listdir(os.path.join(source_folder, directory))
    filelist = []
    folderslist = []
    for i in folder_contents:
        if os.path.isfile(os.path.join(source_folder, directory, i)) == True:
            filelist.append(i)
        elif os.path.isdir(os.path.join(source_folder, directory, i)) == True:
            folderslist.append(i)

    return render_template("index.html", files=filelist, folders=folderslist)


@app.route('/list/<path:directory>')
def list_folder(directory):
    if session['logged_in'] !=  True:
         return redirect('/login')
    folder_contents = os.listdir(os.path.join(source_folder, directory))
    filelist = []
    folderslist = []
    for i in folder_contents:
        if os.path.isfile(os.path.join(source_folder, directory, i)) == True:
            filelist.append(i)
        elif os.path.isdir(os.path.join(source_folder, directory, i)) == True:
            folderslist.append(i)

    return render_template("index.html", files=filelist, folders=folderslist)

@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(source_folder,filename)

@app.route('/delete/<path:filename>')
def delete(directory):
    folder_contents = os.listdir(os.path.join(source_folder, directory))
    filelist = []
    folderslist = []
    for i in folder_contents:
        if os.path.isfile(os.path.join(source_folder, directory, i)) == True:
            filelist.os.remove(i)
        elif os.path.isdir(os.path.join(source_folder, directory, i)) == True:
            folderslist.os.remove(i)


@app.route('/upload', methods=['POST'])
def upload_file():
    username = session['username']
    if request.method == 'POST':
        print(request.files)
        file = request.files['uploadfile']
    if allowed_file(file.filename):
        print(file)
        file.save(os.path.join(source_folder, username, file.filename))
        return redirect('/list/' + username)
    else:
        folder_contents = os.listdir(source_folder)
        filelist = []
        folderslist = []
        for i in folder_contents:
            if os.path.isfile(os.path.join(source_folder, i)) == True:
                filelist.append(i)
            elif os.path.isdir(os.path.join(source_folder, i)) == True:
                folderslist.append(i)
        return redirect('/list/' + username)


def allowed_file(filename):
    f = filename.split('.')
    extension = f[1]
    if extension in ALLOWED_EXTENSIONS:
        return True
    return False


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
            session['username'] = username
            return redirect('/list/' + username)
    else:
            error ='Invalid credentials'
    return render_template('login.html', error = error)

def check_credentials(username,password):
    sql = "select username, password from user_credentials where username = '{}'".format(username)
    result = execute_query(sql)
    hp = hash_password(password)
    print(hash_password(password))
    if username == result[0] and hp == result[1]:
        return True
    return False


def hash_password(password):
    h = hashlib.sha256(password.encode('utf-8') + salt.encode('utf-8'))
    return h.hexdigest()

@app.route('/logout', methods=['GET'])
def logout():
    session['logged_in'] = False
    return redirect ('/login')


if __name__ == "__main__":
#app.run()
    context = ('C:\securestore.crt', 'C:\securestore.key')
    app.run(host='127.0.0.1', port='5000', debug = True, ssl_context=context)

