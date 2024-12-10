import xml.etree.ElementTree as ET
from pathlib import Path

def create_package_xml(fields_path):
    # Create the base package XML structure
    package = ET.Element("Package", xmlns="http://soap.sforce.com/2006/04/metadata")

    # Add CustomObject type for the Archive object
    types_obj = ET.SubElement(package, "types")
    members_obj = ET.SubElement(types_obj, "members")
    members_obj.text = "ContactArchive__c"
    name_obj = ET.SubElement(types_obj, "name")
    name_obj.text = "CustomObject"

    # Add CustomField type for all fields
    types = ET.SubElement(package, "types")

    # Add each field from the directory
    for field_file in Path(fields_path).glob("*.xml"):
        member = ET.SubElement(types, "members")
        member.text = f"ContactArchive__c.{field_file.stem}"

    name = ET.SubElement(types, "name")
    name.text = "CustomField"

    # Add API version
    version = ET.SubElement(package, "version")
    version.text = "58.0"

    # Save with proper formatting
    xml_str = ET.tostring(package)
    from xml.dom import minidom

    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="    ")

    with open("package.xml", "w") as f:
        f.write(pretty_xml)

# Use your actual path
fields_path = "/Users/ausoto/code/na-salesforce/force-app/main/default/objects/ContactArchive__c/fields"
create_package_xml(fields_path)
print("package.xml created!")
