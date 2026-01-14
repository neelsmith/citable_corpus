from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("citable_corpus") # 'name' of package from pyproject.toml
except PackageNotFoundError:
    # Package is not installed (e.g., running from a local script)
    __version__ = "unknown"


from .passage import CitablePassage
from .corpus import CitableCorpus

__all__ = ["CitablePassage", "CitableCorpus"]