import os

# Directory to save the field files
output_dir = "./salesforce_fields/"
os.makedirs(output_dir, exist_ok=True)

# Array of field names in camelCase
field_names = [
    "OtherStreet",
    "OtherCity",
    "OtherState",
    "OtherPostalCode",
    "OtherCountry",
    "OtherLatitude",
    "OtherLongitude",
    "OtherGeocodeAccuracy",
    "MailingStreet",
    "MailingCity",
    "MailingState",
    "MailingPostalCode",
    "MailingCountry",
    "MailingLatitude",
    "MailingLongitude",
    "MailingGeocodeAccuracy",
    "CreatedDate",
    "LastModifiedDate",
    "EmailBouncedReason",
    "EmailBouncedDate",
    "LastModifiedById",
    "AccountId",
    "RecordTypeId",
]


# Function to convert camelCase to label format
def to_label(camel_str):
    return (
        "".join([" " + char if char.isupper() else char for char in camel_str])
        .strip()
        .title()
    )


# Template for the XML content
xml_template = """<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>{field_name}__c</fullName>
    <label>{label_name}</label>
    <length>255</length>
    <trackHistory>false</trackHistory>
    <type>Text</type>
</CustomField>
"""

# Create a file for each field name
for field_name in field_names:
    label_name = to_label(field_name)
    file_content = xml_template.format(field_name=field_name, label_name=label_name)
    file_path = os.path.join(output_dir, f"{field_name}__c.field-meta.xml")
    with open(file_path, "w", encoding="UTF-8") as file:
        file.write(file_content)

print(f"Created {len(field_names)} field files in {output_dir}")
