"""
Project 7,8
From Nand to Tetris course https://www.nand2tetris.org/
Translate VM code to Hack assembly, creates a .asm file
Usage: >VMTranslator.py filename.vm OR >VMTranslator.py folderName
Use no-desc flag to avoid recording comments (>VMTranslator.py file no-desc)
"""
import sys
import os
from Parser import Parser
from CodeWriter import CodeWriter


class VMTranslator:

    def __init__(self, input_, write_desc):
        self.write_desc = write_desc
        self.input_ = input_
        path, file = os.path.split(input_)
        self.path = os.path.join(path, '') if path else ''
        filename, _ = os.path.splitext(file)
        self.outp_file = os.path.join(self.path, filename + '.asm')
        self.parser = Parser()

        # Data needed for CodeWriter
        self.comp_label_num = 0
        self.func_label_num = 0
        self.bootstrap_flag = True  # Controls when bootstrap code is written

    def process_single_file(self, inpfile, outpfile):
        """
        Write to outpfile translated code from inpfile
        :param inpfile: file opened in read mode
        :param outpfile: file opened in append mode
        """
        print(f"Processing file: {inpfile.name}")

        codewriter = CodeWriter(outpfile, self, filename=os.path.basename(inpfile.name)[:-3])
        if self.bootstrap_flag:
            codewriter.bootstrap()
            self.bootstrap_flag = False

        for line in inpfile:
            parsed_line = self.parser.parse_line(line)
            cmd_type = parsed_line[0]
            if cmd_type == 'ARITHMETIC':
                codewriter.WriteArithmetic(parsed_line[1])
            elif cmd_type == 'MEMORY':
                codewriter.WritePushPop(*parsed_line[1])
            elif cmd_type == 'BRANCHING':
                codewriter.WriteBranching(*parsed_line[1])
            elif cmd_type == 'FUNCTION':
                codewriter.WriteFunction(*parsed_line[1])

    def start(self):
        with open(self.outp_file, 'a') as outpfile:
            # if input is a folder
            if os.path.isdir(self.input_):
                for inpfile in os.listdir(self.input_):
                    if inpfile.endswith(".vm"):
                        path = os.path.join(self.outp_file[:-4], '')
                        with open(path + inpfile, 'r') as inpfile:
                            self.process_single_file(inpfile, outpfile)
            # if input is a single file
            else:
                with open(self.input_, 'r') as inpfile:
                    self.process_single_file(inpfile, outpfile)


def main():
    arguments = sys.argv
    if len(arguments) < 2:
        raise ValueError("Usage: >VMTranslator.py filename.vm OR >VMTranslator.py folderName")
    input_ = arguments[1]
    write_desc = True
    if len(arguments) == 3:
        if arguments[2] == 'no-desc':
            write_desc = False

    vm_translator = VMTranslator(input_, write_desc)
    print("Start translating...")
    vm_translator.start()
    print("Translation was completed successfully.")


if __name__ == '__main__':
    main()
