# -*- coding: utf-8 -*-
import os
import sys
sys.path.append('Logic')
sys.path.append('module')
#import Analitic as analit

import time, datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

import Logic

from JobBD import JobBD
import engine as block1

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Program(QMainWindow):

    def __init__(self):

        super().__init__()

        self._variables()
        self.block1 = block1.block1()
        self.data = self.block1.returnData()

        #Получение графиков
        self.canvas_1 = self.data['FormUI'][2].Main.canvas #Линейный график
        self.canvas_2 = self.data['FormUI'][2].Main.canvas2 #Круговой график деления
        

        self.data['Form'].resize(700, 450)
        self.data['Form_2'].resize(350, 450)
        self.data['Form'].setCurrentIndex(0)

        self._logicButton()
        self._logicComboBox()

        self.data['table'][3][0].setContextMenuPolicy(Qt.CustomContextMenu)
        self.data['table'][3][0].customContextMenuRequested.connect(self._RazvertKontectMenu)

        self._perechod(0)

    '''
    self.button; self.label... Переменные где хранятся кнопки и надписи
    0 - Индетификация
    1 - Главное меню
    2 - Аналитика
    3 - Посмотреть квитанцию
    4 - Статистика
    5 - Добавить квитанцию
    6 - Отдельное окно оповещение
    7 - Создать новый адрес
    8 - Удалить адрес
    9 - Выбор адреса для удаления
    10 - Удалить адрес
    
    self.data['Form']UI Формы для перехода
    0 - Индетификация
    1 - Главное меню
    2 - Окно аналитики
    3 - Посмотреть квитанцию
    4 - Статистика

    self.data['Form']IU_2 Формы для отдельного окна
    0 - Добавить квитанцию
    1 - Отдельное окно оповещение
    2 - Создать новый адрес
    3 - Удалить адрес
    4 - Выбор адреса для удаления
    5 - Удалить адрес
    '''
    #---------------------------------------------------------------------------------------------
    #ДЕКОРАТОРЫ
    def timeCheck(func):

        def decor(*arg):
            time_old = time.time()
            a = func(*arg)
            time_new = time.time() - time_old
            print(f'Время выполнения: {round(time_new, 3)}')
            return a
        
        return decor

    #---------------------------------------------------------------------------------------------
    #ЛОГИКА

    def _variables(self):

        #Модуль основных алгоритмов
        self.Logic = Logic.Logic()

        #Модуль работы с данными
        self.JobFile = Logic.JobFile()

        #Проверка состояния файлов db и json
        self.JobFile.checkStartForm()

        #Для работы с бд
        self.JobBD = JobBD()

        #Модуль аналитики
        self.Analitic = None

        #Данные аналитики
        self.DataAnalitic = None

        self.activListWidget = False #Была ли нажата кнопка в qlistwidget в выборе удаления адреса

        #Старые данные с config
        self.old_data = self.JobFile.returnOldData()

        #Выбранный индекс в таблице
        #self.index = None
        self.indexCombobox = None #(index, text)

        #Получение графики
        self.canvas_1 = None #Линейный график
        self.canvas_2 = None #Круговой график деления

        #Фигуры у графиков
        self.ax1 = None
        self.ax2 = None

        #Было ли измененик окна в маштабировании
        self.scale = False

        #Тригер который показывает что график обновлялся не в первый раз
        self.trigerGrafic = False


        #Координаты таблицы
        #self.cordTable = None

    #Переходы
    def _perechod(self, index: int):
        self.data['Form'].setCurrentIndex(index)
        self.data['Form'].setWindowTitle(self.data['title'][index])
        self.data['Form'].closeEvent = lambda event: self.exitMain_1(event)
        self.data['Form'].resizeEvent = lambda event: self.resizeEvent(event)
        self.data['Form'].show()
    
    #Переходы для отдельных окон
    def _perechod_2(self, index: int):

        self.data['Form_2'].setCurrentIndex(index)

        if index in (1, 2, 3):
            self.data['Form_2'].setMinimumSize(QSize(320, 350))
            self.data['Form_2'].setMaximumSize(QSize(480, 600))
            #Устанавливаем на цент экрана
            xy = self.centerWindow()
            self.data['Form_2'].move(xy[0]-(self.data['Form_2'].width() // 2), xy[1]-(self.data['Form_2'].height() // 2))

        elif index in (0, 7):
            self.data['Form_2'].setMinimumSize(QSize(660, 430))
            self.data['Form_2'].setMaximumSize(QSize(2000, 2000))
            self.data['Form_2'].resize(660, 430)

        else:
            self.data['Form_2'].setMinimumSize(QSize(340, 150))
            self.data['Form_2'].setMaximumSize(QSize(400, 180))

            #Устанавливаем на цент экрана
            xy = self.centerWindow()
            self.data['Form_2'].move(xy[0]-(self.data['Form_2'].width() // 2), xy[1]-(self.data['Form_2'].height() // 2))

        self.data['Form_2'].setWindowTitle(self.data['title_2'][index])
        self.data['Form_2'].closeEvent = lambda event: self.exitMain(event)

        self.data['Form_2'].show()
    
    #Получение середину экрана
    def centerWindow(self):
        screen = QDesktopWidget(); screen = screen.screenGeometry()
        center_x = screen.width() // 2
        center_y = screen.height() // 2
        return center_x, center_y
    
    #Обработка изменения размеров окна
    def resizeEvent(self, event):
        self._someFunction()
        return super().resizeEvent(event)

    #Метод реакции на изменение окна
    def _someFunction(self):
        #Шаблоны
        #Стандартные стили
        def defoult():
            
            #Индетифитикация
            indetif = '''QWidget{background: #141529;}\n
            QPushButton{background-color: #595973; color: white; font-family: Consolas; font-size: 12px; border-radius: 2px;}\n
            QComboBox{background-color: white; border: none; font-size: 14px; font-family: Consolas; padding-left: 7px;}\n
            QLabel{color: white; font-size: 14px; font-family: Consolas;}\n
            \n
            QPushButton::hover{background-color: #2D2F5C;}\n
            QPushButton::pressed{background-color: #44478B;}\n
            \n
            #label{font-size: 16px;}\n
            QComboBox::drop-down{image: url(C:/Users/Mike2/OneDrive/Рабочий стол/Отчетность коммунальных платежей/icon/srelka.png); width: 11px; height: 11px; border: none; padding-right: 3px; padding-top: 3px;}\n
            QComboBox QAbstractItemView {background-color: white; padding-left: 4px;}\n'''

            #Главное меню
            gl_main = '''QWidget{background: #141529;}\n
            QPushButton{border: none; text-align: left; color: white; font-family: Consolas;}\n
            QLabel{color: white; font-size: 11px; font-family: Consolas;}\n
            #label_2 {background-color: #1F2035; border: none; border-bottom: 1px solid; color: white; font-family: Consolas; fon-size: 14px}\n
            \n
            QPushButton::hover{background-color: #2D2F5C}\n
            QPushButton::pressed{background-color: #44478B}\n
            \n
            \n
            #frame_2, #frame, #frame QPushButton, #frame_2 QLabel{background: #1F2035; padding-left: 3px;}\n
            #frame QPushButton::hover{background-color: #2D2F5C;}\n
            #frame QPushButton::pressed{background-color: #44478B;}\n
            /*----------------------------------------------------------------------*/\n
            #frame_3, #frame_5, #frame_6 {background-color: #27274B;}\n
            \n
            #label_5, #label_7, #label_9 {background-color: none; font-size: 20px;}\n
            \n
            #label_6, #label_8, #label_10 {font-size: 23px; background: none; font-weight: bold; color: #08DA9D;}\n
            \n
            #label_3 {font-size: 28px; font-weight: bold;}\n
            #label_4 {font-size: 18px; font-weight: bold;}\n
            \n
            #frame #pushButton{background: #44478B;}'''

            #Аналитика
            analitics = '''QWidget{background: #141529;}\n
            QPushButton{border: none; text-align: left; color: white; font-family: Consolas;}\n
            QLabel{color: white; font-size: 11px; font-family: Consolas;}\n
            QComboBox {background: white; border: none;}\n
            QComboBox QAbstractItemView { background-color: white;}
            \n
            QPushButton::hover{background-color: #2D2F5C}\n
            QPushButton::pressed{background-color: #44478B}\n
            \n
            #frame_2, #frame, #frame QPushButton, #frame_2 QLabel{background: #1F2035; padding-left: 3px;}\n
            #frame QPushButton::hover{background-color: #2D2F5C;}\n
            #frame QPushButton::pressed{background-color: #44478B;}\n
            \n
            #label{background-color: #1F2035; border: none; border-bottom: 1px solid; color: white; font-family: Consolas; fon-size: 14px}\n
            /*-------------------------------------------------*/\n
            \n
            #label_8{font-size: 12px; font-family: Consolas;}\n
            QComboBox{font-family: Consolas; font-size: 13px;}\n
            #frame_3{background-color: #1B294B;}\n
            #frame_3 QLabel{background-color: #1B294B; font-size: 11px;}\n
            #label_6{font-size: 13px;}\n
            #label_2{font-size: 14px;}\n
            #label_3, label_4, label_5, label_9{font-family: Consolas; font-size: 10px;}\n
            #widget_2{background: white;}\n
            \n
            #frame #pushButton_3{background: #44478B;}'''

            #Просмотр квитанции
            check_kvit = '''QWidget{background: #141529;}\n
            QPushButton{border: none; text-align: left; color: white; font-family: Consolas;}\n
            QLabel{color: white; font-size: 11px; font-family: Consolas;}\n
            \n
            QPushButton::hover{background-color: #2D2F5C}\n
            QPushButton::pressed{background-color: #44478B}\n
            \n
            #frame_2, #frame, #frame QPushButton, #frame_2 QLabel{background: #1F2035; padding-left: 3px;}\n
            #frame QPushButton::hover{background-color: #2D2F5C;}\n
            #frame QPushButton::pressed{background-color: #44478B;}\n
            \n
            #label{background-color: #1F2035; border: none; border-bottom: 1px solid; color: white; font-family: Consolas; fon-size: 14px}\n
            /*-------------------------------------------------*/\n
            QLineEdit{background-color: white; border: none; font-family: Consolas; font-size: 13px; padding-left: 3px;}\n
            #label_2{font-size: 14px;}\n
            #pushButton_5{font-size: 11px; text-align: center; background-color: #595876;}\n
            #label_3{font-size: 12px;}\n
            #tableView {border: 2px solid black; color: white; font-size: 11px;}\n
            QHeaderView::section {background-color: #444A83; color: white; font-size: 10px;}
            QHeaderView {background-color: #27D94B; color: white;}
            QTableView::item{border: 1px solid;}
            QMenu {background-color: #454776; border 4px solid black; color: white; font-size: 11px; font-family: Consolas;}
            QMenu::item:selected {background-color: #6569AD;}
            \n
            #frame #pushButton_2{background: #44478B;}'''

            #Статистика
            statist = '''QWidget{background: #141529;}\n
            QPushButton{border: none; text-align: left; color: white; font-family: Consolas;}\n
            QLabel{color: white; font-size: 11px; font-family: Consolas;}\n
            #label_2 {background-color: #1F2035; border: none; border-bottom: 1px solid; color: white; font-family: Consolas; fon-size: 14px}\n
            \n
            QPushButton::hover{background-color: #2D2F5C}\n
            QPushButton::pressed{background-color: #44478B}\n
            \n
            \n
            #frame_2, #frame, #frame QPushButton, #frame_2 QLabel{background: #1F2035; padding-left: 3px;}\n
            #frame QPushButton::hover{background-color: #2D2F5C;}\n
            #frame QPushButton::pressed{background-color: #44478B;}\n
            /*----------------------------------------------------------------------*/\n
            #frame_4 {background: #141529;}\n
            \n
            #label_5, #label_7, #label_9, #label_13, #label_15 {background-color: none; font-size: 17px;}\n
            \n
            #label_6, #label_10, #label_14, #label_16 {font-size: 18px; background: none; font-weight: bold; color: #08DA9D;}\n
            \n
            #label_8 {background: none; font-size: 15px; color: #08DA9D; font-weight: bold;}\n
            \n
            #frame_3, #frame_5, #frame_6, #frame_7, #frame_8 {background: #27274B;}\n
            \n
            #label_3 {font-size: 14px;}\n
            #frame #pushButton_5{background: #44478B;}\n
            \n'''

            return {'indetif': indetif,
                    'analitics': analitics,
                    'gl_main': gl_main,
                    'check_kvit': check_kvit,
                    'statist': statist}
        
        #Повышения уровня
        def level_up():
            #Индетифитикация
            indetif = '''QWidget{background: #141529;}\n
            QPushButton{background-color: #595973; color: white; font-family: Consolas; font-size: 14px; border-radius: 3px;}\n
            QComboBox{background-color: white; border: none; font-size: 16px; font-family: Consolas; padding-left: 7px;}\n
            QLabel{color: white; font-size: 16px; font-family: Consolas;}\n
            \n
            QPushButton::hover{background-color: #2D2F5C;}\n
            QPushButton::pressed{background-color: #44478B;}\n
            \n
            #label{font-size: 18px;}\n
            QComboBox::drop-down{image: url(C:/Users/Mike2/OneDrive/Рабочий стол/Отчетность коммунальных платежей/icon/srelka.png); width: 16px; height: 16px; border: none; padding-right: 5px; padding-top: 5px;}\n
            QComboBox QAbstractItemView {background-color: white; padding-left: 4px;}\n'''

            #Главное меню
            gl_main = '''QWidget{background: #141529;}\n
            QPushButton{border: none; text-align: left; color: white; font-family: Consolas; font-size: 14px;}\n
            QLabel{color: white; font-size: 11px; font-family: Consolas;}\n
            #label_2 {background-color: #1F2035; border: none; border-bottom: 1px solid; color: white; font-family: Consolas; fon-size: 15px;}\n
            \n
            QPushButton::hover{background-color: #2D2F5C}\n
            QPushButton::pressed{background-color: #44478B}\n
            \n
            \n
            #frame_2, #frame, #frame QPushButton, #frame_2 QLabel{background: #1F2035; padding-left: 3px;}\n
            #frame QPushButton::hover{background-color: #2D2F5C;}\n
            #frame QPushButton::pressed{background-color: #44478B;}\n
            /*----------------------------------------------------------------------*/\n
            #frame_3, #frame_5, #frame_6 {background-color: #27274B;}\n
            \n
            #label_5, #label_7, #label_9 {background-color: none; font-size: 24px;}\n
            \n
            #label_6, #label_8, #label_10 {font-size: 27px; background: none; font-weight: bold; color: #08DA9D;}\n
            \n
            #label_3 {font-size: 32px; font-weight: bold;}\n
            #label_4 {font-size: 22px; font-weight: bold;}\n
            \n
            #frame #pushButton{background: #44478B;}'''

            #Аналитика
            analitics = '''QWidget{background: #141529;}\n
            QPushButton{border: none; text-align: left; color: white; font-family: Consolas; font-size: 14px;}\n
            QLabel{color: white; font-size: 11px; font-family: Consolas;}\n
            QComboBox {background: white; border: none;}\n
            QComboBox QAbstractItemView { background-color: white;}
            \n
            QPushButton::hover{background-color: #2D2F5C}\n
            QPushButton::pressed{background-color: #44478B}\n
            \n
            #frame_2, #frame, #frame QPushButton, #frame_2 QLabel{background: #1F2035; padding-left: 3px;}\n
            #frame QPushButton::hover{background-color: #2D2F5C;}\n
            #frame QPushButton::pressed{background-color: #44478B;}\n
            \n
            #label{background-color: #1F2035; border: none; border-bottom: 1px solid; color: white; font-family: Consolas; fon-size: 15px;}\n
            /*-------------------------------------------------*/\n
            \n
            #label_8{font-size: 12px; font-family: Consolas;}\n
            QComboBox{font-family: Consolas; font-size: 14px;}\n
            #frame_3{background-color: #1B294B;}\n
            #frame_3 QLabel{background-color: #1B294B; font-size: 11px;}\n
            #label_6{font-size: 13px;}\n
            #label_2{font-size: 14px;}\n
            #label_3, label_4, label_5, label_9{font-family: Consolas; font-size: 12px;}\n
            #widget_2{background: white;}\n
            \n
            #frame #pushButton_3{background: #44478B;}'''

            #Просмотр квитанции
            check_kvit = '''QWidget{background: #141529;}\n
            QPushButton{border: none; text-align: left; color: white; font-family: Consolas; font-size: 14px;}\n
            QLabel{color: white; font-size: 11px; font-family: Consolas;}\n
            \n
            QPushButton::hover{background-color: #2D2F5C}\n
            QPushButton::pressed{background-color: #44478B}\n
            \n
            #frame_2, #frame, #frame QPushButton, #frame_2 QLabel{background: #1F2035; padding-left: 3px;}\n
            #frame QPushButton::hover{background-color: #2D2F5C;}\n
            #frame QPushButton::pressed{background-color: #44478B;}\n
            \n
            #label{background-color: #1F2035; border: none; border-bottom: 1px solid; color: white; font-family: Consolas; fon-size: 15px;}\n
            /*-------------------------------------------------*/\n
            QLineEdit{background-color: white; border: none; font-family: Consolas; font-size: 15px; padding-left: 3px;}\n
            #label_2{font-size: 14px;}\n
            #pushButton_5{font-size: 11px; text-align: center; background-color: #595876;}\n
            #label_3{font-size: 14px;}\n
            #tableView {border: 2px solid black; color: white; font-size: 15px;}\n
            QHeaderView::section {background-color: #444A83; color: white; font-size: 14px;}
            QHeaderView {background-color: #27D94B; color: white;}
            QTableView::item{border: 1px solid;}
            QMenu {background-color: #454776; border 4px solid black; color: white; font-size: 17px; font-family: Consolas;}
            QMenu::item:selected {background-color: #6569AD;}
            \n
            #frame #pushButton_2{background: #44478B;}'''

            #Статистика
            statist = '''QWidget{background: #141529;}\n
            QPushButton{border: none; text-align: left; color: white; font-family: Consolas; font-size: 14px;}\n
            QLabel{color: white; font-size: 11px; font-family: Consolas;}\n
            #label_2 {background-color: #1F2035; border: none; border-bottom: 1px solid; color: white; font-family: Consolas; fon-size: 15px;}\n
            \n
            QPushButton::hover{background-color: #2D2F5C}\n
            QPushButton::pressed{background-color: #44478B}\n
            \n
            \n
            #frame_2, #frame, #frame QPushButton, #frame_2 QLabel{background: #1F2035; padding-left: 3px;}\n
            #frame QPushButton::hover{background-color: #2D2F5C;}\n
            #frame QPushButton::pressed{background-color: #44478B;}\n
            /*----------------------------------------------------------------------*/\n
            #frame_4 {background: #141529;}\n
            \n
            #label_5, #label_7, #label_9, #label_13, #label_15 {background-color: none; font-size: 24px;}\n
            \n
            #label_6, #label_10, #label_14, #label_16 {font-size: 26px; background: none; font-weight: bold; color: #08DA9D;}\n
            \n
            #label_8 {background: none; font-size: 25px; color: #08DA9D; font-weight: bold;}\n
            \n
            #frame_3, #frame_5, #frame_6, #frame_7, #frame_8 {background: #27274B;}\n
            \n
            #label_3 {font-size: 14px;}\n
            #frame #pushButton_5{background: #44478B;}\n
            \n'''

            return {'indetif': indetif,
                    'analitics': analitics,
                    'gl_main': gl_main,
                    'check_kvit': check_kvit,
                    'statist': statist}

        #Определение ширины и высоты экрана
        width = self.data['Form'].width()
        height = self.data['Form'].height()

        #Обработка размеров окна
        size = (1000, 580)
        if width > size[0] and height > size[1] and self.scale == False:
            self.scale = True
            
            #Элементы
            frame = self.data['FormUI'][1].Main.frame #Меню
            frame_1 = self.data['FormUI'][2].Main.frame #Меню
            frame_2 = self.data['FormUI'][3].Main.frame #Меню
            frame_3 = self.data['FormUI'][4].Main.frame #Меню

            frame_2_1 = self.data['FormUI'][1].Main.frame_2 #Верхнее продолж меню
            frame_2_2 = self.data['FormUI'][2].Main.frame_2 #Верхнее продолж меню
            frame_2_3 = self.data['FormUI'][3].Main.frame_2 #Верхнее продолж меню
            frame_2_4 = self.data['FormUI'][4].Main.frame_2 #Верхнее продолж меню

            #Индетификация
            centralwidget = self.data['FormUI'][0].Main.centralwidget #Индетификация шаблон стилей
            comboBox = self.data['FormUI'][0].Main.comboBox
            pushButton_3 = self.data['FormUI'][0].Main.pushButton_3 #Войти
            pushButton = self.data['FormUI'][0].Main.pushButton #Добавить адрес
            pushButton_2 = self.data['FormUI'][0].Main.pushButton_2 #удалить адрес
            #Главное меню
            centralwidget_1 = self.data['FormUI'][1].Main.centralwidget
            #Аналитика
            centralwidget_4 = self.data['FormUI'][2].Main.centralwidget
            #Просмотр квитанций
            centralwidget_2 = self.data['FormUI'][3].Main.centralwidget
            #Статистика
            centralwidget_3 = self.data['FormUI'][4].Main.centralwidget

            #Данные для стилей
            data = level_up()

            #Меняем параметры
            centralwidget.setStyleSheet(data['indetif'])
            centralwidget_1.setStyleSheet(data['gl_main'])
            centralwidget_2.setStyleSheet(data['check_kvit'])
            centralwidget_3.setStyleSheet(data['statist'])
            centralwidget_4.setStyleSheet(data['analitics'])

            frame.setMinimumSize(QSize(200, 0))
            frame.setMaximumSize(QSize(200, 16777215))
            frame_1.setMinimumSize(QSize(200, 0))
            frame_1.setMaximumSize(QSize(200, 16777215))
            frame_2.setMinimumSize(QSize(200, 0))
            frame_2.setMaximumSize(QSize(200, 16777215))
            frame_3.setMinimumSize(QSize(200, 0))
            frame_3.setMaximumSize(QSize(200, 16777215))

            frame_2_1.setMinimumSize(QSize(200, 80))
            frame_2_1.setMaximumSize(QSize(200, 80))
            frame_2_2.setMinimumSize(QSize(200, 80))
            frame_2_2.setMaximumSize(QSize(200, 80))
            frame_2_3.setMinimumSize(QSize(200, 80))
            frame_2_3.setMaximumSize(QSize(200, 80))
            frame_2_4.setMinimumSize(QSize(200, 80))
            frame_2_4.setMaximumSize(QSize(200, 80))

            comboBox.setMinimumSize(QSize(480, 26))
            pushButton_3.setMinimumSize(QSize(80, 28))
            pushButton_3.setMaximumSize(QSize(85, 28))
            pushButton.setMinimumSize(QSize(145, 30))
            pushButton.setMaximumSize(QSize(155, 32))
            pushButton_2.setMinimumSize(QSize(145, 30))
            pushButton_2.setMaximumSize(QSize(155, 32))
        #Переход на дефолные значения
        elif width <= size[0] and height <= size[1] and self.scale == True:
            self.scale = False
            
            #Элементы
            frame = self.data['FormUI'][1].Main.frame #Меню
            frame_1 = self.data['FormUI'][2].Main.frame #Меню
            frame_2 = self.data['FormUI'][3].Main.frame #Меню
            frame_3 = self.data['FormUI'][4].Main.frame #Меню

            frame_2_1 = self.data['FormUI'][1].Main.frame_2 #Верхнее продолж меню
            frame_2_2 = self.data['FormUI'][2].Main.frame_2 #Верхнее продолж меню
            frame_2_3 = self.data['FormUI'][3].Main.frame_2 #Верхнее продолж меню
            frame_2_4 = self.data['FormUI'][4].Main.frame_2 #Верхнее продолж меню

            #Индетификация
            centralwidget = self.data['FormUI'][0].Main.centralwidget #Индетификация шаблон стилей
            comboBox = self.data['FormUI'][0].Main.comboBox
            pushButton_3 = self.data['FormUI'][0].Main.pushButton_3 #Войти
            pushButton = self.data['FormUI'][0].Main.pushButton #Добавить адрес
            pushButton_2 = self.data['FormUI'][0].Main.pushButton_2 #удалить адрес
            #Главное меню
            centralwidget_1 = self.data['FormUI'][1].Main.centralwidget
            #Аналитика
            centralwidget_4 = self.data['FormUI'][2].Main.centralwidget
            #Просмотр квитанций
            centralwidget_2 = self.data['FormUI'][3].Main.centralwidget
            #Статистика
            centralwidget_3 = self.data['FormUI'][4].Main.centralwidget

            #Данные для стилей
            data = defoult()

            #Меняем параметры
            centralwidget.setStyleSheet(data['indetif'])
            centralwidget_1.setStyleSheet(data['gl_main'])
            centralwidget_2.setStyleSheet(data['check_kvit'])
            centralwidget_3.setStyleSheet(data['statist'])
            centralwidget_4.setStyleSheet(data['analitics'])

            frame.setMinimumSize(QSize(170, 0))
            frame.setMaximumSize(QSize(170, 16777215))
            frame_1.setMinimumSize(QSize(170, 0))
            frame_1.setMaximumSize(QSize(170, 16777215))
            frame_2.setMinimumSize(QSize(170, 0))
            frame_2.setMaximumSize(QSize(170, 16777215))
            frame_3.setMinimumSize(QSize(170, 0))
            frame_3.setMaximumSize(QSize(170, 16777215))

            frame_2_1.setMinimumSize(QSize(170, 70))
            frame_2_1.setMaximumSize(QSize(170, 70))
            frame_2_2.setMinimumSize(QSize(170, 70))
            frame_2_2.setMaximumSize(QSize(170, 70))
            frame_2_3.setMinimumSize(QSize(170, 70))
            frame_2_3.setMaximumSize(QSize(170, 70))
            frame_2_4.setMinimumSize(QSize(170, 70))
            frame_2_4.setMaximumSize(QSize(170, 70))

            comboBox.setMinimumSize(QSize(350, 23))
            pushButton_3.setMaximumSize(QSize(80, 24))
            pushButton.setMaximumSize(QSize(105, 26))
            pushButton_2.setMaximumSize(QSize(105, 26))
    
    #---------------------------------------------------------------------------------------------
    #ГЛАВНЫЕ СЦЕНАРИИ
    
    #Сигналы различных элементов
    def _logicButton(self):
        
        '''
        -------------------------------------
            0 - Индетификация
        0 - Войти
        1 - Добавить адрес
        2 - Удалить адрес
        -------------------------------------
            1 - Главное меню
        0 - Домашняя страница
        1 - Список платежей
        2 - Аналитика
        3 - Статистика
        4 - Боковое меню
        -------------------------------------
            2 - Аналитика
        0 - Домашняя страница
        1 - Список платежей
        2 - Аналитика
        3 - Статистика
        4 - Боковое меню
        -------------------------------------
            3 - Посмотреть квитанцию
        0 - Домашняя страница
        1 - Список платежей
        2 - Аналитика
        3 - Статистика
        4 - Боковое меню
        5 - Выгрузка в excel
        -------------------------------------
            4 - Статистика
        0 - Домашняя страница
        1 - Список платежей
        2 - Аналитика
        3 - Статистика
        -------------------------------------
            5 - Добавить квитанцию
        0 - Сохранить
        1 - Отменить
        -------------------------------------
            6 - Отдельное окно оповещение
        0 - ОК
        -------------------------------------
            7 - Создать новый адрес
        0 - Сохранить
        1 - Отменить
        -------------------------------------
            8 - Удалить адрес
        0 - Удалить
        1 - Отменить
        -------------------------------------
            9 - Выбор адреса для удаления
        0 - Отменить
        1 - Удалить
        -------------------------------------
            10 - Выход
        
        -------------------------------------
        '''

        self.button = self.data['button']
        self.QCheckBox = self.data['QCheckBox']

        #Индетификация
        self.button[0][0].clicked.connect(lambda: self.enter()) #Войти
        self.button[0][1].clicked.connect(lambda: self._perechod_2(2)) #Добавить адрес
        self.button[0][2].clicked.connect(lambda: self.sinDelAdres()) #Выбор адреса для удаления

        #Главное меню
            #Меню
        self.button[1][0].clicked.connect(lambda: self._perechod(1)) #Домашняя страница
        self.button[1][1].clicked.connect(lambda: self._perechod(3)) #Список платежей
        self.button[1][2].clicked.connect(lambda: self._perechod(2)) #Аналитика
        self.button[1][3].clicked.connect(lambda: self._perechod(4)) #Статистика
        #self.button[1][4].clicked.connect(lambda: self.signBokMenu()) #Боковое меню

        #Окно аналитики
            #Меню
        self.button[2][0].clicked.connect(lambda: self._perechod(1)) #Домашняя страница
        self.button[2][1].clicked.connect(lambda: self._perechod(3)) #Список платежей
        self.button[2][2].clicked.connect(lambda: self._perechod(2)) #Аналитика
        self.button[2][3].clicked.connect(lambda: self._perechod(4)) #Статистика
        self.data['combobox'][2][0].activated.connect(lambda: self.signComboBox()) #Выбор в combobox
        #self.button[2][4] #Боковое меню

        #Посмотреть квитанцию
            #Меню
        self.button[3][0].clicked.connect(lambda: self._perechod(1)) #Домашняя страница
        self.button[3][1].clicked.connect(lambda: self._perechod(3)) #Просмотреть
        self.button[3][2].clicked.connect(lambda: self._perechod(2)) #Аналитика
        self.button[3][3].clicked.connect(lambda: self._perechod(4)) #Статистика
        #self.button[3][4] #Выгрузка Excel
        self.data['lineedit'][3][0].textChanged.connect(lambda: self.signSearch())
        #self.button[3][5] #Боковое меню

        #Статистика
        #Меню
        self.button[4][0].clicked.connect(lambda: self._perechod(1)) #Домашняя страница
        self.button[4][1].clicked.connect(lambda: self._perechod(3)) #Список платежей
        self.button[4][2].clicked.connect(lambda: self._perechod(2)) #Аналитика
        self.button[4][3].clicked.connect(lambda: self._perechod(4)) #Статистика
        #self.button[4][4] #Боковое меню


        #Создать адрес
        self.button[7][1].clicked.connect(lambda: self.otmena_0()) #Отменить
        self.button[7][0].clicked.connect(lambda: self.signAddNewAdres()) #Сохранить

        #Выбор адреса для удаления
        self.button[8][0].clicked.connect(lambda: self.data['Form_2'].close()) #Отменить
        self.button[8][1].clicked.connect(lambda: self.signDeleteAdress()) #Удалить

        #Создать квитанцию
        self.QCheckBox[5][9].clicked.connect(lambda: self.pressCheckBoxGlavn()) #Главная кнопка
        self.button[5][0].clicked.connect(lambda: self.signCreateReceipt()) #Сохранить
        self.button[5][1].clicked.connect(lambda: self.data['Form_2'].close()) #Отменить

        #Редактировать квитанцию
        self.QCheckBox[12][0].clicked.connect(lambda: self.pressCheckBoxGlavn_2()) #Нажатие на кнопку выбора все значения как неоплачиваемые
        self.button[12][1].clicked.connect(lambda: self.data['Form_2'].close()) #Отменить
        self.button[12][0].clicked.connect(lambda: self.signSveEditReceipt()) #Сохранить

        #Выход
        self.button[9][0].clicked.connect(lambda: self.signViborAdresa()) #Выбрать адрес
        self.button[9][1].clicked.connect(lambda: self.data['Form_2'].close()) #Отмена
        self.button[9][2].clicked.connect(lambda: sys.exit(0)) #Выход

        #Удалить квитанцию
        self.button[11][1].clicked.connect(lambda: self.data['Form_2'].close())
        self.button[11][0].clicked.connect(self.signDeleteReceipt)

    #Сигналы combobox
    def _logicComboBox(self):

        #Логика Combobox (индетификация)
        bd = JobBD()
        data = bd._readReturnBD('SELECT (Адрес) FROM АДРЕС;')
        
        [self.data['combobox'][0][0].addItem(str(i[0])) for i in data]
    
    #Развертка таблицы в список платежей
    def _RazvetTable(self):

        #self.data['table'][3][0].horizontalHeader()
        
        self.model=QStandardItemModel(0,0)
        self.model.setHorizontalHeaderLabels([
            'id_счета',
            'id_адреса',
            'Электроэнергия',
            'Вода', 
            'Отопление', 
            'Водоотведение', 
            'Коэф\nналогов', 
            'Содержание\nжилплощади', 
            'Кап\nремонт', 
            'Домофон', 
            'Обслуживание\nгаза', 
            'Газ', 
            'ТКО', 
            'Дополнительные\nрасходы', 
            'Дата\nсоздания', ])
        
        itemTable = self.DataAnalitic['itemText'][0]
        self.tableData = self.JobBD._readReturnBD(f'SELECT * FROM СЧЕТА WHERE id_адреса="{itemTable}";')

        #Добавить к модели колонки и строки из бд
        for row in range(len(self.tableData)):

            row1 = self.DataAnalitic['data_14'][row]

            for column in range(len(row1)):

                if column not in (0, 1) and row1[column] in ('NULL', 'Null', None):
                    row1[column] = 0

                if column == 14:
                    row1[column] = row1[column].split(' ')[0]


                item=QStandardItem(str(row1[column]))
                self.model.setItem(row,column,item)

        self.data['table'][3][0].setModel(self.model)
        self.data['table'][3][0].setEditTriggers(QAbstractItemView.NoEditTriggers)
        #self.data['table'][3][0].setSelectionBehavior(QAbstractItemView.SelectRows)
        self.data['table'][3][0].setSelectionMode(QAbstractItemView.SingleSelection)

        #self.data['table'][3][0].setAlternatingRowColors(True)
        self.data['table'][3][0].verticalHeader().setVisible(False) #убрать нумерацию 
        self.data['table'][3][0].resizeColumnsToContents() #автоматический подгон по ширине
        #self.data['table'][3][0].clicked.connect(lambda: self._namberRowNamberColumn())

        #Скрываем 1 и 2 колонку
        self.data['table'][3][0].setColumnHidden(0, True)
        self.data['table'][3][0].setColumnHidden(1, True)

    #Получение номера строки и номера колонки
    def _namberRowNamberColumn(self):
        '''Получение номера строки и номера колонки'''
        #selected_indexes = self.data['table'][3][0].selectedIndexes()
        
        # Получаем номера строки и колонки первой выбранной ячейки (если есть)

        row = self.data['table'][3][0].currentIndex().row()
        column = self.data['table'][3][0].currentIndex().column()


        return (row, column) #Координаты таблицы
        #elf.cordTable = [row, column] #Координаты таблицы
    #--------------------------------------------------------------------------------
    #РЕАЛИЗАЦИЯ КОНТЕКСТНОГО МЕНЮ

    #Развертка контекстного меню
    def _RazvertKontectMenu(self, pos):
        
        self.menu = QMenu(self.data['QMenu']) #self.data['QMenuTable']
        new = self.menu.addAction('Создать новую квитанцию')
        edit = self.menu.addAction('Редактировать квитанцию')
        Delete = self.menu.addAction('Удалить квитанцию')

        new.triggered.connect(lambda: self.logButtonMenu(0))
        edit.triggered.connect(lambda: self.logButtonMenu(1))
        Delete.triggered.connect(lambda: self.logButtonMenu(2))
        
        act = self.menu.exec_(self.data['table'][3][0].mapToGlobal(pos)) #Реализация щелчка правой кнопки мыши и его координаты появления
    
    #Логика кнопок меню
    def logButtonMenu(self, mod):
        '''0 - Создать новую квитанцию\n
        1 - Редактировать квитанцию\n
        2 - Удалить квитанцию'''

        #Создать новую квитанцию
        if mod == 0:
            self._perechod_2(0)

            #Устанавливаем текущюю дату
            date = datetime.datetime.now()
            date = f'{date.day}.{date.month}.{date.year}'
            self.data['lineedit'][5][3].setText(date)

        #Редактировать квитанцию
        elif mod == 1:
            self.signOpenEditReceipt()
 
        #Удалить квитанцию
        elif mod == 2:
            self._perechod_2(6)
    #--------------------------------------------------------------------------------
    #ЛОГИКА НАЖАТИЙ НА КНОПКУ

    #Логика нажатия на войти  
    def enter(self):

        import Analitic as analit

        self.combobox = self.data['combobox']
        self.label = self.data['label']
        self.indexCombobox = self.data['indexCombobox']

        #Запись метрик выбора пользователя
        self.indexCombobox[1] = self.combobox[0][0].currentText()
        self.indexCombobox[0] = self.JobBD._readReturnBD(f'SELECT id_адреса FROM АДРЕС WHERE Адрес="{self.indexCombobox[1]}"')[0][0]
        
        #Проверка что есть значения
        if self.indexCombobox[1] != '':

            self.Analit = analit.Analitic(self.indexCombobox[0])

            #Данные из аналитики
            self.Analitic = self.Analit
            self.DataAnalitic = self.Analitic.run()

            text = f'<html><head/><body><p style=line-height: 1.2px><b>Адрес:</b><br>{self.indexCombobox[1]}</p></body></html>'
            
            #Устанавливаем название адреса в меню
            self.label[1][0].setText(text)
            self.label[2][0].setText(text)
            self.label[3][0].setText(text)
            self.label[4][0].setText(text)
            
            #Устанавливаем надписи в главном меню
            self.label[1][1].setText(self.Logic.typeTimeDay())
            self.label[1][2].setText(self.Logic.old_zahod(self.old_data))
            self.label[1][4].setText(self.block1._convertNumber(self.DataAnalitic['colZapisey_1'])) #Количество записей
            self.label[1][6].setText(self.block1._convertNumber(self.DataAnalitic['srednKolZap_2'])) #Среднее количество записей в месяц
            self.label[1][8].setText(self.block1._convertNumber(self.DataAnalitic['KolZapMes_3'])) #Количество записей в данном месяце

            #Устанавливаем надписи в аналитике
            text = '<html><body style="line-height: 1.3;">Самый расходный<br> месяц:<br><b style="color: #CE8632;">' + self.DataAnalitic['MaxRashod_5'] + '</b></body></html>'
            self.label[2][3].setText(text) #Самый расходный месяц

            text = '<html><body style="line-height: 1.3;">Месяц с минимальными<br>расходами:<br><b style="color: #CE8632;">' + self.DataAnalitic['MonthMinExpenses_6'] + '</b></body></html>'
            self.label[2][4].setText(text) #Месяц с минимальными расходами

            text = '<html><body style="line-height: 1.3;">Средние расходы:<br><br><b style="color: #CE8632;">' + str(self.DataAnalitic['AverageMonthlyExpenses_7']) + '</b></body></html>'
            self.label[2][5].setText(text) #Средние расходы

            text = '<html><body style="line-height: 1.3;">Инфляция с<br>прошлым годом:<br><b style="color: #CE8632;">'+ str(self.DataAnalitic['inflationFromLastYear_8']) + '%</b></body></html>'
            self.label[2][6].setText(text) #Инфляция с прошлым годом
            [self.combobox[2][0].addItem(str(i)) for i in self.DataAnalitic['YearPopular']]

            #Устанавливаем надписи в статистике
            self.label[4][3].setText(self.block1._convertNumber(self.DataAnalitic['TotalNumberExpenses_9']))#Общее количество расходов
            self.label[4][5].setText(self.block1._convertNumber(self.DataAnalitic['ExpensesPerYear_12']))#Расходы за этот год
            self.label[4][7].setText(self.block1._convertNumber(self.DataAnalitic['NumberEntriesLastMonth_11'])) #Количество записей в прошлом месяце
            self.label[4][9].setText(self.DataAnalitic['MostExpendableItem_10'])#Самая расходная статья расходов
            self.label[4][11].setText(self.block1._convertNumber(self.DataAnalitic['notPaidYear_13'])) #Не оплачено в этом году

            self._RazvetTable()

            self.ScanGrafic() #Развертка графиков

            self._perechod(1)
    
    #Нажатие на удаление адреса
    def sinDelAdres(self):

        adres = self.JobBD._readReturnBD('SELECT (Адрес) FROM АДРЕС')

        [self.data['listWidget'][8][0].addItem(f'{i[0]}') for i in adres]
        self._perechod_2(3)

    #Нажата кнопка выбора адреса
    def signViborAdresa(self):

        '''#Исключаем задвоение графиков
        if self.ax1 != None and self.ax2 != None:
            #self.canvas_1.figure.clear()
            #self.canvas_2.figure.clear()
            self.ax1.clear()
            self.ax2.clear()'''
            

        self.data['combobox'][2][0].clear()
        self.data['Form_2'].close()
        self._perechod(0)

    #Отмена для создания адреса
    def otmena_0(self):
        self.data['lineedit'][7][0].setText('') 
        #self.data['Form_2'][7]
        self.data['label'][7][1].setText('')
        self.data['Form_2'].close()
    
    #Выход с отдельного окна
    def exitMain(self, e):
        self.data['lineedit'][7][0].setText('')
        self.data['listWidget'][8][0].clear()
        e.accept()

    #Выход с главного окна
    def exitMain_1(self, e):
         self._perechod_2(4)
         e.ignore() 

    #Нажатие на кнопку удалить в выборе адресов для удаления
    def signDeleteAdres(self):
        text = self.data['listWidget'][8][0].currentItem().text()

    #Нажатие в форме выбора адреса для удаления (на кнопку удалить)
    def signDeleteAdress(self):

        if self.data['listWidget'][8][0].count() > 0:
            click = self.data['listWidget'][8][0].currentRow()
            data = self.JobBD._readReturnBD('SELECT * FROM АДРЕС;')

            self.data['label'][10][0].setText(f'Удалить адрес: "{data[click][1]}"')

            data = data[click][0]
            self._perechod_2(5)
            self.data['Form_2'].setWindowTitle('Удалить адрес')


            #Окно с подтверждением удаления адреса
            self.button[10][1].clicked.connect(lambda: self.data['Form_2'].close())
            self.button[10][0].clicked.connect(lambda: self.signDelteAdressON(data))

    #Полное согласие на удаление адреса
    def signDelteAdressON(self, data):
        self.JobBD._readBD(f'DELETE FROM АДРЕС WHERE id_адреса = {data};')

        self._perechod_2(3)

        #Обновление
        self.data['listWidget'][8][0].clear()
        adres = self.JobBD._readReturnBD('SELECT (Адрес) FROM АДРЕС;')
        [self.data['listWidget'][8][0].addItem(f'{i[0]}') for i in adres]

        self.data['combobox'][0][0].clear()
        [self.data['combobox'][0][0].addItem(f'{i[0]}') for i in adres]

    #Сигнал сохранения адреса
    def signAddNewAdres(self):

        #Проверка что нет совпадений в адресе
        data = self.JobBD._readReturnBD('SELECT * FROM АДРЕС;'); data = [i[1] for i in data]

        if len(self.data['lineedit'][7][0].text()) > 0 and self.data['lineedit'][7][0].text() not in data:
            
            self.JobBD._readBD('INSERT INTO АДРЕС (Адрес) VALUES ("' + self.data['lineedit'][7][0].text() + '");')

            adres = self.JobBD._readReturnBD('SELECT (Адрес) FROM АДРЕС;')
            self.data['combobox'][0][0].clear()
            [self.data['combobox'][0][0].addItem(f'{i[0]}') for i in adres]
            self.otmena_0()

        
        else:
            self.data['label'][7][1].setText('Такой адрес уже существует!')
    #---------------------------------------------------------------------------------------------
    #СЦЕРНАРИЙ ВЗАИМОДЕЙСТВИЯ С ТАБЛИЦАМИ

    #Сигнал нажатия на checkBox который контролирует все (в создать новую квитанцию)
    def pressCheckBoxGlavn(self):
        a = self.QCheckBox[5][9].isChecked()
        self.QCheckBox[5][0].setChecked(a)
        self.QCheckBox[5][1].setChecked(a)
        self.QCheckBox[5][2].setChecked(a)
        self.QCheckBox[5][3].setChecked(a)
        self.QCheckBox[5][4].setChecked(a)
        self.QCheckBox[5][5].setChecked(a)
        self.QCheckBox[5][6].setChecked(a)
        self.QCheckBox[5][7].setChecked(a)
        self.QCheckBox[5][8].setChecked(a)
        self.QCheckBox[5][10].setChecked(a)
        self.QCheckBox[5][11].setChecked(a)
        self.QCheckBox[5][12].setChecked(a)

    #Сигнал нажатия на checkBox который контролирует все (в редактировать квитанцию)
    def pressCheckBoxGlavn_2(self):
        a = self.QCheckBox[12][9].isChecked()
        self.QCheckBox[12][0].setChecked(a)
        self.QCheckBox[12][1].setChecked(a)
        self.QCheckBox[12][2].setChecked(a)
        self.QCheckBox[12][3].setChecked(a)
        self.QCheckBox[12][4].setChecked(a)
        self.QCheckBox[12][5].setChecked(a)
        self.QCheckBox[12][6].setChecked(a)
        self.QCheckBox[12][7].setChecked(a)
        self.QCheckBox[12][8].setChecked(a)
        self.QCheckBox[12][10].setChecked(a)
        self.QCheckBox[12][11].setChecked(a)
        self.QCheckBox[12][12].setChecked(a)

    #Удалить квитанцию
    def signDeleteReceipt(self):
        
        #Получение номера строки
        row = list(self._namberRowNamberColumn())
        row = row[0]

        #Получаем id из бд удаляемой строки
        index = self.model.data(self.model.index(row, 0))
        
        #Получение строки из бд (которую удаляем)
        data = self.JobBD._readReturnBD(f'SELECT Электроэнергия, Вода, Отопление, Водоотведение, Коэффициент_налогов, Содержание_жилплощади, Кап_ремонт, Домофон, Обслуживание_газа, Газ, ТКО, Дополнительные_расходы, Дата_создания FROM СЧЕТА WHERE id_счета={index};')

        #Удаляем данные из бд
        self.JobBD._readBD(f'DELETE FROM СЧЕТА WHERE id_счета = {index};')
        self.JobBD._readBD(f'DELETE FROM СТАТУС_СЧЕТА WHERE id_счета={index}')
        
        #Получаем данные 
        self.tableData = data

        #Удаляем строку из модели в tableview
        self.model.removeRow(row)

        #Общее количество записей
        col = self.label[1][4].text()
        col = col.replace(' ', '')
        col = int(col) - 1; col = self.block1._convertNumber(col)
        self.label[1][4].setText(col)

        #Общее количество расходов
        summa = 0
        for i in data[0][0: 11]:
            if i != None:
                summa = summa + i
        out = self.label[4][3].text()
        out = out.replace(' ', ''); out = float(out); out = out - summa
        out = self.block1._convertNumber(out)
        self.label[4][3].setText(str(out))

        #Расходы за этот год
        date = str(datetime.datetime.now().year)
        if date in data[0][-1]:
            out = self.label[4][5].text()
            out = out.replace(' ', ''); out = float(out)
            out = out - summa
            self.label[4][5].setText(self.block1._convertNumber(out))
        

        new_data = self.Analit.returnUpdate()
        #Количество записей в данном месяце
        self.label[1][8].setText(self.block1._convertNumber(new_data[0]))
        #Не оплачено в этом году
        self.label[4][11].setText(self.block1._convertNumber(new_data[1]))
        #Количество записей в прошлом месяце
        self.label[4][7].setText(self.block1._convertNumber(new_data[2]))
        #Самая расходная статья расходов
        self.label[4][9].setText(new_data[3])

        #Обновляем графики
        self.UpdateGrafic()
        
        self.data['Form_2'].close()

    #Создать квитанцию (добавить)
    def signCreateReceipt(self):
        
        #Проверяем месяц на корректность форматированность
        def mounth_check(date: str):
            '''01.6.2020 15:30:10 ---> 01.06.2020 15:30:10'''

            date = date.split(' ')
            date1 = date[0].split('.')
            
            if date1[1] not in ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'):
                date1[1] = f'0{date1[1]}'
                date[0] = '.'.join(date1)
                date = ' '.join(date)
            else:
                date = ' '.join(date)
            
            return date
        #Получения английского, русского алфавита а также знаков
        def getting_signs():

            return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', '-', ' ', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', 'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'ё', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', 'Ё']
        #Проверка текста на содержание символов русского и анлийского алфавита
        def check_text(text: str):
            '''Проверка текста на содержание символов русского и английского алфавита\n
            True - Текст не содержит буквы\n
            False - Текст содержит буквы'''

            alf = getting_signs()
            
            for i in text:
                if i in alf:
                    return False
            
            return True
        #Проверяем есть ли заполненные значения в массиве
        def check_notNULLnotNone(data):
            '''Проверяем есть ли заполненные значения в массиве\n
            1 - Хорошо
            0 - Пусто
            3 - Критическая ошибка'''

            list_data = []
            for i in data:
                if i == '':
                    list_data.append(0)
                elif i[0] == '0':
                    list_data.append(0)
                else:
                    a = []
                    for i1 in i:
                        if i1 not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                            a.append(3)
                        else:
                            a.append(1)

                    if 1 in a and 3 not in a:
                        list_data.append(1)
                    else:
                        list_data.append(3)

            if 1 in list_data and 3 not in list_data:
                return True
            else:
                return False


        lineEdit = []
        checkBox = []

        #QlineEdit ['', '1000']
        lineEdit.append(self.data['lineedit'][5][8].text()) #Электроэнергия 0
        lineEdit.append(self.data['lineedit'][5][2].text()) #Отопление 1
        lineEdit.append(self.data['lineedit'][5][9].text()) #Вода 2
        lineEdit.append(self.data['lineedit'][5][1].text()) #Водоотведение 3
        lineEdit.append(self.data['lineedit'][5][4].text()) #Коэф налогов 4
        lineEdit.append(self.data['lineedit'][5][11].text()) #Содержание жилплощади 5
        lineEdit.append(self.data['lineedit'][5][10].text()) #Газ 6
        lineEdit.append(self.data['lineedit'][5][5].text()) #Дополнительные расходы 7
        lineEdit.append(self.data['lineedit'][5][0].text()) #Кап ремонт 8
        lineEdit.append(self.data['lineedit'][5][6].text()) #Домофон 9
        lineEdit.append(self.data['lineedit'][5][12].text()) #Обслуживание газа 10
        lineEdit.append(self.data['lineedit'][5][7].text()) #ТКО 11
        lineEdit.append(self.data['lineedit'][5][3].text()) #Дата оплаты 12
        

        #QCheckBox [trur, false]
        checkBox.append(self.data['QCheckBox'][5][10].isChecked()) #Электроэнергия 0
        checkBox.append(self.data['QCheckBox'][5][2].isChecked()) #Отопление 1
        checkBox.append(self.data['QCheckBox'][5][3].isChecked()) #Вода 2
        checkBox.append(self.data['QCheckBox'][5][1].isChecked()) #Водоотведение 3
        checkBox.append(self.data['QCheckBox'][5][6].isChecked()) #Коэф налогов 4
        checkBox.append(self.data['QCheckBox'][5][8].isChecked()) #Содержание жилплощади 5
        checkBox.append(self.data['QCheckBox'][5][7].isChecked()) #Газ 6
        checkBox.append(self.data['QCheckBox'][5][12].isChecked()) #Дополнительные расходы 7
        checkBox.append(self.data['QCheckBox'][5][11].isChecked()) #Кап ремонт 8
        checkBox.append(self.data['QCheckBox'][5][4].isChecked()) #Домофон 9
        checkBox.append(self.data['QCheckBox'][5][5].isChecked()) #Обслуживание газа 10
        checkBox.append(self.data['QCheckBox'][5][0].isChecked()) #ТКО 11

        #Проверяем есть ли заполненные значения в массиве
        if check_notNULLnotNone(lineEdit[:12]) == True:

            #Проверка на пустые значения и форматирование в нужный вид
            alf = getting_signs()
            for i in range(len(lineEdit[0: 12])):

                if lineEdit[i] != '' and check_text(lineEdit[i]) == True:
                    lineEdit[i] = lineEdit[i].replace(',', '.')
                    try:
                        lineEdit[i] = float(lineEdit[i])
                    except:
                        lineEdit[i] = 'NULL'
                else:
                    lineEdit[i] = 'NULL'
            
            #Проверка что введен нужный вид даты (и приведение его в нужный вид)
            a = lineEdit[12].split('.')
            if len(a) == 3:
                a1 = [None, None, None]

                #Проверка на правильность ввода даты и месяца
                a1[0] = a[0] in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31')
                a1[1] = a[1] in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12')
                
                #Проверяем на правильность ввода года
                if len(a[2]) > 0:
                    for i in a[2]:
                        if i in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                            a1[2] = True
                        else:
                            a1[2] = False
                            break
                else:
                    a1[2] = False

                #Проверяем что все правильно введено
                if a1[0] == True and a1[1] == True and a1[2] == True:
                    
                    date = datetime.datetime.now()
                    lineEdit[12] = f'{lineEdit[12]} {date.hour}:{date.minute}:{date.second}'

                else:
                    date = datetime.datetime.now()
                    lineEdit[12] = (f'{date.day}.{date.month}.{date.year} {date.hour}:{date.minute}:{date.second}')
            else:

                date = datetime.datetime.now()
                lineEdit[12] = (f'{date.day}.{date.month}.{date.year} {date.hour}:{date.minute}:{date.second}')
            
            lineEdit[12] = mounth_check(lineEdit[12])

            #Делаем запрос на добавление строки в бд и узнаем id запроса
            last_row_id = self.JobBD._requestID(f"INSERT INTO СЧЕТА (id_адреса, Электроэнергия, Вода, Отопление, Водоотведение, Коэффициент_налогов, Содержание_жилплощади, Кап_ремонт, Домофон, Обслуживание_газа, Газ, ТКО, Дополнительные_расходы, Дата_создания) VALUES ({self.DataAnalitic['itemText'][0]}, {lineEdit[0]}, {lineEdit[2]}, {lineEdit[1]}, {lineEdit[3]}, {lineEdit[4]}, {lineEdit[5]}, {lineEdit[8]}, {lineEdit[9]}, {lineEdit[10]}, {lineEdit[6]}, {lineEdit[11]}, {lineEdit[7]}, '{lineEdit[12]}');")


            #Добавляем в tableview значения
            data = self.JobBD._readReturnBD(f'SELECT * FROM СЧЕТА WHERE id_счета={last_row_id};')[0]
            data = list(data)

            #Изменить дату
            data[14] = data[14].split(' ')[0]
            
            row = self.model.rowCount()
            for i in range(len(data)):
                if data[i] == None:
                    item = QStandardItem('0')
                    self.model.setItem(row, i, item)
                else:
                    item = QStandardItem(str(data[i])) #Добавить item
                    self.model.setItem(row, i, item) #Сохранить item (столбец, строка, значение)

            #Добавить статус счета
            self.JobBD._readBD(f'INSERT INTO СТАТУС_СЧЕТА (id_счета, Электроэнергия, Вода, Отопление, Водоотведение, Коэффициент_налогов, Содержание_жилплощади, Кап_ремонт, Домофон, Обслуживание_газа, Газ, ТКО, Дополнительные_расходы) VALUES ({last_row_id}, {checkBox[0]}, {checkBox[2]}, {checkBox[1]}, {checkBox[3]}, {checkBox[4]}, {checkBox[5]}, {checkBox[8]}, {checkBox[9]}, {checkBox[10]}, {checkBox[6]}, {checkBox[11]}, {checkBox[7]});')
            
            #Стереть все данные в форме
            self.data['lineedit'][5][8].setText('') #Электроэнергия 0
            self.data['lineedit'][5][2].setText('') #Отопление 1
            self.data['lineedit'][5][9].setText('') #Вода 2
            self.data['lineedit'][5][1].setText('') #Водоотведение 3
            self.data['lineedit'][5][4].setText('') #Коэф налогов 4
            self.data['lineedit'][5][11].setText('') #Содержание жилплощади 5
            self.data['lineedit'][5][10].setText('') #Газ 6
            self.data['lineedit'][5][5].setText('') #Дополнительные расходы 7
            self.data['lineedit'][5][0].setText('') #Кап ремонт 8
            self.data['lineedit'][5][6].setText('') #Домофон 9
            self.data['lineedit'][5][12].setText('') #Обслуживание газа 10
            self.data['lineedit'][5][7].setText('') #ТКО 11
            self.data['lineedit'][5][3].setText('') #Дата оплаты 12
            

            #QCheckBox [trur, false]
            self.data['QCheckBox'][5][10].setChecked(True) #Электроэнергия 0
            self.data['QCheckBox'][5][2].setChecked(True) #Отопление 1
            self.data['QCheckBox'][5][3].setChecked(True) #Вода 2
            self.data['QCheckBox'][5][1].setChecked(True) #Водоотведение 3
            self.data['QCheckBox'][5][6].setChecked(True) #Коэф налогов 4
            self.data['QCheckBox'][5][8].setChecked(True) #Содержание жилплощади 5
            self.data['QCheckBox'][5][7].setChecked(True) #Газ 6
            self.data['QCheckBox'][5][12].setChecked(True) #Дополнительные расходы 7
            self.data['QCheckBox'][5][11].setChecked(True) #Кап ремонт 8
            self.data['QCheckBox'][5][4].setChecked(True) #Домофон 9
            self.data['QCheckBox'][5][5].setChecked(True) #Обслуживание газа 10
            self.data['QCheckBox'][5][0].setChecked(True) #ТКО 11

            #Закрыть форму
            self.data['Form_2'].close()

            #Общее количество записей
            col = self.label[1][4].text()
            col = col.replace(' ', '')
            col = int(col) + 1; col = self.block1._convertNumber(col)
            self.label[1][4].setText(col)

            #Общее количество расходов
            summa = 0
            for i in lineEdit[:12]:
                if i not in ('NULL', None):
                    summa = summa + i
            out = self.label[4][3].text()
            out = out.replace(' ', ''); out = float(out); out = out + summa
            out = self.block1._convertNumber(out)
            self.label[4][3].setText(str(out))

            #Расходы за этот год
            date = str(datetime.datetime.now().year)
            if date in lineEdit[-1]:
                out = self.label[4][5].text()
                out = out.replace(' ', ''); out = float(out)
                out = out + summa
                self.label[4][5].setText(self.block1._convertNumber(out))

            new_data = self.Analit.returnUpdate()
            #Количество записей в данном месяце
            self.label[1][8].setText(self.block1._convertNumber(new_data[0]))
            #Не оплачено в этом году
            self.label[4][11].setText(self.block1._convertNumber(new_data[1]))
            #Количество записей в прошлом месяце
            self.label[4][7].setText(self.block1._convertNumber(new_data[2]))
            #Самая расходная статья расходов
            self.label[4][9].setText(new_data[3])

            #Обновляем графики
            self.UpdateGrafic()
            
    #Открыть форму редактировать квитанцию
    def signOpenEditReceipt(self):
        
        #Получение данных 
        index = self._namberRowNamberColumn()[0]
        self.index = self.model.data(self.model.index(index, 0))

        data = self.JobBD._readReturnBD(f'SELECT * FROM СЧЕТА WHERE id_счета={self.index}')
        data = list(data); data = list(data[0])

        data_states = self.JobBD._readReturnBD(f'SELECT * FROM СТАТУС_СЧЕТА WHERE id_счета={self.index}')

        #Приведение массива в нужный вид (убираем все None)
        for i in range(len(data)):

            if data[i] == None:
                data[i] = ''
            elif i == 14:
                data[i] = data[i].split(' ')[0]
            else:
                #Проверяем есть ли плавающая пустая точка
                if str(data[i]).split('.0')[-1] == '':
                    data[i] = str(data[i]).split('.')[0]
                else:
                    data[i] = str(data[i])

        data_states = list(data_states); data_states = list(data_states[0])

        #Приведение массива в нужный вид (Выставляем True/False)
        for i in range(len(data_states)):

            if i != 0 and data_states[i] == 1:
                data_states[i] = True
            elif i != 0 and data_states[i] == 0:
                data_states[i] = False
            elif i == 0:
                data_states[i] = str(data_states[i])

        #Внесение данных в форму
        self.data['lineedit'][12][8].setText(data[2]) #Электроэнергия 0
        self.data['lineedit'][12][2].setText(data[4]) #Отопление 1
        self.data['lineedit'][12][9].setText(data[3]) #Вода 2
        self.data['lineedit'][12][1].setText(data[5]) #Водоотведение 3
        self.data['lineedit'][12][4].setText(data[6]) #Коэф налогов 4
        self.data['lineedit'][12][11].setText(data[7]) #Содержание жилплощади 5
        self.data['lineedit'][12][10].setText(data[11]) #Газ 6
        self.data['lineedit'][12][5].setText(data[13]) #Дополнительные расходы 7
        self.data['lineedit'][12][0].setText(data[8]) #Кап ремонт 8
        self.data['lineedit'][12][6].setText(data[9]) #Домофон 9
        self.data['lineedit'][12][12].setText(data[10]) #Обслуживание газа 10
        self.data['lineedit'][12][7].setText(data[12]) #ТКО 11
        self.data['lineedit'][12][3].setText(data[14]) #Дата оплаты 12
        
        '''
        id_счета 0	
        Электроэнергия	 1
        Вода	2
        Отопление	3
        Водоотведение	4
        Коэффициент_налогов	5
        Содержание_жилплощади	6
        Кап_ремонт	7
        Домофон	8
        Обслуживание_газа	9
        Газ	10
        ТКО	11
        Дополнительные_расходы  12
        Дата_создания 13
        '''

        #QCheckBox [true, false]
        self.data['QCheckBox'][12][10].setChecked(data_states[1]) #Электроэнергия 0
        self.data['QCheckBox'][12][2].setChecked(data_states[3]) #Отопление 1
        self.data['QCheckBox'][12][3].setChecked(data_states[2]) #Вода 2
        self.data['QCheckBox'][12][1].setChecked(data_states[4]) #Водоотведение 3
        self.data['QCheckBox'][12][6].setChecked(data_states[5]) #Коэф налогов 4
        self.data['QCheckBox'][12][8].setChecked(data_states[6]) #Содержание жилплощади 5
        self.data['QCheckBox'][12][7].setChecked(data_states[10]) #Газ 6
        self.data['QCheckBox'][12][12].setChecked(data_states[12]) #Дополнительные расходы 7
        self.data['QCheckBox'][12][11].setChecked(data_states[7]) #Кап ремонт 8
        self.data['QCheckBox'][12][4].setChecked(data_states[8]) #Домофон 9
        self.data['QCheckBox'][12][5].setChecked(data_states[9]) #Обслуживание газа 10
        self.data['QCheckBox'][12][0].setChecked(data_states[11]) #ТКО 11

        self._perechod_2(7)

    #Сохранить редактированную версию квитанции
    def signSveEditReceipt(self):
        
        #Проверяем месяц на корректность форматированность
        def mounth_check(date: str):
            '''01.6.2020 15:30:10 ---> 01.06.2020 15:30:10'''

            date = date.split(' ')
            date1 = date[0].split('.')
            
            if date1[1] not in ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'):
                date1[1] = f'0{date1[1]}'
                date[0] = '.'.join(date1)
                date = ' '.join(date)
            else:
                date = ' '.join(date)
            
            return date
        #Получения английского, русского алфавита а также знаков
        def getting_signs():

            return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', '-', ' ', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', 'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'ё', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', 'Ё']
        #Проверка текста на содержание символов русского и анлийского алфавита
        def check_text(text: str):
            '''Проверка текста на содержание символов русского и английского алфавита\n
            True - Текст не содержит буквы\n
            False - Текст содержит буквы'''

            alf = getting_signs()
            
            for i in text:
                if i in alf:
                    return False
            
            return True
        #Проверяем есть ли заполненные значения в массиве
        def check_notNULLnotNone(data):
            '''Проверяем есть ли заполненные значения в массиве'''

            list_data = []
            for i in data:
                if i == '':
                    list_data.append(0)
                elif i[0] == '0':
                    list_data.append(0)
                else:
                    a = []
                    for i1 in i:
                        if i1 not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                            a.append(3)
                        else:
                            a.append(1)

                    if 1 in a and 3 not in a:
                        list_data.append(1)
                    else:
                        list_data.append(3)

            if 1 in list_data and 3 not in list_data:
                return True
            else:
                return False
                        

            

        lineEdit = []
        checkBox = []

        #QlineEdit ['', '1000']
        lineEdit.append(self.data['lineedit'][12][8].text()) #Электроэнергия 0
        lineEdit.append(self.data['lineedit'][12][2].text()) #Отопление 1
        lineEdit.append(self.data['lineedit'][12][9].text()) #Вода 2
        lineEdit.append(self.data['lineedit'][12][1].text()) #Водоотведение 3
        lineEdit.append(self.data['lineedit'][12][4].text()) #Коэф налогов 4
        lineEdit.append(self.data['lineedit'][12][11].text()) #Содержание жилплощади 5
        lineEdit.append(self.data['lineedit'][12][10].text()) #Газ 6
        lineEdit.append(self.data['lineedit'][12][5].text()) #Дополнительные расходы 7
        lineEdit.append(self.data['lineedit'][12][0].text()) #Кап ремонт 8
        lineEdit.append(self.data['lineedit'][12][6].text()) #Домофон 9
        lineEdit.append(self.data['lineedit'][12][12].text()) #Обслуживание газа 10
        lineEdit.append(self.data['lineedit'][12][7].text()) #ТКО 11
        lineEdit.append(self.data['lineedit'][12][3].text()) #Дата оплаты 12
        

        #QCheckBox [trur, false]
        checkBox.append(self.data['QCheckBox'][12][10].isChecked()) #Электроэнергия 0
        checkBox.append(self.data['QCheckBox'][12][2].isChecked()) #Отопление 1
        checkBox.append(self.data['QCheckBox'][12][3].isChecked()) #Вода 2
        checkBox.append(self.data['QCheckBox'][12][1].isChecked()) #Водоотведение 3
        checkBox.append(self.data['QCheckBox'][12][6].isChecked()) #Коэф налогов 4
        checkBox.append(self.data['QCheckBox'][12][8].isChecked()) #Содержание жилплощади 5
        checkBox.append(self.data['QCheckBox'][12][7].isChecked()) #Газ 6
        checkBox.append(self.data['QCheckBox'][12][12].isChecked()) #Дополнительные расходы 7
        checkBox.append(self.data['QCheckBox'][12][11].isChecked()) #Кап ремонт 8
        checkBox.append(self.data['QCheckBox'][12][4].isChecked()) #Домофон 9
        checkBox.append(self.data['QCheckBox'][12][5].isChecked()) #Обслуживание газа 10
        checkBox.append(self.data['QCheckBox'][12][0].isChecked()) #ТКО 11

        #Проверяем есть ли заполненные значения в массиве
        aa = check_notNULLnotNone(lineEdit[:12])
        if check_notNULLnotNone(lineEdit[:12]) == True:

            #Проверка на пустые значения и форматирование в нужный вид
            alf = getting_signs()
            for i in range(len(lineEdit[0: 12])):

                if lineEdit[i] != '' and check_text(lineEdit[i]) == True:
                    lineEdit[i] = lineEdit[i].replace(',', '.')
                    try:
                        lineEdit[i] = float(lineEdit[i])
                    except:
                        lineEdit[i] = 'NULL'
                else:
                    lineEdit[i] = 'NULL'
            
            #Проверка что введен нужный вид даты (и приведение его в нужный вид)
            a = lineEdit[12].split('.')
            if len(a) == 3:
                a1 = [None, None, None]

                #Проверка на правильность ввода даты и месяца
                a1[0] = a[0] in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31')
                a1[1] = a[1] in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12')
                
                #Проверяем на правильность ввода года
                if len(a[2]) > 0:
                    for i in a[2]:
                        if i in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                            a1[2] = True
                        else:
                            a1[2] = False
                            break
                else:
                    a1[2] = False

                #Проверяем что все правильно введено
                if a1[0] == True and a1[1] == True and a1[2] == True:
                    
                    date = datetime.datetime.now()
                    lineEdit[12] = f'{lineEdit[12]} {date.hour}:{date.minute}:{date.second}'

                else:
                    date = datetime.datetime.now()
                    lineEdit[12] = (f'{date.day}.{date.month}.{date.year} {date.hour}:{date.minute}:{date.second}')
            else:

                date = datetime.datetime.now()
                lineEdit[12] = (f'{date.day}.{date.month}.{date.year} {date.hour}:{date.minute}:{date.second}')
            
            lineEdit[12] = mounth_check(lineEdit[12])

            #Запрос на изменение к базе данных
            self.JobBD._readBD(f"UPDATE СЧЕТА SET Электроэнергия={lineEdit[0]}, Вода={lineEdit[2]}, Отопление={lineEdit[1]}, Водоотведение={lineEdit[3]}, Коэффициент_налогов={lineEdit[4]}, Содержание_жилплощади={lineEdit[5]}, Кап_ремонт={lineEdit[8]}, Домофон={lineEdit[9]}, Обслуживание_газа={lineEdit[10]}, Газ={lineEdit[6]}, ТКО={lineEdit[11]}, Дополнительные_расходы={lineEdit[7]}, Дата_создания='{lineEdit[12]}' WHERE id_счета={self.index};")


            self.JobBD._readBD(f'UPDATE СТАТУС_СЧЕТА SET Электроэнергия={checkBox[0]}, Вода={checkBox[2]}, Отопление={checkBox[1]}, Водоотведение={checkBox[3]}, Коэффициент_налогов={checkBox[4]}, Содержание_жилплощади={checkBox[5]}, Кап_ремонт={checkBox[8]}, Домофон={checkBox[9]}, Обслуживание_газа={checkBox[10]}, Газ={checkBox[6]}, ТКО={checkBox[11]}, Дополнительные_расходы={checkBox[7]} WHERE id_счета={self.index};')

            #Изменить строку в таблице
            new_data = self.JobBD._readReturnBD(f'SELECT * FROM СЧЕТА WHERE id_счета={self.index};')
            row = self._namberRowNamberColumn()[0]
            
            #Приведение списка для строки в таблице в нужный вид (None убираем и в str)
            new_data = list(new_data[0])
            for i in range(len(new_data)):
                if new_data[i] == None:
                    new_data[i] = '0'
                else:
                    new_data[i] = str(new_data[i])

            #Изменить модель
            for i in range(len(new_data)):
                item = QStandardItem(new_data[i])
                self.model.setItem(row, i, item)

            #Закрыть форму
            self.data['Form_2'].close()

            new_data_0 = self.Analit.returnUpdate_2()
            #Общее количество расходов
            self.label[4][3].setText(self.block1._convertNumber(new_data_0[0]))
            #Расходы за этот год
            self.label[4][5].setText(self.block1._convertNumber(new_data_0[1]))
            
            
            
            new_data = self.Analit.returnUpdate()
            #Количество записей в данном месяце
            self.label[1][8].setText(self.block1._convertNumber(new_data[0]))
            #Не оплачено в этом году
            self.label[4][11].setText(self.block1._convertNumber(new_data[1]))
            #Количество записей в прошлом месяце
            self.label[4][7].setText(self.block1._convertNumber(new_data[2]))
            #Самая расходная статья расходов
            self.label[4][9].setText(new_data[3])

            #Стереть все данные в форме
            self.data['lineedit'][12][8].setText('') #Электроэнергия 0
            self.data['lineedit'][12][2].setText('') #Отопление 1
            self.data['lineedit'][12][9].setText('') #Вода 2
            self.data['lineedit'][12][1].setText('') #Водоотведение 3
            self.data['lineedit'][12][4].setText('') #Коэф налогов 4
            self.data['lineedit'][12][11].setText('') #Содержание жилплощади 5
            self.data['lineedit'][12][10].setText('') #Газ 6
            self.data['lineedit'][12][5].setText('') #Дополнительные расходы 7
            self.data['lineedit'][12][0].setText('') #Кап ремонт 8
            self.data['lineedit'][12][6].setText('') #Домофон 9
            self.data['lineedit'][12][12].setText('') #Обслуживание газа 10
            self.data['lineedit'][12][7].setText('') #ТКО 11
            self.data['lineedit'][12][3].setText('') #Дата оплаты 12
            

            #QCheckBox [trur, false]
            self.data['QCheckBox'][12][10].setChecked(True) #Электроэнергия 0
            self.data['QCheckBox'][12][2].setChecked(True) #Отопление 1
            self.data['QCheckBox'][12][3].setChecked(True) #Вода 2
            self.data['QCheckBox'][12][1].setChecked(True) #Водоотведение 3
            self.data['QCheckBox'][12][6].setChecked(True) #Коэф налогов 4
            self.data['QCheckBox'][12][8].setChecked(True) #Содержание жилплощади 5
            self.data['QCheckBox'][12][7].setChecked(True) #Газ 6
            self.data['QCheckBox'][12][12].setChecked(True) #Дополнительные расходы 7
            self.data['QCheckBox'][12][11].setChecked(True) #Кап ремонт 8
            self.data['QCheckBox'][12][4].setChecked(True) #Домофон 9
            self.data['QCheckBox'][12][5].setChecked(True) #Обслуживание газа 10
            self.data['QCheckBox'][12][0].setChecked(True) #ТКО 11

            #Обновляем графики
            self.UpdateGrafic()

    #Нажатие отмена в редактировании и в создании квитанции
    def signCloseReceipt(self):
        
        #Стереть все данные в форме
        self.data['lineedit'][12][8].setText('') #Электроэнергия 0
        self.data['lineedit'][12][2].setText('') #Отопление 1
        self.data['lineedit'][12][9].setText('') #Вода 2
        self.data['lineedit'][12][1].setText('') #Водоотведение 3
        self.data['lineedit'][12][4].setText('') #Коэф налогов 4
        self.data['lineedit'][12][11].setText('') #Содержание жилплощади 5
        self.data['lineedit'][12][10].setText('') #Газ 6
        self.data['lineedit'][12][5].setText('') #Дополнительные расходы 7
        self.data['lineedit'][12][0].setText('') #Кап ремонт 8
        self.data['lineedit'][12][6].setText('') #Домофон 9
        self.data['lineedit'][12][12].setText('') #Обслуживание газа 10
        self.data['lineedit'][12][7].setText('') #ТКО 11
        self.data['lineedit'][12][3].setText('') #Дата оплаты 12
        

        #QCheckBox [trur, false]
        self.data['QCheckBox'][12][10].setChecked(True) #Электроэнергия 0
        self.data['QCheckBox'][12][2].setChecked(True) #Отопление 1
        self.data['QCheckBox'][12][3].setChecked(True) #Вода 2
        self.data['QCheckBox'][12][1].setChecked(True) #Водоотведение 3
        self.data['QCheckBox'][12][6].setChecked(True) #Коэф налогов 4
        self.data['QCheckBox'][12][8].setChecked(True) #Содержание жилплощади 5
        self.data['QCheckBox'][12][7].setChecked(True) #Газ 6
        self.data['QCheckBox'][12][12].setChecked(True) #Дополнительные расходы 7
        self.data['QCheckBox'][12][11].setChecked(True) #Кап ремонт 8
        self.data['QCheckBox'][12][4].setChecked(True) #Домофон 9
        self.data['QCheckBox'][12][5].setChecked(True) #Обслуживание газа 10
        self.data['QCheckBox'][12][0].setChecked(True) #ТКО 11

        #Стереть все данные в форме
        self.data['lineedit'][5][8].setText('') #Электроэнергия 0
        self.data['lineedit'][5][2].setText('') #Отопление 1
        self.data['lineedit'][5][9].setText('') #Вода 2
        self.data['lineedit'][5][1].setText('') #Водоотведение 3
        self.data['lineedit'][5][4].setText('') #Коэф налогов 4
        self.data['lineedit'][5][11].setText('') #Содержание жилплощади 5
        self.data['lineedit'][5][10].setText('') #Газ 6
        self.data['lineedit'][5][5].setText('') #Дополнительные расходы 7
        self.data['lineedit'][5][0].setText('') #Кап ремонт 8
        self.data['lineedit'][5][6].setText('') #Домофон 9
        self.data['lineedit'][5][12].setText('') #Обслуживание газа 10
        self.data['lineedit'][5][7].setText('') #ТКО 11
        self.data['lineedit'][5][3].setText('') #Дата оплаты 12
        

        #QCheckBox [trur, false]
        self.data['QCheckBox'][5][10].setChecked(True) #Электроэнергия 0
        self.data['QCheckBox'][5][2].setChecked(True) #Отопление 1
        self.data['QCheckBox'][5][3].setChecked(True) #Вода 2
        self.data['QCheckBox'][5][1].setChecked(True) #Водоотведение 3
        self.data['QCheckBox'][5][6].setChecked(True) #Коэф налогов 4
        self.data['QCheckBox'][5][8].setChecked(True) #Содержание жилплощади 5
        self.data['QCheckBox'][5][7].setChecked(True) #Газ 6
        self.data['QCheckBox'][5][12].setChecked(True) #Дополнительные расходы 7
        self.data['QCheckBox'][5][11].setChecked(True) #Кап ремонт 8
        self.data['QCheckBox'][5][4].setChecked(True) #Домофон 9
        self.data['QCheckBox'][5][5].setChecked(True) #Обслуживание газа 10
        self.data['QCheckBox'][5][0].setChecked(True) #ТКО 11

    #Поиск через lineEdit
    def signSearch(self):
        '''Сигнал поиска по таблице через lineEdit:\n
        - 14.03.1997 Формат (поиск по дате) (также 14.3.1997) (тип 1)
        - 03.1997 Поиск по месяцу (также 3.1997) (тип 2)
        - 1997 Поиск по году (тип 3)
        - Газ/Вода - По ключевым словам (Показывает все строки где были произведены оплаты по данным категориям) (тип 4)
        - None - Ничего не делать
        - '' -  Все строки (тип 6)
        '''

        #Определение тип квитанции
        def CheckTypeReceipt(text):
            '''Определение тип квитанции1'''

            Str = 'электроэнергия, электричество, вода, отопление, водоотведение, коэффициент налогов, коэф, содержание, содержание жилплощади, кап ремонт, капитальный ремонт, капитальный, капитал, домофон, обслуживание газа, обсл газа, обслу газ, газ, тко, дополнительные расходы'.split(', ')

            typeReceipt = None

            #Проверка на тип квитанции
            if '.' in text:
                
                #Находим количество точек
                col = 0
                for i in text:
                    if i == '.':
                        col = col + 1
                
                #Определяем тип квитанции
                if col == 2:
                    typeReceipt = 1
                elif col == 1 and text.split('.')[0] in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '01', '02', '03', '04', '05', '06', '07', '08', '09'):
                    typeReceipt = 2
                else:
                    typeReceipt = 5

            elif text in Str:
                typeReceipt = 4

            elif text != '':
                
                #Проверяем содержит ли строка цифры (если нет то отлавливаем)
                act = True
                for i in text:
                    if i not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                        act = False
                        break

                #Определяем тип
                if act == True:
                    typeReceipt = 3
                else:
                    typeReceipt = 5
            elif text == '' :
                typeReceipt = 6
            else:
                typeReceipt = 5
            
            #Дополнительная проверка
            if typeReceipt == 1:
                if len(text.split('.')[2]) != 4:
                    typeReceipt = 5
            elif typeReceipt == 2:
                if len(text.split('.')[1]) != 4:
                    typeReceipt = 5
            elif typeReceipt == 3:
                if len(text) != 4:
                    typeReceipt = 5
            
            return typeReceipt
        #Переделывает дату в правильный формат
        def DateFormat(data):
            '''Переделывает дату в правильный формат\n
            - data - Данные 13.1.2019 --> 13.01.2019 или массив данных'''

            data = data.split('.')
            if data[0] not in ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'):
                i = f'0{data[0]}'
                data[0] = i
                data = '.'.join(data)
                return data
            else:
                data = '.'.join(data)
                return data
        #Определение тип колонки для поиска в бд
        def sheckTypeReceipt(text):
            '''Определение тип колонки для поиска в бд\n
            - text - Введенный текст в Lineedit'''
            
            if text in ('электроэнергия', 'электричество'):
                vivod = 2
            elif text == 'вода':
                vivod = 3
            elif text == 'отопление':
                vivod = 4
            elif text == 'водоотведение':
                vivod = 5
            elif text in ('коэффициент налогов', 'коэф'):
                vivod = 6
            elif text in ('содержание', 'содержание жилплощади'):
                vivod = 7
            elif text in ('кап ремонт', 'капитальный ремонт', 'капитальный', 'капитал'):
                vivod = 8
            elif text == 'домофон':
                vivod = 9
            elif text in ('обслуживание газа', 'обсл газа', 'обслу газ'):
                vivod = 10
            elif text == 'газ':
                vivod = 11
            elif text == 'тко':
                vivod = 12
            elif text == 'дополнительные расходы':
                vivod = 13
            return vivod

        #Поиск и фильтрация по типу квитанции и вывод отсортированного массива
        def SortingReceipt(text, old_data, typeReceipt):
            '''Поиск и фильтрация по типу квитанции и вывод отсортированного массива\n
            - text - Текст введеный в lineedit
            - old_data - Входной массив данных (таблицы) (длина - 15)
            - typeReceipt - Определенный тип квитанции'''

            if typeReceipt == 1:

                #Проверка что текст введен в нужном формате
                if text.split('.')[1] not in ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'):
                    text = text.split('.'); text[1] = f'0{text[1]}'; text = '.'.join(text)

                new_data = [i for i in old_data if i[14].split(' ')[0] == text]
                return new_data
            
            elif typeReceipt == 2:
                text = DateFormat(text)
                new_data = [i for i in old_data if text.split('.') == i[14].split(' ')[0].split('.')[1:]]
            
                return new_data
            
            elif typeReceipt == 3:
                new_data = [i for i in old_data if text == (i[14].split(' ')[0]).split('.')[2]]
                return new_data

            elif typeReceipt == 4:
                
                index = sheckTypeReceipt(text) #Определяем индекс нужной нам колонки
                new_data = [i for i in old_data if i[index] != None]
                return new_data

            elif typeReceipt == 5:
                pass
            
            elif typeReceipt == 6:
                new_data = self.JobBD._readReturnBD(f'SELECT * FROM СЧЕТА WHERE id_адреса={self.indexCombobox[0]};')
                new_data = list(new_data)
                return new_data
            


        #Получение текста
        text = self.data['lineedit'][3][0].text()
        text = text.lower()

        #Определение тип квитанции
        typeReceipt = CheckTypeReceipt(text)
        data = list(self.JobBD._readReturnBD(f'SELECT * FROM СЧЕТА WHERE id_адреса={self.indexCombobox[0]};'))
        
        #Производим фильтрацию по признаку
        new_data = SortingReceipt(text, data, typeReceipt)

        #Редактируем таблицу
        self.model.clear()
        self.model.setHorizontalHeaderLabels([
            'id_счета',
            'id_адреса',
            'Электроэнергия',
            'Вода', 
            'Отопление', 
            'Водоотведение', 
            'Коэф\nналогов', 
            'Содержание\nжилплощади', 
            'Кап\nремонт', 
            'Домофон', 
            'Обслуживание\nгаза', 
            'Газ', 
            'ТКО', 
            'Дополнительные\nрасходы', 
            'Дата\nсоздания', ])
        self.data['table'][3][0].setColumnHidden(0, True)
        self.data['table'][3][0].setColumnHidden(1, True)

        if typeReceipt != 5:
            #Добавить к модели колонки и строки из бд
            for row in range(len(new_data)):

                row1 = list(new_data[row])

                for column in range(len(row1)):

                    if column not in (0, 1) and row1[column] in ('NULL', 'Null', None):
                        row1[column] = 0

                    if column == 14:
                        row1[column] = row1[column].split(' ')[0]


                    item=QStandardItem(str(row1[column]))
                    self.model.setItem(row,column,item)

        #self.data['table'][3][0].update()
    
    #---------------------------------------------------------------------------------------------
    #СЦЕНАРИИ АНАЛИТИКИ

    #Развертка графиков
    def ScanGrafic(self):

        #Проверка на задвоение
        if self.trigerGrafic == True:
            self.canvas_1.figure.clear()
            self.canvas_2.figure.clear()
            self.canvas_1.draw()
            self.canvas_2.draw()

        #Проверка что имеются какие либо года
        if len(self.DataAnalitic['YearPopular']) > 0:

            #Определяем год (Берем самый старший год)
            year = self.DataAnalitic['YearPopular'][0]

            #Получаем массив суммы по месяцам (по все расходам)
            summa_exenses = self.Analitic._TypeMonthData(year)

            #Месяца года
            month_year = ('Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь')

            #Создаем график
            color = '#CE8632'


            self.ax1 = self.canvas_1.figure.subplots()
            self.ax1.plot(month_year, summa_exenses, marker='o', lw='2.2', ms='4.1', mfc=color, mec=color)
            
            self.ax1.set_xticklabels(month_year, fontsize=7, color=color)
            self.ax1.set_yticklabels([], fontsize=7, color=color)
            
            for i, j in zip(month_year, summa_exenses):
                self.ax1.annotate(str(int(j)), xy=(i, j), xytext=(0, 8), textcoords='offset points', ha='center', fontsize=6.3, color=color)
            
            self.ax1.set_facecolor((1.0, 1.0, 1.0, 0))
            self.ax1.set_position([0.02, 0.14, 0.97, 0.765])

            self.canvas_1.draw()

            # Выводим проценты и проверяем, нужно ли выводить 0%
            def my_autopct(pct):
                return '{:.1f}%'.format(pct) if pct > 0 else ''

            #Создаем график №2 (круговой по типу данных)
            self.ax2 = self.canvas_2.figure.subplots()
            self.ax2.pie(self.Analitic.ExpensesType(year), colors = ('#E6F42A', '#5089CC', '#FF0000', '#72510F', '#FF71F2', '#6CF251', '#FF9700', '#C4BC90', '#4D0051', '#BFBFBF', '#630034', '#FFFFFF'), explode=(0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05), autopct=my_autopct, textprops={'fontsize': 6, 'color': '#029395', 'weight': 'bold'})

            self.ax2.set_position([-0.1, -0.1, 1.18, 1.18])

            self.trigerGrafic = True
            self.canvas_2.draw()

    #Обновление графика
    def UpdateGrafic(self):
        
        #Обновляем Combobox в аналитике
        self.combobox[2][0].clear()
        self.Analitic.returnUpdate_3()
        [self.combobox[2][0].addItem(str(i)) for i in self.DataAnalitic['YearPopular']]

        #Обновляем данные
        self.Analit.returnUpdate_3()

        #Производим расчеты
        if len(self.DataAnalitic['YearPopular']) > 0:

            #Проверка на задвоение
            if self.trigerGrafic == True:
                self.canvas_1.figure.clear()
                self.canvas_2.figure.clear()

            #Определяем год (Берем самый старший год)
            year = self.DataAnalitic['YearPopular'][0]

            #Получаем массив суммы по месяцам (по все расходам)
            summa_exenses = self.Analitic._TypeMonthData(year)

            #Месяца года
            month_year = ('Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь')

            #Создаем график
            color = '#CE8632'


            self.ax1 = self.canvas_1.figure.subplots()
            self.ax1.plot(month_year, summa_exenses, marker='o', lw='2.2', ms='4.1', mfc=color, mec=color)
            
            self.ax1.set_xticklabels(month_year, fontsize=7, color=color)
            self.ax1.set_yticklabels([], fontsize=7, color=color)
            
            for i, j in zip(month_year, summa_exenses):
                self.ax1.annotate(str(int(j)), xy=(i, j), xytext=(0, 8), textcoords='offset points', ha='center', fontsize=6.3, color=color)
            
            self.ax1.set_facecolor((1.0, 1.0, 1.0, 0))
            self.ax1.set_position([0.02, 0.14, 0.97, 0.765])

            self.canvas_1.draw()

            # Выводим проценты и проверяем, нужно ли выводить 0%
            def my_autopct(pct):
                return '{:.1f}%'.format(pct) if pct > 0 else ''

            #Создаем график №2 (круговой по типу данных)
            self.ax2 = self.canvas_2.figure.subplots()
            self.ax2.pie(self.Analitic.ExpensesType(year), colors = ('#E6F42A', '#5089CC', '#FF0000', '#72510F', '#FF71F2', '#6CF251', '#FF9700', '#C4BC90', '#4D0051', '#BFBFBF', '#630034', '#FFFFFF'), explode=(0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05), autopct=my_autopct, textprops={'fontsize': 6, 'color': '#029395', 'weight': 'bold'})

            self.ax2.set_position([-0.1, -0.1, 1.18, 1.18])

            self.trigerGrafic = True
            self.canvas_2.draw()

    #Переключение QComboBox
    def signComboBox(self):

        if len(self.DataAnalitic['YearPopular']) > 0:
            #Выбранный год в ComboBox
            year = str(self.combobox[2][0].currentText())

            #Стераем все графики
            #self.canvas_1.figure.clear()
            #self.canvas_2.figure.clear()

            #Получаем массив суммы по месяцам (по все расходам)
            summa_exenses = self.Analitic._TypeMonthData(year)

            #Месяца года
            month_year = ('Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь')

            #Создаем график
            color = '#CE8632'

            self.canvas_1.figure.clear()

            self.ax1 = self.canvas_1.figure.subplots()
            self.ax1.plot(month_year, summa_exenses, marker='o', lw='2.2', ms='4.1', mfc=color, mec=color)
            
            self.ax1.set_xticklabels(month_year, fontsize=7, color=color)
            self.ax1.set_yticklabels([], fontsize=7, color=color)
            
            for i, j in zip(month_year, summa_exenses):
                self.ax1.annotate(str(int(j)), xy=(i, j), xytext=(0, 8), textcoords='offset points', ha='center', fontsize=6.3, color=color)
            
            self.ax1.set_facecolor((1.0, 1.0, 1.0, 0))
            self.ax1.set_position([0.02, 0.14, 0.97, 0.765])

            self.canvas_1.draw()

            # Выводим проценты и проверяем, нужно ли выводить 0%
            def my_autopct(pct):
                return '{:.1f}%'.format(pct) if pct > 0 else ''

            self.canvas_2.figure.clear()

            self.ax2 = self.canvas_2.figure.subplots()
            self.ax2.pie(self.Analitic.ExpensesType(year), colors = ('#E6F42A', '#5089CC', '#FF0000', '#72510F', '#FF71F2', '#6CF251', '#FF9700', '#C4BC90', '#4D0051', '#BFBFBF', '#630034', '#FFFFFF'), explode=(0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05), autopct=my_autopct, textprops={'fontsize': 6, 'color': '#029395', 'weight': 'bold'})

            self.ax2.set_position([-0.1, -0.1, 1.18, 1.18])
            self.canvas_2.draw()
    #---------------------------------------------------------------------------------------------


def run():
        

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    program = Program()

    sys.exit(app.exec_())
        

if __name__ == '__main__':

    run()