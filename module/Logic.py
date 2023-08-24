# -*- coding: utf-8 -*-
import numpy as np
import datetime
import os
import json
from loguru import logger

import JobBD


class Search:
    '''Модуль работы с поиском'''

    def __init__(self):
        pass
    
    #Вход информации
    def _unputData(self):
        pass

    #Выход информации
    def _returnData(self):
        pass


class Logic:
    '''Логика приложения'''
    
    #Определение тип времени суток
    def typeTimeDay(self):
    
    #Тип дня
        self.TimeDay = np.array(( 
            'Доброе утро!',
            'Добрый день!',
            'Добрый вечер!',
            'Доброй ночи!',
        ))

        date = datetime.datetime.now().time()

        if date > datetime.time(4) and date < datetime.time(12):
            vivod = self.TimeDay[0]
        elif date > datetime.time(12) and date < datetime.time(17):
            vivod = self.TimeDay[1]
        elif date >  datetime.time(17) and date < datetime.time(23, 59, 59):
            vivod = self.TimeDay[2]
        elif date >  datetime.time(0) and date < datetime.time(4):
            vivod = self.TimeDay[3]
        
        return vivod

    #Для определения последнего захода
    def old_zahod(self, data):
        """
        Args:
            data (словарь): старые данные с config

        Returns:
            _type_: _description_
        """

        data = data['last_coming'].split(' ')
        
        date = data[0].split('-'); data = data[1].split(':')

        if data[0] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            data[0] = f'0{data[0]}'

        if data[1] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            data[1] = f'0{data[1]}'


        date = f'{date[2]}.{date[1]}.{date[0]}'; data = f'{data[0]}:{data[1]}'

        data = f'<html><body>Последнее посещение: <span style=color: #08DA9D;>{date} {data}</span></body></html>'

        return data




class JobFile:
    '''Модуль работы с файловой системой'''

    def __init__(self):
        
        self.pathBD = 'Utility_bills.db' #Название файла с базой данных
        self.pathFolderBD = 'db' #Название папки где хранится база данных

    #=========================================================================================================
    #Движок

    #Дефолтные данные для json
    def _defoltData(self):

        defolData = {
            'pathBD': 'Utility_bills.db', #Название файла с базой данных
            'pathFolderBD': 'db', #Название папки где хранится база данных
            'pathJson': 'config.json', #Путь и название конфигурационного файла
            'last_coming': f'{datetime.datetime.now()}' #Последний заход в программу
        }
        return defolData
    
    #Проверка наличия файла или папки
    def _checkFile(self, name: str, path=None):
        '''Проверка наличия файла\n
        path - Путь (если нет то "")\n
        name - Название файла или папки'''

        #Получить список всех обьектов
        listFile = os.listdir(path)

        if name in listFile:
            return True
        else:
            return False
    
    #Создать файл
    def _newFile(self, path: str):
        '''Созать файл\n
        path - Путь к файлу (если есть) и название файла'''

        with open(path, 'w', encoding='utf-8') as file1:
            file1.write('')
    
    #Читать файл json
    def _readJson(self, path: str):
        with open(path, encoding='utf-8') as file1:
            data = json.load(file1)
            return data
    
    #Создание json
    def _createJson(self, path: str, data):
        with open(path, 'w', encoding='utf-8') as file1:
            json.dump(data, file1, indent=3, ensure_ascii=False)
    
    #Проверка инфраструктуры и запуск
    def checkStartForm(self):
        self.checJson()
        self.scanDB()

    #=========================================================================================================
    #Функциональные


    #Проверка есть ли файл и папка где хранится база данных (если нет то создать)
    def scanDB(self):
        
        #Проверка на наличия папки где хранится база данных
        if self._checkFile(self.pathFolderBD) == True:
            
            #Проверка создан ли файл с базой данных
            if self._checkFile(self.pathBD, self.pathFolderBD) == False:
                
                #если нет то создать
                self._newFile(f'{self.pathFolderBD}/{self.pathBD}')

                #Записать базу данных
                bd = JobBD.JobBD()
                bd._writeBD()
                bd._closeBD()

        else:
            #Если нет папки то создать
            os.mkdir(self.pathFolderBD)

            #Создать базу данных
            self._newFile(f'{self.pathFolderBD}/{self.pathBD}')

            #Записать базу данных
            bd = JobBD.JobBD()
            bd._writeBD()
            bd._closeBD()

    #Проверка и в случае чего создания файла json (в случае если есть то меняет дату входа)
    def checJson(self, path = 'config.json'):

        #Проверка создан ли файл json в корневой папке
        if self._checkFile(path) == False:
            
            #Получить дефолтные данные
            data = self._defoltData()
            data['last_coming'] = str(datetime.datetime.now())
            self.old_data = data.copy()

            #Создать файл json
            self._createJson(path, data)

        else:
            data = self._readJson('config.json')

            self.old_data = data.copy()

            date = datetime.datetime.now()
            data['last_coming'] = str(date)

            self._createJson('config.json', data)

    #Получение старых данных
    def returnOldData(self):
        
        return self.old_data


class Log:
    '''Логиирование'''
    
    def __init__(self, func):
        
        try:

            func()

        except Exception as bag:

            logger.add('Debag/debag.log', format="{time:HH:mm:ss} {message}", level='DEBUG', rotation='1 year')
            
            bag = f'Ошибка: "{bag}", в строке {bag.__traceback__.tb_lineno}'
            
            logger.debug(bag)
    


if __name__ == '__main__':
    #a = Logic()
    #a.typeTimeDay()

    a = Logic()
    Log(lambda: print(1/0))
