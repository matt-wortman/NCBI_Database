import sqlite3
import tempfile
from ncbi_downloader import db


def test_insert_and_search(tmp_path):
    db_path = tmp_path / "test.db"
    conn = db.connect(db_path)
    db.initialize_database(conn)
    db.insert_article(conn, "1", "Test Article", "Abstract text", None, "Journal", 2023)
    results = db.search_articles(conn, "Test")
    assert results
    assert results[0][0] == "1"

