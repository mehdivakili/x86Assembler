from operand import Operand
from instruction import Instruction
from helper import *
from mr import MR


class Command:
    def __init__(self, std_command_string, address, labels=()):
        self.instruction = None
        self.operands = []
        self.address = address
        self.labels = labels
        self.std_command_string = std_command_string
        self.analyze_command()

    def analyze_command(self):
        self.ins_key = instruction = self.std_command_string.split(' ')[0]
        operands = ' '.join(self.std_command_string.split(' ')[1:]).split(' , ')

        for i in range(len(operands)):
            if not operands[i]:
                del operands[i]
        for operand in operands:
            self.operands.append(Operand(operand, self.labels))

        self.instruction = Instruction(instruction, self)
        self.mr = MR(self.operands, self)

    def jmp_analyze(self):
        if self.instruction.instruction_str != 'jmp':
            return
        ops = []
        for op in self.operands:
            if op.type == 'immediate' and not op.is_rel_set:
                o = Operand(str(op.int_value - self.address - self.get_size()), self.labels)
                op.is_rel_set = True
            else:
                o = op
            o.is_rel_set = op.is_rel_set
            ops.append(o)

        self.operands = ops
        self.instruction = Instruction('jmp', self)
        self.mr = MR(self.operands, self)

    def label_analyze(self):
        ops = []
        for op in self.operands:
            if op.type == 'immediate' and op.is_label:
                o = Operand(op.label_value, self.labels)
            else:
                o = op
            ops.append(o)

        self.operands = ops
        self.instruction = Instruction(self.ins_key, self)
        self.mr = MR(self.operands, self)

    def get_size(self):
        return len(self.get_bit_code()) // 8

    def get_machine_code(self):
        return convert_bit_to_machine_hex(self.get_bit_code())

    def get_bit_code(self):
        return self.instruction.get_bit_code() + self.mr.get_bit_code()
