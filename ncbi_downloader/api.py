"""NCBI API utilities for searching and retrieving publications."""

from __future__ import annotations

import logging
import time
from typing import Iterable, List

from Bio import Entrez

logger = logging.getLogger(__name__)


def configure_entrez(api_key: str | None = None, email: str | None = None) -> None:
    """Configure global Entrez settings."""
    if api_key:
        Entrez.api_key = api_key
    if email:
        Entrez.email = email


def search_affiliation(affiliation: str, retmax: int = 1000) -> List[str]:
    """Search PubMed for PMIDs matching an affiliation."""
    logger.info("Searching PubMed for affiliation: %s", affiliation)
    handle = Entrez.esearch(db="pubmed", term=f"{affiliation}[AD]", retmax=retmax)
    result = Entrez.read(handle)
    handle.close()
    pmids = result.get("IdList", [])
    logger.debug("Found %d PMIDs", len(pmids))
    return pmids


def fetch_metadata(pmids: Iterable[str]) -> List[dict]:
    """Fetch article metadata for a list of PMIDs."""
    results = []
    pmid_list = list(pmids)
    logger.info("Fetching metadata for %d PMIDs", len(pmid_list))
    if not pmid_list:
        return results

    handle = Entrez.efetch(db="pubmed", id=",".join(pmid_list), rettype="xml")
    records = Entrez.read(handle)
    handle.close()
    for article in records["PubmedArticle"]:
        results.append(article)
    logger.debug("Fetched %d records", len(results))
    return results


def fetch_fulltext(pmcid: str) -> str | None:
    """Fetch full text XML from PubMed Central for a given PMCID."""
    logger.info("Fetching full text for PMCID: %s", pmcid)
    try:
        handle = Entrez.efetch(db="pmc", id=pmcid, rettype="full")
        text = handle.read()
        handle.close()
        time.sleep(0.34)  # be polite with NCBI servers
        return text
    except Exception as exc:  # pragma: no cover - network errors
        logger.error("Failed to fetch full text for %s: %s", pmcid, exc)
        return None

