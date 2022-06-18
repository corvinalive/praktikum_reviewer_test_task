import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # Лучше записать тернарный оператор if без использования отрицания
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        """
        Неудачное имя переменной.
        1. Выбранное имя скрывает имя класса Record.
        2. В соответствии с PEP8 имя переменной должно быть lowercase: 
            https://peps.python.org/pep-0008/#function-and-method-arguments
        """
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                # лучше использовать оператор +=
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # комментарий к функции лучше выполнить в соответствии с Docstring Conventions https://peps.python.org/pep-0257/
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            """Для выполнения требований PEP8 лучше изменить способ разбиения длинной строки, использование  
            бэкслеша для переноса не рекомендуется https://peps.python.org/pep-0008/#maximum-line-length"""
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            # скобки лишние
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    """имена аргументов функций должны быть в lowercase 
    https://peps.python.org/pep-0008/#prescriptive-naming-conventions"""
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):

        """ Выбранное имя переменной currency_type не слишком подходит, так как в этой переменной хранится
        не тип валюты, а название валюты, используемое для вывода в сообщениях.
        Данное присваивание лучше не делать, так как название валюты переназначается ниже перебором"""
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        """ При проверках на тип валюты в первом сравнении идет сравнение с переменной currency,
        в остальных проверках с переменной currency_type.
        """
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            """"Логическая ошибка в коде, надо исправить"""
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                # В соответствии с требованиями к коду студентов в f-строках нельзя применять вызов функций
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            """ В соответствии с требованиями к коду студентов в f-строках нельзя применять арифмитические функции,
            использовать бекслеш для переноса
            """
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    """ Нет смысла переопределять функцию без добавления новой функциональности. Функция get_week_stats
    в классе CashCalculator наследуется от родительского класса, доступна в классе CashCalculator,
    выполняет нужные вычисления и не требует модификации в классе CashCalculator
    """
    def get_week_stats(self):
        super().get_week_stats()
