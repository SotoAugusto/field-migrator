import os
import xml.etree.ElementTree as ET

directory = "/Users/ausoto/code/na-salesforce/force-app/main/default/objects/ContactArchive__c/fields"
nameSpace = "http://soap.sforce.com/2006/04/metadata"
for _root, dirs, files in os.walk(directory):
    for field in files:
        filePath = directory + "/" + field
        _tree = ET.parse(filePath)
        _root = _tree.getroot()
        # attributesToUpdate = []
        for fieldAttribute in _root:
            # delete extension
            xmlTagName = fieldAttribute.tag[41 : len(fieldAttribute.tag)]

            ## updates trackhistory tag to false

            # if xmlTagName == "trackHistory":
            #     print(field)
            #     fieldAttribute.text = "false"
            #     print(f"File {field} has been updated trackHistory to false")
            # _tree.write(filePath, "UTF-8", True, nameSpace)

            ## updates type tag to text when it's a lookup

            if field.__contains__("Region__c"):
                if xmlTagName == "type" and fieldAttribute.text == "Lookup":
                    print(field)
                    fieldAttribute.text = "Text"
                    print(f"File {fieldAttribute.text} has been updated Lookup to Text")

                    custom_field = _root.find("CustomField", nameSpace)
                    custom_field = _root.find(
                    "{http://soap.sforce.com/2006/04/metadata}CustomField"
                    )
                    print('customfield',custom_field)
                    # Create a new element
                    print('_root',_root)
                    print("_tree", _tree)
                    print("field", field)

                    length_255 = ET.SubElement(_root,"length")
                    length_255.text = '255'
                    print('length_255',length_255)
                    print("length_255.tag", length_255.tag)
                    print("length_255.text", length_255.text)

                    is_length_255 = field.find.Element('isLength')
                    print(is_length_255)

                    # _root.append(length_255)
                    # _tree.SubElement(fieldAttribute, "length").text = "255"
                    # lenght_255 = makeelement("length": "255")¶
                    # fieldAttribute.append()
                    print(f"<length> of 255 has been added to {field}")

                #     _tree.write(filePath, "UTF-8", True, nameSpace)

                ## deletes tags from lookup

                # if (
                #     xmlTagName == "deleteConstraint"
                #     or xmlTagName == "relationshipLabel"
                #     or xmlTagName == "referenceTo"
                #     or xmlTagName == "relationshipName"
                # ):
                #     _root.remove(fieldAttribute)
                #     print(
                #         f"{fieldAttribute.tag} attribute has been deleted"
                #     )

## save file
        # _tree.write(filePath, "UTF-8", True, nameSpace)

## formula will not be migrated

# if xmlTagName == 'formula':
#     _root.remove(fieldAttribute)
#     print(
#         f"File {fieldAttribute} has been updated formula attribute deleted"
#     )
#     _tree.write(filePath, "UTF-8", True, nameSpace)

# if xmlTagName == 'formulaTreatBlankAs':
#     _root.remove(fieldAttribute)
#     print(
#         f"File {fieldAttribute} has been updated formulaTreatBlankAs attribute deleted"
#     )
#     _tree.write(filePath, "UTF-8", True, nameSpace)
