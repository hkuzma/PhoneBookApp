import pwinput
import csv
import sqlite3
import pandas as pd

# Connect to SQLite database
con = sqlite3.connect("PhoneBook.db")
cur = con.cursor()

# Create a table, replacing it if it already exists
def create_new_table(table_name, create_string):
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(create_string)

# Insert data from a CSV file into a table    
def insert_records_to_table(file, insert_string):
    infile = open(file)
    table = csv.reader(infile)
    header = next(table) ##junk header
    cur.executemany(insert_string, table)
    
# Print contents of a table    
def print_table(table_name):
    string = f'''SELECT * FROM {table_name}'''
    rows = cur.execute(string).fetchall()
    print(f"{table_name.upper()}:")
    for tup in rows:
        print(tup)
    
# Create Users table
create_table = '''
CREATE TABLE Users (
    'user_id',
    'email',
    'username',
    'password',
    'account_created',
    'first_name',
    'last_name',
    PRIMARY KEY(user_id)
)'''
create_new_table("Users", create_table)

# Load contacts from CSV using pandas
df_contacts = pd.read_csv("Users.csv")

# Insert into the Contact_Info table
df_contacts.to_sql("Users", con, if_exists='append', index=False)

# Create Contact_Info table
create_table = '''
CREATE TABLE Contact_Info (
    'contact_id',
    'user_id',
    'first_name',
    'last_name',
    'email',
    'phone',
    'residence',
    'company',
    'birthday',
    'added_date',
    'friendship_score',
    'relationship_context',
    FOREIGN KEY(user_id) REFERENCES users(user_id)
)'''
create_new_table("Contact_Info", create_table)

# Load contacts from CSV using pandas
df_contacts = pd.read_csv("Contacts.csv")

# Insert into the Contact_Info table
df_contacts.to_sql("Contact_Info", con, if_exists='append', index=False)

# Create Posts table
create_table = '''  
CREATE TABLE Posts (
    'user_id',
    'contact_id',
    'post_id',
    'date_posted',
    'post_text',
    FOREIGN KEY(contact_id) REFERENCES Contact_Info(contact_id),
    FOREIGN KEY(user_id) REFERENCES Users(user_id)
)'''
create_new_table("Posts", create_table)

# Load contacts from CSV using pandas
df_contacts = pd.read_csv("Posts.csv")

# Insert into the Contact_Info table
df_contacts.to_sql("Posts", con, if_exists='append', index=False)


# Create Tags table
create_table = '''
CREATE TABLE Tags (
    'contact_id',
    'user_id',
    'tag_id',
    'tag',
    FOREIGN KEY(contact_id) REFERENCES Contact_Info(contact_id)
    FOREIGN KEY(user_id) REFERENCES Users(user_id)
)'''
create_new_table("Tags", create_table)

# Load contacts from CSV using pandas
df_contacts = pd.read_csv("Tags.csv")

# Insert into the Contact_Info table
df_contacts.to_sql("Tags", con, if_exists='append', index=False)

# Insert a testing user record
insert_records = '''
INSERT INTO Users (
    'user_id',
    'email',
    'username',
    'password',
    'account_created',
    'first_name',
    'last_name'
) VALUES (
    11,
    'henrykuzma42@gmail.com',
    'hkuzma',
    '1234',
    '4/23/2025',
    'Henry',
    'Kuzma'
)'''
cur.execute(insert_records)

# Display contents of Users table
#print_table("Users")
#print_table("Contact_Info")
#print_table("Posts")
print_table("Tags")

con.commit()
con.close()