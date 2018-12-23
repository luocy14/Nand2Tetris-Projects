import re
from SymbolTable import SymbolTable


class CompilationEngine:
    CONVERT_KIND = {
        'ARG': 'ARG',
        'STATIC': 'STATIC',
        'VAR': 'VAR',
        'FIELD': 'THIS'
    }

    ARITHMETIC = {
        '+': 'ADD',
        '-': 'SUB',
        '=': 'EQ',
        '>': 'GT',
        '<': 'LT',
        '&': 'AND',
        '|': 'OR'
    }

    ARITHMETIC_UNARY = {
        '-': 'NEG',
        '~': 'NOT'
    }

    if_index = -1
    while_index = -1

    def __init__(self, vm_writer, tokenizer):
        self.vm_writer = vm_writer
        self.tokenizer = tokenizer
        self.symbol_table = SymbolTable()
        self.buffer = []

    # 'class' className '{' classVarDec* subroutineDec* '}'
    def compile_class(self):
        self.get_token()  # 'class'
        self.class_name = self.get_token()  # className
        self.get_token()  # '{'
        while self.is_class_var_dec():
            self.compile_class_var_dec()  # classVarDec*
        while self.is_subroutine_dec():
            self.compile_subroutine()  # subroutineDec*
        self.vm_writer.close()

    # ('static' | 'field' ) type varName (',' varName)* ';'
    def compile_class_var_dec(self):
        kind = self.get_token()  # ('static' | 'field' )
        type = self.get_token()  # type
        name = self.get_token()  # varName
        self.symbol_table.define(name, type, kind.upper())
        while self.peek() != ';':  # (',' varName)*
            self.get_token()  # ','
            name = self.get_token()  # varName
            self.symbol_table.define(name, type, kind.upper())
        self.get_token()  # ';'

    # subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
    # subroutineBody: '{' varDec* statements '}'
    def compile_subroutine(self):
        subroutine_kind = self.get_token()  # ('constructor' | 'function' | 'method')
        self.get_token()  # ('void' | type)
        subroutine_name = self.get_token()  # subroutineName
        self.symbol_table.start_subroutine()
        if subroutine_kind == 'method':
            self.symbol_table.define('instance', self.class_name, 'ARG')
        self.get_token()  # '('
        self.compile_parameter_list()  # parameterList
        self.get_token()  # ')'
        self.get_token()  # '{'
        while self.peek() == 'var':
            self.compile_var_dec()  # varDec*
        function_name = '{}.{}'.format(self.class_name, subroutine_name)
        num_locals = self.symbol_table.var_count('VAR')
        self.vm_writer.write_function(function_name, num_locals)
        if subroutine_kind == 'constructor':
            num_fields = self.symbol_table.var_count('FIELD')
            self.vm_writer.write_push('CONST', num_fields)
            self.vm_writer.write_call('Memory.alloc', 1)
            self.vm_writer.write_pop('POINTER', 0)
        elif subroutine_kind == 'method':
            self.vm_writer.write_push('ARG', 0)
            self.vm_writer.write_pop('POINTER', 0)
        self.compile_statements()  # statements
        self.get_token()  # '}'

    # ( (type varName) (',' type varName)*)?
    def compile_parameter_list(self):
        if ')' != self.peek():
            type = self.get_token()  # type
            name = self.get_token()  # varName
            self.symbol_table.define(name, type, 'ARG')
        while ')' != self.peek():
            self.get_token()  # ','
            type = self.get_token()  # type
            name = self.get_token()  # varName
            self.symbol_table.define(name, type, 'ARG')

    # 'var' type varName (',' varName)* ';'
    def compile_var_dec(self):
        self.get_token()  # 'var'
        type = self.get_token()  # type
        name = self.get_token()  # varName
        self.symbol_table.define(name, type, 'VAR')
        while self.peek() != ';':  # (',' varName)*
            self.get_token()  # ','
            name = self.get_token()  # varName
            self.symbol_table.define(name, type, 'VAR')
        self.get_token()  # ';'

    # statement*
    # letStatement | ifStatement | whileStatement | doStatement | returnStatement
    def compile_statements(self):
        while self.is_statement():
            token = self.get_token()
            if token == 'let':
                self.compile_let()
            elif token == 'if':
                self.compile_if()
            elif token == 'while':
                self.compile_while()
            elif token == 'do':
                self.compile_do()
            elif token == 'return':
                self.compile_return()

    # 'do' subroutineCall ';'
    def compile_do(self):
        self.compile_subroutine_call()
        self.vm_writer.write_pop('TEMP', 0)
        self.get_token()  # ';'

    # 'let' varName ('[' expression ']')? '=' expression ';'
    def compile_let(self):
        var_name = self.get_token()  # varName
        var_kind = self.CONVERT_KIND[self.symbol_table.kind_of(var_name)]
        var_index = self.symbol_table.index_of(var_name)
        if self.peek() == '[':  # array assignment
            self.get_token()  # '['
            self.compile_expression()  # expression
            self.get_token()  # ']'
            self.vm_writer.write_push(var_kind, var_index)
            self.vm_writer.write_arithmetic('ADD')
            self.vm_writer.write_pop('TEMP', 0)
            self.get_token()  # '='
            self.compile_expression()  # expression
            self.get_token()  # ';'
            self.vm_writer.write_push('TEMP', 0)
            self.vm_writer.write_pop('POINTER', 1)
            self.vm_writer.write_pop('THAT', 0)
        else:  # regular assignment
            self.get_token()  # '='
            self.compile_expression()  # expression
            self.get_token()  # ';'
            self.vm_writer.write_pop(var_kind, var_index)

    # 'while' '(' expression ')' '{' statements '}'
    def compile_while(self):
        self.while_index += 1
        while_index = self.while_index
        self.vm_writer.write_label('WHILE{}\n'.format(while_index))
        self.get_token()  # '('
        self.compile_expression()  # expression
        self.vm_writer.write_arithmetic('NOT')  # eval false condition first
        self.get_token()  # ')'
        self.get_token()  # '{'
        self.vm_writer.write_if('WHILE_END{}\n'.format(while_index))
        self.compile_statements()  # statements
        self.vm_writer.write_goto('WHILE{}\n'.format(while_index))
        self.vm_writer.write_label('WHILE_END{}\n'.format(while_index))
        self.get_token()  # '}'

    # 'return' expression? ';'
    def compile_return(self):
        if self.peek() != ';':
            self.compile_expression()
        else:
            self.vm_writer.write_push('CONST', 0)
        self.vm_writer.write_return()
        self.get_token()  # ';'

    # 'if' '(' expression ')' '{' statements '}' ( 'else' '{' statements '}' )?
    def compile_if(self):
        self.if_index += 1
        if_index = self.if_index
        self.get_token()  # '('
        self.compile_expression()  # expression
        self.get_token()  # ')'
        self.get_token()  # '{'
        self.vm_writer.write_if('IF_TRUE{}\n'.format(if_index))
        self.vm_writer.write_goto('IF_FALSE{}\n'.format(if_index))
        self.vm_writer.write_label('IF_TRUE{}\n'.format(if_index))
        self.compile_statements()  # statements
        self.vm_writer.write_goto('IF_END{}\n'.format(if_index))
        self.get_token()  # '}'
        self.vm_writer.write_label('IF_FALSE{}\n'.format(if_index))
        if self.peek() == 'else':  # ( 'else' '{' statements '}' )?
            self.get_token()  # 'else'
            self.get_token()  # '{'
            self.compile_statements()  # statements
            self.get_token()  # '}'
        self.vm_writer.write_label('IF_END{}\n'.format(if_index))

    # term (op term)*
    def compile_expression(self):
        self.compile_term()  # term
        while self.is_op():  # (op term)*
            op = self.get_token()  # op
            self.compile_term()  # term
            if op in self.ARITHMETIC.keys():
                self.vm_writer.write_arithmetic(self.ARITHMETIC[op])
            elif op == '*':
                self.vm_writer.write_call('Math.multiply', 2)
            elif op == '/':
                self.vm_writer.write_call('Math.divide', 2)

    # integerConstant | stringConstant | keywordConstant | varName |
    # varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
    def compile_term(self):
        if self.is_unary_op_term():
            unary_op = self.get_token()  # unaryOp
            self.compile_term()  # term
            self.vm_writer.write_arithmetic(self.ARITHMETIC_UNARY[unary_op])
        elif self.peek() == '(':
            self.get_token()  # '('
            self.compile_expression()  # expression
            self.get_token()  # ')'
        elif self.peek_type() == 'INT_CONST':  # integerConstant
            self.vm_writer.write_push('CONST', self.get_token())
        elif self.peek_type() == 'STRING_CONST':  # stringConstant
            self.compile_string()
        elif self.peek_type() == 'KEYWORD':  # keywordConstant
            self.compile_keyword()
        else:  # first is a var or subroutine
            if self.is_array():
                array_var = self.get_token()  # varName
                self.get_token()  # '['
                self.compile_expression()  # expression
                self.get_token()  # ']'
                array_kind = self.symbol_table.kind_of(array_var)
                array_index = self.symbol_table.index_of(array_var)
                self.vm_writer.write_push(self.CONVERT_KIND[array_kind], array_index)
                self.vm_writer.write_arithmetic('ADD')
                self.vm_writer.write_pop('POINTER', 1)
                self.vm_writer.write_push('THAT', 0)
            elif self.is_subroutine_call():
                self.compile_subroutine_call()
            else:
                var = self.get_token()
                var_kind = self.CONVERT_KIND[self.symbol_table.kind_of(var)]
                var_index = self.symbol_table.index_of(var)
                self.vm_writer.write_push(var_kind, var_index)

    # (expression (',' expression)* )?
    def compile_expression_list(self):
        number_args = 0
        if self.peek() != ')':
            number_args += 1
            self.compile_expression()
        while self.peek() != ')':
            number_args += 1
            self.get_token()  # ','
            self.compile_expression()
        return number_args

    # private
    def compile_keyword(self):
        keyword = self.get_token()  # keywordConstant
        if keyword == 'this':
            self.vm_writer.write_push('POINTER', 0)
        else:
            self.vm_writer.write_push('CONST', 0)
            if keyword == 'true':
                self.vm_writer.write_arithmetic('NOT')

    # subroutineCall: subroutineName '(' expressionList ')' | ( className | varName) '.' subroutineName '(' expressionList ')'
    def compile_subroutine_call(self):
        identifier = self.get_token()  # (subroutineName | className | varName)
        function_name = identifier
        number_args = 0
        if self.peek() == '.':
            self.get_token()  # '.'
            subroutine_name = self.get_token()  # subroutineName
            type = self.symbol_table.type_of(identifier)
            if type != 'NONE':  # it's an instance
                instance_kind = self.symbol_table.kind_of(identifier)
                instance_index = self.symbol_table.index_of(identifier)
                self.vm_writer.write_push(self.CONVERT_KIND[instance_kind], instance_index)
                function_name = '{}.{}'.format(type, subroutine_name)
                number_args += 1
            else:  # it's a class
                class_name = identifier
                function_name = '{}.{}'.format(class_name, subroutine_name)
        elif self.peek() == '(':
            subroutine_name = identifier
            function_name = '{}.{}'.format(self.class_name, subroutine_name)
            number_args += 1
            self.vm_writer.write_push('POINTER', 0)
        self.get_token()  # '('
        number_args += self.compile_expression_list()  # expressionList
        self.get_token()  # ')'
        self.vm_writer.write_call(function_name, number_args)

    def compile_string(self):
        string = self.get_token()  # stringConstant
        self.vm_writer.write_push('CONST', len(string))
        self.vm_writer.write_call('String.new', 1)
        for char in string:
            self.vm_writer.write_push('CONST', ord(char))
            self.vm_writer.write_call('String.appendChar', 2)

    def is_subroutine_call(self):
        token = self.get_token()
        subroutine_call = self.peek() in ['.', '(']
        self.unget_token(token)
        return subroutine_call

    def is_array(self):
        token = self.get_token()
        array = self.peek() == '['
        self.unget_token(token)
        return array

    def is_class_var_dec(self):
        return self.peek() in ['static', 'field']

    def is_subroutine_dec(self):
        return self.peek() in ['constructor', 'function', 'method']

    def is_statement(self):
        return self.peek() in ['let', 'if', 'while', 'do', 'return']

    def is_op(self):
        return self.peek() in ['+', '-', '*', '/', '&', '|', '<', '>', '=']

    def is_unary_op_term(self):
        return self.peek() in ['~', '-']

    def peek(self):
        return self.peek_info()[0]

    def peek_type(self):
        return self.peek_info()[1]

    def peek_info(self):
        token_info = self.get_token_info()
        self.unget_token_info(token_info)
        return token_info

    def get_token(self):
        return self.get_token_info()[0]

    def get_token_info(self):
        if self.buffer:
            return self.buffer.pop(0)
        else:
            return self.get_next_token()

    def unget_token(self, token):
        self.unget_token_info((token, 'UNKNOWN'))

    def unget_token_info(self, token):
        self.buffer.insert(0, token)

    def get_next_token(self):
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            if self.tokenizer.token_type() is 'KEYWORD':
                return self.tokenizer.key_word().lower(), self.tokenizer.token_type()
            elif self.tokenizer.token_type() is 'SYMBOL':
                return self.tokenizer.symbol(), self.tokenizer.token_type()
            elif self.tokenizer.token_type() is 'IDENTIFIER':
                return self.tokenizer.identifier(), self.tokenizer.token_type()
            elif self.tokenizer.token_type() is 'INT_CONST':
                return self.tokenizer.intVal(), self.tokenizer.token_type()
            elif self.tokenizer.token_type() is 'STRING_CONST':
                return self.tokenizer.stringVal(), self.tokenizer.token_type()
