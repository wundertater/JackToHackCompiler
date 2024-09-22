class CodeWriter:

    def __init__(self, file, main_class, filename):
        self.file = file  # file opened in append mode
        self.VMTranslator = main_class
        self.filename = filename

    def push_D(self):
        # Pushes to the stack value of D register
        return '@SP\nA=M\nM=D\n@SP\nM=M+1\n'

    def pop_to_D(self):
        # Pops the last value from the stack to the D register
        return '@SP\nAM=M-1\nD=M\n'

    def write_command_description(self, desc):
        """
        Write to the file auto generating command description
        """
        if self.VMTranslator.write_desc:  # if script is running without no-desc flag
            self.file.write(desc)

    def WriteArithmetic(self, command: str):
        """
        Write to the file arithmetic code
        :param command: add, sub, neg, eq, gt, lt, and, or, not
        """
        desc = f'// {command}\n'
        self.write_command_description(desc)

        if command == 'neg' or command == 'not':
            code = '@SP\nA=M-1\nM=-M\n'
            if command == 'not':
                code = code + 'M=M-1\n'

        elif command in ('eq', 'gt', 'lt'):
            jump_label = 'TRUE.' + str(self.VMTranslator.comp_label_num)
            self.VMTranslator.comp_label_num += 1
            if command == 'eq':
                jump_cmd = 'JEQ'
            elif command == 'lt':
                jump_cmd = 'JLT'
            else:  # gt command
                jump_cmd = 'JGT'
            code = (f'{self.pop_to_D()}@SP\nA=M-1\nD=M-D\nM=-1\n'
                    f'@{jump_label}\nD;{jump_cmd}\n@SP\nA=M-1\nM=0\n({jump_label})\n')

        else:  # add, sub, and, or
            if command == 'add':
                operation = 'M=D+M\n'
            elif command == 'sub':
                operation = 'M=M-D\n'
            elif command == 'and':
                operation = 'M=D&M\n'
            else:  # or
                operation = 'M=D|M\n'
            code = f'{self.pop_to_D()}@SP\nA=M-1\n' + operation

        self.file.write(code)

    def WritePushPop(self, command: str, segment: str, index):
        """
        Write push or pop commands to the file
        :param command: push or pop
        :param segment: local, argument, this, that, temp, static, pointer
        :param index: non-negative integer number
        """
        desc = f'// {command} {segment} {index}\n'
        self.write_command_description(desc)

        segment_map = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT', 'temp': 'temp',
                       'static': 'static', 'pointer': 'pointer', 'constant': 'constant'}
        segment = segment_map[segment]

        if segment == 'static':
            addr = f'{self.filename}.{index}'
        elif segment == 'pointer':
            addr = 'THAT' if index == '1' else 'THIS'  # if index == 0 -> addr=THIS, if index == 1 -> addr=THAT

        if command == 'pop':
            if segment == 'static' or segment == 'pointer':
                code = f'{self.pop_to_D()}@{addr}\nM=D\n'
            else:  # segments LCL, ARG, THIS, THAT, temp
                if segment == 'temp':
                    temp_value = 5 + int(index)  # 5 is base address of temp
                    code = f'@{temp_value}\nD=A\n@R13\nM=D\n{self.pop_to_D()}@R13\nA=M\nM=D\n'
                else:
                    code = f'@{segment}\nD=M\n@{index}\nD=D+A\n@R13\nM=D\n{self.pop_to_D()}@R13\nA=M\nM=D\n'

        else:  # push
            if segment == 'static' or segment == 'pointer':
                code = f'@{addr}\nD=M\n{self.push_D()}'
            else:  # segments LCL, ARG, THIS, THAT, temp, constant
                if segment == 'temp':
                    temp_value = 5 + int(index)
                    head = f'@{temp_value}\nD=M\n'
                elif segment == 'constant':
                    head = f'@{index}\nD=A\n'
                else:
                    head = f'@{segment}\nD=M\n@{index}\nA=D+A\nD=M\n'
                code = head + self.push_D()

        self.file.write(code)

    def WriteBranching(self, command, label_name):
        """
        Write to a file branching code
        :param command: label, goto, if-goto
        """
        desc = f'// {command} {label_name}\n'
        self.write_command_description(desc)

        if command == 'label':
            code = f'({label_name})\n'
        elif command == 'goto':
            code = f'@{label_name}\n0;JMP\n'
        else:  # if-goto
            code = f'{self.pop_to_D()}@{label_name}\nD;JNE\n'

        self.file.write(code)

    def WriteFunction(self, command, func_name=None, n_vals=None):
        """
        Write function code to the file
        :param command: function, return, call
        :param n_vals: number of local variables or arguments
        """
        if func_name is None:
            desc = f'// {command}\n'
        else:
            desc = f'// {command} {func_name} {n_vals}\n'
        self.write_command_description(desc)

        if command == 'function':
            init_nVars = '@SP\nA=M\nM=0\n@SP\nM=M+1\n'
            code = f'({func_name})\n' + init_nVars * int(n_vals)

        elif command == 'call':
            push_D = self.push_D()
            ARG_repos = 5 + int(n_vals)
            return_addr = f'{func_name}$ret.{self.VMTranslator.func_label_num}'
            self.VMTranslator.func_label_num += 1
            code = (f'@{return_addr}\nD=A\n{push_D}'  # push return address
                    f'@LCL\nD=M\n{push_D}'  # push LCL
                    f'@ARG\nD=M\n{push_D}'  # push ARG
                    f'@THIS\nD=M\n{push_D}'  # push THIS
                    f'@THAT\nD=M\n{push_D}'  # push THAT
                    f'@{ARG_repos}\nD=A\n@SP\nD=M-D\n@ARG\nM=D\n'  # reposition ARG
                    '@SP\nD=M\n@LCL\nM=D\n'  # reposition LCL
                    f'@{func_name}\n0;JMP\n'  # goto function
                    f'({return_addr})\n')

        else:  # return command
            code = ('@5\nD=A\n@LCL\nA=M-D\nD=M\n@R13\nM=D\n'  # saving to R13 return address value
                    '@SP\nA=M-1\nD=M\n@ARG\nA=M\nM=D\n'  # *ARG=pop()
                    'D=A\n@SP\nM=D+1\n'  # SP=ARG+1
                    '@LCL\nAM=M-1\nD=M\n@THAT\nM=D\n'  # restoring THAT value
                    '@LCL\nAM=M-1\nD=M\n@THIS\nM=D\n'  # restoring THIS value
                    '@LCL\nAM=M-1\nD=M\n@ARG\nM=D\n'  # restoring ARG value
                    '@LCL\nA=M-1\nD=M\n@LCL\nM=D\n'  # restoring LCL value
                    '@R13\nA=M\n0;JMP\n')  # goto return address

        self.file.write(code)

    def bootstrap(self):
        """
        Write the bootstrap code to the file to initialize the VM
        """
        stack_pointer_start_value = 261
        desc = '// bootstrap\n'
        self.write_command_description(desc)

        code = (f'@{stack_pointer_start_value}\nD=A\n@SP\nM=D\n'  # booting stack pointer
                '@Sys.init\n0;JMP\n')  # calling Sys.init function
        self.file.write(code)
