"""Command-line interface for the NCBI downloader."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Sequence

from . import api, db
from .utils.logging_config import configure_logging


LOGGER = logging.getLogger(__name__)


DEFAULT_DB = "publications.db"


def cmd_search(args: argparse.Namespace) -> None:
    configure_logging(level=logging.INFO)
    api.configure_entrez(api_key=args.api_key, email=args.email)
    conn = db.connect(args.database)
    db.initialize_database(conn)

    pmids = api.search_affiliation(args.affiliation)
    records = api.fetch_metadata(pmids)
    for record in records:
        medline = record["MedlineCitation"]
        pmid = medline["PMID"]
        article = medline.get("Article", {})
        title = article.get("ArticleTitle", "")
        abstract = article.get("Abstract", {}).get("AbstractText", [""])
        abstract_text = " ".join(abstract) if isinstance(abstract, list) else str(abstract)
        journal = article.get("Journal", {}).get("Title")
        year = None
        if (
            "Journal" in article
            and "JournalIssue" in article["Journal"]
            and "PubDate" in article["Journal"]["JournalIssue"]
        ):
            pubdate = article["Journal"]["JournalIssue"]["PubDate"]
            year = int(pubdate.get("Year", "0")) if pubdate.get("Year") else None
        pmcid = None
        if "PubmedData" in record and "ArticleIdList" in record["PubmedData"]:
            for aid in record["PubmedData"]["ArticleIdList"]:
                if aid.attributes.get("IdType") == "pmc":
                    pmcid = str(aid)
        db.insert_article(conn, str(pmid), str(title), abstract_text, pmcid, journal, year)
        LOGGER.info("Inserted article %s", pmid)


def cmd_query(args: argparse.Namespace) -> None:
    configure_logging(level=logging.INFO)
    conn = db.connect(args.database)
    results = db.search_articles(conn, args.query)
    for pmid, title in results:
        print(pmid, "-", title)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="NCBI publication downloader")
    parser.add_argument("--database", default=DEFAULT_DB, help="Path to SQLite database")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search", help="Search and store publications")
    search_parser.add_argument("affiliation", help="Affiliation to search for")
    search_parser.add_argument("--api-key", help="NCBI API key")
    search_parser.add_argument("--email", help="Contact email for NCBI")
    search_parser.set_defaults(func=cmd_search)

    query_parser = subparsers.add_parser("query", help="Query stored publications")
    query_parser.add_argument("query", help="FTS query string")
    query_parser.set_defaults(func=cmd_query)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    raise SystemExit(main())

