# command-storage

- [command-storage](#command-storage)
  - [How to Use? CRUD Operations](#how-to-use-crud-operations)
    - [C](#c)
    - [R](#r)
    - [U](#u)
    - [D](#d)
    - [Credits](#credits)

A command line tool to store CLI commands for quick access and usage.

I have found myself in need often to store certain commands for later usage. Generally
these are the commands I cant always remember or find useful to remember. Currently I
would store them into a file and then copy paste into the terminal for usage.

So, it got me thinking of creating one simple CLI based tool to store such commands.

## How to Use? CRUD Operations

I would like to do simple CRUD operations. I am listing all features I intend to add
over time. The ones marked with `[Done]` are implemented so far. I will keep updating
these as per my need and development or any reviews. The ones marked `[TODO]` are put
here from on top of my mind as moonshots.

- Enter into interactive mode `cmds`. `[TODO]`.
- Key must be unique for each command. If you repeat the key, you would get a warning
  about the same.

### C

- Be able to store commands by giving them a helpful key name to refer to (description
  is optional). `cmds --store <key> <command> <description>`
- Be able to store parametrized commands so that a command can be passed arguments
  before running/viewing. `[TODO]`

### R

- Get help. `cmds --help` or `cmds -h`
- Be able to view all stored commands. `cmds --view` or `cmds -v`
- Be able to view a command by its key (exact match). `cmds --view <key_name>` or `cmds
  -v <key_name>` or `cmds <key_name>` (shortcut)
- Be able to filter commands using fuzzy search. Add `-f` or `--fuzzy` to previous
  commands to view by key. Can also do `-vf` or `-fv`
- Be able to export all/filtered commands into a file. `cmds --export <file_name>` or
  `cmds -e <file_name>`
- (Interactive mode) Be able to copy selected command (with/without passing parameters).
  `[TODO]`
- (Interactive mode) Be able to run selected command (with/without passing parameters).
  `[TODO]`

### U

- Be able to update a command by its key (Both `--command` and `--description` are
  optional). `cmds --update <key> --command <command> --description <description>`
- Be able to update the original key. `cmds --update --key <key_initial> <key_new>`. You
  can mix it with previous command also `cmds --update --key <key_initial> <key_new>
  --command <command> --description <description>`
- (Interactive mode) Be able to select a command and update it. `[TODO]`

### D

- Be able to delete a command by its key. `cmds --delete <key>`
- (Interactive mode) Be able to select a command and delete it. `[TODO]`

### Credits

- This is my first CLI based application and [Real Python's article](https://realpython.com/python-typer-cli/) helped with the same.