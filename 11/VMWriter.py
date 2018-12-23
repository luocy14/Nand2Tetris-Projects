class VMWriter:
    def __init__(self, output_file):
        self.output = output_file

    # Writes a VM push command
    # CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP
    def write_push(self, segment, index):
        if segment == 'CONST':
            segment = 'constant'
        elif segment == 'ARG':
            segment = 'argument'
        self.output.write('push {} {}\n'.format(segment.lower(), index))

    # Writes a VM pop command
    # CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP
    def write_pop(self, segment, index):
        if segment == 'CONST':
            segment = 'constant'
        elif segment == 'ARG':
            segment = 'argument'
        self.output.write('pop {} {}\n'.format(segment.lower(), index))

    # Writes a VM arithmetic command
    # command (ADD, SUB, NEG, EQ, GT, LT, AND, OR, NOT)
    def write_arithmetic(self, command):
        self.output.write(command.lower() + '\n')

    # Writes a VM label command
    def write_label(self, label):
        self.output.write('label {}'.format(label))

    # Writes a VM label command
    def write_goto(self, label):
        self.output.write('goto {}'.format(label))

    # Writes a VM If-goto command
    def write_if(self, label):
        self.output.write('if-goto {}'.format(label))

    # Writes a VM call command
    def write_call(self, name, nArgs):
        self.output.write('call {} {}\n'.format(name, nArgs))

    # Writes a VM function command
    def write_function(self, name, nLocals):
        self.output.write('function {} {}\n'.format(name, nLocals))

    # Writes a VM return command
    def write_return(self):
        self.output.write('return\n')

    # Closes the output file
    def close(self):
        self.output.close()

    # private
    def write(self, stuff):
        self.output.write(stuff)
