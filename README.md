# Advent of Code 2024

![](https://img.shields.io/badge/day%20📅-3-blue)
![](https://img.shields.io/badge/stars%20⭐-6-yellow)
![](https://img.shields.io/badge/days%20completed-3-red)

This Repository contains some solutions for advent of code 2024 as well as a CLI to make some things easier.
Feel free to use the solutions, as well as the rest of this repo for whatever you want.

## CLI

The CLI is meant to automate some things and make youre life easier. Here a the available commands:

- `create n` - is used to initialize all files needed for a new day with number `n`. These include `days/day{n}.py` and `input/day{n}.test.txt` (the normal input file is downloaded automatically when running the corresponding python file)
- `run n` - this command runs the `days/day{n}.py` file.
- `runall` - this command runs all available days in the `days/` directory.
- `update-badge` - this command will fetch user-data from the AoC Website and update the Badges in the `README.md` accordingly.

For all options you can run the `main.py` file with the `--help` flag.
If you use the CLI, make sure you install all dependencies specified in the `pyproject.toml` file.

## Project Structure

```
.
├── days
│  ├── day1.py
│  └── ...
├── input
│  ├── day1.test.txt
│  ├── day1.txt
│  └── ...
├── util
│  ├── __init__.py
│  ├── env.py
│  ├── fetch.py
│  ├── file.py
│  ├── parse.py
│  ├── read.py
│  └── timer.py
├── main.py
├── README.md
├── example.env
├── pyproject.toml
└── template.py.txt
```

The CLI for managing solutions etc. can be run from the `main.py` file.
All solutions for the days are contained in the `days/` directory.
Days that get created via the CLIs `create` command get populated with the contents of `template.py.txt`, where `{day}` gets replace with the actual number.

The corresponding input files are stored in the `input/` directory, which is gitignored, because the author of AoC [does not want that parts get reuploaded](https://adventofcode.com/2024/about). If you clone this repo, please keep it like this.
The `input/` directory will get created automatically when needed.

The module `util/` contains various helper method for the CLI, as well as the challenges themselves.

If you clone this repo, make sure to create an `.env` file, which contains youre AoC Session-Token as well as youre userid (see `example.env`).
Both can be found on the AoC website (see [here](https://github.com/wimglenn/advent-of-code-wim/issues/1) for help).
