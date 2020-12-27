from app import app
from flask import render_template,flash,redirect, request, url_for
from werkzeug.utils import secure_filename
from datetime import date
import re
import json
import os
from app import MAX_FILE_SIZE,ALLOWED_EXTENSIONS,UPLOAD_FOLDER
from collections import OrderedDict
#import ast
import string
import random


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
            filename = secure_filename(f.filename) 
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            f.seek(0)
            string=f.read()
            main_string = str(string,'utf-8').upper()
            main_string = main_string.replace(' ','')
            file_string = str(string,'utf-8').upper()
            #main_string=str(f.read(),'utf-8')
            return redirect('/')
    return render_template('upload.html')

@app.route('/upload_key',methods=['GET','POST'])
def upload_key():
    global key
    if request.method=='POST':
        if 'file' not in request.files:
            flash('No file Part')
            return redirect('/')
        f = request.files['file']
        if f.filename == '':
            flash('not selected file')
            return redirect('/')
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename) 
            f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
            f.seek(0)
            string=f.read()
            key = str(string,'utf-8')
            #save_key(key)
            #main_string=str(f.read(),'utf-8')
            return redirect(url_for('index'))
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

@app.route('/task4', methods=['GET','POST'])
def task4():
    global main_string,key
    
    if request.method=='POST':
        if request.form.get('upload file') == 'upload':
            return redirect(url_for('upload'))

        elif request.form.get('in message') == 'input text':
            main_string = request.form['message'].upper() 
        
        elif request.form.get('in key') == 'input text':
            key_text = request.form['key'].upper()
            key = VigenerKey(main_string,key_text)
            #save(get_dict_repl(key)) 

        elif request.form.get('upload key') == 'upload':
            return redirect(url_for('upload_key')) 

        elif request.form.get('encrypt') == 'encrypt':
            if main_string != '.' and len(key)<=len(main_string):
                
                key = VigenerKey(main_string,key)
                after = cipherVigener(main_string,key)
                #main_string = after
                save_string(after)
                return render_template('task4.html',key=key, before = main_string, after = after)
            else:
                flash('There are empty fields or something wrong!')

        elif request.form.get('decrypt')=='decrypt':
            if main_string != '.'and len(key)<=len(main_string):
                key = VigenerKey(main_string,key)
                after = ViginerDecrypt(main_string,key)
                save_string(after)
                return render_template('task4.html',key=key, before = main_string, after = after)
            else:
                flash('There are empty fields or something wrong!')
    return render_template('task4.html')  

@app.route('/task5', methods=['GET','POST'])
def task5():
    global main_string,key
    _key = ''
    if request.method=='POST':
        if request.form.get('upload file') == 'upload':
            return redirect(url_for('upload'))

        elif request.form.get('in message') == 'input text':
            main_string = request.form['message'].upper() 
            main_string = main_string.replace(' ','')

        elif request.form.get('upload key') == 'upload':
            return redirect(url_for('upload_key')) 

        elif request.form.get('in key') == 'input text':
            key_text = request.form['key'].upper()
            key_text = key_text.replace(' ','')
            if len(key_text) < len(main_string):
                flash('The length of the key(%s) must be at least the length of the string(%s)!'%(len(key_text),len(main_string)))
            else:
                key = key_text
        
        elif request.form.get('generate key') == 'generate':
            length = len(main_string)
            if length == 0:
                flash('Input message first!!!')
            else:
                key = get_random_string(length) 
                #save_key(key)

        elif request.form.get('encrypt') == 'encrypt':
            if main_string != '.' and len(key)>=len(main_string):
                after = cipherOTP(main_string,key)
                save_string(after)
                save_key(key)
                return render_template('task5.html',key=key, before = main_string, after = after)
            else:
                flash('There are empty fields or something wrong!')

        elif request.form.get('decrypt')=='decrypt':
            if main_string != '.'and len(key)>=len(main_string):
                after = decryptOTP(main_string,key)
                save_string(after)
                save_key(key)
                return render_template('task5.html',key=key, before = main_string, after = after)
            else:
                flash('There are empty fields or something wrong!')

    return render_template('task5.html', key = key, before = main_string)  

#######################Task 6(RSA)############################

def prime_check(a):
    if(a==2):
        return True
    elif((a<2) or ((a%2)==0)):
        return False
    elif(a>2):
        for i in range(2,a):
            if not(a%i):
                return False
    return True

def gcd_e(e,r):
    while(r!=0):
        e,r=r,e%r
    return e
 
#Extended Euclidean Algorithm
def eea(a,b):
    if(a%b==0):
        return(b,0,1)
    else:
        gcd,s,t = eea(b,a%b)
        s = s-((a//b) * t)
        return(gcd,t,s)

def mult_inv(e,r):
    gcd,s,_ = eea(e,r)
    if(gcd!=1):
        return None
    else:
        return s % r

def encrypt_rsa(pub_key,n_text):
    e,n=pub_key
    x=[]
    m=0
    for i in n_text:
        if(i.isupper()):
            m = ord(i)-65
            c=(m**e)%n
            x.append(c)
        # elif(i.islower()):               
        #     m= ord(i)-97
        #     c=(m**e)%n
        #     x.append(c)
        elif(i.isspace()):
            #spc=400
            x.append(400)
    return x

def decrypt_rsa(prvt_key,c_text):
    d,n=prvt_key
    txt=c_text.split(',')
    x=''
    m=0
    for i in txt:
        if(i=='400'):
            x+=' '
        else:
            m=(int(i)**d)%n
            m+=65
            c=chr(m)
            x+=c
    return x

publicKey=0
privateKey=0
P=0
Q=0
@app.route('/task6', methods=['GET','POST'])
def task6():
    global main_string,key, publicKey, privateKey, P, Q

    if request.method=='POST':
        if request.form.get('upload file') == 'upload':
            return redirect(url_for('upload'))

        elif request.form.get('in message') == 'input text':
            main_string = request.form['message'].upper() 
            #main_string = main_string.replace(' ','')

        elif request.form.get('P') == 'input text':
            key = 0
            try_p = int(request.form['primaryP'])
            if prime_check(try_p):
                P = try_p
            else:
                flash('P must be a primary number!')

        elif request.form.get('Q') == 'input text':
            key = 0
            try_q = int(request.form['primaryQ'])
            if prime_check(try_q):
                Q = try_q
            else:
                flash('Q must be a primary number!')

        elif request.form.get('upload pq') == 'upload':
            return redirect(url_for('upload_key')) 

        elif request.form.get('upload public') == 'upload':
            return redirect(url_for('upload_key')) 

        elif request.form.get('upload private') == 'upload':
            return redirect(url_for('upload_key')) 

        elif request.form.get('Public') == 'input text':
            key_text = request.form['key'].upper()
            key_text = key_text.split(',')
            
            if len(key_text) == 2:
                publicKey = tuple(int(x) for x in key_text)
            else:
                flash('Public Key must containt only 2 numbers!')
        
        elif request.form.get('Private') == 'input text':
            key_text = request.form['key'].upper()
            key_text = key_text.split(',')
            
            if len(key_text) == 2:
                privateKey = tuple(int(x) for x in key_text)
            else:
                flash('Private Key must containt only 2 numbers!')

        elif request.form.get('generate key') == 'generate':
            if key != 0:
                key = tuple(int(x) for x in key)
                P = key[0]
                Q = key[1] 
            n = P * Q
            r = (P-1)*(Q-1)
            for i in range(1,1000):
                if(gcd_e(i,r)==1):
                    e=i
                    
            d = mult_inv(e,r)

            publicKey = (e,n)
            privateKey = (d,n)

            savePrivateKey(privateKey)
            savePulicKey(publicKey)

        elif request.form.get('encrypt') == 'encrypt':
            if main_string != '.' and publicKey != 0:
                after = encrypt_rsa(publicKey, main_string)
                save_string(after)
                return render_template('task6.html',key=publicKey, before = main_string, after = after)
            else:
                flash('There are empty fields or something wrong!')

        elif request.form.get('decrypt')=='decrypt':
            if main_string != '.'and privateKey != 0:
                after = decrypt_rsa(privateKey, main_string)
                save_string(after)
                return render_template('task6.html',key=key, before = main_string, after = after)
            else:
                flash('There are empty fields or something wrong!')

    return render_template('task6.html', Public=publicKey, Private=privateKey ,before = main_string, p = P, q = Q) 


#######################Task 7(ElGamal)############################
def hashed(message, p):
    h=[]
    h.append(len(message))
    n=[ord(message[i])-65 for i in range(len(message))]
    
    for i in range(1,len(message)+1):
        h.append(((h[i-1] + n[i-1]) ** 2) % p)
    
    return h[len(h)-1]

def gcd(a, b): 
    if a < b: 
        return gcd(b, a) 
    elif a % b == 0: 
        return b; 
    else: 
        return gcd(b, a % b) 

def mod(g,x,p):
    res = int(pow(g,x)%p)
    return res

def sign(message, publicKey):
    p = publicKey[0]
    g = publicKey[1]
    a = publicKey[2]
    M = hashed(message, p)
    r = random.randint(1, p)

    while (gcd(r,p-1) != 1):
        r = random.randint(1, p)
    

    s1 = mod(g, r, p)
    u = mult_inv(r,p-1)
    
    s2 = ((M - a*s1) * u) % (p - 1)
    Signed = (message, s1, s2)
    return Signed

def verify_sign(Signed ,publicKey):
    m = hashed(Signed[0], publicKey[0])
    left_s = mod(publicKey[1], m, publicKey[0])
    
    right_s = (pow(publicKey[2], int(Signed[1])) * pow(int(Signed[1]), int(Signed[2]))) % publicKey[0]
    if(left_s == right_s):
        print('Verified')
        return True
    else:
        print('verification failed')
        return False

publicKey=0
privateKey=0
P=0
G=0
H=0
A=0
@app.route('/task7', methods=['GET','POST'])
def task7():
    global main_string,key, publicKey, privateKey, P, G, H, A

    if request.method=='POST':
        if request.form.get('upload file') == 'upload':
            return redirect(url_for('upload'))

        elif request.form.get('in message') == 'input text':
            main_string = request.form['message'].upper() 
            #main_string = main_string.replace(' ','')

        elif request.form.get('P') == 'input text':
            key = 0
            try_p = int(request.form['primaryP'])
            if prime_check(try_p):
                P = try_p
               
            else:
                flash('P must be a primary number!')

        elif request.form.get('G') == 'input text':
            key = 0
            try_g = int(request.form['primaryG'])
            if 1 <= try_g < P:
                G = try_g
                
            else:
                flash('G must be in [1, p-1]')

        elif request.form.get('upload pq') == 'upload':
            return redirect(url_for('upload_key')) 

        elif request.form.get('upload public') == 'upload':
            return redirect(url_for('upload_key')) 

        elif request.form.get('upload private') == 'upload':
            return redirect(url_for('upload_key')) 

        elif request.form.get('Public') == 'input text':
            key_text = request.form['key'].upper()
            key_text = key_text.split(',')
            
            if len(key_text) == 3:
                publicKey = tuple(int(x) for x in key_text)
            else:
                flash('Public Key must containt only 3 numbers!')
        
        elif request.form.get('Private') == 'input text':
            key_text = request.form['key'].upper()
            key_text = key_text.split(',')
            
            if len(key_text) == 3:
                privateKey = tuple(int(x) for x in key_text)
            else:
                flash('Private Key must containt only 3 numbers!')

        elif request.form.get('generate key') == 'generate':
            if key != 0:
                key = key.split(',')
                key = tuple(int(x) for x in key)
                P = key[0]
                G = key[1]
            
            A = random.randint(1, P)
            H = mod(G, A, P)

            while(A == H):
                A = random.randint(1, P) 
                H = mod(G, A, P)


            publicKey = (P, G, H)
            privateKey = (P, G, A)

            savePrivateKey(privateKey)
            savePulicKey(publicKey)


        elif request.form.get('sign') == 'sign':
            if key != 0 and isinstance(key, str):
                key = key.split(',')
                privateKey = tuple(int(x) for x in key)
            if main_string != '.' and privateKey != 0:
                after = sign(main_string, privateKey)
                save_signed(after)
                return render_template('task7.html',key=privateKey, before = main_string, after = after)
            else:
                flash('There are empty fields or something wrong!')

        elif request.form.get('verify')=='verify':
            if key != 0 and isinstance(key, str):
                key = key.split(',')
                publicKey = tuple(int(x) for x in key)
                
            if main_string != '.'and publicKey != 0:
                signed = main_string.split(',')
                verify = verify_sign(signed, publicKey)
                if(verify):
                    after = 'Signature verification successful, signature Valid'
                    flash('Signature verification successful, signature Valid')
                else:
                    after = 'Signature verification successful, signature Invalid'
                    flash('Signature verification successful, signature Invalid')
                save_string(after)
                return render_template('task7.html',key=publicKey, before = main_string, after = after)
            else:
                flash('There are empty fields or something wrong!')

    return render_template('task7.html', Public=publicKey, Private=privateKey ,before = main_string, p = P, g = G, h=H, a=A) 



def cipherOTP(string,key):
    cipher_text = []
    for i in range(len(string)):
        s = (ord(string[i]) - ord('A'))
        k = (ord(key[i]) - ord('A')) 
        x = (s ^ k)
        x += ord('A') 
        cipher_text.append(chr(x)) 
    return("" . join(cipher_text))

def decryptOTP(cipher_text,key):
    orig_text = [] 
    for i in range(len(cipher_text)): 
        c=(ord(cipher_text[i]) - ord('A')) 
        k=(ord(key[i]) - ord('A')) 
        x = (c ^ k)           
        x += ord('A') 
        orig_text.append(chr(x)) 
    return("" . join(orig_text)) 


def VigenerKey(string, key): 
    key = list(key) 
    if len(string) == len(key): 
        return(key) 
    else: 
        for i in range(len(string) - len(key)): 
            key.append(key[i % len(key)]) 

    #return str(key)
    return("" . join(key)) 

# def cipherOTP(string,key):
#     cipher_text = []
#     for i in range(len(string)):
#         x = (ord(string[i]) + ord(key[i])) % 26
#         x += ord('A') 
#         cipher_text.append(chr(x)) 
#     return("" . join(cipher_text))

def cipherVigener(string, key): 
    #string = string.replace(' ','')
    cipher_text = [] 
    for i in range(len(string)): 
        x = (ord(string[i]) + ord(key[i])) % 26
        x += ord('A') 
        cipher_text.append(chr(x)) 
    return("" . join(cipher_text)) 

def ViginerDecrypt(cipher_text, key): 
    orig_text = [] 
    for i in range(len(cipher_text)): 
        x = (ord(cipher_text[i]) - ord(key[i]) + 26) % 26
        x += ord('A') 
        orig_text.append(chr(x)) 
    return("" . join(orig_text)) 

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

def get_random_string(length):
    letters = string.ascii_uppercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

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
    if isinstance(string,list):
        with open('cipher.txt','w') as outfile:
            outfile.write(','.join(str(i) for i in string))
            outfile.close()
    else:
        with open('cipher.txt','w') as outfile:
            outfile.write(string)
            outfile.close()

def save_signed(signed):
    with open('signedText.txt','w') as outfile:
        outfile.write(','.join(str(i) for i in signed))
        outfile.close()

def savePulicKey(PubK):
    with open('publicKey.txt','w') as outfile:
        outfile.write(','.join(str(i) for i in PubK))
        outfile.close()

def savePrivateKey(PrvtK):
    with open('privateKey.txt','w') as outfile:
        outfile.write(','.join(str(i) for i in PrvtK))
        outfile.close()

def save_key(string):
    #s = string.upper()
    if isinstance(string,tuple) or isinstance(string,list) :
        with open('key_string.txt','w') as outfile:
            outfile.write(','.join(str(i) for i in string))
            outfile.close()
    else: 
        with open('key_string.txt','w') as outfile:
            outfile.write(string)         
            outfile.close()

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