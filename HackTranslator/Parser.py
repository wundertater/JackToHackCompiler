from SymbolTable import SymbolTable


class Parser:
    A_Instruction = '@'
    L_Instruction = '('
    COMMENT = '//'

    def __init__(self):
        self.symbol_table = SymbolTable()
        self.variable_address = 16

    @staticmethod
    def cmd_type(line: str):
        if line.startswith(Parser.A_Instruction):
            return 'A'
        else:
            return 'C'

    def parse_fst_pass(self, line: str, index):
        line = line.strip()
        if line.startswith(Parser.COMMENT) or line.startswith(' '):
            return None
        elif line.startswith(Parser.L_Instruction):
            label_symbol = line[1:-1]
            self.symbol_table.update({label_symbol: index})
            return None
        else:
            return line

    def parse_A_instruction(self, line: str):
        value = line[1:]
        if not value.isdigit():
            if value not in self.symbol_table:
                self.symbol_table.update({value: self.variable_address})
                self.variable_address += 1

            value = self.symbol_table[value]
        return value

    @staticmethod
    def parse_C_instruction(line: str):
        line = line.replace(" ", "")
        dest, comp, jump = None, None, None

        if '=' in line:
            dest, line = line.split('=')
        if ';' in line:
            comp, jump = line.split(';')
        else:
            comp = line

        return dest, comp, jump
