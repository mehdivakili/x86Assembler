import re

registers = {
    'al': {'code': '000', 'size': 8},
    'bl': {'code': '011', 'size': 8},
    'cl': {'code': '001', 'size': 8},
    'dl': {'code': '010', 'size': 8},
    'ax': {'code': '000', 'size': 16},
    'bx': {'code': '011', 'size': 16},
    'cx': {'code': '001', 'size': 16},
    'dx': {'code': '010', 'size': 16},
    'eax': {'code': '000', 'size': 32},
    'ebx': {'code': '011', 'size': 32},
    'ecx': {'code': '001', 'size': 32},
    'edx': {'code': '010', 'size': 32},
    'ah': {'code': '100', 'size': 8},
    'bh': {'code': '111', 'size': 8},
    'ch': {'code': '101', 'size': 8},
    'dh': {'code': '110', 'size': 8},
    'sp': {'code': '100', 'size': 16},
    'di': {'code': '111', 'size': 16},
    'bp': {'code': '101', 'size': 16},
    'si': {'code': '110', 'size': 16},
    'esp': {'code': '100', 'size': 32},
    'edi': {'code': '111', 'size': 32},
    'ebp': {'code': '101', 'size': 32},
    'esi': {'code': '110', 'size': 32},

}

base_mnemonic_opcode = {
    'add': '000',
    'sub': '101',
    'and': '100',
    'or': '001',
}

base_mode_reg_opcode = {
    'inc': '000',
    'dec': '001',
}

transform_bases = {
    ('reg32', 'imm16'): ('reg32', 'imm32')

}

mnemonic_opcode_reg_mem_gen = {
    ('reg8', 'reg8'): {'before_code': '00', 'after_code': '000'},
    ('mem8', 'reg8'): {'before_code': '00', 'after_code': '000'},
    ('mem16', 'reg8'): {'before_code': '00', 'after_code': '000'},
    ('mem32', 'reg8'): {'before_code': '00', 'after_code': '000'},
    ('reg8', 'mem8'): {'before_code': '00', 'after_code': '010'},
    ('reg8', 'mem16'): {'before_code': '00', 'after_code': '010'},
    ('reg8', 'mem32'): {'before_code': '00', 'after_code': '010'},
    ('reg16', 'reg16'): {'before_code': '00', 'after_code': '001'},
    ('mem8', 'reg16'): {'before_code': '00', 'after_code': '001'},
    ('mem16', 'reg16'): {'before_code': '00', 'after_code': '001'},
    ('mem32', 'reg16'): {'before_code': '00', 'after_code': '001'},
    ('reg16', 'mem8'): {'before_code': '00', 'after_code': '011'},
    ('reg16', 'mem16'): {'before_code': '00', 'after_code': '011'},
    ('reg16', 'mem32'): {'before_code': '00', 'after_code': '011'},
    ('reg32', 'reg32'): {'before_code': '00', 'after_code': '001'},
    ('mem8', 'reg32'): {'before_code': '00', 'after_code': '001'},
    ('mem16', 'reg32'): {'before_code': '00', 'after_code': '001'},
    ('mem32', 'reg32'): {'before_code': '00', 'after_code': '001'},
    ('reg32', 'mem8'): {'before_code': '00', 'after_code': '011'},
    ('reg32', 'mem16'): {'before_code': '00', 'after_code': '011'},
    ('reg32', 'mem32'): {'before_code': '00', 'after_code': '011'},
    ('al', 'imm8'): {'before_code': '00', 'after_code': '100'},
    ('ax', 'imm16'): {'before_code': '00', 'after_code': '101'},
    ('eax', 'imm32'): {'before_code': '00', 'after_code': '101'},

}

mnemonic_opcode_imm_gen = {
    ('reg8', 'imm8'): "10000000",
    ('reg16', 'imm16'): '10000001',
    ('reg32', 'imm32'): '10000001',
    ('reg32', 'imm16'): '10000001',
    ('reg16', 'imm8'): '10000011',
    ('reg32', 'imm8'): '10000011',
}

transforms = {
    ('jmp', 'imm16'): ('jmp', 'imm32')
}

transforms.update({((base_code,) + oper_code): ((base_code,) + after_code)
                   for (base_code, b_v) in base_mnemonic_opcode.items()
                   for (oper_code, after_code) in transform_bases.items()})

mnemonics = {((base_code,) + oper_code): {'code': o_v['before_code'] + b_v + o_v['after_code']}
             for (base_code, b_v) in base_mnemonic_opcode.items()
             for (oper_code, o_v) in mnemonic_opcode_reg_mem_gen.items()}

mnemonics.update({((base_code,) + oper_code): {'code': o_v}
                  for (base_code, b_v) in base_mnemonic_opcode.items()
                  for (oper_code, o_v) in mnemonic_opcode_imm_gen.items()})

mnemonics.update({(base_name, reg_name): {'code': '01' + base_code + reg_code['code']}
                  for (base_name, base_code) in base_mode_reg_opcode.items()
                  for (reg_name, reg_code) in registers.items() if reg_code['size'] != 8})

mnemonics.update({
    ('inc', 'reg8'): {'code': '11111110'},
    ('dec', 'reg8'): {'code': '11111110'},
    ('stc',): {'code': '11111001'},
    ('std',): {'code': '11111101'},
    ('jmp', 'imm8'): {'code': '11101011'},
    ('jmp', 'imm16'): {'code': '11101001'},
    ('jmp', 'imm32'): {'code': '11101001'},
    ('jmp', 'reg32'): {'code': '11111111'},
    ('jmp', 'reg16'): {'code': '11111111'},
    ('jmp', 'mem16'): {'code': '11111111'},
    ('jmp', 'mem32'): {'code': '11111111'},
})

base_mode_reg_opcode.update(base_mnemonic_opcode)
base_mode_reg_opcode.update({
    'jmp': '100'
})

prefixes = {
    'reg16': {'code': '01100110'},
    'mem16': {'code': '01100111'}
}

symbolic_names = {
    'register': 'reg',
    'memory': 'mem',
    'immediate': 'imm'
}


def is_register(s):
    if s in registers:
        return True
    return False


def get_register_info(register):
    if is_register(register):
        return registers[register]
    raise Exception("register not found")


def is_mnemonics_exist(mnemonic):
    if mnemonic in mnemonics:
        return True
    return False


def get_mnemonic_info(mnemonic):
    if is_mnemonics_exist(mnemonic):
        return mnemonics[mnemonic]
    raise Exception("mnemonic not found")


def get_prefix_code(mnemonic):
    out = ""
    for op in mnemonic[1:]:
        if op.get_sym_type() == 'mem16':
            out += prefixes['mem16']['code']
            break

    for op in mnemonic[1:]:
        if op.get_sym_type() == 'reg16':
            out += prefixes['reg16']['code']
            break

    return out


def get_mnemonic_key(complete_ins):
    mnemonic_name = complete_ins[0]
    operands = complete_ins[1:]
    if operands:
        for i in range(2 ** len(operands)):
            operands_key = []
            n = f'{{:0{len(operands)}b}}'.format(i)

            for c in range(len(n)):
                if n[c] == '0':
                    operands_key += [operands[c].operand_str]
                else:
                    operands_key += [operands[c].get_sym_type()]
            if is_mnemonics_exist(tuple([mnemonic_name] + operands_key)):
                return tuple([mnemonic_name] + operands_key)
    else:
        if is_mnemonics_exist(tuple([mnemonic_name])):
            return tuple([mnemonic_name])

    raise Exception("mnemonic not found")


def is_immediate(operand_str):
    try:
        int(operand_str)
        return True
    except:
        pass
    if operand_str[-1] == 'b':
        for c in operand_str[:-1]:
            if c not in ['0', '1']:
                return False
        return True
    if operand_str[-1] == 'h':
        for c in operand_str[:-1]:
            if c not in '0123456789abcdef':
                return False
        return True

    return False


def is_label(text):
    text = remove_comments(text)
    if re.search("^[\w\d]+\s*:$", text):
        return True
    return False


def is_used_label(operand_str):
    if re.search("^[\w\d]+$", operand_str):
        return True
    return False


def remove_comments(command):
    return command.split(';')[0].strip()


def convert_to_std_command(command):
    command = remove_comments(command)
    std_command = command.replace(',', ' , ')

    for i in re.findall("\[.+\]", std_command):
        std_command = std_command.replace(i, ''.join(i.split()))

    return ' '.join(std_command.lower().split())


def get_label(text: str):
    text = remove_comments(text).lower().strip()
    return text.split(':')[0].strip().lower()

