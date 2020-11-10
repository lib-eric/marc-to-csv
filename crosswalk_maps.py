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

    dict_map_fields['filename'] = get_filename(record) # DONE -- 001
    dict_map_fields['dcterms.lcc'] = get_lcc(record) # DONE -- was "dc.subject.lcc"
    dict_map_fields['dcterms.lcsh'] = get_dc_subject_lcsh(record) # DONE -- was "dc.subject.lcsh"
    dict_map_fields['dc.creator'] = get_dc_creator(record) # DONE -- keeping "dc.creator"
    dict_map_fields['dc.title'] = get_dc_title(record) # DONE -- keeping "dc.title"
    dict_map_fields['dc.coverage'] = get_dc_coverage(record) # DONE -- keeping "dc.coverage"
    dict_map_fields['dc.spacial'] = get_dc_spacial(record) # 
    dict_map_fields['dc.date'] = get_dc_date_issued(record) # DONE -- was "dc.date.issued"
    dict_map_fields['dc.publisher'] = get_dc_publisher(record) # DONE -- keeping "dc.publisher"
    dict_map_fields['dcterms.extent'] = get_dc_format_extent(record) # DONE -- was "dc.format.extent"
    dict_map_fields['dc.description'] = get_dc_description(record) # DONE -- keeping "dc.description"
    dict_map_fields['dc.type'] = get_dc_type(record) # DONE -- keeping "dc.type"
    dict_map_fields['dc.contributor'] = get_dc_contributor(record) # DONE -- keeping "dc.contributor"
    dict_map_fields['dc.identifier'] = get_identifier_other(record) # DONE -- was "dc.identifier.other"

    ## Old fields, not using or added elsewhere.
    # dict_map_fields['dc.subject.classification'] = get_dc_subject_classification(record) # DONE -None have
    # dict_map_fields['dc.title.alternative[en]'] = get_dc_title_alternative(record) # Moved to "dc.description"
    # dict_map_fields['dc.date.created'] = get_dc_created(record) # Not really used in maps
    
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
# REPEATABLE REPEATABLE
def get_lcc(record):
    
    # Default variables
    ls_fields = record.get_fields('050','090')
    ls_lcc = []
    dc_lcc = ""

    # Loop through each description field and get their subfields
    for lcc in ls_fields:

        ls_subfields = []

        # Specify condition subfields to extract
        ls_subfields = lcc.get_subfields('a','b')

        # Cleanup -- for each subfield
        for index, subfield in enumerate(ls_subfields):
            
            str_subfield = ""
            str_subfield = cleanup.str_convert_trimmed(subfield)
            
            # Update value index
            ls_subfields[index] = str_subfield
        
        # Cleanup -- remove duplicates and remove empty
        ls_subfields = cleanup.list_remove_duplicates(ls_subfields)
        ls_subfields = cleanup.list_remove_empty(ls_subfields)
        
        # Add if results left
        # Tie together subfields with field delimiter
        if len(ls_subfields) > 0:
            ls_lcc.append(" ".join(ls_subfields))
    
    # Cleanup -- remove duplicates and remove empty
    ls_lcc = cleanup.list_remove_duplicates(ls_lcc)
    ls_lcc = cleanup.list_remove_empty(ls_lcc)

    # Tie together with field delimiter
    if len(ls_lcc) > 0:
        dc_lcc = "||".join(ls_lcc)
    
    return dc_lcc


# MARC: 099$aaa
def get_dc_subject_classification(record):
    
    # Default variables
    ls_fields = record.get_fields('099')
    ls_subject_class = []
    dc_subject_classification = ''

    # Loop through each description field and get their subfields
    for subject_class in ls_fields:

        ls_subfields = []

        # Specify condition subfields to extract
        ls_subfields = subject_class.get_subfields('a')

        # Cleanup -- for each subfield
        for index, subfield in enumerate(ls_subfields):
            
            str_subfield = ""

            # Cleanup
            str_subfield = cleanup.str_convert_trimmed(subfield)

            # Update value index
            ls_subfields[index] = str_subfield

        
        # Cleanup -- remove duplicates and remove empty
        ls_subfields = cleanup.list_remove_duplicates(ls_subfields)
        ls_subfields = cleanup.list_remove_empty(ls_subfields)

        # Add if results left
        # Tie together subfields with field delimiter
        if len(ls_subfields) > 0:
            ls_subject_class.append(" ".join(ls_subfields))

    # Cleanup -- remove duplicates and remove empty
    ls_subject_class = cleanup.list_remove_duplicates(ls_subject_class)
    ls_subject_class = cleanup.list_remove_empty(ls_subject_class)

    # Tie together with field delimiter
    if len(ls_subject_class) > 0:
        dc_subject_classification = "||".join(ls_subject_class)
    
    return dc_subject_classification


# MARC: 600|610|650; ind2: 0-1
# REPEAT REPEAT
def get_dc_subject_lcsh(record):
    
    # Default variables
    ls_fields = record.get_fields('600','610','650')
    dc_subject_lcsh = ''
    ls_subject_lcsh = []

    # Loop through each description field and get their subfields
    for subject_lcsh in ls_fields:

        ls_subfields = []

        # Specify condition subfields to extract
        ls_subfields = subject_lcsh.get_subfields('a','b','v','x','y','z')

        # Cleanup -- for each subfield
        for index, subfield in enumerate(ls_subfields):
            str_subfield = ""

            if subject_lcsh.indicator2 in ['0','1']:

                str_subfield = cleanup.str_convert_trimmed(subfield)
                str_subfield = cleanup.remove_trailing_period(subfield)

            ls_subfields[index] = str_subfield


        # Cleanup -- remove duplicates and remove empty
        ls_subfields = cleanup.list_remove_duplicates(ls_subfields)
        ls_subfields = cleanup.list_remove_empty(ls_subfields)

        # Add if results left
        # Tie together subfields with field delimiter
        if len(ls_subfields) > 0:
            ls_subject_lcsh.append(" ".join(ls_subfields))

    # Cleanup -- remove duplicates and remove empty
    ls_subject_lcsh = cleanup.list_remove_duplicates(ls_subject_lcsh)
    ls_subject_lcsh = cleanup.list_remove_empty(ls_subject_lcsh)

    # Tie together with field delimiter
    if len(ls_subject_lcsh) > 0:
        dc_subject_lcsh = "||".join(ls_subject_lcsh)
    
    return dc_subject_lcsh


# MARC: 100$a OR 110$ab
# Fields & subfields can REPEAT in record
# 110$b REPEATABLE REPEATABLE
def get_dc_creator(record):
    
    # Default variables
    ls_fields = record.get_fields('100','110')
    ls_creator = []
    dc_creator = ''

    for creator in ls_fields:
        
        ls_subfields = []

        # Specify condition subfields to extract
        if creator.tag == '100':
            ls_subfields = creator.get_subfields('a')
        elif creator.tag == '110':
            ls_subfields = creator.get_subfields('a','b')

        # Cleanup -- for each subfield
        for index, subfield in enumerate(ls_subfields):

            str_subfield = ''
            str_subfield = cleanup.str_convert_trimmed(subfield)

            # Cleanup -- Remove trailing period
            str_subfield = cleanup.remove_trailing_period(str_subfield)
            
            # Update value index
            ls_subfields[index] = str_subfield
        

        # Cleanup -- remove duplicates and remove empty
        ls_subfields = cleanup.list_remove_duplicates(ls_subfields)
        ls_subfields = cleanup.list_remove_empty(ls_subfields)
        
        # Add if results left
        # Tie together subfields with field delimiter
        if len(ls_subfields) > 0:
            ls_creator.append(" ".join(ls_subfields))
    
    # Cleanup -- remove duplicates and remove empty
    ls_creator = cleanup.list_remove_duplicates(ls_creator)
    ls_creator = cleanup.list_remove_empty(ls_creator)
    
    # Tie together with field delimiter
    if len(ls_creator) > 0:
        dc_creator = "||".join(ls_creator)

    return dc_creator


# MARC: 245$abc
# Remove punctuation at end, including (/.)
def get_dc_title(record):
    
    # Default variables
    ls_fields = record.get_fields('245')
    ls_titles = []
    dc_title = ""
    
    # Loop through each description field and get their subfields
    for title in ls_fields:
        
        ls_subfields = []

        # Specify condition subfields to extract
        ls_subfields = title.get_subfields('a','b','c')

        # Cleanup -- for each subfield
        for index, subfield in enumerate(ls_subfields):
            str_subfield = ""

            str_subfield = cleanup.str_convert_trimmed(subfield)

            if " :" in str_subfield:
                str_subfield = str_subfield.replace(" :", ":")
            
            # Update value index
            ls_subfields[index] = str_subfield

        # Cleanup -- remove duplicates and remove empty
        ls_subfields = cleanup.list_remove_duplicates(ls_subfields)
        ls_subfields = cleanup.list_remove_empty(ls_subfields)
        
        # Add if results left
        # Tie together subfields with field delimiter
        if len(ls_subfields) > 0:
            ls_titles.append(" ".join(ls_subfields))

    # Cleanup -- remove duplicates and remove empty
    ls_titles = cleanup.list_remove_duplicates(ls_titles)
    ls_titles = cleanup.list_remove_empty(ls_titles)

    # Tie together with field delimiter
    if len(ls_titles) > 0:
        dc_title = "||".join(ls_titles)
    
    return dc_title


# MARC: 246$all
# REPEATABLE REPEATABLE
def get_dc_title_alternative(record):
    
    # Default variables
    ls_fields = record.get_fields('246')
    ls_title_alternative = []
    dc_title_alternative = ''

    # Loop through each description field and get their subfields
    for title_alternative in ls_fields:
        
        ls_subfields = []
        ls_subfields = title_alternative.get_subfields('a','b','f','g','h','i')

        # Cleanup -- for each subfield
        for index, subfield in enumerate(ls_subfields):

            str_subfield = ""

            str_subfield = cleanup.str_convert_trimmed(subfield)

            if " :" in str_subfield:
                str_subfield = str_subfield.replace(" :", ":")
            
            # Update value index
            ls_subfields[index] = str_subfield
        
        # Cleanup -- remove duplicates and remove empty
        ls_subfields = cleanup.list_remove_duplicates(ls_subfields)
        ls_subfields = cleanup.list_remove_empty(ls_subfields)

        # Add if results left
        # Tie together subfields with field delimiter
        if len(ls_subfields) > 0:
            ls_title_alternative.append(" ".join(ls_subfields))
        
    # Cleanup -- remove duplicates and remove empty
    ls_title_alternative = cleanup.list_remove_duplicates(ls_title_alternative)
    ls_title_alternative = cleanup.list_remove_empty(ls_title_alternative)

    # Tie together with field delimiter
    if len(ls_title_alternative) > 0:
        dc_title_alternative = "||".join(ls_title_alternative)
    
    return dc_title_alternative


# MARC 651$v
def get_dc_coverage(record):
    
    # Default variables
    ls_fields = record.get_fields('651')
    ls_coverages = []
    dc_coverage = ""

    # Loop through fields.
    for coverage in ls_fields:

        ls_subfields = []
        
        # Get the appropriate subfields depending on field.
        if coverage.tag == '651':
            ls_subfields = coverage.get_subfields('a','v','x','z')
        
        # Cleanup subfields
        for index, subfield in enumerate(ls_subfields):
            
            str_subfield = ""
            str_subfield = cleanup.str_convert_trimmed(subfield)

            # Cleanup -- Remove trailing period
            str_subfield = cleanup.remove_trailing_period(str_subfield)
            
            # Update value index
            ls_subfields[index] = str_subfield

        # Cleanup -- remove duplicates and remove empty
        ls_subfields = cleanup.list_remove_duplicates(ls_subfields)
        ls_subfields = cleanup.list_remove_empty(ls_subfields)
        
        # Add if results left
        # Tie together subfields with field delimiter
        if len(ls_subfields) > 0:
            ls_coverages.append("--".join(ls_subfields))

    # Cleanup -- remove duplicates and remove empty
    ls_coverages = cleanup.list_remove_duplicates(ls_coverages)
    ls_coverages = cleanup.list_remove_empty(ls_coverages)
    
    # Tie together with field delimiter
    if len(ls_coverages) > 0:
        dc_coverage = "||".join(ls_coverages)

    return dc_coverage


# MARC 255$c
def get_dc_spacial(record):
    
    # Default variables.
    ls_fields = record.get_fields('255')
    ls_spacial = []
    dc_spacial = ""

    # Loop through fields.
    for spacial in ls_fields:

        ls_subfields = []

        # Get the appropriate subfields depending on field.
        if spacial.tag == '255':
            ls_subfields = spacial.get_subfields('c')
        
        # Cleanup subfields.
        for index, subfield in enumerate(ls_subfields):

            str_subfield = ""
            str_subfield = cleanup.str_convert_trimmed(subfield)

            # Cleanup -- remove trailing period.
            str_subfield = cleanup.remove_trailing_period(str_subfield)

            # Update value index.
            ls_subfields[index] = str_subfield

        # Cleanup -- remove duplicates and remove empty.
        ls_subfields = cleanup.list_remove_duplicates(ls_subfields)
        ls_subfields = cleanup.list_remove_empty(ls_subfields)
        
        # Add if results left.
        # To together subfields with field delimiter
        if len(ls_subfields) > 0:
            ls_spacial.append("--".join(ls_subfields))

    # Cleanup -- remove duplicates and remove empty.
    ls_spacial = cleanup.list_remove_duplicates(ls_spacial)
    ls_spacial = cleanup.list_remove_empty(ls_spacial)
    
    # Tie together with field delimiter.
    if len(ls_spacial) > 0:
        dc_spacial = "||".join(ls_spacial)
    
    return dc_spacial


# MARC: 260$c or 264$c
# Remove punctuation
def get_dc_date_issued(record):
    
    # Default variables
    ls_fields = record.get_fields('260','264')
    ls_date_issued = []
    dc_date_issued = ''

    # Loop through each description field and get their subfields
    for date_issued in ls_fields:

        ls_subfields = []
        # Specify condition subfields to extract
        ls_subfields = date_issued.get_subfields('c')

        # Cleanup subfield
        for index, subfield in enumerate(ls_subfields):
            
            str_subfield = ""
            
            str_subfield = cleanup.str_convert_trimmed(subfield)
            
            # str_subfield = cleanup.only_numbers(subfield)
            
            # Update value index
            ls_subfields[index] = str_subfield

        # Cleanup -- remove duplicates and remove empty
        ls_subfields = cleanup.list_remove_duplicates(ls_subfields)
        ls_subfields = cleanup.list_remove_empty(ls_subfields)

        # Add if results left
        # Tie together subfields with field delimiter
        if len(ls_subfields) > 0:
            ls_date_issued.append(" ".join(ls_subfields))

    # Cleanup -- remove duplicates and remove empty
    ls_date_issued = cleanup.list_remove_duplicates(ls_date_issued)
    ls_date_issued = cleanup.list_remove_empty(ls_date_issued)
    
    # Tie together with field delimiter
    if len(ls_date_issued) > 0:
        dc_date_issued = "||".join(ls_date_issued)
    
    return dc_date_issued


# MARC: 264$b
# Remove punctuation
def get_dc_publisher(record):
    
    # Default variables
    ls_fields = record.get_fields('264')
    ls_publishers = []
    dc_publisher = ""

    # Loop through each description field and get their subfields
    for publisher in ls_fields:
        
        ls_subfields = []

        # Specify condition subfields to extract
        ls_subfields = publisher.get_subfields('b')

        # Cleanup -- for each subfield
        for index, subfield in enumerate(ls_subfields):
            
            str_subfield = ""
            str_subfield = cleanup.str_convert_trimmed(subfield)
            
            # str_subfield = cleanup.remove_trailing_punctuation(str_subfield)
            
            # Update value index
            ls_subfields[index] = str_subfield
        
        # Cleanup -- remove duplicates and remove empty
        ls_subfields = cleanup.list_remove_duplicates(ls_subfields)
        ls_subfields = cleanup.list_remove_empty(ls_subfields)

        # Add if results left
        # Tie together subfields with field delimiter
        if len(ls_subfields) > 0:
            ls_publishers.append(" ".join(ls_subfields))

    # Cleanup -- remove duplicates and remove empty
    ls_publishers = cleanup.list_remove_duplicates(ls_publishers)
    ls_publishers = cleanup.list_remove_empty(ls_publishers)
    
    # Tie together with field delimiter
    if len(ls_publishers) > 0:
        dc_publisher = "||".join(ls_publishers)

    return dc_publisher


# MARC: 300$abc
# Add space between subfields
def get_dc_format_extent(record):
    
    # Default variables
    ls_fields = record.get_fields('300')
    ls_format_extents = []
    dc_format_extent = ''

    # Loop through each description field and get their subfields
    for extend in ls_fields:

        ls_subfields = []

        # Specify condition subfields to extract
        ls_subfields = extend.get_subfields('a','b','c')

        # Cleanup -- for each subfield
        for index, subfield in enumerate(ls_subfields):
            
            str_subfield = ""
            
            str_subfield = cleanup.str_convert_trimmed(subfield)
            
            str_subfield = cleanup.remove_trailing_punctuation(str_subfield)

            ls_subfields[index] = str_subfield

        # Cleanup -- remove duplicates and remove empty
        ls_subfields = cleanup.list_remove_duplicates(ls_subfields)
        ls_subfields = cleanup.list_remove_empty(ls_subfields)

        # Add if results left
        # Tie together subfields with field delimiter
        if len(ls_subfields) > 0:
            ls_format_extents.append(" ".join(ls_subfields))

    # Cleanup -- remove duplicates and remove empty
    ls_format_extents = cleanup.list_remove_duplicates(ls_format_extents)
    ls_format_extents = cleanup.list_remove_empty(ls_format_extents)
    
    # Tie together with field delimiter
    if len(ls_format_extents) > 0:
        dc_format_extent = "||".join(ls_format_extents)

    return dc_format_extent


# MARC: 500$all, 505$all, 550$all, 255$ab
# No dc.title.alternative option in Fedora so include MARC: 246
# MARC: 246$all
# REPEAT REPEAT REPEAT
def get_dc_description(record):
    
    # Default variables
    ls_fields = record.get_fields('246', '255', '500', '505', '550')
    ls_description = []
    dc_description = ''

    # Loop through each description field and get their subfields
    for description in ls_fields:
        
        ls_subfields = []

        # Specify condition subfields to extract
        if description.tag == '255':
            ls_subfields = description.get_subfields('a','b')
        elif description.tag == '246':
            ls_subfields = description.get_subfields('a','b')
        else:
            ls_subfields = description.get_subfields('a') # Gets all subfields

        # Cleanup -- for each subfield
        for index, subfield in enumerate(ls_subfields):
            str_subfield = ""

            str_subfield = cleanup.str_convert_trimmed(subfield)
            
            if " :" in str_subfield:
                str_subfield = str_subfield.replace(" :", ":").strip()


            # Cleanup -- Remove trailing period
            str_subfield = cleanup.remove_trailing_period(str_subfield)
            # Update value index
            ls_subfields[index] = str_subfield

        # Cleanup -- remove duplicates and remove empty
        ls_subfields = cleanup.list_remove_duplicates(ls_subfields)
        ls_subfields = cleanup.list_remove_empty(ls_subfields)

        # Add if results left
        # Tie together subfields with field delimiter
        if len(ls_subfields) > 0:
            ls_description.append(" ".join(ls_subfields))
            print(ls_description)

    # Cleanup -- remove duplicates and remove empty
    ls_description = cleanup.list_remove_duplicates(ls_description)
    ls_description = cleanup.list_remove_empty(ls_description)

    # Tie together with field delimiter
    if len(ls_description) > 0:
        dc_description = "||".join(ls_description)
        print(dc_description)

    return dc_description


# MARC: 655$a
# REPEAT REPEAT
def get_dc_type(record):
    
    # Default variables
    ls_fields = record.get_fields('655')
    ls_types = []
    dc_type = ""

    # Loop through each description field and get their subfields
    for map_type in ls_fields:

        ls_subfields = []

        # Specify condition subfields to extract
        ls_subfields = map_type.get_subfields('a')

        # Cleanup -- for each subfield
        for index, subfield in enumerate(ls_subfields):
            str_subfield = ""

            str_subfield = cleanup.remove_trailing_punctuation(subfield)

            # Update value index
            ls_subfields[index] = str_subfield

        # Cleanup -- remove duplicates and remove empty
        ls_subfields = cleanup.list_remove_duplicates(ls_subfields)
        ls_subfields = cleanup.list_remove_empty(ls_subfields)

        # Add if results left
        # Tie together subfields with field delimiter
        if len(ls_subfields) > 0:
            ls_types.append(" ".join(ls_subfields))

    # Cleanup -- remove duplicates and remove empty
    ls_types = cleanup.list_remove_duplicates(ls_types)
    ls_types = cleanup.list_remove_empty(ls_types)
    
    # Tie together with field delimiter
    if len(ls_types) > 0:
        dc_type = "||".join(ls_types)
    
    return dc_type


# MARC: 700$ad & 710$ab
# REPEAT REPEAT
def get_dc_contributor(record):
    
    # Default variables
    ls_fields = record.get_fields('700','710')
    ls_contributors = []
    dc_contributor = ''
    
    # Loop through each description field and get their subfields
    for contributor in ls_fields:

        ls_subfields = []

        # Specify condition subfields to extract
        if contributor.tag == '700':
            ls_subfields = contributor.get_subfields('a','d')
        elif contributor.tag == '710':
            ls_subfields = contributor.get_subfields('a','b')
        
        # Cleanup -- for each subfield
        for index, subfield in enumerate(ls_subfields):
            
            cleaned = cleanup.remove_trailing_period(subfield)
            
            # Update value index
            ls_subfields[index] = cleaned

        # Cleanup -- remove duplicates and remove empty
        ls_subfields = cleanup.list_remove_duplicates(ls_subfields)
        ls_subfields = cleanup.list_remove_empty(ls_subfields)

        # Add if results left
        # Tie together subfields with field delimiter
        if len(ls_subfields) > 0:
            ls_contributors.append(" ".join(ls_subfields))

    # Cleanup -- remove duplicates and remove empty
    ls_contributors = cleanup.list_remove_duplicates(ls_contributors)
    ls_contributors = cleanup.list_remove_empty(ls_contributors)
    
    # Tie together with field delimiter
    if len(ls_contributors) > 0:
        dc_contributor = "||".join(ls_contributors)

    return dc_contributor


# MARC: 001
# Bib ID
def get_identifier_other(record):

    # Default variables
    # ls_fields = record.get_fields('001')
    dc_identifier_other = ''

    # Get BIB_ID
    if record['001'] != None:
        dc_identifier_other = str(record['001'].data).strip()

    return dc_identifier_other

