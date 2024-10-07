"""Client for Biotools API.

Data is available from this resource under
the `CC BY 4.0 <https://biotools.readthedocs.io/en/latest/license.html>`_
license.
"""

import json
from collections import defaultdict
from typing import Any, cast

import pystow
import requests
from tqdm import tqdm

__all__ = [
    "get_raw_biotools_records",
    "get_biotools_to_orcids",
]

URL = "https://bio.tools/api/tool/"
MODULE = pystow.module("bio", "biotools")
PATH = MODULE.join(name="records.json")
NAMES = MODULE.join(name="names.tsv")
ORCIDS = MODULE.join(name="orcids.tsv")


def _request(page: int) -> dict[str, Any]:
    res = requests.get(URL, params={"format": "json", "page": str(page)}, timeout=5)
    res.raise_for_status()
    res_json = res.json()
    return cast(dict[str, Any], res_json)


def get_raw_biotools_records(force: bool = False) -> list[dict[str, Any]]:
    """Get raw records from the `bio.tools API <https://bio.tools/api/tool/>`_."""
    if PATH.is_file() and not force:
        return cast(list[dict[str, Any]], json.loads(PATH.read_text()))

    records = []
    res_json = _request(1)
    first_list = res_json["list"]
    records.extend(first_list)
    count = res_json["count"]
    with tqdm(
        total=count - len(first_list), unit_scale=True, unit="record", desc="Downloading bio.tools"
    ) as pbar:
        while res_json["next"]:  # 3024 was maximum on October 1, 2024
            page = int(res_json["next"].removeprefix("?page="))
            res_json = _request(page)
            these_records = res_json["list"]
            records.extend(these_records)
            pbar.update(len(these_records))
            PATH.write_text(json.dumps(records, indent=2, ensure_ascii=False))

    return records


def get_biotools_to_orcids() -> dict[str, set[str]]:
    """Get ORCID identifiers for researchers who contributed to each resource."""
    rv: defaultdict[str, set[str]] = defaultdict(set)
    for biotools_id, orcids in _get_credits().items():
        rv[biotools_id].update(orcids)
    return dict(rv)


def _get_credits(raw_records: list[dict[str, Any]] | None = None) -> dict[str, dict[str, str]]:
    """Get a mapping from bio.tools identifiers to ORCID identifier to name."""
    if raw_records is None:
        raw_records = get_raw_biotools_records()
    rv: defaultdict[str, dict[str, str]] = defaultdict(dict)
    for record in raw_records:
        for author in record.get("credit", []):
            orcid = author.get("orcidid")
            name = author.get("name")
            if name and orcid:
                orcid = (
                    orcid.removeprefix("https://orcid.org/")
                    .removeprefix("http://orcid.org/")
                    .removesuffix("/")
                )
                rv[record["biotoolsID"]][orcid] = name
    return dict(rv)
