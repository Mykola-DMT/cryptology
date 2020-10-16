from app import app
from flask import render_template,flash,redirect, request, url_for
from werkzeug.utils import secure_filename
from datetime import date
import re
import json
import os
from app import MAX_FILE_SIZE,ALLOWED_EXTENSIONS,UPLOAD_FOLDER
from collections import OrderedDict
import ast

main_string='.'
key=0
file_string = '.'

@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    today=date.today()
    return render_template('index.html',today=today)

@app.route('/upload',methods=['GET','POST'])
def upload():
    global main_string, file_string
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
            main_string = str(string,'utf-8')
            file_string = str(string,'utf-8')
            #main_string=str(f.read(),'utf-8')
            return redirect('/')
    return render_template('upload.html')

k=0
@app.route('/task2', methods=['GET','POST'])
def task2():
    global main_string,key,k
    result={}
    if request.method=='POST':

        # if request.form.get('save results')=='save':
        #     s_type = ''
        #     if k == 1:
        #         s_type='Encrypt'
        #     elif k == 2:
        #         s_type='Decrypt'
        #     string = re.sub(r'[^A-Za-z]', '', main_string).lower()
        #     after=smpl_repl(string,key,s_type)
        #     result=get_dict_repl(string,after)
        #     save(result)
            #return redirect(url_for('save',letters=result))

        if request.form.get('upload file') == 'upload':
            return redirect(url_for('upload'))

        elif request.form.get('in message') == 'input text':
            main_string = request.form['message'] 
        
        elif request.form.get('in key') == 'input text':
            key = int(request.form['key'])
            save(get_dict_repl(key)) 

        elif request.form.get('change ltr') == 'change':
            s_type = ''
            if k == 1:
                s_type='Encrypt'
            elif k == 2:
                s_type='Decrypt'
            result=get_dict_from_json()
            return redirect(url_for('change_table'))

        elif request.form.get('show table') == 'show':
            s_type = ''
            if k == 1:
                s_type='Encrypt'
            elif k == 2:
                s_type='Decrypt'
            string = re.sub(r'[^A-Za-z]', '', main_string).lower()
            after=smpl_repl(main_string,s_type)
            result=get_dict_from_json()
            total=len(string)
            #save(result)
            return render_template('table.html', task=2, key=key, before = main_string, after = after, result1=result, text=s_type, total=total, value='Decrypted')

        elif request.form.get('encrypt') == 'encrypt':
            if main_string != '.':
                k=1
                s_type='Encrypt'
                after=smpl_repl(main_string,s_type)
                save_string(after)
                return render_template('task2.html', key=key, before = main_string, after = after)
            else:
                flash('There are empty fields!')

        elif request.form.get('decrypt')=='decrypt':
            if main_string != '.':
                k=2
                s_type='Decrypt'
                after=smpl_repl(main_string,s_type)
                save_string(after)
                return render_template('task2.html', task=2, key=key, before = main_string, after = after)
            else:
                flash('There are empty fields!')
    return render_template('task2.html')

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
            return render_template('table.html',task=1,result1=result,text=s_type,total=total,value='Count in %')

        elif request.form.get('sort by count')=='count':
            s_type='Count'
            result=get_dict('by_count',main_string)
            string = re.sub(r'[^A-Za-z]', '', main_string).lower()
            total=len(string)
            return render_template('table.html',task=1,result1=result,text=s_type,total=total,value='Count in %')

    return render_template('task1.html')


@app.route('/task3', methods=['GET','POST'])
def task3():
    global main_string, file_string
    after = '.'
    freq_dict=get_dict('by_letter',file_string)
    if request.method=='POST':

        if request.form.get('upload file') == 'upload':
            return redirect(url_for('upload'))

        elif request.form.get('show text') == 'show':
            return redirect(url_for('show'))

        elif request.form.get('undo text') == 'reset':

            main_string = file_string

        elif request.form.get('decrypt') == 'decrypt':
            s_type='Decrypt'
            after=smpl_repl(main_string,s_type)
            save_string(after)
            main_string = after
        elif request.form.get('change ltr') == 'change':
            result=get_dict_from_json()
            return redirect(url_for('change_table'))

        elif request.form.get('show table') == 'table':
            string = re.sub(r'[^A-Za-z]', '', main_string).lower()
            #after=smpl_repl(main_string,'Decrypt')
            result=get_dict_from_json()
            total=len(string)
            #save(result)
            return render_template('table.html', task=3, key=key,content=file_string,content1=main_string, result1=result, text='Decrypt', total=total, value='Decrypted', result2=freq_dict)
    return render_template('task3.html',content=file_string,content1=after,result2=freq_dict)
            

def dict_freq_repl():
    global main_string
    Ef='etaoinsrhldcumfpgwybvkxjqz'.upper()
    
    ch_d = get_dict('by_count',main_string)
    key_list = list(ch_d.keys())
    dic = {}
    i=0
    for s in Ef:
        dic[s]=key_list[i]
        i += 1
    result = dict(OrderedDict(sorted(dic.items())))
    save(result)
    return result



w1 = '.'
w2 = '.'
a_w = '.'
@app.route('/change_table',methods=['GET','POST'])
def change_table():
    global w1, w2, a_w
    d=get_dict_from_json()
    key_list = list(d.keys())
    val_list = list(d.values())
    if len(key_list) >= 1:
        if request.method == 'POST':
            if request.form.get('in ltr') == 'input text':
                w1 = request.form['ltr']

            elif request.form.get('in cr ltr') == 'input text':
                w2 = request.form['cr ltr']

            elif request.form.get('change') == 'change':
                a_w = d[w1]
                d[w1] = w2
                d[key_list[val_list.index(w2)]] = a_w

            elif request.form.get('save table') == 'save':
                save(d)
                return redirect('/')
                
    else:
        flash('Please Input message and key')
        return redirect('/')

    save(d)
    return render_template('change_table.html',value='Cipher',result1=d)


# dict:  letters -> count
def get_dict(typ,text):
    #text=str(text,'utf-8')
    string=re.sub(r'[^A-Za-z]', '', text).upper()
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

# dict:  letters -> new_letter(crypto)
def get_dict_repl(key):
    result = {}
    LTRS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    for s in LTRS:
        n = LTRS.find(s)
        n = n + key
        if n >= len(LTRS):
                n = n - len(LTRS)
        elif n < 0:
            n = n + len(LTRS)   
        result[s] = LTRS[n] 
    # for i in range(len(before)): 
    #     if before[i] not in result: 
    #         result[before[i]] = after [i]

    results=dict(OrderedDict(sorted(result.items())))
    return results

def smpl_repl(message,mode):
    ciphered = ''
    message = message.upper()
    d=get_dict_from_json()
    key_list = list(d.keys())
    val_list = list(d.values())
    for symbol in message:
        if symbol in key_list:
            
            if mode == 'Encrypt':
                n = key_list.index(symbol) 
                ciphered = ciphered + val_list[n]
            elif mode == 'Decrypt':
                n = val_list.index(symbol)
                ciphered = ciphered + key_list[n]

        else:
            ciphered = ciphered + symbol
    
    return ciphered


#@app.route('/save/<letters>')
def save(letters):
    
    with open('result.json','w') as outfile:
        json.dump(letters,outfile,indent=2)
    flash('Succesfuly saved!')

def save_string(string):
    with open('cipher.txt','w') as outfile:
        outfile.write(string)
         

@app.route('/show')
def show():
    global main_string
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
        letters[i]=round(letters[i]/total,3)
        #letters[i]/=total
    return letters

def total_count(all_letter):
    tot=sum(all_letter.values())
    return tot

def get_dict_from_json():
    with open('result.json','r') as f:
        d=json.load(f)
        # d=d.replace("\'", "\"")
        # di=json.loads(d)
        # print(type(di))
        # for key,value in di.items():
        #     print(key, ":", value)
    return d