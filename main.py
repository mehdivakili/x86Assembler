from program import Program


# if you want to get input from the file, uncomment the commented codes and comment "commend = input()" line

def main():
    program = Program()
    # f = open("tests/input1.txt", "r")
    # commands = f.readlines()
    # i = 0
    while True:
        try:
            command = input()
            # command = commands[i]
            # i += 1
        except Exception as e:
            print(program.get_machine_code())
            break

        if command.lower() == "end":
            print(program.get_machine_code())
            break
        if command:
            program.add_command(command)


if __name__ == '__main__':
    main()
