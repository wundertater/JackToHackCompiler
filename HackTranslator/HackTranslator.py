import sys
import os
from Parser import Parser
from Code import Code


class HackTranslator:

    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        path, filename = os.path.split(path_to_file)
        self.path = path + "\\" if path else ''
        filename, _ = os.path.splitext(filename)
        self.filename = filename + '.hack'

        self.parser = Parser()
        self.code = Code()

    def assemble(self):
        with open(self.path_to_file) as f:
            formatted_commands = self.fst_pass_assemble(f)
            self.snd_pass_assemble(formatted_commands)

    def fst_pass_assemble(self, file):
        formatted_lines = []
        index = 0
        for line in file:
            formatted_line = self.parser.parse_fst_pass(line, index)
            if formatted_line:
                formatted_lines.append(formatted_line)
                index += 1
        return formatted_lines

    def snd_pass_assemble(self, commands):
        with open(self.path + self.filename, 'w') as f:
            for command in commands:
                if self.parser.cmd_type(command) == "A":
                    res = self.parser.parse_A_instruction(command)
                    f.write(self.code.A_instruction(res) + '\n')
                else:
                    res = self.parser.parse_C_instruction(command)
                    f.write(self.code.C_instruction(*res) + '\n')


def main():
    arguments = sys.argv
    if len(arguments) != 2:
        raise ValueError(r"Usage: >HackTranslator.py path_to_file\filename.asm")
    path_to_file = arguments[1]

    hack_assembler = HackTranslator(path_to_file)
    hack_assembler.assemble()


if __name__ == '__main__':
    main()
