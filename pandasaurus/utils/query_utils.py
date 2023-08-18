from typing import Iterator

from oaklib.implementations import UbergraphImplementation

oi = UbergraphImplementation()


def run_sparql_query(query: str) -> Iterator:
    return oi.query(query=query, prefixes=get_prefixes(query, oi.prefix_map().keys()))


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def get_prefixes(text, prefix_map):
    _prefixes = []
    for prefix in prefix_map:
        if prefix + ":" in text:
            _prefixes.append(prefix)

    return _prefixes
