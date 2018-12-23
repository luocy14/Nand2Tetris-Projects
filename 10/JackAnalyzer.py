import re
import itertools


class JackTokenizer:
    keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean',
                'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
    symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']

    def __init__(self, file_name):
        self.jack_file = open(file_name, 'r')
        self.t_xml_file = open(file_name.replace('.jack', 'T.xml'), 'w')
        self.t_xml_file.write('<tokens>\n')

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
                                        self.t_xml_file.write(JackTokenizer.process_prev_string(
                                            ''.join(list_cur_item[:list_cur_item.index(char)])))
                                    self.t_xml_file.write(JackTokenizer.symbol(char))
                                    list_cur_item = list_cur_item[list_cur_item.index(char) + 1:]
                                elif char == '\"':
                                    if in_string:
                                        cur_string += (' ' + ''.join(list_cur_item[:list_cur_item.index(char)]))
                                        self.t_xml_file.write(JackTokenizer.string_val(cur_string))
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
                            self.t_xml_file.write(JackTokenizer.keyword(item))
                        elif item.isdigit():
                            self.t_xml_file.write(JackTokenizer.int_val(item))
                        elif item in JackTokenizer.symbols:
                            self.t_xml_file.write(JackTokenizer.symbol(item))
                        elif item.isalnum():
                            self.t_xml_file.write(JackTokenizer.identifier(item))
                        else:
                            list_cur_item = list(item)
                            for char in list_cur_item:
                                if char in JackTokenizer.symbols:
                                    if list_cur_item.index(char) != 0:
                                        self.t_xml_file.write(JackTokenizer.process_prev_string(
                                            ''.join(list_cur_item[:list_cur_item.index(char)])))
                                    self.t_xml_file.write(JackTokenizer.symbol(char))
                                    list_cur_item = list_cur_item[list_cur_item.index(char) + 1:]
                                elif char == '\"':
                                    in_string = not in_string
                                    cur_string += ''.join(list_cur_item[list_cur_item.index(char) + 1:])
                                    break
                                elif list_cur_item.index(char) == len(list_cur_item) - 1:
                                    self.t_xml_file.write(JackTokenizer.process_prev_string(''.join(list_cur_item)))
            cur_line = self.jack_file.readline()
        self.t_xml_file.write('</tokens>\n')
        self.t_xml_file.close()
        self.jack_file.close()

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
    op = ['+', '-', '*', '/', '&', '|', '<', '>', '=']

    def __init__(self, file_name):
        self.t_xml_file = open(file_name.replace('.jack', 'T.xml'), 'r')
        self.xml_file = open(file_name.replace('.jack', '.xml'), 'w')
        self.indent_count = 0
        self.written = True
        self.t_xml_file.readline()  # skip <tokens> line

    # className '{' classVarDec* subroutineDec* '}'
    def compile_class(self):
        self.write_open_tag('class')
        self.write_next_token()  # 'class'
        self.write_next_token()  # className
        self.write_next_token()  # '{'
        while self.is_class_var_dec():
            self.compile_class_var_dec()
            self.save_token_if_written()

        while self.is_subroutine_dec():
            self.compile_subroutine()
            self.save_token_if_written()

        self.write_next_token()  # '}'
        self.write_close_tag('class')

    def compile_class_var_dec(self):
        self.write_open_tag('classVarDec')
        self.write_next_token()  # '('static' | 'field')'
        self.write_next_token()  # type
        self.write_next_token()  # varName
        self.compile_multiple(',', 'identifier')  # (',' varName)*
        self.write_next_token()  # ';'
        self.write_close_tag('classVarDec')

    # subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
    # subroutineBody: '{' varDec* statements '}'
    def compile_subroutine(self):
        self.write_open_tag('subroutineDec')
        self.write_next_token()  # ('constructor' | 'function' | 'method')
        self.write_next_token()  # ('void' | type)
        self.write_next_token()  # subroutineName
        self.write_next_token()  # '('
        self.compile_parameter_list()  # parameterList
        self.write_next_token()  # ')'
        self.write_open_tag('subroutineBody')
        self.write_next_token()  # '{'
        self.save_token_if_written()
        while 'var' in self.current_token:
            self.compile_var_dec()  # varDec*
            self.save_token_if_written()
        self.compile_statements()  # statements
        self.write_next_token()  # '}'
        self.write_close_tag('subroutineBody')
        self.write_close_tag('subroutineDec')

    # ( (type varName) (',' type varName)*)?
    def compile_parameter_list(self):
        self.write_open_tag('parameterList')
        self.save_token_if_written()
        if ')' not in self.current_token:
            self.write_next_token()  # type
            self.write_next_token()  # varName
            self.save_token_if_written()
        while ')' not in self.current_token:
            self.write_next_token()  # ','
            self.write_next_token()  # type
            self.write_next_token()  # varName
            self.save_token_if_written()
        self.write_close_tag('parameterList')

    # 'var' type varName (',' varName)* ';'
    def compile_var_dec(self):
        self.write_open_tag('varDec')
        self.write_next_token()  # 'var'
        self.write_next_token()  # type
        self.write_next_token()  # varName
        self.compile_multiple(',', 'identifier')  # (',' varName)*
        self.write_next_token()  # ';'
        self.write_close_tag('varDec')

    # statement*
    # letStatement | ifStatement | whileStatement | doStatement | returnStatement
    def compile_statements(self):
        self.write_open_tag('statements')
        while self.is_statement():
            if 'let' in self.current_token:
                self.compile_let()
            elif 'if' in self.current_token:
                self.compile_if()
            elif 'while' in self.current_token:
                self.compile_while()
            elif 'do' in self.current_token:
                self.compile_do()
            elif 'return' in self.current_token:
                self.compile_return()
            self.save_token_if_written()
        self.write_close_tag('statements')

    # 'do' subroutineCall ';'
    # subroutineCall: subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName '(' expressionList ')'
    def compile_do(self):
        self.write_open_tag('doStatement')
        self.write_next_token()  # 'do'
        self.write_next_token()  # (subroutineName | className | varName)
        self.save_token_if_written()
        if '.' in self.current_token:
            self.write_next_token()  # '.'
            self.write_next_token()  # subroutineName
        self.write_next_token()  # '('
        self.compile_expression_list()  # expressionList
        self.write_next_token()  # ')'
        self.write_next_token()  # ';'
        self.write_close_tag('doStatement')

    # 'let' varName ('[' expression ']')? '=' expression ';'
    def compile_let(self):
        self.write_open_tag('letStatement')
        self.write_next_token()  # 'let'
        self.write_next_token()  # varName
        self.save_token_if_written()
        if '[' in self.current_token:  # ('[' expression ']')?
            self.write_next_token()  # '['
            self.compile_expression()  # expression
            self.write_next_token()  # ']'
        self.write_next_token()  # '='
        self.compile_expression()  # expression
        self.write_next_token()  # ';'
        self.write_close_tag('letStatement')

    # 'while' '(' expression ')' '{' statements '}'
    def compile_while(self):
        self.write_open_tag('whileStatement')
        self.write_next_token()  # 'while'
        self.write_next_token()  # '('
        self.compile_expression()  # expression
        self.write_next_token()  # ')'
        self.write_next_token()  # '{'
        self.compile_statements()  # statements
        self.write_next_token()  # '}'
        self.write_close_tag('whileStatement')

    # 'return' expression? ';'
    def compile_return(self):
        self.write_open_tag('returnStatement')
        self.write_next_token()  # 'return'
        self.save_token_if_written()
        if ';' not in self.current_token:  # expression?
            self.compile_expression()  # expression
        self.write_next_token()  # ';'
        self.write_close_tag('returnStatement')

    # 'if' '(' expression ')' '{' statements '}' ( 'else' '{' statements '}' )?
    def compile_if(self):
        self.write_open_tag('ifStatement')
        self.write_next_token()  # if
        self.write_next_token()  # '('
        self.compile_expression()  # expression
        self.write_next_token()  # ')'
        self.write_next_token()  # '{'
        self.compile_statements()  # statements
        self.write_next_token()  # '}'
        self.save_token_if_written()
        if 'else' in self.current_token:  # else?
            self.write_next_token()  # else
            self.write_next_token()  # '{'
            self.compile_statements()  # statements
            self.write_next_token()  # '}'
        self.write_close_tag('ifStatement')

    # term (op term)*
    def compile_expression(self):
        self.write_open_tag('expression')
        self.compile_term()  # term
        while self.is_op():
            self.write_next_token()  # op
            self.compile_term()  # term
        self.write_close_tag('expression')

    # integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
    def compile_term(self):
        self.write_open_tag('term')
        self.save_token_if_written()
        if self.is_unary_op_term():
            self.write_next_token()  # unaryOp
            self.compile_term()  # term
        elif '(' in self.current_token:
            self.write_next_token()  # '('
            self.compile_expression()  # expression
            self.write_next_token()  # ')'
        else:  # first is an identifier
            self.write_next_token()  # identifier
            self.save_token_if_written()
            if '[' in self.current_token:
                self.write_next_token()  # '['
                self.compile_expression()  # expression
                self.write_next_token()  # ']'
            elif '.' in self.current_token:
                self.write_next_token()  # '.'
                self.write_next_token()  # subroutineName
                self.write_next_token()  # '('
                self.compile_expression_list()  # expressionList
                self.write_next_token()  # ')'
            elif '(' in self.current_token:
                self.write_next_token()  # '('
                self.compile_expression_list()  # expressionList
                self.write_next_token()  # ')'
        self.write_close_tag('term')

    # (expression (',' expression)* )?
    def compile_expression_list(self):
        self.write_open_tag('expressionList')
        self.save_token_if_written()
        if ')' not in self.current_token:
            self.compile_expression()  # expression
            self.save_token_if_written()  # for while
        while ')' not in self.current_xml_token:
            self.write_next_token()  # ','
            self.compile_expression()  # expression
            self.save_token_if_written()
        self.write_close_tag('expressionList')

    # starts here
    def compile_multiple(self, first_identifier, second_identifier):
        self.save_token_if_written()
        while first_identifier in self.current_token or second_identifier in self.current_token:
            self.write_next_token()
            self.save_token_if_written()

    def is_class_var_dec(self):
        self.save_token_if_written()
        return 'static' in self.current_token or 'field' in self.current_token

    def is_subroutine_dec(self):
        self.save_token_if_written()
        return 'constructor' in self.current_token or 'function' in self.current_token or 'method' in self.current_token

    def is_statement(self):
        self.save_token_if_written()
        return 'let' in self.current_token or 'if' in self.current_token or 'while' in self.current_token or 'do' in self.current_token or 'return' in self.current_token

    def is_op(self):
        self.save_token_if_written()
        return re.search(r'> (\+|-|\*|/|&amp;|\||&lt;|&gt;|=) <', self.current_token)

    def is_unary_op_term(self):
        self.save_token_if_written()
        return re.search(r'> (-|~) <', self.current_token)

    def write_next_token(self):
        if self.written:
            self.current_token = self.t_xml_file.readline()
        else:
            self.written = True
        self.xml_file.write(self.current_indent() + self.current_token)

    def save_token_if_written(self):
        if self.written:
            self.current_token = self.t_xml_file.readline()
            self.written = False

    def write_open_tag(self, tag):
        self.xml_file.write(self.current_indent() + '<' + tag + '>\n')
        self.indent_count += 1

    def write_close_tag(self, tag):
        self.indent_count -= 1
        self.xml_file.write(self.current_indent() + '</' + tag + '>\n')

    def current_indent(self):
        return '\t' * self.indent_count


class JackAnalyzer:
    def __init__(self, file_name):
        test_jack_tokenizer = JackTokenizer(file_name)
        test_jack_tokenizer.advance()
        test_compilation_engine = CompilationEngine(file_name)
        test_compilation_engine.compile_class()


test_jack_analyzer = JackAnalyzer('')  # enter your file path here
