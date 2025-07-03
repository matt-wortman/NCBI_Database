"""SQLite database utilities for storing publications."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable, Optional

DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS articles (
    pmid TEXT PRIMARY KEY,
    title TEXT,
    abstract TEXT,
    pmcid TEXT,
    journal TEXT,
    year INTEGER
);

CREATE VIRTUAL TABLE IF NOT EXISTS article_fts USING fts5(
    pmid,
    title,
    abstract
);
"""


def connect(db_path: str | Path) -> sqlite3.Connection:
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(db_path)
    return conn


def initialize_database(conn: sqlite3.Connection) -> None:
    """Initialize the database schema."""
    with conn:
        conn.executescript(DB_SCHEMA)


def insert_article(conn: sqlite3.Connection, pmid: str, title: str, abstract: str | None,
                   pmcid: str | None, journal: str | None, year: int | None) -> None:
    """Insert a single article into the database."""
    with conn:
        conn.execute(
            "INSERT OR REPLACE INTO articles (pmid, title, abstract, pmcid, journal, year)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (pmid, title, abstract, pmcid, journal, year),
        )
        conn.execute(
            "INSERT OR REPLACE INTO article_fts (pmid, title, abstract) VALUES (?, ?, ?)",
            (pmid, title, abstract),
        )


def search_articles(conn: sqlite3.Connection, query: str) -> list[tuple[str, str]]:
    """Search articles using the full-text index."""
    cursor = conn.execute(
        "SELECT pmid, title FROM article_fts WHERE article_fts MATCH ? ORDER BY rank",
        (query,),
    )
    return cursor.fetchall()

