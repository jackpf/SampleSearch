from dataclasses import dataclass
from pathlib import Path

from .vector_repository import VectorRepository


@dataclass
class SampleInfo:
    id: int | None
    path: Path
    mtime: float | None
    file_hash: str
    vector: list[float] | None


class SamplesRepository(VectorRepository):
    def __init__(self, db_file: Path) -> None:
        super().__init__(db_file)

        self._db.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS samples USING vec0(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT,
                mtime FLOAT,
                file_hash TEXT,
                embedding float[512]
            );
        """)

    def upsert(self, samples: list[SampleInfo]) -> None:
        upsert = []
        for sample in samples:
            vector = (
                self._serialize_f32(sample.vector) if sample.vector is not None else []
            )
            upsert.append(
                (
                    sample.id,
                    str(sample.path.resolve()),
                    sample.mtime,
                    sample.file_hash,
                    vector,
                )
            )

        self._db.executemany(
            "INSERT OR REPLACE INTO samples(rowid, path, mtime, file_hash, embedding) VALUES (?, ?, ?, ?, ?)",
            upsert,
        )
        self._db.commit()

    def search(
        self, query_vector: list[float], k: int = 5, fetch_embedding: bool = False
    ) -> list[SampleInfo]:
        fetch_embedding_q = ",embedding" if fetch_embedding else ""
        results = self._db.execute(
            f"""
            SELECT
                rowid,
                path,
                mtime,
                file_hash,
                distance
                {fetch_embedding_q}
            FROM samples
            WHERE embedding MATCH ?
            AND k = ?
            ORDER BY distance
        """,
            (self._serialize_f32(query_vector), k),
        ).fetchall()

        samples = []
        for result in results:
            samples.append(
                SampleInfo(
                    id=result["rowid"],
                    path=Path(result["path"]),
                    mtime=result["mtime"],
                    file_hash=result["file_hash"],
                    vector=self._deserialize_f32(result["embedding"])
                    if fetch_embedding
                    else None,
                )
            )

        return samples
