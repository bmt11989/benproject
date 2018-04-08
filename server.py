import os
from flask import Flask, render_template, send_from_directory, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/list/<path:directory>'
ALLOWED_EXTENSIONS = set([])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.debug = True
source_folder = r"C:\Users\Ben\benproject"

@app.route('/list/<path:directory>')
def list_folder(directory):
    folder_contents = os.listdir(os.path.join(source_folder,directory))
    print folder_contents
    filelist = []
    folderslist = []
    for i in folder_contents:
        if os.path.isfile(os.path.join(source_folder,directory,i)) == True:
            filelist.append(i)
        elif os.path.isdir(os.path.join(source_folder,directory,i)) == True:
            folderslist.append(i)

    return render_template("index.html",files=filelist, folders=folderslist)

@app.route('/list')
def list_folderroot():
    folder_contents = os.listdir(source_folder)
    filelist = []
    folderslist = []
    for i in folder_contents:
        if os.path.isfile(os.path.join(source_folder,i)) == True:
            filelist.append(i)
        elif os.path.isdir(os.path.join(source_folder,i)) == True:
            folderslist.append(i)

    return render_template("index.html",files=filelist, folders=folderslist)
@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(source_folder,filename)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    print (file)


#Upload files
#Download files
#List files

if __name__ == "__main__":
    app.run()

