class Parser:
    ARITHMETIC = ('add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not')
    MEMORY_COMMANDS = ('pop', 'push')
    MEMORY_SEGMENTS = ('local', 'argument', 'this', 'constant', 'that', 'temp', 'static', 'pointer')
    BRANCHING_COMMANDS = ('label', 'goto', 'if-goto')
    FUNCTION_COMMANDS = ('return', 'function', 'call')

    @staticmethod
    def parse_line(line):
        """
        Parse a single line of VM code and classify it
        :param line: a string containing one line of VM code
        :return: a list where the first element is the command type and the second is the parsed command
        """
        # Strip out comments and unnecessary whitespaces
        line = line.split('//')[0].split()

        # Blank line or comment
        if len(line) == 0:
            return ['BLANK']

        # Arithmetic command (single-word command)
        elif len(line) == 1 and line[0] in Parser.ARITHMETIC:
            return ['ARITHMETIC', line[0]]

        # Branching command (two-word command)
        elif len(line) == 2 and line[0] in Parser.BRANCHING_COMMANDS:
            return ['BRANCHING', line]

        # Memory access command (pop/push, three-word command)
        elif len(line) == 3 and line[0] in Parser.MEMORY_COMMANDS and line[1] in Parser.MEMORY_SEGMENTS and \
                int(line[2]) >= 0:
            return ['MEMORY', line]

        # Function commands (return, single-word command; function/call, three-word command)
        elif (len(line) == 1 and line[0] in Parser.FUNCTION_COMMANDS) or (
                len(line) == 3 and line[0] in Parser.FUNCTION_COMMANDS and int(line[2]) >= 0):
            return ['FUNCTION', line]

        raise ValueError(f"Invalid command: {' '.join(line)}")
