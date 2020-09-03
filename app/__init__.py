from flask import Flask


app=Flask(__name__)
MAX_FILE_SIZE=1024*1024+1
#app.config['MAX_CONTENT_LENGTH']=16*1024*1024


from app import routes