import sqlite3
import struct
from abc import ABC
from pathlib import Path

import sqlite_vec


class VectorRepository(ABC):
    def __init__(self, db_file: Path) -> None:
        self._db = sqlite3.connect(db_file.resolve())
        self._db.enable_load_extension(True)
        sqlite_vec.load(self._db)
        self._db.enable_load_extension(False)
        self._db.row_factory = sqlite3.Row

    def _serialize_f32(self, vector: list[float]) -> bytes:
        """Serializes a list of floats into a raw byte string."""
        return struct.pack(f"{len(vector)}f", *vector)

    def _deserialize_f32(self, data: bytes) -> list[float]:
        """Deserializes a byte string back into a list of floats."""
        count = len(data) // 4
        return list(struct.unpack(f"{count}f", data))
