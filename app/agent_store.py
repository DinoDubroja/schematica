"""Isolated durable drafts, sessions and immutable dev-library revisions.

The repository library and approval ledger are never write destinations.
"""
from contextlib import contextmanager
import json
from pathlib import Path
import sqlite3
import uuid

from core import ROOT, ValidationError

MARKER = ".schematica-store.json"


def checked_root(path):
    path = Path(path).absolute()
    # Local integration stores are deliberately confined to this checkout's build.
    # Symlinks/junctions at any ancestor must not redirect into another checkout.
    base = ROOT / "build"
    if not path.is_relative_to(base) or path == base:
        raise ValidationError("Store must be a separate directory under this checkout's app/build")
    for parent in (path, *path.parents):
        if parent.is_symlink() or parent.is_junction():
            raise ValidationError("Store paths may not contain symlinks or junctions")
    if not path.resolve().is_relative_to(base.resolve()):
        raise ValidationError("Store escapes this checkout")
    return path.resolve()


def initialize(path):
    path = checked_root(path)
    marker = path / MARKER
    if marker.exists():
        return Store(path).status()
    if path.exists() and any(path.iterdir()):
        raise ValidationError("Initialize an empty directory; refusing to adopt existing data")
    path.mkdir(parents=True, exist_ok=True)
    marker.write_text(json.dumps({"schema_version": 1, "root": str(path), "purpose": "integration-dev-library"}), encoding="utf-8")
    return Store(path).status()


class Store:
    def __init__(self, root):
        self.root = checked_root(root)
        try:
            marker = json.loads((self.root / MARKER).read_text(encoding="utf-8"))
        except (FileNotFoundError, ValueError):
            raise ValidationError("Initialize and verify the isolated store before enabling writes") from None
        if marker != {"schema_version": 1, "root": str(self.root), "purpose": "integration-dev-library"}:
            raise ValidationError("Store identity does not match its actual destination")
        with self.connection() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS documents(kind TEXT, id TEXT, value TEXT,
                    PRIMARY KEY(kind,id));
                CREATE TABLE IF NOT EXISTS versions(id TEXT, revision INTEGER, value TEXT,
                    PRIMARY KEY(id,revision));
            """)

    @contextmanager
    def connection(self):
        checked_root(self.root)
        for name in ("state.sqlite3", "state.sqlite3-journal", "state.sqlite3-wal", "state.sqlite3-shm"):
            file = self.root / name
            if file.is_symlink() or file.is_junction():
                raise ValidationError("Database files may not redirect outside the isolated store")
        db = sqlite3.connect(self.root / "state.sqlite3", timeout=30)
        try:
            with db:
                yield db
        finally:
            db.close()

    def status(self):
        return {"root": str(self.root), "purpose": "integration-dev-library",
                "official_approval_writes": False, "initialized": True}

    def get(self, kind, key):
        with self.connection() as db:
            row = db.execute("SELECT value FROM documents WHERE kind=? AND id=?", (kind, key)).fetchone()
        if row is None:
            raise ValidationError(f"Unknown {kind}: {key}")
        return json.loads(row[0])

    def put(self, kind, key, value):
        with self.connection() as db:
            db.execute("INSERT OR REPLACE INTO documents VALUES(?,?,?)", (kind, key, json.dumps(value)))

    def create(self, kind, value):
        key = uuid.uuid4().hex
        self.put(kind, key, value)
        return key

    def current_versions(self):
        with self.connection() as db:
            rows = db.execute("SELECT value FROM versions v WHERE revision=(SELECT MAX(revision) FROM versions WHERE id=v.id)").fetchall()
        return [json.loads(row[0]) for row in rows]

    def version(self, sid, revision):
        with self.connection() as db:
            row = db.execute("SELECT value FROM versions WHERE id=? AND revision=?", (sid, revision)).fetchone()
        return json.loads(row[0]) if row else None

    def save_version(self, value, expected_revision):
        sid, revision = value["id"], value["revision"]
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            current = db.execute("SELECT MAX(revision) FROM versions WHERE id=?", (sid,)).fetchone()[0]
            if current is not None and current != expected_revision:
                raise ValidationError("Symbol changed since this draft began; create a fresh draft")
            if current is not None and revision <= current:
                raise ValidationError("Revision must advance")
            db.execute("INSERT INTO versions VALUES(?,?,?)", (sid, revision, json.dumps(value)))

    def artifact(self, relative):
        path = checked_root(self.root) / relative
        if not path.resolve().is_relative_to(self.root) or path.is_symlink() or path.is_junction():
            raise ValidationError("Invalid artifact path")
        for parent in path.parents:
            if parent == self.root:
                break
            if parent.is_symlink() or parent.is_junction():
                raise ValidationError("Redirected artifact directory")
        return path
