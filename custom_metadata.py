import pandas as pd
import os
from lxml import etree

# Load Excel sheet
excel_file = "ONDL-5861_Custom_Metadata_Mapping(Managed).xlsx"
output_dir = "output_xml_metadata"  # Directory to save XML files
os.makedirs(output_dir, exist_ok=True)

# Read data
data = pd.read_excel(excel_file)

# Namespace definitions
NSMAP = {
    None: "http://soap.sforce.com/2006/04/metadata",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xsd": "http://www.w3.org/2001/XMLSchema",
}

# Generate XML for each row
for _, row in data.iterrows():
    root = etree.Element("CustomMetadata", nsmap=NSMAP)

    # Add label
    label_elem = etree.SubElement(root, "label")
    label_elem.text = str(row["Label"])

    # Add protected flag
    protected_elem = etree.SubElement(root, "protected")
    protected_elem.text = "false"

    # Add values
    values = [
        ("DoNotMoveFlag__c", "xsd:boolean", "false"),
        ("Source_Field__c", "xsd:string", row["Source Field"]),
        ("Source_SObject__c", "xsd:string", row["Source SObject"]),
        ("Target_Field__c", "xsd:string", row["Target Field"]),
        ("Target_SObject__c", "xsd:string", row["Target SObject"]),
    ]

    for field, xsi_type, value in values:
        values_elem = etree.SubElement(root, "values")
        field_elem = etree.SubElement(values_elem, "field")
        field_elem.text = field

        value_elem = etree.SubElement(values_elem, "value")
        value_elem.set("{http://www.w3.org/2001/XMLSchema-instance}type", xsi_type)
        value_elem.text = str(value)

    # Save XML to file
    file_name = (
        f"Duplication_Field_Mapping.{row['Duplication Field Mapping Name']}.md-meta.xml"
    )
    file_path = os.path.join(output_dir, file_name)
    with open(file_path, "wb") as f:
        f.write(
            etree.tostring(
                root, pretty_print=True, xml_declaration=True, encoding="UTF-8"
            )
        )

print(f"XML files have been saved to {output_dir}.")
