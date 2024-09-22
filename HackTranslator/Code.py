class Code:
    DEST_VALUES = [None, 'M', 'D', 'MD', 'A', 'AM', 'AD', 'AMD']
    COMP_CODES = {'0': '0101010', '1': '0111111', '-1': '0111010', 'D': '0001100', 'A': '0110000', '!D': '0001101',
                  '!A': '0110001', '-D': '0001111', '-A': '0110011', 'D+1': '0011111', 'A+1': '0110111',
                  'D-1': '0001110', 'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011', 'A-D': '0000111',
                  'D&A': '0000000', 'D|A': '0010101', 'M': '1110000', '!M': '1110001', '-M': '1110011',
                  'M+1': '1110111', 'M-1': '1110010', 'D+M': '1000010', 'D-M': '1010011', 'M-D': '1000111',
                  'D&M': '1000000', 'D|M': '1010101'}
    JUMP_VALUES = [None, 'JGT', 'JEQ', 'JGE', 'JLT', 'JNE', 'JLE', 'JMP']

    @staticmethod
    def binary(value):
        return bin(int(value))[2:]

    def A_instruction(self, value: str):
        return '0' + self.binary(value).zfill(15)

    def C_instruction(self, dest, comp, jump):
        dest = self.binary(self.DEST_VALUES.index(dest)).zfill(3)
        comp = self.COMP_CODES[comp]
        jump = self.binary(self.JUMP_VALUES.index(jump)).zfill(3)
        return '111' + comp + dest + jump
