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
                                    self.process_prev_string(''.join(list_cur_item[:list_cur_item.index(char)]))
                                    self.symbol(char)
                                    list_cur_item = list_cur_item[list_cur_item.index(char) + 1:]
                                elif char == '\"':
                                    if in_string:
                                        cur_string += (' ' + ''.join(list_cur_item[:list_cur_item.index(char)]))
                                        self.string_val(cur_string)
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
                            self.keyword(item)
                        elif item.isdigit():
                            self.int_val(item)
                        elif item in JackTokenizer.symbols:
                            self.symbol(item)
                        elif item.isalnum():
                            self.identifier(item)
                        else:
                            list_cur_item = list(item)
                            for char in list_cur_item:
                                if char in JackTokenizer.symbols:
                                    self.process_prev_string(''.join(list_cur_item[:list_cur_item.index(char)]))
                                    self.symbol(char)
                                    list_cur_item = list_cur_item[list_cur_item.index(char) + 1:]
                                elif char == '\"':
                                    in_string = not in_string
                                    cur_string += ''.join(list_cur_item[list_cur_item.index(char) + 1:])
                                    break
                                elif list_cur_item.index(char) == len(list_cur_item) - 1:
                                    self.process_prev_string(''.join(list_cur_item))
            cur_line = self.jack_file.readline()
        self.xml_file.write('</tokens>\n')

    def process_prev_string(self, prev_string):
        if prev_string == '':
            pass
        elif prev_string in JackTokenizer.keywords:
            self.keyword(prev_string)
        elif prev_string.isdigit():
            self.int_val(prev_string)
        else:
            self.identifier(prev_string)

    def keyword(self, key_word):
        self.xml_file.write('<keyword> ' + key_word + ' </keyword>\n')

    def symbol(self, symbol):
        if symbol == '<':
            self.xml_file.write('<symbol> &lt; </symbol>\n')
        elif symbol == '>':
            self.xml_file.write('<symbol> &gt; </symbol>\n')
        elif symbol == '&':
            self.xml_file.write('<symbol> &amp; </symbol>\n')
        else:
            self.xml_file.write('<symbol> ' + symbol + ' </symbol>\n')

    def identifier(self, identifier):
        self.xml_file.write('<identifier> ' + identifier + ' </identifier>\n')

    def int_val(self, int_val):
        self.xml_file.write('<integerConstant> ' + str(int_val) + ' </integerConstant>\n')

    def string_val(self, string_val):
        self.xml_file.write('<stringConstant> ' + string_val + ' </stringConstant>\n')


test_jack_tokenizer = JackTokenizer("ArrayTest\Main.jack")
test_jack_tokenizer.advance()
