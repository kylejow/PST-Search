# https://github.com/libratom/libratom
# https://github.com/libratom/libratom/tree/main/examples

from libratom.lib.pff import PffArchive
import json
from pathlib import Path
from tempfile import gettempdir
from libratom.cli.subcommands import emldump


with open("main.txt", "r") as file:
    lines = file.readlines()

backupName = lines[0].strip()
searchItems = [line.strip() for line in lines[1:]]
id_list = []

try:
    archive = PffArchive(backupName)
except Exception as e:
    print("Cannot open file: " + backupName)
    print("Error message:", str(e))
    exit(0)

for folder in archive.folders():
    if folder.get_number_of_sub_messages() != 0:
        for message in folder.sub_messages:
            # print(message.identifier)
            subject = str(message.subject)
            body = archive.format_message(message)
            for item in searchItems:
                if item.casefold() in subject.casefold() or item.casefold() in body.casefold():
                    # print("found in" + subject)
                    # print(archive.format_message(message))
                    # print(message.identifier)
                    id_list.append(message.identifier)

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
