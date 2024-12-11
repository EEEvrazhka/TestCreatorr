import sys
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QFileDialog, QTextEdit, QCheckBox, QVBoxLayout, QScrollArea, QFrame
from PyQt5.QtGui import QPixmap, QIcon


class Editor(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./static/ui/Editor.ui', self)
        self.current_question = 1
        self.current_image_filename = ''
        self.test_id = 1

        self.widgets = [[self.label_1, self.textEdit_1, self.checkBox_1],
                        [self.label_2, self.textEdit_2, self.checkBox_2],
                        [self.label_3, self.textEdit_3, self.checkBox_3],
                        [self.label_4, self.textEdit_4, self.checkBox_4],
                        [self.label_5, self.textEdit_5, self.checkBox_5]]
        self.change_buttons = [self.pushButton_1, self.pushButton_2,
                               self.pushButton_3, self.pushButton_4, self.pushButton_5]

        self.label.setText("Вопрос " + str(self.current_question))

        self.pushButton2_1.clicked.connect(self.close_window2)
        self.pushButton_img.clicked.connect(self.add_image)

        self.pushButton_7.clicked.connect(self.next_question)

        for i in range(5):
            self.change_buttons[i].clicked.connect(lambda _, num=i: self.change_visibility(num))

    def close_window2(self):
        self.close()

    def next_question(self):
        try:
            connection = sqlite3.connect('./db/my_database.db')
            cursor = connection.cursor()

            cursor.execute('INSERT INTO Questions (test_id, question_text, image_path) VALUES (?, ?, ?)',
                           (self.test_id, self.textEdit.toPlainText(), self.current_image_filename))

            for widget in self.widgets:
                if widget[1].isEnabled():
                    if widget[2].isChecked():
                        cursor.execute('INSERT INTO Answers (question_id, answer_text, is_correct) VALUES (?, ?, ?)',
                                       (self.current_question, widget[1].toPlainText(), 1))
                    else:
                        cursor.execute('INSERT INTO Answers (question_id, answer_text, is_correct) VALUES (?, ?, ?)',
                                       (self.current_question, widget[1].toPlainText(), 0))

            connection.commit()
            connection.close()
            # print(self.textEdit.toPlainText())
        except Exception as e:
            print(e)
        self.current_question += 1
        self.label.setText("Вопрос " + str(self.current_question))

    def add_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "",
                                                   "Images (*.png *.xpm *.jpg *.jpeg);;All Files (*)",
                                                   options=options)
        try:
            if file_name:
                self.current_image_filename = file_name
                pixmap = QPixmap(file_name)

                label_image = QLabel(self)
                label_image.setPixmap(pixmap.scaled(281, 261))
                label_image.setGeometry(self.pushButton_img.geometry())
                label_image.show()

                self.pushButton_img.hide()
        except Exception as e:
            print(f"Ошибка: {e}")

    def change_visibility(self, num):
        if self.widgets[num][0].isEnabled():
            self.change_buttons[num].setText("Показать")
        else:
            self.change_buttons[num].setText("Скрыть")

        for widget in self.widgets[num]:
            widget.setEnabled(not widget.isEnabled())


class Example(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            uic.loadUi('./static/ui/TestCreator.ui', self)
            self.pushButton.clicked.connect(self.add_test)

            self.test_buttons = [self.pushButton_3, self.pushButton_4, self.pushButton_5]
            self.current_test_index = 0

        except Exception as e:
            print(e)

        connection = sqlite3.connect('db/my_database.db')
        cursor = connection.cursor()

        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS Tests (
                        id INTEGER PRIMARY KEY  ,
                        title TEXT NOT NULL
                        )
                        ''')

        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS Questions (
                        id INTEGER PRIMARY KEY  ,
                        test_id INTEGER NOT NULL,
                        question_text TEXT NOT NULL,
                        image_path TEXT NOT NULL
                        )
                        ''')

        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS Answers (
                        id INTEGER PRIMARY KEY  ,
                        question_id INTEGER NOT NULL,
                        answer_text TEXT NOT NULL,
                        is_correct INTEGER NOT NULL
                        )
                        ''')
        cursor.execute('SELECT * FROM Tests')
        results = cursor.fetchall()
        print(*results)
        for i in results:
            print(i)
        connection.close()

    def add_test(self):
        test_name = self.lineEdit.text()
        try:
            connection = sqlite3.connect('./db/my_database.db')
            cursor = connection.cursor()

            cursor.execute('SELECT * FROM Tests')
            results = cursor.fetchall()
            for i in results:
                if i[1] == test_name:
                    self.lineEdit.setText("Test exists")
                    return

            if test_name and self.current_test_index < len(self.test_buttons):
                self.test_buttons[self.current_test_index].setText(test_name)
                self.current_test_index += 1
                self.lineEdit.clear()

            cursor.execute('INSERT INTO Tests (title) VALUES (?)',
                           (test_name,))
            connection.commit()
            connection.close()

            self.open_second_window()
        except Exception as e:
            print(f"Ошибка: {e}")

    def open_second_window(self):
        try:
            self.second_window = Editor()
            self.second_window.show()
        except Exception as e:
            print(f"Ошибка: {e}")

    def open_test(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
