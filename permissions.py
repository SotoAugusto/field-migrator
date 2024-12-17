import os
from lxml import etree

# Directory containing profile files
profiles_dir = "/Users/ausoto/code/na-salesforce/force-app/main/default/profiles/"

# Field mapping: Format {'Contact.FieldName': 'ContactArchive__c.CustomFieldName__c'}
# Automatically fallback to identical field names if not mapped
field_mapping = {
    "Contact.Account": "ContactArchive__c.Account__c",
    "Contact.CanAllowPortalSelfReg": "ContactArchive__c.CanAllowPortalSelfReg__c",
    "Contact.AssistantName": "ContactArchive__c.AssistantName__c",
    "Contact.AssistantPhone": "ContactArchive__c.AssistantPhone__c",
    "Contact.Birthdate": "ContactArchive__c.Birthdate__c",
    "Contact.Owner": "ContactArchive__c.Owner__c",
    "Contact.RecordType": "ContactArchive__c.RecordType__c",
    "Contact.CreatedBy": "ContactArchive__c.CreatedBy__c",
    "Contact.ContactSource": "ContactArchive__c.ContactSource__c",
    "Contact.Jigsaw": "ContactArchive__c.Jigsaw__c",
    "Contact.Department": "ContactArchive__c.Department__c",
    "Contact.Description": "ContactArchive__c.Description__c",
    "Contact.DoNotCall": "ContactArchive__c.DoNotCall__c",
    "Contact.Email": "ContactArchive__c.Email__c",
    "Contact.HasOptedOutOfEmail": "ContactArchive__c.HasOptedOutOfEmail__c",
    "Contact.Fax": "ContactArchive__c.Fax__c",
    "Contact.HasOptedOutOfFax": "ContactArchive__c.HasOptedOutOfFax__c",
    "Contact.Gender": "ContactArchive__c.Gender__c",
    "Contact.GenderIdentity": "ContactArchive__c.GenderIdentity__c",
    "Contact.HomePhone": "ContactArchive__c.HomePhone__c",
    "Contact.Individual": "ContactArchive__c.Individual__c",
    "Contact.LastModifiedBy": "ContactArchive__c.LastModifiedBy__c",
    "Contact.LastCURequestDate": "ContactArchive__c.LastCURequestDate__c",
    "Contact.LastCUUpdateDate": "ContactArchive__c.LastCUUpdateDate__c",
    "Contact.LeadSource": "ContactArchive__c.LeadSource__c",
    "Contact.MailingAddress": "ContactArchive__c.MailingAddress__c",
    "Contact.MobilePhone": "ContactArchive__c.MobilePhone__c",
    "Contact.Name": "ContactArchive__c.Name__c",
    "Contact.Salutation": "ContactArchive__c.Salutation__c",
    "Contact.FirstName": "ContactArchive__c.FirstName__c",
    "Contact.LastName": "ContactArchive__c.LastName__c",
    "Contact.OtherAddress": "ContactArchive__c.OtherAddress__c",
    "Contact.OtherPhone": "ContactArchive__c.OtherPhone__c",
    "Contact.Phone": "ContactArchive__c.Phone__c",
    "Contact.Pronouns": "ContactArchive__c.Pronouns__c",
    "Contact.ReportsTo": "ContactArchive__c.ReportsTo__c",
    "Contact.Title": "ContactArchive__c.Title__c",
    "Contact.CareMetxRxBv__Active__c": "ContactArchive__c.CareMetxRxBv_Active__c",
    "Contact.CareMetxRxBv__Gender__c": "ContactArchive__c.CareMetxRxBv_Gender__c",
    "Contact.CareMetxRxBv__Medical_Member_Id__c": "ContactArchive__c.CareMetxRxBv_Medical_Member_Id__c",
    "Contact.CareMetxRxBv__Medical_Payer_Name__c": "ContactArchive__c.CareMetxRxBv_Medical_Payer_Name__c",
    "Contact.CareMetxRxBv__Medical_Payer_Phone_Number__c": "ContactArchive__c.  CareMetxRxBv_Medical_Payer_Phone_Number__c",
    "Contact.CareMetxRxBv__NPI__c": "ContactArchive__c.CareMetxRxBv_NPI__c",
    "Contact.CareMetxRxBv__Patient_Drug_ID__c": "ContactArchive__c.CareMetxRxBv_Patient_Drug_ID__c",
    "Contact.CareMetxRxBv__Patient_Medicare_ID__c": "ContactArchive__c.CareMetxRxBv_Patient_Medicare_ID__c",
    "Contact.CareMetxRxBv__Patient_Payer_ID__c": "ContactArchive__c.CareMetxRxBv_Patient_Payer_ID__c",
    "Contact.CareMetxRxBv__Payer_Account__c": "ContactArchive__c.CareMetxRxBv_Payer_Account__c",
    "Contact.CareMetxRxBv__Practice_Location_Name__c": "ContactArchive__c.CareMetxRxBv_Practice_Location_Name__c",
    "Contact.CareMetxRxBv__Primary_HCP__c": "ContactArchive__c.CareMetxRxBv_Primary_HCP__c",
    "Contact.CareMetxRxBv__PrimaryHCP__c": "ContactArchive__c.CareMetxRxBv_PrimaryHCP__c",
    "Contact.CareMetxRxBv__TIN__c": "ContactArchive__c.CareMetxRxBv_TIN__c",
    "Contact.et4ae5__HasOptedOutOfMobile__c": "ContactArchive__c.et4ae5_HasOptedOutOfMobile__c",
    "Contact.et4ae5__Mobile_Country_Code__c": "ContactArchive__c.et4ae5_Mobile_Country_Code__c",
    "Contact.HealthCloudGA__ConditionStatus__c": "ContactArchive__c.HealthCloudGA_ConditionStatus__c",
    "Contact.HealthCloudGA__ConvertedReferrals__c": "ContactArchive__c.HealthCloudGA_ConvertedReferrals__c",
    "Contact.HealthCloudGA__CountryOfBirth__c": "ContactArchive__c.HealthCloudGA_CountryOfBirth__c",
    "Contact.HealthCloudGA__CreatedFromLead__c": "ContactArchive__c.HealthCloudGA_CreatedFromLead__c",
    "Contact.HealthCloudGA__DeceasedDate__c": "ContactArchive__c.HealthCloudGA_DeceasedDate__c",
    "Contact.HealthCloudGA__Gender__c": "ContactArchive__c.HealthCloudGA_Gender__c",
    "Contact.HealthCloudGA__IndividualType__c": "ContactArchive__c.HealthCloudGA_IndividualType__c",
    "Contact.HealthCloudGA__MedicalRecordNumber__c": "ContactArchive__c.HealthCloudGA_MedicalRecordNumber__c",
    "Contact.HealthCloudGA__Monitored_at_Home__c": "ContactArchive__c.HealthCloudGA_Monitored_at_Home__c",
    "Contact.HealthCloudGA__PreferredName__c": "ContactArchive__c.HealthCloudGA_PreferredName__c",
    "Contact.HealthCloudGA__PrimaryLanguage__c": "ContactArchive__c.HealthCloudGA_PrimaryLanguage__c",
    "Contact.HealthCloudGA__SecondaryLanguage__c": "ContactArchive__c.HealthCloudGA_SecondaryLanguage__c",
    "Contact.HealthCloudGA__SourceSystem__c": "ContactArchive__c.HealthCloudGA_SourceSystem__c",
    "Contact.HealthCloudGA__SourceSystemId__c": "ContactArchive__c.HealthCloudGA_SourceSystemId__c",
    "Contact.HealthCloudGA__StatusGroup__c": "ContactArchive__c.HealthCloudGA_StatusGroup__c",
    "Contact.HealthCloudGA__Testing_Status__c": "ContactArchive__c.HealthCloudGA_Testing_Status__c",
    "Contact.HealthCloudGA__TotalReferrals__c": "ContactArchive__c.HealthCloudGA_TotalReferrals__c",
    "Contact.lmsilt__Languages__c": "ContactArchive__c.lmsilt_Languages__c",
    "Contact.lmsilt__Level__c": "ContactArchive__c.lmsilt_Level__c",
    "Contact.mkto2__Acquisition_Date__c": "ContactArchive__c.mkto2_Acquisition_Date__c",
    "Contact.mkto2__Acquisition_Program__c": "ContactArchive__c.mkto2_Acquisition_Program__c",
    "Contact.mkto2__Acquisition_Program_Id__c": "ContactArchive__c.mkto2_Acquisition_Program_Id__c",
    "Contact.mkto2__Inferred_City__c": "ContactArchive__c.mkto2_Inferred_City__c",
    "Contact.mkto2__Inferred_Company__c": "ContactArchive__c.mkto2_Inferred_Company__c",
    "Contact.mkto2__Inferred_Country__c": "ContactArchive__c.mkto2_Inferred_Country__c",
    "Contact.mkto2__Inferred_Metropolitan_Area__c": "ContactArchive__c.mkto2_Inferred_Metropolitan_Area__c",
    "Contact.mkto2__Inferred_Phone_Area_Code__c": "ContactArchive__c.mkto2_Inferred_Phone_Area_Code__c",
    "Contact.mkto2__Inferred_Postal_Code__c": "ContactArchive__c.mkto2_Inferred_Postal_Code__c",
    "Contact.mkto2__Inferred_State_Region__c": "ContactArchive__c.mkto2_Inferred_State_Region__c",
    "Contact.mkto2__Lead_Score__c": "ContactArchive__c.mkto2_Lead_Score__c",
    "Contact.mkto2__Original_Referrer__c": "ContactArchive__c.mkto2_Original_Referrer__c",
    "Contact.mkto2__Original_Search_Engine__c": "ContactArchive__c.mkto2_Original_Search_Engine__c",
    "Contact.mkto2__Original_Search_Phrase__c": "ContactArchive__c.mkto2_Original_Search_Phrase__c",
    "Contact.mkto2__Original_Source_Info__c": "ContactArchive__c.mkto2_Original_Source_Info__c",
    "Contact.mkto2__Original_Source_Type__c": "ContactArchive__c.mkto2_Original_Source_Type__c",
}

# Loop through each profile file
for filename in os.listdir(profiles_dir):
    if filename.endswith(".profile-meta.xml"):
        file_path = os.path.join(profiles_dir, filename)

        # Parse the XML file
        parser = etree.XMLParser(remove_blank_text=False)
        tree = etree.parse(file_path, parser)
        root = tree.getroot()
        namespace = {"sf": "http://soap.sforce.com/2006/04/metadata"}

        modified = False

        # Find all readable field permissions for Contact using xpath
        contact_field_perms = root.xpath(
            './/sf:fieldPermissions[sf:field[starts-with(text(), "Contact.") and ../sf:readable="true"]]',
            namespaces=namespace,
        )
        if len(contact_field_perms) > 1:
            print(
                f"✅Found {len(contact_field_perms)} readable Contact field permissions in {file_path}."
            )
        else:
            print(
                f"❌Found {len(contact_field_perms)} readable Contact field permissions in {file_path}."
            )

        for field_perm in contact_field_perms:
            field_name_elem = field_perm.find("sf:field", namespaces=namespace)
            field_name = field_name_elem.text

            # Check if field has a mapping to ContactArchive
            archived_field_name = field_mapping.get(
                field_name, f"ContactArchive__c.{field_name.split('.')[1]}"
            )

            # Check if this field permission already exists
            existing_perm = root.xpath(
                f'.//sf:fieldPermissions[sf:field="{archived_field_name}"]',
                namespaces=namespace,
            )
            if not existing_perm:
                # Create a new fieldPermission element
                new_field_perm = etree.Element(
                    "{http://soap.sforce.com/2006/04/metadata}fieldPermissions"
                )
                field_elem = etree.SubElement(
                    new_field_perm, "{http://soap.sforce.com/2006/04/metadata}field"
                )
                readable_elem = etree.SubElement(
                    new_field_perm,
                    "{http://soap.sforce.com/2006/04/metadata}readable",
                )
                editable_elem = etree.SubElement(
                    new_field_perm,
                    "{http://soap.sforce.com/2006/04/metadata}editable",
                )

                # Copy permissions from Contact
                field_elem.text = archived_field_name
                readable_elem.text = "true"  # Already filtered by readable
                editable_elem.text = "false"

                # Format the new fieldPermission
                etree.indent(new_field_perm, space="    ")
                new_field_perm.tail = "\n"

                # Find the last fieldPermissions element and insert after it
                last_field_perm = root.xpath(
                    ".//sf:fieldPermissions[last()]", namespaces=namespace
                )[0]
                last_field_perm.addnext(new_field_perm)
                modified = True

        # Write changes if modified
        if modified:
            # Ensure the last element's tail has a newline
            if len(root) > 0:
                root[-1].tail = "\n"

            # Write the formatted XML back to the file
            with open(file_path, "wb") as f:
                tree.write(
                    f,
                    encoding="UTF-8",
                    xml_declaration=True,
                    method="xml",
                    pretty_print=True,  # Ensures proper indentation
                )
