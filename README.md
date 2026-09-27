# cli-todo

[![CI](https://github.com/cfdgasman/cli-todo/actions/workflows/ci.yml/badge.svg)](https://github.com/cfdgasman/cli-todo/actions/workflows/ci.yml)

A tiny command-line to-do list written in plain Python (no dependencies). Tasks are stored in a JSON file.

## Install

```bash
pip install git+https://github.com/cfdgasman/cli-todo.git
```

## Usage

```bash
todo add buy milk
todo add finish the report
todo list
todo done 1
todo rm 2
todo clear        # remove all completed tasks
```

```
[x]   1  buy milk
[ ]   2  finish the report
```

Tasks are saved to `~/.todo.json`. Use `--file path.json` or set `TODO_FILE` to use another file.

## Development

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
