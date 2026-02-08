from flask import Flask, render_template,request, redirect, url_for, session, flash, jsonify
from flask_socketio import SocketIO, emit, join_room
from fonctions import *
from model.user import User
from model.station import Station
from model.config import Config
import secrets
from datetime import timedelta, date
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message





app = Flask('__name__')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)


socketio = SocketIO(app, cors_allowed_origins="*")
app.config.from_object(Config)
mail = Mail(app)

@app.route('/', methods = ['GET', 'POST'])
def index():
       
    return render_template('index.html')



@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User(email=email, password=password).Get_user()
        
        if user and check_password_hash(user.password, password):
            session['email'] = email
            session['name'] = user.nom
            session['id'] = user.id
            session['ville'] = user.ville
            session['quartier'] = user.quartier
            return redirect(url_for('acceuil'))
        else:
            flash('Email ou mot de passe incorrect', 'danger')
    return render_template('login.html')




@app.route('/slogin', methods = ['GET', 'POST'])
def slogin():
    if request.method == 'POST':
        title = request.form['title']
        ville = request.form['ville']
        station = Station(title=title).Get_station()
        if station and station.ville == ville:
            session['title'] = title
            return redirect(url_for('station_manage'))
        else:
            flash('Nom de station ou ville incorrect', 'danger')
    return render_template('slogin.html')




@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        nom = request.form['fullname']
        email = request.form['email']
        tel = request.form['phone']
        password = request.form['password']
        confirm = request.form['confirm-password']
        hash_password = generate_password_hash(password)
        ville = 'Yaounde'
        quartier = request.form['quartier']
        
        if password != confirm:
            flash('Les mots de passe ne correspondent pas', 'danger')
            return render_template('register.html')

        user = User(nom=nom, email=email, tel=tel, password=hash_password, ville=ville, quartier=quartier)
        
        if user.Add_user():
            flash('Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Email déjà utilisé. Veuillez choisir un autre email.', 'danger')
    return render_template('register.html')



@app.route('/acceuil')
def acceuil():
    if 'id' in session:
        avatar = trunc_name(session['name'])
        if 'stations' not in session:
            stations = Station().Get_all()
            nearest = get_nearest_stations(stations, quarter= session['quartier'])
            nearest = [{
                'title': n.title,
                'address': n.address,
                'tel': n.tel,
                'localisation': n.localisation,
                'hours': n.hours,
                'stock': n.stock
            } for n in nearest]
            session['stations'] = nearest
        
        return render_template('acceuil.html', avatar = avatar)
    else:
        return redirect(url_for('login'))
    
    
    
@app.route('/reservation/<title>', methods = ['GET', 'POST'])
def reservation(title):
    if 'id' in session or 'title' in session:
        avatar = trunc_name(session['name'])
        st = Station(title = title).Get_station()
        return render_template('reservation.html', title=title, avatar=avatar, station=st)
    else:
        return redirect(url_for('login'))
    
    
@app.route('/station_manage', methods = ['GET', 'POST'])
def station_manage():
    if 'title' in session:
        avatar = trunc_name(session['title'])
        st = Station(title = session['title']).Get_station()
        return render_template('station-manage.html', title=session['title'], avatar=avatar, station=st)
    else:
        return redirect(url_for('slogin'))
    
    
@app.route('/update_stock/<stock>', methods = ['GET', 'POST'])
def update_stock(stock):
    if 'title' in session:
        st = Station(title = session['title']).Get_station()
        st.stock = stock
        st.Update(title = session['title'])
        
        avatar = trunc_name(session['title'])
        return redirect(url_for('station_manage', title = session['title'], avatar=avatar, station=st))
    else:
        return redirect(url_for('slogin'))
    
    
@app.route('/payment/<title>', methods = ['GET', 'POST'])
def payment(title):
    if 'id' in session:
        avatar = trunc_name(session['name'])
        st = Station(title = title).Get_station()
        return render_template('payment.html', title=title, avatar=avatar, station=st)
    else:
        return redirect(url_for('login'))
    
    
@app.route('/confirmation/<title>', methods = ['GET', 'POST'])
def confirmation(title):
    if 'id' in session:
        avatar = trunc_name(session['name'])
        st = Station(title = title).Get_station()
        
        msg = Message("Reservation depuis le site SmartGaz ",
                recipients=[session['email']]                    
        )
        aujourdhui = date.today()
        msg.html = f"Reservation effectuée le : {aujourdhui} sur <span style='color: purple;'>SmartGaz</span>"
        msg.html += f"<p > <span style='font-weight: bolder;'>Station :</span> {title}</p>"
        msg.html += f"<p > <span style='font-weight: bolder;'>Adresse :</span> {st.address}</p>"
        msg.html += f"<p > <span style='font-weight: bolder;'>Prix :</span> 6500fcfa 1 bouteille</p>"
        msg.html += f"<p> Merci de votre confiance !</p>"
        
        mail.send(msg)
        return redirect(url_for('acceuil', avatar=avatar))
    else:
        return redirect(url_for('login', avatar=avatar))


@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    if 'id' in session:
        avatar = trunc_name(session['name'])
        user = User(email=session['email']).Get_user()
        return render_template('profile.html', avatar=avatar, user = user)
    else:
        return redirect(url_for('login'))
    
    
@app.route('/update_profile', methods = ['GET', 'POST'])
def update_profile():
    if request.method == 'POST':
        email = request.form['email']
        user = User(email=email).Get_user()
        user.nom = request.form['fullname']
        user.email = email
        user.tel = request.form['phone']
        user.ville = 'Yaounde'
        user.quartier = request.form['quartier']
        user.Update(session['id'])
        print("user updated"   )
        
        
    return redirect(url_for('profile'))
    
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/precedent')
def precedent():
    return redirect(request.referrer)



if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    

    