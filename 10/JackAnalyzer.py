class JackTokenizer:
    keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean',
                'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
    symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']

    def __init__(self, file_name):
        self.jack_file = open(file_name, 'r')
        self.xml_file = open(file_name.replace('.jack', 'T.xml'), 'w')
        self.xml_file.write('<tokens>\n')

    def advance(self):
        cur_line = self.jack_file.readline()
        while cur_line:
            cur_line = cur_line.replace('\n', '')
            if cur_line.startswith('//') | (cur_line == '') | (cur_line.find('/**') != -1) | (
                    cur_line.find('*/') != -1) | cur_line.startswith(' *'):
                pass
            else:
                list_cur_line = cur_line.split()
                in_string = False
                cur_string = ''
                for item in list_cur_line:
                    if in_string:
                        if item.find('\"') != -1:
                            list_cur_item = list(item)
                            for char in list_cur_item:
                                if (char in JackTokenizer.symbols) and not in_string:
                                    if list_cur_item.index(char) != 0:
                                        self.xml_file.write(JackTokenizer.process_prev_string(''.join(list_cur_item[:list_cur_item.index(char)])))
                                    self.xml_file.write(JackTokenizer.symbol(char))
                                    list_cur_item = list_cur_item[list_cur_item.index(char) + 1:]
                                elif char == '\"':
                                    if in_string:
                                        cur_string += (' ' + ''.join(list_cur_item[:list_cur_item.index(char)]))
                                        self.xml_file.write(JackTokenizer.string_val(cur_string))
                                        cur_string = ''
                                        list_cur_item = list_cur_item[list_cur_item.index(char) + 1:]
                                    else:
                                        cur_string += ''.join(list_cur_item[list_cur_item.index(char) + 1:])
                                    in_string = not in_string
                        else:
                            cur_string += (' ' + item)
                    else:
                        if item.startswith('//'):
                            break
                        elif item in JackTokenizer.keywords:
                            self.xml_file.write(JackTokenizer.keyword(item))
                        elif item.isdigit():
                            self.xml_file.write(JackTokenizer.int_val(item))
                        elif item in JackTokenizer.symbols:
                            self.xml_file.write(JackTokenizer.symbol(item))
                        elif item.isalnum():
                            self.xml_file.write(JackTokenizer.identifier(item))
                        else:
                            list_cur_item = list(item)
                            for char in list_cur_item:
                                if char in JackTokenizer.symbols:
                                    if list_cur_item.index(char) != 0:
                                        self.xml_file.write(JackTokenizer.process_prev_string(''.join(list_cur_item[:list_cur_item.index(char)])))
                                    self.xml_file.write(JackTokenizer.symbol(char))
                                    list_cur_item = list_cur_item[list_cur_item.index(char) + 1:]
                                elif char == '\"':
                                    in_string = not in_string
                                    cur_string += ''.join(list_cur_item[list_cur_item.index(char) + 1:])
                                    break
                                elif list_cur_item.index(char) == len(list_cur_item) - 1:
                                    self.xml_file.write(JackTokenizer.process_prev_string(''.join(list_cur_item)))
            cur_line = self.jack_file.readline()
        self.xml_file.write('</tokens>\n')

    @staticmethod
    def process_prev_string(prev_string):
        if prev_string == '':
            return
        elif prev_string in JackTokenizer.keywords:
            return JackTokenizer.keyword(prev_string)
        elif prev_string.isdigit():
            return JackTokenizer.int_val(prev_string)
        else:
            return JackTokenizer.identifier(prev_string)

    @staticmethod
    def keyword(key_word):
        return '<keyword> ' + key_word + ' </keyword>\n'

    @staticmethod
    def symbol(symbol):
        if symbol == '<':
            return '<symbol> &lt; </symbol>\n'
        elif symbol == '>':
            return '<symbol> &gt; </symbol>\n'
        elif symbol == '&':
            return '<symbol> &amp; </symbol>\n'
        else:
            return '<symbol> ' + symbol + ' </symbol>\n'

    @staticmethod
    def identifier(identifier):
        return '<identifier> ' + identifier + ' </identifier>\n'

    @staticmethod
    def int_val(int_val):
        return '<integerConstant> ' + str(int_val) + ' </integerConstant>\n'

    @staticmethod
    def string_val(string_val):
        return '<stringConstant> ' + string_val + ' </stringConstant>\n'


class CompilationEngine:
    def __init__(self, file_name):
        self.t_xml_file = open(file_name.replace('.jack', 'T.xml'), 'r')
        self.xml_file = open(file_name.replace('T.xml', '.xml'), 'w')
        self.list_tokens = []
        cur_line = self.t_xml_file.readline()
        while cur_line:
            self.list_tokens.append(cur_line.split())
            cur_line = self.t_xml_file.readline()

    def compile_class(self):
        output = '<class>\n\t' + JackTokenizer.keyword('class') + '\t' + JackTokenizer.identifier(self.list_tokens[2][1]) + '\t' + JackTokenizer.symbol('{')
        subroutine_head_indexes = []
        for i in range(len(self.list_tokens)):
            if self.list_tokens[i][1] in ['static', 'field']:
                for m in range(i+2, len(self.list_tokens)):
                    if self.list_tokens[m][1] == ';':
                        output += CompilationEngine.compile_class_var_dec(self.list_tokens[i, m+1])
                        break
            elif self.list_tokens[i][1] in ['constructor', 'function', 'method']:
                subroutine_head_indexes.append(i)
        for head_index in subroutine_head_indexes:
            if subroutine_head_indexes.index(head_index) == -1:
                output += CompilationEngine.compile_subroutine(self.list_tokens[head_index: -2])
            else:
                output += CompilationEngine.compile_subroutine(self.list_tokens[head_index: subroutine_head_indexes.index(head_index)+1])
        output += '\t' + JackTokenizer.symbol('}') + '<\class>\n'
        self.xml_file.write(output)
        return output

    @staticmethod
    def compile_class_var_dec(tokens):
        output = '\t<classVarDec>\n'
        for token in tokens:
            output += '\t\t' + ' '.join(token)
        output += '\t</classVarDec>\n'
        return output

    @staticmethod
    def compile_subroutine(tokens):
        output = '\t<subroutineDec>\n'
        for token in tokens[:4]:
            output += '\t\t' + ' '.join(token)
        output += CompilationEngine.compile_parameter_list(tokens[tokens.index('(')+1:tokens.index(')')]) + '\t\t' + JackTokenizer.symbol(')') + '\t\t<subroutineBody>\n\t\t' + JackTokenizer.symbol('{')
        for i in range(tokens.index('{')+1, len(tokens)):
            if tokens[i][1] == 'var':
                for m in range(i+2, len(tokens)):
                    if tokens[m][1] == ';':
                        statement_start = m + 1
                        output += CompilationEngine.compile_var_dec(tokens[i:statement_start])
                        break
            output += CompilationEngine.compile_statements(tokens[statement_start:-1])
        output += '\t\t' + JackTokenizer.symbol('}') + '\t\t</subroutineBody>\n\t</subroutineDec>\n'
        return output

    @staticmethod
    def compile_parameter_list(tokens):
        output = '\t\t<parameterList>\n'
        for token in tokens:
            output += '\t\t\t' + ' '.join(token)
        output += '\t\t</parameterList>\n'
        return output

    @staticmethod
    def compile_var_dec(tokens):
        output = '\t\t\t<varDec>\n'
        for token in tokens:
            output += '\t\t\t\t' + ' '.join(token)
        output += '\t\t\t</varDec>\n'
        return output

    @staticmethod
    def compile_statements(tokens):
        output = '\t\t\t<statements>\n'
        statement_head_types_indexes = []
        for i in range(len(tokens)):
            if tokens[i][1] in ['let', 'if', 'while', 'do', 'return']:
                statement_head_types_indexes.append([tokens[i][1], tokens[i][0]])
        for i in range(len(statement_head_types_indexes)):
            if i == len(statement_head_types_indexes)-1:
                if statement_head_types_indexes[i][0] == 'let':
                    output += CompilationEngine.compile_let(tokens[statement_head_types_indexes[i][1]:])
                elif statement_head_types_indexes[i][0] == 'if':
                    output += CompilationEngine.compile_if(tokens[statement_head_types_indexes[i][1]:])
                elif statement_head_types_indexes[i][0] == 'while':
                    output += CompilationEngine.compile_while(tokens[statement_head_types_indexes[i][1]:])
                elif statement_head_types_indexes[i][0] == 'do':
                    output += CompilationEngine.compile_do(tokens[statement_head_types_indexes[i][1]:])
                elif statement_head_types_indexes[i][0] == 'return':
                    output += CompilationEngine.compile_return(tokens[statement_head_types_indexes[i][1]:])
            else:
                if statement_head_types_indexes[i][0] == 'let':
                    output += CompilationEngine.compile_let(tokens[statement_head_types_indexes[i][1]:statement_head_types_indexes[i+1][1]])
                elif statement_head_types_indexes[i][0] == 'if':
                    output += CompilationEngine.compile_if(tokens[statement_head_types_indexes[i][1]:statement_head_types_indexes[i+1][1]])
                elif statement_head_types_indexes[i][0] == 'while':
                    output += CompilationEngine.compile_while(tokens[statement_head_types_indexes[i][1]:statement_head_types_indexes[i+1][1]])
                elif statement_head_types_indexes[i][0] == 'do':
                    output += CompilationEngine.compile_do(tokens[statement_head_types_indexes[i][1]:statement_head_types_indexes[i+1][1]])
                elif statement_head_types_indexes[i][0] == 'return':
                    output += CompilationEngine.compile_return(tokens[statement_head_types_indexes[i][1]:statement_head_types_indexes[i+1][1]])
        output += '\t\t\t</statements>\n'
        return output
    
    @staticmethod
    def compile_do(tokens):
        output = '\t\t\t\t<doStatement>\n'
        for token in tokens[:tokens.index('(')+1]:
            output += '\t\t\t\t\t' + ' '.join(token)
        output += CompilationEngine.compile_expression_list(tokens[tokens.index('(')+1:tokens.index(')')]) + '\t\t\t\t\t' + JackTokenizer.symbol(')') + tokens[-1] + '\t\t\t\t</doStatement>\n'
        return output
    
    @staticmethod
    def compile_let(tokens):
        output = '\t\t\t\t<letStatement>\n'
        for token in tokens[:3]:
            output += '\t\t\t\t\t' + ' '.join(token)
        if tokens[2][1] == '[':
            output += CompilationEngine.compile_expression(tokens[3:tokens.index(']')]) + '\t\t\t\t\t' + JackTokenizer.symbol(']') + '\t\t\t\t\t' + JackTokenizer.symbol('=')
        output += CompilationEngine.compile_expression(tokens[tokens.index('=')+1:tokens.index(';')]) + '\t\t\t\t\t' + tokens[-1] + '\t\t\t\t</letStatement>\n'
        return output
    
    @staticmethod
    def compile_while(tokens):
        output = '\t\t\t\t<whileStatement>\n'
        for token in tokens[:2]:
            output += '\t\t\t\t\t' + ' '.join(token)
        output += CompilationEngine.compile_expression(tokens[2:tokens.index(')')]) + '\t\t\t\t\t' + JackTokenizer.symbol(')') + '\t\t\t\t\t' + JackTokenizer.symbol('{') + CompilationEngine.compile_statements(tokens[tokens.index('{')+1:tokens[::-1].index('}')]) + '\t\t\t\t\t' + JackTokenizer.symbol('}') + '\t\t\t\t</whileStatement>\n'
        return output
    
    @staticmethod
    def compile_return(tokens):
        output = '\t\t\t\t<returnStatement>\n\t\t\t\t\t' + tokens[0]
        if tokens[1][1] == ';':
            output += '\t\t\t\t\t' + ' '.join(tokens[1])
        else:
            output += CompilationEngine.compile_expression(tokens[1:tokens.index(';')]) + '\t\t\t\t\t' + tokens[-1] + '\t\t\t\t</returnStatement>\n'
        return output
    
    @staticmethod
    def compile_if(tokens):
        output = '\t\t\t\t<ifStatement>\n'
        for token in tokens[:2]:
            output += '\t\t\t\t\t' + ' '.join(token)
        output += CompilationEngine.compile_expression(tokens[2:tokens.index(')')]) + '\t\t\t\t\t' + JackTokenizer.symbol(')') + '\t\t\t\t\t' + JackTokenizer.symbol('{')
        if 'else' in tokens:
            output += CompilationEngine.compile_statements(tokens[tokens.index('{')+1, (tokens[:tokens.index('else')])[::-1].index('}')]) + '\t\t\t\t\t' + JackTokenizer.symbol('}')
            for token in tokens[tokens.index('else'):tokens.index('else')+2]:
                output += '\t\t\t\t\t' + ' '.join(token)
            output += CompilationEngine.compile_expression(tokens[tokens.index('else')+2:tokens[::-1].index('}')]) + '\t\t\t\t\t' + JackTokenizer.symbol('}')
        else:
            output += CompilationEngine.compile_statements(tokens[tokens.index('{')+1, tokens[::-1].index('}')]) + '\t\t\t\t\t' + JackTokenizer.symbol('}')
        output += '\t\t\t\t</ifStatement>\n'
        return output

    @staticmethod
    def compile_expression(tokens):
        output = ''
        return output

    @staticmethod
    def compile_term(tokens):
        output = ''
        return output

    @staticmethod
    def compile_expression_list(tokens):
        output = '\t\t\t\t\t<expressionList>\n'
        comma_indexes = []
        for i in range(len(tokens)):
            if tokens[i][1] == ',':
                comma_indexes.append(i)
        output += CompilationEngine.compile_expression(tokens[:comma_indexes[0]])
        for i in range(1, len(comma_indexes)):
            output += '\t\t\t\t\t\t' + JackTokenizer.symbol(',') + CompilationEngine.compile_expression(tokens[:comma_indexes[i]])
        return output
    

class JackAnalyzer:
    def __init__(self, file_name):
        test_jack_tokenizer = JackTokenizer(file_name)
        test_jack_tokenizer.advance()
        test_compilation_engine = CompilationEngine(file_name)
        test_compilation_engine.compile_class()


test_jack_tokenizer = JackTokenizer('Square/SquareGame.jack')
test_jack_tokenizer.advance()
