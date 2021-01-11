import sys
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import operator
from random import choice, randrange
import pyqtgraph as pg
import csv
import math
import datetime


class Main_program(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Главное окно')
        # Добавляем изображение
        self.pixmap = QPixmap('mathmem.jpg')
        self.pic_mem1.setPixmap(self.pixmap)
        # Включаем кнопки
        list_btn = [self.btn_calculator, self.btn_oral_count, self.btn_theory, self.btn_practice, self.btn_decision,
                    self.btn_randomv, self.btn_graph, self.btn_table]
        for i in list_btn:
            i.clicked.connect(self.run)

    def run(self):
        text = self.sender().text()
        if text == 'КАЛЬКУЛЯТОР':
            self.w1 = Calculator()
            self.w1.show()
        elif text == 'УСТНЫЙ СЧЁТ':
            self.w2 = Oral_count()
            self.w2.show()
        elif text == 'ТЕОРИЯ':
            self.w3 = Theory()
            self.w3.show()
        elif text == 'ПРАКТИКА':
            self.w4 = Practice()
            self.w4.show()
        elif text == 'ОТВЕТЫ':
            self.w5 = Decision()
            self.w5.show()
        elif text == 'РАНДОМНЫЙ ВАРИАНТ':
            self.w6 = Random_variant()
            self.w6.show()
        elif text == 'ГРАФИК':
            self.w7 = Graph()
            self.w7.show()
        elif text == 'ТАБЛИЦА С РЕЗУЛЬТАТАМИ':
            self.w8 = Table()
            self.w8.show()


class Random_variant(QMainWindow):  # Создание рандомного варианта из 12 задач
    def __init__(self):
        super().__init__()
        self.number_question = ''
        uic.loadUi('random_varik.ui', self)
        self.color = QPixmap('color.png')
        self.color_fon.setPixmap(self.color)
        self.setWindowTitle('Случайный вариант')
        self.pointer = 0  # Указатель на то, какой сейчас вопрос решается
        self.start = datetime.datetime.today()  # засекаем время начала
        self.doing_problem()
        self.ans_list = []  # Хранятся ответы пользователя
        self.btn_next_p1.clicked.connect(self.doing_problem)

    def doing_problem(self):  # Ищем пример из базы
        if self.pointer == 12:
            self.answer()
            self.end = datetime.datetime.today()  # засекаем время конца
            self.data = f'{self.end.year}.{self.end.month}.{self.end.day}'  # пишем сегодняшнюю дату
            self.minutes = divmod((self.end - self.start).seconds, 60)  # время в минутах и секундах
            self.v1 = Answer(self.ans_list, self.minutes, self.data)  # Выводим вердикт по решению варианта
            self.v1.show()
        else:
            if self.pointer > 0:
                self.answer()
            self.pointer = self.pointer + 1
            self.number_question = str(randrange(1, 31))
            if self.pointer > 9:
                self.pic1 = QPixmap('photo/' + str(self.pointer) + '.' + self.number_question + '.png')
                self.problems.setPixmap(self.pic1)
            else:
                self.pic1 = QPixmap('photo/' + '0' + str(self.pointer) + '.' + self.number_question + '.png')
                self.problems.setPixmap(self.pic1)

    def answer(self):  # Проверка ответа
        text = self.ans_p1.text()  # Получим текст из поля ввода
        if self.pointer > 9:
            if text == answer_p[str(self.pointer) + '.' + self.number_question]:
                self.ans_list.append([str(self.pointer) + '.' + self.number_question, 'Правильно', '+'])
            else:
                self.ans_list.append([str(self.pointer) + '.' + self.number_question, 'Неправильно', '-'])
        else:
            if text == answer_p['0' + str(self.pointer) + '.' + self.number_question]:
                self.ans_list.append([str(self.pointer) + '.' + self.number_question, 'Правильно', '+'])
            else:
                self.ans_list.append([str(self.pointer) + '.' + self.number_question, 'Неправильно', '-'])


class Answer(QMainWindow):  # Вывод вердикта
    def __init__(self, ans_list, minutes, data):
        super().__init__()
        self.ans_list = ans_list
        self.minutes = minutes
        self.data = data
        uic.loadUi('answer.ui', self)
        self.setWindowTitle('Вердикт')
        list_label = [self.label_1, self.label_2, self.label_3, self.label_4, self.label_5, self.label_6, self.label_7,
                      self.label_8, self.label_9, self.label_10, self.label_11, self.label_12]
        for i in range(0, 12):
            list_label[i].setText(self.ans_list[i][0] + ' вопрос: ' + self.ans_list[i][1])
        self.verdict.setText(f'Время выполнения: {self.minutes[0]} min. {self.minutes[1]} sec.')
        self.btn_save.clicked.connect(self.writing)

    def writing(self):  # записываем в файл данные о результате решения варианта
        with open('table.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quotechar='"', )
            d = list()
            for i in range(0, 12):
                d.append(self.ans_list[i][2])
            d.append(f'{self.minutes[0]} min. {self.minutes[1]} sec.')
            d.append(self.data)
            writer.writerow(d)


class Table(QMainWindow):  # Результаты решения пробников
    def __init__(self):
        super().__init__()
        uic.loadUi('table.ui', self)
        self.loadTable('table.csv')

    def loadTable(self, table_name):
        with open(table_name, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile,
                                delimiter=';', quotechar='"')
            title = next(reader)
            self.tableWidget.setColumnCount(len(title))
            self.tableWidget.setHorizontalHeaderLabels(title)
            self.tableWidget.setRowCount(0)
            for i, row in enumerate(reader):
                self.tableWidget.setRowCount(
                    self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(elem))
        self.tableWidget.resizeColumnsToContents()


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('calculator.ui', self)
        self.status = 0
        self.enter = 1
        # запуски всех кнопок
        for n in range(0, 10):
            getattr(self, 'btn_n%s' % n).pressed.connect(lambda x=n: self.input_number(x))

        self.btn_add.pressed.connect(lambda: self.operation(operator.add))
        self.btn_sub.pressed.connect(lambda: self.operation(operator.sub))
        self.btn_mul.pressed.connect(lambda: self.operation(operator.mul))
        self.btn_div.pressed.connect(lambda: self.operation(operator.truediv))
        self.btn_pc.pressed.connect(self.operation_pc)
        self.btn_equal.pressed.connect(self.equals)
        self.btn_ac.pressed.connect(self.reset)
        self.btn_m.pressed.connect(self.memory_store)
        self.btn_mr.pressed.connect(self.memory_recall)

        self.memory = 0
        self.reset()
        self.show()

    def display(self):  # отображение чисел
        self.lcdNumber.display(self.stack[-1])

    def reset(self):  # очистка стека
        self.state = self.status  # Разграничивает поступившие и выполнившие запросы
        self.stack = [0]
        self.last_operation = None
        self.current_op = None
        self.display()

    def input_number(self, x):  # Добавление чисел в стек
        if self.state == self.status:
            self.state = self.enter
            self.stack[-1] = x
        else:
            self.stack[-1] = self.stack[-1] * 10 + x
        self.display()

    def operation(self, op):
        if self.current_op:  # Содержит текущую ситуацию
            self.equals()
        self.stack.append(0)
        self.state = self.enter
        self.current_op = op

    def operation_pc(self):  # Отдельно для процентов
        self.state = self.enter
        self.stack[-1] *= 0.01
        self.display()

    def equals(self):
        # Если новые данные не введены, повторяем
        if self.state == self.status and self.last_operation:
            s, self.current_op = self.last_operation
            self.stack.append(s)

        if self.current_op:
            self.last_operation = self.stack[-1], self.current_op
            try:
                self.stack = [self.current_op(*self.stack)]
            except Exception:
                self.lcdNumber.display('Err')
                self.stack = [0]
            else:
                self.current_op = None
                self.state = self.status
                self.display()

    def memory_store(self):  # Хранение памяти
        self.memory = self.lcdNumber.value()

    def memory_recall(self):  # Повторный вызов
        self.state = self.enter
        self.stack[-1] = self.memory
        self.display()


class Oral_count(QMainWindow):
    def __init__(self):
        super().__init__()
        self.example = ''
        uic.loadUi('chot.ui', self)
        self.setWindowTitle('Устный счёт')
        self.pixmap3 = QPixmap('important_text')
        self.important_text.setPixmap(self.pixmap3)
        self.doing_example()
        self.btn_ok.clicked.connect(self.answer)
        self.btn_next.clicked.connect(self.doing_example)

    def doing_example(self):  # Вывод выражения
        self.random_example()
        self.problem.setText(self.example)

    def random_example(self):  # Составление выражения
        a = ['+', '-', '*', '//']
        mark = choice(a)
        if mark == "+":
            self.example = str(randrange(-1000, 1000)) + ' ' + '+' + ' ' + str(randrange(0, 1000))
        elif mark == "-":
            self.example = str(randrange(-1000, 1000)) + ' ' + '-' + ' ' + str(randrange(0, 1000))
        elif mark == "*":
            self.example = str(randrange(0, 100)) + ' ' + '*' + ' ' + str(randrange(0, 100))
        else:
            x = randrange(1, 100)
            y = randrange(1, 100)
            self.example = str(x * y) + ' ' + '//' + ' ' + str(y)

    def answer(self):  # Проверка ответа
        text = self.ans.text()  # Получим текст из поля ввода
        if text == str(eval(self.example)):
            self.pixmap1 = QPixmap('true.jpg')
            self.ans_program.setPixmap(self.pixmap1)
        else:
            self.pixmap2 = QPixmap('false.jpg')
            self.ans_program.setPixmap(self.pixmap2)


class Theory(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('theory.ui', self)
        self.setWindowTitle('Теория')
        self.initUI1()

    def initUI1(self):
        # Добавляем изображение
        self.pixmap1 = QPixmap('mathmem3.jpeg')
        self.pic_mem2.setPixmap(self.pixmap1)
        # Включаем кнопки
        list_btn = [self.btn_1, self.btn_2, self.btn_3, self.btn_4, self.btn_5, self.btn_6, self.btn_7, self.btn_8,
                    self.btn_9, self.btn_10, self.btn_11, self.btn_12]
        for i in list_btn:
            i.clicked.connect(self.theor)

    def theor(self):
        self.t1 = All_theory(self.sender().text())
        self.t1.show()


class All_theory(QMainWindow):
    def __init__(self, number_btn):
        super().__init__()
        self.number_btn = number_btn  # На какую кнопку было нажато
        self.number_btn = self.number_btn.split()[0]
        uic.loadUi('theory_' + self.number_btn + '.ui', self)
        self.color = QPixmap('color_fon2.png')  # Ставим фон
        self.color_fon.setPixmap(self.color)
        self.setWindowTitle('Теория')
        if int(self.number_btn) > 9:
            self.tr = QPixmap('photo_theory/t' + self.number_btn + '.1' + '.png')
            self.theories.setPixmap(self.tr)
        else:
            self.tr = QPixmap('photo_theory/t0' + self.number_btn + '.1' + '.png')
            self.theories.setPixmap(self.tr)
        self.pointer = 1  # Указатель на номер страницы теории
        self.btn_back.clicked.connect(self.moving_back)
        self.btn_next.clicked.connect(self.moving_next)

    def moving_back(self):  # Вернуться к прошлой странице
        if self.pointer > 1:
            self.pointer = self.pointer - 1
            if int(self.number_btn) > 9:
                self.pic_back = QPixmap('photo_theory/t' + self.number_btn + '.' + str(self.pointer) + '.png')
                self.theories.setPixmap(self.pic_back)
            else:
                self.pic_back = QPixmap('photo_theory/t0' + self.number_btn + '.' + str(self.pointer) + '.png')
                self.theories.setPixmap(self.pic_back)

    def moving_next(self):  # Пройти на следующую строку
        # Обрабатываем для разных кнопок по-разному, тк у них разное кол-во страниц
        if self.number_btn == '1':
            if self.pointer < 6:
                self.pointer = self.pointer + 1
                self.pic_next = QPixmap('photo_theory/t01' + '.' + str(self.pointer) + '.png')
                self.theories.setPixmap(self.pic_next)
        if self.number_btn == '2':
            if self.pointer < 5:
                self.pointer = self.pointer + 1
                self.pic_next = QPixmap('photo_theory/t02' + '.' + str(self.pointer) + '.png')
                self.theories.setPixmap(self.pic_next)
        if self.number_btn == '3':
            if self.pointer < 5:
                self.pointer = self.pointer + 1
                self.pic_next = QPixmap('photo_theory/t03' + '.' + str(self.pointer) + '.png')
                self.theories.setPixmap(self.pic_next)
        if self.number_btn == '4':
            if self.pointer < 12:
                self.pointer = self.pointer + 1
                self.pic_next = QPixmap('photo_theory/t04' + '.' + str(self.pointer) + '.png')
                self.theories.setPixmap(self.pic_next)
        if self.number_btn == '5':
            if self.pointer < 14:
                self.pointer = self.pointer + 1
                self.pic_next = QPixmap('photo_theory/t05' + '.' + str(self.pointer) + '.png')
                self.theories.setPixmap(self.pic_next)
        if self.number_btn == '6':
            if self.pointer < 51:
                self.pointer = self.pointer + 1
                self.pic_next = QPixmap('photo_theory/t06' + '.' + str(self.pointer) + '.png')
                self.theories.setPixmap(self.pic_next)
        if self.number_btn == '7':
            if self.pointer < 15:
                self.pointer = self.pointer + 1
                self.pic_next = QPixmap('photo_theory/t07' + '.' + str(self.pointer) + '.png')
                self.theories.setPixmap(self.pic_next)
        if self.number_btn == '8':
            if self.pointer < 13:
                self.pointer = self.pointer + 1
                self.pic_next = QPixmap('photo_theory/t08' + '.' + str(self.pointer) + '.png')
                self.theories.setPixmap(self.pic_next)
        if self.number_btn == '9':
            if self.pointer < 24:
                self.pointer = self.pointer + 1
                self.pic_next = QPixmap('photo_theory/t09' + '.' + str(self.pointer) + '.png')
                self.theories.setPixmap(self.pic_next)
        if self.number_btn == '10':
            if self.pointer < 7:
                self.pointer = self.pointer + 1
                self.pic_next = QPixmap('photo_theory/t10' + '.' + str(self.pointer) + '.png')
                self.theories.setPixmap(self.pic_next)
        if self.number_btn == '11':
            if self.pointer < 8:
                self.pointer = self.pointer + 1
                self.pic_next = QPixmap('photo_theory/t11' + '.' + str(self.pointer) + '.png')
                self.theories.setPixmap(self.pic_next)
        if self.number_btn == '12':
            if self.pointer < 11:
                self.pointer = self.pointer + 1
                self.pic_next = QPixmap('photo_theory/t12' + '.' + str(self.pointer) + '.png')
                self.theories.setPixmap(self.pic_next)


class Practice(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('practice.ui', self)
        self.setWindowTitle('Практика')
        self.initUI1()

    def initUI1(self):
        # Добавляем изображение
        self.pixmap1 = QPixmap('mathmem2.jpg')
        self.pic_mem2.setPixmap(self.pixmap1)
        # Включаем кнопки
        list_btn = [self.btn_1, self.btn_2, self.btn_3, self.btn_4, self.btn_5, self.btn_6, self.btn_7, self.btn_8,
                    self.btn_9, self.btn_10, self.btn_11, self.btn_12, self.btn_choice]
        for i in list_btn:
            i.clicked.connect(self.pract)

    def pract(self):
        self.p1 = Problem(self.sender().text())
        self.p1.show()


class Problem(QMainWindow):
    def __init__(self, number_btn):
        super().__init__()
        self.number_question = ''
        self.choice_list = []
        self.number_btn = number_btn  # Номер нажатой кнопки
        if self.number_btn == 'РАНДОМНЫЕ ЗАДАНИЯ':
            for i in range(1, 13):
                for j in range(1, 13):
                    if i > 9:
                        self.choice_list.append(str(i) + '.' + str(j))
                    else:
                        self.choice_list.append('0' + str(i) + '.' + str(j))
            uic.loadUi('problem_choice.ui', self)
            self.setWindowTitle('Случайные задачи')
        else:
            self.number_btn = self.number_btn.split()[0]
            for i in range(1, 31):
                if int(self.number_btn) > 9:
                    self.choice_list.append(self.number_btn + '.' + str(i))
                else:
                    self.choice_list.append('0' + self.number_btn + '.' + str(i))
            uic.loadUi('problem_' + self.number_btn + '.ui', self)
            self.setWindowTitle('Решение задач')
        self.color = QPixmap('color.png')
        self.color_fon.setPixmap(self.color)
        self.doing_problem()
        self.btn_ok_p1.clicked.connect(self.answer)
        self.btn_next_p1.clicked.connect(self.doing_problem)
        self.btn_repeat.clicked.connect(self.repeatition)

    def repeatition(self):  # Кнопка "оставить на повторение"
        self.choice_list.append(self.number_question)

    def doing_problem(self):  # Ищем пример из базы
        if len(self.choice_list) == 0:  # Если решили все примеры
            self.pixmap = QPixmap('congratilation.png')
            self.problem_1.setPixmap(self.pixmap)
        else:
            self.number_question = choice(self.choice_list)
            del self.choice_list[self.choice_list.index(self.number_question)]
            self.pixmap = QPixmap('photo/' + self.number_question + '.png')
            self.problem_1.setPixmap(self.pixmap)

    def answer(self):  # Проверка ответа
        text = self.ans_p1.text()  # Получим текст из поля ввода
        if text == answer_p[self.number_question]:
            self.pixmap1 = QPixmap('true.jpg')
            self.t_or_f_p1.setPixmap(self.pixmap1)
        else:
            self.pixmap2 = QPixmap('false.jpg')
            self.t_or_f_p1.setPixmap(self.pixmap2)


class Decision(QMainWindow):  # Ответы на все примеры
    def __init__(self):
        super().__init__()
        uic.loadUi('decision.ui', self)
        self.color = QPixmap('color_fon2.png')
        self.color_fon.setPixmap(self.color)
        self.setWindowTitle('Ответы')
        self.btn_ok.clicked.connect(self.check)

    def check(self):
        n1 = self.number_1.text()
        n2 = self.number_2.text()
        if n1 + "." + n2 in answer_p.keys() or '0' + n1 + "." + n2 in answer_p.keys():
            self.pixmap1 = QPixmap('correct.png')
            self.correct.setPixmap(self.pixmap1)
            if int(n1) > 9:
                self.main_decision = QPixmap('photo_practice/' + 'p' + n1 + '.' + n2 + '.png')
                self.fon_problem.setPixmap(self.main_decision)
            else:
                self.main_decision = QPixmap('photo_practice/' + 'p' + '0' + n1 + '.' + n2 + '.png')
                self.fon_problem.setPixmap(self.main_decision)
        else:
            self.pixmap2 = QPixmap('nocorrect.png')
            self.correct.setPixmap(self.pixmap2)


class Graph(QMainWindow):  # Построение графиков
    def __init__(self):
        super().__init__()
        uic.loadUi('graph.ui', self)
        self.setWindowTitle('Графики')
        self.a = []
        self.b = []
        self.btn_create.clicked.connect(self.run1)
        self.group.buttonClicked.connect(self.run)

    def run(self, rb):
        self.a = []
        self.b = []
        if rb.text() == '&y=x':
            for i in range(-500, 500, 1):
                self.a.append(i)
                self.b.append(i)
        if rb.text() == 'y=&x^2':
            for i in range(-100, 100, 1):
                self.a.append(i)
                self.b.append(i ** 2)
        if rb.text() == 'y=x^&3':
            for i in range(-150, 150, 1):
                self.a.append(i)
                self.b.append(i ** 3)
        if rb.text() == 'y = &sin(x)':
            for i in range(-5, 5, 1):
                for j in range(10):
                    self.a.append(i + j / 10)
                    self.b.append(math.sin(i + j / 10))
        if rb.text() == 'y=&cos(x)':
            for i in range(-5, 5, 1):
                for j in range(10):
                    self.a.append(i + j / 10)
                    self.b.append(math.cos(i + j / 10))
        if rb.text() == 'y=&1/x':
            for i in range(-150, 150, 1):
                if i != 0:
                    self.a.append(i)
                    self.a.append(i + 0.5)
                    self.b.append(1 / i)
                    self.b.append(1 / (i + 0.5))
        if rb.text() == 'y=|x|':
            for i in range(-500, 500, 1):
                self.a.append(i)
                self.b.append(abs(i))
        if rb.text() == 'y=√x':
            for i in range(0, 500, 1):
                self.a.append(i)
                self.b.append(math.sqrt(i))
        if rb.text() == 'y = const':
            for i in range(-100, 100, 1):
                self.a.append(i)
                self.b.append(5)

    def run1(self):
        self.graph.clear()
        self.graph.plot(self.a, self.b, pen='r')


# Словарь из заданий и ответов к ним
answer_p = {'01.1': '10675', '01.2': '7', '01.3': '4', '01.4': '3300', '01.5': '133', '01.6': '3000',
            '01.7': '10800', '01.8': '21', '01.9': '12', '01.10': '5', '01.11': '9,2', '01.12': '9',
            '01.13': '25200', '01.14': '20', '01.15': '6', '01.16': '4', '01.17': '10370', '01.18': '10',
            '01.19': '25', '01.20': '44', '01.21': '0,9', '01.22': '90', '01.23': '20', '01.24': '6',
            '01.25': '8', '01.26': '22,7', '01.27': '8', '01.28': '15225', '01.29': '20', '01.30': '320',

            '02.1': '25', '02.2': '6', '02.3': '72', '02.4': '18', '02.5': '7', '02.6': '28',
            '02.7': '9', '02.8': '4', '02.9': '70000', '02.10': '465', '02.11': '3150000', '02.12': '50',
            '02.13': '8', '02.14': '13', '02.15': '7', '02.16': '12', '02.17': '6', '02.18': '40',
            '02.19': '12', '02.20': '24', '02.21': '4', '02.22': '6', '02.23': '2', '02.24': '8085',
            '02.25': '8', '02.26': '3', '02.27': '13500', '02.28': '10', '02.29': '9', '02.30': '650000',

            '03.1': '6', '03.2': '6', '03.3': '6', '03.4': '45', '03.5': '40', '03.6': '7',
            '03.7': '8', '03.8': '15', '03.9': '3', '03.10': '68', '03.11': '12', '03.12': '7.5',
            '03.13': '28', '03.14': '10', '03.15': '6', '03.16': '36', '03.17': '2', '03.18': '2',
            '03.19': '96', '03.20': '8', '03.21': '153', '03.22': '27', '03.23': '0.8', '03.24': '8',
            '03.25': '14', '03.26': '25.5', '03.27': '5', '03.28': '3', '03.29': '4', '03.30': '17.5',

            '04.1': '0.09', '04.2': '0.52', '04.3': '0.4', '04.4': '0.28', '04.5': '0.008', '04.6': '3',
            '04.7': '0.72', '04.8': '0.17', '04.9': '0.125', '04.10': '0.25', '04.11': '0.125', '04.12': '0.0545',
            '04.13': '0.375', '04.14': '0.91', '04.15': '0.9', '04.16': '0.9991', '04.17': '0.21', '04.18': '0.3',
            '04.19': '0.16', '04.20': '0.02', '04.21': '0.0625', '04.22': '0.25', '04.23': '0.23', '04.24': '0.0294',
            '04.25': '0.25', '04.26': '0.75', '04.27': '0.25', '04.28': '0.035', '04.29': '0.8836', '04.30': '0.2',

            '05.1': '5', '05.2': '-4', '05.3': '2', '05.4': '12.5', '05.5': '-1.5', '05.6': '-1',
            '05.7': '-10', '05.8': '-2', '05.9': '13', '05.10': '-0.4', '05.11': '-0.2', '05.12': '1',
            '05.13': '-124', '05.14': '4', '05.15': '5', '05.16': '-80', '05.17': '0', '05.18': '1',
            '05.19': '-42', '05.20': '30', '05.21': '9.5', '05.22': '-6.5', '05.23': '3.5', '05.24': '-5',
            '05.25': '31', '05.26': '2', '05.27': '13.4', '05.28': '-94', '05.29': '-4', '05.30': '3',

            '06.1': '2', '06.2': '105', '06.3': '1', '06.4': '40', '06.5': '4.8', '06.6': '49',
            '06.7': '57', '06.8': '120', '06.9': '64', '06.10': '110.25', '06.11': '48', '06.12': '65',
            '06.13': '30', '06.14': '40', '06.15': '49', '06.16': '28', '06.17': '60', '06.18': '58',
            '06.19': '74', '06.20': '8', '06.21': '58', '06.22': '4', '06.23': '3.2', '06.24': '4',
            '06.25': '104', '06.26': '152', '06.27': '160', '06.28': '24', '06.29': '9.6', '06.30': '56',

            '07.1': '-5', '07.2': '6', '07.3': '-3', '07.4': '7', '07.5': '44', '07.6': '3',
            '07.7': '3', '07.8': '3', '07.9': '-1.25', '07.10': '6', '07.11': '-2', '07.12': '7',
            '07.13': '2', '07.14': '-33', '07.15': '1', '07.16': '-5', '07.17': '-8', '07.18': '12',
            '07.19': '14', '07.20': '2.7', '07.21': '5', '07.22': '4', '07.23': '39', '07.24': '4',
            '07.25': '5', '07.26': '6.75', '07.27': '-19', '07.28': '20', '07.29': '5', '07.30': '7',

            '08.1': '17', '08.2': '72', '08.3': '7', '08.4': '0.95', '08.5': '140', '08.6': '10',
            '08.7': '9', '08.8': '94', '08.9': '64', '08.10': '54', '08.11': '2744', '08.12': '1.28',
            '08.13': '120', '08.14': '2304', '08.15': '12', '08.16': '12', '08.17': '130', '08.18': '5',
            '08.19': '8', '08.20': '33', '08.21': '34', '08.22': '3375', '08.23': '7', '08.24': '196',
            '08.25': '102', '08.26': '20', '08.27': '4', '08.28': '2', '08.29': '2', '08.30': '18',

            '09.1': '4', '09.2': '49', '09.3': '-34', '09.4': '2', '09.5': '-3', '09.6': '1',
            '09.7': '32', '09.8': '20', '09.9': '5', '09.10': '-22', '09.11': '46', '09.12': '5',
            '09.13': '-7', '09.14': '2', '09.15': '27', '09.16': '3.75', '09.17': '12', '09.18': '13.5',
            '09.19': '8', '09.20': '-16', '09.21': '-94', '09.22': '1', '09.23': '-9', '09.24': '6.4',
            '09.25': '3', '09.26': '5', '09.27': '1', '09.28': '2', '09.29': '6', '09.30': '702',

            '10.1': '180000', '10.2': '8.8', '10.3': '15', '10.4': '2', '10.5': '0.8', '10.6': '6',
            '10.7': '4.5', '10.8': '4000', '10.9': '0.2', '10.10': '22.2', '10.11': '0.75', '10.12': '3',
            '10.13': '3.5', '10.14': '16000', '10.15': '60', '10.16': '37.5', '10.17': '3', '10.18': '30',
            '10.19': '117', '10.20': '1.4', '10.21': '35', '10.22': '34', '10.23': '5', '10.24': '4',
            '10.25': '62.5', '10.26': '0.012', '10.27': '4.4', '10.28': '400', '10.29': '6', '10.30': '8',

            '11.1': '23', '11.2': '32', '11.3': '17', '11.4': '18', '11.5': '24', '11.6': '99',
            '11.7': '44036', '11.8': '150', '11.9': '3', '11.10': '35', '11.11': '15', '11.12': '96',
            '11.13': '24', '11.14': '55', '11.15': '60', '11.16': '10', '11.17': '320000', '11.18': '62',
            '11.19': '3', '11.20': '4', '11.21': '10', '11.22': '342', '11.23': '11', '11.24': '20',
            '11.25': '18', '11.26': '5', '11.27': '9', '11.28': '25', '11.29': '8', '11.30': '30',

            '12.1': '2', '12.2': '20', '12.3': '5', '12.4': '3', '12.5': '10', '12.6': '-11',
            '12.7': '1', '12.8': '20', '12.9': '8', '12.10': '73', '12.11': '7', '12.12': '15',
            '12.13': '-15', '12.14': '7', '12.15': '-14', '12.16': '13', '12.17': '9', '12.18': '-3',
            '12.19': '14', '12.20': '-2', '12.21': '29', '12.22': '-1', '12.23': '10', '12.24': '5',
            '12.25': '74', '12.26': '256', '12.27': '43', '12.28': '-3.25', '12.29': '4', '12.30': '10'}


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main_program()
    ex.show()
    sys.exit(app.exec())