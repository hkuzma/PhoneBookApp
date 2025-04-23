import pwinput
import csv
import sqlite3

con = sqlite3.connect("PhoneBook.db")
cur = con.cursor()

def create_new_table(table_name, create_string):
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(create_string)
    
def insert_records_to_table(file, insert_string):
    infile = open(file)
    table = csv.reader(infile)
    header = next(table) ##junk header
    cur.executemany(insert_string, table)
    
def print_table(table_name):
    string = f'''SELECT * FROM {table_name}'''
    rows = cur.execute(string).fetchall()
    print(f"{table_name.upper()}:")
    for tup in rows:
        print(tup)
    
create_table = '''CREATE TABLE Users('user_id','email','username','password','account_created','first_name','last_name')'''
create_new_table("Users", create_table)


#Relationship_context == how you met/know them/etc...
create_table = '''CREATE TABLE Contact_Info('contact_id','user_id','first_name','last_name','email','phone','relationship_context','residence', 'company', 'birthday', 'added_date', FOREIGN KEY(user_id) REFERENCES users(user_id))'''
create_new_table("Contact_Info", create_table)

create_table = '''CREATE TABLE Posts('user_id','contact_id','post_id','date_posted','post_text', FOREIGN KEY(contact_id) REFERENCES Contact_Info(contact_id), FOREIGN KEY (user_id) REFERENCES Users(user_id))'''
create_new_table("Posts", create_table)

create_table = '''CREATE TABLE Tags('contact_id','tag_id','tag', FOREIGN KEY(contact_id) REFERENCES Contact_Info(contact_id))'''
create_new_table("Tags",create_table)

insert_records = '''INSERT INTO Users('user_id','email','username','password','account_created','first_name','last_name') VALUES('1','henrykuzma42@gmail.com','hkuzma','1234','4/23/25','Henry','Kuzma')'''
cur.execute(insert_records)

print_table("Users")




con.commit()
con.close()


