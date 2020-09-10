from app import app
from flask import render_template,flash,redirect, request, url_for
from werkzeug.utils import secure_filename
from datetime import date
import re
import json
import os
from app import MAX_FILE_SIZE
from collections import OrderedDict

@app.route('/')
@app.route('/index')
def index():
    today=date.today()
    return render_template('index.html',today=today)

@app.route('/task1', methods=['GET','POST'])
def task1():
    doc_path=os.path.abspath(os.path.dirname(__file__))+'/text.txt'
    doc=open(doc_path,'r',encoding='utf-8')
    all_string=doc.read()
    string=re.sub(r'[^A-Za-z]', '', all_string).lower()
    result_no_percent=dict(count_letter(string))
    total=total_count(result_no_percent)
    result=letter_percent(result_no_percent,total)
    sort_by_letter=dict(OrderedDict(sorted(result.items())))
    print(type(sort_by_letter))
    sort_by_count=dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
    if request.method=='POST':
        return redirect(url_for('save',letters=sort_by_letter))
    return render_template('task1.html',result1=sort_by_letter,result2=sort_by_count,total=total)

@app.route('/save/<letters>')
def save(letters):
    
    with open('result.json','w') as outfile:
        json.dump(letters,outfile,indent=2)
    return redirect('/')

def count_letter(string):
    all_letter = {} 
  
    for i in string: 
        if i in all_letter: 
            all_letter[i] += 1
            #all_letter[i].append()
        else: 
            all_letter[i] = 1
    return all_letter

def letter_percent(letters,total):
    for i in letters.keys():
        letters[i]=round(letters[i]/total,4)
        #letters[i]/=total
    return letters

def total_count(all_letter):
    tot=sum(all_letter.values())
    return tot

def get_dict_from_json():
    with open('result.json','r') as f:
        d=json.load(f)
        d=d.replace("\'", "\"")
        di=json.loads(d)
        print(type(di))
        for key,value in di.items():
            print(key, ":", value)
    return di