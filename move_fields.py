import os
import shutil
import xml.etree.ElementTree as ET

# Define the paths
fields_folder = (
    "/Users/ausoto/code/na-salesforce/force-app/main/default/objects/ContactArchive__c/fields"
)
lookup_folder = os.path.join(os.path.dirname(fields_folder), "lookup")
formula_folder = os.path.join(os.path.dirname(fields_folder), "formula")
managed_packaged_folder = os.path.join(os.path.dirname(fields_folder), "managed_packaged")
standard_folder = os.path.join(os.path.dirname(fields_folder), "standard")

report_file = "moved_files_report.txt"

# Create the formula folder if it doesn't exist
if not os.path.exists(formula_folder):
    os.makedirs(formula_folder)

if not os.path.exists(lookup_folder):
    os.makedirs(lookup_folder)

if not os.path.exists(managed_packaged_folder):
    os.makedirs(managed_packaged_folder)

if not os.path.exists(standard_folder):
    os.makedirs(standard_folder)

# Initialize the report content
report_content = []

# Initialize counters
total_files = 0
moved_formula_files = 0
moved_lookup_files = 0
moved_managed_packaged_files = 0
moved_standard_files = 0


# Iterate over all files in the fields folder
for filename in os.listdir(fields_folder):
    if filename.endswith(".xml"):
        total_files += 1
        file_path = os.path.join(fields_folder, filename)

        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # move formula

        # Check if the file contains a <formula> tag
        formula_tag = root.find("{http://soap.sforce.com/2006/04/metadata}formula")
        if formula_tag is not None:
            moved_formula_files += 1
            # Find the type of the field
            type_tag = root.find("{http://soap.sforce.com/2006/04/metadata}type")
            field_type = type_tag.text if type_tag is not None else "Unknown"

            # Move the file to the formula folder
            shutil.move(file_path, os.path.join(formula_folder, filename))

            # Add the file and its type to the report content
            report_content.append(f"{filename}, Formula ({field_type})")
            continue

        # move managed packaged

        # delete __c.field-meta.xml
        without_file_extension_c = filename[0:-18]
        if without_file_extension_c.__contains__('__'):
            moved_managed_packaged_files += 1
            #   Move the file to the formula folder
            shutil.move(file_path, os.path.join(managed_packaged_folder, filename))

            # Add the file and its type to the report content
            report_content.append(f"{filename}, Managed package")
            continue

        # move standard fields

        #delete .field-meta.xml
        without_file_extension = filename[0:-15]
        if not without_file_extension.__contains__("__c"):
            moved_standard_files += 1
            shutil.move(file_path, os.path.join(standard_folder, filename))
            # Add the file and its type to the report content
            report_content.append(f"{filename}, Standard")
            continue

        # Move lookup

        # Check if the file contains a <formula> tag
        # type_tag = root.find("{http://soap.sforce.com/2006/04/metadata}type")
        # if type_tag is not None and type_tag.text == "Lookup":
        #     moved_lookup_files += 1
        #     # Move the file to the formula folder
        #     shutil.move(file_path, os.path.join(lookup_folder, filename))

        #     # Add the file and its type to the report content
        #     report_content.append(f"{filename}, Lookup")
        #     continue

        # count custom?????


# Calculate the number of files that are not formula fields
non_formula_files = total_files - moved_formula_files
non_lookup_files = total_files - moved_lookup_files

custom_fields = total_files - (
    moved_formula_files
    + moved_lookup_files
    + moved_managed_packaged_files
    + moved_standard_files
)

# Write the report content to the report file
with open(report_file, "w") as f:
    f.write(f"Total number of field files: {total_files}\n")
    f.write(f"Total number of moved formula files: {moved_formula_files}\n")
    # f.write(f"Number of files that are not formula fields: {non_formula_files}\n")

    f.write(f"Total number of moved lookup files: {moved_lookup_files}\n")
    # f.write(f"Number of files that are not lookup fields: {non_lookup_files}\n")

    f.write(f"Total number of moved managed_packaged files: {moved_managed_packaged_files}\n")

    f.write(f"Total number of moved standard files: {moved_standard_files}\n")

    f.write(f"Total number of custom files: {custom_fields}\n")

    f.write("\nMoved Files:\n")
    for line in report_content:
        f.write(line + "\n")

# print(
#     f"Files containing <formula> tags have been moved to '{formula_folder}' and a report with statistics has been generated in '{report_file}'."
# )
# print(
#     f"Files containing <lookup> tags have been moved to '{lookup_folder}' and a report with statistics has been generated in '{report_file}'."
# )
print(
    f"A report with statistics has been generated in '{report_file}'."
)
