from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import sys

sys.path.append('Logic')
sys.path.append('module')

import os
import Logic

from Главное_меню import Ui_MainWindow as Gl_Main
from Аналитика import Ui_MainWindow as Analitic
from Добавить import Ui_MainWindow as Add_Main
from Индетификация import Ui_MainWindow as Indefication
from Оповещения import Ui_MainWindow as Opoweshenie
from Посмотреть_квитанцию import Ui_MainWindow as Check_kvitanc
from Создать_адрес import Ui_MainWindow as New_adress
from Удалить_адрес import Ui_MainWindow as Delete_adres
from Выбор_адреса_для_удаления import Ui_MainWindow as Check_adres_del
from Статистика import Ui_MainWindow as Statistica
from Выход import Ui_MainWindow as ExitMain
from Удалить_адрес import Ui_MainWindow as Del_Adres
from Удалить_квитанцию import Ui_MainWindow as DeleteReceipt
from Редактировать_квитанцию import Ui_MainWindow as EditReceipt

import time
#import ParseObject


class block1:
    '''Добавление виджетов, заголовков виджетов и насначение сценариев'''

    def __init__(self):

        self._variables()
        self._formWin()
        self._add_widget()
        self.obh_title()

    def checkTime(fun):

        def block(*arg):
            time1 = time.time()
            a = fun(*arg)
            time2 = time.time() - time1
            print(f'Время выполнения: {round(time2, 3)}')
            return a
        
        return block

    #Переменные
    def _variables(self):
        
        #Начальная страница индентификации
        self.name_form = ('Indefication', #0
                          'Gl_Main', #Главное меню 1
                          'Analitic', #Окно аналитики 2
                          'Check_kvitanc', #Посмотреть квитанцию 3
                          'Statistica' #Статистика 4
                          )
        self.name_form_2 = (
            'Add_Main', #Добавить квитанцию 0
            'Opoweshenie', #Отдельное окно оповещение 1
            'New_adress', #Создать новый адрес 2
            'Check_adres_del', #Выбор адреса для удаления 3
            'ExitMain', #Меню выхода 4
            'Del_Adres', #Удаление квитанции
            'DeleteReceipt', #Удалить квитанцию
            'EditReceipt' #Редактировать квитанцию
        )
        
        #Тип расходов
        self.nameTypeExpenses = (
            'Электроэнергия',
            'Отопление',
            'Вода',
            'Водоотведение',
            'Коэффициент налогов',
            'Содержание жилплощади',
            'Газ',
            'Капитальный ремонт',
            'Домофон',
            'Обслуживание газа',
            'ТКО',
            'Дополнительные расходы',
        )

        #Выбранный item в combobox (Индетификация) (1 - индекс; 2 - текст)
        self.indexCombobox = [0, '']
        
        #Формы для переходов
        self.Form = QStackedWidget()

        #Формы для переходов отдельных окон
        self.Form_2 = QStackedWidget()
        
        #Заголовки
        self.title = []
        self.title_2 = []

        #Все переменные QLabel
        self.label = []

        #Все переменные QPushButton
        self.button = []

        #Все остальные переменные
        self.lineedit = []
        self.table = []
        self.combobox = []
        self.listwidget = []
        self.QCheckBox = []

    #-------------------------------------------------------------------------------
    #Развертка

    #Развертка форм
    def _formWin(self):

        #Развертка форм и добавление списков
        self.FormUI = [Start(eval(f'{i}')) for i in self.name_form]
        self.FormUI_2 = [Start(eval(f'{i}')) for i in self.name_form_2]

        

        #Добавить формы в переходы
        [self.Form.addWidget(i) for i in self.FormUI]

        #Добавить отдельные окна для переходов
        [self.Form_2.addWidget(i) for i in self.FormUI_2]

        #ParseObject.Pars(self.FormUI + self.FormUI_2)

    #Получение всех заголовок
    def obh_title(self):

        self.title = [self.FormUI[i].windowTitle() for i in range(len(self.FormUI))]
        self.title_2 = [self.FormUI_2[i].windowTitle() for i in range(len(self.FormUI_2))]
    
    #Добавление всех виджетов
    def _add_widget(self):

        for i in self.FormUI:
            
            #Добавление кнопок
            self.button.append([i1 for i1 in i.findChildren(QPushButton)])

            #Добавление Qlabel
            self.label.append([i1 for i1 in i.findChildren(QLabel)])

            #Добавление qcombobox
            self.combobox.append([i1 for i1 in i.findChildren(QComboBox)])

            #Добавление table
            self.table.append([i1 for i1 in i.findChildren(QTableView)])
            
            #Добавление qlineedit
            self.lineedit.append([i1 for i1 in i.findChildren(QLineEdit)])

            #Добавление qlistwidget
            self.listwidget.append([i1 for i1 in i.findChildren(QListWidget)])

            #Добавление QCheckBox
            self.QCheckBox.append([i1 for i1 in i.findChildren(QCheckBox)])

        for i in self.FormUI_2:
            
            #Добавление кнопок
            self.button.append([i1 for i1 in i.findChildren(QPushButton)])

            #Добавление Qlabel
            self.label.append([i1 for i1 in i.findChildren(QLabel)])

            #Добавление qcombobox
            self.combobox.append([i1 for i1 in i.findChildren(QComboBox)])

            #Добавление table
            self.table.append([i1 for i1 in i.findChildren(QTableView)])
            
            #Добавление qlineedit
            self.lineedit.append([i1 for i1 in i.findChildren(QLineEdit)])

            #Добавление qlistwidget
            self.listwidget.append([i1 for i1 in i.findChildren(QListWidget)])

            #Добавление QCheckBox
            self.QCheckBox.append([i1 for i1 in i.findChildren(QCheckBox)])
        
        self.label[7][1].setText('')

    #Перевод чисел в удобный вид 1000 --> 1 000
    def _convertNumber(self, number):

        number = str(number)
        number1 = '' #Плавающая точка

        if number[-2:] == '.0':
            print(f'{number} <----')

            number = number.split('.')[0]
            print(f'----> {number}')

        elif '.' in number:
            print(f'{number} <----')
            number1 = number.split('.')
            number = number1[0]; number1 = f'.{number1[1]}'
            print(f'----> {number}')


        if len(number) == 4:
            number = number[:1] + ' ' + number[1:] + number1

        elif len(number) == 5:
            number = number[:2] + ' ' + number[2:] + number1

        elif len(number) == 6:
            number = number[:3] + ' ' + number[3:] + number1

        elif len(number) == 7:
            number = number[:1] + ' ' + number[1:4] + ' ' + number[4:] + number1

        elif len(number) == 8:
            number = number[:2] + ' ' + number[2:5] + ' ' + number[5:] + number1

        elif len(number) == 9:
            number = number[:3] + ' ' + number[3:6] + ' ' + number[6:] + number1

        elif len(number) == 10:
            number = number[:1] + ' ' + number[1:4] + ' ' + number[4:7] + ' ' + number[7:] + number1
        
        return str(number)
    #-------------------------------------------------------------------------------
    #Выводы

    #Данные
    def returnData(self):
        
        self.data = {
            'FormUI': self.FormUI,
            'FormUI_2': self.FormUI_2,
            'Form': self.Form, #Стек 1
            'Form_2': self.Form_2, #Стек 2
            'name_form': self.name_form, #Название 1 группы
            'name_form_2': self.name_form_2, #Название 2 группы
            'nameTypeExpenses': self.nameTypeExpenses, #Тип расходов
            'indexCombobox': self.indexCombobox, #Выбранный item в combobox (Индетификация) (1 - индекс; 2 - текст)
            'title': self.title, #Титульники для 1 группы
            'title_2': self.title_2, #Титульники для 2 группы
            'label': self.label, 
            'button': self.button,
            'lineedit': self.lineedit,
            'table': self.table,
            'combobox': self.combobox,
            'listWidget': self.listwidget,
            'QCheckBox': self.QCheckBox,
            'QMenu': QMenu(self.table[3][0])
        }
        return self.data

        #return self.label

    #Создание файла и проверка файла (для запуска в единственном экземпляре)
    def checkFile(ind: int):
        '''Проверяет есть ли файл запуска (что бы предотвратить запуск дупликата\n
        ind - (1 - Вход; 2 - выход))'''

        #Вход
        if ind == 1:

            #Проверка есть ли файл
            if 'startMain.txt' not in os.listdir():

                with open('startMain.txt', 'w', encoding='utf-8') as file1:
                    file1.write('')
                
                return True
            
            else:

                return False
            
        #Выход
        elif ind == 2:
            
            os.remove('startMain.txt')

    #-------------------------------------------------------------------------------
#Развертка
class Start(QMainWindow):
    '''Развертка'''
    def __init__(self, Main):
        super(Start, self).__init__()
        self.Main = Main()
        self.Main.setupUi(self)
    #-------------------------------------------------------------------------------



if __name__ == '__main__':

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)


    block1 = block1()
    a = block1._convertNumber(1000)
    print(a)
    sys.exit(app.exec_())