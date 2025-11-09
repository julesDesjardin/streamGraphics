import sqlite3
import json
import threading
import time
from typing import Any, Callable, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os


class SQLiteQueue:
    def __init__(self, db_path: str, callback: Optional[Callable[[Any], None]] = None):
        self.db_path = db_path
        self.callback = callback
        self._lock = threading.Lock()
        self._init_db()

        # Track last seen id to avoid duplicate callbacks
        self._last_seen_id = self._get_max_id()

        # Start a file watcher if callback is provided
        if callback:
            self._start_watcher()

    # --- Database setup ---
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT NOT NULL
                )
            """)
            conn.commit()

    # --- Basic queue ops ---
    def put(self, item: Any):
        """Add an item to the queue."""
        with self._lock, sqlite3.connect(self.db_path, timeout=5) as conn:
            conn.execute("INSERT INTO queue (data) VALUES (?)", (json.dumps(item),))
            conn.commit()

    def get(self) -> Optional[Any]:
        """Retrieve and remove the oldest item (FIFO)."""
        with self._lock, sqlite3.connect(self.db_path, timeout=5) as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, data FROM queue ORDER BY id LIMIT 1")
            row = cur.fetchone()
            if not row:
                return None
            conn.execute("DELETE FROM queue WHERE id = ?", (row[0],))
            conn.commit()
            return json.loads(row[1])

    def _get_max_id(self) -> int:
        """Return the highest existing ID in the queue."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT MAX(id) FROM queue")
            row = cur.fetchone()
            return row[0] or 0

    # --- Watchdog integration ---
    def _start_watcher(self):
        """Start a filesystem watcher on the DB file."""
        class _Handler(FileSystemEventHandler):
            def __init__(self, outer):
                self.outer = outer

            def on_modified(self, event):
                if os.path.abspath(event.src_path) == os.path.abspath(self.outer.db_path):
                    self.outer._check_new_items()

        handler = _Handler(self)
        observer = Observer()
        observer.schedule(handler, path=os.path.dirname(os.path.abspath(self.db_path)) or ".", recursive=False)
        observer.daemon = True
        observer.start()
        self._observer = observer

    def _check_new_items(self):
        """Check for new rows and trigger callback."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, data FROM queue WHERE id > ? ORDER BY id", (self._last_seen_id,))
            rows = cur.fetchall()

        for row_id, data in rows:
            self._last_seen_id = max(self._last_seen_id, row_id)
            try:
                if self.callback:
                    print(json.loads(data))
                    self.callback(json.loads(data))
            except Exception as e:
                print(f"[Callback error] {e}")

    def stop(self):
        """Stop the watcher thread."""
        if hasattr(self, "_observer"):
            self._observer.stop()
            self._observer.join()
