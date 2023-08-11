import os
import shutil

def searchContent(archive, searchItems):
    id_list = []
    for folder in archive.folders():
        if folder.get_number_of_sub_messages() != 0:
            for message in folder.sub_messages:
                subject = str(message.subject)
                body = str(message.plain_text_body)
                content = subject + body
                for item in searchItems:
                    if item.casefold() in content.casefold():
                        id_list.append(message.identifier)
    return id_list


def searchHeaders(archive, searchItems):
    id_list = []
    for folder in archive.folders():
        if folder.get_number_of_sub_messages() != 0:
            for message in folder.sub_messages:
                header = str(message.transport_headers)
                for item in searchItems:
                    if item.casefold() in header.casefold():
                        id_list.append(message.identifier)
    return id_list

def moveToFolders(backupName):

    # Specify the path to the directory containing folders and files
    directory_path = backupName.rsplit(".", 1)[0] + "/"

    # Iterate through the folders
    for folder_name in os.listdir(directory_path):
        if folder_name.endswith("_attachments") and os.path.isdir(os.path.join(directory_path, folder_name)):
            num = folder_name.split("_")[0]
            eml_filename = f"{num}.eml"

            # Check if the corresponding ".eml" file exists
            if eml_filename in os.listdir(directory_path):
                source_path = os.path.join(directory_path, eml_filename)
                destination_folder = os.path.join(directory_path, folder_name)
                destination_path = os.path.join(destination_folder, eml_filename)

                # Move the ".eml" file to the respective folder
                shutil.move(source_path, destination_path)
                print(f"Moved {eml_filename} to {destination_folder}")

                # Rename the folder to remove "_attachments"
                new_folder_name = f"{num}"
                new_folder_path = os.path.join(directory_path, new_folder_name)
                os.rename(destination_folder, new_folder_path)
                print(f"Renamed folder {folder_name} to {new_folder_name}")
            else:
                print(f"File {eml_filename} not found for folder {folder_name}")