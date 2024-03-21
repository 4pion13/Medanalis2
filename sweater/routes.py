import flask
from flask import Flask, render_template, request, redirect, session, url_for
import flask_session
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from sweater.models import UserInfo, Symptoms, Doctor_info, Doctor_schedule
from sweater import login_manager, db, app, mail,  Message, ALLOWED_EXTENSIONS
import uuid, os
import joblib
import numpy as np
import datetime
from cryptography.fernet import Fernet


key = Fernet.generate_key()
fernet = Fernet(key)
loaded_model = joblib.load('medmodel/model_cat.joblib')



@login_manager.user_loader
def load_user(user_id):
    return UserInfo.query.get(int(user_id))

@app.route('/f1', methods=['POST','GET'])
def main_first():
     
     if current_user.is_authenticated:
        
        status = True
        if request.method == "POST":
            number = request.form.get('numeric')
            print(number)
            enctex = fernet.encrypt(str(number).encode())

            return redirect(url_for('analyse', enctex=enctex))
        
        return render_template("mainpage.html", methods=['POST','GET'], status = status, status_first = True)

     else:
        if request.method == "POST":
            number = request.form.get('numeric')
            enctex = fernet.encrypt(str(number).encode())
            return redirect(url_for('number_login', enctex=enctex))

            print(number)

        return render_template("mainpage.html", methods=['POST','GET'])
     
@app.route('/', methods=['POST','GET'])
def mainpage():
     
     if current_user.is_authenticated:
        status = True
        if request.method == "POST":
            number = request.form.get('numeric')
            print(number)
            enctex = fernet.encrypt(str(number).encode())

            return redirect(url_for('analyse', enctex=enctex))
            
        return render_template("mainpage.html", methods=['POST','GET'], status = status, status_first = False)

     else:
        if request.method == "POST":
            number = request.form.get('numeric')
            enctex = fernet.encrypt(str(number).encode())
            return redirect(url_for('number_login', enctex=enctex))

            print(number)

        return render_template("mainpage.html", methods=['POST','GET'])
     


@app.route('/login/<enctex>', methods=['POST','GET'])
def number_login(enctex):
    if current_user.is_authenticated:
        return redirect(url_for('analyse', enctex=enctex))
    else:
        if request.method == "POST":
            email = request.form.get('email')
            password = request.form.get('password')

            # Find user by email entered
            user = UserInfo.query.filter_by(email=email).first()
            status = UserInfo.query.filter_by(status="Admin", email=email).first()

            # Email doesn't exist
            if not user:
                flash("Такого пользователя не существует!")
                return redirect(url_for('login'))
            # Password incorrect
            elif not check_password_hash(user.password, password):
                flash('Пароль не подходит!')

            else:
                login_user(user)
                return redirect(url_for('analyse', enctex=enctex))
        
        return render_template("login.html", logged_in=current_user.is_authenticated)
         


@app.route('/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('test_three'))
    else:
        if request.method == "POST":
            email = request.form.get('email')
            password = request.form.get('password')

            # Find user by email entered
            user = UserInfo.query.filter_by(email=email).first()
            status = UserInfo.query.filter_by(status="Admin", email=email).first()

            # Email doesn't exist
            if not user:
                flash("Такого пользователя не существует!")
                return redirect(url_for('login'))
            # Password incorrect
            elif not check_password_hash(user.password, password):
                flash('Пароль не подходит!')

            else:
                login_user(user)
                return redirect(url_for('main_first'))

        return render_template("login.html", logged_in=current_user.is_authenticated)
    

@app.route('/symptomcounter', methods=['POST','GET'])
def symptomcounter():
    if current_user.is_authenticated:
        status = True
        return render_template("modalcounter.html", methods=['POST','GET'], status = status)
    else:
        return redirect(url_for('login'))


@app.route('/registration', methods=['POST','GET'])
def registration_user():
    if current_user.is_authenticated:
        return redirect(url_for('analyse'))
    else:
        if request.method == "POST":

            if UserInfo.query.filter_by(email=request.form.get('email')).first():
                # User already exists
                flash("You've already signed up with that email, log in instead")
                return redirect(url_for('login'))

            hash_and_salted_password = generate_password_hash(
                request.form.get('password'),
                method='pbkdf2:sha256',
                salt_length=8
            )
            new_user = UserInfo(
                email=request.form.get('email'),
                name=request.form.get('name'),
                password=hash_and_salted_password,
                status="Admin",
                age=request.form.get('age'),
            )

            db.session.add(new_user)
            db.session.commit()
            flash('The account has been created.')
            return redirect(url_for("login"))

        return render_template("registration.html", methods=['POST','GET'])




@app.route('/doctoranalyzer/<enctex>/', methods=['POST','GET'])
def analyse(enctex):
    if current_user.is_authenticated:
        dectex = fernet.decrypt(enctex).decode()
        print(dectex)
        number_list = []
        for item in range(int(dectex)):
            number_list.append(item)

        symptoms_list = Symptoms.query.with_entities(Symptoms.Symptom).all()


            #print(loaded_model.predict((np.array([1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])).reshape(1, -1)))

        return render_template("index.html", symptoms_list=symptoms_list, name=current_user.name, number_list=number_list, status = True)

    else:
        return redirect(url_for('login'))
    

@app.route('/doctoranalyzer/send_data', methods=['POST'])
def analyse_send():
    if flask.request.method == 'POST':
            field_list = []
            for key, val in request.form.items():
                if key.startswith("field"):
                    field_list.append(val)


            for item in range(len(field_list)):
                if field_list[item] == "":
                    field_list[item] = 0

            print(field_list)
            for i, item in enumerate(field_list):
                print(i)
                print(item)
                if item == str(item):
                    request_data = Symptoms.query.filter_by(Symptom=item).first()
                    print(request_data)
                    if request_data != None:
                        field_list[i] = int(request_data.Weight)
                else:
                    field_list[i] = 0



            
            print(field_list)


            
            """
            print(field_list)
            print(dictionary.keys())
            for item in field_list:
                for value, key in dictionary.items():
                    if value.Sympt not in field_list:
                        continue
                    print('Сработало')
                    index = field_list.index(value.Sympt)
                    print(index)
                    field_list[index] = int(key.Wei)
            print(field_list)
            """
            print(field_list)

            while len(field_list) <= 13:
                field_list.append(0)

            print(field_list)
            
            #if all(isinstance(item, int) for item in field_list) == False:
                #flash('Select a value from the list!')
            
                #return redirect(url_for('analyse'))
            

            result = loaded_model.predict((np.array(field_list)).reshape(1, -1))
            print(*result)
            print(result)
            return result[0][0]

@app.route('/doctoranalyzer/rep', methods=['POST','GET'])
def analyse_repeat():
    if flask.request.method == 'POST':
        number = request.form.get('numeric')
        print(number)
        enctex = fernet.encrypt(str(number).encode())
        return redirect(url_for('analyse', enctex=enctex))
    

@app.route('/doctor_choice', methods=['POST','GET'])
def doctor_choice():
    if current_user.is_authenticated:
        doctor_list = Doctor_info.query.all()
        print(doctor_list)
        if flask.request.method == 'POST':
            for key, val in request.form.items():
                if key.startswith("doctor"):
                    enctex = fernet.encrypt(str(val).encode())
                    return redirect(url_for('time', enctex=enctex))
                    
        return render_template("doctor_choice.html", doctor_list=doctor_list, status = True, methods=['POST','GET'])
    else:
        return redirect(url_for('login'))
    

@app.route('/time/<enctex>/', methods=['POST','GET'])
def time(enctex):
    if current_user.is_authenticated:
        dectex = fernet.decrypt(enctex).decode()
        #currentDate = datetime.datetime.now()
        currentDate = datetime.date(2024, 3, 18)
        week_now = currentDate.isocalendar()[1]
        request_name = Doctor_info.query.filter_by(id = dectex).first()
        request_data = Doctor_schedule.query.filter(Doctor_schedule.reception_time >= currentDate, Doctor_schedule.doctor_id == dectex, Doctor_schedule.week == week_now, Doctor_schedule.status == 0).all()
        request_data_two = Doctor_schedule.query.with_entities(Doctor_schedule.reception_time).filter_by(doctor_id = dectex).all()
        list = [[],[],[],[],[],[],[]]
        for item in request_data:
            list[item.reception_time.weekday()].append(item)
            #if item.reception_time.weekday() == 0:
            #    list[0].append(item)
        if flask.request.method == 'POST':
            for key, val in request.form.items():
                    if key.startswith("yes"):
                        new_status = Doctor_schedule.query.filter_by(id = val).update(dict(status = 1))
                        new_patient = Doctor_schedule.query.filter_by(id = val).update(dict(patients = current_user.id))
                        db.session.commit()
                        msg = Message(current_user.name, recipients=[current_user.email])
                        msg.html = "<h2>Hello</h2>\n<p>You have an appointment with a doctor.</p>"
                        mail.send(msg)
                        return redirect(url_for('user_menu'))
                    
    else:
        return redirect(url_for('login'))
                    

                    
        







    
    return render_template("doctor_time.html", status = True, methods=['POST','GET'], list = list, request_name = request_name)
    



@app.route('/client_menu', methods=['POST','GET'])
def user_menu():
    if current_user.is_authenticated:
        request_visit_data = Doctor_schedule.query.filter_by(patients = current_user.id).all()
        try:
            request_doctor_data = Doctor_info.query.filter_by(id = request_visit_data[0].doctor_id).first()
            if flask.request.method == 'POST':
                for key, val in request.form.items():
                    if key.startswith("accept"):
                        print(val)
                        new_status = Doctor_schedule.query.filter_by(id = val).update(dict(status = 0))
                        new_patient = Doctor_schedule.query.filter_by(id = val).update(dict(patients = 0))
                        db.session.commit()
                        return redirect(url_for('user_menu'))
            return render_template("client_menu.html", current_user = current_user, methods=['POST','GET'], status = True, request_visit_data=request_visit_data, request_doctor_data=request_doctor_data)
        except:
            print('Нет')

        


        return render_template("client_menu.html", current_user = current_user, methods=['POST','GET'], status = True, request_visit_data=request_visit_data)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))