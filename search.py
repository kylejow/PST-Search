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
