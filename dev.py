# Custom
import cleanup_functions as cleanup

# Third party libraries
# MARC processing/extraction
import pymarc
from pymarc import MARCReader
from pymarc import marc8_to_unicode

# CSV creation and writing
import os
from pathlib import Path
import csv

def start():
    extract_from = r"./downloads/2020-11-10_Maps_export.mrc"

    # Check if the path is surrounded by quotes (default in Windows "Copy Path" option)
    if extract_from:
        if extract_from[0]=='"' and extract_from[-1]=='"':
            # remove first and last quote
            extract_from = extract_from[1:-1]
        # Convert the string to a Path
        extract_from = Path(extract_from)

    # Open File
    with open(extract_from, 'rb') as mf:
        reader = pymarc.MARCReader(mf, to_unicode=True, force_utf8=True)
        
        # Loop through file
        for record in reader:
            # print(record)
            dict_csv_fields = {}

            dict_csv_fields = extract_fields(record)


def extract_fields(record):
    dict_map_fields = {}

    dict_map_fields['dc.subject'] = get_dc_subject_str(record)

    return dict_map_fields


def get_dc_subject_str(record):
    str_results = ""

    dict_fields_subs = {'600':['a','b','v','x','y','z'], '610':['a','b','v','x','y','z'], '650':['a','b','v','x','y','z']}
    dict_field_first_indicators = {'600': ['none','0','1','3'], '610': ['none','0','1','3'],'650': ['none','0','1','3']}
    dict_field_second_indicators = {'600': ['0','1'], '610': ['0','1'], '650': ['0','1']}
    dict_subfield_cleanup = {'600': ['remove trailing period'], '610': ['remove trailing period'], '650': ['remove trailing period']}
    subfield_delimiter = '--'
    field_delimiter = '||'

    str_results = process_field(record=record,
        dict_fields_subs=dict_fields_subs,
        dict_field_first_indicators=dict_field_first_indicators,
        dict_field_second_indicators=dict_field_second_indicators,
        dict_subfield_cleanup=dict_subfield_cleanup,
        subfield_delimiter=subfield_delimiter,
        field_delimiter=field_delimiter)


    # print(str_results)
    return str_results


def process_field(record=None,
    dict_fields_subs={},
    dict_field_first_indicators={},
    dict_field_second_indicators={},
    dict_subfield_cleanup={},
    subfield_delimiter=' ',
    field_delimiter='||',
    ):
    
    # Default output variable.
    return_str = ''
    # Get fields based on field passed as keys in dict.
    ls_fields = []
    # ls_results
    ls_results = []

    for k in dict_fields_subs.keys():

        # Check if field is present.
        if record.get_fields(k):
            print("list is not empty")
            ls_fields.extend(record.get_fields(k))
    
    print("fields list is: " + str(ls_fields))
    
    # Get and process subfield data.
    for f in ls_fields:
        ls_subfields = []

        # Filter on indicator
        exclude = False
        indicator1 = ''
        indicator2 = ''

        if f.indicator1 is None or f.indicator1 == ' ':
            print(str(f.tag) + " ind1 is NONE.")
            indicator1 = 'none'
        else:
            indicator1 = f.indicator1

        if f.indicator2 is None or f.indicator2 == ' ':
            print(str(f.tag) + " ind2 is NONE.")
            indicator2 = 'none'
        else:
            indicator2 = f.indicator2
        
        if indicator1 not in dict_field_first_indicators.get(f.tag) or indicator2 not in dict_field_second_indicators.get(f.tag):
            # Skip and try next field.
            continue
        
        # Continue working on field assuming it has approved indicators.
        ls_sub_letters = dict_fields_subs.get(f.tag)
        print("sub letters are: " + str(ls_sub_letters))
        



        # # Only add subfield if there is a value.
        # for s in ls_sub_letters:
        #     print(s)
            
        #     # If there is a value, add it to the list.
        #     if f.get_subfields(s):
        #         ls_subfields.extend(f.get_subfields(s))
        ls_subfields = f.get_subfields(*ls_sub_letters)





        
        # Cleanup -- for each subfield.
        for index, subfield in enumerate(ls_subfields):
            str_subfield = ""

            # Default cleanup, converting to string and trimming white space.
            str_subfield = cleanup.str_convert_trimmed(subfield)

            # Run requested cleanup operations.
            for c in dict_subfield_cleanup.get(f.tag):
                # Run the cleanup operations:
                if c == "remove trailing period":
                    str_subfield = cleanup.remove_trailing_period(str_subfield)
            
            ls_subfields[index] = str_subfield
        
        # Cleanup -- remove duplicates and remove any empty.
        ls_subfields = cleanup.list_remove_duplicates(ls_subfields)
        ls_subfields = cleanup.list_remove_empty(ls_subfields)

        # Add if results left:
        # Tie together subfields with subfield delimiter.
        if len(ls_subfields) > 0:
            ls_results.append(str(subfield_delimiter).join(ls_subfields))
        
    # Cleanup -- remove duplicates and remove empty.
    ls_results = cleanup.list_remove_duplicates(ls_results)
    ls_results = cleanup.list_remove_empty(ls_results)

    # Tie together with field delimiter.
    if len(ls_results) > 0:
        return_str = str(field_delimiter).join(ls_results)

    return return_str




if __name__ == "__main__":
    start()