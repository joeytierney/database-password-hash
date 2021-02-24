# database sign up and login system
# 21/01/2021
# joey tierney

import uuid, hashlib, mysql.connector, os, re, winsound, getpass, time

con = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="root",
    database="user_database"
)

cur = con.cursor()

def registerUser():
    isValid = False
    print("\n *** REGISTER ***\n")
    while isValid == False:
        username = input(" Enter a username: ")
        password = getpass.getpass(" Enter a password: ")   #getpass is used to hide the text from the command line
        email = input(" Enter an e-mail address: ")
        while not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email): # verify email address is valid
            print("\n *** Sorry, that was an invalid email, try again! ***")
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            time.sleep(1)
            email = input("\n Enter an e-mail address: ")
        if username and password and email:
            isValid = True
    
    return username, password, email

def loginUser():
    isValid = False
    loggedIn = False
    print("\n *** LOGIN ***\n")
    
    while isValid == False:
        username = input(" Enter your username: ")
        password = getpass.getpass(" Enter your password: ")

        sql = f"""SELECT password FROM users WHERE username='{username}'"""
        cur.execute(sql)
        storedPassword = cur.fetchone()[0]
        
        while loggedIn == False:
            sql = f"""SELECT password FROM users WHERE username='{username}'"""
            cur.execute(sql)
            items = cur.fetchone()
            if items:
                dbPassword = items[0]
                match = verifyhash(password, dbPassword)
                if match:
                    isValid = True
                    loggedIn = True
                    print(f"\n *** Welcome {username}! ***\n")
                    time.sleep(1)
                else:
                    print("\n *** Sorry, I didn't recognise that username or password! ***\n")
                    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                    time.sleep(1)
                    username = input(" Enter your username: ")
                    password = getpass.getpass(" Enter your password: ")
                    
    sql = f"""SELECT username, email FROM users WHERE username='{username}'"""
    cur.execute(sql)
    items = cur.fetchall()
    print("\n *** USERNAME AND EMAIL ***\n",items,"\n")

# this function is to just make sure the user is logged in so they can't freely edit anyone's details
def updateDetails():
    isValid = False
    loggedIn = False
    print("\n *** UPDATING DETAILS ***\n")
    
    while isValid == False:
        username = input(" Enter your username: ")
        password = getpass.getpass(" Enter your password: ")
        email = input(" Enter your email address: ")
        while not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            print("\n *** Sorry, that was an invalid email, try again! ***")
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            time.sleep(1)
            email = input("\n Enter your e-mail address: ")

        sql = f"""SELECT password FROM users WHERE username='{username}'"""
        cur.execute(sql)
        storedPassword = cur.fetchone()[0]
        
        while loggedIn == False:
            sql = f"""SELECT password FROM users WHERE username='{username}'"""
            cur.execute(sql)
            items = cur.fetchone()
            if items:
                dbPassword = items[0]
                match = verifyhash(password, dbPassword)
                if match:
                    isValid = True
                    loggedIn = True
                    print(f"\n *** Upadting {username}! ***\n")
                    time.sleep(1)
                else:
                    print("\n *** Sorry, I didn't recognise that username or password! ***\n")
                    winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
                    time.sleep(1)
                    username = input(" Enter your username: ")
                    password = getpass.getpass(" Enter your password: ")
                    
    sql = f"""SELECT username, email FROM users WHERE username='{username}'"""
    cur.execute(sql)
    items = cur.fetchall()
    print("\n *** USERNAME AND EMAIL ***\n",items,"\n")

    return username, password, email

def addUser(username, hashedPassword, email):
    try:
        sql = f"""INSERT INTO `users` VALUES ('{username}', '{hashedPassword}', '{email}')"""
        cur.execute(sql)
        con.commit()
        print(f"\n *** Registration successful! Welcome to the database '{username}'! :) ***\n")
    except:
        print("\n *** Woah there! This username already exists! Try another one! ***\n")
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)

def updateUser(username, hashedPassword, email):
    # updating password doesn't currently work, will always use the first password registered for that user
    isValid = False
    while isValid == False:
        newUsername = input(" Enter new username: ")
        password = getpass.getpass(" Enter new password: ")
        newEmail = input(" Enter new e-mail address: ")
        while not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            print("\n *** Sorry, that was an invalid email, try again! ***")
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            time.sleep(1)
            email = input("\n Enter new e-mail address: ")
        if newUsername and password and newEmail:
            isValid = True
    try:
        sql = f"""INSERT INTO `users` VALUES ('{newUsername}', '{hashedPassword}', '{newEmail}')"""
        cur.execute(sql)
        con.commit()
        print(f"\n *** Update successful! ***\n")
        sql = f"""DELETE FROM users WHERE username = '{username}'"""
        cur.execute(sql)
        con.commit()
    except:
        print("\n *** Woah there! This username already exists! Try another one! ***\n")
        winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)

    return username, password, email

def hashPassword(password):
    salt = uuid.uuid4().hex
    hashedPassword = hashlib.sha256(salt.encode()+password.encode()).hexdigest()+":"+salt

    return hashedPassword

def verifyhash(userpass, storedpass):
    try:
        password,salt=storedpass.split(":")
    except:
        pass
    else:
        data = []
        data.append(password)
        data.append(hashlib.sha256(salt.encode()+userpass.encode()).hexdigest())
    
    return data[0]==data[1]

def main():
    choiceValid = False
    
    while choiceValid == False:
        print(" ***** DATABASE MENU *****\n 1. Register User\n 2. Login\n 3. Update Details\n 4. Exit")
        choice = input(" Enter option: ")
        if choice == "1":
            username, password, email = registerUser()
            hashedUserPass = hashPassword(password)
            addUser(username, hashedUserPass, email)
        elif choice == "2":
            loginUser()
        elif choice == "3":
            username, password, email = updateDetails()
            hashedUserPass = hashPassword(password)
            updateUser(username, hashedUserPass, email)
        elif choice == "4":
            print("\n *** CLOSING THE PROGRAM ***")
            winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
            time.sleep(1)
            exit()
        else:
            print("\n Please enter 1-4 only!\n")
            winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
print()
main()