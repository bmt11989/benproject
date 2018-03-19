import os
from flask import Flask, render_template, send_from_directory
app = Flask(__name__)

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

@app.route('/upload',methods=["post"])
def upload():
    pass


#Upload files
#Download files
#List files

if __name__ == "__main__":
    app.run()

