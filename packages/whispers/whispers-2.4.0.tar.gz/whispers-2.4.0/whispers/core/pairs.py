import logging
from pathlib import Path
from typing import Iterator, Optional

from whispers.core.constants import REGEX_AST_FILE, REGEX_PRIVKEY_FILE
from whispers.core.utils import global_exception_handler, is_static, strip_string
from whispers.models.appconfig import AppConfig
from whispers.models.pair import KeyValuePair


def make_pairs(config: AppConfig, file: Path) -> Optional[Iterator[KeyValuePair]]:
    """Generates KeyValuePair objects by parsing given file"""
    try:
        if not file.exists():
            return None

        if not file.is_file():
            return None

    except Exception:  # pragma: no cover
        global_exception_handler(file.as_posix(), "make_pairs()")
        return None

    # First, return file name to check if it is a sensitive file
    pair = KeyValuePair("file", file.as_posix())
    if filter_included(config, pair):
        yield tag_file(file, pair)

    # Second, attempt to parse the file with a plugin
    plugin = load_plugin(file, config.ast)

    logging.debug(f"make_pairs '{plugin}' for '{file}'")

    if not plugin:
        return None

    pairs = plugin().pairs(file)
    static = filter(None, map(filter_static, pairs))
    included = filter(None, map(lambda pair: filter_included(config, pair), static))
    tagged = map(lambda pair: tag_file(file, pair), included)

    try:
        yield from tagged

    except Exception:  # pragma: no cover
        global_exception_handler(file.as_posix(), "make_pairs()")
        return None


def tag_file(file: Path, pair: KeyValuePair) -> KeyValuePair:
    """Add pair file path"""
    pair.file = file.as_posix()
    return pair


def filter_included(config: AppConfig, pair: KeyValuePair) -> Optional[KeyValuePair]:
    """Check if pair should be included based on config"""
    if config.exclude.keys:
        for key in pair.keypath:
            if config.exclude.keys.match(str(key)):
                logging.debug(f"filter_included excluded key '{key}'")
                return None  # Excluded key

    if config.exclude.values:
        if config.exclude.values.match(pair.value):
            logging.debug(f"filter_included excluded value '{pair.value}'")
            return None  # Excluded value

    logging.debug(f"filter_included included pair '{pair}'")
    return pair  # Included value


def filter_static(pair: KeyValuePair) -> Optional[KeyValuePair]:
    """Check if pair contains hardcoded static values"""
    pair.key = strip_string(pair.key)
    pair.value = strip_string(pair.value)

    if not is_static(pair.key, pair.value):
        logging.debug(f"filter_static excluded value '{pair.value}'")
        return None  # Dynamic value

    logging.debug(f"filter_static included value '{pair.value}'")
    return pair  # Static value


def load_plugin(file: Path, ast: bool = False) -> Optional[object]:
    """
    Loads the correct plugin for a given file.
    Optional `ast` param enables/disables Semgrep.
    Returns None if no plugin found.
    """
    file_name = file.name.lower()

    logging.debug(f"load_plugin: ast:{ast} file:{file}")

    if file.suffix.lower() in [".dist", ".template"]:
        filetype = file.stem.split(".")[-1].lower()
    else:
        filetype = file_name.split(".")[-1]

    if filetype in ["yaml", "yml"]:
        from whispers.plugins.yml import Yml

        return Yml

    elif filetype == "json":
        from whispers.plugins.json import Json

        return Json

    elif filetype == "xml":
        from whispers.plugins.xml import Xml

        return Xml

    elif filetype.startswith("npmrc"):
        from whispers.plugins.npmrc import Npmrc

        return Npmrc

    elif filetype.startswith("pypirc"):
        from whispers.plugins.pypirc import Pypirc

        return Pypirc

    elif file_name == "pip.conf":
        from whispers.plugins.pip import Pip

        return Pip

    elif file_name == "build.gradle":
        from whispers.plugins.gradle import Gradle

        return Gradle

    elif filetype in ["conf", "cfg", "cnf", "config", "ini", "credentials", "s3cfg"]:
        from whispers.plugins.config import Config

        return Config

    elif filetype == "properties":
        from whispers.plugins.jproperties import Jproperties

        return Jproperties

    elif filetype.startswith(("sh", "bash", "zsh", "env")) or file_name == "environment":
        from whispers.plugins.shell import Shell

        return Shell

    elif "dockerfile" in file_name:
        from whispers.plugins.dockerfile import Dockerfile

        return Dockerfile

    elif filetype == "dockercfg":
        from whispers.plugins.dockercfg import Dockercfg

        return Dockercfg

    elif filetype.startswith("htpasswd"):
        from whispers.plugins.htpasswd import Htpasswd

        return Htpasswd

    elif filetype == "txt":
        from whispers.plugins.plaintext import Plaintext

        return Plaintext

    elif filetype.startswith("htm"):
        from whispers.plugins.html import Html

        return Html

    elif filetype == "exs":
        from whispers.plugins.elixir import Elixir

        return Elixir

    elif REGEX_PRIVKEY_FILE.match(filetype):
        from whispers.plugins.plaintext import Plaintext

        return Plaintext

    elif ast and REGEX_AST_FILE.match(filetype):
        from whispers.plugins.semgrep import Semgrep

        return Semgrep

    return None
