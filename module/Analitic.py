# -*- coding: utf-8 -*-
from JobBD import JobBD
import datetime
import numpy as np
import math
import time


class Analitic:
    '''Модуль для аналитики данных из бд'''

    def __init__(self, index):
        '''index - Индекс адреса'''

        self._variables()

        self.index = index
        self.data_14(self.index)

        self.data['colZapisey_1'] = self.colZapisey_1()
        self.data['ExpensesPerYear_12'] = self.ExpensesPerYear_12()
        self.data['KolZapMes_3'] = self.KolZapMes_3()
        self.data['NumberEntriesLastMonth_11'] = self.NumberEntriesLastMonth_11()
        self.data['TotalNumberExpenses_9'] = self.TotalNumberExpenses_9()
        self.data['indexsMonth'] = self._indexsMonth()
        self.data['srednKolZap_2'] = self.srednKolZap_2()
        self.data['AverageMonthlyExpenses_7'] = self.AverageMonthlyExpenses_7()
        self.data['ObhRashod_4'] = self._TypeMonthData(str(datetime.datetime.now().date()).split(' ')[0].split('-')[0])
        self.data['MaxRashod_5'] = self.MaxRashod_5()
        self.data['MonthMinExpenses_6'] = self.MonthMinExpenses_6()
        self.data['inflationFromLastYear_8'] = self.inflationFromLastYear_8()
        self.data['MostExpendableItem_10'] = self.MostExpendableItem_10()
        self.data['notPaidYear_13'] = self.notPaidYear_13()
        self.data['YearPopular'] = self.YearPopular()
    
    #Обновление для нескольких строк
    def returnUpdate(self):
        '''Обновление для нескольких строк\n
        Выводит:\n
        -Количество записей в этом месяце\n
        -Не оплачено в этом году\n
        -Количество записей в прошлом месяце\n
        -Самая расходная статья расходов'''
        
        self.data_14(self.index)
        a = self.KolZapMes_3()
        b = self.notPaidYear_13()
        c = self.NumberEntriesLastMonth_11()
        d = self.MostExpendableItem_10()

        return (a, b, c, d)
    
    def returnUpdate_2(self):
        '''Обновление для нескольких строк\n
        Выводит:\n
        -Общее количество расходов\n
        -Расходы за этот год\n'''
        
        self.data_14(self.index)

        a = self.TotalNumberExpenses_9()
        b = self.ExpensesPerYear_12()
        return (a, b)

    #Обновление для графиков
    def returnUpdate_3(self):

        self.data_14(self.index)
        self.data['YearPopular'] = self.YearPopular() #Все года
    
        

    #--------------------------------------------------------------------------------------
    def _variables(self):
        self.data = {
            'itemText': np.array([]), #индекс/текст ---
            'colZapisey_1': 0, #Количество записей ---
            'srednKolZap_2': 0, #Среднее количество записей в месяц ---
            'KolZapMes_3': 0, #Количество записей в данном месяце ---
            'ObhRashod_4': np.array([]), #Все расходы по месяцам --- [0, 100...] ---
            'MaxRashod_5': 0, #Самый расходный месяц ---
            'MonthMinExpenses_6': 0, #Месяц с минимальными расходами ---
            'AverageMonthlyExpenses_7': 0, #Средние расходы в месяц ---
            'inflationFromLastYear_8': 0, #Инфляция с прошлым годом ---
            'TotalNumberExpenses_9': 0, #Общее количество расходов (р.) ---
            'MostExpendableItem_10': 0, #Самая расходная статья расходов (тип) ---
            'NumberEntriesLastMonth_11': 0, #Количество записей в прошлом месяце ---
            'ExpensesPerYear_12': 0, #Расходы за этот год ---
            'notPaidYear_13': 0, #Всего не оплачено (р.) ---
            'data_14': np.array([]), #Все данные счетов по выбранному адресу ---
            'data_oplat': np.array([]), #Данные по оплате по выбранному адресу (в этом году) ---
            'indexsMonth': np.array([]), #Индексы записей по месяцам [[..],[..]] ---
            'YearPopular': np.array([]) #Все импользуемые года
        }
        self.jobBd = JobBD()

        #Список чисел от -5 000 до 5 000
        self.listNumber = (-5001, 5001)

    #-------------------------------------------------------------------------------------
    #Декораторы
    def timeCheck(func):
        def decor(*arg):
            time1 = time.time()
            a = func(*arg)
            time2 = time.time() - time1
            print(f'Время выполнения: {round(time2, 3)} с.')
            return a
        return decor

    #--------------------------------------------------------------------------------------
    #Определение месяца (Принимает 01, 0, 1)
    def _dataMonth(self, month):

        month = str(month)

        if month in ('0', '0'):
            return 'Январь'
        
        elif month in ('01', '1'):
            return 'Февраль'
        
        elif month in ('02', '2'):
            return 'Март'
        
        elif month in ('03', '3'):
            return 'Апрель'
        
        elif month in ('04', '4'):
            return 'Май'
        
        elif month in ('05', '5'):
            return 'Июнь'
        
        elif month in ('06', '6'):
            return 'Июль'
        
        elif month in ('07', '7'):
            return 'Август'
        
        elif month in ('08', '8'):
            return 'Сентябрь'
        
        elif month in ('09', '9'):
            return 'Октябрь'
        
        elif month in '10':
            return 'Ноябрь'
        
        elif month in '11':
            return 'Декабрь'
    
    #Определения процента (вход 0.1)
    def _percent(self, perc: float):
        vivod = perc * 100

        if vivod > self.listNumber[0] and vivod < self.listNumber[1]:
            vivod = int(vivod)
        else:
            vivod = round(vivod, 2)

        return vivod
    
    #Определение инфляции с прошлым годом
    def _inflacia(self, data1, data2):
        '''data1 - Прошлый год\n
        data2 - Текущий год'''

        try:
            vivod = ((data2 / data1) * 100) - 100

            if vivod > self.listNumber[0] and vivod < self.listNumber[1]:
                vivod = int(vivod)
            else:
                vivod = round(vivod, 2)
            
            return vivod
        
        except ZeroDivisionError:
            return 0
    
    #формирования стандарта времени
    def _standartDatetime(self, date: str):
        '''date - время в формате г-м-д ч:м:с.милисек\n
        Возвращает дату в формате: д.м.г ч:м:с.милисек'''

        date = str(date)

        #Парсинг времени и разбитие на данные
        date = date.split(' '); time = date[1]; date = date[0].split('-')

        vivod = f'{date[2]}.{date[1]}.{date[0]} {time}'
        return vivod

    #Индексы записей по месяцам
    def _indexsMonth(self):

        data = self.data['data_14']
        a = ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12')
        vivod = [[], [], [], [], [], [], [], [], [], [], [], []]
        index = 0

        #Получение количество по месяцам
        for i in data:
            
            #Получение месяца и года ['05', '2020']
            date = ['', '']
            date[0] = i[14].split(' ')[0].split('.')[1]; date[1] = i[14].split(' ')[0].split('.')[2]
            
            date_year = str(datetime.datetime.now().date()).split('-')[0] #Получение текущего года
            
            if date[0] == a[0] and date[1] == date_year:
                vivod[0].append(index)

            elif date[0] == a[1] and date[1] == date_year:
                vivod[1].append(index)

            elif date[0] == a[2] and date[1] == date_year:
                vivod[2].append(index)

            elif date[0] == a[3] and date[1] == date_year:
                vivod[3].append(index)

            elif date[0] == a[4] and date[1] == date_year:
                vivod[4].append(index)

            elif date[0] == a[5] and date[1] == date_year:
                vivod[5].append(index)

            elif date[0] == a[6] and date[1] == date_year:
                vivod[6].append(index)

            elif date[0] == a[7] and date[1] == date_year:
                vivod[7].append(index)

            elif date[0] == a[8] and date[1] == date_year:
                vivod[8].append(index)

            elif date[0] == a[9] and date[1] == date_year:
                vivod[9].append(index)

            elif date[0] == a[10] and date[1] == date_year:
                vivod[10].append(index)

            elif date[0] == a[11] and date[1] == date_year:
                vivod[11].append(index)

            index = index + 1

        vivod = np.array(vivod, dtype=object)
        return vivod

    #сумма расходов по месяцам согласно указанному году
    def _TypeMonthData(self, year: str):

        #Отсортируем значения согласно году
        data = [i for i in self.data['data_14'] if i[14].split(' ')[0].split('.')[2] == year]
        
        vivod = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        for i in data:
            
            a = i[14].split(' ')[0].split('.')[1]
            i = i[2:14]
            i = i[i != None]

            if a == '01':
                vivod[0] = vivod[0] + i.sum()
            elif a == '02':
                vivod[1] = vivod[1] + i.sum()
            elif a == '03':
                vivod[2] = vivod[2] + i.sum()
            elif a == '04':
                vivod[3] = vivod[3] + i.sum()
            elif a == '05':
                vivod[4] = vivod[4] + i.sum()
            elif a == '06':
                vivod[5] = vivod[5] + i.sum()
            elif a == '07':
                vivod[6] = vivod[6] + i.sum()
            elif a == '08':
                vivod[7] = vivod[7] + i.sum()
            elif a == '09':
                vivod[8] = vivod[8] + i.sum()
            elif a == '10':
                vivod[9] = vivod[9] + i.sum()
            elif a == '11':
                vivod[10] = vivod[10] + i.sum()
            elif a == '12':
                vivod[11] = vivod[11] + i.sum()
        
        vivod = np.array(vivod)
        return vivod
        
        
                


    #--------------------------------------------------------------------------------------
    #Основные расчеты
    '''
    Вход индекс адреса
    1. Количество записей
    2. Среднее количество записей в месяц
    3. Количество записей в данном месяце
    4. Все расходы по месяцам
    5. Самый расходный месяц
    6. Месяц с минимальными расходами
    7. Средние расходы в месяц
    8. Инфляция с прошлым годом
    9. Общее количество расходов (р.)
    10. Самая расходная статья расходов (тип)
    11. Количество записей в прошлом месяце
    12. Расходы за этот год
    13. Не оплачено в этом году (р.)
    14. Все данные
    '''
    #Количество записей
    def colZapisey_1(self):
        
        a = len(self.data['data_14'])

        return a
        
    #Среднее количество записей в месяц
    def srednKolZap_2(self):
        

        #Вычисляем общее количество
        col = 0
        for i in self.data['indexsMonth']:
            a = len(i); col = col + a
        
        
        #Вычисляем среднее количество
        vivod = math.floor(col/12)
        return vivod
        
    #Количество записей в данном месяце
    def KolZapMes_3(self):
        
        #Определение месяца
        date = str(datetime.datetime.now().date()).split('-')[1]
        year = str(datetime.datetime.now().date()).split('-')[0]
        
        #Ищем индексы записей в данном месяце
        col = 0

        for i in self.data['data_14']:

            if i[1] == self.index:
                i1 = (i[14].split(' ')[0]).split('.')[1]
                i2 = i[14].split(' ')[0].split('.')[2]

                if date == i1 and i2 == year:
                    col = col + 1

        #Возвращаем значение
        return col

    #Самый расходный месяц
    def MaxRashod_5(self):
        
        a = self.data['ObhRashod_4'].max()

        col = 0
        for i in self.data['ObhRashod_4']:
            if a == i:
                break
            else:
                col = col + 1

        vivod = self._dataMonth(col)

        return vivod
    
    #Месяц с минимальными расходами
    def MonthMinExpenses_6(self):
        
        a = self.data['ObhRashod_4'].min()

        col = 0
        for i in self.data['ObhRashod_4']:
            if a == i:
                break
            else:
                col = col + 1

        vivod = self._dataMonth(col)

        return vivod
    
    #Средние расходы в месяц
    def AverageMonthlyExpenses_7(self):
        
        data = self.data['ExpensesPerYear_12'] #Расходы за этот год
        vivod = round(data/12, 2)

        return vivod
    
    #Инфляция с прошлым годом 0.032
    def inflationFromLastYear_8(self):

        #Находим текущий год и прошлый
        currentYear = str(datetime.datetime.now().year) #Текущий год
        lasYear = str(int(currentYear) - 1) #Прошлый год

        currentYearSum = sum(self._TypeMonthData(currentYear)) #Сумма текущего года
        lasYearSum = sum(self._TypeMonthData(lasYear)) #Сумма прошлого года
                

        #Высчитываем расходы за прошлый год
        vivod = self._inflacia(lasYearSum, currentYearSum)
        return vivod

    #Общее количество расходов (р.) 0.14
    def TotalNumberExpenses_9(self):
        
        vivod = 0

        for i in self.data['data_14']:
            i = i[2:14]

            for i1 in i:
                if i1 not in (None, 0):
                    vivod = vivod + i1

        return vivod
    
    #Самая расходная статья расходов (тип)
    def MostExpendableItem_10(self):
        
        #Электроэнергия 
        #Вода
        #Отопление
        #Водоотведение
        #Коэффициент_налогов
        #Содержание_жилплощади
        #Кап_ремонт
        #Домофон
        #Обслуживание_газа
        #Газ
        #ТКО
        #Дополнительные_расходы #12

        typeRash = ('Электроэнергия', 'Вода', 'Отопление', 'Водоотведение', 'Коэффициент налогов', 'Содержание жилплощади', 'Кап. ремонт', 'Домофон', 'Обслуживание газа', 'Газ', 'ТКО', 'Дополнительные расходы')
        
        #Определяем текущий год
        year = str(datetime.datetime.now().year)
        vivod = np.array(self.ExpensesType(year))

        #Самая расходная часть расходов
        vivod = vivod.argmax()
        vivod = typeRash[vivod]
        return vivod
        
    #Количество записей в прошлом месяце
    def NumberEntriesLastMonth_11(self):
        
        #Определение месяца
        date = str(datetime.datetime.now().date()).split('-')[1]
        date = int(date) - 1;
        
        #Приводим в нужный вид 
        if date in range(1, 10):
            date = f'0{date}'
        
        year = datetime.datetime.now().date()
        year = str(year).split('-')[0]
        
        #Ищем индексы записей в данном месяце
        col = 0

        for i in self.data['data_14']:

            if i[1] == self.index:
                i1 = i[14].split(' ')[0].split('.')[1]
                i2 = i[14].split(' ')[0].split('.')[2]

                if i1 == date and i2 == year:
                    col = col + 1

        #Возвращаем значение
        return col


        #for i in self.data['data_14']
    
    #Расходы за этот год
    def ExpensesPerYear_12(self):
        
        #Текущий год
        date = str(datetime.datetime.now().year)
        
        vivod = [i[2:14] for i in self.data['data_14'] if i[14].split(' ')[0].split('.')[2] == date]
        _ = []

        for i in vivod:
            _.append(sum([i1 for i1 in i if i1 != None]))
        
        vivod = sum(_)

        return vivod
                
    #Всего не оплачено
    def notPaidYear_13(self):
        
        #Таблица с состоянием оплаты
        data = self.jobBd._readReturnBD(f'SELECT * FROM СТАТУС_СЧЕТА;') 
        data=list(data)
        #data1 = self.jobBd._readReturnBD('SELECT * FROM СЧЕТА;'); data1 = list(data1)

        #Ищем сумму всех не оплаченных счетов

        sum1 = 0
        for i in range(len(data)):

            if 0 in data[i][1:]:
                index = data[i][0]

                for i1 in range(len(data[i])):
                    if data[i][i1] == 0:
                        data1 = list(self.jobBd._readReturnBD(f'SELECT * FROM СЧЕТА WHERE id_счета={index};')[0][1:])
                        
                        if data1[i1] != None and data1[0] == self.index:
                            sum1 = sum1 + data1[i1]
        return sum1

    #Расходы типам согласно году
    def ExpensesType(self, year: str):
        '''Расходы типам согласно году\n
        - year - Год за который нужно вывести расходы\n
        Вывод:\n
        [100, 200, 300]\n
        0 электроэнергия\n
        1 Вода\n
        2 Отопление\n
        3 Водоотведение\n
        4 Коэф налогов\n
        5 Содерж жилплощ\n
        6 Кап рем\n
        7 Домофон\n
        8 Обслуж газа\n
        9 Газ\n
        10 Тко\n
        11 Дополнительные расходы'''

        typeEx = [] #Расходы по типам
        typeEx = [[] for i in range(12)]
        
        #Все данные из бд
        DATA = self.jobBd._readReturnBD(f'SELECT * FROM СЧЕТА WHERE id_адреса={self.index};')
        DATA = list(DATA)

        #Находим все записи за указанный год
        New_data = [i for i in DATA if i[14].split(' ')[0].split('.')[2] == year]

        for i in range(12):
            typeEx[i] = [i1[i+2] for i1 in New_data if i1[i+2] != None]
            typeEx[i] = sum(typeEx[i])

        return typeEx

    #Все данные
    def data_14(self, item):
        '''item - Индекс адреса в бд (согласно бд)\n
        Выводит:
        Адрес и его текст и данные этого адреса'''

        #Получение данных
        data = self.jobBd._readReturnBD('SELECT * FROM АДРЕС')

        
        if len(data) > 0:
            
            #Добавить item/text
            self.data['itemText'] = [i for i in data if i[0] == item][0]

            
            self.data['data_14'] = np.array([self.jobBd._readReturnBD(f'SELECT * FROM СЧЕТА WHERE id_адреса="{item}"')][0])

            #self.data['data_14'] = data.copy()

            #Получить данные о статусах оплаты
            indexs = self.jobBd._readReturnBD(f'SELECT (id_счета) FROM СЧЕТА WHERE id_адреса={item}') #Индексы все где содержатся нужный нам адрес
            indexs = [i[0] for i in indexs]

            '''a = []
            for i in indexs:
                data = self.jobBd._readReturnBD(f'SELECT * FROM СТАТУС_СЧЕТА WHERE id_счета={i[0]}') 
                a.append(data)'''
            
            
            #a = [self.jobBd._readReturnBD(f'SELECT * FROM СТАТУС_СЧЕТА WHERE id_счета={i[0]}') for i in indexs]
            a_ = self.jobBd._readReturnBD(f'SELECT * FROM СТАТУС_СЧЕТА')
            self.data['data_oplat'] = ([i for i in a_ if i[0] in indexs],)

            #self.data['data_oplat'] = (a,)

    #Расчет все года которые часто встречаются
    def YearPopular(self):

        vivod = np.array([])
        vivod = [i[14].split(' ')[0].split('.')[2] for i in self.data['data_14']]
        vivod = np.unique(vivod)
        vivod = vivod[::-1]
        return vivod

    #Запус
    def run(self):
        return self.data


'''#Подсчет времени
def decorator(func):

    def decor(*arg):
        time_old = time.time()
        func(*arg)
        time_new = time.time() - time_old
        print(round(time_new, 4))
    return decor

#Запуск
@decorator
def run(i):
    a = Analitic(i)
    b = a.run()'''


if __name__ == '__main__':
    
    a = Analitic(3)
    a.ExpensesType('2023')
    input()
    






