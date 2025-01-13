import sys
import os
import sqlite3

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout, QScrollArea)
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from functools import partial

from TestCreator import Ui_MainWindow
from Editor import Ui_Form as UI_Editor
from TestPassing import Ui_Form as UI_pass
from Passed import Ui_Form as UI_passed


class Passed(QWidget, UI_passed):
    def __init__(self, correct_answers, total_answers):
        super().__init__()
        # uic.loadUi('./static/ui/Passed.ui', self)
        #self.ui = Ui_Form()
        self.setupUi(self)
        # self.correct_answers = correct_answers
        # self.total_answers = total_answers
        self.label.setText(f'Ваш результат: {correct_answers}/{total_answers}')


class TestPass(QWidget, UI_pass):
    def __init__(self, test_ID):
        super().__init__()
        #uic.loadUi('./static/ui/TestPassing.ui', self)
        self.setupUi(self)
        self.test_id = test_ID
        self.current_question = 1
        self.correct_answers_count = 0
        self.total_questions = 0

        self.results_questions = ''
        self.results_answers = ''

        self.widgets = [[self.label_1, self.textEdit_1, self.checkBox_1],
                        [self.label_2, self.textEdit_2, self.checkBox_2],
                        [self.label_3, self.textEdit_3, self.checkBox_3],
                        [self.label_4, self.textEdit_4, self.checkBox_4],
                        [self.label_5, self.textEdit_5, self.checkBox_5]]

        self.load_questions_and_answers()
        self.pushButton2_1.clicked.connect(self.close)
        self.pushButton_7.clicked.connect(self.open_question)
        self.open_question()

    def close_window(self):
        self.close()

    def load_questions_and_answers(self):
        connection = sqlite3.connect('./db/my_database.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM Questions WHERE test_id = ?', (self.test_id,))
        self.results_questions = cursor.fetchall()

        cursor.execute('SELECT * FROM Answers WHERE test_id = ?', (self.test_id,))
        self.results_answers = cursor.fetchall()

        connection.close()

        self.total_questions = len(self.results_questions)
        print(f"Загруженные вопросы для теста {self.test_id}: {self.results_questions}")
        print(f"Загруженные ответы для теста {self.test_id}: {self.results_answers}")

    def check_answer(self):
        selected_answers = []
        correct_answers = []

        print(self.current_question)
        print(self.results_questions)

        for answer in self.results_answers:
            if answer[2] == self.current_question - 1:
                if answer[4] == 1:
                    correct_answers.append(answer[3])

        for widget in self.widgets:
            if widget[2].isChecked():
                selected_answers.append(widget[1].toPlainText())

        if set(selected_answers) == set(correct_answers):
            self.correct_answers_count += 1
            print("Правильный ответ!")
        else:
            print("Неправильный ответ.")

    def open_question(self):
        if self.current_question != 1:
            self.check_answer()

        if self.current_question > self.total_questions:
            print(f"Тест завершен. Правильные ответы: {self.correct_answers_count}")
            try:
                self.passed = Passed(self.correct_answers_count, self.total_questions)
                self.passed.show()
            except Exception as e:
                print(e)
            return

        for widget in self.widgets:
            widget[1].clear()
            widget[2].setChecked(False)
            widget[1].setEnabled(False)

        current_question_data = self.results_questions[self.current_question - 1]
        question_text = current_question_data[2]
        image_path = current_question_data[3]

        self.label_8.setText("Вопрос " + str(self.current_question))
        self.label_9.setText(question_text)

        pixmap = QPixmap(str(image_path))
        label_image = QLabel(self)
        label_image.setPixmap(pixmap.scaled(281, 261))
        label_image.setGeometry(self.label.geometry())
        label_image.show()

        answers_for_question = [answer for answer in self.results_answers if answer[2] == self.current_question]
        print(f"Ответы для вопроса {self.current_question}: {answers_for_question}")  # Отладка

        for i, answer in enumerate(answers_for_question):
            if i < len(self.widgets):
                self.widgets[i][1].setPlainText(answer[3])

        self.current_question += 1


class Editor(QWidget, UI_Editor):
    def __init__(self, test_ID, queston_ID):
        super().__init__()
        uic.loadUi('./static/ui/Editor.ui', self)
        # self.ui = Ui_Form()
        self.setupUi(self)
        self.current_question = queston_ID
        self.current_image_filename = ''
        self.test_id = test_ID

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

        self.pushButton_save.clicked.connect(self.save_test)

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
                        cursor.execute('INSERT INTO Answers (test_id, question_id, answer_text, is_correct) VALUES (?, ?, ?, ?)',
                                       (self.test_id, self.current_question, widget[1].toPlainText(), 1))
                    else:
                        cursor.execute(
                            'INSERT INTO Answers (test_id, question_id, answer_text, is_correct) VALUES (?, ?, ?, ?)',
                            (self.test_id, self.current_question, widget[1].toPlainText(), 0))

            connection.commit()
            connection.close()

        except Exception as e:
            print(e)
        self.current_question += 1
        self.editor = Editor(self.test_id, self.current_question)
        self.editor.show()
        self.close()
        self.label.setText("Вопрос " + str(self.current_question))

    def add_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Выберите изображение", "",
                                                   "Images (*.png *.xpm *.jpg *.jpeg);;All Files (*)",
                                                   options=options)
        try:
            if file_name:

                pixmap = QPixmap(file_name)

                self.save_image(file_name)

                label_image = QLabel(self)
                label_image.setPixmap(pixmap.scaled(281, 261))
                label_image.setGeometry(self.pushButton_img.geometry())
                label_image.show()

                self.pushButton_img.hide()
        except Exception as e:
            print(f"Ошибка: {e}")

    def save_image(self, file_name):
        static_folder = "static\img"
        if not os.path.exists(static_folder):
            os.makedirs(static_folder)

        base_name = os.path.basename(file_name)
        new_file_path = os.path.join(static_folder, base_name)
        pixmap = QPixmap(file_name)
        self.current_image_filename = new_file_path
        if pixmap.save(new_file_path):
            print(f"Изображение сохранено в {new_file_path}")
        else:
            print("Ошибка при сохранении изображения")

    def change_visibility(self, num):
        if self.widgets[num][0].isEnabled():
            self.change_buttons[num].setText("Показать")
        else:
            self.change_buttons[num].setText("Скрыть")

        for widget in self.widgets[num]:
            widget.setEnabled(not widget.isEnabled())

    def save_test(self):
        try:
            connection = sqlite3.connect('./db/my_database.db')
            cursor = connection.cursor()

            cursor.execute('INSERT INTO Questions (test_id, question_text, image_path) VALUES (?, ?, ?)',
                           (self.test_id, self.textEdit.toPlainText(), self.current_image_filename))

            for widget in self.widgets:
                if widget[1].isEnabled():
                    if widget[2].isChecked():
                        cursor.execute('INSERT INTO Answers (test_id, question_id, answer_text, is_correct) VALUES (?, ?, ?, ?)',
                                       (self.test_id, self.current_question, widget[1].toPlainText(), 1))
                    else:
                        cursor.execute(
                            'INSERT INTO Answers (test_id, question_id, answer_text, is_correct) VALUES (?, ?, ?, ?)',
                            (self.test_id, self.current_question, widget[1].toPlainText(), 0))

            connection.commit()
            connection.close()

        except Exception as e:
            print(e)
        self.close()


class MainMenu(QMainWindow, Ui_MainWindow):
    def __init__(self):
        self.test_pass = None
        self.second_window = None
        try:
            super().__init__()
            uic.loadUi('./static/ui/TestCreator.ui', self)
            # self.ui = Ui_MainWindow()
            self.setupUi(self)
            self.pushButton.clicked.connect(self.add_test)

            self.test_buttons = []
            self.current_test_index = 0
            self.test_id = 0

            self.scrollArea = QScrollArea(self.centralwidget)
            self.scrollArea.setGeometry(20, 80, 280, 400)
            self.scrollArea.setWidgetResizable(True)

            self.scrollContent = QWidget()
            self.scrollLayout = QVBoxLayout(self.scrollContent)

            self.scrollContent.setLayout(self.scrollLayout)
            self.scrollArea.setWidget(self.scrollContent)

            self.scrollLayout.setContentsMargins(0, 0, 0, 380)
            self.scrollLayout.setSpacing(0)

            self.pushButton_2.clicked.connect(self.close)

        except Exception as e:
            print("Ошибка при инициализации виджетов" + e)

        try:
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
                            test_id INTEGER NOT NULL,
                            question_id INTEGER NOT NULL,
                            answer_text TEXT NOT NULL,
                            is_correct INTEGER NOT NULL
                            )
                            ''')
            cursor.execute('SELECT * FROM Tests')
            results = cursor.fetchall()
            #print(*results)
            for i in results:
                #print(i[1])
                button = QPushButton(i[1], self.scrollContent)
                button.clicked.connect(partial(self.open_test_window, i[1]))
                self.test_buttons.append(button)
                self.scrollLayout.addWidget(button)

            connection.close()
        except Exception as e:
            print("Ошибка при создании таблиц: " + e)

    def open_test_window(self, name):
        try:
            connection = sqlite3.connect('./db/my_database.db')
            cursor = connection.cursor()

            cursor.execute('SELECT * FROM Tests WHERE title = ?', (name,))
            result = cursor.fetchone()

            if result:
                self.test_pass = TestPass(int(result[0]))
                self.test_pass.show()
            else:
                print(f"Тест с именем {name} не найден.")

            connection.close()
        except Exception as e:
            print(f"Ошибка при открытии окна теста: {e}")

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

            if test_name:
                button = QPushButton(test_name, self.scrollContent)
                button.clicked.connect(partial(self.open_test_window, test_name))
                self.test_buttons.append(button)
                self.scrollLayout.addWidget(button)
                self.lineEdit.clear()
                cursor.execute('INSERT INTO Tests (title) VALUES (?)',
                               (test_name,))
            cursor.execute('SELECT * FROM Tests')
            results = cursor.fetchall()
            self.test_id = int(results[len(results)-1][0])

            connection.commit()
            connection.close()

            self.open_second_window()
        except Exception as e:
            print(f"Ошибка: {e}")

    def open_second_window(self):
        try:
            self.second_window = Editor(self.test_id, 1)
            self.second_window.show()
        except Exception as e:
            print(f"Ошибка: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainMenu()
    ex.show()
    sys.exit(app.exec())
