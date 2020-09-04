from app import app
from flask import render_template,flash,redirect, request, url_for
from werkzeug.utils import secure_filename
import re
import os
from app import MAX_FILE_SIZE
from collections import OrderedDict

@app.route('/')
@app.route('/index')
def index():
    doc_path=os.path.abspath(os.path.dirname(__file__))+'/text.txt'
    doc=open(doc_path,'r',encoding='utf-8')
    all_string=doc.read()
    string=re.sub(r'[^A-Za-z]', '', all_string).lower()
    result=dict(count_letter(string))
    sort_by_letter=OrderedDict(sorted(result.items()))
    sort_by_count=dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
    total=total_count(result)
    return render_template('index.html',result1=sort_by_letter,result2=sort_by_count,total=total)

def count_letter(string):
    all_letter = {} 
  
    for i in string: 
        if i in all_letter: 
            all_letter[i] += 1
        else: 
            all_letter[i] = 1
    return all_letter

def total_count(all_letter):
    tot=sum(all_letter.values())
    return tot
