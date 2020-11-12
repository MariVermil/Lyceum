import sys
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import *
import operator
from random import choice, randrange


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
        self.btn_calculator.clicked.connect(self.calculators)
        self.btn_oral_count.clicked.connect(self.oral_count)
        self.btn_theory.clicked.connect(self.theories)
        self.btn_practice.clicked.connect(self.practices)
        self.btn_decision.clicked.connect(self.decise)
        self.btn_randomv.clicked.connect(self.randomv)

    def calculators(self):
        self.w1 = Calculator()
        self.w1.show()

    def oral_count(self):
        self.w2 = Oral_count()
        self.w2.show()

    def theories(self):
        self.w3 = Theory()
        self.w3.show()

    def practices(self):
        self.w4 = Practice()
        self.w4.show()

    def decise(self):
        self.w5 = Decision()
        self.w5.show()

    def randomv(self):
        self.w6 = Random_variant()
        self.w6.show()


class Random_variant(QMainWindow):  # Создание рандомного варианта из 12 задач
    def __init__(self):
        super().__init__()
        self.number_question = ''
        uic.loadUi('random_varik.ui', self)
        self.color = QPixmap('color.png')
        self.color_fon.setPixmap(self.color)
        self.setWindowTitle('Случайный вариант')
        self.pointer = 0  # Указатель на то, какой сейчас вопрос решается
        self.doing_problem()
        self.ans_list = []  # Хранятся ответы пользователя
        self.btn_ok_p1.clicked.connect(self.answer)
        self.btn_next_p1.clicked.connect(self.doing_problem)

    def doing_problem(self):  # Ищем пример из базы
        if self.pointer == 12:
            self.v1 = Answer(self.ans_list)  # Выводим вердикт по решению варианта
            self.v1.show()
        else:
            self.pointer = self.pointer + 1
            self.number_question = str(randrange(1, 31))
            self.pic1 = QPixmap(str(self.pointer) + '.' + self.number_question + '.png')
            self.problems.setPixmap(self.pic1)

    def answer(self):  # Проверка ответа
        text = self.ans_p1.text()  # Получим текст из поля ввода
        if text == answer_p[str(self.pointer) + '.' + self.number_question]:
            self.ans_list.append([str(self.pointer) + '.' + self.number_question, 'Правильно'])
        else:
            self.ans_list.append([str(self.pointer) + '.' + self.number_question, 'Неправильно'])


class Answer(QMainWindow):  # Вывод вердикта
    def __init__(self, ans_list):
        super().__init__()
        self.ans_list = ans_list
        uic.loadUi('answer.ui', self)
        self.setWindowTitle('Вердикт')
        self.label_1.setText(self.ans_list[0][0] + ' вопрос: ' + self.ans_list[0][1])
        self.label_2.setText(self.ans_list[1][0] + ' вопрос: ' + self.ans_list[1][1])
        self.label_3.setText(self.ans_list[2][0] + ' вопрос: ' + self.ans_list[2][1])
        self.label_4.setText(self.ans_list[3][0] + ' вопрос: ' + self.ans_list[3][1])
        self.label_5.setText(self.ans_list[4][0] + ' вопрос: ' + self.ans_list[4][1])
        self.label_6.setText(self.ans_list[5][0] + ' вопрос: ' + self.ans_list[5][1])
        self.label_7.setText(self.ans_list[6][0] + ' вопрос: ' + self.ans_list[6][1])
        self.label_8.setText(self.ans_list[7][0] + ' вопрос: ' + self.ans_list[7][1])
        self.label_9.setText(self.ans_list[8][0] + ' вопрос: ' + self.ans_list[8][1])
        self.label_10.setText(self.ans_list[9][0] + ' вопрос: ' + self.ans_list[9][1])
        self.label_11.setText(self.ans_list[10][0] + ' вопрос: ' + self.ans_list[10][1])
        self.label_12.setText(self.ans_list[11][0] + ' вопрос: ' + self.ans_list[11][1])


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
        self.btn_1.clicked.connect(self.theor)
        self.btn_2.clicked.connect(self.theor)
        self.btn_3.clicked.connect(self.theor)
        self.btn_4.clicked.connect(self.theor)
        self.btn_5.clicked.connect(self.theor)
        self.btn_6.clicked.connect(self.theor)
        self.btn_7.clicked.connect(self.theor)
        self.btn_8.clicked.connect(self.theor)
        self.btn_9.clicked.connect(self.theor)
        self.btn_10.clicked.connect(self.theor)
        self.btn_11.clicked.connect(self.theor)
        self.btn_12.clicked.connect(self.theor)

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
        self.tr = QPixmap('t' + self.number_btn + '.1' + '.png')
        self.theories.setPixmap(self.tr)
        self.pointer = 1  # Указатель на номер страницы теории
        self.btn_back.clicked.connect(self.moving_back)
        self.btn_next.clicked.connect(self.moving_next)

    def moving_back(self):  # Вернуться к прошлой странице
        if self.pointer > 1:
            self.pointer = self.pointer - 1
            self.pic_back = QPixmap('t' + self.number_btn + '.' + str(self.pointer) + '.png')
            self.theories.setPixmap(self.pic_back)

    def moving_next(self):  # Пройти на следующую строку
        # Обрабатываем для разных кнопок по-разному, тк у них разное кол-во страниц
        if self.number_btn == '1':
            if self.pointer < 6:
                self.pointer = self.pointer + 1
                self.pic_next = QPixmap('t1' + '.' + str(self.pointer) + '.png')
                self.theories.setPixmap(self.pic_next)
        if self.number_btn == '2':
            if self.pointer < 5:
                self.pointer = self.pointer + 1
                self.pic_next = QPixmap('t2' + '.' + str(self.pointer) + '.png')
                self.theories.setPixmap(self.pic_next)
        if self.number_btn == '3':
            if self.pointer < 5:
                self.pointer = self.pointer + 1
                self.pic_next = QPixmap('t3' + '.' + str(self.pointer) + '.png')
                self.theories.setPixmap(self.pic_next)
        if self.number_btn == '4':
            if self.pointer < 12:
                self.pointer = self.pointer + 1
                self.pic_next = QPixmap('t4' + '.' + str(self.pointer) + '.png')
                self.theories.setPixmap(self.pic_next)
        if self.number_btn == '5':
            if self.pointer < 14:
                self.pointer = self.pointer + 1
                self.pic_next = QPixmap('t5' + '.' + str(self.pointer) + '.png')
                self.theories.setPixmap(self.pic_next)
        if self.number_btn == '6':
            if self.pointer < 51:
                self.pointer = self.pointer + 1
                self.pic_next = QPixmap('t6' + '.' + str(self.pointer) + '.png')
                self.theories.setPixmap(self.pic_next)
        if self.number_btn == '7':
            if self.pointer < 15:
                self.pointer = self.pointer + 1
                self.pic_next = QPixmap('t7' + '.' + str(self.pointer) + '.png')
                self.theories.setPixmap(self.pic_next)
        if self.number_btn == '8':
            if self.pointer < 13:
                self.pointer = self.pointer + 1
                self.pic_next = QPixmap('t8' + '.' + str(self.pointer) + '.png')
                self.theories.setPixmap(self.pic_next)
        if self.number_btn == '9':
            if self.pointer < 25:
                self.pointer = self.pointer + 1
                self.pic_next = QPixmap('t9' + '.' + str(self.pointer) + '.png')
                self.theories.setPixmap(self.pic_next)
        if self.number_btn == '10':
            if self.pointer < 7:
                self.pointer = self.pointer + 1
                self.pic_next = QPixmap('t10' + '.' + str(self.pointer) + '.png')
                self.theories.setPixmap(self.pic_next)
        if self.number_btn == '11':
            if self.pointer < 8:
                self.pointer = self.pointer + 1
                self.pic_next = QPixmap('t11' + '.' + str(self.pointer) + '.png')
                self.theories.setPixmap(self.pic_next)
        if self.number_btn == '12':
            if self.pointer < 11:
                self.pointer = self.pointer + 1
                self.pic_next = QPixmap('t12' + '.' + str(self.pointer) + '.png')
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
        self.btn_1.clicked.connect(self.pract)
        self.btn_2.clicked.connect(self.pract)
        self.btn_3.clicked.connect(self.pract)
        self.btn_4.clicked.connect(self.pract)
        self.btn_5.clicked.connect(self.pract)
        self.btn_6.clicked.connect(self.pract)
        self.btn_7.clicked.connect(self.pract)
        self.btn_8.clicked.connect(self.pract)
        self.btn_9.clicked.connect(self.pract)
        self.btn_10.clicked.connect(self.pract)
        self.btn_11.clicked.connect(self.pract)
        self.btn_12.clicked.connect(self.pract)
        self.btn_choice.clicked.connect(self.pract_choice)

    def pract(self):
        self.p1 = Problem(self.sender().text())
        self.p1.show()

    def pract_choice(self):
        self.pc = Problem_choice()
        self.pc.show()


class Problem(QMainWindow):
    def __init__(self, number_btn):
        super().__init__()
        self.number_question = 1
        self.choice_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                            26, 27, 28, 29, 30]
        self.number_btn = number_btn  # Номер нажатой кнопки
        self.number_btn = self.number_btn.split()[0]
        uic.loadUi('problem_' + self.number_btn + '.ui', self)
        self.color = QPixmap('color.png')
        self.color_fon.setPixmap(self.color)
        self.setWindowTitle('Решение задач')
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
            self.pixmap = QPixmap(self.number_btn + '.' + str(self.number_question) + '.png')
            self.problem_1.setPixmap(self.pixmap)

    def answer(self):  # Проверка ответа
        text = self.ans_p1.text()  # Получим текст из поля ввода
        if text == answer_p[self.number_btn + '.' + str(self.number_question)]:
            self.pixmap1 = QPixmap('true.jpg')
            self.t_or_f_p1.setPixmap(self.pixmap1)
        else:
            self.pixmap2 = QPixmap('false.jpg')
            self.t_or_f_p1.setPixmap(self.pixmap2)


class Problem_choice(QMainWindow):  # Рандомные примеры
    def __init__(self):
        super().__init__()
        self.number_question = ''
        self.choice_list = []  # Всеразличные примеры
        for i in range(1, 13):
            for j in range(1, 13):
                self.choice_list.append(str(i) + '.' + str(j))
        uic.loadUi('problem_choice.ui', self)
        self.color = QPixmap('color.png')
        self.color_fon.setPixmap(self.color)
        self.setWindowTitle('Случайные задачи')
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
            self.pixmap = QPixmap(self.number_question + '.png')
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
        if n1 + "." + n2 in answer_p.keys():
            self.pixmap1 = QPixmap('correct.png')
            self.correct.setPixmap(self.pixmap1)
            self.main_decision = QPixmap('r' + n1 + '.' + n2 + '.png')
            self.fon_problem.setPixmap(self.main_decision)
        else:
            self.pixmap2 = QPixmap('nocorrect.png')
            self.correct.setPixmap(self.pixmap2)


# Словарь из заданий и ответов к ним
answer_p = {'1.1': '10675', '1.2': '7', '1.3': '4', '1.4': '3300', '1.5': '133', '1.6': '3000',
            '1.7': '10800', '1.8': '21', '1.9': '12', '1.10': '5', '1.11': '9,2', '1.12': '9',
            '1.13': '25200', '1.14': '20', '1.15': '6', '1.16': '4', '1.17': '10370', '1.18': '10',
            '1.19': '25', '1.20': '44', '1.21': '0,9', '1.22': '90', '1.23': '20', '1.24': '6',
            '1.25': '8', '1.26': '22,7', '1.27': '8', '1.28': '15225', '1.29': '20', '1.30': '320',

            '2.1': '25', '2.2': '6', '2.3': '72', '2.4': '18', '2.5': '7', '2.6': '28',
            '2.7': '9', '2.8': '4', '2.9': '70000', '2.10': '465', '2.11': '3150000', '2.12': '50',
            '2.13': '8', '2.14': '13', '2.15': '7', '2.16': '12', '2.17': '6', '2.18': '40',
            '2.19': '12', '2.20': '24', '2.21': '4', '2.22': '6', '2.23': '2', '2.24': '8085',
            '2.25': '8', '2.26': '3', '2.27': '13500', '2.28': '10', '2.29': '9', '2.30': '650000',
            '3.1': '6', '3.2': '6', '3.3': '6', '3.4': '45', '3.5': '40', '3.6': '7',

            '3.7': '8', '3.8': '15', '3.9': '3', '3.10': '68', '3.11': '12', '3.12': '7.5',
            '3.13': '28', '3.14': '10', '3.15': '6', '3.16': '36', '3.17': '2', '3.18': '2',
            '3.19': '96', '3.20': '8', '3.21': '153', '3.22': '27', '3.23': '0.8', '3.24': '8',
            '3.25': '14', '3.26': '25.5', '3.27': '5', '3.28': '3', '3.29': '4', '3.30': '17.5',

            '4.1': '0.09', '4.2': '0.52', '4.3': '0.4', '4.4': '0.28', '4.5': '0.008', '4.6': '3',
            '4.7': '0.72', '4.8': '0.17', '4.9': '0.125', '4.10': '0.25', '4.11': '0.125', '4.12': '0.0545',
            '4.13': '0.375', '4.14': '0.91', '4.15': '0.9', '4.16': '0.9991', '4.17': '0.21', '4.18': '0.3',
            '4.19': '0.16', '4.20': '0.02', '4.21': '0.0625', '4.22': '0.25', '4.23': '0.23', '4.24': '0.0294',
            '4.25': '0.25', '4.26': '0.75', '4.27': '0.25', '4.28': '0.035', '4.29': '0.8836', '4.30': '0.2',

            '5.1': '5', '5.2': '-4', '5.3': '2', '5.4': '12.5', '5.5': '-1.5', '5.6': '-1',
            '5.7': '-10', '5.8': '-2', '5.9': '13', '5.10': '-0.4', '5.11': '-0.2', '5.12': '1',
            '5.13': '-124', '5.14': '4', '5.15': '5', '5.16': '-80', '5.17': '0', '5.18': '1',
            '5.19': '-42', '5.20': '30', '5.21': '9.5', '5.22': '-6.5', '5.23': '3.5', '5.24': '-5',
            '5.25': '31', '5.26': '2', '5.27': '13.4', '5.28': '-94', '5.29': '-4', '5.30': '3',

            '6.1': '2', '6.2': '105', '6.3': '1', '6.4': '40', '6.5': '4.8', '6.6': '49',
            '6.7': '57', '6.8': '120', '6.9': '64', '6.10': '110.25', '6.11': '48', '6.12': '65',
            '6.13': '30', '6.14': '40', '6.15': '49', '6.16': '28', '6.17': '60', '6.18': '58',
            '6.19': '74', '6.20': '8', '6.21': '58', '6.22': '4', '6.23': '3.2', '6.24': '4',
            '6.25': '104', '6.26': '152', '6.27': '160', '6.28': '24', '6.29': '9.6', '6.30': '56',

            '7.1': '-5', '7.2': '6', '7.3': '-3', '7.4': '7', '7.5': '44', '7.6': '3',
            '7.7': '3', '7.8': '3', '7.9': '-1.25', '7.10': '6', '7.11': '-2', '7.12': '7',
            '7.13': '2', '7.14': '-33', '7.15': '1', '7.16': '-5', '7.17': '-8', '7.18': '12',
            '7.19': '14', '7.20': '2.7', '7.21': '5', '7.22': '4', '7.23': '39', '7.24': '4',
            '7.25': '5', '7.26': '6.75', '7.27': '-19', '7.28': '20', '7.29': '5', '7.30': '7',

            '8.1': '17', '8.2': '72', '8.3': '7', '8.4': '0.95', '8.5': '140', '8.6': '10',
            '8.7': '9', '8.8': '94', '8.9': '64', '8.10': '54', '8.11': '2744', '8.12': '1.28',
            '8.13': '120', '8.14': '2304', '8.15': '12', '8.16': '12', '8.17': '130', '8.18': '5',
            '8.19': '8', '8.20': '33', '8.21': '34', '8.22': '3375', '8.23': '7', '8.24': '196',
            '8.25': '102', '8.26': '20', '8.27': '4', '8.28': '2', '8.29': '2', '8.30': '18',

            '9.1': '4', '9.2': '49', '9.3': '-34', '9.4': '2', '9.5': '-3', '9.6': '1',
            '9.7': '32', '9.8': '20', '9.9': '5', '9.10': '-22', '9.11': '46', '9.12': '5',
            '9.13': '-7', '9.14': '2', '9.15': '27', '9.16': '3.75', '9.17': '12', '9.18': '13.5',
            '9.19': '8', '9.20': '-16', '9.21': '-94', '9.22': '1', '9.23': '-9', '9.24': '6.4',
            '9.25': '3', '9.26': '5', '9.27': '1', '9.28': '2', '9.29': '6', '9.30': '702',

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
