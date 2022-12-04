# -*- coding: UTF-8 -*-
import csv
import sys

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtGui import QPixmap, QPalette, QColor
from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtWidgets import QTableWidgetItem
from random import randint
from datetime import timedelta, datetime


class MainMenu(QMainWindow):  # Главное меню
    def __init__(self):
        super().__init__()
        uic.loadUi('Главное_меню.ui', self)
        self.setWindowTitle('Меню')
        self.Play.clicked.connect(self.inputdata)
        self.Rules.clicked.connect(self.rulesmenu)
        self.Records.clicked.connect(self.recordstable)
        self.QuitGame.clicked.connect(self.gameend)
        self.game = MainGame()
        self.rule = RulesWindow()
        self.record = RecordTableWindow()

    def inputdata(self):  # Начало игры
        self.name, ok_pressed = QInputDialog.getText(self, "Введите имя",
                                                "Как тебя зовут?")
        if ok_pressed:  # Успешно ввели имя
            self.difficulty, ok_pressed = QInputDialog.getItem(
                self, "Выберите сложность игры", "Выбери сложность игры: ",
                ("Лёгкая", "Сложная", "Хардкор"), 1, False)
            if ok_pressed:
                self.game = MainGame(self.name, self.difficulty)  # Успешно выбрали сложность
                self.game.show()

    def rulesmenu(self):
        self.rule = RulesWindow()# Открываем меню правил
        self.rule.show()

    def recordstable(self):
        self.record = RecordTableWindow()# Открываем таблицу рекордов
        self.record.show()

    def returntothemenu(self):
        self.game.close()
        self.rule.close()
        self.record.close()

    def gameend(self):  # Закрываем игру
        menu.close()
        self.returntothemenu()


class MainGame(QMainWindow):  # Сама игра
    def __init__(self, name=' ', difficulty='лёгкая'):
        super().__init__()
        uic.loadUi('Главная_игра.ui', self)
        self.setWindowTitle('Игра')
        self.name = name
        self.difficulty = difficulty
        self.QuitGame.clicked.connect(self.gameend)
        self.monitors = ['self.Tenth', 'self.Ninth', 'self.Eighth', 'self.Seventh', 'self.Sixth', 'self.Fifth',
                         'self.Fourth', 'self.Third', 'self.Second', 'self.First', 'self.Zero']
        self.powers = list(reversed([2 ** i for i in range(11)]))
        self.lifecount = 3
        self.showlife = '♥' * self.lifecount
        self.Lives.setText(self.showlife)
        if self.difficulty == 'Лёгкая':
            self.timegiven = 10
            self.points = 10
        elif self.difficulty == 'Сложная':
            self.timegiven = 7
            self.points = 20
        else:
            self.timegiven = 3
            self.points = 60
        self.currentpoints = 0
        self.Count.display(self.currentpoints)
        for i in self.buttonGroup.buttons():
            i.setEnabled(False)
        [btn.clicked.connect(
            self.countleft) for btn in self.buttonGroup.buttons()]
        self.Start.clicked.connect(self.startnew)
        self.Reset.clicked.connect(self.startnew)
        self.Reset.clicked.connect(self.minuslife)

    def startnew(self):
        self.Start.setEnabled(False)
        self.timer = QTimer()
        self.timer.stop()
        self.timer.timeout.connect(self.onTimeout)
        self.timer.start(1000)
        self.begin = datetime.strptime(f'00:{str(self.timegiven)}', '%M:%S')
        self.statusBar().clearMessage()
        self.currentn = randint(0, 2047)
        self.n = self.currentn
        self.CurrentNumber.display(self.currentn)
        self.Left.display(self.n)
        for i in self.monitors:
            eval(i).display(0)
        for i in self.buttonGroup.buttons():
            i.setEnabled(True)


    def countleft(self):
        ind = self.buttonGroup.buttons().index(self.sender())
        power, position = self.powers[ind], self.monitors[ind]
        if self.n - power == 0:
            self.currentpoints += self.points
            self.Count.display(self.currentpoints)
            self.startnew()
        else:
            self.sender().setEnabled(False)
            if self.n - power < 0:
                self.minuslife()
                self.statusBar().showMessage('Ошибка! Остаток меньше нуля -> Вы неправильно расставили коэффициенты')
            else:
                self.n -= power
                self.Left.display(self.n)
                eval(position).display(1)
                self.statusBar().clearMessage()
        self.checklife()

    def gameend(self):  # Принудительно останавливаем игру и выходим в главное меню
        self.timer.stop()
        menu.returntothemenu()

    def onTimeout(self):
        if str(self.begin).split()[1] == '00:00:01':
            self.minuslife()
            self.timer.stop()
            self.checklife()
            self.startnew()
        self.begin = self.begin - timedelta(seconds=1)
        self.TimeLeft.display(str(self.begin))

    def minuslife(self):
        self.lifecount -= 1
        self.showlife = '♥' * self.lifecount
        self.Lives.setText(self.showlife)
        self.checklife()

    def checklife(self):
        if self.lifecount == 0:
            self.end = EndWindow(self.currentpoints, self.name)
            with open('Рекорды.csv', 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([self.name, self.currentpoints, self.difficulty])
            self.end.show()
            self.gameend()


class RulesWindow(QMainWindow):  # Окно правил
    def __init__(self):
        super().__init__()
        uic.loadUi('Правила.ui', self)
        self.setWindowTitle('Правила')
        self.Transrules.clicked.connect(self.opentransrules)
        self.Gamerules.clicked.connect(self.opengamerules)
        self.Levelrules.clicked.connect(self.openlevelrules)
        self.ToMenu.clicked.connect(self.windowclose)

    def opentransrules(self):
        self.transition = TransRulesWindow()
        self.transition.show()

    def opengamerules(self):  # Открываем окно правил игры
        self.gamerules = GamerulesWindow()
        self.gamerules.show()

    def openlevelrules(self):  # Открываем окно справки об игре
        self.levelrules = LevelrulesWindow()
        self.levelrules.show()

    def windowclose(self):  # Закрываем окно правил и возвращаемся в меню
        self.close()
        menu.returntothemenu()


class TransRulesWindow(RulesWindow):  # Окно правил для перевода
    def __init__(self):
        super().__init__()
        uic.loadUi('Правила_перевода.ui', self)
        self.setWindowTitle('Правила перевода')
        self.initUI()
        self.ToMenu.clicked.connect(self.windowclose)

    def initUI(self):  # картинка-правила
        self.pixmap = QPixmap('transrules.png')
        self.image.resize(897, 433)
        self.image.setPixmap(self.pixmap)


class GamerulesWindow(RulesWindow):  # Окно правил игры
    def __init__(self):
        super().__init__()
        uic.loadUi('Правила_игры.ui', self)
        self.setWindowTitle('Правила игры для чайников')
        self.initUI()
        self.scrollArea.setBackgroundRole(QPalette.Shadow)
        self.ToMenu_2.clicked.connect(self.windowclose)

    def initUI(self):  # картинка-правила
        self.pixmap = QPixmap('gamerules.png')
        self.image.resize(747, 400)
        self.image.setPixmap(self.pixmap)


class LevelrulesWindow(RulesWindow):  # Окно справки об уровнях сложности
    def __init__(self):
        super().__init__()
        uic.loadUi('Уровни_сложности.ui', self)
        self.setWindowTitle('Уровни сложности')
        self.ToMenu.clicked.connect(self.windowclose)


class RecordTableWindow(QMainWindow):  # Окно таблицы рекордов
    def __init__(self):
        super().__init__()
        uic.loadUi('Таблица_рекордов.ui', self)
        self.setWindowTitle('Таблица рекордов')
        self.ToMenu.clicked.connect(self.windowclose)
        self.loadTable('Рекорды.csv')
        self.color_row(0, QColor(173, 255, 255))

    def loadTable(self, table_name):
        with open(table_name, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile,
                                delimiter=';', quotechar='"')
            title = next(reader)
            self.RecordTable.setColumnCount(len(title))
            self.RecordTable.setHorizontalHeaderLabels(title)
            self.RecordTable.setRowCount(0)
            for i, row in enumerate(reader):
                self.RecordTable.setRowCount(
                    self.RecordTable.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.RecordTable.setItem(
                        i, j, QTableWidgetItem(elem))
        self.RecordTable.resizeColumnsToContents()

    def color_row(self, row, color):
        for i in range(self.RecordTable.columnCount()):
            self.RecordTable.item(row, i).setBackground(color)

    def windowclose(self):  # Закрываем таблицу рекордов и возвращаемся в главное меню
        menu.returntothemenu()


class EndWindow(QMainWindow):  # Окно результата
    def __init__(self, n, name):
        super().__init__()
        uic.loadUi('Конец.ui', self)
        self.setWindowTitle('Конец')
        self.Count.display(n)
        try:
            with open('Рекорды.csv', encoding="utf8") as csvfile:
                reader = csv.DictReader(csvfile,
                                        delimiter=';', quotechar='"')
                this_user = list(filter(lambda x: x['Имя'] == name, reader))
            users_scores = [int(i['Кол-во набранных очков']) for i in this_user]
            self.Record.display(max(users_scores))
        except Exception:
            self.Record.display(0)
        self.TryAgain.clicked.connect(self.returntogame)
        self.ToMenu.clicked.connect(self.windowclose)

    def returntogame(self):  # Возвращаемся на выбор имени
        self.windowclose()
        menu.inputdata()

    def windowclose(self):  # Возвращаемся в главное меню и закрывам все остальное
        self.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    menu = MainMenu()
    menu.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
