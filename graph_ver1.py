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

    graph = dict()  # список для графа
    tops = list()  # список уникальных вершин
    table_token = list()  # таблица токенов
    i: int = 0  # Позиция в списке токенов
    j: int = -1  # позиция столбца в списке токенов
    line_token: list = None  # строка токенов
    n = 0  # количество строк
    m = 0  # количество столбцов
    numbers_title = 0  # уникальное число для хранения в графе

    # наименования выражения

    def __init__(self, table_token):
        self.table_token = table_token
        self.line_token = self.table_token[self.i]
        self.n = len(self.table_token)
        self.m = len(self.line_token)
        self.stmt()

    def next_token(self):
        self.j += 1
        return self.line_token[self.j]

    def add_in_graph_title_gram(self, title, number_title=None, list_=False):
        # title = наименование грамматики
        #  добавление наименования грамматики в граф
        if not len(self.graph):
            # если граф пустой стартовая позиция
            node = {self.numbers_title: title}
            self.tops.append("stmt")
            self.tops.append(node)
            self.graph["stmt"] = [node]
            self.graph[self.numbers_title] = []
            self.numbers_title += 1

        elif number_title and not list_:
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
        return self.graph

    def stmt(self):
        if self.i >= self.n - 1:
            # если пробежались по всем строкам
            return self.graph

        if self.j == self.m - 1:
            # если текущий индекс столбца в строке токенов равен размеру
            # длине строки
            self.j = -1
            self.i += 1
            self.line_token = self.table_token[self.i]
            self.m = len(self.line_token)

        number_title = 'stmt'
        token = self.next_token()
        if token.get("VAR"):
            self.add_in_graph_title_gram(title=token)
            token = self.next_token()
            if token.get("AM"):
                """if self.tops[-2] == 'stmt':
                    self.add_in_graph_title_gram(title=token,
                                                 number_title="stmt")
                else:"""
                number_title = list(self.tops[-1].keys())[0]
                self.add_in_graph_title_gram(title=token,
                                             number_title=number_title)

        # pprint(self.graph)
        # pprint(self.tops)
        # self.add_in_graph_title_gram()
        # print(token)
        self.stmt()
