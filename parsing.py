# Синтаксический анализ
import re


class Parsing:
    keywords = ('break', 'default', 'func', 'interface', 'select', 'main()',
                'package', 'case', 'defer', 'go', 'map', 'struct', 'main',
                'chan', 'goto', 'package', 'switch',
                'const', 'fallthrough', 'range', 'type',
                'continue', 'for', 'import', 'return', 'var', ';')

    def parsing_lexeme(self, code):
        lexeme = LexicalDictionary()
        table = Table()
        for line_code in code:
            for key in line_code:
                if key in self.keywords:
                    lexeme.keywords(key)
                    continue

                if word := re.findall(
                        r'[-+]?[0-9]*[.,][0-9]+(?:[eE][-+]?[0-9]+)*', key):
                    # число с плавающей запятой
                    lexeme.decimal("".join(word))
                    continue

                if key == "if":
                    lexeme.condition(key)
                    continue

                if word := re.findall(r'else$', key):
                    lexeme.other("".join(word))
                    continue

                if key[0] == '"' and key[-1] == '"':
                    lexeme.string(key)
                    continue

                if word := re.findall(r'[-+]?[0-9]+', key):
                    # целое число
                    lexeme.integer("".join(word))

                if word := re.findall(r'^}$', key):
                    # закрывающая фигурная скобка
                    lexeme.closing_curly_brace("".join(word))

                if word := re.findall(r'{', key):
                    # открывающая фигурная скобка
                    lexeme.open_curly_brace("".join(word))

                if word := re.findall(r'\)', key):
                    # закрывающая скобка
                    lexeme.closing_brace("".join(word))

                if word := re.findall(r'\(', key):
                    # открывающая скобка
                    lexeme.open_brace("".join(word))

                if word := re.findall(r'[a-zA-Z][a-zA-Z]*', key):
                    # переменная
                    lexeme.variable("".join(word))

                if word := re.findall(r'<', key):
                    # меньше или равно
                    if len(key) > 1:
                        if key[1] == '=':
                            # <=
                            word = re.findall(r'<=', key)
                            lexeme.less_equally("".join(word))
                    else:
                        # <
                        lexeme.less("".join(word))

                if word := re.findall(r'>', key):
                    # больше или равно
                    if len(key) > 1:
                        if key[1] == '=':
                            # >=
                            word = re.findall(r'>=', key)
                            lexeme.more_equally("".join(word))
                    else:
                        # >
                        lexeme.more("".join(word))

                if word := re.findall(r'=', key):
                    # равно
                    if word := re.findall(r'==', key):
                        # >=
                        lexeme.equality("".join(word))
                    elif len(key) == 1:
                        # Знак присвоения =
                        word = re.findall(r'=', key)
                        lexeme.assignment_mark("".join(word))

                if word := re.findall(r':=', key):
                    # Знак присвоения =
                    lexeme.assignment_mark("".join(word))

                if word := re.findall(r'/', key):
                    # Знак деления
                    if len(key) == 1:
                        word = re.findall(r'/', key)
                        lexeme.division("".join(word))
                    elif len(key) > 1:
                        word = re.findall(r'//', key)
                        lexeme.comment("".join(word))

                if word := re.findall(r'%', key):
                    # Знак деления с остатком
                    lexeme.division_remainder("".join(word))

                if word := re.findall(r'\*', key):
                    # Знак умножения
                    lexeme.multiplication("".join(word))

                if word := re.findall(r'-', key):
                    # Знак вычитания
                    idx = key.index('-')
                    if idx == 0:
                        if idx+1 == len(key):
                            lexeme.subtraction("".join(word))

                if word := re.findall(r'\+', key):
                    # Знак сложения
                    lexeme.add("".join(word))

                if word := re.findall(r'!=', key):
                    # Знак сложения
                    lexeme.not_equal("".join(word))

                if word := re.findall(r';', key):
                    lexeme.keywords("".join(word))

            if lex := lexeme.get_lexical():
                table.append_table(lex.copy())
                lexeme.clear_lexical()


class Table:
    table = list()

    def append_table(self, words: dict):
        self.table.append(words)

    def get_table(self):
        return self.table


class LexicalDictionary:
    table_word = list()

    def keywords(self, key: str):
        self.table_word.append({'KEYWORDS': key})

    def var_init(self, key: str):
        self.table_word.append({'VAR_INIT': key})

    def variable(self, key: str):
        self.table_word.append({'VAR': key})

    def decimal(self, key: str):
        self.table_word.append({'FLOAT': key})

    def integer(self, key: str):
        self.table_word.append({'INT': key})

    def string(self, key: str):
        self.table_word.append({'STR': key})

    def closing_curly_brace(self, key: str):
        self.table_word.append({'CCB': key})

    def open_curly_brace(self, key: str):
        self.table_word.append({'OCB': key})

    def other(self, key: str):
        self.table_word.append({'ELSE': key})

    def condition(self, key: str):
        self.table_word.append({'IF': key})

    def closing_brace(self, key: str):
        self.table_word.append({'CB': key})

    def open_brace(self, key: str):
        self.table_word.append({'OB': key})

    def less_equally(self, key: str):
        self.table_word.append({'LQ': key})

    def more_equally(self, key: str):
        self.table_word.append({'MQ': key})

    def less(self, key: str):
        self.table_word.append({'LESS': key})

    def assignment_mark(self, key: str):
        self.table_word.append({'AM': key})

    def not_equal(self, key: str):
        self.table_word.append({'NOTE': key})

    def equality(self, key: str):
        self.table_word.append({'Equality': key})

    def division(self, key: str):
        self.table_word.append({'DIV': key})

    def division_remainder(self, key: str):
        self.table_word.append({'DIVREM': key})

    def more(self, key: str):
        self.table_word.append({'MORE': key})

    def multiplication(self, key: str):
        self.table_word.append({'MULT': key})

    def subtraction(self, key: str):
        self.table_word.append({'SUB': key})

    def add(self, key: str):
        self.table_word.append({'ADD': key})

    def comment(self, key: str):
        self.table_word.append({'comment': key})

    def get_lexical(self):
        return self.table_word

    def clear_lexical(self):
        self.table_word.clear()


def get_file(file):
    array = list()
    with open(file, 'r') as f:
        for row in f:
            if arr := row.split():
                array.append(arr)
    return array
