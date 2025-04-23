from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import random
from datetime import datetime, timedelta


def add_item(item):
    con = sqlite3.connect('PhoneBook.db')
    cursor = con.cursor()
    
    con.commit()
    con.close()

def query_items(search):
    con = sqlite3.connect('PhoneBook.db')
    cur = con.cursor()

    con.close()

    return None
def check_user(user_name, password):
    con = sqlite3.connect('Phonebook.db')
    cur = con.cursor()

    user_andpw = cur.execute("SELECT username, password, user_id FROM Users").fetchall()
    
    found = False
    for tup in user_andpw:
        if user_name == tup[0] and password == tup[1]:
            found = True
            user = tup[2]
    if found == True:
        return user
    else:
        return -1
            
            


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rally_cat.db'
# db = SQLAlchemy(app)

@app.route("/")
def login():
    
    return render_template("landing.html")

@app.route("/Submit", methods=['GET', 'POST'])
def submit():
    
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    
    user_id = check_user(username, password)
    
    if  user_id != -1:
        return redirect(url_for('Welcome',user_id=user_id))
    else:
        return redirect(url_for('login'))

@app.route("/Welcome")
def Welcome():
    
    user_id = request.args.get('user_id')
    
    if user_id:
        return render_template("Welcome.html", user_id=user_id)
    return render_template("Welcome.html")


    
    return render_template("Welcome.html")

# class Item(db.Model):
#     __tablename__ = "Item"
#     item_id = db.Column(db.Integer, primary_key=True)
#     itemName = db.Column(db.String(50))
#     category = db.Column(db.String(50))
#     quantity = db.Column(db.String(50))
#     kosher = db.Column(db.Integer)
#     hallal = db.Column(db.Integer)
#     vegetarian = db.Column(db.Integer)
#     vegan = db.Column(db.Integer)
#     peanuts = db.Column(db.Integer)
#     gf = db.Column(db.Integer)
#     eggs = db.Column(db.Integer)
#     fish = db.Column(db.Integer)
#     soy = db.Column(db.Integer)
#     treenuts = db.Column(db.Integer)
#     shellfish = db.Column(db.Integer)

#     def __repr__(self):
#         return f'<Item {self.itemName}>'
    
#with app.app_context():
    #db.create_all()




if __name__ == "__main__":
    app.run(debug=True)