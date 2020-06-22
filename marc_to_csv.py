import os
from pathlib import Path
import csv
import pymarc
from pymarc import MARCReader
from pymarc import marc8_to_unicode


def encoding_conversion_test(string_to_test=None):
    results = None

    if string_to_test:
        encoded_string = string_to_test.encode('utf-8')

        decode_encoded = encoded_string.decode('utf-8')

        if string_to_test == decode_encoded:
            results = 'Pass encode/decode'
        else:
            results = 'Fail encode/decode'

    return results


def write_csv_from_marc(filename, title, abstract, provided_csv=None):
    if not provided_csv:
        provided_csv = 'csv_export.csv'

    if not os.path.isfile(provided_csv):

        with open(provided_csv, mode='w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

            # Write to csv file HEADERS
            writer.writerow([
                'filename',
                'dc.title',
                'dc.description.abstract',
                ])
    

    with open(provided_csv, mode='a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow([
            str(filename),
            str(title),
            str(abstract)
            ])


def read_marc_file(binary_mrc_file=None):
    
    # Check if the path is surrounded by quotes (default in Windows "Copy Path" option)
    if binary_mrc_file:
        if binary_mrc_file[0]=='"' and binary_mrc_file[-1]=='"':
            # remove first and last quote
            binary_mrc_file = binary_mrc_file[1:-1]
        # Convert the string to a Path
        binary_mrc_file = Path(binary_mrc_file)

    # Open File
    with open(binary_mrc_file.absolute(), 'rb') as mf:
        reader = MARCReader(mf, to_unicode=True, force_utf8=True)
        
        # Loop through file
        for record in reader:
            # Get FILENAME
            # File names are the '{BibID}.pdf' format
            archiveFileName = record['001'].data
            archiveFileName = archiveFileName + ".pdf"


            # Get TITLE
            if record['245']['a'] != None:
                # Get the 245 from MARC
                title245 = record['245']['a']


            # Get ABSTRACT
            abstract = None

            if record['520'] is not None:
                # Get the 520 from MARC
                abstract = record['520']['a']

            elif record['880'] is not None:
                # Get the 880 from MARC
                abstract = record['880']['a']

            else:
                abstract = "No abstract in 520$a or 880$a"

            
            # Test encode/decode of abstract
            encoding_issue = encoding_conversion_test(abstract)

            # Print to terminal to check
            print("Abstract Encoding Test: {0}".format(encoding_issue) + "\r\n" + title245)
            
            # Write extracted values into CSV file
            write_csv_from_marc(archiveFileName, title245, abstract)


# Get INPUT from user for {path to file}
input_file = input("Input the path and filename with extension to a Binary MARC file (*.bib, *.dat):")
# Run
read_marc_file(input_file)