from flask import (Flask, url_for, render_template, request, redirect, flash)
import login

app = Flask(__name__)

app.secret_key = "whiptails"
numRequest=0

@app.route('/preferences', methods=['POST', 'GET'])
def login():
    if request.method == ('GET'):
        return render_template('userinfo.html')
    else:
        email = request.form.get("email")
        uname = request.form.get("username")
        pwd = request.form.get("password")
        pwd1 = request.form.get("password1")
        name = request.form.get("name")
        nname = request.form.get("nname")
        year = request.form.get("year")
        phnum =request.form.get("pnum")
        sprefs = request.form.get("radio")
        

        if email == "" or "@" not in email:
            flash("Invalid email address")
        if pwd1 == "" or pwd == "":
            flash("One or both of the password fields are incomplete")
        if pwd1!= pwd:
            flash("The passwords do not match")
        if name == "":
            flash("The name fields is incomplete")
        if uname =="":
            flash("The user name incomplete")
    
        if not any([email=="",pwd=="", pwd1!= pwd, name == "",uname ==""]):
            try:
                login.insert(name, email, uname, pwd, nname, phnum, year, \
                sprefs)
            except:
                flash("username already exist")
            # username not in database
    return render_template('userinfo.html')

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8081)
