from flask import Flask, render_template, url_for, request, redirect, jsonify, session
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import random
from datetime import datetime, timedelta
import datetime

# gets specific column from user    
def get_info_item(USER, item):
    con = sqlite3.connect('PhoneBook.db')
    cur = con.cursor()
    info_item = cur.execute(f"SELECT {item} FROM Users WHERE user_id = {USER}").fetchall()
    con.close()
    return info_item[0][0]
    
# def remove_contact(USER, CONTACT):

    


def query_items(search):
    con = sqlite3.connect('PhoneBook.db')
    cur = con.cursor()

    con.close()

def get_birthdays(contacts):
    today = datetime.datetime.now()
    yearhold = str(today).split('-')[0]
    
    year = yearhold[2]
    year += yearhold[3]
    year = int(year)
    month = int(str(today).split('-')[1])
    day = int(str(today).split('-')[2].split(' ')[0])
    
    next7 = []
    birthday = []
    
    for contact in contacts:
        contactmonth = int(contact[9].split('/')[0])
        contactday = int(contact[9].split('/')[1])
        contactyear = int(contact[9].split('/')[2])
        
        if contactmonth == month:
            if contactday-7<day and contactday >= day:
                if contactday == day:
                    birthday.append((contact))
                else:
                    next7.append(contact)

        #print(f"{contactmonth}//{contactday}")
        #print(int(contactmonth))
        #print(f"{month}/{day}")
        
    return (next7, birthday)
    

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
    
def get_contacts(user):
    con = sqlite3.connect('Phonebook.db')
    cur = con.cursor()
    contacts = cur.execute(f"SELECT * FROM Contact_Info WHERE user_id == {user} ").fetchall()
    
    return contacts

# Add a contact
def add_contact(user_id):
    print("Add New Contact:")
    first = input("First Name: ")
    last = input("Last Name: ")
    phone = input("Phone Number: ")
    email = input("Email: ")

    con = sqlite3.connect('Phonebook.db')
    cursor = con.cursor()
    cursor.execute("INSERT INTO Contact_Info (user_id, first_name, last_name, phone, email) VALUES (?, ?, ?, ?, ?)",
                   (user_id, first, last, phone, email))
    con.commit()
    con.close()
    print("Contact added!\n")

# Edit a contact
    
def edit_contact(USER, CONTACT, firstname, lastname, email, phone, residence, company, birthday, score, description):
    con = sqlite3.connect('Phonebook.db')
    cursor = con.cursor()
    if birthday != "":
        cursor.execute(f'''UPDATE Contact_Info SET 
                        first_name = ?, 
                        last_name = ?, 
                        email = ?, 
                        phone = ?, 
                        residence = ?, 
                        company = ?, 
                        birthday = ?, 
                        friendship_score = ?,
                        relationship_context = ?
                        WHERE contact_id = ? AND user_id = ?''', (firstname, lastname, email, phone, residence, company, birthday, score, description, CONTACT, USER))
    else:
        cursor.execute(f'''UPDATE Contact_Info SET 
                        first_name = ?, 
                        last_name = ?, 
                        email = ?, 
                        phone = ?, 
                        residence = ?, 
                        company = ?, 
                        friendship_score = ?,
                        relationship_context = ?
                        WHERE contact_id = ? AND user_id = ?''', (firstname, lastname, email, phone, residence, company, score, description, CONTACT, USER))
    con.commit()
    con.close()
    

# Delete a contact
def delete_contact(user_id):
    contact_id = input("Enter the Contact ID to delete: ")

    con = sqlite3.connect('Phonebook.db')
    cursor = con.cursor()
    cursor.execute("DELETE FROM Contact_Info WHERE contact_id = ? AND user_id = ?", (contact_id, user_id))
    con.commit()
    con.close()
    print("Contact deleted!\n")    
            
            


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rally_cat.db'
# db = SQLAlchemy(app)
app.secret_key = '2d99dbc8730b4445330703f9ee7158ac'  # required to use sessions


@app.route("/")
def login():
    
    return render_template("landing.html")

@app.route("/Edit/<int:contact_id>")
def edit(contact_id):
    # render_template("Edit.html")
    user_id = session.get('user_id')
    username = get_info_item(user_id, 'first_name')
    contacts = get_contacts(user_id)
    contact = contacts[contact_id]
    
    birthday_info = get_birthdays(contacts)
    
    upcomingbirthdays = birthday_info[0]
    todaybirthdays = birthday_info[1]
    
    js_contacts = [list(contact) for contact in contacts]

    return render_template("Edit.html", user_id=user_id, username=username, contact=contact, js_contacts=js_contacts, upcomingbirthdays=upcomingbirthdays, todaybirthdays=todaybirthdays)

@app.route("/SubmitContact/<int:contact_id>", methods=['GET','POST'])
def submitContact(contact_id):
    
    user_id = session.get('user_id')

    
    first = request.form['first']
    last =  request.form['last']
    email = request.form['email']
    phone = request.form['phone']
    residence = request.form['residence']
    company = request.form['company']
    birthday = request.form['birthday']
    score = request.form['friendshipscore']
    description = request.form['description']
    
    if birthday != "":
        yearhold = str(birthday).split('-')[0]
        
        year = yearhold[2]
        year += yearhold[3]
        year = int(year)
        month = int(str(birthday).split('-')[1])
        day = int(str(birthday).split('-')[2].split(' ')[0])
        
        birthday = str(month)
        birthday += "/"
        birthday += str(day)
        birthday += "/"
        birthday += str(year)
        
        
    
    edit_contact(user_id, contact_id, first, last, email, phone, residence, company, birthday, score, description)

    
    
    
    username = get_info_item(user_id, 'first_name')
    contacts = get_contacts(user_id)
    
    birthday_info = get_birthdays(contacts)
    
    upcomingbirthdays = birthday_info[0]
    todaybirthdays = birthday_info[1]
    
    js_contacts = [list(contact) for contact in contacts]
    
    return render_template("Welcome.html", user_id=user_id, username=username, contacts=contacts, js_contacts=js_contacts, upcomingbirthdays=upcomingbirthdays, todaybirthdays=todaybirthdays)

    

@app.route("/Submit", methods=['GET', 'POST'])
def submit():
    
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    
    user_id = check_user(username, password)
    
    if  user_id != -1:
        session['user_id'] = user_id 
        return redirect(url_for('Welcome'))
    else:
        return redirect(url_for('login'))

@app.route("/Welcome")
def Welcome():
    
    user_id = session.get('user_id')
    username = get_info_item(user_id, 'first_name')
    contacts = get_contacts(user_id)
    
    birthday_info = get_birthdays(contacts)
    
    upcomingbirthdays = birthday_info[0]
    todaybirthdays = birthday_info[1]
    
    js_contacts = [list(contact) for contact in contacts]

    
    if user_id:
        return render_template("Welcome.html", user_id=user_id, username=username, contacts=contacts, js_contacts=js_contacts, upcomingbirthdays=upcomingbirthdays, todaybirthdays=todaybirthdays)
    return render_template("Welcome.html")

@app.route("/Contacts")
def Contacts():
    user_id = session.get('user_id')
    contacts = get_contacts(user_id)
    
    return render_template("Contacts.html", user_id=user_id, contacts=contacts)



    

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