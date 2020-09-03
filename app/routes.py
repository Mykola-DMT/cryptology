from app import app
from flask import render_template,flash,redirect, request, url_for
from werkzeug.utils import secure_filename
import re
import os
from app import MAX_FILE_SIZE

@app.route('/')
@app.route('/index')
def index():
    doc_path=os.path.abspath(os.path.dirname(__file__))+'/text.txt'
    doc=open(doc_path,'r')
    all_string=doc.read()
    string=re.sub(r'[^A-Za-z]', '', all_string).lower()
    result=dict(count_letter(string))
    return render_template('index.html',result=result)

def count_letter(string):
    all_freq = {} 
  
    for i in string: 
        if i in all_freq: 
            all_freq[i] += 1
        else: 
            all_freq[i] = 1
    return all_freq
