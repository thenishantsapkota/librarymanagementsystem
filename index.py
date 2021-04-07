#CODE_REVISION(2020/11/2)
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import  *
import sys
import MySQLdb
import datetime
from datetime import datetime  
from datetime import timedelta 


from PyQt5.uic import loadUiType

ui,_ = loadUiType('library.ui')

class MainApp(QMainWindow , ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_UI_Changes()
        self.Handle_Buttons()
        self.Dark_Blue_Theme()

        self.Show_Category()
        self.Show_Authors()
        self.Show_Publishers()

        self.Show_Category_ComboBox()
        self.Show_Authors_ComboBox()
        self.Show_Publishers_ComboBox()
        self.Show_Books_ComboBox()
        self.Show_Students_ComboBox()
        self.Show_RollNo_ComboBox()

        self.Show_All_Students()
        self.Show_All_Books()
        self.Show_All_Borrows()
        self.Show_Returns()

    def Handle_UI_Changes(self):
        self.Hide_Themes()
        self.tabWidget.tabBar().setVisible(False)
    
    
    def Handle_Buttons(self):
        self.pushButton_5.clicked.connect(self.Show_Themes)
        self.pushButton_21.clicked.connect(self.Hide_Themes)
        self.pushButton.clicked.connect(self.Open_Todo)
        self.pushButton_2.clicked.connect(self.Open_Books_Tab)
        self.pushButton_3.clicked.connect(self.Open_Users_Tab)
        self.pushButton_4.clicked.connect(self.Open_Settings_Tab)
        self.pushButton_7.clicked.connect(self.Add_New_Books)
        self.pushButton_6.clicked.connect(self.Borrow_Books)
        self.pushButton_14.clicked.connect(self.Add_Category)
        self.pushButton_15.clicked.connect(self.Add_Author)
        self.pushButton_16.clicked.connect(self.Add_Publishers)
        self.pushButton_9.clicked.connect(self.Search_Books)
        self.pushButton_8.clicked.connect(self.Edit_Books)
        self.pushButton_10.clicked.connect(self.Delete_Books)
        self.pushButton_11.clicked.connect(self.Add_User)
        self.pushButton_12.clicked.connect(self.Login)
        self.pushButton_22.clicked.connect(self.Open_Book_List_Tab)
        self.pushButton_13.clicked.connect(self.Edit_User)
        self.pushButton_17.clicked.connect(self.Dark_Blue_Theme)
        self.pushButton_18.clicked.connect(self.Dark_Orange_Theme)
        self.pushButton_19.clicked.connect(self.QDark)
        self.pushButton_20.clicked.connect(self.QDarkGray)

        self.pushButton_24.clicked.connect(self.Add_New_Student)
        self.pushButton_26.clicked.connect(self.Search_Students)
        self.pushButton_25.clicked.connect(self.Edit_Student)
        self.pushButton_27.clicked.connect(self.Delete_Student)
        self.pushButton_23.clicked.connect(self.Open_Return)
        self.pushButton_44.clicked.connect(self.Return_Books)
        self.pushButton_28.clicked.connect(self.Delete_Returns)
        self.pushButton_29.clicked.connect(self.Enable_Delete)
        self.pushButton_30.clicked.connect(self.Disable_Delte)


    def Show_Themes(self):
        warning = QMessageBox.warning(self , 'Warning', "Changing the Theme may result in Extreme Changes to the program. Do you want to proceed?", QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes:
            self.groupBox_3.show()
        else:
            pass

    def Hide_Themes(self):
        self.groupBox_3.hide()
    
    
    ############################
    ######OPENING TABS################


    def Open_Todo(self):
        self.tabWidget.setCurrentIndex(0)
        
    
    def Open_Books_Tab(self):
        self.tabWidget.setCurrentIndex(1)
    
    def Open_Users_Tab(self):
        self.tabWidget.setCurrentIndex(2)
    
    def Open_Settings_Tab(self):
        self.tabWidget.setCurrentIndex(3)
    
    def Open_Book_List_Tab(self):
        self.tabWidget.setCurrentIndex(4)
    
    def Open_Return(self):
        self.tabWidget.setCurrentIndex(5)
   ############################
    ######BOOKS################
    def Show_All_Books(self):
        self.db = MySQLdb.connect(host ='localhost', user='root', password='toor' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT book_name , book_description , book_code , book_category, book_author , book_publisher , book_price FROM book''')
        data = self.cur.fetchall()
        #print(data)
        self.tableWidget_7.setRowCount(0)
        self.tableWidget_7.insertRow(0)

        for row ,form in enumerate(data):
            for column ,item in enumerate(form):
                self.tableWidget_7.setItem(row , column ,QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget_7.rowCount()
            self.tableWidget_7.insertRow(row_position)
        self.db.close()
   
    def Add_New_Books(self):
        self.db = MySQLdb.connect(host ='localhost', user='root', password='toor' , db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_3.text()
        book_description = self.textEdit.toPlainText()
        book_code = self.lineEdit_4.text()
        book_category = self.comboBox_4.currentText()
        book_author = self.comboBox_5.currentText()
        book_publisher = self.comboBox_3.currentText()
        book_price = self.lineEdit_5.text()
        
        self.cur.execute('''
            INSERT INTO book(book_name , book_description , book_code , book_category , book_author , book_publisher , book_price)
            VALUES (%s , %s , %s , %s , %s , %s , %s)
        ''',(book_title , book_description , book_code , book_category , book_author , book_publisher , book_price))
        self.db.commit()
        self.statusBar().showMessage('Book Added Sucessfully!')
        self.lineEdit_3.setText('')
        self.textEdit.setPlainText('')
        self.lineEdit_4.setText('')
        self.lineEdit_5.setText('')
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_5.setCurrentIndex(0)
        self.comboBox_3.setCurrentIndex(0)
        self.Show_All_Books()
        self.Show_Books_ComboBox()

    def Search_Books(self):
        self.db = MySQLdb.connect(host ='localhost', user='root', password='toor' , db='library')
        self.cur = self.db.cursor()

        book_code = self.lineEdit_7.text()
        
        
        sql = '''SELECT * FROM book WHERE book_code = %s'''
        self.cur.execute(sql,[(book_code)])

        data = self.cur.fetchone()
        self.lineEdit_9.setText(data[1])
        self.lineEdit_8.setText(data[3])
        self.comboBox_6.setCurrentText(data[4])
        self.comboBox_7.setCurrentText(data[5])
        self.comboBox_8.setCurrentText(data[6])
        self.lineEdit_6.setText(data[7])
        self.textEdit_2.setPlainText(data[2])
        
    
    def Edit_Books(self):
        self.db = MySQLdb.connect(host ='localhost', user='root', password='toor' , db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_9.text()
        book_description = self.textEdit_2.toPlainText()
        book_code = self.lineEdit_8.text()
        book_category = self.comboBox_6.currentText()
        book_author = self.comboBox_7.currentText()
        book_publisher = self.comboBox_8.currentText()
        book_price = self.lineEdit_6.text()

        search_book_title = self.lineEdit_7.text()

        self.cur.execute('''
            UPDATE book SET book_name=%s, book_description=%s, book_code=%s, book_category=%s, book_author=%s, book_publisher=%s, book_price=%s WHERE book_name=%s
        ''',(book_title , book_description , book_code , book_category , book_author , book_publisher , book_price, search_book_title))
        self.db.commit()
        self.statusBar().showMessage('Book Updated Sucessfully!')
        self.lineEdit_9.setText('')
        self.textEdit_2.setPlainText('')
        self.lineEdit_8.setText('')
        self.comboBox_6.setCurrentIndex(0)
        self.comboBox_7.setCurrentIndex(0)
        self.comboBox_8.setCurrentIndex(0)
        self.lineEdit_6.setText('')
        self.lineEdit_7.setText('')
        self.Show_All_Books()
        self.Show_Books_ComboBox()

    
    def Delete_Books(self):
        self.db = MySQLdb.connect(host ='localhost', user='root', password='toor' , db='library')
        self.cur = self.db.cursor()

        book_code = self.lineEdit_7.text()
        
        warning = QMessageBox.warning(self , 'Delete Book', "Are You Sure You warWant to Delete this book?", QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes :
            sql = '''DELETE FROM book WHERE book_code=%s'''
            self.cur.execute(sql, [(book_code)])
            self.db.commit()
            self.statusBar().showMessage('Book Deleted Sucessfully!')
            self.lineEdit_9.setText('')
            self.textEdit_2.setPlainText('')
            self.lineEdit_8.setText('')
            self.comboBox_6.setCurrentIndex(0)
            self.comboBox_7.setCurrentIndex(0)
            self.comboBox_8.setCurrentIndex(0)
            self.lineEdit_6.setText('')
            self.lineEdit_7.setText('')
            self.Show_All_Books()
            self.Show_Books_ComboBox()

    def Borrow_Books(self):
        self.db = MySQLdb.connect(host ='localhost', user='root', password='toor' , db='library')
        self.cur = self.db.cursor()

        book_name = self.comboBox_9.currentText()
        book_code = self.comboBox_14.currentText()
        student_name = self.comboBox_12.currentText()
        student_rollno = self.comboBox_13.currentText()
        days_borrowed_for = self.comboBox_2.currentIndex()
        return_date = (datetime.date(datetime.now())+timedelta(weeks=days_borrowed_for))
        
        self.cur.execute(''' 
                INSERT INTO borrow(book_name , book_code , student_name , student_rollno , return_date)
                VALUES (%s , %s , %s , %s , %s)
            ''',(book_name , book_code , student_name , student_rollno , return_date))
        self.db.commit()
        self.statusBar().showMessage('Book Borrowed Successfully!')
        self.comboBox_12.setCurrentIndex(0)
        self.comboBox_13.setCurrentIndex(0)
        self.comboBox_14.setCurrentIndex(0)
        self.comboBox_2.setCurrentIndex(0)
        self.Show_All_Borrows()
    
    def Show_All_Borrows(self):
        self.db = MySQLdb.connect(host ='localhost', user='root', password='toor' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT book_name , book_code , student_name , student_rollno , return_date FROM borrow''')
        data = self.cur.fetchall()
        #print(data)
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)

        for row ,form in enumerate(data):
            for column ,item in enumerate(form):
                self.tableWidget_2.setItem(row , column ,QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(row_position)

    def Return_Books(self):
        self.db = MySQLdb.connect(host = 'localhost' , user = 'root' , password = 'toor' , db='library')
        self.cur = self.db.cursor()

        book_name = self.comboBox_22.currentText()
        book_code = self.comboBox_15.currentText()
        student_name = self.comboBox_10.currentText()
        student_rollno = self.comboBox_11.currentText()
        returned_date = self.lineEdit_2.text()

        self.cur.execute(''' 
                INSERT INTO returned(book_name, book_code , student_name , student_rollno , returned_date)
                VALUES (%s , %s , %s , %s , %s)
            ''',(book_name , book_code , student_name , student_rollno , returned_date))
        self.db.commit()
        self.statusBar().showMessage('Book Returned Successfully!')
        self.comboBox_22.setCurrentIndex(0)
        self.comboBox_15.setCurrentIndex(0)
        self.comboBox_10.setCurrentIndex(0)
        self.comboBox_11.setCurrentIndex(0)
        self.lineEdit_2.setText('')
        self.Delete_Borrowed_When_Returned()
        self.Show_Returns()


    def Delete_Borrowed_When_Returned(self):
        self.db = MySQLdb.connect(host = 'localhost' , user = 'root' , password = 'toor' , db='library')
        self.cur = self.db.cursor()
        
        book_name = self.comboBox_22.currentText()
        book_code = self.comboBox_15.currentText()
        student_name = self.comboBox_10.currentText()
        student_rollno = self.comboBox_11.currentText()
        returned_date = self.lineEdit_2.text()

        sql = '''DELETE FROM borrow WHERE student_name=%s'''
        self.cur.execute(sql, [(student_name)])
        self.db.commit()
        self.Show_All_Borrows()
    
    def Show_Returns(self):
        self.db = MySQLdb.connect(host = 'localhost' , user = 'root' , password = 'toor' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT book_name , book_code , student_name , student_rollno , returned_date FROM returned''')
        data = self.cur.fetchall()
        #print(data)
        self.tableWidget_16.setRowCount(0)
        self.tableWidget_16.insertRow(0)

        for row ,form in enumerate(data):
            for column ,item in enumerate(form):
                self.tableWidget_16.setItem(row , column ,QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget_16.rowCount()
            self.tableWidget_16.insertRow(row_position)
    
    def Enable_Delete(self):
        self.comboBox_16.setEnabled(True)
    
    def Disable_Delte(self):
        self.comboBox_16.setEnabled(False)

    def Delete_Returns(self):
        self.db = MySQLdb.connect(host = 'localhost' , user = 'root' , password = 'toor' , db='library')
        self.cur = self.db.cursor()

        book_name = self.comboBox_22.currentText()
        book_code = self.comboBox_16.currentText()
        student_name = self.comboBox_10.currentText()
        student_rollno = self.comboBox_11.currentText()
        returned_date = self.lineEdit_2.text()

        warning = QMessageBox.warning(self , 'Delete Return Data', "Are You Sure You Want to Delete this return data?", QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes :
            sql = '''DELETE FROM returned WHERE book_code=%s'''
            self.cur.execute(sql, [(book_code)])
            self.db.commit()
            self.comboBox_22.setCurrentIndex(0)
            self.comboBox_15.setCurrentIndex(0)
            self.comboBox_10.setCurrentIndex(0)
            self.comboBox_11.setCurrentIndex(0)
            self.lineEdit_2.setText('')
            self.Show_Returns()


   ############################
    ######USERS################
    def Add_User(self):
        self.db = MySQLdb.connect(host ='localhost', user='root', password='toor' , db='library')
        self.cur = self.db.cursor()
        
        username = self.lineEdit_10.text()
        email = self.lineEdit_11.text()
        password = self.lineEdit_12.text()
        password2 = self.lineEdit_13.text()

        if password == password2:
            self.cur.execute(''' 
                INSERT INTO users(user_name, user_email, user_password)
                VALUES (%s , %s , %s)
            ''',(username , email , password))

            self.db.commit()
            self.statusBar().showMessage('User Added Sucessfully!')
            self.lineEdit_10.setText('')
            self.lineEdit_11.setText('')
            self.lineEdit_12.setText('')
            self.lineEdit_13.setText('')


        else:
            self.statusBar().showMessage("Passwords don't match!")
            self.lineEdit_12.setText('')
            self.lineEdit_13.setText('')
    
    def Login(self):
        self.db = MySQLdb.connect(host ='localhost', user='root', password='toor' , db='library')
        self.cur = self.db.cursor()
        
        username = self.lineEdit_15.text()
        password = self.lineEdit_14.text()

        sql = ''' SELECT * FROM users'''
        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row in data:
            if username == row[1] and password == row[3]:
                self.statusBar().showMessage('User Login Sucessful!')
                self.groupBox_4.setEnabled(True)

                self.lineEdit_17.setText(row[1])
                self.lineEdit_18.setText(row[2])
                self.lineEdit_16.setText(row[3])
            
            else:
                warning = QMessageBox.warning(self , 'Error', "Username or Password Error,Please Try Again!", QMessageBox.Ok)
                self.lineEdit_14.setText('')

    def Edit_User(self):
        username = self.lineEdit_17.text()
        email = self.lineEdit_18.text()
        password = self.lineEdit_16.text()
        password2 = self.lineEdit_19.text()
        original_name = self.lineEdit_15.text()

        if password == password2:
            self.db = MySQLdb.connect(host ='localhost', user='root', password='toor' , db='library')
            self.cur = self.db.cursor()
            self.cur.execute('''
                UPDATE users SET user_name = %s , user_email = %s , user_password = %s WHERE user_name = %s
            ''',(username , email , password , original_name))
            self.db.commit()
            self.statusBar().showMessage('User Information Updated Sucessfully!')
            self.lineEdit_17.setText('')
            self.lineEdit_18.setText('')
            self.lineEdit_16.setText('')
            self.lineEdit_19.setText('')
            self.lineEdit_15.setText('')
            self.lineEdit_14.setText('')
            self.groupBox_4.setEnabled(False)

        else:
            warning = QMessageBox.warning(self , 'Error', "Passwords Donot Match , Please Enter again!", QMessageBox.Ok)
            self.lineEdit_16.setText('')
            self.lineEdit_19.setText('')

    ############################
    ######SETTINGS################

    def Add_Category(self):
        self.db = MySQLdb.connect(host ='localhost', user='root', password='toor' , db='library')
        self.cur = self.db.cursor()

        category_name = self.lineEdit_23.text()

        self.cur.execute('''
            INSERT INTO category (category_name) VALUES (%s)
        ''',(category_name,))
        
        self.db.commit()
        self.statusBar().showMessage('New Category Added')
        self.lineEdit_23.setText('')
        self.Show_Category()
        self.Show_Category_ComboBox()
    
    def Show_Category(self):
        self.db = MySQLdb.connect(host ='localhost', user='root', password='toor' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT category_name FROM category ''')
        data = self.cur.fetchall()
        
        if data:
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_3.setItem(row , column , QTableWidgetItem(str(item)))
                    column += 1
                
                row_position = self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(row_position)
    
    def Add_Author(self):
        self.db = MySQLdb.connect(host ='localhost', user='root', password='toor' , db='library')
        self.cur = self.db.cursor()
        author_name = self.lineEdit_21.text()

        self.cur.execute('''
            INSERT INTO authors (author_name) VALUES (%s)
        ''',(author_name,))
        
        self.db.commit()
        self.lineEdit_21.setText('')
        self.statusBar().showMessage('New Author Added')
        self.Show_Authors()
        self.Show_Authors_ComboBox()

    def Show_Authors(self):
        self.db = MySQLdb.connect(host ='localhost', user='root', password='toor' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT author_name FROM authors ''')
        data = self.cur.fetchall()
        
        if data:
            self.tableWidget_4.setRowCount(0)
            self.tableWidget_4.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_4.setItem(row , column , QTableWidgetItem(str(item)))
                    column += 1
                
                row_position = self.tableWidget_4.rowCount()
                self.tableWidget_4.insertRow(row_position)

    def Add_Publishers(self):
        self.db = MySQLdb.connect(host ='localhost', user='root', password='toor' , db='library')
        self.cur = self.db.cursor()
        publisher_name = self.lineEdit_22.text()

        self.cur.execute('''
            INSERT INTO publisher (publisher_name) VALUES (%s)
        ''',(publisher_name,))
        
        self.db.commit()
        self.lineEdit_22.setText('')
        self.statusBar().showMessage('New Publisher Added')
        self.Show_Publishers()
        self.Show_Publishers_ComboBox()

    def Show_Publishers(self):
        self.db = MySQLdb.connect(host ='localhost', user='root', password='toor' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT publisher_name FROM publisher ''')
        data = self.cur.fetchall()
        
        if data:
            self.tableWidget_5.setRowCount(0)
            self.tableWidget_5.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_5.setItem(row , column , QTableWidgetItem(str(item)))
                    column += 1
                
                row_position = self.tableWidget_5.rowCount()
                self.tableWidget_5.insertRow(row_position)

    #############COMBO BOXES###############
    ######SETTINGS STUFF################
    def Show_Category_ComboBox(self):
        self.db = MySQLdb.connect(host ='localhost', user='root', password='toor' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT category_name FROM category''')
        data = self.cur.fetchall()
        self.comboBox_4.clear()
        for category in data:
            #print(category[0])
            self.comboBox_4.addItem(category[0])
            self.comboBox_6.addItem(category[0])
    
    def Show_Authors_ComboBox(self):
        self.db = MySQLdb.connect(host ='localhost', user='root', password='toor' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT author_name FROM authors''')
        data = self.cur.fetchall()
        self.comboBox_5.clear()
        for authors in data:
            #print(authors[0])
            self.comboBox_5.addItem(authors[0])
            self.comboBox_7.addItem(authors[0])
    
    def Show_Publishers_ComboBox(self):
        self.db = MySQLdb.connect(host ='localhost', user='root', password='toor' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT publisher_name FROM publisher''')
        data = self.cur.fetchall()
        self.comboBox_3.clear()
        for publisher in data:
            #print(publisher[0])
            self.comboBox_3.addItem(publisher[0])
            self.comboBox_8.addItem(publisher[0])


    def Show_Books_ComboBox(self):
        self.db = MySQLdb.connect(host ='localhost', user='root', password='toor' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT book_name FROM book''')
        data = self.cur.fetchall()
        self.comboBox_9.clear()
        for book in data:
            self.comboBox_9.addItem(book[0])
            self.comboBox_22.addItem(book[0])
        
        self.cur.execute('''SELECT book_code FROM book ''')
        data1 = self.cur.fetchall()
        self.comboBox_14.clear()
        for bookcode in data1:
            self.comboBox_14.addItem(bookcode[0])
            self.comboBox_15.addItem(bookcode[0])
            self.comboBox_16.addItem(bookcode[0])

    def Show_Students_ComboBox(self):
        self.db = MySQLdb.connect(host = 'localhost', user='root' , password='toor', db='library')
        self.cur = self.db.cursor()


        self.cur.execute('''SELECT student_name FROM students''')
        data = self.cur.fetchall()
        self.comboBox_10.clear()
        for student in data:
            self.comboBox_12.addItem(student[0])
            self.comboBox_10.addItem(student[0])
    

    def Show_RollNo_ComboBox(self):
        self.db = MySQLdb.connect(host = 'localhost', user='root' , password='toor', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT student_rollno FROM students''')
        data = self.cur.fetchall()
        self.comboBox_11.clear()
        for rollno in data:
            self.comboBox_11.addItem(rollno[0])
            self.comboBox_13.addItem(rollno[0])

    
    ############################
    ######THEMES################

    def Dark_Blue_Theme(self):
        style = open('themes/darkblue.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def Dark_Orange_Theme(self):
        style = open('themes/darkorange.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def QDark(self):
        style = open('themes/qdark.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)

    def QDarkGray(self):
        style = open('themes/qdarkgray.css' , 'r')
        style = style.read()
        self.setStyleSheet(style)


    ############################
    ######STUDENTS################

    def Add_New_Student(self):
        self.db = MySQLdb.connect(host ='localhost', user='root', password='toor' , db='library')
        self.cur = self.db.cursor()
        
        studentname = self.lineEdit_20.text()
        studentrollno = self.lineEdit_25.text()
        studentdob = self.lineEdit_30.text()
        studentyear = self.lineEdit_31.text()
        studentemail = self.lineEdit_32.text()

        self.cur.execute('''
            INSERT INTO students(student_name , student_rollno , student_dob , student_year , student_email)
            VALUES (%s , %s , %s , %s , %s)
        ''',(studentname , studentrollno , studentdob , studentyear , studentemail))
        self.db.commit()
        self.db.close()
        self.statusBar().showMessage('Student Added Sucessfully!')
        self.lineEdit_20.setText('')
        self.lineEdit_25.setText('')
        self.lineEdit_30.setText('')
        self.lineEdit_31.setText('')
        self.lineEdit_32.setText('')
        self.Show_All_Students()
        self.Show_Students_ComboBox()
        self.Show_RollNo_ComboBox()


    def Show_All_Students(self):
        self.db = MySQLdb.connect(host ='localhost', user='root', password='toor' , db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT student_name , student_rollno , student_dob , student_year, student_email FROM students''')
        data = self.cur.fetchall()
        #print(data)
        self.tableWidget_6.setRowCount(0)
        self.tableWidget_6.insertRow(0)

        for row ,form in enumerate(data):
            for column ,item in enumerate(form):
                self.tableWidget_6.setItem(row , column ,QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget_6.rowCount()
            self.tableWidget_6.insertRow(row_position)


    def Search_Students(self):
        try:
            self.db = MySQLdb.connect(host ='localhost', user='root', password='toor' , db='library')
            self.cur = self.db.cursor()
            
            if self.lineEdit_27.text() != '':
                studentrollno = self.lineEdit_27.text()

                sql = '''SELECT * FROM students WHERE student_rollno=%s'''
                self.cur.execute(sql, [(studentrollno)])
                data = self.cur.fetchone()
                #print(data)

                self.lineEdit_24.setText(data[1])
                self.lineEdit_26.setText(data[2])
                self.lineEdit_35.setText(data[3])
                self.lineEdit_33.setText(data[4])
                self.lineEdit_34.setText(data[5])
            else:
                warning = QMessageBox.warning(self , 'Warning', "Provide Data to Search!", QMessageBox.Ok)
        except:
            warning = QMessageBox.warning(self , 'Warning', "Student with that Roll Number doesn't exist", QMessageBox.Ok)
            pass
            self.lineEdit_27.setText('')

    def Edit_Student(self):
        try:
            self.db = MySQLdb.connect(host ='localhost', user='root', password='toor' , db='library')
            self.cur = self.db.cursor()
            
            studentnameoriginal = self.lineEdit_27.text()
            studentname = self.lineEdit_24.text()
            studentrollno = self.lineEdit_26.text()
            studentdob = self.lineEdit_35.text()
            studentyear = self.lineEdit_33.text()
            studentemail = self.lineEdit_34.text()

            if self.lineEdit_24.text() != '':
                self.cur.execute('''
                    UPDATE students SET student_name = %s , student_rollno = %s , student_dob = %s , student_year = %s , student_email = %s WHERE student_name = %s
                ''',(studentname, studentrollno, studentdob , studentyear , studentemail , studentnameoriginal))
                self.db.commit()
                self.statusBar().showMessage('Student Information Updated Sucessfully!')
                self.lineEdit_24.setText('')
                self.lineEdit_26.setText('')
                self.lineEdit_35.setText('')
                self.lineEdit_33.setText('')
                self.lineEdit_34.setText('')
                self.Show_All_Students()
                self.Show_Students_ComboBox()
                self.Show_RollNo_ComboBox()
            else:
                warning = QMessageBox.warning(self , 'Warning', "There is Nothing to edit", QMessageBox.Ok)
        
        except:
            pass

    def Delete_Student(self):
        try:
            if self.lineEdit_24.text() != '':
                self.db = MySQLdb.connect(host ='localhost', user='root', password='toor' , db='library')
                self.cur = self.db.cursor()

                studentname = self.lineEdit_24.text()
                studentrollno = self.lineEdit_26.text()
                studentdob = self.lineEdit_35.text()
                studentyear = self.lineEdit_33.text()
                studentemail = self.lineEdit_34.text()
                
                warning = QMessageBox.warning(self , 'Delete Student Data', "Are You Sure You Want to Delete this student data?", QMessageBox.Yes | QMessageBox.No)
                if warning == QMessageBox.Yes :
                    sql = '''DELETE FROM students WHERE student_name=%s'''
                    self.cur.execute(sql, [(studentname)])
                    self.db.commit()
                    self.statusBar().showMessage('Student Data Deleted Sucessfully!')
                    self.lineEdit_24.setText('')
                    self.lineEdit_26.setText('')
                    self.lineEdit_35.setText('')
                    self.lineEdit_33.setText('')
                    self.lineEdit_34.setText('')
                    self.lineEdit_27.setText('')
                    self.Show_All_Students()
                    self.Show_Students_ComboBox()
                    self.Show_RollNo_ComboBox()
                else:
                    pass
            else:
                warning = QMessageBox.warning(self , 'Warning', "There is Nothing to delete", QMessageBox.Ok)
        
        except:
            pass

############################
    ######STUDENTS END################

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()