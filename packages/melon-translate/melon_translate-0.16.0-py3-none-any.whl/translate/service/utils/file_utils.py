import glob
import json
from pathlib import Path

import polib
from django.conf import settings


def read_po_files(language_fixture) -> list:
    """Read po files."""
    translations_used = []
    # Construct the absolute fixture path
    fixture_dir = str(Path(__file__).parent.parent / f"tests/fixtures/{language_fixture}" / "**/*.po")

    po_files = [polib.pofile(po_file, encoding="utf-8") for po_file in glob.iglob(fixture_dir, recursive=True)]

    for po_file in po_files:
        for entry in po_file:
            if entry.msgid and entry.msgid not in translations_used:
                translations_used.append(entry.msgid)
            if entry.msgstr and entry.msgstr not in translations_used:
                translations_used.append(entry.msgstr)

    return translations_used


def read_json_files(directory, file_name) -> dict:
    """Read json files."""
    base_path = settings.BASE_DIR
    pattern = f"**/{directory}/{file_name}.json"
    file_path = next(base_path.glob(pattern), None)

    if file_path is None:
        raise FileNotFoundError(f"File not found for pattern: {pattern}")

    # Load the JSON data from the found file
    with open(file_path, "r", encoding="utf-8") as file:
        translations_data_used = json.load(file)

    return translations_data_used
