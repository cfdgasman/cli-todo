import pytest

from todo.cli import main
from todo.store import TodoStore


def test_add_and_persist(tmp_path):
    path = tmp_path / "todo.json"
    store = TodoStore(path)
    store.add("buy milk")
    store.add("write code")
    store.save()

    reloaded = TodoStore(path)
    assert [t.title for t in reloaded.tasks] == ["buy milk", "write code"]
    assert [t.id for t in reloaded.tasks] == [1, 2]


def test_complete_and_remove(tmp_path):
    store = TodoStore(tmp_path / "todo.json")
    a = store.add("a")
    b = store.add("b")
    store.complete(a.id)
    store.remove(b.id)
    assert len(store.tasks) == 1
    assert store.tasks[0].done is True


def test_ids_do_not_repeat_after_remove(tmp_path):
    store = TodoStore(tmp_path / "todo.json")
    store.add("a")
    b = store.add("b")
    store.remove(b.id)
    assert store.add("c").id == 2


def test_empty_title_rejected(tmp_path):
    store = TodoStore(tmp_path / "todo.json")
    with pytest.raises(ValueError):
        store.add("   ")


def test_cli_roundtrip(tmp_path, capsys):
    f = str(tmp_path / "todo.json")
    assert main(["--file", f, "add", "learn", "git"]) == 0
    assert main(["--file", f, "done", "1"]) == 0
    assert main(["--file", f, "list"]) == 0
    out = capsys.readouterr().out
    assert "[x]   1  learn git" in out


def test_cli_unknown_id(tmp_path, capsys):
    f = str(tmp_path / "todo.json")
    assert main(["--file", f, "done", "42"]) == 1
    assert "No task with id 42" in capsys.readouterr().err
