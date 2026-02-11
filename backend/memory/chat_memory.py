import json
import os
from threading import Lock

class ChatMemory:
    def __init__(self, storage_path='backend/memory/chat_history.json'):
        self.storage_path = storage_path
        self.lock = Lock()
        self.chat_history = {}  # dict of session_id -> list of messages
        self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    self.chat_history = json.load(f)
            except Exception:
                self.chat_history = {}
        else:
            self.chat_history = {}

    def _save(self):
        with self.lock:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.chat_history, f, ensure_ascii=False, indent=2)

    def add_message(self, session_id, message):
        """Add a message to the chat history for a session."""
        with self.lock:
            if session_id not in self.chat_history:
                self.chat_history[session_id] = []
            self.chat_history[session_id].append(message)
            self._save()

    def get_history(self, session_id):
        """Get the full chat history for a session."""
        with self.lock:
            return list(self.chat_history.get(session_id, []))

    def clear_history(self, session_id):
        """Clear the chat history for a session."""
        with self.lock:
            self.chat_history[session_id] = []
            self._save()
