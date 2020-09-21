from flask import Flask

UPLOAD_FOLDER='C:'
ALLOWED_EXTENSIONS={'txt'}

app=Flask(__name__)
MAX_FILE_SIZE=1024*1024+1
app.secret_key='you-will-never-guess'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
main_string='.'

from app import routes