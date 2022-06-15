# PyCord

Translate Python code into Discord bots.

## Description

There are quite a few people who know a little Python and have wanted to make a Discord bot, but not wanted to learn how to use a new framework. PyCord is meant to bridge that gap by turning pure Python code like this running total program:

```py
total = 0
print("Enter your numbers for a running total!")
while True:
    x = input().strip().lower()
    if x == "quit":
        break
    else:
        try:
            total += float(x)
            print("Running total:", total)
        except ValueError():
            print("Not a number, enter `quit` to quit")
print("Goodbye!")
```

Into discord bot behavior:

<image src="images/running_total.png" width="30%">

Currently the project is in a very early stage, and struggles to run some programs. Some key caveats are:
* Prompts must end with newlines, that is, `input("Enter a number:")` must be replaced with `input("Enter a number:\n")`.
* If a program takes too long to output (more than 3 seconds), its output won't be received until the next input.

## Getting Started

### Dependencies

* [Git](https://git-scm.com/)
* [Python 3](https://www.python.org/)

### Installing

* Clone to this repository and navigate to the directory
```sh
git clone https://github.com/Swiddis/PyCord.git
cd PyCord
```
* Create a new virtual environment named `venv`
```sh
python -m venv venv
```
* Activate `venv` and install needed dependencies
```sh
.\\venv\\scripts\\activate.bat
pip install asyncio discord.py
```
* [Create a Discord bot](https://discord.com/developers/applications) and get the token
* Create a token file using your discord token
```sh
echo [DISCORD TOKEN HERE] > token.txt
```

### Executing program

* Run the bot through python:
```sh
python bot.py
```

The bot will read command programs from the `programs` folder, the names of the programs are the names that the bot will use. Note that you need to make sure the virtual environment is activated on every run.

## Version History

* 0.1
    * Initial Release: Early stage, quite buggy, poorly structured, and don't ask about the documentation I wrote this in one evening.

## Contributing

Any and all contributions are welcome. Here's a quick list of TODOs:
- Switch from a queue with a timeout to directly monitoring program pipes for output.
- General quality improvements.
- Better code documentation and structuring.
- Simplify the installation process.
- Better error handling.
    - In particular, reading programs' STDERR streams.
- Turn PyCord into a Python library than can be run as part of an existing bot.

## License

This project is licensed under the MIT License - see the LICENSE file for details
