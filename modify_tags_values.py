import os
import xml.etree.ElementTree as ET

directory = "/Users/ausoto/code/na-salesforce/force-app/main/default/objects/ContactArchive__c/fields"
nameSpace = "http://soap.sforce.com/2006/04/metadata"
ET.register_namespace("", nameSpace)
for _root, dirs, files in os.walk(directory):
    for field in files:
        filePath = directory + "/" + field
        _tree = ET.parse(filePath)
        _root = _tree.getroot()
        for fieldAttribute in _root:
            # select tagName
            xmlTagName = fieldAttribute.tag[41 : len(fieldAttribute.tag)]

            ## updates trackhistory tag to false

            if xmlTagName == "trackHistory" and fieldAttribute.text == "true":
                fieldAttribute.text = "false"
                print(f"File {field} has been updated trackHistory to false")
                # save
                _tree.write(filePath, "UTF-8", True, nameSpace)

            ## updates type tag to text when it's a lookup

            if xmlTagName == "type" and fieldAttribute.text == "Lookup":
                fieldAttribute.text = "Text"
                print(
                    f"File {fieldAttribute.text} has been updated Lookup to Text at {field}"
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
                    print(f"<length> of 255 has been added to {field}")
                    # save
                    _tree.write(filePath, "UTF-8", True, nameSpace)

            ## deletes tags from lookup

            if (
                xmlTagName == "relationshipLabel"
                or xmlTagName == "deleteConstraint"
                or xmlTagName == "referenceTo"
                or xmlTagName == "relationshipName"
                or xmlTagName == "lookupFilter"
            ):
                _root.remove(fieldAttribute)
                print(f"<{xmlTagName}> attribute has been deleted at {field}")
                _tree.write(filePath, "UTF-8", True, nameSpace)

        # save
        _tree.write(filePath, "UTF-8", True, nameSpace)

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
