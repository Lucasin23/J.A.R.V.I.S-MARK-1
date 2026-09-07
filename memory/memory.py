import json
from pathlib import Path

MEMORY_FILE = Path(__file__).parent / "memory.json"


def load_memory():
    if not MEMORY_FILE.exists():
        return {}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}


def save_memory(memory):
    temporary_file = MEMORY_FILE.with_suffix(".tmp")
    with open(temporary_file, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=4, ensure_ascii=False)
    temporary_file.replace(MEMORY_FILE)


def remember(key, value):
    memory = load_memory()
    memory[key] = value
    save_memory(memory)


def recall(key):
    memory = load_memory()
    return memory.get(key)


def forget(key):
    """Remove one saved memory and report whether it existed."""
    memory = load_memory()
    if key not in memory:
        return False
    del memory[key]
    save_memory(memory)
    return True


def memory_keys():
    """Return memory labels without exposing every saved value by default."""
    return sorted(load_memory())
