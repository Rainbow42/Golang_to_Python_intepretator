from pprint import pprint

from parsing import get_file, Parsing, Table

if __name__ == '__main__':
    code = get_file('example.go')
    lexemes = Parsing().parsing_lexeme(code)
    table_lexemes = Table().get_table()
    pprint(table_lexemes)
