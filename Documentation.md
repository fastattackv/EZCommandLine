# Documentation for EZCommandLine
By Fastattack, 2024 for version 1.0.0

Summary:
- [Global information about the EZCommandLine](Documentation.md#global-information-about-the-ezcommandline)
- [CommandLineInterpreter](Documentation.md#commandlineinterpreter)
  - [Global information about the CommandLineInterpreter class](Documentation.md#global-information-about-the-commandlineinterpreter-class)
  - [Create an interpreter](Documentation.md#create-an-interpreter)
  - [Use an interpreter](Documentation.md#use-an-interpreter)
  - [Export / import interpreters](Documentation.md#export--import-interpreters)
  - [Documentation for all functions and methods](Documentation.md#documentation-for-all-functions-and-methods)
    - [Public functions and classes](Documentation.md#public-functions-and-classes)
      - [CommandLineInterpreter()](Documentation.md#commandlineinterpreter-1)
      - [ModifiableCommandLineInterpreter()](Documentation.md#modifiablecommandlineinterpreter)
      - [export_interpreter()](Documentation.md#export_interpreter)
      - [import_interpreter()](Documentation.md#import_interpreter)
      - [mutable_interpreter() and non_mutable_interpreter()](Documentation.md#mutable_interpreter-and-non_mutable_interpreter)
    - [Hidden functions](Documentation.md#hidden-functions)
      - [_check_arguments_dict()](Documentation.md#_check_arguments_dict)
      - [_get_str_of_type()](Documentation.md#_get_str_of_type)
      - [_get_type_of_str()](Documentation.md#_get_type_of_str)
      - [_encode_str() and _decode_str()](Documentation.md#_encode_str-and-_decode_str)
      - [_encode_interpreter()](Documentation.md#_encode_interpreter)
      - [_decode_interpreter()](Documentation.md#_decode_interpreter)
- [EZCommandLineErrors](Documentation.md#ezcommandlineerrors)
  - [DecryptionError](Documentation.md#decryptionerror)
- [Interpreter encoding](Documentation.md#interpreter-encoding)
  - [Global information for the encoding](Documentation.md#global-information-for-the-encoding)
  - [Encoding functioning](Documentation.md#encoding-functioning)
  - [Encoding example](Documentation.md#encoding-example)
- [Examples](Documentation.md#examples)
  - [Example to create an interpreter](Documentation.md#example-to-create-an-interpreter)
  - [Example to use an interpreter](Documentation.md#example-to-use-an-interpreter)
  - [Example to export / import an interpreter](Documentation.md#example-to-export--import-an-interpreter)
  - [Encoding example](Documentation.md#encoding-example-1)

## Global information about the EZCommandLine
The functions without an underscore ('\_') at the start of their name check the arguments you give them whilst the functions (or methods) that have a name starting with an underscore ('\_') are internal functions and do not check any values: you should not use them unless you are forced to.

Normally, files containing an interpreter have the extension `.EZCI` (for EZCommandInterpreter) but any type of text file can be used.

---

## CommandLineInterpreter

### Global information about the CommandLineInterpreter class

This class allows to create a command line-like interpreter. This class does not create a command line, just the interpreter.

There are 2 types of interpreters in the EZCommandLine module:
- `CommandLineInterpreter`: a non-mutable interpreter, perfect to interpret commands but not modifiable
- `ModifiableCommandLineInterpreter`: a mutable interpreter, perfect to create interpreters but uses more memory so is less efficient to interpret commands.

You can transform a non-mutable interpreter into a mutable interpreter and vice-versa using the `mutable_interpreter()` and `non_mutable_interpreter()` functions.

### Create an interpreter

To create an interpreter, you can: write a .EZCI file yourself using the documentation about the interpreter encoding (see here: [Documentation](Documentation.md#interpreter-encoding)), or create an interpreter directly in python using the `ModifiableCommandLineInterpreter` class and the`add_command()` method.

See here for examples: [Documentation](Documentation.md#example-to-create-an-interpreter)

### Use an interpreter

Using an interpreter is easy: you just input the command to the interpreter using `CommandLineInterpreter.interpret(command)`.

This method will call the callback function assigned to the given command or call the error_func given to the interpreter if a syntax error is raised.

See here for examples: [Documentation](Documentation.md#example-to-use-an-interpreter)

### Export / import interpreters

To export an interpreter you created, just use the `export_interpreter()` function and give it the interpreter you want to export and the file path to export to.

To import an interpreter, just use the `import_interpreter()` function and give it the path of the file to import, and it will return you the interpreter stored in the given file.

See here for examples: [Documentation](Documentation.md#example-to-export--import-an-interpreter)

### Documentation for all functions and methods

#### Public functions and classes

##### CommandLineInterpreter()

The `CommandLineInterpreter()` class is used to make a command line interpreter that can interpret text commands and call the functions assigned to this command.

Entries:
- `error_func`: Optional: a function that the interpreter calls when a syntax error is raised during the interpretation of the command.

Methods:
- `get_object_number()`: Returns the number assigned to the interpreter, each interpreter is assigned a different number, so they can be differentiated.
- `get_error_func()`: Returns the error_func assigned to the interpreter. If no error_func were assigned to the interpreter: returns None
- `configure()`: Configures the given arguments of the CommandLineInterpreter. Accepted arguments: `error_func`
- `interpret()`: Interprets the given command and calls the function assigned to the command. Entries: `command`: the command to interpret.

##### ModifiableCommandLineInterpreter()

The `ModifiableCommandLineInterpreter()` class is used to create a command line interpreter but uses more memory.

It has the same entries and methods as the `CommandLineInterpreter()` class.

Methods:
- `get_command()`: Returns the given command infos (callback_func and arguments_dict). Entry: `name`: name of the command to obtain the infos from
- `add_command()`: 
  - Adds a command to the interpreter. 
  - Entries: 
    - `name`: name of the command to add
    - `callback_func`: function to call when the command is executed (the func has to accept a dict containing the arguments entered by the user, if a base argument is specified: its key in the dictionary will be ""). 
    - `base_argument`: the type of the base argument (can be either `str`, `int`, `float` or `None`) (if None is given, there will be no base argument).
    - `arguments`: dictionary containing the arguments of the command (following this syntax: `{"argument_name": type_of_the_argument, "second_argument": type}`). If None is given, the command will not accept any arguments.
  - Output:
    - If the command's name is already in use, the previous command will be overwritten and the method will return True. If the name isn't already in use, the method will return False. 
- `remove_command()`: Removes the given command from the interpreter. Entry: `name`: name of the command to remove

##### export_interpreter()

This function will export the given interpreter at the specified filepath.

Entries:
- `interpreter`: interpreter (either mutable or not) to export
- `path`: file path to export the interpreter to (not a directory)

##### import_interpreter()

This function will import the interpreter stored in the specified filepath.

Entries:
- `path`: path of the file containing the interpreter to import
- `funcs_dict`: dictionary containing the callback functions for the commands stored in the given file. Ex: `{"command_name": callback_func}`

Output:
- Non-mutable interpreter stored in the given filepath.

##### mutable_interpreter() and non_mutable_interpreter()

These functions transform a mutable interpreter into a non-mutable one and vice-versa.

Entries:
- `interpreter`: interpreter to transform into the other type of interpreter

Output:
- interpreter transformed in the other type of interpreter

#### Hidden functions

##### _check_arguments_dict()

This function returns 'ok' if the given dict is a valid argument dict (dict passed to the `add_command` method), if it is not: it returns the error.

Entries:
- `arguments`: arguments dict to check

Outputs:
- `'ok'` if the dict is valid, the error and its cause if it is not: for example: `'argument 'tes"t': not valid name'`

##### _get_str_of_type()

This functions returns the given type transformed in str (only works for str, int, float and None)

Entries:
- `value`: type to transform in str (can only be str, int, float or None)

Outputs:
- string of the given value, for example if `str` is given, `'str'` is returned. If `None` is given, `'none'` is returned.

##### _get_type_of_str()

This function returns the given type stored in the given text (only works for str, int, float and None)

Entries:
- `text`: str to transform in type (can only be 'str', 'int', 'float' or 'none')

Outputs:
- type in the given string, for example if `'str'` is given, `str` is returned. If `'none'` is given, `none` is returned.

##### _encode_str() and _decode_str()

These functions encode or decode a given string, so it can be written into a `.EZCI` file.

The encoding function will replace any `#` by `\1` and any `\` by `\\`. The decoding function will do the exact opposite.

Entries:
- `string`: string to encode or decode

Outputs:
- Encoded / decoded string

##### _encode_interpreter()

This function encodes an interpreter into text, so it can be written into a `.EZCI` file.

Entries:
- `interpreter` interpreter (either mutable or non-mutable) to encode into text.

Outputs:
- Encoded interpreter: text that can be written to a `.EZCI` file.

##### _decode_interpreter()

This function decodes a text into an interpreter.

Entries:
- `text` to decode the interpreter from. 

Outputs:
- interpreter contained in the given text

---

## EZCommandLineErrors

### DecryptionError
This error is raised when the functions `import_interpreter()` or `_decode_interpreter()` are given a corrupted file, which means that the decoder couldn't read a part of the file.

---

## Interpreter encoding

### Global information for the encoding

Commands are stored in command blocks.

Line breaks to add more space in the file aren't interpreted.

If any str in a command contains a `#`, it will be replaced by `\1`

If any str in a command contains a `\`, it will be replaced by `\\`

If you give a corrupted / non-valid file to the decoder, it will raise a `DecryptionError` (see here: [Documentation](Documentation.md#decryptionerror)).

### Encoding functioning

A command block starts with `#COMMAND` and ends with `#COMMANDEND`

Each command block contains a line indicating the name of the command: it starts with `#NAME` and is followed by the name of the command.

Each command block can contain a base argument: it is represented by a line starting with `#BASEARGUMENT` and followed by the type of value accepted by the base argument (`str`, `int` or `float`)

The other lines of the command block are the argument accepted by the command stored in the following encoding:

```
#ARGUMENT argument_name type_of_the_argument
```

In this encoding, type_of_the_argument is either `str`, `int`, `float` or `none`.

The lines starting with `##` aren't interpreted, you can use them to put comments in the file.

### Encoding example

See the examples here: [Documentation](Documentation.md#encoding-example-1)

---

## Examples

### Example to create an interpreter

This is an example on how to create an interpreter:

```python
import EZCommandLine as cl

interpreter = cl.ModifiableCommandLineInterpreter()
interpreter.add_command("show", lambda a: print(a), base_argument=str, arguments={"-color": int})
interpreter.add_command("input", lambda a: print(a), arguments={"-hint": str, "-hidden": None})
```

### Example to use an interpreter

By taking the example above (Example to create an interpreter), we can interpret a command like this:

```python
# Code creating the interpreter

interpreter.interpret('show aaaabbaba -color 1')
interpreter.interpret('input -hint "enter some text"')
```

### Example to export / import an interpreter

This is an example to export an interpreter:

```python
import EZCommandLine as cl

# Code creating the interpreter

cl.export_interpreter(interpreter, "file_path")
```

This is an example to import an interpreter:

```python
import EZCommandLine as cl

interpreter = cl.import_interpreter("file_path")
```

### Encoding example

This interpreter:

```python
import EZCommandLine as cl

interpreter = cl.ModifiableCommandLineInterpreter()
interpreter.add_command("show", lambda a: print(a), base_argument=str, arguments={"-color": int})
interpreter.add_command("input", lambda a: print(a), arguments={"-hint": str, "-hidden": None})

cl.export_interpreter(interpreter, "file_path")
```

Is encoded like this:

```
## This file contains a command to show text and another command to input text

#COMMAND
#NAME show
#BASEARGUMENT str
#ARGUMENT -color int
#COMMANDEND

## Example command: show aaaabbaba -color 1

#COMMAND
#NAME input
#ARGUMENT -hint str
#ARGUMENT -hidden none
#COMMANDEND

## Example command: input -hint "enter some text"
```
