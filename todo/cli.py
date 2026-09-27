"""Command-line interface: `todo add|list|done|rm`."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from .store import TodoStore

DEFAULT_FILE = Path.home() / ".todo.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="todo", description="A tiny to-do list.")
    parser.add_argument(
        "--file",
        type=Path,
        default=Path(os.environ.get("TODO_FILE", DEFAULT_FILE)),
        help="where tasks are stored (default: ~/.todo.json or $TODO_FILE)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="add a task")
    add.add_argument("title", nargs="+")

    sub.add_parser("list", help="list tasks")

    done = sub.add_parser("done", help="mark a task as done")
    done.add_argument("id", type=int)

    rm = sub.add_parser("rm", help="remove a task")
    rm.add_argument("id", type=int)

    sub.add_parser("clear", help="remove all completed tasks")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    store = TodoStore(args.file)

    try:
        if args.command == "add":
            task = store.add(" ".join(args.title))
            store.save()
            print(f"Added #{task.id}: {task.title}")
        elif args.command == "list":
            if not store.tasks:
                print("Nothing to do. 🎉")
            for task in store.tasks:
                mark = "x" if task.done else " "
                print(f"[{mark}] {task.id:>3}  {task.title}")
        elif args.command == "done":
            task = store.complete(args.id)
            store.save()
            print(f"Done #{task.id}: {task.title}")
        elif args.command == "rm":
            task = store.remove(args.id)
            store.save()
            print(f"Removed #{task.id}: {task.title}")
        elif args.command == "clear":
            count = store.clear_done()
            store.save()
            print(f"Cleared {count} completed task(s)")
    except (KeyError, ValueError) as err:
        print(f"error: {err.args[0]}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
