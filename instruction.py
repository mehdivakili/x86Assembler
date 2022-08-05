import opcodes


class Instruction:
    def __init__(self, ins_str, command):
        self.instruction_str = ins_str
        self.command = command
        self.operands = command.operands
        self.complete_ins = tuple([self.instruction_str] + self.operands)
        self.analyze_instruction()

    def analyze_instruction(self):
        self.instruction_key = opcodes.get_mnemonic_key(self.complete_ins)
        self.info = opcodes.get_mnemonic_info(self.instruction_key)
        self.code = self.info['code']

    def get_prefix_code(self):
        return opcodes.get_prefix_code(self.complete_ins)

    def get_bit_code(self):
        return self.get_prefix_code() + self.code
