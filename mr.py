from opcodes import symbolic_names, base_mode_reg_opcode, transforms
import re
from helper import imm_to_binary


class MR:
    # this class generate mode/reg/rm, sib, displacement and ... bytes

    def __init__(self, operands, command):
        self.operands = [i for i in operands]
        self.instruction_key = command.instruction.instruction_key

        self.remove_instruction_used_operands()
        self.set_memory_last()
        if len(operands) == 0:
            pass
        elif len(operands) == 1:
            self.one_analyze_operand()
        elif len(operands) == 2:
            self.two_analyze_operand()
        else:
            raise Exception("many operands")

    def get_bit_code(self):
        if len(self.operands) == 0:
            return ""
        if len(self.operands) == 1:
            return self.get_one_bit_operand_code()
        if len(self.operands) == 2:
            return self.get_two_bit_operand_code()

    def remove_instruction_used_operands(self):
        deleted_operands_number = 0
        for i in range(len(self.instruction_key[1:])):
            name = self.instruction_key[i + 1]
            is_sym = False
            for sym in symbolic_names.values():
                if name.startswith(sym):
                    is_sym = True
                    break
            if not is_sym:
                del self.operands[i - deleted_operands_number]
                deleted_operands_number += 1

    def one_analyze_operand(self):
        pass

    def two_analyze_operand(self):
        pass

    def get_one_operand_bit_mod(self):
        if self.operands[0].type == 'register':
            return '11'
        if self.operands[0].type == 'memory':
            return '00'
        raise Exception('not supported')

    def get_two_operand_bit_mod(self):
        if self.operands[0].type == 'register' and self.operands[1].type in ['register', 'immediate']:
            return '11'
        if self.operands[0].type == 'memory' or self.operands[1].type == 'memory':
            if re.search('\[e?bp\]', self.operands[0].operand_str):
                return '01'
            return '00'
        raise Exception('not supported')

    def get_one_bit_operand_code(self):
        if self.operands[0].type == 'immediate':
            return self.get_const_code()
        return self.get_one_operand_bit_mod() + self.get_one_operand_reg_code() + self.get_one_operand_rm_code() + self.get_disp_code()

    def get_two_bit_operand_code(self):
        return self.get_two_operand_bit_mod() + self.get_two_operand_reg_code() + self.get_two_operand_rm_code() + self.get_disp_code() + self.get_const_code()

    def get_two_operand_reg_code(self):
        if self.operands[1].type in ['register', 'memory']:
            return self.operands[1].get_reg_bit_code()
        elif self.operands[1].type == 'immediate':
            return base_mode_reg_opcode[self.instruction_key[0]]

        raise Exception('not supported')

    def get_two_operand_rm_code(self):
        if self.operands[0].type in ['register', 'memory']:
            return self.operands[0].get_reg_bit_code()
        raise Exception('not supported')

    def get_one_operand_rm_code(self):
        if self.operands[0].type in ['register', 'immediate']:
            return self.operands[0].get_reg_bit_code()
        raise Exception('not supported')

    def get_disp_code(self):
        return ""

    def get_const_code(self):
        size = None
        if self.instruction_key in transforms:
            tr = transforms[self.instruction_key]
            for i in range(len(tr)):
                if self.instruction_key[i] == tr[i]:
                    continue
                if tr[i].startswith('imm'):
                    size = int(tr[i][3:])

        for op in self.operands:
            if op.type == 'immediate':
                if size:
                    s = imm_to_binary(op.int_value, size)
                    return s
                s = imm_to_binary(op.int_value, op.size)
                return s
        return ""

    def get_one_operand_reg_code(self):
        return base_mode_reg_opcode[self.instruction_key[0]]

    def set_memory_last(self):
        if len(self.operands) == 2 and self.operands[-1].type == 'memory':
            self.operands.reverse()
