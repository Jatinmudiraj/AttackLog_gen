# utils/memory_utils.py
import os
import json
from typing import Dict, List

MEMORY_FILE = "llm_memory.json"
MAX_TURNS_PER_KEY = 3         # keep last 3 user+assistant turns
MAX_ASSISTANT_CHARS = 4000    # truncate stored logs to avoid huge context


def _load_memory() -> Dict[str, List[Dict[str, str]]]:
    """
    Load the full memory dictionary from disk.
    Structure:
      {
        "memory_id_1": [
            {"role": "user", "content": "..."},
            {"role": "assistant", "content": "..."},
            ...
        ],
        ...
      }
    """
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_memory(data: Dict[str, List[Dict[str, str]]]) -> None:
    """Safely write the memory dictionary back to disk."""
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        # If saving fails, we just skip; do not crash generation.
        pass


def get_history(memory_id: str) -> List[Dict[str, str]]:
    """
    Return the stored message history for a given memory_id.
    """
    mem = _load_memory()
    return mem.get(memory_id, [])


def add_turn(memory_id: str, user_msg: str, assistant_msg: str) -> None:
    """
    Append a (user, assistant) turn to the memory for memory_id.
    Assistant message is truncated to avoid very large context.
    """
    mem = _load_memory()
    history = mem.get(memory_id, [])

    # Append new turn
    history.append({"role": "user", "content": user_msg})
    history.append({
        "role": "assistant",
        "content": assistant_msg[:MAX_ASSISTANT_CHARS]
    })

    # Keep only the last MAX_TURNS_PER_KEY turns (user+assistant pairs)
    max_messages = MAX_TURNS_PER_KEY * 2
    if len(history) > max_messages:
        history = history[-max_messages:]

    mem[memory_id] = history
    _save_memory(mem)
