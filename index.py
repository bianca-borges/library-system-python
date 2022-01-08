import pymysql
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import datetime

from PyQt5.uic import loadUiType

ui,_ = loadUiType('library.ui')


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_Buttons()
        self.show_category()
        self.show_author()
        self.show_publisher()
        self.category_options()
        self.author_options()
        self.publisher_options()
        self.show_all_books()
        self.show_operations()

    # -------------- Buttons ----------------- #
    def Handle_UI_Changes(self):
        self.tabWidget.tabBar().setVisible(False)

    def Handle_Buttons(self):
        self.pushButton.clicked.connect(self.OpenDayTab)
        self.pushButton_2.clicked.connect(self.OpenBooksTab)
        self.pushButton_26.clicked.connect(self.OpenUsersTab)
        self.pushButton_4.clicked.connect(self.OpenSettingTab)
        self.pushButton_7.clicked.connect(self.add_new_books)
        self.pushButton_14.clicked.connect(self.add_category)
        self.pushButton_15.clicked.connect(self.add_author)
        self.pushButton_16.clicked.connect(self.add_publisher)
        self.pushButton_9.clicked.connect(self.search_books)
        self.pushButton_8.clicked.connect(self.edit_books)
        self.pushButton_10.clicked.connect(self.delete_books)
        self.pushButton_11.clicked.connect(self.add_new_user)
        self.pushButton_12.clicked.connect(self.login)
        self.pushButton_13.clicked.connect(self.edit_user)
        self.pushButton_6.clicked.connect(self.daily_operations)


    def OpenDayTab(self):
        self.tabWidget.setCurrentIndex(0)

    def OpenBooksTab(self):
        self.tabWidget.setCurrentIndex(1)

    def OpenUsersTab(self):
        self.tabWidget.setCurrentIndex(3)

    def OpenSettingTab(self):
        self.tabWidget.setCurrentIndex(4)

    # -------------- Daily ----------------- #    
    def daily_operations(self):
        book_title = self.lineEdit.text()
        client_name = self.lineEdit_29.text()
        type = self.comboBox.currentText()
        days_number = self.comboBox_2.currentIndex() + 1
        today_date = datetime.date.today()
        to_date = today_date + datetime.timedelta(days=days_number)

        self.db = pymysql.connect(host='localhost', user='root', password='root', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''
            INSERT INTO dayoperations(book_name, client, type, days, date, to_date )
            VALUES (%s , %s , %s, %s , %s , %s)
        ''' , (book_title, client_name, type, days_number, today_date, to_date))

        self.db.commit()
        self.statusBar().showMessage('New Operation Added')
        self.show_operations()

    def show_operations(self):
        self.db = pymysql.connect(host='localhost', user='root', password='root', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' 
            SELECT book_name , client , type , date , to_date FROM dayoperations
        ''')

        data = self.cur.fetchall()

        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        for row , form in enumerate(data):
            for column , item in enumerate(form):
                self.tableWidget.setItem(row , column , QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)


    # -------------- Books ----------------- #
    def show_all_books(self):
        self.db = pymysql.connect(host='localhost', user='root', password='root', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT book_code, book_name, book_description, book_category, book_author, book_publisher, book_price FROM book''')
        data = self.cur.fetchall()

        self.tableWidget_5.setRowCount(0)
        self.tableWidget_5.insertRow(0)

        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget_5.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget_5.rowCount()
            self.tableWidget_5.insertRow(row_position)

        self.db.close()

    def add_new_books(self):
        self.db = pymysql.connect(host='localhost', user='root', password ='root', db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_2.text()
        book_description = self.textEdit.toPlainText()
        book_code = self.lineEdit_3.text()
        book_category = self.comboBox_3.currentText()
        book_author = self.comboBox_4.currentText()
        book_publisher = self.comboBox_5.currentText()
        book_price = self.lineEdit_4.text()

        self.cur.execute('''
            INSERT INTO book(book_name, book_description, book_code, book_category, book_author, book_publisher, book_price)
            VALUES (%s , %s , %s , %s , %s , %s , %s)
        ''' ,(book_title, book_description, book_code, book_category, book_author, book_publisher, book_price))

        self.db.commit()
        self.statusBar().showMessage('New Book Added')
        self.show_all_books()

        self.lineEdit_2.setText('')
        self.textEdit.setPlainText('')
        self.lineEdit_3.setText('')
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_5.setCurrentIndex(0)
        self.lineEdit_4.setText('')

    def search_books(self):
        self.db = pymysql.connect(host='localhost', user='root', password ='root', db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_5.text()
        self.cur.execute(''' SELECT * FROM book WHERE book_name=%s ''', book_title)

        data = self.cur.fetchone()
        print(data)
        
        self.lineEdit_8.setText(data[1])
        self.textEdit_2.setPlainText(data[2])
        self.lineEdit_7.setText(data[3])
        self.comboBox_7.setCurrentText(data[4])
        self.comboBox_8.setCurrentText(data[5])
        self.comboBox_6.setCurrentText(data[6])
        self.lineEdit_6.setText(str(data[7]))

    def edit_books(self):
        self.db = pymysql.connect(host='localhost', user='root', password ='root', db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_8.text()
        book_description = self.textEdit_2.toPlainText()
        book_code = self.lineEdit_7.text()
        book_category = self.comboBox_7.currentText()
        book_author = self.comboBox_8.currentText()
        book_publisher = self.comboBox_6.currentText()
        book_price = self.lineEdit_6.text()


        search_book_title = self.lineEdit_5.text()

        self.cur.execute('''
            UPDATE book SET book_name=%s, book_description=%s, book_code=%s, book_category=%s, book_author=%s, book_publisher=%s, book_price=%s WHERE book_name = %s            
        ''', (book_title, book_description, book_code, book_category, book_author, book_publisher, book_price, search_book_title))

        self.db.commit()
        self.statusBar().showMessage('Book updated!')
        self.show_all_books()


    def delete_books(self):
        self.db = pymysql.connect(host='localhost', user='root', password ='root', db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_5.text()

        self.cur.execute('''
            DELETE FROM book WHERE book_name=%s
        ''', (book_title))

        self.db.commit()
        self.statusBar().showMessage('Book deleted!')
        self.show_all_books()

    # -------------- Users ----------------- #
    def add_new_user(self):
        self.db = pymysql.connect(host='localhost', user='root', password ='root', db='library')
        self.cur = self.db.cursor()

        username = self.lineEdit_9.text()
        email = self.lineEdit_10.text()
        password = self.lineEdit_11.text()
        password2 = self.lineEdit_12.text()

        if password == password2 :
            self.cur.execute(''' 
                INSERT INTO users(user_name , user_email , user_password)
                VALUES (%s , %s , %s)
            ''' , (username, email, password))

            self.db.commit()
            self.statusBar().showMessage('New User Added')

        else:
            self.label_38.setText('Please, add a valid password twice')

    def login(self):
        self.db = pymysql.connect(host='localhost' , user='root' , password ='root' , db='library')
        self.cur = self.db.cursor()

        username = self.lineEdit_14.text()
        password = self.lineEdit_13.text()

        sql = ''' SELECT * FROM users'''

        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row in data  :
            if username == row[1] and password == row[3]:
                print('user match')
                self.statusBar().showMessage('Valid Username & Password')
                self.groupBox_4.setEnabled(True)

                self.lineEdit_17.setText(row[1])
                self.lineEdit_15.setText(row[2])
                self.lineEdit_16.setText(row[3])

    def edit_user(self):

        username = self.lineEdit_17.text()
        email = self.lineEdit_15.text()
        password = self.lineEdit_16.text()
        password2 = self.lineEdit_18.text()

        original_name = self.lineEdit_14.text()

        if password == password2 :
            self.db = pymysql.connect(host='localhost', user='root', password='root', db='library')
            self.cur = self.db.cursor()

            print(username)
            print(email)
            print(password)

            self.cur.execute('''
                UPDATE users SET user_name=%s, user_email=%s, user_password=%s WHERE user_name=%s
            ''', (username, email, password, original_name))

            self.db.commit()
            self.statusBar().showMessage('User Data Updated Successfully')

        else:
            print('make sure you entered you password correctly')

    # -------------- Settings ----------------- #
    def add_category(self):
        self.db = pymysql.connect(host='localhost', user='root', password='root', db='library')
        self.cur = self.db.cursor()

        category_name = self.lineEdit_19.text()
        self.cur.execute('''
            INSERT INTO category (category_name) VALUES (%s)
        ''', category_name,)

        self.db.commit()
        self.statusBar().showMessage('Added Successfully!')
        self.lineEdit_19.setText('')
        self.show_category()
        self.category_options()

    def show_category(self):
        self.db = pymysql.connect(host='localhost', user='root', password='root', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT category_name FROM category ''')
        data = self.cur.fetchall()
        
        if data:
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)


    def add_author(self):
        self.db = pymysql.connect(host='localhost', user='root', password='root', db='library')
        self.cur = self.db.cursor()

        author_name = self.lineEdit_20.text()
        self.cur.execute('''
            INSERT INTO authors (author_name) VALUES (%s)
        ''', author_name,)

        self.db.commit()
        self.statusBar().showMessage('Added Successfully!')
        self.lineEdit_20.setText('')
        self.show_author()
        self.author_options()
    
    def show_author(self):
        self.db = pymysql.connect(host='localhost', user='root', password='root', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT author_name FROM authors ''')
        data = self.cur.fetchall()
        
        if data:
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_3.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(row_position)


    def add_publisher(self):
        self.db = pymysql.connect(host='localhost', user='root', password='root', db='library')
        self.cur = self.db.cursor()

        publisher_name = self.lineEdit_21.text()
        self.cur.execute('''
            INSERT INTO publishers (publisher_name) VALUES (%s)
        ''', publisher_name,)

        self.db.commit()
        self.lineEdit_21.setText('')
        self.statusBar().showMessage('Added Successfully!')
        self.show_publisher()
        self.publisher_options()

    def show_publisher(self):
        self.db = pymysql.connect(host='localhost', user='root', password='root', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT publisher_name FROM publishers ''')
        data = self.cur.fetchall()
        
        if data:
            self.tableWidget_4.setRowCount(0)
            self.tableWidget_4.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_4.rowCount()
                self.tableWidget_4.insertRow(row_position)

    # ----------------------- Displaying Options --------------------------- #
    def category_options(self):
        self.db = pymysql.connect(host='localhost', user='root', password='root', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT category_name FROM category ''')
        data = self.cur.fetchall()

        self.comboBox_3.clear()
        for category in data:
            self.comboBox_3.addItem(category[0])
            self.comboBox_7.addItem(category[0])

    def author_options(self):
        self.db = pymysql.connect(host='localhost', user='root', password='root', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT author_name FROM authors ''')
        data = self.cur.fetchall()

        self.comboBox_4.clear()
        for author in data:
            self.comboBox_4.addItem(author[0])
            self.comboBox_8.addItem(author[0])

    def publisher_options(self):
        self.db = pymysql.connect(host='localhost', user='root', password='root', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT publisher_name FROM publishers ''')
        data = self.cur.fetchall()

        self.comboBox_5.clear()
        for publisher in data:
            self.comboBox_5.addItem(publisher[0])
            self.comboBox_6.addItem(publisher[0])


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
