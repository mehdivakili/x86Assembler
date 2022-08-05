from command import Command

from opcodes import is_label, get_label, convert_to_std_command


class Program:

    def __init__(self):
        self.commands = {}
        self.last_address = 0
        self.labels = {}

    def add_command(self, std_command_string):
        if is_label(std_command_string):
            l = get_label(std_command_string)
            self.labels[l] = self.last_address
            return
        std_command_string = convert_to_std_command(std_command_string)
        if std_command_string == "":
            return
        command = Command(std_command_string, self.last_address, self.labels)
        self.commands[self.last_address] = command
        self.last_address += command.get_size()

    def get_machine_code(self):
        machine_code = ""
        for command in self.commands.values():
            command.labels = self.labels
            command.label_analyze()
            command.jmp_analyze()
            machine_code += command.get_machine_code()

        return machine_code
