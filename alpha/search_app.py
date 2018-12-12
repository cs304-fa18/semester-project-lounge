from flask import (Flask, url_for, flash, render_template, request, session, redirect)
import search_db


app = Flask(__name__)
app.secret_key = "whiptails"


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == 'GET':
        return render_template('searchForm.html')
    else:
        name = request.form.get("name")
        year= request.form.get("year")
        indust = request.form.get("Industry")
        
        if all([name=="", year=="", indust==""]):
            flash("enter something to filter your search by")
            return render_template('searchForm.html')
        # if year!="":
        #     try:
        #         int(year)
        #     except:
        #         flash("year is not an integer")
        #         return render_template('searchForm.html')
                
        searchItems = []
        if name!="":
            searchItems.append(["name", "%"+name+"%"])
        if year !="" and year.isdigit():
            searchItems.append(["classyear","%"+year+"%" ])
        if indust !="":
            searchItems.append(["iname","%"+indust+"%" ])
        
        transpose = zip(*searchItems)
        
        table = search_db.search(transpose)
        
        return render_template('searchForm.html', table=table)


@app.route("/profile", methods=["GET", "POST"])
def profile(username): #need to get a username from somewhere
    user= seach_db.preference(username)
    indus= search_db.preference(username)
    if user['sprefs']=='all':
        return render_template('preference.html', user=user, indus=indus)
    else:
        return render_template('preference_base.html', user=user)
    
    
    
    
    

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0',8080)
