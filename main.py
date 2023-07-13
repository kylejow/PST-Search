#https://github.com/libratom/libratom
#https://github.com/libratom/libratom/tree/main/examples

from libratom.lib.pff import PffArchive
import json
from pathlib import Path
from tempfile import gettempdir
from libratom.cli.subcommands import emldump

filename = "backup.pst"
archive = PffArchive(filename)
searchItems = []
id_list = []

for folder in archive.folders():
    if folder.get_number_of_sub_messages() != 0:
        for message in folder.sub_messages:
            #print(message.identifier)
            subject = str((message.subject))
            body = archive.format_message(message)
            for item in searchItems:
                if item in subject or item in body:
                    #print("found in" + subject)
                    #print(archive.format_message(message))
                    #print(message.identifier)
                    id_list.append(message.identifier)

print(id_list)
id_list = list(dict.fromkeys(id_list))
print(id_list)

eml_export_input = [
    {
        "filename": filename,
        "id_list": id_list,
    },
]

# Write it to a file to pass to emldump()
json_file_path = Path(gettempdir()) / "eml_export_input.json"
with json_file_path.open(mode="w") as json_file:
    json.dump(eml_export_input, json_file)
status = emldump(out=Path.cwd(), location=Path.cwd(), src=json_file_path)
