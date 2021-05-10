from pprint import pprint


class Graph:
    """
    создание синтаксического дерева
    graph - список для графа
    tops - список уникальных вершин
    graph =  {
        "stmt": [{0: "expr"}, ],
        "0": [1:"term"],
        "1": ["{"2":"fact"}", "*", {3: "term"}],
        "3": [{4: "fact"}],
        "4": ["LP", "5:expr"],
        "5": [{6: "term"}],
        "2": ["Num"]}
    tops =[ {0:"stmt"},
            {1:"term"},
            {2:"fact"},
            ...
            {6:"term"}]
    """

    graph = {"stmt": []}  # список для графа
    tops = list()  # список уникальных вершин
    table_token = list()  # таблица токенов
    i: int = 0  # Позиция в списке токенов
    j: int = -1  # позиция столбца в списке токенов
    line_token: list = None  # строка токенов
    n = 0  # количество строк
    m = 0  # количество столбцов
    numbers_title = 0  # уникальное число для хранения в графе
    open_brackets = list()  # для отслеживания открытых скобок
    close_brackets = list()  # для отслеживания закрытых скобок
    open_braces = list()  # для отслеживания открытых фигурных скобок
    close_braces = list()  # для отслеживания закрытых фигурных скобок

    # наименования выражения

    def __init__(self, table_token):
        self.table_token = table_token
        self.line_token = self.table_token[self.i]
        self.n = len(self.table_token)
        self.m = len(self.line_token)

    def next_token(self):
        self.j += 1
        return self.line_token[self.j]

    def before_token(self):
        return self.line_token[self.j - 1]

    def add_in_graph_title_gram(self, title, number_title=None, list_=False):
        # title = наименование грамматики
        #  добавление наименования грамматики в граф
        """if not len(self.graph):
            # если граф пустой стартовая позиция
            node = {self.numbers_title: title}
            self.tops.append("stmt")
            self.tops.append(node)
            self.graph["stmt"] = [node]
            self.graph[self.numbers_title] = []
            self.numbers_title += 1"""

        if (number_title or number_title == 0) and not list_:
            # если требуется занести в граф новый узел
            # заносим новый узел в указный узел
            # создаем новый узел и
            # увеличившем уникально число для хранение узлов
            node = {self.numbers_title + 1: title}
            self.tops.append(node)
            self.graph[number_title].append(node)
            self.graph[self.numbers_title + 1] = []

            self.numbers_title += 1

        elif number_title and list_:
            # если требуется занести в граф лист
            # берем номер вершины и заносим значение
            self.graph[number_title].append(title)

        else:
            node = {self.numbers_title + 1: title}
            self.tops.append(node)
            self.graph[self.numbers_title] = [node]
            self.graph[self.numbers_title + 1] = []
            self.numbers_title += 1

    def get_abstract_syntax_trees(self):
        return self.stmt()

    def get_number_title(self):
        number_title = None

        for val in self.open_braces:  # для слежения за вложенностью
            val = list(val.keys())[0]
            for val2 in self.close_braces:
                if val2:
                    val2 = list(val2.keys())[0]
                    if val != val2:
                        number_title = val
                else:
                    number_title = val
            else:
                number_title = val
        return number_title

    def stmt(self):
        if self.i >= self.n:
            # если пробежались по всем строкам
            return self.graph

        if self.j >= self.m - 1:
            # если текущий индекс столбца в строке токенов равен размеру
            # длине строки
            self.j = -1
            self.i += 1
            if len(self.open_brackets) != len(self.close_brackets):
                raise ValueError("Не хватает закрывающей скобки")
            if self.i >= self.n:
                return self.graph
            self.line_token = self.table_token[self.i]
            self.m = len(self.line_token)

        token = self.next_token()
        if token.get("VAR") and self.m == 3:
            # инициализация переменных или присваивание
            self.add_in_graph_title_gram(title=token, number_title="stmt")
            token = self.next_token()
            # pprint(token)
            if token.get("AM"):
                number_title = list(self.tops[-1].keys())[0]
                self.add_in_graph_title_gram(title=token,
                                             number_title=number_title)
                token = self.next_token()
                if token.get('FLOAT') or token.get('INT') or token.get('VAR') \
                        or token.get("STR"):
                    number_title = list(self.tops[-1].keys())[0]
                    self.add_in_graph_title_gram(title=token,
                                                 number_title=number_title,
                                                 list_=True)
                else:
                    raise ValueError("Ожидалась переменная или число, строка")

        elif token.get("VAR"):
            self.add_in_graph_title_gram(title=token, number_title="stmt")
            token = self.next_token()

            if token.get("AM"):
                number_title = list(self.tops[-1].keys())[0]
                self.add_in_graph_title_gram(title=token,
                                             number_title=number_title)
                self.uzel = list(self.tops[-1].keys())[0]
                self.mathematic()

        elif token.get("IF"):
            self.add_in_graph_title_gram(title=token, number_title="stmt")
            self.uzel = list(self.tops[-1].keys())[0]
            token = self.next_token()
            if token.get('FLOAT') or token.get('INT') or token.get('VAR') \
                    or token.get("STR"):
                number_title = list(self.tops[-1].keys())[0]
                self.add_in_graph_title_gram(title=token,
                                             number_title=number_title)
                token = self.next_token()
                if token.get('Equality') or token.get('MQ') or token.get('LQ') \
                        or token.get("LESS") or token.get("MORE") \
                        or token.get('NOTE'):
                    number_title = list(self.tops[-1].keys())[0]
                    self.add_in_graph_title_gram(title=token,
                                                 number_title=number_title,
                                                 list_=False)
                    token = self.next_token()
                    if token.get('FLOAT') or token.get('INT') or token.get(
                            'VAR') or token.get("STR"):
                        number_title = list(self.tops[-1].keys())[0]
                        self.add_in_graph_title_gram(title=token,
                                                     number_title=number_title,
                                                     list_=True)
                        self.condition()
                    else:
                        raise ValueError("В условии ожидалась переменная для "
                                         "сравнения")
                else:
                    raise ValueError("В условии ожидался операнд сравнения")
            else:
                raise ValueError("В условии ожидалась переменная или число, "
                                 "строка")
        elif token.get("ELSE"):
            self.add_in_graph_title_gram(title=token, number_title="stmt")
            self.uzel = list(self.tops[-1].keys())[0]
            self.condition()

        pprint(self.graph)
        # pprint(self.tops)
        # self.add_in_graph_title_gram()
        # print(token)
        self.stmt()

    def condition(self):
        """Условие"""
        if self.i >= self.n-1:
            # если пробежались по всем строкам
            return

        if self.j >= self.m - 1:
            # если текущий индекс столбца в строке токенов равен размеру
            # длине строки
            self.j = -1
            self.i += 1
            if len(self.open_brackets) != len(self.close_brackets):
                raise ValueError("Не хватает закрывающей скобки")
            elif len(self.open_braces) == len(self.close_braces):
                return
            elif self.i >= self.n-1:
                return
            self.line_token = self.table_token[self.i]
            self.m = len(self.line_token)

        token = self.next_token()
        if token.get('OCB'):
            self.add_in_graph_title_gram(title="cont",
                                         number_title=self.uzel,
                                         list_=False)
            number_title = list(self.tops[-1].keys())[0]
            self.open_braces.append({number_title: token})
            self.add_in_graph_title_gram(title=token,
                                         number_title=number_title,
                                         list_=True)

        elif token.get("VAR") and self.m == 3:
            # инициализация переменных или присваивание
            number_title = self.get_number_title()

            self.add_in_graph_title_gram(title=token, number_title=number_title)
            token = self.next_token()

            if token.get("AM"):
                number_title = list(self.tops[-1].keys())[0]
                self.add_in_graph_title_gram(title=token,
                                             number_title=number_title)
                token = self.next_token()
                if token.get('FLOAT') or token.get('INT') or token.get('VAR') \
                        or token.get("STR"):
                    number_title = list(self.tops[-1].keys())[0]
                    self.add_in_graph_title_gram(title=token,
                                                 number_title=number_title,
                                                 list_=True)
                else:
                    raise ValueError("Ожидалась переменная или число, строка")
        elif token.get("VAR"):
            number_title = self.get_number_title()
            self.add_in_graph_title_gram(title=token, number_title=number_title)
            token = self.next_token()

            if token.get("AM"):
                number_title = list(self.tops[-1].keys())[0]
                self.add_in_graph_title_gram(title=token,
                                             number_title=number_title)
                self.uzel = list(self.tops[-1].keys())[0]
                self.mathematic()

        elif token.get("IF"):
            number_title = self.get_number_title()

            self.add_in_graph_title_gram(title=token, number_title=number_title)
            self.uzel = list(self.tops[-1].keys())[0]
            token = self.next_token()

            if token.get('FLOAT') or token.get('INT') or token.get('VAR') \
                    or token.get("STR"):
                number_title = list(self.tops[-1].keys())[0]
                self.add_in_graph_title_gram(title=token,
                                             number_title=number_title)
                token = self.next_token()

                if token.get('Equality') or token.get('MQ') or token.get('LQ') \
                        or token.get("LESS") or token.get("MORE") \
                        or token.get('NOTE'):
                    number_title = list(self.tops[-1].keys())[0]
                    self.add_in_graph_title_gram(title=token,
                                                 number_title=number_title,
                                                 list_=False)
                    token = self.next_token()
                    if token.get('FLOAT') or token.get('INT') or token.get(
                            'VAR') or token.get("STR"):
                        number_title = list(self.tops[-1].keys())[0]
                        self.add_in_graph_title_gram(title=token,
                                                     number_title=number_title,
                                                     list_=True)
                    else:
                        raise ValueError("В условии ожидалась переменная для "
                                         "сравнения")
                else:
                    raise ValueError("В условии ожидался операнд сравнения")
            else:
                raise ValueError("В условии ожидалась переменная или число, "
                                 "строка")
        elif token.get("ELSE"):
            number_title = self.get_number_title()
            self.add_in_graph_title_gram(title=token, number_title=number_title)
            self.uzel = list(self.tops[-1].keys())[0]

        elif token.get('CCB'):
            number_title = self.get_number_title()
            self.close_braces.append({number_title: token})
            self.add_in_graph_title_gram(title=token,
                                         number_title=number_title,
                                         list_=True)
            if len(self.open_braces) == len(self.close_braces):
                self.close_braces.clear()
                self.open_braces.clear()
        self.condition()

    def mathematic(self):
        """Математические операции"""
        if self.j >= self.m - 1:
            return
        token = self.next_token()

        if token.get('ADD') or token.get('MULT') \
                or token.get("SUB") or token.get("DIV"):
            before_token = self.before_token()
            if before_token.get('CB'):
                # если до этого была закрывающая скобка графа
                self.add_in_graph_title_gram(title=token,
                                             number_title=self.uzel)
            else:
                number_title = list(self.tops[-1].keys())[0]
                self.add_in_graph_title_gram(title=token,
                                             number_title=number_title)

        elif token.get('OB'):
            self.open_brackets.append({self.numbers_title: token})
            self.add_in_graph_title_gram(title="fact",
                                         number_title=self.uzel,
                                         list_=False)

            number_title = list(self.tops[-1].keys())[0]
            self.add_in_graph_title_gram(title=token,
                                         number_title=number_title,
                                         list_=True)

        elif token.get('FLOAT') or token.get('INT') or token.get('VAR'):
            number_title = list(self.tops[-1].keys())[0]
            self.add_in_graph_title_gram(title=token,
                                         number_title=number_title,
                                         list_=True)

        elif token.get('CB'):
            keys = 0
            for value in self.tops:
                if list(value.values())[0] == 'fact':
                    keys = list(value.keys())[0]
            self.close_brackets.append({self.numbers_title + 1: token})
            self.add_in_graph_title_gram(title=token,
                                         number_title=keys,
                                         list_=True)
        elif token.get('comment'):
            self.add_in_graph_title_gram(title=token,
                                         number_title=self.uzel,
                                         list_=False)
        else:
            raise ValueError("Ожидалась переменная или матем. операнд")
        self.mathematic()
