"""Process raw bio.tools records."""

from collections import Counter
from collections.abc import Iterator
from functools import lru_cache
from typing import Any, cast

from orcid_downloader import ground_researcher_unambiguous
from pydantic import BaseModel
from tqdm import tqdm

from biotools_client.api import NAMES, ORCIDS, _get_credits, get_raw_biotools_records


def count_names(raw_records: list[dict[str, Any]]) -> Counter[str]:
    """Count the names appearing in raw records."""
    return Counter(
        author["name"]
        for record in tqdm(raw_records)
        for publication in record.get("publication", [])
        for author in (publication.get("metadata") or {}).get("authors", [])
    )


def count_credits_orcids(raw_records: list[dict[str, Any]]) -> Counter[str]:
    """Get a counter of how many bio.tools records an ORCID appears in."""
    return Counter(orcid for orcids in _get_credits(raw_records).values() for orcid in orcids)


@lru_cache(10_000)
def _cached(name: str) -> str | None:
    return cast(str | None, ground_researcher_unambiguous(name))


class Author(BaseModel):
    """A model for an author."""

    name: str
    orcid: str | None


class Publication(BaseModel):
    """A model for a publication."""

    name: str
    doi: str | None
    pubmed: str | None
    pmc: str | None
    authors: list[Author]


class Record(BaseModel):
    """A model for a record."""

    name: str
    identifier: str
    homepage: str
    publications: list[Publication]


def _process(d: dict[str, Any]) -> Record:
    return Record(
        name=d["name"],
        homepage=d["homepage"],
        identifier=d["biotoolsID"],
        publications=_process_publications(d.get("publication", [])),
    )


def _process_author(a: dict[str, Any]) -> Author:
    name = a["name"]
    orcid = _cached(name)
    return Author(name=name, orcid=orcid)


def _process_publication(raw_publication: dict[str, Any]) -> Publication | None:
    doi = (raw_publication.get("doi") or "").lower() or None
    pubmed = raw_publication.get("pmid") or None
    pmc = raw_publication.get("pmcid") or None
    if not doi and not pubmed and not pmc:
        return None

    metadata = raw_publication["metadata"]
    if metadata is None:
        return None
    name = metadata["title"]
    authors = [_process_author(author) for author in metadata["authors"]]
    return Publication(
        name=name,
        doi=doi,
        pubmed=pubmed,
        pmc=pmc,
        authors=authors,
    )


def _process_publications(raw_publications: list[dict[str, Any]]) -> list[Publication]:
    rv = []
    for raw_publication in raw_publications:
        processed_publication = _process_publication(raw_publication)
        if processed_publication:
            rv.append(processed_publication)
    return rv


def iter_biotools_records() -> Iterator[Record]:
    """Iterate over processed records."""
    for record in tqdm(
        get_raw_biotools_records(), unit="record", unit_scale=True, desc="Standardizing bio.tools"
    ):
        yield _process(record)


def _main() -> None:
    raw_records = get_raw_biotools_records()
    counter = count_names(raw_records)
    with NAMES.open("w") as file:
        print("name", "count", sep="\t", file=file)
        for name, count in counter.most_common():
            print(name, count, sep="\t", file=file)

    orcid_to_name = {}
    for v in _get_credits(raw_records).values():
        orcid_to_name.update(v)

    orcid_counter = count_credits_orcids(raw_records)
    with ORCIDS.open("w") as file:
        print("orcid", "name", "count", sep="\t", file=file)
        for orcid, count in orcid_counter.most_common():
            print(orcid, orcid_to_name[orcid], count, sep="\t", file=file)

    rr = iter_biotools_records()
    i = 0
    for record in rr:
        if i < 10_000:
            if record.publications:
                i += 1
                tqdm.write(record.name)
                for p in record.publications:
                    tqdm.write(f"- {p.authors}")
        else:
            break


if __name__ == "__main__":
    _main()
