#importing modules needed
import mysql.connector as connector
import datetime
import tabulate

#setting up database connections
connection=connector.connect(host='localhost',user='root',password='1234',database='library_management')
cursor_obj=connection.cursor()

#creating tables, if not already present
cursor_obj.execute("CREATE TABLE IF NOT EXISTS accounts(Admission_No varchar(255) PRIMARY KEY NOT NULL,Name varchar(255) NOT NULL,Password varchar(255) NOT NULL)")
cursor_obj.execute("CREATE TABLE IF NOT EXISTS books(Title varchar(255) PRIMARY KEY NOT NULL,Author varchar(255) NOT NULL,Year varchar(4),Genre varchar(255),Available_Or_Not varchar(1) DEFAULT 'Y')")
cursor_obj.execute("CREATE TABLE IF NOT EXISTS borrowed_books(Title varchar(255) PRIMARY KEY NOT NULL,Borrower_ID varchar(255),Date_of_Borrowing datetime NOT NULL,Deadline datetime NOT NULL)")
connection.commit()

##functions to be used in the program code

#to determine whether it's the librarian or a student using system, and the features they can use
def succesful_login(admin_or_student):
    if admin_or_student=='0000':
        while True:
            print('\nx---------------------------------------x')
            print('1. Add Books')
            print('2. Browse books')
            print('3. Lend Books')
            print('4. Return Books')
            print('5. View students with unreturned books')
            print('6. Exit')
            print('x---------------------------------------x\n')
            admin_use=int(input("Enter operation -→ "))
            if admin_use==1:
                add_book()         
            elif admin_use==3:
                lend_book()
            elif admin_use==4:
                return_book()
            elif admin_use==5:
                currently_borrowed_books()
            elif admin_use==6:
                break
            elif admin_use==2:
                browse()
            else:
                print('\nX--Please enter a valid input--X\n')
    else:
        while True:
            print('\nx-----------------------------x')
            print('1. Browse books')
            print('2. Check availability of books')
            print('3. View borrowed books')
            print('4. Exit')
            print('x-----------------------------x\n')
            student_use=int(input('Enter operation -→ '))
            if student_use==1:
                browse()
            elif student_use==2:
                filter('Availability')
                Availabnull=input('\nPress any key to continue -→ ')
            elif student_use==3:
                cursor_obj.execute('SELECT * FROM borrowed_books')
                borrowed_book_details=cursor_obj.fetchall()
                book_borrowed=False
                for i in borrowed_book_details:
                    if i[1]==admission_no:
                        book_borrowed=True
                        print('\nx--------------------------------------------x')
                        print('Borrowed book           :',i[0])
                        print('Borrowed on             :',i[2])
                        print('Deadline for return     :',i[3])
                        print('x--------------------------------------------x')
                if book_borrowed==False:
                    print('\nYou currently have no borrowed books.')
                    Availabnull=input('\nPress any key to continue -→ ')
            elif student_use==4:
                break
            else:
                print('\nX--Please enter a valid input--X\n')

#to filter the books according to the user
def filter(filter_input):
    if filter_input != 'Availability':
        filter_value=input('Search -→ ').upper()
    cursor_obj.execute('SELECT * FROM books')
    book_details=cursor_obj.fetchall()
    filtered_values=[]
    for i in book_details:
        if filter_input=='Title':
            if filter_value==i[0]:
                filtered_values.append(i)
        elif filter_input=='Author':
            if filter_value==i[1]:
                filtered_values.append(i)
        elif filter_input=='Year':
            if filter_value==i[2]:
                filtered_values.append(i)
        elif filter_input=='Genre':
            if filter_value==i[3]:
                filtered_values.append(i)
        elif filter_input=='Availability':
            if i[4]=='Y':
                filtered_values.append(i)
    print('\nx-------------------------------------------------------x')                
    print(tabulate.tabulate(filtered_values,headers=['Title','Author','Year','Genre','Availability']))
    print('x-------------------------------------------------------x')

#to browse books available in the library
def browse():
    cursor_obj.execute('SELECT * FROM books')
    book_details=cursor_obj.fetchall()
    print('\nx-----------------------------------------------------x')
    print(tabulate.tabulate(book_details,headers=['Title','Author','Year','Genre','Availability']))
    print('x-----------------------------------------------------x')
    filter_or_no=input('Would you like to filter the results? (Y/N) -→ ')
    if filter_or_no.upper()=='Y':
        print('\nFilter by ;')
        print(' 1. Title')
        print(' 2. Author')
        print(' 3. Year of publishing')
        print(' 4. Genre')
        print(' 5. Availability')
        filter_value=int(input('-→ '))
        if filter_value==1:
            filter('Title')
        elif filter_value==2:
            filter('Author')
        elif filter_value==3:
            filter('Year')
        elif filter_value==4:
            filter('Genre')
        elif filter_value==5:
            filter('Availability')
        else:
            print('\nX--Please enter a valid input--X\n')
    elif filter_or_no.upper()=='N':
        pass
    else:
        print('\nX--Please enter a valid input--X\n')

#to add a new book into the library database by the librarian
def add_book():
    book_name=input("Enter book name : ")
    book_author=input("Enter author's name : ")
    book_year=input("Enter year of publication : ")
    book_genre=input("Enter genre : ")
    a="'"+book_name.upper()+"'"
    b="'"+book_author.upper()+"'"
    c="'"+book_year+"'"
    d="'"+book_genre.upper()+"'"
    cursor_obj.execute("INSERT INTO books VALUES({},{},{},{},{e})".format(a,b,c,d,e="'Y'"))
    connection.commit()
    Availabnull=input('\nPress any key to continue -→ ')

#to lend a book to a student 
def lend_book():
    borrowing_book_name=input("Which book is being borrowed? : ").upper()
    cursor_obj.execute('SELECT * FROM books')
    book_details=cursor_obj.fetchall()
    book_exists=False
    for i in book_details:
        if borrowing_book_name in i:
            book_exists=True
            book_available=i[4]
    if book_exists==True:
        if book_available=='Y':
            borrower_id=input("Who is borrowing the book? (admission id): ").upper()
            cursor_obj.execute("SELECT Admission_No from accounts")
            admission_ids=cursor_obj.fetchall()
            account_exists=False
            for i in admission_ids:
                if borrower_id in i:
                    account_exists=True
            if account_exists==True:
                current_date=datetime.datetime.today()
                current_date_1=current_date.strftime('%Y-%m-%d %H:%M:%S')
                deadline=datetime.datetime.today() + datetime.timedelta(days=7)
                deadline_formatted=deadline.strftime('%Y-%m-%d %H:%M:%S')
                a="'"+borrowing_book_name+"'"
                b="'"+borrower_id+"'"
                c="'"+current_date_1+"'"
                d="'"+deadline_formatted+"'"
                cursor_obj.execute("INSERT INTO borrowed_books VALUES({},{},{},{})".format(a,b,c,d))
                connection.commit()
                cursor_obj.execute("UPDATE books SET Available_Or_Not='N' WHERE Title={}".format(a))
                connection.commit()
                print('\nOperation succesful!\n')
            else:
                print("\nStudent doesn't have an account\n")
        else:
            print("\n"+borrowing_book_name,"is currently with someone else.\n")
    else:
        print("\n"+borrowing_book_name,"is not present in the library.\n")
    null=input('Press any key to continue -→ ')

#to return lended books back to the library
def return_book():
    returner_id=input('Enter admission no. of the student :').upper()
    returning_book=input('Enter name of book :').upper()
    cursor_obj.execute("SELECT * FROM borrowed_books")
    borrowed_details=cursor_obj.fetchall()
    for i in borrowed_details:
        if returning_book in i:
            if i[1]==returner_id:
                today=datetime.datetime.today()
                deadline=i[3]
                if deadline>today:
                    print('\nStudent has returned the book before the deadline.\n')
                elif deadline<today:
                    difference=today-deadline
                    print('\nDeadline for book return was over',difference,'days ago\n')
                cursor_obj.execute("UPDATE books SET Available_Or_Not='Y' WHERE Title='{}'".format(returning_book))
                cursor_obj.execute("DELETE FROM borrowed_books WHERE Title='{}'".format(returning_book))
                connection.commit()
            else:
                print("The student has not borrowed the said book.")
        else:
            print('\n'+returning_book,'has not been borrowed by anyone.')
    Availabnull=input('Press any key to continue -→ ')

#to view currently borrowed books and whom they're with
def currently_borrowed_books():
    cursor_obj.execute("SELECT Admission_No,Name,Title,Date_Of_borrowing,Deadline FROM accounts,borrowed_books WHERE borrowed_books.Borrower_ID=accounts.Admission_No")
    borrowers_details=cursor_obj.fetchall()
    if len(borrowers_details)>0:
        print('\nx-----------------------------------------------------------------------------x')
        print(tabulate.tabulate(borrowers_details,headers=['Admission_No','Name','Title','Date_of_Borrowing','Deadline']))
        print('x-----------------------------------------------------------------------------x')
    else:
        print('\nThere are currently no borrowed books.')
    null=input('\nPress any key to continue -→ ')

#to log in a user into the system
def login():
    cursor_obj.execute('SELECT * FROM accounts')
    account_details=cursor_obj.fetchall()
    print('x---------------------------------------x')
    global admission_no
    admission_no=input('Enter your admission number : ').upper()
    input_password=input('Enter your password : ')
    print('x---------------------------------------x')
    account_present=False
    for i in account_details:
        if admission_no in i:
            password=i[2]
            account_present=True
    if account_present==True:
        if input_password==password:
            succesful_login(admission_no)
        else:
            print('\nWrong password entered.')
            Availabnull=input('\nPress any key to continue -→ ')
    else:
        print("\nAccount doesn't exist. Please sign up.\n")
        Availabnull=input('\nPress any key to continue -→ ')

##program code

print('''
                                             _ _ _ ____ _    ____ ____ _  _ ____    ___ ____  
                                             | | | |___ |    |    |  | |\/| |___     |  |  | .
                                             |_|_| |___ |___ |___ |__| |  | |___     |  |__| .
                                                                                                
                         ░█░░░▀█▀░█▀▄░█▀▄░█▀█░█▀▄░█░█░░░█▄█░█▀█░█▀█░█▀█░█▀▀░█▀▀░█▄█░█▀▀░█▀█░▀█▀░░░█▀▀░█░█░█▀▀░▀█▀░█▀▀░█▄█
                         ░█░░░░█░░█▀▄░█▀▄░█▀█░█▀▄░░█░░░░█░█░█▀█░█░█░█▀█░█░█░█▀▀░█░█░█▀▀░█░█░░█░░░░▀▀█░░█░░▀▀█░░█░░█▀▀░█░█
                         ░▀▀▀░▀▀▀░▀▀░░▀░▀░▀░▀░▀░▀░░▀░░░░▀░▀░▀░▀░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀░▀▀▀░▀░▀░░▀░░░░▀▀▀░░▀░░▀▀▀░░▀░░▀▀▀░▀░▀
''')

#login page
print('\nDo you want to login or sign up?\n\n1.Log in\n2.Sign up \n')
login_or_signup=input('Enter what you want to do :')

if login_or_signup=='1':
    login()
elif login_or_signup=='2':
    admission_no=input('Enter your admission number :').upper()
    name=input('Enter your name :').upper()
    password=input('Enter the password you want to use :')
    a="'"+admission_no+"'"
    b="'"+name+"'"
    c="'"+password+"'"
    cursor_obj.execute('INSERT INTO accounts VALUES({},{},{})'.format(a,b,c))
    connection.commit()
    exit_or_no=input('Would you like to login now? (Y/N) : ')
    print()
    if exit_or_no.upper()=='N':
        exit
    elif exit_or_no.upper()=='Y':
        login()
    else:
        print('\nX--Please enter a valid input--X\n')
else:
    print('\nX--Please enter a valid input--X\n')


connection.close()