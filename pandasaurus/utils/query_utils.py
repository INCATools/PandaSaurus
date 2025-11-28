import os
from typing import Iterable, Iterator, List, Sequence, TypeVar

import certifi
from oaklib.implementations import UbergraphImplementation

# Ensure HTTPS requests trust the certifi bundle; this avoids local certificate issues.
os.environ.setdefault("SSL_CERT_FILE", certifi.where())
os.environ.setdefault("REQUESTS_CA_BUNDLE", certifi.where())

oi = UbergraphImplementation()
T = TypeVar("T")


def run_sparql_query(query: str) -> Iterator:
    """Execute a SPARQL query against Ubergraph."""
    return oi.query(query=query, prefixes=get_prefixes(query, oi.prefix_map().keys()))


def chunks(items: Sequence[T], size: int) -> Iterator[Sequence[T]]:
    """Yield slices of `items` with at most `size` entries."""
    for i in range(0, len(items), size):
        yield items[i : i + size]


def get_prefixes(text: str, prefix_map: Iterable[str]) -> List[str]:
    """Return CURIE prefixes referenced in `text`."""
    return [prefix for prefix in prefix_map if f"{prefix}:" in text]
