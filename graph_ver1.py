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
    braces = list()  # для отслеживания закрытых фигурных скобок

    # наименования выражения

    def __init__(self, table_token):
        self.table_token = table_token
        self.line_token = self.table_token[self.i]
        self.n = len(self.table_token)
        self.m = len(self.line_token)

    def next_token(self):
        self.j += 1
        # print(self.j)
        return self.line_token[self.j]

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

        # number_title = 'stmt'
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
            # pprint(token)

            if token.get("AM"):
                number_title = list(self.tops[-1].keys())[0]
                self.add_in_graph_title_gram(title=token,
                                             number_title=number_title)
                self.uzel = list(self.tops[-1].keys())[0]
                self.mathematic()
                # token = self.next_token()

        pprint(self.graph)
        # pprint(self.tops)
        # self.add_in_graph_title_gram()
        # print(token)
        self.stmt()

    def mathematic(self):
        if self.j >= self.m - 1:
            return
        token = self.next_token()

        if token.get('ADD') or token.get('MULT') \
                or token.get("SUB") or token.get("DIV"):
            number_title = list(self.tops[-1].keys())[0]
            self.add_in_graph_title_gram(title=token,
                                         number_title=number_title)
        elif token.get('OB'):
            self.open_brackets.append({self.numbers_title + 1: token})
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
        else:
            raise ValueError("Ожидалась переменная или матем. операнд")
        self.mathematic()
        """if token.get('OB') or token.get('ADD') or token.get('MULT') \
                or token.get("SUB") or token.get("DIV"):"""
