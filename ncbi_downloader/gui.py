"""Minimal PySide6 GUI for the NCBI downloader."""

from __future__ import annotations

import sys
from typing import Iterable

from PySide6 import QtWidgets

from . import api, db
from .utils.logging_config import configure_logging


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, database: str) -> None:
        super().__init__()
        self.database = database
        self.conn = db.connect(database)
        db.initialize_database(self.conn)
        self.setWindowTitle("NCBI Downloader")

        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)

        search_layout = QtWidgets.QHBoxLayout()
        self.term_edit = QtWidgets.QLineEdit()
        self.search_button = QtWidgets.QPushButton("Search")
        search_layout.addWidget(self.term_edit)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)

        self.results = QtWidgets.QListWidget()
        layout.addWidget(self.results)

        self.search_button.clicked.connect(self.run_search)

    def run_search(self) -> None:
        affiliation = self.term_edit.text()
        pmids = api.search_affiliation(affiliation)
        records = api.fetch_metadata(pmids)
        for record in records:
            medline = record["MedlineCitation"]
            pmid = medline["PMID"]
            title = medline.get("Article", {}).get("ArticleTitle", "")
            self.results.addItem(f"{pmid}: {title}")


def run(database: str = "publications.db") -> None:
    configure_logging()
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(database)
    window.show()
    app.exec()


if __name__ == "__main__":  # pragma: no cover - GUI entry point
    run()

