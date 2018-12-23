from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine
from VMWriter import VMWriter
from Util import Util
from FileSet import FileSet
import os


class JackCompiler:
    @staticmethod
    def jack_compiler():
        path = Util.get_command_line_argument(1)
        if os.path.isdir(path):
            files = FileSet(path, 'jack')
            while files.has_more_files():
                filename = files.next_file()
                JackCompiler.compile_jack(filename)
        elif os.path.isfile(path):
            JackCompiler.compile_jack(path)
        else:
            print('{} is not a file or dir'.format(path))

    @staticmethod
    def compile_jack(jack_file_name):
        token_file_name = jack_file_name.replace('.jack', 'T.xml')
        token_file = open(token_file_name, 'w')
        jack_file = open(jack_file_name, 'rU')
        tokenizer = JackTokenizer(jack_file, token_file)
        vm_file = open(jack_file_name.replace('.jack', '') + '.vm', 'w')
        vm_writer = VMWriter(vm_file)
        engine = CompilationEngine(vm_writer, tokenizer)
        engine.compile_class()


JackCompiler.jack_compiler()
