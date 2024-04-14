from typing import Callable, Union
import os


_version = "1.0.0"
_command_interpreters_count = 1  # DON'T TOUCH THIS VARIABLE


class EZCommandLineErrors:
    class DecryptionError(Exception):
        def __init__(self, message="The given file is corrupted or not readable: "):
            super().__init__(message)


def _check_arguments_dict(arguments: dict[str: type]) -> str:
    """ Returns "ok" if the given dict is a valid argument dict, else returns the error """
    for argument_name in arguments:
        if argument_name:
            # name checking
            if argument_name == "" or " " in argument_name or '"' in argument_name:
                return f"argument '{argument_name}': not valid name"

        # type checking
        if arguments[argument_name] is not str and arguments[argument_name] is not int and arguments[argument_name] is not float and arguments[argument_name] is not None:
            return f"argument '{argument_name}': not valid type"

    return "ok"


def _get_str_of_type(value: Union[type, None]) -> str:
    """ Returns the given type transformed in str (only works for str, int, float and None) """
    if value is str:
        return "str"
    elif value is int:
        return "int"
    elif value is float:
        return "float"
    elif value is None:
        return "none"
    else:
        raise ValueError(f"The given type value is incorrect: {value}")


def _get_type_of_str(text: str) -> Union[type, None]:
    """ Returns the given type transformed stored in the given text (only works for str, int, float and None) """
    if text == "str":
        return str
    elif text == "int":
        return int
    elif text == "float":
        return float
    elif text == "none":
        return None
    else:
        raise ValueError(f"The given text is incorrect: {text}")


class CommandLineInterpreter:
    def __init__(self, error_func: Callable = None):
        """Class used to create command line interpreter. This interpreter cannot be modified but uses less memory

        :param error_func: optional: function to call when a command entered using self.interpret(command) raises a syntax error. This function should accept 2 arguments: the error name (str) and the cause of the error (str).
        """
        global _command_interpreters_count

        if error_func is not None and not callable(error_func):
            raise TypeError(f"The given object for error_func is not callable: {error_func}")

        self.__object_number = _command_interpreters_count
        _command_interpreters_count += 1

        self.commands = {}

        self.__error_func = error_func

    def __str__(self):
        return f"CommandLineInterpreter object n°{self.__object_number}"

    def __call_error(self, error_name: str, error_cause: str):
        if self.__error_func is not None:
            self.__error_func(error_name, error_cause)

    def get_object_number(self) -> int:
        """Returns the number of this instance

        :return: number of the CommandLineInterpreter instance
        """
        return self.__object_number

    def get_error_func(self) -> Union[Callable, None]:
        """Returns the error func assigned to this interpreter

        :return: error_func of the interpreter
        """
        return self.__error_func

    def configure(self, **kwargs):
        """Configures the given arguments

        :param kwargs: same arguments as the __init__ method
        """
        if "error_func" in kwargs:
            value = kwargs.pop("error_func")
            if callable(value):
                self.__error_func = value
            else:
                raise TypeError(f"The given object for error_func is not callable: {value}")

        if kwargs:  # not empty
            raise ValueError(f"The given arguments aren't valid: {", ".join(kwargs.keys())}")

    def interpret(self, command: str):
        """Interprets the given command

        :param command: command string to interpret
        """
        # analysing command syntax (splitting arguments)
        split_command = []
        word = ""
        in_quotation_marks = False
        for char in command:
            if char == " ":
                if in_quotation_marks:
                    word += " "
                else:
                    split_command.append(word)
                    word = ""
            elif char == '"':
                if in_quotation_marks:
                    in_quotation_marks = False
                else:
                    in_quotation_marks = True
            else:
                word += char
        if word:
            split_command.append(word)

        if split_command:  # command not empty
            if split_command[0] in self.commands:  # known command
                called_arguments = {}
                if self.commands[split_command[0]][1][""] is not None:  # base argument needed
                    command_start_length = 2
                    if len(split_command) >= 2:
                        try:
                            value = self.commands[split_command[0]][1][""](split_command[1])
                        except ValueError:
                            self.__call_error("not respected type", split_command[1])
                            return
                        else:
                            called_arguments[""] = value
                    else:
                        self.__call_error("no base argument entered", "")
                        return
                else:
                    command_start_length = 1
                current_argument = ""
                for x in range(command_start_length, len(split_command)):
                    if not current_argument:  # current_argument == ""
                        if split_command[x] in self.commands[split_command[0]][1]:  # known argument
                            if split_command[x] not in called_arguments:
                                if self.commands[split_command[0]][1][split_command[x]] is None:  # argument does not accept a value
                                    called_arguments[split_command[x]] = None
                                else:  # argument needs a value
                                    current_argument = split_command[x]
                            else:  # same argument entered 2 times
                                self.__call_error("repeated argument", split_command[x])
                                return
                        else:  # unknown argument
                            self.__call_error("unknown argument", split_command[x])
                            return
                    else:  # current argument != ""
                        if self.commands[split_command[0]][1][current_argument] is str:
                            called_arguments[current_argument] = split_command[x]
                            current_argument = ""
                        elif self.commands[split_command[0]][1][current_argument] is int:
                            try:
                                value = int(split_command[x])
                            except ValueError:
                                self.__call_error("not respected type", split_command[x])
                                return
                            else:
                                called_arguments[current_argument] = value
                                current_argument = ""
                        elif self.commands[split_command[0]][1][current_argument] is float:
                            try:
                                value = float(split_command[x])
                            except ValueError:
                                self.__call_error("not respected type", split_command[x])
                                return
                            else:
                                called_arguments[current_argument] = value
                                current_argument = ""
                if current_argument:  # last argument not closed
                    self.__call_error("last argument's value not entered", current_argument)
                    return

                self.commands[split_command[0]][0](called_arguments)  # calls the callback_func
            else:  # unknown command
                self.__call_error("unknown command", split_command[0])
                return


class ModifiableCommandLineInterpreter(CommandLineInterpreter):
    """Class used to create command line interpreter. This interpreter can be modified but uses more memory"""
    def get_command(self, name: str) -> tuple[Callable, dict[str: type]]:
        """Returns the given command info

        :param name: name of the command
        :return: command info: (callback_func, arguments_dict)
        """
        if name in self.commands:
            return self.commands[name]
        else:
            raise KeyError(f"The given command name does not exist: {name}")

    def add_command(self, name: str, callback_func: Callable, base_argument: type = None, arguments: dict[str: type] = None) -> bool:
        """Adds a command to the interpreter

        :param name: name of the command to add, if the name is already in use, overwrites the old command
        :param callback_func: function called when the command is interpreted, this function should accept 1 argument: the dict containing the arguments given to the command.
        :param base_argument: basic argument of the command (which doesn't need an argument name before the value). Should be: str, int or float.
        :param arguments: arguments of the command, their type and their optionality follow the given syntax:
            {"argument_name": type_of_the_argument, "second_argument": type}.
            The argument name should not contain spaces or quotation marks, the type of the argument should be int, str, float or None.
        :return: True if an old command was overwritten, else returns False
        """
        if isinstance(name, str):
            if name:  # not ""
                if callable(callback_func):
                    if base_argument is None or base_argument is str or base_argument is int or base_argument is float:
                        if arguments is None:
                            arguments = {}
                            checking = "ok"
                        else:
                            checking = _check_arguments_dict(arguments)
                        if checking == "ok":
                            if name in self.commands:
                                self.commands[name] = (callback_func, {"": base_argument} | arguments)
                                return True
                            else:
                                self.commands[name] = (callback_func, {"": base_argument} | arguments)
                                return False
                        else:
                            raise ValueError(f"Arguments dict isn't valid: {checking}")
                    else:
                        raise ValueError(f"The given base argument type is not valid: {base_argument}")
                else:
                    raise TypeError(f"The given object for callback_func is not callable: {callback_func}")
            else:
                raise ValueError("The given name is not valid: the name is empty")
        else:
            raise TypeError(f"The given name is not an str: {type(name)}")

    def remove_command(self, name: str):
        """Removes a command from the interpreter

        :param name: name of the command to remove
        """
        if name in self.commands:
            del self.commands[name]
        else:
            raise KeyError(f"The given command name does not exist: {name}")


def _encode_str(string: str) -> str:
    """Encodes the given string by replacing the characters used to store the interpreter

    :param string: string to encode
    :return: encoded string
    """
    return string.replace("#", "\\1").replace("\\", "\\\\")


def _decode_str(string: str) -> str:
    """Decodes the given string by replacing the characters used to store the interpreter

    :param string: string to decode
    :return: decoded string
    """
    return string.replace("\\1", "#").replace("\\\\", "\\")


def _encode_interpreter(interpreter: Union[CommandLineInterpreter, ModifiableCommandLineInterpreter]) -> str:
    """Encodes the given interpreter into text

    :param interpreter: interpreter to encode
    :return: interpreter encoded in text form
    """
    if isinstance(interpreter, (CommandLineInterpreter, ModifiableCommandLineInterpreter)):
        text = ""
        for command in interpreter.commands:
            text = text + "#COMMAND\n"
            text = text + f"#NAME {_encode_str(command)}\n"
            arguments = interpreter.commands[command][1].copy()
            if "" in arguments:  # base argument
                value = arguments.pop("")
                text = text + f"#BASEARGUMENT {_get_str_of_type(value)}\n"
            for argument in arguments:
                text = text + f"#ARGUMENT {argument} {_get_str_of_type(arguments[argument])}\n"
            text = text + "#COMMANDEND\n\n"
        return text
    else:
        raise TypeError(f"The given interpreter is not an interpreter: {type(interpreter)}")


def _decode_interpreter(text: str, funcs_dict: dict[str: Callable]) -> CommandLineInterpreter:
    """Decodes the given text into interpreter

    :param text: text to decode
    :param funcs_dict: dict containing the callback functions for the commands stored in the given .EZCI file
    :return: decoded interpreter in the text
    """
    if type(text) is str:
        interpreter = ModifiableCommandLineInterpreter()

        in_command = False
        command_name = None
        base_argument = None
        command_arguments = {}
        for line in text.split("\n"):
            if line == "":
                pass
            elif line.startswith("##"):
                pass
            elif line == "#COMMAND":
                if not in_command:
                    in_command = True
                else:
                    raise EZCommandLineErrors.DecryptionError("Corrupted line: started a new #COMMAND without closing the previous one")
            elif line.startswith("#NAME"):
                if in_command:
                    command_name = line.removeprefix("#NAME ")
                else:
                    raise EZCommandLineErrors.DecryptionError("Corrupted line: #NAME outside of #COMMAND")
            elif line.startswith("#BASEARGUMENT"):
                if in_command:
                    base_argument = _get_type_of_str(line.removeprefix("#BASEARGUMENT "))
                else:
                    raise EZCommandLineErrors.DecryptionError("Corrupted line: #BASEARGUMENT outside of #COMMAND")
            elif line.startswith("#ARGUMENT"):
                if in_command:
                    if len(line.split(" ")) == 3:
                        command_arguments[line.split(" ")[1]] = _get_type_of_str(line.split(" ")[2])
                    else:
                        raise EZCommandLineErrors.DecryptionError(f"Corrupted line: {line}")
                else:
                    raise EZCommandLineErrors.DecryptionError("Corrupted line: #ARGUMENT outside of #COMMAND")
            elif line == "#COMMANDEND":
                if in_command:
                    if command_name is not None:
                        if command_name in funcs_dict:
                            interpreter.add_command(command_name, funcs_dict[command_name], base_argument, command_arguments)
                            in_command = False
                            command_name = None
                            base_argument = None
                            command_arguments = {}
                        else:
                            raise ValueError(f"The funcs_dict is missing the callback function for: {command_name}")
                    else:
                        raise EZCommandLineErrors.DecryptionError("Missing a #NAME tag in #COMMAND")
                else:
                    raise EZCommandLineErrors.DecryptionError("Corrupted line: #COMMANDEND without starting starting #COMMAND")
            else:
                raise EZCommandLineErrors.DecryptionError(f"Corrupted line: {line}")

        if in_command:  # last command not closed (with #COMMANDEND)
            raise EZCommandLineErrors.DecryptionError("The last command was never closed with a #COMMANDEND tag")

        return non_mutable_interpreter(interpreter)
    else:
        raise TypeError(f"The given text is not str type: {type(text)}")


def export_interpreter(interpreter: Union[CommandLineInterpreter, ModifiableCommandLineInterpreter], path: str):
    """Exports the given interpreter in the given file path

    :param interpreter: interpreter to export
    :param path: path of the file to export to, overwrites the file already existing if there is one. The path should be a .EZCI but can be any type of text file
    """
    if os.path.isdir(path):
        raise ValueError("The given path is a directory, it should be a file")
    elif not os.path.isdir(os.path.dirname(path)):
        raise ValueError("The given path does not exist")
    elif not isinstance(interpreter, (CommandLineInterpreter, ModifiableCommandLineInterpreter)):
        raise ValueError(f"The given interpreter is not an interpreter: {type(interpreter)}")
    else:  # valid path
        text = _encode_interpreter(interpreter)
        with open(path, "w") as f:
            f.write(text)


def import_interpreter(path: str, funcs_dict: dict[str: Callable]) -> CommandLineInterpreter:
    """Imports the interpreter in the given file

    :param path: path of the file to read
    :param funcs_dict: dict containing the callback functions for the commands stored in the given .EZCI file. Ex: {"command_name": callback_func}
    :return: CommandLineInterpreter instance contained in the given file
    """
    if os.path.isfile(path):
        with open(path, "r") as f:
            interpreter = _decode_interpreter(f.read(), funcs_dict)
        return interpreter
    else:
        raise ValueError("The given file path does not exist")


def mutable_interpreter(interpreter: CommandLineInterpreter) -> ModifiableCommandLineInterpreter:
    """Converts a non-mutable interpreter to a mutable interpreter

    :param interpreter: non-mutable interpreter to convert to a mutable one
    :return: mutable interpreter
    """
    if isinstance(interpreter, CommandLineInterpreter):
        new_interpreter = ModifiableCommandLineInterpreter(interpreter.get_error_func())
        new_interpreter.commands = interpreter.commands
        return new_interpreter
    else:
        raise TypeError(f"The given interpreter is not a non-mutable interpreter: {type(interpreter)}")


def non_mutable_interpreter(interpreter: ModifiableCommandLineInterpreter) -> CommandLineInterpreter:
    """Converts a mutable interpreter to a non-mutable interpreter

    :param interpreter: mutable interpreter to convert to a non-mutable one
    :return: non-mutable interpreter
    """
    if isinstance(interpreter, ModifiableCommandLineInterpreter):
        new_interpreter = CommandLineInterpreter(interpreter.get_error_func())
        new_interpreter.commands = interpreter.commands
        return new_interpreter
    else:
        raise TypeError(f"The given interpreter is not a mutable interpreter: {type(interpreter)}")
