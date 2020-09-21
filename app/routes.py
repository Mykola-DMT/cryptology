from app import app
from flask import render_template,flash,redirect, request, url_for
from werkzeug.utils import secure_filename
from datetime import date
import re
import json
import os
from app import MAX_FILE_SIZE,ALLOWED_EXTENSIONS,UPLOAD_FOLDER
from collections import OrderedDict

main_string='.'

@app.route('/')
@app.route('/index')
def index():
    today=date.today()
    return render_template('index.html',today=today)

@app.route('/upload',methods=['GET','POST'])
def upload():
    global main_string
    if request.method=='POST':
        if 'file' not in request.files:
            flash('No file Part')
            return redirect('/')
        f = request.files['file']
        if f.filename == '':
            flash('not selected file')
            return redirect('/')
        if f and allowed_file(f.filename):
            filename= secure_filename(f.filename) 
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            f.seek(0)
            string=f.read()
            main_string=str(string,'utf-8')
            #main_string=str(f.read(),'utf-8')
            return redirect(url_for('task1'))
    return render_template('upload.html')

@app.route('/task1', methods=['GET','POST'])
def task1():
    global main_string
    if request.method=='POST':

        if request.form.get('save results')=='save':
            result=get_dict('by_letter',main_string)
            return redirect(url_for('save',letters=result))

        elif request.form.get('upload file') == 'upload':
            return redirect(url_for('upload'))

        elif request.form.get('show text') == 'show':
            return redirect(url_for('show'))

        elif request.form.get('input') == 'input text':
            main_string = request.form['text'] 

        elif request.form.get('sort by letters') == 'letter':
            s_type='Letters'
            result=get_dict('by_letter',main_string)
            string = re.sub(r'[^A-Za-z]', '', main_string).lower()
            total=len(string)
            return render_template('table.html',result1=result,text=s_type,total=total)

        elif request.form.get('sort by count')=='count':
            s_type='Count'
            result=get_dict('by_count',main_string)
            string = re.sub(r'[^A-Za-z]', '', main_string).lower()
            total=len(string)
            return render_template('table.html',result1=result,text=s_type,total=total)

    return render_template('task1.html')


def get_dict(typ,text):
    #text=str(text,'utf-8')
    string=re.sub(r'[^A-Za-z]', '', text).lower()
    result_no_percent=dict(count_letter(string))
    total=total_count(result_no_percent)
    result=letter_percent(result_no_percent,total)
    if typ == 'by_letter':
        sort_by_letter=dict(OrderedDict(sorted(result.items())))
        return sort_by_letter

    elif typ == 'by_count':
        sort_by_count=dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
        return sort_by_count

    return result

@app.route('/save/<letters>')
def save(letters):
    
    with open('result.json','w') as outfile:
        json.dump(letters,outfile,indent=2)
    flash('Succesfuly saved!')
    return redirect('/')    

@app.route('/show')
def show():
    content = main_string
    return render_template('show.html',content=content)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

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