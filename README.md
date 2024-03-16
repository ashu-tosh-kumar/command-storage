# command-storage

- [command-storage](#command-storage)
  - [About](#about)
  - [Features](#features)
  - [Installation](#installation)
  - [Examples](#examples)
  - [Usage](#usage)
    - [`cmds delete`](#cmds-delete)
    - [`cmds export`](#cmds-export)
    - [`cmds init`](#cmds-init)
    - [`cmds list`](#cmds-list)
    - [`cmds store`](#cmds-store)
    - [`cmds update`](#cmds-update)
  - [Release History](#release-history)
  - [Credits](#credits)

## About

`cmds` is a command-line tool designed to store CLI commands for quick access and usage.
Think of it as a simple notes app specifically tailored for storing commands using
customizable keys.

Oftentimes, we find ourselves needing to store certain commands for later use. These may
be commands that are not easily remembered or ones that we find useful but don't want to
keep looking up. Traditionally, we might store these commands in a file and then copy
and paste them into the terminal when needed. Recognizing the need for a more efficient
solution, I decided to create a CLI application to streamline this process.

You can find the project on [pip](https://pypi.org/project/command-storage/).

## Features

- Store CLI commands with custom keys for easy retrieval.
- Quickly access stored commands with fuzzy search without the need to search through
  files.
- Organize commands based on your workflow or preferences.
- Export all commands into a JSON file.

## Installation

Using [pip](https://pypi.org/project/command-storage/).

```bash
pip install command-storage
```

Using [brew](https://brew.sh/). Gem file maintained in repository [homebrew-command-storage](https://github.com/ashu-tosh-kumar/homebrew-command-storage).
  
```bash
brew tap ashu-tosh-kumar/command-storage
brew install command-storage
```

Using [pipx](https://pipx.pypa.io/stable/).

```bash
pipx install command-storage
```

**NOTE**: Initialize the application by running `cmds init`. Note that if you want to have
cross platform sync of data, you can choose location of file to be inside a drive
installed on your system like Onedrive.

## Examples

Seeking help.

```bash
cmds --help
```

![alt text](<images/cmds help.png>)

Storing some commands into the `cmds`.

```bash
cmds store --key "count no of files" --command "ls | wc -l" --description "count no of files in a directory"
cmds store --key "run python test with cov" --command "pytest --cov --cov-report term --cov-report xml:coverage.xml" --description "pytest with cov"
```

Viewing all commands stored in `cmds`.

```bash
cmds list
```

![alt text](<images/cmds list.png>)

## Usage

```bash
cmds [OPTIONS] COMMAND [ARGS]...
```

**Options**:

- `-v, --version`: Show cmds version.
- `--help`: Show this message and exit.

**Commands**:

- `delete`: Allows deletion of stored command by key
- `export`: Exports all stored commands into a JSON file.
- `init`: Initialize the application.
- `list`: Show list of all stored commands.
- `store`: Store a new command into cmds.
- `update`: Allows updating a stored command by its key.

### `cmds delete`

Allows deletion of stored command by key

**Usage**:

```bash
cmds delete [OPTIONS] [KEY]
```

**Arguments**:

- `[KEY]`

**Options**:

- `-a, --all`: Delete all commands
- `--help`: Show this message and exit.

### `cmds export`

Exports all stored commands into a JSON file.

**Usage**:

```bash
cmds export [OPTIONS]
```

**Options**:

- `-f, --file TEXT`: Export file address with extension  [default: command_storage_export_2024-02-28 19:37:47.575256.json]
- `--help`: Show this message and exit.

### `cmds init`

Initialize the application. One time process and overwrites existing config and
data files.

Args:
    db_path (str, optional): `--db-path` argument. Defaults to_INITIAL_DB_PATH.

Raises:
    typer.Exit: If error in app initialization
    typer.Exit: if error in database file initialization

**Usage**:

```bash
cmds init [OPTIONS]
```

**Options**:

- `-db, --db-path TEXT`: [default: <home_path>.<home_path_name>_cmds.json]
- `--help`: Show this message and exit.

### `cmds list`

Show list of all stored commands. Also supports fuzzy matching on key. Run 'cmds
list --help' to see how.

**Usage**:

```bash
cmds list [OPTIONS]
```

**Arguments**:

- `[KEY]`: Key for the command.
-

**Options**:

- `--help`: Show this message and exit.

### `cmds store`

Store a new command into cmds by giving a helpful key name to refer to.

**Usage**:

```bash
cmds store [OPTIONS]
```

**Options**:

- `-k, --key TEXT`: Key for the command.  [required]
- `-c, --command TEXT`: Command to be stored.  [required]
- `-des, --description TEXT`: Description of command to be stored.
- `--help`: Show this message and exit.

### `cmds update`

Allows updating a stored command by its key. Also supports changing the key.

**Usage**:

```bash
cmds update [OPTIONS] ORIG_KEY
```

**Arguments**:

- `ORIG_KEY`: [required]

**Options**:

- `-k, --key TEXT`: Key for the command.
- `-c, --command TEXT`: Command to be stored.
- `-des, --description TEXT`: Description of command to be stored.
- `--help`: Show this message and exit.

## Release History

`0.1.0` - First working release (built using Python 3.11)

`0.1.1` - Lowered Python version requirement to 3.9. Added support to be installable via multiple package managers.

## Credits

- This is my first CLI based application and [Real Python's
  article](https://realpython.com/python-typer-cli/) helped a lot.
- Built with ❤️ using [Typer](https://typer.tiangolo.com/).
- Fuzzy Matching logic: [TheFuzz](https://github.com/seatgeek/thefuzz).
- Printing in tabular format: [tabulate](https://github.com/astanin/python-tabulate)
- CLI usage documentation generated using
  [typer-cli](https://typer.tiangolo.com/typer-cli/) command: `typer
  command_storage.views.cli utils docs`.
