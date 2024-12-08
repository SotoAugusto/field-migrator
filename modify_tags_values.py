# this script is used to modify the tags values of the fields in order to make them deployable
# the idea is to convertem to a read only field
# is supposed to be ran after move_fields.py
import os
import xml.etree.ElementTree as ET
list_folders_to_iterate = ["fields", "lookup", "managed_packaged", "standard"]
nameSpace = "http://soap.sforce.com/2006/04/metadata"
ET.register_namespace("", nameSpace)
start_directory = (
    "/Users/ausoto/code/na-salesforce/force-app/main/default/objects/ContactArchive__c/"
)

for root, dirs, files in os.walk(start_directory):
    current_folder_name = os.path.basename(root)
    # print("files: ", files)
    # print("dirs: ", dirs)
    # print("root: ", root)
    print("🚀current_folder_name: ", current_folder_name)

    if current_folder_name not in list_folders_to_iterate:
        print(f"❌Inside incorrect folder {current_folder_name} skipping...")
        continue

    #! iterate over field-meta.xml files
    for field in files:
        # ignore these files
        if field.__contains__(".object-meta.xml") or field.__contains__(".DS_Store"):
            # print skipped file
            print(field + " is skipped")
            continue

        # delete __c.field-meta.xml
        filename_without__c = field[:-18]

        # delete .field-meta.xml
        filename_without_extension = field[:-15]

        ## ! is standard field
        if (
            current_folder_name == "standard"
            and not filename_without_extension.__contains__("__c")
        ):

            new_filename_standard_with__c = (
                filename_without_extension + "__c.field-meta.xml"
            )
            os.rename(root + "/" + field, root + "/" + new_filename_standard_with__c)
            field = new_filename_standard_with__c
            print(
                f"🟠{field}'s name has been updated to {new_filename_standard_with__c}"
            )

        ## ! is managed_packaged
        if (
            filename_without__c.__contains__("__")
            and current_folder_name == "managed_packaged"
        ):
            one_underscore_field_name = filename_without__c.replace("__", "_")
            new_filename_managed_package = (
                one_underscore_field_name + "__c.field-meta.xml"
            )
            os.rename(
                root + "/" + field,
                root + "/" + new_filename_managed_package,
            )
            field = new_filename_managed_package
            print(
                f"🟠{field}'s name has been updated to {new_filename_managed_package}"
            )

        filePath = root + "/" + field
        # print(f"🟧 filePath to generate tree {filePath}")
        _tree = ET.parse(filePath)
        _root = _tree.getroot()

        #! iterate over the tag attributes of a file(field)
        for fieldAttribute in _root:

            # delete namespace to leave <tag> only
            xmlTagName = fieldAttribute.tag[41 : len(fieldAttribute.tag)]

            ##! is standard field
            # change fullname text to add __c
            if current_folder_name == "standard":
                # change fullname text to add __c
                if xmlTagName == "fullName" and not fieldAttribute.text.__contains__(
                    "__c"
                ):
                    fieldAttribute.text = field[:-15]

                # add label tag and value
                # find if label tag exists, returns None if it doesn't
                contains_label_tag = _root.find(
                    "{http://soap.sforce.com/2006/04/metadata}label"
                )
                if contains_label_tag is None:
                    label_tag = ET.SubElement(
                        _root, "{{{}}}{}".format(nameSpace, "label")
                    )
                    label_tag.text = field[:-15]

                    # Create a namespace map
                    nsmap = {"label": nameSpace}

                    # Serialize the XML with the namespace map
                    ET.tostring(_root, encoding="utf-8", xml_declaration=True)
                    print(f"🟤<label> of {label_tag.text} has been added to {field}")

                # if current_folder_name == "standard" and not _root.__contains__(type):
                # find if <type> tag exists, returns None if it doesn't
                contains_type_tag = _root.find(
                    "{http://soap.sforce.com/2006/04/metadata}type"
                )
                if contains_type_tag is None:
                    label_tag = ET.SubElement(
                        _root, "{{{}}}{}".format(nameSpace, "type")
                    )
                    label_tag.text = "Text"

                    # Create a namespace map
                    nsmap = {"label": nameSpace}

                    # Serialize the XML with the namespace map
                    ET.tostring(_root, encoding="utf-8", xml_declaration=True)
                    print(f"🟤<type> of {label_tag.text} has been added to {field}")

                    # append <length> tag and value of 255
                    length_tag = ET.SubElement(
                        _root, "{{{}}}{}".format(nameSpace, "length")
                    )
                    length_tag.text = "255"

                    # Create a namespace map
                    nsmap = {"length": nameSpace}

                    # Serialize the XML with the namespace map
                    ET.tostring(_root, encoding="utf-8", xml_declaration=True)
                    print(f"🟤<length> of 255 has been added to {field}")

            #! is managed_packaged
            # select tagName full name, take out __c, if it contains __ then change it to _
            if xmlTagName == "fullName" and fieldAttribute.text[:-3].__contains__("__"):
                fieldAttribute.text = field[:-15]
                print(
                    f"🟧<fullName> tag for manage_packaged field {field} has been updated to {fieldAttribute.text}"
                )
                # ? save file
                # _tree.write(filePath, "UTF-8", True, nameSpace)

            ##! trackhistory tag to false

            if xmlTagName == "trackHistory" and fieldAttribute.text == "true":
                fieldAttribute.text = "false"
                print(f"🟪File {field} has been updated trackHistory to false")
                # ? save
                # _tree.write(filePath, "UTF-8", True, nameSpace)

            ## ! Lookup convertion

            if xmlTagName == "type" and fieldAttribute.text == "Lookup":
                fieldAttribute.text = "Text"
                print(
                    f"🟫File {fieldAttribute.text} has been updated Lookup to Text at {field}"
                )

                # add length tag
                if not xmlTagName.__contains__("length"):
                    length_tag = ET.SubElement(
                        _root, "{{{}}}{}".format(nameSpace, "length")
                    )
                    length_tag.text = "255"

                    # Create a namespace map
                    nsmap = {"length": nameSpace}

                    # Serialize the XML with the namespace map
                    ET.tostring(_root, encoding="utf-8", xml_declaration=True)
                    print(f"🟤<length> of 255 has been added to {field}")
                    # ? save
                    # _tree.write(filePath, "UTF-8", True, nameSpace)

            ## deletes tags from lookup

            if (
                xmlTagName == "relationshipLabel"
                or xmlTagName == "deleteConstraint"
                or xmlTagName == "referenceTo"
                or xmlTagName == "relationshipName"
                or xmlTagName == "lookupFilter"
            ):
                _root.remove(fieldAttribute)
                print(f"⬜<{xmlTagName}> attribute has been deleted at {field}")
                # ? save
                # _tree.write(filePath, "UTF-8", True, nameSpace)

        # ? save file after all changes
        _tree.write(filePath, "UTF-8", True, nameSpace)

## formula will not be migrated

# if xmlTagName == 'formula':
#     _root.remove(fieldAttribute)
#     print(
#         f"File {fieldAttribute} has been updated formula attribute deleted"
#     )


# if xmlTagName == 'formulaTreatBlankAs':
#     _root.remove(fieldAttribute)
#     print(
#         f"File {fieldAttribute} has been updated formulaTreatBlankAs attribute deleted"
#     )
