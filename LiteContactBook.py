import sqlite3
import pwinput

# Connect to the contact book database
def connect_db():
    return sqlite3.connect('PhoneBook.db')

# Authenticate user
def authenticate_user():
    conn = connect_db()
    cursor = conn.cursor()

    print("Welcome to Contact Book App")

    while True:
        username = input("Username: ")
        password = pwinput.pwinput("Password: ")

        cursor.execute("SELECT password FROM Users WHERE username = ?", (username,))
        result = cursor.fetchone()

        if result is None:
            print("User not found.\n")
            continue

        if password == result[0]:
            print("Login successful!\n")
            conn.close()
            return username
        else:
            print("Incorrect password.\n")

# Get full user record
def get_user_info(username):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# Display and optionally edit user info
def display_user_info(user):
    print(f"Username: {user[2]}")
    print(f"Account Created: {user[4]}")
    print(f"First Name: {user[5]}")
    print(f"Last Name: {user[6]}")
    print("\na) Go Back\nb) Edit")
    return input("=> ")

def edit_user_info(user_id):
    columns = ["email", "password", "first_name", "last_name"]
    print("Editable Fields:", ", ".join(columns))
    column = input("Which field do you want to update? ")

    if column not in columns:
        print("Invalid column.")
        return 'b'

    new_value = input(f"Enter new value for {column}: ")

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(f"UPDATE Users SET {column} = ? WHERE user_id = ?", (new_value, user_id))
        conn.commit()
        print("Updated successfully!")
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()

    return input("a) Go Back\nb) Edit\n=> ")

# View contacts
def view_contacts(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Contact_Info WHERE user_id = ?", (user_id,))
    contacts = cursor.fetchall()
    conn.close()

    print("Your Contacts:")
    for contact in contacts:
        print(f"{contact[2]} {contact[3]} - {contact[5]} - {contact[6]}")

    print("\na) Go Back\nb) View Posts for Contact")
    return input("=> ")

# Add and view notes (posts) for a contact
def view_posts(user_id):
    contact_id = input("Enter contact ID: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT date_posted, post_text FROM Posts WHERE user_id = ? AND contact_id = ?", (user_id, contact_id))
    posts = cursor.fetchall()
    conn.close()

    print("Posts:")
    for post in posts:
        print(f"{post[0]}: {post[1]}")

    print("\na) Go Back\nb) Add Post")
    return input("=> "), contact_id

def add_post(user_id, contact_id):
    new_post = input("Write your note about the contact: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Posts (user_id, contact_id, post_id, date_posted, post_text) VALUES (?, ?, NULL, date('now'), ?)",
                   (user_id, contact_id, new_post))
    conn.commit()
    conn.close()
    print("Note added!")
    return input("a) Go Back\nb) Add Another\n=> ")

# Exit app
def logout():
    print("Logging out...")
    exit()

# Main menu
def main():
    username = authenticate_user()
    user = get_user_info(username)

    while True:
        print("\na) User Info")
        print("b) View Contacts")
        print("c) Log Out")
        choice = input("=> ")

        if choice == 'a':
            option = display_user_info(user)
            while option == 'b':
                option = edit_user_info(user[0])
                if option == 'a':
                    user = get_user_info(username)
                    break
        elif choice == 'b':
            contact_option = view_contacts(user[0])
            if contact_option == 'b':
                post_choice, contact_id = view_posts(user[0])
                while post_choice == 'b':
                    post_choice = add_post(user[0], contact_id)
        elif choice == 'c':
            logout()
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()