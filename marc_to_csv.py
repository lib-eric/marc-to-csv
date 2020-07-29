# MARC processing/extraction
import pymarc
from pymarc import MARCReader
from pymarc import marc8_to_unicode
# CSV creation and writing
import os
from pathlib import Path
import csv


# Start
def process_marc(extract_from=None, save_name=None):
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
    if not output_name:
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
    dissertation_fields = {}

    dissertation_fields['filename'] = get_filename(record)
    dissertation_fields['dc.subject.classification'] = get_dc_subject_classification(record)
    dissertation_fields['dc.creator'] = get_dc_creator(record)
    dissertation_fields['dc.title'] = get_dc_title(record)
    dissertation_fields['dc.title.alternative'] = get_dc_title_alternative(record)
    dissertation_fields['dc.date.issued'] = get_dc_date_issued(record)
    dissertation_fields['dc.format.extent'] = get_dc_format_extent(record)
    dissertation_fields['dc.description'] = get_dc_description(record)
    dissertation_fields['dc.description.abstract'] = get_dc_description_abstract(record)
    dissertation_fields['thesis.degree.name'] = get_thesis_degree_name(record)
    dissertation_fields['thesis.degree.level'] = get_thesis_degree_level(record)
    dissertation_fields['thesis.degree.decipline'] = get_thesis_degree_discipline(record)
    dissertation_fields['dc.subject'] = get_dc_subject(record)
    dissertation_fields['dc.subject.mesh'] = get_dc_subject_mesh(record)
    dissertation_fields['dc.subject.nalt'] = get_dc_subject_nalt(record)
    dissertation_fields['dc.subject.lcsh'] = get_dc_subject_lcsh(record)
    dissertation_fields['dc.contributor.committeeMember'] = get_contributor_committeemember(record)
    dissertation_fields['dc.contributor.advisor'] = get_contributor_advisor(record)
    dissertation_fields['handle'] = get_handle(record)
    dissertation_fields['dc.identifier.other'] = get_identifier_other(record)
    
    return dissertation_fields



# MARC: 001
# Add ".pdf" to end
def get_filename(record):
    filename = ''

    # Get FILENAME
    if record['001'] != None:
        # FILENAME standard is to use the id = 001 and append '.pdf' as the filename
        filename = '{id}.pdf'.format(id=str(record['001'].data).strip())
    
    return filename



# MARC: 099
def get_dc_subject_classification(record):
    dc_subject_classification = ''
    ls_subfields = ''

    # Get SUBJECT CLASSIFICATION
    if record['099'] != None:

        # dc_subject_classification = str(record['099']).strip()
        ls_subfields = record['099'].get_subfields('a')

        if len(ls_subfields) > 0:
            for subfield in ls_subfields:
                subfield = subfield.strip()
        
        # Join together SUBFIELDS with spaces
        dc_subject_classification = ' '.join(ls_subfields)

        # Some records have 'Disseration' split weirdly; cleanup
        if "Disser- tation" in dc_subject_classification:
            dc_subject_classification = dc_subject_classification.replace('Disser- tation', 'Dissertation')
    
    return dc_subject_classification



# MARC: 100$a
# REPEAT REPEAT
def get_dc_creator(record):
    # Default variables
    dc_creator = ''
    ls_100 = []
    ls_creator = []

    # Check if there is 100 field in record, if so get all and put into list
    if record['100'] != None:
        ls_100 = record.get_fields('100')
    
    # Loop through the 100 fields
    for person in ls_100:
        initial_name = person['a'].strip()

        # If last character is ',' remove it
        if initial_name[-1] == ',' or '.':
            formatted_name = initial_name[0:-1].strip()

        ls_creator.append(formatted_name)

    # Join together CREATOR(S) with double pipe (||) if there are multiple
    if len(ls_creator) > 0:
        dc_creator = '||'.join(ls_creator)

    return dc_creator



# MARC: 245$a$b
# Remove punctuation at end, including /
def get_dc_title(record):
    # Default variables
    title_a = ''
    title_b = ''
    dc_title = ''

    # Get TITLE$a
    if record['245'] != None:
        title_a = record['245']['a']
        title_a = title_a.strip()

        # Remove trailing [spaces, '.', '/']
        while title_a[-1] in ['.','/']:
            title_a = title_a[0:-1].strip()
        
        # Get TITLE$b
        if record['245']['b'] != None:
            title_b = str(record['245']['b']).strip()

            # Remove trailing [spaces, '.', '/']
            while title_b[-1] in ['.','/']:
                title_b = title_b[0:-1].strip()
    
    # Combine together the two
    dc_title = title_a + ' ' + title_b
    
    return dc_title



# MARC: 246$a
# Remove punctuation at end, including /
def get_dc_title_alternative(record):
    # Default variables
    dc_title_alternative = ''

    # Get TITLE ALTERNATIVE
    if record['246'] != None:
        dc_title_alternative = record['246']['a']
        dc_title_alternative = dc_title_alternative.strip()

        # Remove trailing [spaces, '.', '/']
        while dc_title_alternative[-1] in ['.','/']:
            dc_title_alternative = dc_title_alternative[0:-1].strip()
    
    return dc_title_alternative



# MARC: 260$c
# Remove punctuation
def get_dc_date_issued(record):
    # Default variables
    dc_date_issued = ''

    # Get DATE ISSUED - Check 260 first
    if record['260'] != None:
        dc_date_issued = record['260']['c']
        dc_date_issued = dc_date_issued.strip()

        # Remove trailing [spaces, '.', '/']
        while dc_date_issued[-1] in ['.','/']:
            dc_date_issued = dc_date_issued[0:-1].strip()
    
    # Get DATE ISSUED - Check 260 first
    if record['264'] != None:
        dc_date_issued = record['264']['c']

        # Remove trailing [spaces, '.', '/']
        while dc_date_issued[-1] in ['.','/']:
            dc_date_issued = dc_date_issued[0:-1].strip()
    
    return dc_date_issued



# MARC: 300$a
def get_dc_format_extent(record):
    # Default variables
    dc_format_extent = ''

    # Get FORMAT EXTENT
    if record['300'] != None:
        dc_format_extent = record['300']['a']
        dc_format_extent = dc_format_extent.strip()

        # Remove trailing [spaces, '.', '/']
        while dc_format_extent[-1] in ['.','/']:
            dc_format_extent = dc_format_extent[0:-1].strip()
        
        # Remove ' :'
        if ' :' in dc_format_extent:
            dc_format_extent = dc_format_extent.replace(' :', '')
    
    return dc_format_extent



# MARC: 500$a
def get_dc_description(record):
    # Default variables
    dc_description = ''

    # Get DESCRIPTION
    if record['500'] != None:
        dc_description = record['500']['a']
        dc_description = dc_description.strip()
    
    return dc_description



# MARC: 520
def get_dc_description_abstract(record):
    # Default variables
    dc_description_abstract = ''

    # Get DESCRIPTION ABSTRACT
    if record['520'] != None:
        dc_description_abstract = record['520']['a']
    
    return dc_description_abstract



# MARC: 502$b
# Will be either Doctoral|Masters|Bachelors in/of [field name]
def get_thesis_degree_name(record):
    # Default variables
    thesis_degree_name = ''

    # Get DEGREE TYPE
    if record['502'] != None:
        field_502a = record['502']['b']
        field_502a = field_502a.strip()

        if field_502a[-1] == '.':
            field_502a = field_502a[0:-1]
        
        thesis_degree_name = field_502a
    
    return thesis_degree_name



# MARC: 502$b
# Will be Doctoral, Masters, or Bachelor
def get_thesis_degree_level(record):
    # Default variables
    thesis_degree_level = ''

    # Get DEGREE LEVEL
    if record['502'] != None:
        field_502a = record['502']['b']

        if " in " in field_502a:
            # "{type part} in {department}" -- grabs the {type part}
            type_part_extract = field_502a[0:field_502a.find(" in ")]

            lower = type_part_extract.lower()

            # Doctorial/Ph.D
            if lower in ["ph. d", "ph. d.", "ph.d.", "ph d"]:
                thesis_degree_level = 'Doctorial'
            # Master
            elif lower in ['master']:
                thesis_degree_level = 'Master'
            # Bachelor
            elif lower in ['bachelor']:
                thesis_degree_level = 'Bachelor'
    
    return thesis_degree_level



# MARC: 502$b
# Name of department
def get_thesis_degree_discipline(record):
    # Default variables
    thesis_degree_discipline = ''

    # Get DEGREE DISCIPLINE
    if record['502'] != None:
        field_502a = record['502']['b']

        if " in " in field_502a:
            thesis_degree_discipline = field_502a[field_502a.find(" in ")+4:]

    return thesis_degree_discipline



# MARC: 600|610|650; ind2: 4-7
# REPEAT REPEAT
def get_dc_subject(record):
    # Default variables
    dc_subject = ''
    ls_subject = []

    for field in ['600','610','650']:
        ls_fields = record.get_fields(field)

        # Process subfields based on INDICATOR
        for subject in ls_fields:
            # Test ind2
            if subject.indicator2 in ['4', '5', '6', '7']:
                
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
                        ls_subject.append(cleaned)


    # Join together SUBJECT with double pipe (||)
    if len(ls_subject) > 0:
        dc_subject = '||'.join(ls_subject)

    return dc_subject



# MARC: 600|610|650; ind2: 2
# REPEAT REPEAT
def get_dc_subject_mesh(record):
    # Default variables
    dc_subject_mesh = ''
    ls_subject_mesh = []

    # Process applicable fields
    for field in ['600','610','650']:
        ls_fields = record.get_fields(field)

        # Process subfields based on INDICATOR
        for subject in ls_fields:
            # Test ind2
            if subject.indicator2 in ['2']:
                
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
                        ls_subject_mesh.append(cleaned)

    # Join together SUBJECT with double pipe (||)
    if len(ls_subject_mesh) > 0:
        dc_subject_mesh = '||'.join(ls_subject_mesh)
    
    return dc_subject_mesh



# MARC: 600|610|650; ind2: 3
# REPEAT REPEAT
def get_dc_subject_nalt(record):
    # Default variables
    dc_subject_nalt = ''
    ls_subject_nalt = []

    # Process applicable fields
    for field in ['600','610','650']:
        ls_fields = record.get_fields(field)

        # Process subfields based on INDICATOR
        for subject in ls_fields:
            # Test ind2
            if subject.indicator2 in ['3']:
                
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
                        ls_subject_nalt.append(cleaned)

    # Join together SUBJECT with double pipe (||)
    if len(ls_subject_nalt) > 0:
        dc_subject_nalt = '||'.join(ls_subject_nalt)
    
    return dc_subject_nalt



# MARC: 600|610|650; ind2: 0-1
# REPEAT REPEAT
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



# MARC: 700$a
# REPEAT REPEAT
def get_contributor_committeemember(record):
    # Default variables
    dc_contributor_committeeMember = ''
    ls_700 = []
    ls_committee_member = []

    # Check if there is 700 field in record, if so get all and put into list
    if record['700'] != None:
        ls_700 = record.get_fields('700')
    
    # Loop through the 700 fields and grab names if RELATOR TERM ($e) has 'committee member'
    for person in ls_700:
        if person['e'] != None:
            lower_case_relator = str(person['e']).lower()
            if 'committee member' in lower_case_relator:
                initial_name = person['a'].strip()

                # If last character is ',' remove it
                if initial_name[-1] == ',':
                    formatted_name = initial_name[0:-1].strip()
                ls_committee_member.append(formatted_name)

    # Join together COMMITTEE_MEMBERS with double pipe (||) if there are multiple
    if len(ls_committee_member) > 0:
        dc_contributor_committeeMember = '||'.join(ls_committee_member)

    return dc_contributor_committeeMember



# MARC: 700$a
# REPEAT REPEAT
def get_contributor_advisor(record):
    # Default variables
    dc_contributor_advisor = ''
    ls_700 = []
    ls_advisor = []

    # Check if there is 700 field in record, if so get all and put into list
    if record['700'] != None:
        ls_700 = record.get_fields('700')
    
    # Loop through the 700 fields and grab names if RELATOR TERM ($e) has 'supervisor'
    for person in ls_700:
        if person['e'] != None:
            lower_case_relator = person['e'].lower()
            if 'advisor' in lower_case_relator or 'supervisor' in lower_case_relator:
                initial_name = person['a'].strip()

                # If last character is ',' remove it
                if initial_name[-1] == ',':
                    formatted_name = initial_name[0:-1].strip()
                ls_advisor.append(formatted_name)

    # Join together SUPERVISOR(S) with double pipe (||) if there are multiple
    if len(ls_advisor) > 0:
        dc_contributor_advisor = '||'.join(ls_advisor)

    return dc_contributor_advisor



# MARC: 856$u
def get_handle(record):
    # Default variables
    handle = ''
    ls_856 = []

    # Check if there is 856 field in record, if so get all and put into list
    if record['856'] != None:
        ls_856 = record.get_fields('856')
    
    # Loop through the 856 fields and grab url if HANDLE link
    for url in ls_856:
        if 'hdl.handle.net' in url['u']:
            handle = url['u'].strip()
            
            # Uppercase 'dissertation'
            if 'dissertations' or 'Dissertations' in handle:
                handle = handle.replace('Dissertations', 'DISSERTATIONS')

    return handle



# MARC: 001
# Voyager Bib... or ends up being OCLC if exporting from OCLC
def get_identifier_other(record):
    # Default variables
    dc_identifier_other = ''

    # Check if there is 001 field in record
    if record['001'] != None:
        id = record['001']
        dc_identifier_other = str(id).strip()

    return dc_identifier_other



#################################################



print("Welcome to 'Marc to CSV'")

# Get INPUT from user for {path to file}
input_file = input("Input the path and filename with extension to a Binary MARC file (*.bib, *.dat):")
# Get INPUT from user for {output file name}
input_output_name = input("Give the output file a name (eg. output.csv):")

# Run
process_marc(extract_from=input_file, save_name=input_output_name)