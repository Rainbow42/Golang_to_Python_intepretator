from pprint import pprint

from graph_ver1 import Graph
from parsing import get_file, Parsing, Table

if __name__ == '__main__':
    code = get_file('cont.go')
    lexemes = Parsing().parsing_lexeme(code)
    table_lexemes = Table().get_table()
    # pprint(table_lexemes)
    graph = Graph(table_lexemes[2:]).stmt()
    # pprint(graph)
