import opcodes
from helper import *


class Operand:
    def __init__(self, operand_str, labels=()):
        self.operand_str = operand_str
        self.labels = labels
        self.label_value = None
        self.is_label = False
        self.is_rel_set = False
        self.analyze_operand()

    def analyze_operand(self):
        self.type = self.get_type()

        if self.type == 'register':
            self.register_analyze()
        elif self.type == 'immediate':
            self.immediate_analyze()
        elif self.type == 'memory':
            self.memory_analyze()

        elif self.type == 'label':
            self.label_analyze()
        else:
            raise Exception('operand not found')

    def register_analyze(self):
        data = opcodes.get_register_info(self.operand_str)
        self.opcode = data['code']
        self.size = data['size']

    def get_type(self):
        if opcodes.is_register(self.operand_str):
            return "register"
        if opcodes.is_immediate(self.operand_str):
            return "immediate"
        if opcodes.is_used_label(self.operand_str):
            return "label"
        return "memory"

    def get_sym_type(self):
        size = ''
        if self.size:
            size = str(self.size)
        return opcodes.symbolic_names[self.type] + size

    def get_reg_bit_code(self):
        return self.opcode

    def immediate_analyze(self):
        self.opcode = '000'
        self.operand_str = self.get_decimal_value()
        self.__int_value = int(self.operand_str)
        self.size = self.get_immediate_size()

    @property
    def int_value(self):
        return self.__int_value

    def get_immediate_size(self):
        i = 1
        while abs(self.int_value) >= 2 ** (i * 8 - 1):
            i *= 2
        return i * 8

    def get_decimal_value(self):
        if self.operand_str[-1] == 'b':
            return binary_to_decimal(self.operand_str[:-1])
        elif self.operand_str[-1] == 'h':
            return hex_to_decimal(self.operand_str[:-1])
        return self.operand_str

    def memory_analyze(self):
        reg = self.operand_str[1:-1]

        if reg in ['ax', 'cx', 'dx', 'sp']:
            raise Exception(f"[{reg}] is invalid addressing")

        self.opcode = opcodes.get_register_info(reg)['code']
        self.size = opcodes.get_register_info(reg)['size']
        if self.size == 16:
            if reg == 'bx':
                self.opcode = '111'
            if reg == 'bp':
                self.opcode = '11000000000'
            elif reg == 'di':
                self.opcode = '101'
            elif reg == 'si':
                self.opcode = '100'

    def label_analyze(self):
        self.type = 'immediate'
        self.is_label = True
        l = self.get_label_value(self.operand_str)
        if l:
            self.operand_str = l
            self.immediate_analyze()
        else:
            self.label_value = self.operand_str
            self.operand_str = '127'
            self.immediate_analyze()

    def get_label_value(self, operand_str):

        if not self.is_label:
            return False
        if operand_str in self.labels:
            self.is_label = False
            return str(self.labels[operand_str.lower()])
        else:
            return False
