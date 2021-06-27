from pprint import pprint


class GenerationCodePython:
    token_graph = {1: [{2: {'AM': '='}}],
                   2: [{'INT': '1'}],
                   3: [{4: {'AM': '='}}],
                   4: [{'INT': '0'}],
                   5: [{6: 'cont'}],
                   6: [{7: {'VAR': 'j'}}, {10: {'VAR': 'j'}},
                       {13: {'VAR': 'j'}}, {14: 'cont'}],
                   7: [{8: {'AM': ':='}}],
                   8: [{9: {'INT': '7'}}],
                   9: [{'SEM': ';'}],
                   10: [{11: {'NOTE': '!='}}],
                   11: [{12: {'INT': '9'}}],
                   12: [{'SEM': ';'}],
                   13: [{'ADD': '++'}],
                   14: [{'OCB': '{'},
                        {15: {'VAR': 'sum'}},
                        {18: {'FOREACH': 'for'}},
                        {30: {'IF': 'if'}},
                        {'CCB': '}'}],
                   15: [{16: {'AM': '='}}],
                   16: [{'VAR': 'sum'}, {17: {'ADD': '+'}}],
                   17: [{'INT': '1'}],
                   18: [{19: {'VAR': 'j'}}, {22: {'VAR': 'j'}},
                        {25: {'VAR': 'j'}}, {26: 'cont'}],
                   19: [{20: {'AM': ':='}}],
                   20: [{21: {'INT': '7'}}],
                   21: [{'SEM': ';'}],
                   22: [{23: {'NOTE': '!='}}],
                   23: [{24: {'INT': '9'}}],
                   24: [{'SEM': ';'}],
                   25: [{'ADD': '++'}],
                   26: [{'OCB': '{'}, {27: {'VAR': 'sum'}}, {'CCB': '}'}],
                   27: [{28: {'AM': '='}}],
                   28: [{'VAR': 'sum'}, {29: {'ADD': '+'}}],
                   29: [{'INT': '1'}],
                   30: [{31: {'VAR': 'grade'}}, {33: 'cont'}],
                   31: [{32: {'Equality': '=='}}],
                   32: [{'INT': '0'}],
                   33: [{'OCB': '{'}, {34: {'VAR': 'answer'}}, {'CCB': '}'}],
                   34: [{35: {'AM': '='}}],
                   35: [{36: 'fact'}, {40: {'DIV': '/'}}],
                   36: [{'OB': '('}, {'INT': '2'}, {37: {'ADD': '+'}},
                        {'CB': ')'}],
                   37: [{'INT': '3'}, {38: {'SUB': '-'}}],
                   38: [{'INT': '9'}, {39: {'MULT': '*'}}],
                   39: [{'INT': '6'}],
                   40: [{'INT': '7'}],
                   'stmt': [{1: {'VAR': 'sum'}}, {3: {'VAR': 'grade'}},
                            {5: {'FOREACH': 'for'}}]}
    i = 0  # итерация по графу
    len_node_start = 0
    number_poz_node = 0
    include_p = 0  # вложенность
    number_tabs = 0  # количество отступов для вложенности

    def __init__(self):
        self.start_graph = self.token_graph['stmt']
        self.len_node_start = len(self.start_graph)

    def write_token(self, tmp_custom, fp):
        if tmp_custom == 'cont':
            pass
        elif lex := tmp_custom.get('VAR'):
            fp.write(lex + " ")
        elif lex := tmp_custom.get('INT'):
            fp.write(lex + " ")
        elif lex := tmp_custom.get('AM'):
            fp.write(lex + " ")
        elif lex := tmp_custom.get('CCB'):
            self.number_tabs -= 4
        return

    def foreach(self, number_node, fp):
        start_rang = 0
        stop_rang = 0
        tmp_custom = self.token_graph[number_node]
        if self.include_p >= len(tmp_custom):
            return
        if self.include_p == 0:
            lex = tmp_custom[self.include_p]
            kye = list(lex.keys())[0] + 1
            start_rang = list(self.token_graph[kye][0][kye + 1].values())[0]
            self.include_p += 1
        if self.include_p == 1:
            lex = tmp_custom[self.include_p]
            kye = list(lex.keys())[0] + 1
            stop_rang = list(self.token_graph[kye][0][kye + 1].values())[0]
            self.include_p += 1

        if self.include_p == 2:
            lex = tmp_custom[self.include_p]
            iter_var = list(list(lex.values())[0].values())[0]
            kye = list(lex.keys())[0]
            condition_direction = list(self.token_graph[kye][0].values())[0]
            self.include_p = 0
        if condition_direction == '++':
            fp.write(str(iter_var) + " in range({},{}):".format(start_rang,
                                                                stop_rang))
        else:
            fp.write(str(iter_var) + " in range({},{}):".format(start_rang,
                                                                stop_rang, -1))
        self.number_tabs += 4
        pass

    def cont_for(self, number_node, fp):
        tmp_custom = self.token_graph[number_node][0]
        count_node = 3  # перепрыгиваем
        kye = list(tmp_custom.keys())[0]
        if tmp_custom[kye] == 'cont':
            self.foreach(kye, fp)
        if count_node == len(self.token_graph[kye]):
            return
        fp.write("\n")
        for i in range(0, self.number_tabs):
            fp.write(" ")
        # count_node

        code_include_cycle = list(self.token_graph[kye][count_node])[0]
        val_include_cycle = list(self.token_graph[kye][count_node].values())[0] # значение элемента
        if val_include_cycle == 'cont':
            self.token_pars(code_include_cycle, fp)
        else:
            raise ValueError("Цикл не может быть пустым")

    def token_pars(self, number_node, fp):
        if len(self.token_graph[number_node]) > 1:
            pass
        tmp_custom = self.token_graph[number_node][0]
        pprint(tmp_custom)
        kye = list(tmp_custom.keys())[0]
        if not type(kye).__name__ == 'int':
            self.write_token(tmp_custom, fp)
            return fp.write("\n")
        else:
            self.write_token(tmp_custom[kye], fp)
            return self.token_pars(kye, fp)

    def next_node(self):
        self.i += 1

    def spusk(self):
        if self.i >= self.len_node_start:
            return
        node = self.start_graph[self.i]
        kye = list(node.keys())[0]
        with open('custom.py', 'a') as fp:
            if type(kye).__name__ == 'int':
                # значит не лист
                token = node.get(kye)
                if lex := token.get('VAR'):
                    fp.write(lex + " ")
                    self.token_pars(kye, fp)
                elif lex := token.get('FOREACH'):
                    fp.write(lex + " ")
                    self.cont_for(kye, fp)
                    self.number_tabs = 0
                elif lex := token.get('IF'):
                    fp.write(lex + " ")
                    self.token_pars(kye, fp)
        self.next_node()
        self.spusk()


GenerationCodePython().spusk()
