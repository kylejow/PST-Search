# https://github.com/libratom/libratom
# https://github.com/libratom/libratom/tree/main/examples

from libratom.lib.pff import PffArchive
import json
from pathlib import Path
from tempfile import gettempdir
from libratom.cli.subcommands import emldump
import search

with open("searchContent.txt", "r") as file:
    searchContent = file.readlines()
if len(searchContent) == 0:
    print("searchContent.txt is empty.\nUsage: Enter filename followed by search terms on newlines.")
    exit(0)

doSearchHeaders = False
with open("searchHeaders.txt", "r") as file:
    searchHeaders = file.readlines()
if len(searchHeaders) != 0:
    searchHeaders = [line.strip() for line in searchHeaders]
    doSearchHeaders = True

backupName = searchContent[0].strip()
searchItems = [line.strip() for line in searchContent[1:]]
id_list = []

try:
    archive = PffArchive(backupName)
except Exception as e:
    print("Cannot open file: " + backupName)
    print("Error message:", str(e))
    exit(0)

id_list = search.searchContent(archive, searchItems)

if doSearchHeaders:
    id_list_headers = search.searchHeaders(archive, searchHeaders)
    id_list = list(set(id_list).intersection(id_list_headers))
    # id_list += id_list_headers

eml_export_input = [
    {
        "filename": backupName,
        "id_list": id_list,
    },
]

# Write it to a file to pass to emldump()
json_file_path = Path(gettempdir()) / "eml_export_input.json"
with json_file_path.open(mode="w") as json_file:
    json.dump(eml_export_input, json_file)
status = emldump(out=Path.cwd(), location=Path.cwd(), src=json_file_path)
