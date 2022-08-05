def convert_bit_to_machine_hex(bit_str):
    out = ""
    for i in range(len(bit_str) // 8):
        out += '\\x' + str(hex(int(bit_str[i * 8:i * 8 + 4], 2)))[2:] + str(hex(int(bit_str[i * 8 + 4:i * 8 + 8], 2)))[
                                                                        2:]

    return out


def binary_to_decimal(bit_str):
    return str(int(bit_str, 2))


def hex_to_decimal(bit_str):
    return str(int(bit_str, 16))


def decimal_to_binary(int_value):
    return str(bin(int_value))[2:]


def real_decimal_to_binary(n, bits):
    s = bin(n & int("1" * bits, 2))[2:]
    return ("{0:0>%s}" % (bits)).format(s)


def binary_to_little_indian(bits: str):
    bits = bits[::-1]
    out = ""
    for i in range(len(bits) // 8):
        out += bits[i * 8:(i + 1) * 8][::-1]

    return out


def imm_to_binary(n, bits):
    return binary_to_little_indian(real_decimal_to_binary(n, bits))
