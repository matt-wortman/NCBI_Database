# NCBI Downloader

This package provides a command-line interface and a minimal PySide6 GUI for
retrieving publications from NCBI's databases and storing them in an SQLite
database. It supports searching by affiliation and full-text search of stored
articles.

## Installing
Install dependencies from `requirements.txt` using `pip`.

```bash
pip install -r requirements.txt
```

## Command Line Usage
Search and store publications by affiliation:

```bash
python -m ncbi_downloader.cli search "Cincinnati Children's Hospital" --api-key YOUR_KEY --email you@example.com
```

Query stored articles:

```bash
python -m ncbi_downloader.cli query "gene therapy"
```

## GUI Usage
Run the GUI with:

```bash
python -m ncbi_downloader.gui
```

