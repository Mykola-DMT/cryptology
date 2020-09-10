from flask import Flask

app=Flask(__name__)
MAX_FILE_SIZE=1024*1024+1

from app import routes