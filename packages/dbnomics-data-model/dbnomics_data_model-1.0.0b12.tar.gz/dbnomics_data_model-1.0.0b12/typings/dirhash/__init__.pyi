from collections.abc import Iterable
from pathlib import Path

def dirhash(
    directory: str | Path,
    *,
    algorithm: str,
    match: Iterable[str] = ("*",),
    ignore: Iterable[str] | None = None,
    linked_dirs: bool = True,
    linked_files: bool = True,
    empty_dirs: bool = False,
    entry_properties: Iterable[str] = ("name", "data"),
    allow_cyclic_links: bool = False,
    chunk_size: int = ...,
    jobs: int = 1,
) -> str: ...
