import pwinput
import csv
import sqlite3

con = sqlite3.connect("SocialMedia.db")
cur = con.cursor()

def create_new_table(table_name, create_string):
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(create_string)
    
    
create_table = '''CREATE TABLE users('user_id','email','username','password','account_created','first_name','last_name')'''
create_new_table("Users", create_table)


#Relationship_context == how you met/know them/etc...
create_table = '''CREATE TABLE Contact Info('contact_id','user_id','first_name','last_name','email','phone','relationship_context','residence', 'company', 'birthday', 'added_date' FOREIGN KEY(user_id) REFERENCES users(user_id))'''
create_new_table("Contact Info", create_table)

create_table = '''CREATE TABLE posts('user_id','contact_id','post_id','date_posted','post_text' FOREIGN KEY(contact_id) REFERENCES Contact Info(contact_id) FOREIGN KEY (user_id) REFERENCES Users(user_id))'''
create_new_table("Posts", create_table)

create_table = '''CREATE TABLE Tags('contact_id,'tag_id','tag' FOREIGN KEY(contact_id) REFERENCES Contact Info(contact_id))'''
create_new_table("Tags",create_table)

con.commit()
con.close()


