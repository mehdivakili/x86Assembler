import os


def read_command(command):
    stream = os.popen(command)
    out = stream.read().strip()
    stream.close()
    return out


i = 1
while os.path.exists(f'tests\\input{i}.txt'):

    t = open(f'tests\\output{i}.txt', 'r').read().strip()
    s = read_command(f'python main.py < tests\\input{i}.txt')
    if s == t:
        print(f"TEST {i} PASSED")
    else:
        raise Exception(f"TEST {i} FAILED\ntrue:   {t}\noutput: {s}")
    i += 1
