# 2020-10-07 3hrs
# 2020-01-12 3hrs

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

# CSV creation and writing
import os
from pathlib import Path
import csv
# # REGEX for formatting/clean-up
# import re

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

    dict_map_fields['filename'] = get_filename(record) # DONE
    dict_map_fields['dc.lcc'] = get_lcc(record) # DONE
    dict_map_fields['dc.subject.classification'] = get_dc_subject_classification(record) # DONE -None have
    dict_map_fields['dc.creator'] = get_dc_creator(record) # DONE
    dict_map_fields['dc.title[en]'] = get_dc_title(record) # DONE
    dict_map_fields['dc.title.alternative[en]'] = get_dc_title_alternative(record) # DONE
    dict_map_fields['dc.dc.coverage'] = get_dc_coverage(record) # DONE
    dict_map_fields['dc.date.issued'] = get_dc_date_issued(record) # DONE
    dict_map_fields['dc.date.created'] = get_dc_created(record) # TODO Needs follow up
    dict_map_fields['dc.publisher'] = get_dc_publisher(record) # DONE
    dict_map_fields['dc.format.extent[en]'] = get_dc_format_extent(record) # DONE
    dict_map_fields['dc.description[en]'] = get_dc_description(record) # DONE
    dict_map_fields['dc.subject.lcsh[en]'] = get_dc_subject_lcsh(record) # DONE
    dict_map_fields['dc.type'] = get_dc_type(record) # DONE
    dict_map_fields['dc.contributor'] = get_dc_contributor(record) # DONE
    dict_map_fields['dc.identifier.other'] = get_identifier_other(record) # DONE
    
    return dict_map_fields


# MARC: 001
# Should only be one
def get_filename(record):
    ls_001 = record.get_fields('001')

    ls_ctrl_number = []
    str_filename = ''

    # Get FILENAME
    for ctrl_number in ls_001:
        ls_ctrl_number.append(str(ctrl_number.data).strip())
    
    str_filename = "||".join(ls_ctrl_number)

    return str_filename


# MARC: 050$ab
# Add a space between the subfields
# *Field can be REPEATED in record
def get_lcc(record):
    
    ls_050 = record.get_fields('050')
    
    ls_LLC = []
    dc_LCC = ""

    # Loop over all found '050' fields
    for call_no in ls_050:

        # Get subfields a & b
        ls_050_subfields = call_no.get_subfields('a','b')

        # Field cleanup - remove leading or trailing spaces
        for index, sub in enumerate(ls_050_subfields):
            ls_050_subfields[index] = str(sub).strip()
        
        
        # Remove empty results
        ls_050_subfields = list(filter(None,ls_050_subfields))
        
        # Combine the subfields for the given 050 and add to list of found
        if len(ls_050_subfields) > 0:
            ls_LLC.append(" ".join(ls_050_subfields))
    
    # For all of the 050 found, string together with double pipes
    dc_LCC = "||".join(ls_LLC)
    
    return dc_LCC


# MARC: 099$aaa
def get_dc_subject_classification(record):
    
    # Default variables
    ls_099 = record.get_fields('099')
    ls_subject_class = []
    dc_subject_classification = ''

    # Loop over all found '099'
    for sub_class in ls_099:

        ls_099_subfields = sub_class.get_subfields('a')

        # Cleanup subfields
        for index, subfield in enumerate(ls_099_subfields):
            ls_099_subfields[index] = str(subfield).strip()

        
        # Remove empty results
        ls_099_subfields = list(filter(None,ls_099_subfields))

        # Add if results left
        if len(ls_099_subfields) > 0:
            ls_subject_class.append(" ".join(ls_099_subfields))

    dc_subject_classification = "||".join(ls_subject_class)
    
    return dc_subject_classification


# MARC: 100$a OR 110$ab
# Fields & subfields can REPEAT in record
def get_dc_creator(record):
    # Default variables
    ls_100_110 = record.get_fields('100','110')
    
    ls_creator = []
    dc_creator = ''

    for creator in ls_100_110:
        # Get subfields
        ls_100_110_subfields = []
        ls_100_110_subfields = creator.get_subfields('a','b')

        # Itterate over subfields & clean
        for index, sub in enumerate(ls_100_110_subfields):
            
            removed_trailing_period = cleanup.remove_trailing_period(sub)
            
            # Update value of subfield in list
            ls_100_110_subfields[index] = removed_trailing_period
        

        # Remove empty results
        ls_100_110_subfields = list(filter(None,ls_100_110_subfields))
        
        # Add if results left
        if len(ls_100_110_subfields) > 0:
            ls_creator.append(" ".join(ls_100_110_subfields))
    
    dc_creator = "||".join(ls_creator)

    return dc_creator


# MARC: 245$a$b$c
# Remove punctuation at end, including (/.)
def get_dc_title(record):
    # Default variables
    ls_245 = record.get_fields('245')

    ls_titles = []
    dc_title = ""
    

    for title in ls_245:

        # Get subfields a,b,c
        ls_245_subfields = title.get_subfields('a','b','c')


        # Loop through and cleanup subfields
        for index, subfield in enumerate(ls_245_subfields):
            cleaned_subfield = ""
            cleaned_subfield = str(subfield).strip()

            if cleaned_subfield[-1] in ['.','/']:
                cleaned_subfield = str(cleaned_subfield[0:-1]).strip()
            
            ls_245_subfields[index] = str(cleaned_subfield).strip()

        # Remove empty results
        ls_245_subfields = list(filter(None, ls_245_subfields))
        
        # Add if results left
        if len(ls_245_subfields) > 0:
            ls_titles.append(" ".join(ls_245_subfields))

    dc_title = "||".join(ls_titles)
    
    return dc_title


# MARC: 246$a
# Remove punctuation at end, including /
def get_dc_title_alternative(record):
    # Default variables
    dc_title_alternative = ''

    # Get TITLE ALTERNATIVE
    if record['246'] != None:
        field_246 = record['246']

        if field_246['a'] != None:
            dc_title_alternative = field_246['a']
            dc_title_alternative = dc_title_alternative.strip()

            # Remove trailing [spaces, '.', '/']
            while dc_title_alternative[-1] in ['.','/']:
                dc_title_alternative = dc_title_alternative[0:-1].strip()
    
    return dc_title_alternative


# MARC 255$c or 651$v
def get_dc_coverage(record):
    
    # Default variables
    ls_255_651 = record.get_fields('255','651')
    ls_coverages = []
    dc_coverage = ""

    # Loop over all found '255' and '651' fields
    for coverage in ls_255_651:

        ls_subfields = []
        
        # Get the appropriate subfields depending on field
        if coverage.tag == '255':
            ls_subfields = coverage.get_subfields('c')
        elif coverage.tag == '651':
            ls_subfields = coverage.get_subfields('v')
        
        # Cleanup subfields
        for index, sub in enumerate(ls_subfields):

            cleaned = cleanup.remove_trailing_period(sub)

            ls_subfields[index] = cleaned

        # Remove empty results
        ls_subfields = list(filter(None, ls_subfields)) # remove empty
        
        # Add if results left
        if len(ls_subfields) > 0:
            ls_coverages.append(" ".join(ls_subfields))

    # Combine 'coverage' by double pipe
    dc_coverage = "||".join(ls_coverages)

    return dc_coverage


# MARC: 260$c or 264$c
# Remove punctuation
def get_dc_date_issued(record):
    # Default variables
    ls_260 = record.get_fields('260','264')
    ls_date_issued = []
    dc_date_issued = ''

    # Loop over all found '260' fields
    for date_issued in ls_260:

        ls_260_c = []
        ls_260_c = date_issued.get_subfields('c')

        # Cleanup subfield
        for index, date in enumerate(ls_260_c):
            cleaned = cleanup.only_numbers(date)

            ls_260_c[index] = cleaned

        # Remove empty results
        ls_260_c = list(filter(None,ls_260_c))
        
        # Add to list of dates
        if len(ls_260_c) > 0:
            ls_date_issued.append(" ".join(ls_260_c))

    # Remove duplicates -- incase there are any
    ls_date_issued = list(dict.fromkeys(ls_date_issued))
    
    # Combine 'date_issued' by double pipe
    dc_date_issued = "||".join(ls_date_issued)
    
    return dc_date_issued


# MARC: ???
# TODO
def get_dc_created(record):
    # Default variables
    dc_created = ""

    return dc_created


# MARC: 264$b
# Remove punctuation
def get_dc_publisher(record):
    
    # Default variables
    ls_264 = record.get_fields('264')
    ls_publishers = []
    dc_publisher = ""

    # Loop over all found '264' 
    for publisher in ls_264:
        ls_264_b = []
        ls_264_b = publisher.get_subfields('b')

        # Cleanup subfield
        for index, sub_b in enumerate(ls_264_b):
            cleaned = cleanup.remove_trailing_punctuation(sub_b)

            ls_264_b[index] = cleaned
        
        # Remove empty results
        ls_264_b = list(filter(None,ls_264_b))
        
        # Add to list of publishers
        if len(ls_264_b) > 0:
            ls_publishers.append(" ".join(ls_264_b))

    # Combine 'publishers' by double pipe
    dc_publisher = "||".join(ls_publishers)

    return dc_publisher


# MARC: 300$abc
# Add space between subfields
def get_dc_format_extent(record):
    
    # Default variables
    ls_300 = record.get_fields('300')
    ls_extents = []
    dc_format_extent = ''

    # Loop over all found '300' fields
    for extend in ls_300:

        ls_300_abc = []
        ls_300_abc = extend.get_subfields('a','b','c')

        # Cleanup subfields
        for index, sub in enumerate(ls_300_abc):
            cleaned = cleanup.remove_trailing_punctuation(sub)

            ls_300_abc[index] = cleaned

        # Remove empty results
        ls_300_abc = list(filter(None,ls_300_abc))
        
        # Add to list of publishers
        if len(ls_300_abc) > 0:
            ls_extents.append(" ".join(ls_300_abc))

    # Combine 'extent' by double pipe
    dc_format_extent = "||".join(ls_extents)

    return dc_format_extent


# MARC: 500$a
# REPEAT REPEAT REPEAT
def get_dc_description(record):
    # Default variables
    ls_500 = record.get_fields('500')
    
    ls_notes = []

    dc_description = ''

    for note in ls_500:
        ls_500_a = []
        ls_500_a = note.get_subfields('a')

        for index, sub_a in enumerate(ls_500_a):
            sub_a = str(sub_a)
            
            ls_500_a[index] = sub_a

        # Remove empty results
        ls_500_a = list(filter(None,ls_500_a))

        # Add if results left
        if len(ls_500_a) > 0:
            ls_notes.append(" ".join(ls_500_a))

    dc_description = "||".join(ls_notes)

    return dc_description


# MARC: 600|610|650; ind2: 0-1
# REPEAT REPEAT
# TODO -- needs reformat
def get_dc_subject_lcsh(record):
    # Default variables
    dc_subject_lcsh = ''
    ls_subject_lcsh = []

    # Process applicable fields
    for field in ['600','610','650']:
        ls_fields = record.get_fields(field)

        # Process subfields based on INDICATOR
        for subject in ls_fields:
            # Test ind2
            if subject.indicator2 in ['0','1']:
                
                # Get subfields:
                for sub in ['a','b','v','x','y','z']:
                    results = []
                    if subject[sub] != None:
                        results = subject.get_subfields(sub)
                    
                    # Cleanup subfield
                    for val in results:
                        cleaned = val.strip()
                        if cleaned[-1] == '.':
                            cleaned = cleaned[0:-1].strip()

                        # Add CLEANED subject to list of subjects
                        ls_subject_lcsh.append(cleaned)

    # Join together SUBJECT with double pipe (||)
    if len(ls_subject_lcsh) > 0:
        dc_subject_lcsh = '||'.join(ls_subject_lcsh)
    
    return dc_subject_lcsh


# MARC: 655$a
# REPEAT REPEAT
def get_dc_type(record):
    ls_655 = record.get_fields('655')

    ls_types = []

    dc_type = ""

    # Loop over all found '655' fields
    for map_type in ls_655:

        # Get all occurances of subfield 'a'
        ls_655_a = []
        ls_655_a = map_type.get_subfields('a')

        # Cleanup subfields
        for index, sub_a in enumerate(ls_655_a):
            cleaned = cleanup.remove_trailing_punctuation(sub_a)

            ls_655_a[index] = cleaned
        
        # Remove duplicates
        ls_655_a = list(dict.fromkeys(ls_655_a))
        
        # Remove empty results
        ls_655_a = list(filter(None,ls_655_a))
        
        # Add field to list
        if len(ls_655_a) > 0:
            ls_types.append(" ".join(ls_655_a))
    
    # For all of the '655' found, string together with double pipes
    dc_type = "||".join(ls_types)
    
    return dc_type


# MARC: 700$ad & 710$ab
# REPEAT REPEAT
def get_dc_contributor(record):
    # Default variables
    ls_700_710 = record.get_fields('700','710')
    contributor_subfields = []
    
    ls_contributors = []
    dc_contributor = ''
    
    # Loop over all found '700' & '710' fields
    for contributor in ls_700_710:
        
        # If 700 field get $ad
        if contributor.tag == '700':
            contributor_subfields = contributor.get_subfields('a','d')
        # If 710 field get $ab
        elif contributor.tag == '710':
            contributor_subfields = contributor.get_subfields('a','b')
        
        # Clean up subfields
        for index, subfield in enumerate(contributor_subfields):
            
            cleaned = cleanup.remove_trailing_period(subfield)

            contributor_subfields[index] = cleaned

        # Remove empty results
        contributor_subfields = list(filter(None,contributor_subfields))
        
        # Add if results left
        if len(contributor_subfields) > 0:
            ls_contributors.append(" ".join(contributor_subfields))

    # Join together
    if len(ls_contributors) > 0:
        dc_contributor = '||'.join(ls_contributors)

    return dc_contributor


# MARC: 001
# Bib ID
def get_identifier_other(record):

    # Default variables
    dc_identifier_other = ''

    # Get BIB_ID
    if record['001'] != None:
        dc_identifier_other = str(record['001'].data).strip()

    return dc_identifier_other


