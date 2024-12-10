import os

# Directory to search
directory = "/Users/ausoto/code/na-salesforce/force-app/main/default/objects/Contact/fields"
# directory = "/Users/ausoto/code/na-salesforce/force-app/main/default/objects/ContactArchive__c/fields"

# Output file in the home directory
output_file = os.path.expanduser("~/code/field-migrator/sorted_filenames.txt")

# Find all files ending with 'field-meta.xml', remove that part, and save to the output file
filenames = []
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('field-meta.xml'):
            filenames.append(file.replace('.field-meta.xml', ''))

# Sort filenames alphabetically (case-insensitive)
filenames.sort(key=lambda s: s.lower())

# Write sorted filenames to the output file
with open(output_file, 'w') as f:
    for filename in filenames:
        f.write(f"{filename}\n")

print(f"Filenames saved to {output_file}")
