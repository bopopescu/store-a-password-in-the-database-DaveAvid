import hashlib
import pymysql
import uuid
from click._compat import raw_input

connection = pymysql.connect(host='mrbartucz.com',
                             user='rv7388ow',
                             password='S3qu3nc3112358',
                             db='rv7388ow_Local_416',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


def getChoice():
    print("\nMenu\n(C)reate Account\n(L)ogin\n(Q)uit")
    choice = raw_input(">>> ").lower().rstrip()
    return choice


def create():
    try:
        with connection.cursor() as cursor:
            print("Choose a user name: ")
            userName = input()
            print("Choose a password: ")
            password = input().encode("utf-8")
            salt = uuid.uuid4().hex.encode('utf-8')
            hashed_password = hashlib.sha512(password + salt).hexdigest()

            # Select from Students Table the name set as input
            sql = "INSERT INTO Member_Login (User_Name, salt, hash) VALUES (%s,%s,%s)"
            to_sql = (userName, salt, hashed_password)
            cursor.execute(sql, to_sql)
    finally:
        connection.commit()


def login():
    try:
        with connection.cursor() as cursor:
            userName_login = input("Please enter user name to login: ")
            password_login = input("Enter your password to login: ").encode('utf-8')

            sql = "SELECT * FROM Member_Login WHERE User_Name = %s"
            to_sql = userName_login
            cursor.execute(sql, to_sql)

        for result in cursor:
            savedSalt = result.get('salt').encode('utf-8')
            savedHash = result.get('hash')
        connection.commit()

        check_hashed_password = hashlib.sha512(password_login + savedSalt).hexdigest()
        connection.commit()
        if savedHash == check_hashed_password:
            print("Password accepted, please log out when done")
        else:
            print("Incorrect Password, please try again.")
    finally:
        connection.commit()


choice = getChoice()

while True:
    if choice == "c":
        create()
    elif choice == "l":
        login()
    elif choice == "q":
        break
    else:
        print("Invalid choice, please choose again")
        print("\n")
    choice = getChoice()

print("Thank you for registering")
