from flask import Flask, render_template, request, session
import os

application.secret_key = 'bismillaah'
application = Flask(__name__)

@application.route('/', methods=['GET', 'POST'])
def home():
    return index()

@application.route('index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['alamat']
        #tes = "Halo"
        return render_template('index.html', url=url)
    else:
        return render_template('index.html')

@application.route('/login', methods=['GET', 'POST'])
def do_admin_login():
    error = None
    if request.method == 'POST':
        if request.form['password'] == '1234':
            session['logged_in'] = True
            return render_template('index.html')
        else:            
            error = True
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')
        
@application.route("/logout")
def logout():
    session['logged_in'] = False
    #return home()
    #print("admin keluar")
    return render_template('login.html')

if __name__ == "__main__":
    application.run()
