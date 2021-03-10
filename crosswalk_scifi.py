# CSV creation and writing
import os
from pathlib import Path
import csv
# REGEX for formatting/clean-up
import re

# Third party libraries
# MARC processing/extraction
import pymarc
from pymarc import MARCReader
from pymarc import marc8_to_unicode

# Custom local libraries
import cleanup_functions as cleanup


# Start
def process_marc(extract_from=None, save_name=None):
    if save_name is None or save_name == "":
        save_name = "output_mapping_maps.csv"

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
            dict_csv_fields = {}

            dict_csv_fields = extract_fields(record)

            dictionary_to_csv(dict_data=dict_csv_fields, output_name=save_name)


# Write contents to CSV file
def dictionary_to_csv(dict_data=None, output_name=None):
    # Assign CSV output name
    if output_name is None:
    # if not output_name:
        csv_file = 'csv_export.csv'
    else:
        # Ensure '.csv' is appended to the filename
        if not output_name[-4:] == '.csv':
            csv_file = output_name + '.csv'
        else:
            csv_file = output_name
    

    # Check if the file already exists, if no, add in HEADERS
    if not os.path.isfile(csv_file):
        with open(csv_file, mode='w', encoding='utf-8', newline='') as csvfile:
            field_names = dict_data.keys()
            writer = csv.DictWriter(csvfile, fieldnames=field_names, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

            # Write to csv file HEADERS
            writer.writeheader()

    # Append/add new row of data to file
    with open(csv_file, mode='a', encoding='utf-8', newline='') as csvfile:
        field_names = dict_data.keys()
        writer = csv.DictWriter(csvfile, fieldnames=field_names, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        writer.writerow(dict_data)


# Store record fields in a Dictionary while processing
def extract_fields(record=None):
    dict_map_fields = {}

    dict_map_fields['filename'] = process_field(record=record,
        dict_fields_subs={'001': []},
        dict_field_first_indicators={},
        dict_field_second_indicators={},
        dict_subfield_cleanup={},
        subfield_delimiter=' ',
        field_delimiter='||',)

    dict_map_fields['dc.creator'] = process_field(record=record,
        dict_fields_subs={'100': ['a','q','d'], '110': ['a','b']},
        dict_field_first_indicators={},
        dict_field_second_indicators={},
        dict_subfield_cleanup={'100': ['remove trailing period'], '110': ['remove trailing period']},
        subfield_delimiter=' ',
        field_delimiter='||',)

    dict_map_fields['dc.title'] = process_field(record=record,
        dict_fields_subs={'245': ['a','b']},
        dict_field_first_indicators={'245': []},
        dict_field_second_indicators={'245': []},
        dict_subfield_cleanup={'245': ['remove trailing period']},
        subfield_delimiter=' ',
        field_delimiter='||',)
    
    dict_map_fields['dc.edition'] = process_field(record=record,
        dict_fields_subs={'250': ['a','b']},
        dict_field_first_indicators={},
        dict_field_second_indicators={},
        dict_subfield_cleanup={'250': ['remove trailing period']},
        subfield_delimiter=' ',
        field_delimiter='||',)
    
    dict_map_fields['dc.publisher'] = process_field(record=record,
        dict_fields_subs={'260': ['b'], '264': ['b']},
        dict_field_first_indicators={},
        dict_field_second_indicators={},
        dict_subfield_cleanup={'260': ['remove trailing period'], '264': ['remove trailing period']},
        subfield_delimiter=' ',
        field_delimiter='||',)
    
    dict_map_fields['dc.date'] = process_field(record=record,
        dict_fields_subs={'260': ['c'], '264': ['c']},
        dict_field_first_indicators={},
        dict_field_second_indicators={},
        dict_subfield_cleanup={'260': ['remove trailing period'], '264': ['remove trailing period']},
        subfield_delimiter=' ',
        field_delimiter='||',)
    
    dict_map_fields['dc.date'] = process_field(record=record,
        dict_fields_subs={'260': ['c'], '264': ['c']},
        dict_field_first_indicators={},
        dict_field_second_indicators={},
        dict_subfield_cleanup={'260': ['remove trailing period'], '264': ['remove trailing period']},
        subfield_delimiter=' ',
        field_delimiter='||',)

    # {LC subject headings}
    dict_map_fields['dc.headings_lc'] = process_field(record=record,
        dict_fields_subs={'600': ['a','b','c','v'], '648': ['a','b','c','v'],'650': ['a','b','c','v'],'651': ['a','b','c','v'],'653': ['a','b','c','v'],'655': ['a','b','c','v']},
        dict_field_first_indicators={'600': ['0','1','2','3'],'648': ['0','1','2','3'],'650': ['0','1','2','3'],'651': ['0','1','2','3'],'653': ['0','1','2','3'],'655': ['0','1','2','3']},
        dict_field_second_indicators={'600': ['1','2','3','4','5','6','7'],'648': ['1','2','3','4','5','6','7'],'650': ['1','2','3','4','5','6','7'],'651': ['1','2','3','4','5','6','7'],'653': ['1','2','3','4','5','6','7'],'655': ['1','2','3','4','5','6','7'],},
        dict_subfield_cleanup={'600': ['remove trailing period'], '648': ['remove trailing period'], '650': ['remove trailing period'], '651': ['remove trailing period'], '653': ['remove trailing period'], '655': ['remove trailing period']},
        subfield_delimiter='--',
        field_delimiter='||',)
    # {FAST and lcgft headings}
    dict_map_fields['dc.headings_fast'] = process_field_heading(record=record,
        dict_fields_subs={'600': ['a','b','c','v'], '648': ['a','b','c','v'],'650': ['a','b','c','v'],'651': ['a','b','c','v'],'653': ['a','b','c','v'],'655': ['a','b','c','v']},
        dict_field_first_indicators={'600': ['0','1','2','3'],'648': ['0','1','2','3'],'650': ['0','1','2','3'],'651': ['0','1','2','3'],'653': ['0','1','2','3'],'655': ['0','1','2','3']},
        dict_field_second_indicators={'600': ['0','1','2','3','4','5','6'],'648': ['0','1','2','3','4','5','6'],'650': ['0','1','2','3','4','5','6'],'651': ['0','1','2','3','4','5','6'],'653': ['0','1','2','3','4','5','6'],'655': ['0','1','2','3','4','5','6']},
        dict_subfield_cleanup={'600': ['remove trailing period'], '648': ['remove trailing period'], '650': ['remove trailing period'], '651': ['remove trailing period'], '653': ['remove trailing period'], '655': ['remove trailing period']},
        subfield_delimiter='--',
        field_delimiter='||',)

    dict_map_fields['dc.type'] = process_field(record=record,
        dict_fields_subs={'336': ['a']},
        dict_field_first_indicators={},
        dict_field_second_indicators={},
        dict_subfield_cleanup={'336': ['remove trailing period']},
        subfield_delimiter=' ',
        field_delimiter='||',)
    
    return dict_map_fields


# Test template.
def process_field(
        record=None,
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
            
            # Determine if requested field is a data field. Will be processed differently.
            field_data = ''
            try:
                field_data = f.data
            except:
                pass
            
            if field_data != '':
                print("There is a data field.")
                
                # Assign the return string to be the field's data string.
                return_str = field_data
                
                # Data field is finished processing. Return value and don't continue.
                return return_str

            # If not a data field, continue process.

            ls_subfields = []

            # Filter on indicator.
            # Default for inidicators.
            indicator1 = ''
            indicator2 = ''

            # If indicator is blank or missing, standardize to "none".
            try:
                indicator1 = f.indicator1

                if indicator1 is None or indicator1 == ' ':
                    print(str(f.tag) + " ind1 is NONE.")
                    indicator1 = 'none'
                else:
                    indicator1 = f.indicator1
            except:
                indicator1 = 'none'
            
            try:
                indicator2 = f.indicator2

                if indicator2 is None or indicator2 == ' ':
                    print(str(f.tag) + " ind2 is NONE.")
                    indicator2 = 'none'
                else:
                    indicator2 = f.indicator2
            except:
                indicator2 = 'none'
            
            # Check if any of the indicators match ones to exclude.
            try:
                if indicator1 in dict_field_first_indicators.get(f.tag):
                    continue
            except:
                pass

            try:
                if indicator2 in dict_field_second_indicators.get(f.tag):
                    continue
            except:
                pass
            # if indicator1 in dict_field_first_indicators.get(f.tag) or indicator2 in dict_field_second_indicators.get(f.tag):
            #     # Stop processing this field, Skip and continue to next.
            #     continue
            
            # Continue working on field, assuming it has approved indicators.
            ls_sub_letters = dict_fields_subs.get(f.tag)
            print("sub letters are: " + str(ls_sub_letters))

            # Get subfields.
            ls_subfields = f.get_subfields(*ls_sub_letters)

            # Cleanup -- for each subfield.
            for index, subfield in enumerate(ls_subfields):
                str_subfield = ''

                # Default cleanup, converting to string and trimming white space.
                str_subfield = cleanup.str_convert_trimmed(subfield)

                # Run requested cleanup operations.
                for c in dict_subfield_cleanup.get(f.tag):
                    # Run the cleanup operations:
                    if c == "remove trailing period":
                        str_subfield = cleanup.remove_trailing_period(str_subfield)
                    if c == "remove trailing punctuation":
                        str_subfield = cleanup.remove_trailing_punctuation(str_subfield)
                
                # Update the value in the list.
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


# Test template.
def process_field_heading(
        record=None,
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
            
            # Determine if requested field is a data field. Will be processed differently.
            field_data = ''
            try:
                field_data = f.data
            except:
                pass
            
            if field_data != '':
                print("There is a data field.")
                
                # Assign the return string to be the field's data string.
                return_str = field_data
                
                # Data field is finished processing. Return value and don't continue.
                return return_str

            # If not a data field, continue process.

            ls_subfields = []

            # Filter on indicator.
            # Default for inidicators.
            indicator1 = ''
            indicator2 = ''

            # If indicator is blank or missing, standardize to "none".
            try:
                indicator1 = f.indicator1

                if indicator1 is None or indicator1 == ' ':
                    print(str(f.tag) + " ind1 is NONE.")
                    indicator1 = 'none'
                else:
                    indicator1 = f.indicator1
            except:
                indicator1 = 'none'
            
            try:
                indicator2 = f.indicator2

                if indicator2 is None or indicator2 == ' ':
                    print(str(f.tag) + " ind2 is NONE.")
                    indicator2 = 'none'
                else:
                    indicator2 = f.indicator2
            except:
                indicator2 = 'none'
            
            # # Check if any of the indicators match ones to exclude.
            try:
                if indicator1 in dict_field_first_indicators.get(f.tag):
                    continue
            except:
                pass

            try:
                if indicator2 in dict_field_second_indicators.get(f.tag):
                    continue
            except:
                pass
            
            # Continue working on field, assuming it has approved indicators.
            ls_sub_letters = dict_fields_subs.get(f.tag)
            print("sub letters are: " + str(ls_sub_letters))

            # Check if $2 is one of the approved.
            fast_lcgft = ''
            fast_lcgft = f.get_subfields('2')
            if fast_lcgft:
                fast_lcgft = fast_lcgft[0]
                fast_lcgft = fast_lcgft.strip()
                fast_lcgft = fast_lcgft.lower()
            if fast_lcgft == 'fast' or fast_lcgft == 'lcgft':
                pass # Pass this test and resume.
            else:
                continue # Continue to the next field.

            # Get subfields.
            ls_subfields = f.get_subfields(*ls_sub_letters)

            # Cleanup -- for each subfield.
            for index, subfield in enumerate(ls_subfields):
                str_subfield = ''

                # Default cleanup, converting to string and trimming white space.
                str_subfield = cleanup.str_convert_trimmed(subfield)

                # Run requested cleanup operations.
                for c in dict_subfield_cleanup.get(f.tag):
                    # Run the cleanup operations:
                    if c == "remove trailing period":
                        str_subfield = cleanup.remove_trailing_period(str_subfield)
                    if c == "remove trailing punctuation":
                        str_subfield = cleanup.remove_trailing_punctuation(str_subfield)
                
                # Update the value in the list.
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