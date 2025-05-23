from flask import Flask, render_template, url_for, request, redirect, jsonify, session, send_file
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import random
from datetime import datetime, timedelta
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from io import BytesIO

# gets specific column from user    
def get_info_item(USER, item):
    con = sqlite3.connect('PhoneBook.db')
    cur = con.cursor()
    info_item = cur.execute(f"SELECT {item} FROM Users WHERE user_id = {USER}").fetchall()
    con.close()
    return info_item[0][0]

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
        contactmonth = int(contact[8].split('/')[0])
        contactday = int(contact[8].split('/')[1])
        contactyear = int(contact[8].split('/')[2])
        
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

def get_posts(user, contact):
    con = sqlite3.connect('Phonebook.db')
    cur = con.cursor()
    posts = cur.execute(f"SELECT * FROM Posts WHERE user_id == {user} AND contact_id == {contact} ").fetchall()
    
    return posts

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
            
def get_contacts_by_score(user_id):
    con = sqlite3.connect('PhoneBook.db')
    cur = con.cursor()
    # Ensure contacts are ordered by friendship_score in descending order
    contacts = cur.execute(f"SELECT * FROM Contact_Info WHERE user_id = ? ORDER BY friendship_score DESC", (user_id,)).fetchall()
    con.close()
    return contacts            


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


@app.route('/ContactPosts/<int:contact_id>')
def view_contact_posts(contact_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('PhoneBook.db')
    c = conn.cursor()

    # Get contact's name
    c.execute("SELECT first_name, last_name FROM Contact_Info WHERE contact_id = ?", (contact_id,))
    contact = c.fetchone()
    if not contact:
        conn.close()
        return "Contact not found", 404
    contact_name = f"{contact[0]} {contact[1]}"

    # Get posts associated with this contact
    c.execute('''SELECT post_text, date_posted 
                 FROM Posts 
                 WHERE contact_id = ? 
                 ORDER BY date_posted DESC''', (contact_id,))
    posts = c.fetchall()

    conn.close()

    return render_template('Posts.html', contact_name=contact_name, posts=posts, contact_id=contact_id)


    
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
    if user_id:
        contacts = get_contacts_by_score(user_id)  # Fetch contacts sorted by friendship_score
        birthday_info = get_birthdays(contacts)
        upcomingbirthdays = birthday_info[0]
        todaybirthdays = birthday_info[1]
        
        # Prepare data for JS chart
        js_contacts = [list(contact) for contact in contacts]

        return render_template("Welcome.html", 
                               user_id=user_id, 
                               username=get_info_item(user_id, 'first_name'),
                               contacts=contacts, 
                               js_contacts=js_contacts, 
                               upcomingbirthdays=upcomingbirthdays, 
                               todaybirthdays=todaybirthdays)
    return render_template("Welcome.html")

@app.route("/Contacts")
def Contacts():
    user_id = session.get('user_id')
    contacts = get_contacts(user_id)
    
    return render_template("Contacts.html", user_id=user_id, contacts=contacts)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    # Extract form data
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form.get('email', None)
    phone = request.form['phone']
    relationship_context = request.form['relationship_context']
    residence = request.form.get('residence', None)
    company = request.form.get('company', None)
    birthday = request.form.get('birthday', None)
    friendship_score = request.form.get('friendship_score', None)
    
    
    if birthday == "":
        birthday == 00-00-0000
    
    # Get today's date in m/d/y format
    added_date = datetime.datetime.now()
    
    yearhold = str(added_date).split('-')[0]
    print(yearhold)
    year = yearhold[2]
    year += yearhold[3]
    year = year
    month = str(added_date).split('-')[1]
    day = str(added_date).split('-')[2].split(' ')[0]
    
    date = month
    date += "/"
    date+=day
    date+= year
    
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

    # User ID from session (assuming a logged-in user)
    user_id = session.get('user_id')

    # Insert into database
    con = sqlite3.connect('PhoneBook.db')
    cursor = con.cursor()

    cursor.execute('''
        INSERT INTO Contact_Info (
            user_id, first_name, last_name, email, phone, relationship_context,
            residence, company, birthday, added_date, friendship_score
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id, first_name, last_name, email, phone, relationship_context,
        residence, company, birthday, date, friendship_score
    ))

    con.commit()
    con.close()

    # Redirect back to the welcome page after adding the contact
    return redirect(url_for('Welcome'))

@app.route('/add_post/<int:contact_id>', methods=['POST'])
def add_post(contact_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if the user is not logged in

    # Retrieve the content of the new post from the form
    content = request.form['content'].strip()
    if not content:
        return "Post content cannot be empty.", 400  # Handle empty posts

    # Get the current date and format it as MM/DD/YY
    added_date = datetime.datetime.now()
    year = str(added_date.year)[2:]  # Last two digits of the year
    month = str(added_date.month).zfill(2)  # Ensure two digits for month
    day = str(added_date.day).zfill(2)  # Ensure two digits for day
    date = f"{month}/{day}/{year}"

    # Get the current user's ID from the session
    user_id = session['user_id']

    # Insert the new post into the database
    try:
        conn = sqlite3.connect('PhoneBook.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO Posts (contact_id, user_id, post_text, date_posted)
            VALUES (?, ?, ?, ?)
        ''', (contact_id, user_id, content, date))
        conn.commit()
        conn.close()
    except Exception as e:
        return f"Error while adding post: {e}", 500  # Handle any database errors

    # After adding the post, redirect to the contact's posts page
    return redirect(url_for('view_contact_posts', contact_id=contact_id))

    # post = request.form['post']
    # con = sqlite3.connect('PhoneBook.db')
    # cursor = con.cursor()
    # cursor.execute('''
    #     INSERT INTO Posts (
    #         user_id, contact_id, date_posted, post_text, 
    #     ) VALUES (?, ?, ?, ?)
    # ''', (
    #     user_id, contact_id, date, post))
    # con.commit()
    # con.close()
    
    contacts = get_contacts(user_id)
    print(contacts)
    print(contact_id)
    contact = contacts[contact_id]
    username = get_info_item(user_id, 'first_name')
    
    posts = get_posts(user_id, contact_id)
    
        
    js_contacts = [list(contact) for contact in contacts]
    print(app.url_map)
    
    print("REDIRECTING!!!")

    return redirect(url_for('Welcome'))


    

@app.route('/Remove/<int:contact_id>', methods=['POST'])
def remove_contact(contact_id):
    if 'user_id' not in session:
        return redirect('/')
    
    user_id = session['user_id']
    con = sqlite3.connect('PhoneBook.db')
    cur = con.cursor()

    # Only delete if this contact belongs to the current user
    cur.execute("DELETE FROM Contact_Info WHERE contact_id = ? AND user_id = ?", (contact_id, user_id))
    con.commit()
    con.close()

    return redirect('/Welcome') 

@app.route('/chart')
def chart():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('landing'))

    # Use non-GUI backend
    import matplotlib
    matplotlib.use('Agg')

    # Connect and load friendship scores for user's contacts
    con = sqlite3.connect('PhoneBook.db')
    query = """
        SELECT first_name || ' ' || last_name AS name, friendship_score
        FROM Contact_Info
        WHERE user_id = ?
    """
    contacts_df = pd.read_sql_query(query, con, params=(user_id,))
    con.close()

    # Clean and sort
    contacts_df['friendship_score'] = pd.to_numeric(contacts_df['friendship_score'], errors='coerce')
    contacts_df = contacts_df.dropna().sort_values(by='friendship_score', ascending=False)

    # Create chart
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.barplot(x='friendship_score', y='name', data=contacts_df, palette='coolwarm')
    plt.title('Your Contacts Ranked by Friendship Score')
    plt.xlabel('Friendship Score')
    plt.ylabel('Contact Name')
    plt.tight_layout()

    # Save chart to BytesIO and return as response
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype='image/png')

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