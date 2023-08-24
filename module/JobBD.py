# -*- coding: utf-8 -*-
import sqlite3



class JobBD:
    '''Модуль работы с базой данных'''

    def __init__(self):
        
        self._variables()

        self.db = sqlite3.connect(self.path)
        self.cur = self.db.cursor()
    
    #============================================================================================================
    #Движок

    #Переменные
    def _variables(self):
        
        self.data = ('''PRAGMA foreign_keys=on;''',
        '''
        CREATE TABLE АДРЕС (
        id_адреса INTEGER PRIMARY KEY AUTOINCREMENT,
        Адрес TEXT CONSTRAINT Адрес NOT NULL UNIQUE
        );''',
        '''
        CREATE TABLE СЧЕТА (
        id_счета INTEGER PRIMARY KEY AUTOINCREMENT,
        id_адреса INTEGER,
        Электроэнергия REAL,
        Вода REAL,
        Отопление REAL,
        Водоотведение REAL,
        Коэффициент_налогов REAL,
        Содержание_жилплощади REAL,
        Кап_ремонт REAL,
        Домофон REAL,
        Обслуживание_газа REAL,
        Газ REAL,
        ТКО REAL,
        Дополнительные_расходы REAL,
        Дата_создания REAL,
        FOREIGN KEY (id_адреса) REFERENCES АДРЕС(id_адреса) ON DELETE CASCADE ON UPDATE CASCADE
        );
        ''',
        '''
        CREATE TABLE СТАТУС_СЧЕТА (
        id_счета INTEGER CONSTRAINT id_счета NOT NULL UNIQUE,
        Электроэнергия BOOLEAN,
        Вода BOOLEAN,
        Отопление BOOLEAN,
        Водоотведение BOOLEAN,
        Коэффициент_налогов BOOLEAN,
        Содержание_жилплощади BOOLEAN,
        Кап_ремонт BOOLEAN,
        Домофон BOOLEAN,
        Обслуживание_газа BOOLEAN,
        Газ BOOLEAN,
        ТКО BOOLEAN,
        Дополнительные_расходы BOOLEAN,
        FOREIGN KEY (id_счета) REFERENCES СЧЕТА (id_счета) ON DELETE CASCADE ON UPDATE CASCADE
        );
        ''')

        self.path = 'db/Utility_bills.db'


    #Запрос к бд
    def _readBD(self, request):

        self.cur.execute('PRAGMA foreign_keys=on')
        self.db.commit()

        self.cur.execute(request)
        self.db.commit()

    #Запрос к бд с выводом
    def _readReturnBD(self, request):
        
        self.cur.execute('PRAGMA foreign_keys=on')
        self.db.commit()

        self.cur.execute(request)
        self.db.commit()
        data = self.cur.fetchall()

        return data

    #Записать новую базу данных
    def _writeBD(self):
        for i in self.data:
            self.cur.execute(i)
            self.db.commit()

    #Запрос и получение номера id запроса
    def _requestID(self, request):
        self.cur.execute('PRAGMA foreign_keys=on')
        self.db.commit()

        self.cur.execute(request)
        last_row_id = self.cur.lastrowid

        self.db.commit()

        return last_row_id

    #Завершить работу с бд
    def _closeBD(self):
        self.db.close()

if __name__ == '__main__':


    a = JobBD()
    #a._readBD('INSERT INTO АДРЕС VALUES (3, "Адрес_3");')
    b = a._requestID('INSERT INTO СЧЕТА (id_адреса, Электроэнергия, Вода, Отопление, Водоотведение, Коэффициент_налогов, Содержание_жилплощади, Кап_ремонт, Домофон, Обслуживание_газа, Газ, ТКО, Дополнительные_расходы, Дата_создания) VALUES (1, "Null", "Null", 1, "Null", "Null", "Null", "Null", "Null", "Null", "Null", "Null", "Null", "17.06.2023 2:57:17");')
    print(b)





